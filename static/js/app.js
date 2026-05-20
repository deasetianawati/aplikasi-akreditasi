
(function () {
  'use strict';

  // Helper untuk melakukan escape HTML mencegah serangan XSS pada notifikasi
  function escHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;')
              .replace(/</g, '&lt;')
              .replace(/>/g, '&gt;')
              .replace(/"/g, '&quot;')
              .replace(/'/g, '&#039;'); // SINTAKS SUDAH DIPERBAIKI
  }

  // Ambil CSRF Token dari hidden input secara presisi
  function getCSRF() {
    const input = document.querySelector('#uploadForm input[name="csrf_token"]');
    return input ? input.value : '';
  }

  // 1. Terapkan Tema Secepat Mungkin (Mencegah Layar Berkedip Putih)
  const savedTheme = localStorage.getItem('theme') ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', savedTheme);

  document.addEventListener('DOMContentLoaded', function () {

    // ── 2. Kontrol Tema (Dark / Light Mode) ───────────────────────
    const themeBtn = document.getElementById('themeBtn');
    const iconMoon = document.getElementById('iconMoon');
    const iconSun  = document.getElementById('iconSun');

    function applyTheme(t) {
      document.documentElement.setAttribute('data-theme', t);
      localStorage.setItem('theme', t);
      if (iconMoon && iconSun) {
        iconMoon.style.display = t === 'dark'  ? 'none' : '';
        iconSun.style.display  = t === 'light' ? 'none' : '';
      }
    }
    applyTheme(savedTheme);

    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        applyTheme(current === 'dark' ? 'light' : 'dark');
      });
    }

    // ── 3. Menu Sidebar & Overlay Mobile ──────────────────────────
    const menuBtn = document.getElementById('menuBtn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    function openSidebar()  {
      sidebar && sidebar.classList.add('open');
      overlay && overlay.classList.add('show');
      document.body.style.overflow = 'hidden';
    }
    function closeSidebar() {
      sidebar && sidebar.classList.remove('open');
      overlay && overlay.classList.remove('show');
      document.body.style.overflow = '';
    }

    if (menuBtn) menuBtn.addEventListener('click', openSidebar);
    if (overlay) overlay.addEventListener('click', closeSidebar);

    // Deteksi geser layar (Swipe) untuk menutup sidebar di mobile
    let touchStartX = 0;
    document.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
    document.addEventListener('touchend', e => {
      const dx = touchStartX - e.changedTouches[0].clientX;
      if (dx > 60 && sidebar && sidebar.classList.contains('open')) closeSidebar();
    }, { passive: true });

    // Deteksi geser dari tepi kiri untuk membuka sidebar
    document.addEventListener('touchend', e => {
      const startX = touchStartX;
      const endX = e.changedTouches[0].clientX;
      if (startX < 20 && endX - startX > 60 && sidebar && !sidebar.classList.contains('open')) openSidebar();
    }, { passive: true });

    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeSidebar(); });

    // ── 4. Sistem Notifikasi Real-time ────────────────────────────
    const notifBtn  = document.getElementById('notifBtn');
    const notifDrop = document.getElementById('notifDropdown');
    const notifDot  = document.getElementById('notifDot');
    const notifList = document.getElementById('notifList');
    const markAll   = document.getElementById('markAllRead');

    function loadNotifCount() {
      fetch('/api/notif-count')
        .then(r => r.json())
        .then(d => {
          if (notifDot) notifDot.style.display = d.count > 0 ? '' : 'none';
        }).catch(() => {});
    }

    function renderNotifs(notifs) {
      if (!notifList) return;
      if (!notifs || notifs.length === 0) {
        notifList.innerHTML = `
          <div class="empty-state" style="padding:28px 16px;">
            <div class="empty-state-icon" style="margin:0 auto 12px;">
              <svg xmlns="http://w3.org" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
              </svg>
            </div>
            <div class="empty-state-sub">Tidak ada notifikasi</div>
          </div>`;
        return;
      }
      notifList.innerHTML = notifs.map(n => `
        <div class="notif-item ${n.is_read ? '' : 'unread'}">
          <div class="notif-icon-box">
            <svg xmlns="http://w3.org" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
          </div>
          <div style="flex:1;min-width:0;">
            <div class="notif-msg">${escHtml(n.message)}</div>
            <div class="notif-time">${(n.created_at||'').slice(0,16).replace('T',' ')}</div>
          </div>
        </div>`).join('');
    }

    if (notifBtn) {
      notifBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        const isOpen = notifDrop.classList.toggle('open');
        if (isOpen) {
          fetch('/api/notifications')
            .then(r => r.json())
            .then(d => renderNotifs(d.notifications))
            .catch(() => {});
        }
      });
    }

    if (markAll) {
      markAll.addEventListener('click', function (e) {
        e.stopPropagation();
        fetch('/notifications/read', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': getCSRF() }
        }).then(() => {
          if (notifDot) notifDot.style.display = 'none';
          if (notifDrop) notifDrop.classList.remove('open');
          loadNotifCount();
        }).catch(() => {});
      });
    }

    document.addEventListener('click', e => {
      if (notifDrop && !notifDrop.contains(e.target) && notifBtn && !notifBtn.contains(e.target)) {
        notifDrop.classList.remove('open');
      }
    });

    loadNotifCount();

    // ── 5. Animasi Angka Statistik (Counters) ─────────────────────
    function animateCounter(el) {
      const target = parseInt(el.getAttribute('data-to') || el.textContent.replace(/[^0-9]/g, '') || '0');
      const duration = 900;
      const start = performance.now();
      el.classList.add('animate');
      (function tick(now) {
        const p = Math.min((now - start) / duration, 1);
        const ease = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(ease * target).toLocaleString('id-ID');
        if (p < 1) requestAnimationFrame(tick);
        else el.textContent = target.toLocaleString('id-ID') + (el.dataset.suffix || '');
      })(start);
    }
    document.querySelectorAll('.stat-val[data-to]').forEach(el => {
      const obs = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting) { animateCounter(el); obs.disconnect(); }
      }, { threshold: .5 });
      obs.observe(el);
    });

    // ── 6. Bar Kemajuan (Progress Bars) ───────────────────────────
    setTimeout(() => {
      document.querySelectorAll('[data-width]').forEach(el => {
        el.style.width = el.getAttribute('data-width') + '%';
      });
      document.querySelectorAll('.stat-progress-fill[data-pct]').forEach(el => {
        el.style.width = el.getAttribute('data-pct') + '%';
      });
      document.querySelectorAll('.rem-bar-fill[data-pct]').forEach(el => {
        el.style.width = el.getAttribute('data-pct') + '%';
      });
    }, 100);

    // ── 7. Kartu Kepatuhan (Compliance Card Color) ────────────────
    const compCard = document.getElementById('complianceCard');
    if (compCard) {
      const pct = parseInt(compCard.getAttribute('data-pct') || '0');
      compCard.classList.add(pct >= 80 ? 'c-green' : pct >= 50 ? 'c-yellow' : 'c-red');
      const fill = document.getElementById('progressFill');
      if (fill) {
        fill.setAttribute('data-pct', pct);
        fill.style.background = pct >= 80 ? '#10b981' : pct >= 50 ? '#f59e0b' : '#ef4444';
      }
    }

    // ── 8. Dropdown Chain (Filter Otomatis Standar Berdasar Pokja) ─
    const pokjaSelect = document.getElementById('pokjaSelect');
    const standarSelect = document.getElementById('standarSelect');

    if (pokjaSelect && standarSelect) {
      const originalOptions = Array.from(standarSelect.options);

      pokjaSelect.addEventListener('change', function () {
        const selectedPokja = this.value;
        standarSelect.innerHTML = '';

        originalOptions.forEach(option => {
          const optPokja = option.getAttribute('data-pokja');
          if (!selectedPokja || !optPokja || optPokja === selectedPokja || option.value === "") {
            standarSelect.appendChild(option.cloneNode(true));
          }
        });
        standarSelect.value = "";
      });
    }

    // ── 9. Integrasi Kontrol Manual Dropzone (ANTI-MEMBEKU) ───────
    if (typeof Dropzone !== 'undefined') {
      Dropzone.autoDiscover = false;
    }

    const dropzoneEl = document.getElementById('dropzoneBox');

    if (uploadForm && dropzoneEl) {
      if (dropzoneEl.dropzone) {
        dropzoneEl.dropzone.destroy();
      }

      const myDropzone = new Dropzone("#dropzoneBox", {
        url: uploadForm.action || window.location.pathname,
        autoProcessQueue: false,
        uploadMultiple: false,
        maxFiles: 1,
        maxFilesize: 50,
        paramName: "file",
        acceptedFiles: ".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.jpg,.jpeg,.png,.txt,.zip,.rar",
        clickable: true,
        dictDefaultMessage: "",

        init: function () {
          const dz = this;
          const submitBtn = uploadForm.querySelector("button[type='submit']");

          if (submitBtn) {
            submitBtn.addEventListener("click", function (e) {
              e.preventDefault();
              e.stopPropagation();

              if (!pokjaSelect || !pokjaSelect.value) {
                alert("Silakan pilih Pokja terlebih dahulu!");
                if (pokjaSelect) pokjaSelect.focus();
                return;
              }

              if (dz.getQueuedFiles().length > 0) {
                dz.processQueue();
              } else {
                alert("Silakan pilih atau seret berkas dokumen Anda ke dalam kotak terlebih dahulu!");
              }
            });
          }

          this.on("sending", function (file, xhr, formData) {
            formData.append("csrf_token", getCSRF());
            formData.append("pokja_id", pokjaSelect.value);
            formData.append("standar_id", standarSelect ? standarSelect.value : "");
            formData.append("description", document.getElementById("description").value);
            formData.append("tags", document.getElementById("tags").value);
          });

          this.on("success", function () {
            window.location.href = "/dokumen";
          });

          this.on("error", function (file, message) {
            console.error("Dropzone Error:", message);
            alert("Gagal mengunggah dokumen. Pastikan ukuran file di bawah 50 MB.");
            dz.removeFile(file);
          });
        }
      });
    }

  });
})();
