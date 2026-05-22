/* ================================================================
   AkreditasiRS Pro v5.0 — Premium Design System
   Mobile-first, Android-optimized, Dark Mode Native
   ================================================================ */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --sidebar-w: 272px;
  --topbar-h: 64px;

  /* Brand Palette — deep teal to cyan */
  --brand:        #0e7c72;
  --brand-mid:    #0d9488;
  --brand-dark:   #0a6560;
  --brand-light:  #5eead4;
  --brand-xlight: #f0fdfa;
  --brand-glow:   rgba(13,148,136,.18);
  --brand-2:      #0891b2;

  /* Surface */
  --bg:         #f1f5f9;
  --surface:    #ffffff;
  --surface-2:  #f8fafc;
  --surface-3:  #f1f5f9;
  --surface-4:  #e8f0fe;
  --border:     #e2e8f0;
  --border-2:   #cbd5e1;

  /* Text */
  --text-1: #0f172a;
  --text-2: #1e293b;
  --text-3: #475569;
  --text-4: #94a3b8;
  --text-5: #cbd5e1;

  /* Semantic */
  --red:       #ef4444; --red-mid: #dc2626; --red-dark: #b91c1c;
  --red-bg:    #fef2f2; --red-border: #fecaca;
  --yellow:    #f59e0b; --yellow-mid: #d97706;
  --yellow-bg: #fffbeb; --yellow-border: #fde68a;
  --green:     #10b981; --green-mid: #059669;
  --green-bg:  #ecfdf5; --green-border: #a7f3d0;
  --blue:      #3b82f6; --blue-mid: #2563eb;
  --blue-bg:   #eff6ff; --blue-border: #bfdbfe;
  --purple:    #8b5cf6; --purple-mid: #7c3aed;
  --purple-bg: #f5f3ff; --purple-border: #ddd6fe;
  --orange:    #f97316; --orange-mid: #ea580c;
  --orange-bg: #fff7ed; --orange-border: #fed7aa;
  --cyan:      #06b6d4; --cyan-mid: #0891b2;
  --cyan-bg:   #ecfeff; --cyan-border: #a5f3fc;
  --indigo:    #6366f1; --indigo-mid: #4f46e5;
  --indigo-bg: #eef2ff; --indigo-border: #c7d2fe;
  --pink:      #ec4899; --pink-mid: #db2777;
  --pink-bg:   #fdf2f8; --pink-border: #fbcfe8;

  /* Shadows */
  --shadow-xs: 0 1px 2px rgba(0,0,0,.04);
  --shadow-sm: 0 2px 4px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);
  --shadow:    0 4px 16px rgba(0,0,0,.08),0 2px 4px rgba(0,0,0,.04);
  --shadow-md: 0 8px 28px rgba(0,0,0,.10),0 3px 8px rgba(0,0,0,.05);
  --shadow-lg: 0 20px 60px rgba(0,0,0,.13),0 8px 20px rgba(0,0,0,.06);
  --shadow-xl: 0 32px 80px rgba(0,0,0,.18);
  --shadow-brand: 0 8px 24px rgba(14,124,114,.28);

  /* Radii */
  --r-xs: 4px; --r-sm: 8px; --r: 12px;
  --r-lg: 16px; --r-xl: 20px; --r-2xl: 28px;

  /* Transitions */
  --t: .18s cubic-bezier(.4,0,.2,1);
  --t-slow: .35s cubic-bezier(.4,0,.2,1);
  --t-spring: .4s cubic-bezier(.34,1.56,.64,1);
}

/* ── Dark Mode ── */
[data-theme="dark"] {
  --bg:       #0a0e1a;
  --surface:  #111827;
  --surface-2:#161e2e;
  --surface-3:#1c2537;
  --surface-4:#1a2642;
  --border:   #1f2937;
  --border-2: #283347;
  --text-1:   #f0f6ff;
  --text-2:   #cbd5e1;
  --text-3:   #8b9cb6;
  --text-4:   #4b5e7a;
  --text-5:   #2d3f58;
  --brand-xlight: #0f2d2a;
  --brand-glow: rgba(13,148,136,.22);
  --red-bg:    #1a0808; --yellow-bg: #1a1000;
  --green-bg:  #071a10; --blue-bg:   #060e22;
  --purple-bg: #100a1f; --orange-bg: #1a0a00;
  --cyan-bg:   #031218; --indigo-bg: #0a0d24;
  --pink-bg:   #1a0510;
  --shadow:    0 4px 16px rgba(0,0,0,.4);
  --shadow-md: 0 8px 28px rgba(0,0,0,.55);
  --shadow-lg: 0 20px 60px rgba(0,0,0,.65);
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-1);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
  max-width: 100vw;
}
/* Pastikan semua elemen tidak melebihi lebar viewport */
*, *::before, *::after { max-width: 100%; }
img, video, iframe { max-width: 100%; height: auto; }
/* Table tidak force lebar */
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; max-width: 100%; }
a { color: inherit; text-decoration: none; }
button { font-family: inherit; cursor: pointer; border: none; background: none; }
input, select, textarea { font-family: inherit; }
img { max-width: 100%; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-2); border-radius: 99px; }

/* ============================================================
   LAYOUT
   ============================================================ */
.layout { display: flex; min-height: 100vh; }

/* ── Sidebar Overlay (mobile) ── */
.sidebar-overlay {
  display: none;
  position: fixed; inset: 0;
  background: rgba(0,0,0,.55);
  backdrop-filter: blur(4px);
  z-index: 190;
  animation: fade-in .2s ease;
}
.sidebar-overlay.show { display: block; }

/* ── SIDEBAR ── */
.sidebar {
  width: var(--sidebar-w);
  min-height: 100vh;
  background: linear-gradient(180deg, #081c19 0%, #060d0b 60%, #040909 100%);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0; left: 0;
  z-index: 200;
  transition: transform var(--t-slow);
  overflow-y: auto;
  overflow-x: hidden;
  border-right: 1px solid rgba(255,255,255,.05);
  box-shadow: 4px 0 24px rgba(0,0,0,.25);
}

/* Sidebar decorative gradient line */
.sidebar::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, #0d9488, #06b6d4, #8b5cf6, #0d9488);
  background-size: 200% 100%;
  animation: shimmer 4s linear infinite;
}
@keyframes shimmer { 0% { background-position: 0% } 100% { background-position: 200% } }

/* ── Brand ── */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 22px 18px 18px;
  border-bottom: 1px solid rgba(255,255,255,.06);
  flex-shrink: 0;
  position: relative;
}
.brand-logo {
  width: 42px; height: 42px;
  background: linear-gradient(135deg, #0d9488, #0891b2);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 14px rgba(13,148,136,.45), 0 0 0 1px rgba(255,255,255,.1);
  position: relative;
  overflow: hidden;
}
.brand-logo::after {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,.12) 50%, transparent 60%);
  animation: logo-shine 3s ease-in-out infinite;
}
@keyframes logo-shine { 0%,100% { transform: translateX(-100%) } 50% { transform: translateX(100%) } }
.brand-logo svg { color: #fff; width: 20px; height: 20px; position: relative; z-index: 1; }
.brand-name { font-size: 14px; font-weight: 800; color: #fff; letter-spacing: -.3px; }
.brand-ver {
  font-size: 10px;
  color: rgba(255,255,255,.3);
  margin-top: 1px;
  font-family: 'JetBrains Mono', monospace;
}

/* ── Nav Sections ── */
.sidebar-section { padding: 14px 10px 4px; }
.sidebar-label {
  font-size: 9.5px;
  font-weight: 800;
  color: rgba(255,255,255,.18);
  letter-spacing: .14em;
  text-transform: uppercase;
  padding: 4px 10px 4px;
  margin-bottom: 2px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 11px;
  color: rgba(255,255,255,.5);
  border-radius: 10px;
  margin-bottom: 2px;
  transition: all var(--t);
  font-size: 13px;
  font-weight: 500;
  position: relative;
  letter-spacing: -.1px;
}
.nav-item svg {
  width: 17px; height: 17px;
  flex-shrink: 0;
  opacity: .65;
  transition: opacity var(--t);
}
.nav-item:hover {
  background: rgba(255,255,255,.08);
  color: rgba(255,255,255,.9);
  transform: translateX(2px);
}
.nav-item:hover svg { opacity: 1; }
.nav-item.active {
  background: linear-gradient(135deg, rgba(13,148,136,.35), rgba(8,145,178,.2));
  color: #fff;
  font-weight: 700;
  box-shadow: 0 2px 12px rgba(13,148,136,.2);
}
.nav-item.active svg { opacity: 1; }
.nav-item.active::before {
  content: '';
  position: absolute;
  left: -1px; top: 20%; height: 60%; width: 3px;
  background: linear-gradient(180deg, #0d9488, #06b6d4);
  border-radius: 0 3px 3px 0;
}
.nav-badge {
  margin-left: auto;
  font-size: 10px; font-weight: 800;
  background: var(--red);
  color: #fff;
  border-radius: 99px;
  padding: 1px 6px;
  min-width: 18px;
  text-align: center;
  animation: pulse 2s infinite;
}

/* ── Sidebar Footer ── */
.sidebar-footer {
  margin-top: auto;
  padding: 12px 10px;
  border-top: 1px solid rgba(255,255,255,.06);
  flex-shrink: 0;
}
.user-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 11px;
  border-radius: 10px;
  background: rgba(255,255,255,.06);
  margin-bottom: 6px;
  transition: all var(--t);
  cursor: pointer;
}
.user-card:hover { background: rgba(255,255,255,.1); }
.user-avatar {
  width: 34px; height: 34px;
  border-radius: 10px;
  background: linear-gradient(135deg, #0d9488, #0891b2);
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 800; color: #fff;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(13,148,136,.3);
}
.user-info-name { font-size: 12.5px; font-weight: 700; color: #fff; }
.user-info-role {
  font-size: 10px;
  color: rgba(255,255,255,.35);
  margin-top: 1px;
}
.btn-logout {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 11px;
  border-radius: 10px;
  color: rgba(255,255,255,.4);
  font-size: 12.5px; font-weight: 500;
  transition: all var(--t);
  width: 100%;
}
.btn-logout svg { width: 14px; height: 14px; }
.btn-logout:hover {
  background: rgba(239,68,68,.15);
  color: #fca5a5;
}

/* ── MAIN CONTENT ── */
.main {
  flex: 1;
  margin-left: var(--sidebar-w);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: margin-left var(--t-slow);
}

/* ── TOPBAR ── */
.topbar {
  height: var(--topbar-h);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center;
  padding: 0 24px;
  gap: 14px;
  position: sticky; top: 0; z-index: 100;
  box-shadow: var(--shadow-xs);
  backdrop-filter: blur(12px);
  background: rgba(var(--surface-rgb, 255,255,255), .95);
}
.btn-menu {
  display: none;
  align-items: center; justify-content: center;
  width: 38px; height: 38px;
  border-radius: 10px;
  color: var(--text-3);
  transition: all var(--t);
}
.btn-menu:hover { background: var(--surface-2); color: var(--text-1); }
.btn-menu svg { width: 20px; height: 20px; }
.topbar-title {
  font-size: 16px; font-weight: 800;
  color: var(--text-1);
  flex: 1;
  letter-spacing: -.3px;
}
.topbar-right { display: flex; align-items: center; gap: 8px; }
.icon-btn {
  width: 36px; height: 36px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-3);
  background: var(--surface-2);
  border: 1.5px solid var(--border);
  transition: all var(--t);
  position: relative;
  cursor: pointer;
}
.icon-btn svg { width: 17px; height: 17px; }
.icon-btn:hover {
  background: var(--brand-xlight);
  color: var(--brand);
  border-color: var(--brand-light);
  transform: scale(1.05);
}
.notif-dot {
  position: absolute; top: 6px; right: 6px;
  width: 8px; height: 8px;
  background: var(--red);
  border-radius: 50%;
  border: 2px solid var(--surface);
  animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.25)} }
.role-pill {
  display: inline-flex; align-items: center;
  padding: 4px 12px;
  border-radius: 99px;
  font-size: 11px; font-weight: 800;
  letter-spacing: .06em;
  text-transform: uppercase;
}
.role-admin { background: linear-gradient(135deg,#0f766e,#0891b2); color: #fff; box-shadow: 0 2px 8px rgba(14,124,114,.3); }
.role-ketua_pokja { background: var(--purple-bg); color: var(--purple-mid); border: 1.5px solid var(--purple-border); }
.role-pegawai { background: var(--blue-bg); color: var(--blue-mid); border: 1.5px solid var(--blue-border); }

/* ── Content ── */
.content { flex: 1; padding: 24px; }

/* ── Notifications Dropdown ── */
.notif-dropdown {
  position: absolute; top: calc(100% + 10px); right: 0;
  width: 360px;
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--r-xl);
  box-shadow: var(--shadow-lg);
  z-index: 400; display: none;
  overflow: hidden;
  animation: pop-in .2s ease;
}
.notif-dropdown.open { display: block; }
.notif-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  background: var(--surface-2);
}
.notif-title { font-size: 13.5px; font-weight: 800; }
.notif-item {
  display: flex; gap: 10px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  transition: background var(--t);
}
.notif-item:hover { background: var(--surface-2); }
.notif-item.unread { background: var(--brand-xlight); }
.notif-icon-box {
  width: 34px; height: 34px;
  border-radius: 50%;
  background: var(--brand-xlight);
  color: var(--brand);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.notif-icon-box svg { width: 14px; height: 14px; }
.notif-msg { font-size: 12.5px; color: var(--text-1); line-height: 1.4; }
.notif-time { font-size: 10.5px; color: var(--text-4); margin-top: 3px; }

/* ============================================================
   COMPONENTS
   ============================================================ */

/* ── Cards ── */
.card {
  background: var(--surface);
  border-radius: var(--r-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-xs);
  overflow: hidden;
  transition: box-shadow var(--t);
}
.card:hover { box-shadow: var(--shadow-sm); }
.card-body { padding: 20px; }
.card-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  background: var(--surface-2);
}
.card-title {
  font-size: 13.5px; font-weight: 800;
  color: var(--text-1);
  display: flex; align-items: center; gap: 8px;
  letter-spacing: -.2px;
}
.card-title svg { width: 16px; height: 16px; color: var(--brand); }

/* ── Stat Cards — Dashboard ── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card {
  background: var(--surface);
  border-radius: var(--r-lg);
  border: 1px solid var(--border);
  padding: 20px;
  position: relative;
  overflow: hidden;
  transition: all var(--t);
  box-shadow: var(--shadow-xs);
  cursor: default;
}
.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  border-radius: var(--r-lg) var(--r-lg) 0 0;
}
.stat-card::after {
  content: '';
  position: absolute;
  top: -20px; right: -20px;
  width: 100px; height: 100px;
  border-radius: 50%;
  opacity: .07;
}
.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}
.stat-card.c-blue::before { background: linear-gradient(90deg,var(--blue),var(--indigo)); }
.stat-card.c-blue::after  { background: var(--blue); }
.stat-card.c-green::before { background: linear-gradient(90deg,var(--green),var(--cyan)); }
.stat-card.c-green::after  { background: var(--green); }
.stat-card.c-purple::before { background: linear-gradient(90deg,var(--purple),var(--pink)); }
.stat-card.c-purple::after  { background: var(--purple); }
.stat-card.c-yellow::before { background: linear-gradient(90deg,var(--yellow),var(--orange)); }
.stat-card.c-yellow::after  { background: var(--yellow); }
.stat-card.c-orange::before { background: linear-gradient(90deg,var(--orange),var(--red)); }
.stat-card.c-orange::after  { background: var(--orange); }
.stat-card.c-red::before { background: linear-gradient(90deg,var(--red),var(--pink)); }
.stat-card.c-red::after  { background: var(--red); }
.stat-card.c-brand::before { background: linear-gradient(90deg,var(--brand-mid),var(--brand-2)); }
.stat-card.c-brand::after  { background: var(--brand-mid); }
.stat-top {
  display: flex; align-items: flex-start; justify-content: space-between;
}
.stat-icon-box {
  width: 46px; height: 46px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.stat-icon-box svg { width: 22px; height: 22px; }
.stat-card.c-blue .stat-icon-box   { background:var(--blue-bg);color:var(--blue-mid); }
.stat-card.c-green .stat-icon-box  { background:var(--green-bg);color:var(--green-mid); }
.stat-card.c-purple .stat-icon-box { background:var(--purple-bg);color:var(--purple-mid); }
.stat-card.c-yellow .stat-icon-box { background:var(--yellow-bg);color:var(--yellow-mid); }
.stat-card.c-orange .stat-icon-box { background:var(--orange-bg);color:var(--orange-mid); }
.stat-card.c-red .stat-icon-box    { background:var(--red-bg);color:var(--red-mid); }
.stat-card.c-brand .stat-icon-box  { background:var(--brand-xlight);color:var(--brand); }
.stat-val {
  font-size: 30px; font-weight: 800;
  color: var(--text-1);
  line-height: 1.1;
  letter-spacing: -1px;
  font-variant-numeric: tabular-nums;
}
.stat-lbl { font-size: 12.5px; font-weight: 700; color: var(--text-2); margin-top: 4px; }
.stat-sub { font-size: 11px; color: var(--text-4); margin-top: 2px; }
.stat-progress {
  height: 5px; background: var(--border);
  border-radius: 99px; margin-top: 14px; overflow: hidden;
}
.stat-progress-fill {
  height: 100%; border-radius: 99px;
  background: var(--green);
  transition: width .9s cubic-bezier(.4,0,.2,1);
}
.stat-trend {
  display: inline-flex; align-items: center; gap: 3px;
  font-size: 11px; font-weight: 700;
  padding: 2px 7px;
  border-radius: 99px;
  margin-top: 4px;
}
.stat-trend.up { background: var(--green-bg); color: var(--green-mid); }
.stat-trend.down { background: var(--red-bg); color: var(--red-mid); }
.stat-trend svg { width: 11px; height: 11px; }

/* ── Grids ── */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.grid-3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; }
.grid-70-30 { display: grid; grid-template-columns: 1fr 320px; gap: 20px; }
.mb-16{margin-bottom:16px} .mb-20{margin-bottom:20px}
.mb-24{margin-bottom:24px} .mb-28{margin-bottom:28px}

/* ── Buttons ── */
.btn {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 9px 18px;
  border-radius: 10px;
  font-size: 13px; font-weight: 700;
  cursor: pointer;
  transition: all var(--t);
  border: 1.5px solid transparent;
  white-space: nowrap;
  line-height: 1.4;
  letter-spacing: -.1px;
}
.btn svg { width: 15px; height: 15px; flex-shrink: 0; }
.btn:active { transform: scale(.96); }
.btn-primary {
  background: var(--brand);
  color: #fff;
  border-color: var(--brand-dark);
  box-shadow: 0 2px 10px rgba(14,124,114,.3);
}
.btn-primary:hover {
  background: var(--brand-dark);
  box-shadow: var(--shadow-brand);
  transform: translateY(-1px);
}
.btn-secondary {
  background: var(--surface);
  color: var(--text-2);
  border-color: var(--border-2);
}
.btn-secondary:hover {
  background: var(--surface-2);
  border-color: var(--brand);
  color: var(--brand);
}
.btn-ghost {
  background: transparent;
  color: var(--text-3);
  border-color: transparent;
}
.btn-ghost:hover { background: var(--surface-2); color: var(--text-1); }
.btn-danger {
  background: var(--red);
  color: #fff;
  border-color: var(--red-mid);
  box-shadow: 0 2px 10px rgba(239,68,68,.25);
}
.btn-danger:hover { background: var(--red-dark); }
.btn-success {
  background: var(--green);
  color: #fff;
  border-color: var(--green-mid);
}
.btn-success:hover { background: var(--green-mid); }
.btn-sm { padding: 6px 13px; font-size: 12px; border-radius: 8px; }
.btn-lg { padding: 11px 22px; font-size: 14.5px; }
.btn-full { width: 100%; justify-content: center; }
.btn-icon { width: 34px; height: 34px; padding: 0; justify-content: center; border-radius: 9px; }

/* ── Forms ── */
.form-group { margin-bottom: 16px; }
.form-label {
  display: block;
  font-size: 12.5px; font-weight: 700;
  color: var(--text-2); margin-bottom: 6px;
  letter-spacing: -.1px;
}
.form-label .req { color: var(--red); margin-left: 2px; }
.form-hint { font-size: 11px; color: var(--text-4); margin-top: 4px; }
input[type=text],input[type=password],input[type=email],input[type=number],input[type=search],select,textarea {
  width: 100%;
  padding: 9px 13px;
  border: 1.5px solid var(--border-2);
  border-radius: 10px;
  background: var(--surface);
  color: var(--text-1);
  font-size: 13.5px;
  transition: all var(--t);
  outline: none;
  -webkit-appearance: none;
}
input:focus,select:focus,textarea:focus {
  border-color: var(--brand);
  box-shadow: 0 0 0 4px var(--brand-glow);
}
input::placeholder,textarea::placeholder { color: var(--text-4); }
textarea { resize: vertical; min-height: 90px; }
.input-with-icon { position: relative; }
.input-icon {
  position: absolute; left: 11px; top: 50%;
  transform: translateY(-50%);
  color: var(--text-4); pointer-events: none;
  display: flex; align-items: center;
}
.input-icon svg { width: 15px; height: 15px; }
.input-with-icon input { padding-left: 36px; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }
.col-span-2{grid-column:span 2} .col-span-3{grid-column:span 3}

/* ── Tables ── */
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table thead th {
  background: var(--surface-2);
  padding: 11px 14px;
  text-align: left;
  font-size: 11px; font-weight: 800;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: .07em;
  border-bottom: 2px solid var(--border);
  white-space: nowrap;
}
.data-table tbody tr {
  border-bottom: 1px solid var(--border);
  transition: background var(--t);
}
.data-table tbody tr:hover { background: var(--surface-2); }
.data-table tbody tr:last-child { border-bottom: none; }
.data-table tbody td { padding: 11px 14px; color: var(--text-2); vertical-align: middle; }
.data-table td[data-label="Aksi"] > div,
.data-table td[data-label="Aksi"] { overflow: visible; }
.data-table .td-main { font-weight: 700; color: var(--text-1); }
.data-table .td-muted { color: var(--text-4); font-size: 12px; }
.td-clamp { max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

/* ── Badges ── */
.badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 9px;
  border-radius: 99px;
  font-size: 11px; font-weight: 700;
  white-space: nowrap;
}
.badge svg { width: 10px; height: 10px; }
.badge-teal   {background:var(--brand-xlight);color:var(--brand-dark);border:1px solid var(--brand-light);}
.badge-blue   {background:var(--blue-bg);color:var(--blue-mid);border:1px solid var(--blue-border);}
.badge-green  {background:var(--green-bg);color:var(--green-mid);border:1px solid var(--green-border);}
.badge-red    {background:var(--red-bg);color:var(--red-mid);border:1px solid var(--red-border);}
.badge-yellow {background:var(--yellow-bg);color:var(--yellow-mid);border:1px solid var(--yellow-border);}
.badge-purple {background:var(--purple-bg);color:var(--purple-mid);border:1px solid var(--purple-border);}
.badge-orange {background:var(--orange-bg);color:var(--orange-mid);border:1px solid var(--orange-border);}
.badge-gray   {background:var(--surface-3);color:var(--text-3);border:1px solid var(--border);}
.badge-cyan   {background:var(--cyan-bg);color:var(--cyan-mid);border:1px solid var(--cyan-border);}
.badge-indigo {background:var(--indigo-bg);color:var(--indigo-mid);border:1px solid var(--indigo-border);}
.badge-pink   {background:var(--pink-bg);color:var(--pink-mid);border:1px solid var(--pink-border);}

/* ── File type icons ── */
.file-icon {
  display: inline-flex; align-items: center; justify-content: center;
  width: 32px; height: 32px;
  border-radius: 8px;
  font-size: 9px; font-weight: 900;
  flex-shrink: 0;
  letter-spacing: 0;
}
.fi-pdf  {background:#fee2e2;color:#b91c1c}
.fi-doc,.fi-docx {background:#dbeafe;color:#1d4ed8}
.fi-xls,.fi-xlsx {background:#d1fae5;color:#065f46}
.fi-ppt,.fi-pptx {background:#ffedd5;color:#c2410c}
.fi-jpg,.fi-jpeg,.fi-png {background:#f3e8ff;color:#7c3aed}
.fi-zip,.fi-rar  {background:#fef3c7;color:#b45309}
.fi-txt  {background:#f0f9ff;color:#0369a1}
.fi-def  {background:var(--surface-2);color:var(--text-3)}

/* ── Alerts ── */
.alert {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 13px 16px;
  border-radius: 12px;
  font-size: 13px;
  margin-bottom: 14px;
  animation: slide-down .25s ease;
  border: 1px solid;
}
@keyframes slide-down { from{opacity:0;transform:translateY(-10px)} to{opacity:1;transform:none} }
.alert svg { width: 16px; height: 16px; flex-shrink: 0; margin-top: 2px; }
.alert-body { flex: 1; line-height: 1.5; }
.alert-close {
  background: none; border: none; cursor: pointer;
  opacity: .5; margin-left: auto; flex-shrink: 0;
  color: inherit; display: flex; align-items: center;
  transition: opacity var(--t);
}
.alert-close:hover { opacity: 1; }
.alert-close svg { width: 15px; height: 15px; }
.alert-success {background:var(--green-bg);color:#065f46;border-color:var(--green-border);border-left:4px solid var(--green);}
.alert-danger  {background:var(--red-bg);color:#7f1d1d;border-color:var(--red-border);border-left:4px solid var(--red);}
.alert-warning {background:var(--yellow-bg);color:#78350f;border-color:var(--yellow-border);border-left:4px solid var(--yellow);}
.alert-info    {background:var(--blue-bg);color:#1e3a5f;border-color:var(--blue-border);border-left:4px solid var(--blue);}

/* ── Modal ── */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,.6);
  backdrop-filter: blur(6px);
  display: flex; align-items: center; justify-content: center;
  z-index: 500;
  animation: fade-in .2s ease;
}
@keyframes fade-in { from{opacity:0} to{opacity:1} }
.modal {
  background: var(--surface);
  border-radius: var(--r-2xl);
  padding: 28px;
  width: min(540px, calc(100vw - 24px));
  max-height: calc(100vh - 48px);
  max-height: calc(var(--vh, 1vh) * 100 - 48px);
  overflow-y: auto;
  overflow-x: hidden;
  box-shadow: var(--shadow-xl);
  animation: pop-in .28s cubic-bezier(.34,1.56,.64,1);
  border: 1px solid var(--border);
}
@keyframes pop-in { from{opacity:0;transform:scale(.9) translateY(16px)} to{opacity:1;transform:none} }
.modal-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 22px;
}
.modal-title {
  font-size: 16px; font-weight: 800;
  color: var(--text-1);
  display: flex; align-items: center; gap: 8px;
}
.modal-title svg { width: 18px; height: 18px; color: var(--brand); }
.modal-close {
  background: var(--surface-2);
  border: 1.5px solid var(--border);
  width: 32px; height: 32px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: var(--text-3);
  transition: all var(--t);
}
.modal-close svg { width: 15px; height: 15px; }
.modal-close:hover { background: var(--red-bg); color: var(--red); border-color: var(--red-border); }

/* ── Login ── */
.login-page {
  min-height: 100vh;
  display: flex;
  position: relative;
  overflow: hidden;
}
.login-left {
  flex: 1;
  background: linear-gradient(145deg, #071c19 0%, #080d20 50%, #060c1a 100%);
  display: flex; flex-direction: column;
  align-items: flex-start; justify-content: center;
  padding: 60px;
  position: relative;
  z-index: 1;
  overflow: hidden;
}
.login-left::before {
  content: '';
  position: absolute;
  width: 500px; height: 500px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(13,148,136,.25), transparent 70%);
  top: -150px; right: -100px; z-index: 0;
}
.login-left::after {
  content: '';
  position: absolute;
  width: 350px; height: 350px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(99,102,241,.15), transparent 70%);
  bottom: -80px; left: 40px; z-index: 0;
}
/* Animated grid lines in login bg */
.login-grid {
  position: absolute; inset: 0; z-index: 0;
  background-image:
    linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
  background-size: 40px 40px;
}
.login-right {
  width: 460px;
  background: var(--surface);
  display: flex; align-items: center; justify-content: center;
  padding: 52px 48px;
  box-shadow: -24px 0 80px rgba(0,0,0,.18);
}
.login-brand {
  display: flex; align-items: center; gap: 13px;
  margin-bottom: 52px;
  position: relative; z-index: 1;
}
.login-brand-logo {
  width: 50px; height: 50px;
  background: linear-gradient(135deg, #0d9488, #0891b2);
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 6px 20px rgba(13,148,136,.4);
}
.login-brand-logo svg { width: 26px; height: 26px; color: #fff; }
.login-brand-name { font-size: 21px; font-weight: 900; color: #fff; letter-spacing: -.5px; }
.login-brand-sub { font-size: 11px; color: rgba(255,255,255,.35); margin-top: 2px; }
.login-hero { position: relative; z-index: 1; }
.login-hero-title { font-size: 36px; font-weight: 900; color: #fff; line-height: 1.1; margin-bottom: 16px; letter-spacing: -1px; }
.login-hero-title span { color: var(--brand-light); }
.login-hero-sub { font-size: 15px; color: rgba(255,255,255,.5); line-height: 1.75; max-width: 360px; }
.login-features {
  display: flex; flex-direction: column; gap: 16px;
  margin-top: 48px;
  position: relative; z-index: 1;
}
.login-feat { display: flex; align-items: center; gap: 13px; }
.login-feat-icon {
  width: 38px; height: 38px;
  background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.login-feat-icon svg { width: 17px; height: 17px; color: var(--brand-light); }
.login-feat-text { font-size: 14px; color: rgba(255,255,255,.7); font-weight: 500; }
.login-form-wrap { width: 100%; }
.login-form-title { font-size: 26px; font-weight: 900; color: var(--text-1); margin-bottom: 4px; letter-spacing: -.5px; }
.login-form-sub { font-size: 13.5px; color: var(--text-4); margin-bottom: 30px; }
.pw-wrap { position: relative; }
.pw-wrap input { padding-right: 42px; }
.pw-toggle {
  position: absolute; right: 11px; top: 50%;
  transform: translateY(-50%);
  color: var(--text-4); transition: color var(--t);
  display: flex; align-items: center;
  background: none; border: none; cursor: pointer; padding: 0;
}
.pw-toggle svg { width: 16px; height: 16px; }
.pw-toggle:hover { color: var(--text-2); }
.login-divider {
  display: flex; align-items: center; gap: 12px;
  color: var(--text-4); font-size: 12px;
  margin: 20px 0;
}
.login-divider::before, .login-divider::after {
  content: ''; flex: 1; height: 1px;
  background: var(--border);
}
.login-demo {
  padding: 12px 14px;
  background: var(--surface-2);
  border: 1.5px solid var(--border);
  border-radius: 10px;
  font-size: 12px; color: var(--text-3);
  text-align: center; margin-top: 18px;
  line-height: 1.6;
}
.login-demo strong {
  color: var(--brand);
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
}
.login-security {
  display: flex; align-items: center; gap: 5px;
  font-size: 11px; color: var(--text-4);
  justify-content: center; margin-top: 16px;
}
.login-security svg { width: 12px; height: 12px; }

/* ── Dashboard: Reminder Cards ── */
.reminder-list { display: flex; flex-direction: column; gap: 10px; padding: 16px; }
.reminder-card {
  padding: 14px 16px;
  border-radius: 12px;
  border: 1.5px solid;
  transition: all var(--t);
  cursor: pointer;
}
.reminder-card:hover { transform: translateX(4px); box-shadow: var(--shadow-sm); }
.reminder-card.rem-red {
  background: var(--red-bg);
  border-color: var(--red-border);
}
.reminder-card.rem-yellow {
  background: var(--yellow-bg);
  border-color: var(--yellow-border);
}
.reminder-card.rem-green {
  background: var(--green-bg);
  border-color: var(--green-border);
}
.rem-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px; }
.rem-kode { font-weight: 900; font-size: 13px; font-family: 'JetBrains Mono', monospace; }
.rem-count { font-size: 12px; font-weight: 800; }
.rem-nama { font-size: 12.5px; font-weight: 600; margin-bottom: 2px; }
.rem-pokja { font-size: 10.5px; color: var(--text-4); margin-bottom: 8px; }
.rem-bar { height: 5px; background: rgba(0,0,0,.1); border-radius: 99px; overflow: hidden; }
.rem-bar-fill { height: 100%; border-radius: 99px; opacity: .65; transition: width .7s ease; }

/* ── Activity Feed ── */
.activity-list { padding: 4px 0; }
.activity-item {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 11px 20px;
  border-bottom: 1px solid var(--border);
  transition: background var(--t);
}
.activity-item:last-child { border-bottom: none; }
.activity-item:hover { background: var(--surface-2); }
.act-icon {
  width: 34px; height: 34px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; margin-top: 1px;
}
.act-icon svg { width: 15px; height: 15px; }
.act-icon.login    {background:var(--green-bg);color:var(--green-mid);}
.act-icon.upload   {background:var(--blue-bg);color:var(--blue-mid);}
.act-icon.download {background:var(--purple-bg);color:var(--purple-mid);}
.act-icon.delete   {background:var(--red-bg);color:var(--red-mid);}
.act-icon.create   {background:var(--green-bg);color:var(--green-mid);}
.act-icon.toggle   {background:var(--yellow-bg);color:var(--yellow-mid);}
.act-icon.export   {background:var(--cyan-bg);color:var(--cyan-mid);}
.act-icon.default  {background:var(--surface-2);color:var(--text-3);}
.act-content { flex: 1; min-width: 0; }
.act-title { font-size: 12.5px; color: var(--text-1); line-height: 1.45; }
.act-title strong { font-weight: 800; }
.act-meta { font-size: 11px; color: var(--text-4); margin-top: 2px; font-family: 'JetBrains Mono', monospace; }
.act-time { font-size: 10.5px; color: var(--text-4); flex-shrink: 0; white-space: nowrap; padding-top: 3px; }

/* ── Pagination ── */
.pagination {
  display: flex; align-items: center; justify-content: center;
  gap: 6px; padding: 16px 0;
}
.page-btn {
  width: 34px; height: 34px;
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700;
  color: var(--text-3);
  border: 1.5px solid var(--border);
  background: var(--surface);
  transition: all var(--t);
  cursor: pointer;
}
.page-btn:hover { border-color: var(--brand); color: var(--brand); }
.page-btn.active {
  background: var(--brand);
  color: #fff;
  border-color: var(--brand);
  box-shadow: 0 2px 8px rgba(14,124,114,.3);
}
.page-btn:disabled { opacity: .4; cursor: not-allowed; }

/* ── Upload Dropzone ── */
.dropzone {
  border: 2px dashed var(--border-2);
  border-radius: var(--r-lg);
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all var(--t);
  background: var(--surface-2);
  position: relative;
}
.dropzone:hover, .dropzone.dragover {
  border-color: var(--brand);
  background: var(--brand-xlight);
}
.dropzone-icon {
  width: 60px; height: 60px;
  border-radius: 16px;
  background: var(--surface);
  border: 2px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
  transition: all var(--t);
}
.dropzone:hover .dropzone-icon, .dropzone.dragover .dropzone-icon {
  border-color: var(--brand);
  color: var(--brand);
  transform: scale(1.08);
}
.dropzone-icon svg { width: 28px; height: 28px; color: var(--text-3); }
.dropzone-title { font-size: 15px; font-weight: 700; color: var(--text-1); }
.dropzone-sub { font-size: 12.5px; color: var(--text-4); margin-top: 4px; }
.dropzone-types {
  display: flex; flex-wrap: wrap; justify-content: center;
  gap: 6px; margin-top: 14px;
}
.dropzone-type-pill {
  padding: 2px 9px;
  border-radius: 99px;
  background: var(--surface);
  border: 1px solid var(--border);
  font-size: 11px; font-weight: 700;
  color: var(--text-3);
}

/* ── Empty State ── */
.empty-state {
  padding: 48px 24px;
  text-align: center;
}
.empty-state-icon {
  width: 64px; height: 64px;
  border-radius: 16px;
  background: var(--surface-2);
  border: 1.5px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
}
.empty-state-icon svg { width: 28px; height: 28px; color: var(--text-4); }
.empty-state-title { font-size: 15px; font-weight: 800; color: var(--text-2); }
.empty-state-sub { font-size: 13px; color: var(--text-4); margin-top: 6px; line-height: 1.6; }

/* ── Filter Bar ── */
.filter-bar {
  display: flex; flex-wrap: wrap; gap: 10px; align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  background: var(--surface-2);
}
.filter-bar select, .filter-bar input {
  width: auto; min-width: 120px; flex: 1;
}

/* ── Compliance Progress ── */
.compliance-bar {
  height: 8px;
  background: var(--border);
  border-radius: 99px;
  overflow: hidden;
}
.compliance-fill {
  height: 100%;
  border-radius: 99px;
  transition: width .8s ease;
}
.compliance-fill.high   { background: linear-gradient(90deg, #10b981, #06b6d4); }
.compliance-fill.medium { background: linear-gradient(90deg, #f59e0b, #f97316); }
.compliance-fill.low    { background: linear-gradient(90deg, #ef4444, #ec4899); }

/* ── Section Header ── */
.section-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 20px;
}
.section-title { font-size: 18px; font-weight: 900; color: var(--text-1); letter-spacing: -.4px; }
.section-sub { font-size: 13px; color: var(--text-4); margin-top: 3px; }

/* ── Stats mini chips ── */
.mini-stat-row {
  display: flex; gap: 8px; flex-wrap: wrap;
  margin-bottom: 20px;
}
.mini-stat {
  display: flex; align-items: center; gap: 7px;
  padding: 8px 14px;
  border-radius: 99px;
  font-size: 12.5px; font-weight: 700;
  border: 1.5px solid;
}

/* ── Compliance overview stats ── */
.compliance-overview {
  display: flex; gap: 0;
  border: 1.5px solid var(--border);
  border-radius: var(--r-lg);
  overflow: hidden;
  margin-bottom: 20px;
  background: var(--surface);
}
.comp-stat {
  flex: 1; padding: 18px 16px; text-align: center;
  border-right: 1px solid var(--border);
}
.comp-stat:last-child { border-right: none; }
.comp-stat-val { font-size: 26px; font-weight: 900; letter-spacing: -1px; }
.comp-stat-lbl { font-size: 11px; font-weight: 700; color: var(--text-4); text-transform: uppercase; letter-spacing: .06em; margin-top: 3px; }

/* ── Search ── */
.search-input-wrap {
  position: relative; flex: 1; min-width: 200px;
}
.search-input-wrap input { padding-left: 38px; }
.search-icon {
  position: absolute; left: 12px; top: 50%;
  transform: translateY(-50%);
  color: var(--text-4);
  pointer-events: none;
}
.search-icon svg { width: 15px; height: 15px; }

/* ── Profile ── */
.profile-header {
  background: linear-gradient(135deg, #071c19, #060e22);
  border-radius: var(--r-xl);
  padding: 32px;
  display: flex; align-items: center; gap: 20px;
  margin-bottom: 24px;
  position: relative; overflow: hidden;
}
.profile-header::before {
  content: ''; position: absolute;
  width: 250px; height: 250px;
  border-radius: 50%;
  background: radial-gradient(circle,rgba(13,148,136,.2),transparent 70%);
  top: -80px; right: -60px;
}
.profile-avatar-lg {
  width: 70px; height: 70px;
  border-radius: 18px;
  background: linear-gradient(135deg, #0d9488, #0891b2);
  display: flex; align-items: center; justify-content: center;
  font-size: 28px; font-weight: 900; color: #fff;
  flex-shrink: 0;
  box-shadow: 0 6px 20px rgba(13,148,136,.35);
  border: 3px solid rgba(255,255,255,.15);
}
.profile-name { font-size: 20px; font-weight: 900; color: #fff; }
.profile-role { font-size: 13px; color: rgba(255,255,255,.5); margin-top: 4px; }
.profile-stats {
  display: flex; gap: 20px; margin-top: 12px;
}
.profile-stat-item { text-align: center; }
.profile-stat-val { font-size: 20px; font-weight: 900; color: #fff; }
.profile-stat-lbl { font-size: 10.5px; color: rgba(255,255,255,.4); }

/* ── Audit log action badges ── */
.action-badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 9px;
  border-radius: 99px;
  font-size: 10.5px; font-weight: 800;
  letter-spacing: .04em;
  font-family: 'JetBrains Mono', monospace;
}
.ab-login   {background:var(--green-bg);color:var(--green-mid);border:1px solid var(--green-border);}
.ab-logout  {background:var(--surface-3);color:var(--text-3);border:1px solid var(--border);}
.ab-upload  {background:var(--blue-bg);color:var(--blue-mid);border:1px solid var(--blue-border);}
.ab-download{background:var(--purple-bg);color:var(--purple-mid);border:1px solid var(--purple-border);}
.ab-delete  {background:var(--red-bg);color:var(--red-mid);border:1px solid var(--red-border);}
.ab-create  {background:var(--green-bg);color:var(--green-mid);border:1px solid var(--green-border);}
.ab-toggle  {background:var(--yellow-bg);color:var(--yellow-mid);border:1px solid var(--yellow-border);}
.ab-export  {background:var(--cyan-bg);color:var(--cyan-mid);border:1px solid var(--cyan-border);}
.ab-default {background:var(--surface-3);color:var(--text-3);border:1px solid var(--border);}

/* ── Progress Ring (SVG) ── */
.progress-ring { transform: rotate(-90deg); }
.progress-ring-bg { fill: none; stroke: var(--border); stroke-width: 5; }
.progress-ring-fill { fill: none; stroke-width: 5; stroke-linecap: round; transition: stroke-dashoffset 1s ease; }

/* ── Dashboard — quick action ── */
.quick-actions { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 24px; }
.quick-action-btn {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 8px; padding: 16px 20px;
  border-radius: var(--r-lg);
  border: 1.5px solid var(--border);
  background: var(--surface);
  color: var(--text-2);
  font-size: 12.5px; font-weight: 700;
  cursor: pointer; transition: all var(--t);
  min-width: 100px;
  text-align: center;
  box-shadow: var(--shadow-xs);
}
.quick-action-btn svg { width: 22px; height: 22px; }
.quick-action-btn:hover {
  border-color: var(--brand);
  color: var(--brand);
  background: var(--brand-xlight);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

/* ── Error page ── */
.error-page {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  background: var(--bg);
}
.error-card {
  background: var(--surface);
  border-radius: var(--r-2xl);
  padding: 48px;
  text-align: center;
  max-width: 460px;
  width: 90%;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border);
}
.error-code {
  font-size: 80px; font-weight: 900;
  background: linear-gradient(135deg,#0d9488,#0891b2);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  line-height: 1;
}

/* ============================================================
   RESPONSIVE — Mobile First
   ============================================================ */
@media (max-width: 1024px) {
  .grid-70-30 { grid-template-columns: 1fr; }
  .login-left { display: none; }
  .login-right { width: 100%; padding: 40px 28px; }
}

@media (max-width: 768px) {
  :root { --sidebar-w: 272px; --topbar-h: 58px; }

  /* Sidebar hides off-screen on mobile */
  .sidebar {
    transform: translateX(-100%);
    box-shadow: none;
  }
  .sidebar.open {
    transform: translateX(0);
    box-shadow: 6px 0 40px rgba(0,0,0,.35);
  }

  /* Main takes full width */
  .main { margin-left: 0; }

  /* Show hamburger */
  .btn-menu { display: flex; }

  .content { padding: 16px; }

  .grid-2 { grid-template-columns: 1fr; }
  .grid-3 { grid-template-columns: 1fr 1fr; }
  .form-row-2 { grid-template-columns: 1fr; }
  .form-row-3 { grid-template-columns: 1fr; }
  .col-span-2 { grid-column: span 1; }
  .col-span-3 { grid-column: span 1; }

  .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .stat-val { font-size: 24px; }

  .section-header { flex-direction: column; align-items: flex-start; gap: 10px; }

  .filter-bar { flex-direction: column; align-items: stretch; }
  .filter-bar select, .filter-bar input { width: 100%; }

  .profile-header { flex-direction: column; text-align: center; padding: 24px; }
  .profile-header::before { display: none; }
  .profile-stats { justify-content: center; }

  .compliance-overview { flex-direction: column; }
  .comp-stat { border-right: none; border-bottom: 1px solid var(--border); }

  .modal { padding: 22px; border-radius: var(--r-xl); }

  .notif-dropdown { width: calc(100vw - 24px); right: -8px; max-width: 340px; }

  .login-page { min-height: 100vh; }
  .login-right { padding: 36px 24px; }

  .topbar { padding: 0 16px; gap: 10px; }
  .topbar-title { font-size: 14.5px; }
  .role-pill { display: none; }

  .data-table thead { display: none; }
  .data-table tbody tr {
    display: block;
    padding: 12px 0;
    border-bottom: 2px solid var(--border) !important;
  }
  .data-table tbody td {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 16px;
    border-bottom: none;
  }
  .data-table tbody td::before {
    content: attr(data-label);
    font-size: 11px;
    font-weight: 800;
    color: var(--text-4);
    text-transform: uppercase;
    letter-spacing: .06em;
    flex-shrink: 0;
    margin-right: 10px;
  }
  .td-clamp { max-width: 160px; }

  .quick-actions { gap: 8px; }
  .quick-action-btn { padding: 12px 14px; min-width: 80px; font-size: 11.5px; }
}

@media (max-width: 480px) {
  .stats-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
  .stat-card { padding: 12px; }
  .stat-val { font-size: 22px; }
  .stat-icon-box { width: 36px; height: 36px; }
  .stat-icon-box svg { width: 17px; height: 17px; }
  .grid-3 { grid-template-columns: 1fr; }
  .login-right { padding: 28px 20px; }

  .content { padding: 10px; }

  /* Tabel aksi: tombol lebih kecil */
  .btn-sm { padding: 5px 10px; font-size: 11px; }

  /* Modal full-bottom-sheet di layar sangat kecil */
  .modal-overlay { align-items: flex-end; }
  .modal {
    width: 100%;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    max-height: 88vh;
    padding: 16px;
    animation: slide-up-modal .28s cubic-bezier(.34,1.2,.64,1);
  }
  @keyframes slide-up-modal {
    from { transform: translateY(40px); opacity: 0; }
    to   { transform: translateY(0);    opacity: 1; }
  }

  /* Section header tombol full width */
  .section-header { gap: 8px; }
  .section-header .btn { font-size: 12.5px; }

  /* Search form stack */
  .mb-20 form > div { flex-direction: column; }
  .mb-20 form .btn { width: 100%; justify-content: center; }

  /* Tabel kolom user: kurangi padding avatar */
  .data-table tbody td { padding: 5px 10px; }
}

/* ── Touch Optimizations ── */
@media (hover: none) {
  .nav-item:hover { transform: none; }
  .stat-card:hover { transform: none; }
  .btn-primary:hover { transform: none; }
  .reminder-card:hover { transform: none; }
}

/* ── Safe Area (iPhone notch etc) ── */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .sidebar-footer {
    padding-bottom: calc(12px + env(safe-area-inset-bottom));
  }
  .topbar {
    padding-left: max(14px, env(safe-area-inset-left));
    padding-right: max(14px, env(safe-area-inset-right));
  }
  .content {
    padding-left: max(14px, env(safe-area-inset-left));
    padding-right: max(14px, env(safe-area-inset-right));
  }
}

/* ── Utility ── */
.sr-only { position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0; }
.flex { display: flex; } .flex-col { flex-direction: column; }
.items-center { align-items: center; } .justify-between { justify-content: space-between; }
.gap-8 { gap: 8px; } .gap-12 { gap: 12px; } .gap-16 { gap: 16px; }
.text-center { text-align: center; }
.font-mono { font-family: 'JetBrains Mono', monospace; }
.truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.w-full { width: 100%; }
.mt-4{margin-top:4px} .mt-8{margin-top:8px} .mt-12{margin-top:12px} .mt-16{margin-top:16px}

/* ── Animated counter ── */
@keyframes count-up {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: none; }
}
.stat-val.animate { animation: count-up .5s ease forwards; }







/* ── Viewport height fix untuk iOS Safari ── */
/* JS di base.html harus set: document.documentElement.style.setProperty('--vh', window.innerHeight * 0.01 + 'px') */

/* ── Prevent zoom on input focus (iOS) ── */
@media (max-width: 768px) {
  input[type=text],
  input[type=password],
  input[type=email],
  input[type=number],
  input[type=search],
  select,
  textarea {
    font-size: 16px !important;
  }
}
