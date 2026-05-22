"""
Sistem Akreditasi RS
Developer-grade upgrade: rate limiting, pagination, notifications,
profile management, activity feed, password change, advanced search.
"""
import os, sqlite3, uuid, json, hashlib, secrets, csv, io, logging, math
from datetime import datetime, timedelta, timezone
UTC = timezone.utc


from pathlib import Path
from functools import wraps
from collections import defaultdict

from flask import (Flask, flash, g, redirect, render_template, request,
                   send_from_directory, session, url_for, jsonify, abort, Response)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

BASE_DIR   = Path(__file__).resolve().parent
DB_PATH    = BASE_DIR / "akreditasi.db"
UPLOAD_DIR = BASE_DIR / "uploads"
LOG_DIR    = BASE_DIR / "logs"

ALLOWED_EXTENSIONS = {"pdf","doc","docx","xls","xlsx","ppt","pptx","txt","jpg","jpeg","png","zip","rar"}
PER_PAGE           = 15
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_SECONDS    = 300   # 5 menit

LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ── In-memory brute force tracker ────────────────────────────────────────────
_login_attempts: dict = defaultdict(lambda: {"count": 0, "until": 0})


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", secrets.token_hex(32)),
        MAX_CONTENT_LENGTH=50 * 1024 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
    )
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # ── Jinja2 global: csrf_token() bisa dipanggil dari semua template ──
    @app.context_processor
    def inject_csrf():
        def csrf_token():
            if "_csrf" not in session:
                session["_csrf"] = secrets.token_hex(16)
            return session["_csrf"]
        return dict(csrf_token=csrf_token)

    @app.before_request
    def before_request():
        g.db   = get_db_connection()
        g.user = get_current_user()

    @app.teardown_request
    def teardown_request(_exc=None):
        db = getattr(g, "db", None)
        if db:
            db.close()

    @app.after_request
    def security_headers(resp):
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"]         = "SAMEORIGIN"
        resp.headers["X-XSS-Protection"]        = "1; mode=block"
        resp.headers["Referrer-Policy"]         = "strict-origin-when-cross-origin"
        return resp

    # ── Auth ──────────────────────────────────────────────────────────────────
    @app.route("/")
    @login_required
    def index():
        return redirect(url_for("dashboard"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if g.user:
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            username = request.form.get("username", "").strip().lower()
            password = request.form.get("password", "")
            ip       = request.remote_addr

            # Brute force check
            rec = _login_attempts[ip]
            now = datetime.now(UTC).timestamp()
            if rec["count"] >= MAX_LOGIN_ATTEMPTS and now < rec["until"]:
                remaining = int(rec["until"] - now)
                flash(f"Terlalu banyak percobaan login. Coba lagi dalam {remaining} detik.", "danger")
                return render_template("login.html")

            row = g.db.execute(
                "SELECT id,username,full_name,role,password_hash,active FROM users WHERE lower(username)=?",
                (username,)).fetchone()

            if not row or not check_password_hash(row["password_hash"], password):
                rec["count"] += 1
                if rec["count"] >= MAX_LOGIN_ATTEMPTS:
                    rec["until"] = now + LOCKOUT_SECONDS
                _audit("LOGIN_FAILED", None, f"user={username} ip={ip}")
                flash("Username atau password salah.", "danger")
                return render_template("login.html")

            if int(row["active"]) != 1:
                flash("Akun Anda telah dinonaktifkan. Hubungi administrator.", "danger")
                return render_template("login.html")

            # Reset on success
            _login_attempts[ip] = {"count": 0, "until": 0}
            session.permanent = True
            session["user_id"] = row["id"]
            session["_csrf"]   = secrets.token_hex(16)
            _audit("LOGIN_SUCCESS", row["id"], f"ip={ip}")
            _notify(row["id"], "login", f"Login berhasil dari {ip}")
            flash(f"Selamat datang kembali, {row['full_name']}! 👋", "success")
            return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        _audit("LOGOUT", g.user["id"])
        session.clear()
        flash("Anda telah keluar. Sampai jumpa! 👋", "info")
        return redirect(url_for("login"))

    # ── Dashboard ─────────────────────────────────────────────────────────────
    @app.route("/dashboard")
    @login_required
    def dashboard():
        allowed_ids = _allowed_pokja(g.user["id"], g.user["role"], g.db)
        stats       = _stats(g.db, allowed_ids, g.user["role"])
        reminders   = _reminders(g.db)
        activities  = _recent_activities(g.db, limit=8)
        notifs      = _get_notifications(g.user["id"], g.db)
        return render_template("dashboard.html",
            stats=stats, reminders=reminders,
            activities=activities, notifs=notifs,
            csrf=_csrf())

    # ── Dokumen (paginated, advanced search) ──────────────────────────────────
    @app.route("/dokumen")
    @login_required
    def dokumen():
        search    = request.args.get("q", "").strip()
        sel_pokja = request.args.get("pokja_id", "all")
        sel_type  = request.args.get("file_type", "all")
        sort      = request.args.get("sort", "newest")
        page      = max(1, int(request.args.get("page", 1)))

        allowed_ids = _allowed_pokja(g.user["id"], g.user["role"], g.db)
        pokja_rows  = _pokja_user(g.db, allowed_ids, g.user["role"])
        params, where = [], []

        if g.user["role"] != "admin":
            if not allowed_ids:
                return render_template("dokumen.html", files=[], pokja_rows=pokja_rows,
                    search=search, selected_pokja="all", selected_type="all",
                    sort=sort, page=1, total_pages=1, total_count=0, csrf=_csrf())
            ph = ",".join(["?"] * len(allowed_ids))
            where.append(f"f.pokja_id IN ({ph})")
            params.extend(allowed_ids)

        if sel_pokja != "all":
            where.append("f.pokja_id=?"); params.append(int(sel_pokja))
        if sel_type != "all":
            where.append("f.file_type=?"); params.append(sel_type.upper())
        if search:
            where.append("(f.original_name LIKE ? OR f.description LIKE ? OR f.tags LIKE ?)")
            like = f"%{search}%"; params.extend([like, like, like])

        wsql  = ("WHERE " + " AND ".join(where)) if where else ""
        order = {"newest": "f.uploaded_at DESC", "oldest": "f.uploaded_at ASC",
                 "name": "f.original_name ASC", "size": "f.file_size DESC"}.get(sort, "f.uploaded_at DESC")

        total_count = g.db.execute(f"SELECT COUNT(*) FROM files f {wsql}", tuple(params)).fetchone()[0]
        total_pages = max(1, math.ceil(total_count / PER_PAGE))
        page        = min(page, total_pages)
        offset      = (page - 1) * PER_PAGE

        files = g.db.execute(f"""
            SELECT f.id, f.original_name, f.description, f.tags, f.uploaded_at,
                   f.file_size, f.file_type, f.file_hash,
                   p.name AS pokja_name, p.id AS pokja_id,
                   u.full_name AS uploader_name,
                   s.kode AS standar_kode, s.nama AS standar_nama
            FROM files f
            INNER JOIN pokja p ON p.id=f.pokja_id
            INNER JOIN users u ON u.id=f.uploaded_by
            LEFT JOIN standar s ON s.id=f.standar_id
            {wsql} ORDER BY {order} LIMIT ? OFFSET ?
        """, tuple(params) + (PER_PAGE, offset)).fetchall()

        file_types = g.db.execute("SELECT DISTINCT file_type FROM files WHERE file_type!='' ORDER BY file_type").fetchall()

        return render_template("dokumen.html", files=files, pokja_rows=pokja_rows,
            file_types=file_types, search=search, selected_pokja=sel_pokja,
            selected_type=sel_type, sort=sort,
            page=page, total_pages=total_pages, total_count=total_count,
            csrf=_csrf())

        # ── Upload ────────────────────────────────────────────────────────────────
    @app.route("/upload", methods=["GET", "POST"])
    @login_required
    def upload_file():
        allowed_ids  = _allowed_pokja(g.user["id"], g.user["role"], g.db)
        pokja_rows   = _pokja_user(g.db, allowed_ids, g.user["role"])
        standar_rows = g.db.execute("SELECT id,kode,nama,pokja_id FROM standar ORDER BY kode").fetchall()

        if not pokja_rows:
            flash("Anda belum memiliki akses ke pokja manapun. Hubungi administrator.", "warning")
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            if not _csrf_ok(): abort(403)

            file       = request.files.get("file")
            desc       = request.form.get("description", "").strip()
            tags       = request.form.get("tags", "").strip()
            standar_id = request.form.get("standar_id") or None

            # --- PERBAIKAN VALIDASI POKJA (ANTI-CRASH) ---
            raw_pokja_id = request.form.get("pokja_id", "").strip()

            if not raw_pokja_id:
                flash("Pokja wajib dipilih.", "danger")
                pokja_id = None
            else:
                try:
                    pokja_id = int(raw_pokja_id)
                except ValueError:
                    flash("Input Pokja tidak valid.", "danger")
                    pokja_id = None

            # Evaluasi validasi input sebelum memproses file
            if not file or not file.filename.strip():
                flash("File wajib dipilih.", "danger")
            elif not _allowed_ext(file.filename):
                flash("Format file tidak diizinkan.", "danger")
            elif pokja_id is None:
                # Menahan proses jika validasi pokja_id di atas gagal
                pass
            elif g.user["role"] != "admin" and pokja_id not in allowed_ids:
                flash("Anda tidak memiliki akses ke pokja tersebut.", "danger")
            else:
                ext   = file.filename.rsplit(".", 1)[1].lower()
                sname = f"{uuid.uuid4().hex}.{ext}"
                fpath = UPLOAD_DIR / sname
                file.save(fpath)
                fsize = fpath.stat().st_size
                fhash = _hash(fpath)

                # --- PERBAIKAN WAKTU (MENGGUNAKAN STANDAR MODERN UTC) ---
                current_time_utc = datetime.now(UTC).isoformat(timespec="seconds") + "Z"

                g.db.execute("""
                    INSERT INTO files
                      (original_name,stored_name,description,tags,pokja_id,standar_id,
                       uploaded_by,uploaded_at,file_size,file_type,file_hash)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)
                """, (secure_filename(file.filename), sname, desc, tags, pokja_id,
                      standar_id, g.user["id"], current_time_utc,
                      fsize, ext.upper(), fhash))

                fid = g.db.execute("SELECT last_insert_rowid()").fetchone()[0]
                g.db.commit()
                _audit("UPLOAD", g.user["id"], f"file_id={fid} pokja={pokja_id} name={secure_filename(file.filename)}")

                # Notify all admins
                for adm in g.db.execute("SELECT id FROM users WHERE role='admin' AND active=1").fetchall():
                    _notify(adm["id"], "upload",
                        f"{g.user['full_name']} mengupload dokumen baru: {secure_filename(file.filename)}")

                flash("✅ Dokumen berhasil diupload!", "success")
                return redirect(url_for("dokumen"))

        return render_template("upload.html", pokja_rows=pokja_rows,
            standar_rows=standar_rows, csrf=_csrf())


    # ── Download ──────────────────────────────────────────────────────────────
    @app.route("/files/<int:fid>/download")
    @login_required
    def download_file(fid: int):
        row = g.db.execute(
            "SELECT id,original_name,stored_name,pokja_id FROM files WHERE id=?", (fid,)).fetchone()
        if not row:
            flash("File tidak ditemukan.", "danger")
            return redirect(url_for("dokumen"))
        if g.user["role"] != "admin":
            if row["pokja_id"] not in _allowed_pokja(g.user["id"], g.user["role"], g.db):
                _audit("DOWNLOAD_DENIED", g.user["id"], f"file_id={fid}")
                abort(403)
        _audit("DOWNLOAD", g.user["id"], f"file_id={fid} name={row['original_name']}")
        return send_from_directory(UPLOAD_DIR, row["stored_name"],
            as_attachment=True, download_name=row["original_name"])

    # ── Delete File ───────────────────────────────────────────────────────────
    @app.route("/files/<int:fid>/delete", methods=["POST"])
    @login_required
    @admin_required
    def delete_file(fid: int):
        if not _csrf_ok(): abort(403)
        row = g.db.execute("SELECT stored_name,original_name FROM files WHERE id=?", (fid,)).fetchone()
        if row:
            fp = UPLOAD_DIR / row["stored_name"]
            if fp.exists():
                fp.unlink()
            g.db.execute("DELETE FROM files WHERE id=?", (fid,))
            g.db.commit()
            _audit("DELETE_FILE", g.user["id"], f"file_id={fid} name={row['original_name']}")
            flash(f"File '{row['original_name']}' berhasil dihapus.", "success")
        return redirect(url_for("dokumen"))

    # ── Profile ───────────────────────────────────────────────────────────────
    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    def profile():
        if request.method == "POST":
            if not _csrf_ok(): abort(403)
            action = request.form.get("action", "update_profile")

            if action == "update_profile":
                full_name = request.form.get("full_name", "").strip()
                theme     = request.form.get("theme", "light")
                if len(full_name) < 3:
                    flash("Nama lengkap minimal 3 karakter.", "danger")
                else:
                    g.db.execute("UPDATE users SET full_name=?, theme=? WHERE id=?",
                        (full_name, theme, g.user["id"]))
                    g.db.commit()
                    session["theme"] = theme
                    _audit("UPDATE_PROFILE", g.user["id"], "updated name/theme")
                    flash("✅ Profil berhasil diperbarui.", "success")

            elif action == "change_password":
                old_pw  = request.form.get("current_password", "")
                new_pw  = request.form.get("new_password", "")
                conf_pw = request.form.get("confirm_password", "")
                row     = g.db.execute("SELECT password_hash FROM users WHERE id=?",
                    (g.user["id"],)).fetchone()
                if not check_password_hash(row["password_hash"], old_pw):
                    flash("Password lama tidak sesuai.", "danger")
                elif new_pw != conf_pw:
                    flash("Konfirmasi password tidak cocok.", "danger")
                elif not _strong_pw(new_pw):
                    flash("Password baru harus minimal 8 karakter, ada huruf besar, kecil, dan angka.", "danger")
                else:
                    g.db.execute("UPDATE users SET password_hash=? WHERE id=?",
                        (generate_password_hash(new_pw), g.user["id"]))
                    g.db.commit()
                    _audit("CHANGE_PASSWORD", g.user["id"])
                    flash("✅ Password berhasil diubah.", "success")

            return redirect(url_for("profile"))

        row = g.db.execute(
            "SELECT id,username,full_name,role,created_at,theme FROM users WHERE id=?",
            (g.user["id"],)).fetchone()
        my_files = g.db.execute(
            "SELECT COUNT(*) as c FROM files WHERE uploaded_by=?", (g.user["id"],)).fetchone()["c"]
        my_pokja = g.db.execute(
            "SELECT p.name FROM user_pokja up JOIN pokja p ON p.id=up.pokja_id WHERE up.user_id=?",
            (g.user["id"],)).fetchall()
        stats = {
            "doc_count":   my_files,
            "pokja_count": len(my_pokja),
        }
        return render_template("profile.html", user=row, my_files=my_files,
            my_pokja=my_pokja, stats=stats, csrf=_csrf())

    # ── Notifications ─────────────────────────────────────────────────────────
    @app.route("/notifications/read", methods=["POST"])
    @login_required
    def read_notifications():
        g.db.execute("UPDATE notifications SET is_read=1 WHERE user_id=?", (g.user["id"],))
        g.db.commit()
        return jsonify({"ok": True})

    @app.route("/api/notifications")
    @login_required
    def api_notifications():
        notifs = g.db.execute(
            "SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 20",
            (g.user["id"],)).fetchall()
        return jsonify({"notifications": [dict(n) for n in notifs]})

    @app.route("/api/notif-count")
    @login_required
    def notif_count():
        c = g.db.execute("SELECT COUNT(*) FROM notifications WHERE user_id=? AND is_read=0",
            (g.user["id"],)).fetchone()[0]
        return jsonify({"count": c})

    # ── Admin: Pokja ──────────────────────────────────────────────────────────
    @app.route("/admin/pokja", methods=["GET", "POST"])
    @login_required
    @admin_required
    def manage_pokja():
        if request.method == "POST":
            if not _csrf_ok(): abort(403)
            action = request.form.get("action", "add")
            if action == "add":
                name = request.form.get("name", "").strip()
                desc = request.form.get("description", "").strip()
                if len(name) < 2:
                    flash("Nama pokja minimal 2 karakter.", "danger")
                elif g.db.execute("SELECT id FROM pokja WHERE lower(name)=lower(?)", (name,)).fetchone():
                    flash("Nama pokja sudah ada.", "warning")
                else:
                    g.db.execute("INSERT INTO pokja(name,description) VALUES(?,?)", (name, desc))
                    g.db.commit()
                    _audit("CREATE_POKJA", g.user["id"], f"name={name}")
                    flash(f"✅ Pokja '{name}' berhasil ditambahkan.", "success")
            elif action == "delete":
                pid = int(request.form.get("pokja_id", 0))
                row = g.db.execute("SELECT name FROM pokja WHERE id=?", (pid,)).fetchone()
                if row:
                    g.db.execute("DELETE FROM pokja WHERE id=?", (pid,))
                    g.db.commit()
                    _audit("DELETE_POKJA", g.user["id"], f"id={pid}")
                    flash(f"Pokja dihapus.", "success")
            elif action == "edit":
                pid  = int(request.form.get("pokja_id", 0))
                name = request.form.get("name", "").strip()
                desc = request.form.get("description", "").strip()
                if len(name) >= 2:
                    g.db.execute("UPDATE pokja SET name=?, description=? WHERE id=?", (name, desc, pid))
                    g.db.commit()
                    flash("✅ Pokja diperbarui.", "success")
            return redirect(url_for("manage_pokja"))

        pokja_rows = g.db.execute("""
            SELECT p.id, p.name, p.description,
                   COUNT(DISTINCT f.id) AS total_files,
                   COUNT(DISTINCT up.user_id) AS total_users,
                   COUNT(DISTINCT s.id) AS total_standar
            FROM pokja p
            LEFT JOIN files f ON f.pokja_id=p.id
            LEFT JOIN user_pokja up ON up.pokja_id=p.id
            LEFT JOIN standar s ON s.pokja_id=p.id
            GROUP BY p.id ORDER BY p.name
        """).fetchall()
        return render_template("pokja.html", pokja_rows=pokja_rows, csrf=_csrf())

    # ── Admin: Standar ────────────────────────────────────────────────────────
    @app.route("/admin/standar", methods=["GET", "POST"])
    @login_required
    @admin_required
    def manage_standar():
        if request.method == "POST":
            if not _csrf_ok(): abort(403)
            action = request.form.get("action", "add")
            if action == "add":
                kode   = request.form.get("kode", "").strip()
                nama   = request.form.get("nama", "").strip()
                pid    = request.form.get("pokja_id") or None
                target = max(1, int(request.form.get("target_dokumen", 1)))
                if kode and nama:
                    if g.db.execute("SELECT id FROM standar WHERE kode=?", (kode,)).fetchone():
                        flash(f"Kode standar '{kode}' sudah ada.", "warning")
                    else:
                        g.db.execute(
                            "INSERT INTO standar(kode,nama,pokja_id,target_dokumen) VALUES(?,?,?,?)",
                            (kode, nama, pid, target))
                        g.db.commit()
                        flash(f"✅ Standar '{kode}' berhasil ditambahkan.", "success")
            elif action == "delete":
                sid = int(request.form.get("standar_id", 0))
                g.db.execute("DELETE FROM standar WHERE id=?", (sid,))
                g.db.commit()
                flash("Standar dihapus.", "success")
            elif action == "edit":
                sid    = int(request.form.get("standar_id", 0))
                nama   = request.form.get("nama", "").strip()
                pid    = request.form.get("pokja_id") or None
                target = max(1, int(request.form.get("target_dokumen", 1)))
                g.db.execute("UPDATE standar SET nama=?, pokja_id=?, target_dokumen=? WHERE id=?",
                    (nama, pid, target, sid))
                g.db.commit()
                flash("✅ Standar diperbarui.", "success")
            return redirect(url_for("manage_standar"))

        standar_rows = g.db.execute("""
            SELECT s.id, s.kode, s.nama, s.target_dokumen, s.pokja_id,
                   p.name AS pokja_name, COUNT(f.id) AS uploaded
            FROM standar s
            LEFT JOIN pokja p ON p.id=s.pokja_id
            LEFT JOIN files f ON f.standar_id=s.id
            GROUP BY s.id ORDER BY s.kode
        """).fetchall()
        pokja_rows = g.db.execute("SELECT id,name FROM pokja ORDER BY name").fetchall()
        total_s = len(standar_rows)
        if total_s > 0:
            avg_compliance = round(sum(
                min(100, (r["uploaded"] / max(r["target_dokumen"],1) * 100))
                for r in standar_rows) / total_s)
        else:
            avg_compliance = 0
        full_count     = sum(1 for r in standar_rows if r["uploaded"] >= r["target_dokumen"])
        critical_count = sum(1 for r in standar_rows if r["uploaded"] == 0)
        return render_template("standar.html", standar_rows=standar_rows,
            pokja_rows=pokja_rows, avg_compliance=avg_compliance,
            full_count=full_count, critical_count=critical_count, csrf=_csrf())

    # ── Admin: Users ──────────────────────────────────────────────────────────
    @app.route("/admin/users", methods=["GET", "POST"])
    @login_required
    @admin_required
    def manage_users():
        if request.method == "POST":
            if not _csrf_ok(): abort(403)
            username  = request.form.get("username", "").strip().lower()
            fullname  = request.form.get("full_name", "").strip()
            role      = request.form.get("role", "pegawai").strip()
            password  = request.form.get("password", "").strip()
            sel_pokja = request.form.getlist("pokja_ids")
            err = []
            if len(username) < 3: err.append("Username minimal 3 karakter")
            if len(fullname) < 3: err.append("Nama lengkap minimal 3 karakter")
            if len(password) < 8: err.append("Password minimal 8 karakter")
            if not _strong_pw(password): err.append("Password harus ada huruf besar, kecil, angka")
            if role not in {"admin", "ketua_pokja", "pegawai"}: err.append("Role tidak valid")
            if g.db.execute("SELECT id FROM users WHERE lower(username)=?", (username,)).fetchone():
                err.append("Username sudah dipakai")
            if err:
                for e in err: flash(e, "danger")
                return redirect(url_for("manage_users"))

            g.db.execute("""
                INSERT INTO users(username,full_name,role,password_hash,active,created_at,theme)
                VALUES(?,?,?,?,1,?,?)
            """, (username, fullname, role, generate_password_hash(password),
                 datetime.now(UTC).isoformat(timespec="seconds") + "Z", "light"))
            uid = g.db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()["id"]
            if role != "admin":
                for pid in sel_pokja:
                    g.db.execute("INSERT OR IGNORE INTO user_pokja(user_id,pokja_id) VALUES(?,?)",
                        (uid, int(pid)))
            g.db.commit()
            _audit("CREATE_USER", g.user["id"], f"new={username} role={role}")
            _notify(uid, "system", f"Akun Anda telah dibuat oleh {g.user['full_name']}. Selamat bergabung!")
            flash(f"✅ User '{username}' berhasil dibuat.", "success")
            return redirect(url_for("manage_users"))

        search_u = request.args.get("q", "").strip()
        if search_u:
            users = g.db.execute(
                "SELECT id,username,full_name,role,active,created_at FROM users WHERE username LIKE ? OR full_name LIKE ? ORDER BY id",
                (f"%{search_u}%", f"%{search_u}%")).fetchall()
        else:
            users = g.db.execute(
                "SELECT id,username,full_name,role,active,created_at FROM users ORDER BY id").fetchall()

        pokja_rows = g.db.execute("SELECT id,name FROM pokja ORDER BY name").fetchall()
        access_map = {}
        for r in g.db.execute("""
            SELECT up.user_id, p.id AS pokja_id, p.name AS pokja_name
            FROM user_pokja up INNER JOIN pokja p ON p.id=up.pokja_id ORDER BY p.name
        """).fetchall():
            access_map.setdefault(r["user_id"], []).append(dict(r))
        return render_template("users.html", users=users, pokja_rows=pokja_rows,
            access_map=access_map, search_u=search_u, csrf=_csrf())

    @app.route("/admin/users/<int:uid>/toggle", methods=["POST"])
    @login_required
    @admin_required
    def toggle_user(uid):
        if not _csrf_ok(): abort(403)
        row = g.db.execute("SELECT username,active FROM users WHERE id=?", (uid,)).fetchone()
        if not row: flash("User tidak ditemukan.", "danger"); return redirect(url_for("manage_users"))
        if row["username"] == "admin":
            flash("Admin utama tidak bisa dinonaktifkan.", "warning")
            return redirect(url_for("manage_users"))
        desired = 0 if int(row["active"]) == 1 else 1
        g.db.execute("UPDATE users SET active=? WHERE id=?", (desired, uid))
        g.db.commit()
        _audit("TOGGLE_USER", g.user["id"], f"uid={uid} status={desired}")
        flash(f"Status user diperbarui menjadi {'Aktif' if desired else 'Nonaktif'}.", "success")
        return redirect(url_for("manage_users"))

    @app.route("/admin/users/<int:uid>/access", methods=["POST"])
    @login_required
    @admin_required
    def update_user_access(uid):
        if not _csrf_ok(): abort(403)
        row = g.db.execute("SELECT role FROM users WHERE id=?", (uid,)).fetchone()
        if not row or row["role"] == "admin":
            flash("Aksi tidak valid.", "warning")
            return redirect(url_for("manage_users"))
        sel = [int(x) for x in request.form.getlist("pokja_ids")]
        g.db.execute("DELETE FROM user_pokja WHERE user_id=?", (uid,))
        for pid in sel:
            g.db.execute("INSERT OR IGNORE INTO user_pokja(user_id,pokja_id) VALUES(?,?)", (uid, pid))
        g.db.commit()
        _audit("UPDATE_ACCESS", g.user["id"], f"uid={uid} pokja={sel}")
        flash("✅ Hak akses pokja diperbarui.", "success")
        return redirect(url_for("manage_users"))

    @app.route("/admin/users/<int:uid>/reset-password", methods=["POST"])
    @login_required
    @admin_required
    def reset_password(uid):
        if not _csrf_ok(): abort(403)
        new_pw = secrets.token_urlsafe(10)
        g.db.execute("UPDATE users SET password_hash=? WHERE id=?",
            (generate_password_hash(new_pw), uid))
        g.db.commit()
        _audit("RESET_PASSWORD", g.user["id"], f"uid={uid}")
        flash(f"✅ Password baru: <strong>{new_pw}</strong> (catat sekarang!)", "info")
        return redirect(url_for("manage_users"))

    # ── Audit Trail ───────────────────────────────────────────────────────────
    @app.route("/admin/audit")
    @login_required
    @admin_required
    def audit_trail():
        page    = max(1, int(request.args.get("page", 1)))
        action_filter = request.args.get("action", "all")
        q       = request.args.get("q", "").strip()

        params, where = [], []
        if action_filter != "all":
            where.append("al.action LIKE ?"); params.append(f"{action_filter}%")
        if q:
            where.append("(al.detail LIKE ? OR u.full_name LIKE ?)")
            like = f"%{q}%"; params.extend([like, like])

        wsql = ("WHERE " + " AND ".join(where)) if where else ""
        total = g.db.execute(f"""
            SELECT COUNT(*) FROM audit_log al LEFT JOIN users u ON u.id=al.user_id {wsql}
        """, tuple(params)).fetchone()[0]
        total_pages = max(1, math.ceil(total / PER_PAGE))
        page = min(page, total_pages)
        offset = (page - 1) * PER_PAGE

        logs = g.db.execute(f"""
            SELECT al.id, al.action, al.detail, al.created_at, u.full_name AS user_name
            FROM audit_log al LEFT JOIN users u ON u.id=al.user_id
            {wsql} ORDER BY al.created_at DESC LIMIT ? OFFSET ?
        """, tuple(params) + (PER_PAGE, offset)).fetchall()

        action_types = ["LOGIN", "LOGOUT", "UPLOAD", "DOWNLOAD", "DELETE", "CREATE", "TOGGLE", "UPDATE"]
        return render_template("audit.html", logs=logs, action_types=action_types,
            action_filter=action_filter, q=q,
            page=page, total_pages=total_pages, total=total)

    # ── Analytics API ─────────────────────────────────────────────────────────

    @app.route("/api/analytics")
    @login_required
    def api_analytics():
        # ── 1. GENERATE RENTANG 7 HARI TERAKHIR (1 MINGGU) ──
        today_dt = datetime.now(UTC).date()
        date_list = [str(today_dt - timedelta(days=i)) for i in range(6, -1, -1)]

        # Ambil statistik upload dari database filter 7 hari terakhir
        raw_uploads = g.db.execute("""
            SELECT SUBSTR(uploaded_at, 1, 10) AS tgl, COUNT(*) AS total
            FROM files
            WHERE SUBSTR(uploaded_at, 1, 10) >= DATE('now', '-7 days')
            GROUP BY tgl
        """).fetchall()

        db_data = {r["tgl"]: r["total"] for r in raw_uploads}
        id_months = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

        formatted_chart = []
        for date_str in date_list:
            y, m, d = date_str.split("-")
            month_label = id_months[int(m) - 1]
            total_upload = db_data.get(date_str, 0)

            # Tampilkan semua label tanggal harian karena rentang waktu pendek
            display_label = f"{int(d)} {month_label}"

            formatted_chart.append({
                "tgl": display_label,
                "total": total_upload
            })

        # ── 2. DATA ANALISIS KARTU DAN TABEL LAINNYA ──
        pokja_chart = g.db.execute("""
            SELECT p.name, COUNT(f.id) AS total
            FROM pokja p LEFT JOIN files f ON f.pokja_id=p.id
            GROUP BY p.id ORDER BY total DESC
        """).fetchall()

        compliance = g.db.execute("""
            SELECT s.kode, s.nama, s.target_dokumen, COUNT(f.id) AS uploaded, p.name AS pokja_name
            FROM standar s
            LEFT JOIN files f ON f.standar_id=s.id
            LEFT JOIN pokja p ON p.id=s.pokja_id
            GROUP BY s.id ORDER BY s.kode
        """).fetchall()

        type_dist = g.db.execute("""
            SELECT file_type, COUNT(*) AS total FROM files WHERE file_type!='' GROUP BY file_type ORDER BY total DESC
        """).fetchall()

        weekly = g.db.execute("""
            SELECT strftime('%w', uploaded_at) AS dow, COUNT(*) AS total
            FROM files GROUP BY dow ORDER BY dow
        """).fetchall()

        return jsonify({
            "uploads_chart": formatted_chart,
            "pokja_chart":   [dict(r) for r in pokja_chart],
            "type_dist":     [dict(r) for r in type_dist],
            "weekly":        [dict(r) for r in weekly],
            "compliance":    [{
                "kode": r["kode"], "nama": r["nama"], "pokja": r["pokja_name"],
                "uploaded": r["uploaded"], "target": r["target_dokumen"],
                "pct": min(100, round(r["uploaded"] / max(r["target_dokumen"], 1) * 100))
            } for r in compliance]
        })



    # ── Export ────────────────────────────────────────────────────────────────
    @app.route("/export/csv")
    @login_required
    @admin_required
    def export_csv():
        rows = g.db.execute("""
            SELECT f.original_name, f.description, f.tags, f.uploaded_at,
                   f.file_size, f.file_type, f.file_hash,
                   p.name AS pokja_name, u.full_name AS uploader,
                   s.kode AS standar_kode, s.nama AS standar_nama
            FROM files f
            INNER JOIN pokja p ON p.id=f.pokja_id
            INNER JOIN users u ON u.id=f.uploaded_by
            LEFT JOIN standar s ON s.id=f.standar_id
            ORDER BY f.uploaded_at DESC
        """).fetchall()
        out = io.StringIO()
        w   = csv.writer(out)
        w.writerow(["Nama File", "Pokja", "Standar", "Nama Standar", "Deskripsi", "Tags",
                    "Uploader", "Tgl Upload", "Ukuran (KB)", "Tipe", "Hash"])
        for r in rows:
            w.writerow([r["original_name"], r["pokja_name"],
                r["standar_kode"] or "", r["standar_nama"] or "",
                r["description"], r["tags"], r["uploader"],
                r["uploaded_at"][:19].replace("T", " "),
                round((r["file_size"] or 0) / 1024, 1),
                r["file_type"], r["file_hash"]])
        out.seek(0)
        fname = f"laporan_akreditasi_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        _audit("EXPORT_CSV", g.user["id"])
        return Response(out.getvalue(), mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={fname}"})

    # ── Error handlers ────────────────────────────────────────────────────────
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html", code=403,
            msg="Akses ditolak. Anda tidak memiliki izin untuk halaman ini."), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404,
            msg="Halaman tidak ditemukan."), 404

    @app.errorhandler(413)
    def too_large(e):
        flash("File terlalu besar. Maksimum 50 MB.", "danger")
        return redirect(url_for("upload_file"))

    @app.errorhandler(500)
    def server_error(e):
        logger.error(f"500: {e}")
        return render_template("error.html", code=500,
            msg="Terjadi kesalahan pada server. Silakan coba lagi."), 500

    return app


# ── Helpers ────────────────────────────────────────────────────────────────────
def get_db_connection():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("PRAGMA journal_mode=WAL")
    return c

def get_current_user():
    uid = session.get("user_id")
    if not uid: return None
    db  = getattr(g, "db", None)
    if not db: return None
    row = db.execute(
        "SELECT id,username,full_name,role,active,theme FROM users WHERE id=?", (uid,)).fetchone()
    if not row or int(row["active"]) != 1:
        session.clear(); return None
    return row

def login_required(func):
    @wraps(func)
    def wrapper(*a, **kw):
        if not g.user: return redirect(url_for("login"))
        return func(*a, **kw)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*a, **kw):
        if not g.user or g.user["role"] != "admin":
            flash("Akses ditolak. Halaman ini hanya untuk administrator.", "danger")
            return redirect(url_for("dashboard"))
        return func(*a, **kw)
    return wrapper

def _allowed_ext(fn):
    return "." in fn and fn.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def _allowed_pokja(uid, role, db):
    if role == "admin":
        return [r["id"] for r in db.execute("SELECT id FROM pokja").fetchall()]
    return [r["pokja_id"] for r in
            db.execute("SELECT pokja_id FROM user_pokja WHERE user_id=?", (uid,)).fetchall()]

def _pokja_user(db, allowed_ids, role):
    if role == "admin":
        return db.execute("SELECT id,name FROM pokja ORDER BY name").fetchall()
    if not allowed_ids: return []
    ph = ",".join(["?"] * len(allowed_ids))
    return db.execute(f"SELECT id,name FROM pokja WHERE id IN ({ph}) ORDER BY name",
        tuple(allowed_ids)).fetchall()

def _stats(db, allowed_ids, role):
    params, where = [], ""
    if role != "admin" and allowed_ids:
        ph = ",".join(["?"] * len(allowed_ids))
        where = f"WHERE pokja_id IN ({ph})"; params = list(allowed_ids)
    total_files   = db.execute(f"SELECT COUNT(*) FROM files {where}", params).fetchone()[0]
    total_pokja   = db.execute("SELECT COUNT(*) FROM pokja").fetchone()[0]
    total_standar = db.execute("SELECT COUNT(*) FROM standar").fetchone()[0]
    total_users   = db.execute("SELECT COUNT(*) FROM users WHERE active=1").fetchone()[0]
    rows = db.execute(
        "SELECT target_dokumen, COUNT(f.id) AS up FROM standar s LEFT JOIN files f ON f.standar_id=s.id GROUP BY s.id"
    ).fetchall()
    pct = sum(min(100, r["up"] / max(r["target_dokumen"], 1) * 100) for r in rows) / len(rows) if rows else 0
    today = db.execute(

        "SELECT COUNT(*) FROM files WHERE SUBSTR(uploaded_at, 1, 10)=DATE('now')", []).fetchone()[0]

    return {
        "total_files": total_files, "total_pokja": total_pokja,
        "total_standar": total_standar, "total_users": total_users,
        "compliance_pct": round(pct, 1), "today_uploads": today
    }

def _reminders(db):
    return db.execute("""
        SELECT s.kode, s.nama, s.target_dokumen, COUNT(f.id) AS uploaded, p.name AS pokja_name
        FROM standar s
        LEFT JOIN files f ON f.standar_id=s.id
        LEFT JOIN pokja p ON p.id=s.pokja_id
        GROUP BY s.id HAVING uploaded < s.target_dokumen
        ORDER BY (CAST(uploaded AS REAL)/s.target_dokumen) ASC LIMIT 6
    """).fetchall()

def _recent_activities(db, limit=8):
    return db.execute(f"""
        SELECT al.action, al.detail, al.created_at, u.full_name
        FROM audit_log al LEFT JOIN users u ON u.id=al.user_id
        ORDER BY al.created_at DESC LIMIT {limit}
    """).fetchall()

def _notify(uid, notif_type, message):
    try:
        db = get_db_connection()
        db.execute(
            "INSERT INTO notifications(user_id,type,message,created_at,is_read) VALUES(?,?,?,?,0)",
            (uid, notif_type, message, datetime.utcnow().isoformat(timespec="seconds") + "Z"))
        db.commit(); db.close()
    except Exception as e:
        logger.error(f"notify error: {e}")

def _get_notifications(uid, db, limit=10):
    return db.execute("""
        SELECT id, type, message, created_at, is_read FROM notifications
        WHERE user_id=? ORDER BY created_at DESC LIMIT ?
    """, (uid, limit)).fetchall()

def _audit(action, uid, detail=""):
    try:
        db = get_db_connection()
        db.execute(
            "INSERT INTO audit_log(action,user_id,detail,created_at) VALUES(?,?,?,?)",
            (action, uid, detail, datetime.utcnow().isoformat(timespec="seconds") + "Z"))
        db.commit(); db.close()
    except Exception as e:
        logger.error(f"audit error: {e}")

def _hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]

def _strong_pw(pw):
    return (len(pw) >= 8 and any(c.isupper() for c in pw)
            and any(c.islower() for c in pw) and any(c.isdigit() for c in pw))

def _csrf():    return session.get("_csrf", "")
def _csrf_ok():
    # Terima baik nama _csrf (lama) maupun csrf_token (baru dari template)
    t = (request.form.get("csrf_token")
         or request.form.get("_csrf")
         or request.headers.get("X-CSRF-Token"))
    return t and t == session.get("_csrf")


# ── Init DB ────────────────────────────────────────────────────────────────────
def init_db():
    db  = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    cur.executescript("""
        PRAGMA foreign_keys=ON;
        PRAGMA journal_mode=WAL;

        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            theme TEXT NOT NULL DEFAULT 'light',
            created_at TEXT NOT NULL);

        CREATE TABLE IF NOT EXISTS pokja(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT DEFAULT '');

        CREATE TABLE IF NOT EXISTS standar(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode TEXT UNIQUE NOT NULL,
            nama TEXT NOT NULL,
            pokja_id INTEGER REFERENCES pokja(id),
            target_dokumen INTEGER NOT NULL DEFAULT 1);

        CREATE TABLE IF NOT EXISTS user_pokja(
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            pokja_id INTEGER NOT NULL REFERENCES pokja(id) ON DELETE CASCADE,
            PRIMARY KEY(user_id, pokja_id));

        CREATE TABLE IF NOT EXISTS files(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_name TEXT NOT NULL,
            stored_name TEXT NOT NULL,
            description TEXT DEFAULT '',
            tags TEXT DEFAULT '',
            pokja_id INTEGER NOT NULL REFERENCES pokja(id),
            standar_id INTEGER REFERENCES standar(id),
            uploaded_by INTEGER NOT NULL REFERENCES users(id),
            uploaded_at TEXT NOT NULL,
            file_size INTEGER DEFAULT 0,
            file_type TEXT DEFAULT '',
            file_hash TEXT DEFAULT '');

        CREATE TABLE IF NOT EXISTS audit_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            user_id INTEGER REFERENCES users(id),
            detail TEXT DEFAULT '',
            created_at TEXT NOT NULL);

        CREATE TABLE IF NOT EXISTS notifications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            type TEXT NOT NULL DEFAULT 'info',
            message TEXT NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL);

        CREATE INDEX IF NOT EXISTS idx_files_pokja    ON files(pokja_id);
        CREATE INDEX IF NOT EXISTS idx_files_standar  ON files(standar_id);
        CREATE INDEX IF NOT EXISTS idx_audit_created  ON audit_log(created_at);
        CREATE INDEX IF NOT EXISTS idx_notif_user     ON notifications(user_id, is_read);
    """)

    # Default admin
    if not cur.execute("SELECT id FROM users WHERE username='admin'").fetchone():
        cur.execute(
            "INSERT INTO users(username,full_name,role,password_hash,active,theme,created_at) VALUES(?,?,?,?,1,?,?)",
            ("admin", "Administrator", "admin",
             generate_password_hash("Admin123!"), "light",
             datetime.utcnow().isoformat(timespec="seconds") + "Z"))

    # Default pokja
    for pname, pdesc in [
        ("Pokja Manajemen", "Manajemen Fasilitas & Keselamatan"),
        ("Pokja Pelayanan Klinis", "Standar Pelayanan & Asuhan Pasien"),
        ("Pokja Keselamatan Pasien", "Identifikasi & Insiden Keselamatan"),
        ("Pokja SDM", "Sumber Daya Manusia & Kompetensi"),
        ("Pokja Sarpras", "Sarana, Prasarana & Peralatan"),
        ("Pokja PPI", "Pencegahan & Pengendalian Infeksi"),
    ]:
        if not cur.execute("SELECT id FROM pokja WHERE name=?", (pname,)).fetchone():
            cur.execute("INSERT INTO pokja(name,description) VALUES(?,?)", (pname, pdesc))

    # Default standar SNARS
    for kode, nama, pokja_name, target in [
        ("MFK.1", "Manajemen Fasilitas & Keselamatan", "Pokja Manajemen", 3),
        ("MFK.2", "Program Manajemen Risiko Fasilitas", "Pokja Manajemen", 2),
        ("MFK.3", "Keselamatan & Keamanan", "Pokja Manajemen", 3),
        ("PP.1",  "Pelayanan & Asuhan Pasien", "Pokja Pelayanan Klinis", 4),
        ("PP.2",  "Penilaian Pasien", "Pokja Pelayanan Klinis", 3),
        ("PP.3",  "Pelayanan Anestesi & Bedah", "Pokja Pelayanan Klinis", 3),
        ("KP.1",  "Identifikasi Pasien dengan Benar", "Pokja Keselamatan Pasien", 2),
        ("KP.2",  "Komunikasi Efektif", "Pokja Keselamatan Pasien", 2),
        ("KP.3",  "Keamanan Obat yang Perlu Diwaspadai", "Pokja Keselamatan Pasien", 3),
        ("SDM.1", "Perencanaan & Rekrutmen SDM", "Pokja SDM", 2),
        ("SDM.2", "Kompetensi & Orientasi Staff", "Pokja SDM", 3),
        ("PPI.1", "Program PPI", "Pokja PPI", 2),
        ("PPI.2", "Kebersihan Tangan", "Pokja PPI", 2),
    ]:
        if not cur.execute("SELECT id FROM standar WHERE kode=?", (kode,)).fetchone():
            prow = cur.execute("SELECT id FROM pokja WHERE name=?", (pokja_name,)).fetchone()
            if prow:
                cur.execute("INSERT INTO standar(kode,nama,pokja_id,target_dokumen) VALUES(?,?,?,?)",
                    (kode, nama, prow[0], target))

    db.commit()
    db.close()
    logger.info("Database initialized — Pro v3.0")


init_db()
app = create_app()

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    logger.info(f"AkreditasiRS Pro v3.0 starting on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
