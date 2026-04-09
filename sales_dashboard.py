"""
Universal Sales Intelligence Hub — v14.0 (FIXED)
Fixed:
  1. SBDM නැති excel: DMs සියල්ලම පෙනේ
  2. SBDM ඇති excel: SBDM → DM → RP hierarchy සම්පූර්ණයෙන් පෙනේ
  3. render_full_hierarchy: data_ms zero-filter bug fix
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Sales Intelligence Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Plus Jakarta Sans',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0 2rem 2rem 2rem !important;}

[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d1b2a 0%,#112240 100%) !important;border-right:1px solid #1e3a5f;}
[data-testid="stSidebar"] *{color:#a8b2c8 !important;}
[data-testid="stSidebar"] .stSelectbox>div>div{background:#162032 !important;border:1px solid #1e3a5f !important;border-radius:9px !important;}
[data-testid="stSidebar"] hr{border-color:#1e3a5f !important;margin:1rem 0 !important;}

.page-header{background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 55%,#1d4ed8 100%);border-radius:0 0 24px 24px;padding:2rem 2.5rem;margin:0 -2rem 2rem;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(37,99,235,.3);}
.page-header h1{font-size:1.6rem;font-weight:800;color:#f8fafc;margin:0;letter-spacing:-.03em;}
.page-header p{font-size:.83rem;color:#93c5fd;margin:5px 0 0;}
.hdr-chips{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;}
.hdr-chip{font-size:.72rem;font-weight:700;padding:5px 14px;border-radius:999px;letter-spacing:.04em;}
.hdr-chip.live{background:rgba(37,99,235,.35);border:1px solid rgba(96,165,250,.4);color:#93c5fd;}
.hdr-chip.month{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#e2e8f0;}

[data-testid="stTabs"] [data-baseweb="tab-list"]{background:#f8fafc;border-radius:12px;padding:4px;gap:2px;border:1px solid #e2e8f0;margin-bottom:1.5rem;}
[data-testid="stTabs"] [data-baseweb="tab"]{border-radius:9px;font-weight:600;font-size:.83rem;color:#64748b;padding:8px 20px;}
[data-testid="stTabs"] [aria-selected="true"]{background:#fff !important;color:#1e293b !important;box-shadow:0 1px 4px rgba(0,0,0,.08);}

.kpi-card{background:#fff;border-radius:16px;padding:1.2rem 1.3rem 1rem;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,.06);position:relative;overflow:hidden;height:100%;}
.kpi-card::after{content:'';position:absolute;top:0;left:0;right:0;height:4px;border-radius:16px 16px 0 0;}
.kpi-card.c-blue::after{background:linear-gradient(90deg,#3b82f6,#60a5fa);}
.kpi-card.c-green::after{background:linear-gradient(90deg,#22c55e,#4ade80);}
.kpi-card.c-amber::after{background:linear-gradient(90deg,#f59e0b,#fbbf24);}
.kpi-card.c-purple::after{background:linear-gradient(90deg,#8b5cf6,#a78bfa);}
.kpi-card.c-red::after{background:linear-gradient(90deg,#ef4444,#f87171);}
.kpi-card.c-teal::after{background:linear-gradient(90deg,#14b8a6,#2dd4bf);}
.kpi-card.c-indigo::after{background:linear-gradient(90deg,#6366f1,#818cf8);}
.kpi-card.c-orange::after{background:linear-gradient(90deg,#f97316,#fb923c);}
.kpi-icon-wrap{width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;margin-bottom:12px;}
.c-blue .kpi-icon-wrap{background:#dbeafe;}.c-green .kpi-icon-wrap{background:#dcfce7;}.c-amber .kpi-icon-wrap{background:#fef3c7;}
.c-purple .kpi-icon-wrap{background:#ede9fe;}.c-red .kpi-icon-wrap{background:#fee2e2;}.c-teal .kpi-icon-wrap{background:#ccfbf1;}
.c-indigo .kpi-icon-wrap{background:#e0e7ff;}.c-orange .kpi-icon-wrap{background:#ffedd5;}
.kpi-label{font-size:.7rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:5px;}
.kpi-value{font-size:1.75rem;font-weight:800;color:#0f172a;line-height:1;letter-spacing:-.03em;}
.kpi-sub{font-size:.72rem;color:#94a3b8;margin-top:4px;}
.kpi-badge{display:inline-flex;align-items:center;gap:3px;font-size:.72rem;font-weight:700;padding:3px 9px;border-radius:999px;margin-top:8px;}
.kpi-badge.up{background:#dcfce7;color:#15803d;}.kpi-badge.down{background:#fee2e2;color:#b91c1c;}.kpi-badge.neu{background:#f1f5f9;color:#64748b;}

.card{background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:1.3rem 1.4rem .8rem;box-shadow:0 2px 8px rgba(0,0,0,.05);margin-bottom:1rem;}
.card-title{font-size:.9rem;font-weight:700;color:#1e293b;margin-bottom:.8rem;}

.sec-div{display:flex;align-items:center;gap:12px;margin:2rem 0 1.2rem;}
.sec-div-line{flex:1;height:1px;background:#e2e8f0;}
.sec-div-text{font-size:.72rem;font-weight:800;color:#94a3b8;text-transform:uppercase;letter-spacing:.1em;white-space:nowrap;}

/* SBDM Block */
.sbdm-block{border:2px solid #c7d2fe;border-radius:20px;margin-bottom:2rem;overflow:hidden;box-shadow:0 4px 20px rgba(99,102,241,.15);}
.sbdm-header{background:linear-gradient(135deg,#312e81 0%,#4338ca 60%,#6366f1 100%);padding:1.3rem 1.8rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;}
.sbdm-tag{font-size:.62rem;font-weight:700;color:#c7d2fe;text-transform:uppercase;letter-spacing:.12em;margin-bottom:4px;}
.sbdm-name{font-size:1.15rem;font-weight:800;color:#fff;}
.sbdm-formula{font-size:.68rem;color:#a5b4fc;margin-top:3px;font-family:monospace;}
.sbdm-kpis{display:flex;gap:0;border:1px solid rgba(255,255,255,.15);border-radius:12px;overflow:hidden;}
.sbdm-kpi-box{padding:.7rem 1.2rem;border-right:1px solid rgba(255,255,255,.15);}
.sbdm-kpi-box:last-child{border-right:none;}
.sbdm-kpi-label{font-size:.58rem;font-weight:700;color:rgba(255,255,255,.5);text-transform:uppercase;margin-bottom:3px;}
.sbdm-kpi-value{font-size:1rem;font-weight:800;color:#fff;}
.sbdm-body{background:#f5f3ff;padding:1rem 1.2rem;}
.sbdm-dm-list{display:flex;flex-direction:column;gap:12px;}

/* DM Block */
.dm-block{border:1px solid #e2e8f0;border-radius:16px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.dm-header{padding:1rem 1.4rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;}
.dm-name{font-size:1rem;font-weight:800;color:#fff;}
.dm-formula{font-size:.68rem;color:#93c5fd;margin-top:2px;font-family:monospace;}
.dm-kpis{display:flex;gap:0;border:1px solid rgba(255,255,255,.15);border-radius:10px;overflow:hidden;}
.dm-kpi-box{padding:.6rem 1rem;border-right:1px solid rgba(255,255,255,.15);}
.dm-kpi-box:last-child{border-right:none;}
.dm-kpi-label{font-size:.58rem;font-weight:700;color:rgba(255,255,255,.5);text-transform:uppercase;margin-bottom:2px;}
.dm-kpi-value{font-size:.95rem;font-weight:800;color:#fff;}

/* RP rows */
.rp-header-row{display:flex;align-items:center;gap:10px;padding:7px 1.4rem;background:#f8fafc;border-bottom:2px solid #e2e8f0;font-size:.65rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;}
.rp-data-row{display:flex;align-items:center;gap:10px;padding:10px 1.4rem;border-bottom:1px solid #f1f5f9;}
.rp-data-row:last-child{border-bottom:none;}
.rp-data-row:hover{background:#f8fafc;}
.rp-bullet{width:7px;height:7px;border-radius:50%;flex-shrink:0;}
.rp-name{font-size:.85rem;font-weight:600;color:#1e293b;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.rp-bar-wrap{flex:1.5;background:#f1f5f9;border-radius:999px;height:7px;overflow:hidden;min-width:60px;}
.rp-bar-fill{height:100%;border-radius:999px;}
.rp-tar{font-size:.78rem;color:#94a3b8;width:115px;text-align:right;flex-shrink:0;}
.rp-ach{font-size:.78rem;font-weight:700;width:115px;text-align:right;flex-shrink:0;}
.rp-var{font-size:.78rem;font-weight:700;width:105px;text-align:right;flex-shrink:0;}
.rp-pct{font-size:.72rem;font-weight:800;padding:3px 9px;border-radius:999px;width:58px;text-align:center;flex-shrink:0;}
.pct-green{background:#dcfce7;color:#15803d;}
.pct-amber{background:#fef3c7;color:#92400e;}
.pct-red{background:#fee2e2;color:#b91c1c;}

.dm-totals{display:flex;align-items:center;gap:10px;padding:9px 1.4rem;background:#f0f9ff;border-top:2px solid #bae6fd;font-size:.78rem;font-weight:700;color:#0369a1;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
PALETTE = ["#3b82f6","#22c55e","#f59e0b","#ef4444","#8b5cf6",
           "#ec4899","#14b8a6","#f97316","#06b6d4","#a78bfa"]
SKIP_SHEETS = {'SOURCE','HO','SPC','SOURCE (2)','SIX MONTHS',
               'JAN-2','FEB-2','MAR-2','six months','DEC-2'}
MONTH_ORDER = ['APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC','JAN','FEB','MAR']
PLOTLY_BASE = dict(
    font=dict(family="Plus Jakarta Sans, sans-serif", size=12),
    plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
    hoverlabel=dict(bgcolor="#0f172a", font_size=12, font_color="#f8fafc"),
)

# ══════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════
def fmt_n(n):
    try: return f"{int(round(float(n))):,}"
    except: return str(n)

def fmt_lkr(n):
    try:
        v = float(n)
        if abs(v) >= 1_000_000: return f"LKR {v/1_000_000:.2f}M"
        if abs(v) >= 1_000: return f"LKR {v/1_000:.1f}K"
        return f"LKR {v:,.0f}"
    except: return str(n)

def safe_round(v, d=0):
    try:
        f = float(v)
        if np.isnan(f) or np.isinf(f): return 0
        return round(f, d)
    except: return 0

def pct_badge(p): return "pct-green" if p >= 100 else "pct-amber" if p >= 80 else "pct-red"
def pct_color(p): return "#16a34a" if p >= 100 else "#d97706" if p >= 80 else "#dc2626"
def pct_cls(p):   return "up" if p >= 100 else "neu" if p >= 80 else "down"

def is_sbdm(name): return "(SBDM)" in str(name).upper()
def is_dm(name):   return "(DM)" in str(name).upper()

def section(title):
    st.markdown(f"""<div class="sec-div">
        <div class="sec-div-line"></div>
        <div class="sec-div-text">{title}</div>
        <div class="sec-div-line"></div>
    </div>""", unsafe_allow_html=True)

def kpi_card(col, label, value, icon, color, badge_text=None, badge_cls="neu", sub=None):
    badge = f'<div class="kpi-badge {badge_cls}">{badge_text}</div>' if badge_text else ""
    sub_  = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    col.markdown(f"""<div class="kpi-card {color}">
        <div class="kpi-icon-wrap">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {sub_}{badge}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# HIERARCHY BUILDER
# ══════════════════════════════════════════════════════
def build_hierarchy(entity_order):
    """SBDM → DM → RP. '__NO_SBDM__' sentinel if no SBDM exists."""
    hierarchy = {}
    cur_sbdm = '__NO_SBDM__'
    cur_dm   = None

    for name in entity_order:
        if name == 'TOTAL':
            continue
        if is_sbdm(name):
            cur_sbdm = name
            cur_dm   = None
            hierarchy.setdefault(cur_sbdm, {})
        elif is_dm(name):
            cur_dm = name
            hierarchy.setdefault(cur_sbdm, {})
            hierarchy[cur_sbdm][cur_dm] = []
        else:
            hierarchy.setdefault(cur_sbdm, {})
            if cur_dm is None:
                cur_dm = '__STANDALONE__'
            hierarchy[cur_sbdm].setdefault(cur_dm, [])
            hierarchy[cur_sbdm][cur_dm].append(name)

    return hierarchy

def has_sbdm(hierarchy):
    return any(k != '__NO_SBDM__' for k in hierarchy)

# ══════════════════════════════════════════════════════
# EXCEL PARSING
# ══════════════════════════════════════════════════════
def find_total_row(raw):
    for i in range(2, min(80, raw.shape[0])):
        if str(raw.iloc[i, 1]).strip() != 'TOTAL':
            continue
        for col in range(4, min(raw.shape[1], 10)):
            val = raw.iloc[i, col]
            if pd.notna(val):
                try:
                    if float(val) > 100000:
                        return i
                except: pass
    return None

def find_product_rows(raw, total_row):
    skip = {'', 'nan', 'TOTAL', '0', 'PRODUCT', '#'}
    rows = []
    for r in range(2, total_row):
        pname = raw.iloc[r, 1]
        if not isinstance(pname, str): continue
        if pname.strip() in skip: continue
        tar = pd.to_numeric(raw.iloc[r, 4], errors='coerce')
        if pd.notna(tar) and float(tar) > 0:
            rows.append(r)
    return rows

def parse_excel(file_obj):
    xls = pd.ExcelFile(file_obj)
    sheets = [s for s in xls.sheet_names if s.upper() not in {x.upper() for x in SKIP_SHEETS}]

    all_lkr = {}; all_units = {}; all_hierarchy = {}
    all_eo  = {}; all_prod  = {}; all_prod_entity = {}

    for sheet in sheets:
        try:
            raw = pd.read_excel(file_obj, sheet_name=sheet, header=None)
        except: continue
        if raw.shape[0] < 6 or raw.shape[1] < 6: continue

        lkr_row = find_total_row(raw)
        if lkr_row is None: continue

        prod_rows = find_product_rows(raw, lkr_row)
        if not prod_rows: continue

        # Parse entity columns
        entity_cols = {}
        name_count  = {}
        for j in range(4, raw.shape[1] - 1, 2):
            name_cell = raw.iloc[0, j] if j < raw.shape[1] else None
            if pd.isna(name_cell) or str(name_cell).strip() in ('', 'nan'): continue
            hdr = str(raw.iloc[1, j]).strip() if pd.notna(raw.iloc[1, j]) else ''
            if hdr not in ('TAR', ''): continue
            base = str(name_cell).strip()
            if base in name_count:
                name_count[base] += 1
                uname = f"{base}-{name_count[base]}"
            else:
                name_count[base] = 1
                uname = base
            entity_cols[uname] = j

        if not entity_cols: continue

        ordered = list(entity_cols.keys())
        all_eo[sheet]        = ordered
        all_hierarchy[sheet] = build_hierarchy(ordered)

        units_ms = {}; pe_sheet = {}

        for ename, tc in entity_cols.items():
            ac = tc + 1
            tar_v = raw.iloc[prod_rows, tc].apply(pd.to_numeric, errors='coerce').fillna(0)
            ach_v = (raw.iloc[prod_rows, ac].apply(pd.to_numeric, errors='coerce').fillna(0)
                     if ac < raw.shape[1] else pd.Series([0]*len(prod_rows)))
            tar_t = float(tar_v.sum()); ach_t = float(ach_v.sum())
            units_ms[ename] = dict(TAR=tar_t, ACH=ach_t, VAR=ach_t-tar_t,
                                   PCT=(ach_t/tar_t*100) if tar_t else 0.0)
            pe_sheet[ename] = {}
            for idx, r in enumerate(prod_rows):
                pname = str(raw.iloc[r, 1]).strip()
                t = float(tar_v.iloc[idx]) if pd.notna(tar_v.iloc[idx]) else 0.0
                a = float(ach_v.iloc[idx]) if pd.notna(ach_v.iloc[idx]) else 0.0
                pe_sheet[ename][pname] = dict(TAR=max(t,0), ACH=max(a,0))

        all_units[sheet]       = units_ms
        all_prod_entity[sheet] = pe_sheet

        lkr_ms = {}
        for ename, tc in entity_cols.items():
            ac = tc + 1
            t = float(pd.to_numeric(raw.iloc[lkr_row, tc], errors='coerce') or 0)
            a = float(pd.to_numeric(raw.iloc[lkr_row, ac], errors='coerce') or 0) if ac < raw.shape[1] else 0.0
            lkr_ms[ename] = dict(TAR_LKR=t, ACH_LKR=a, VAR_LKR=a-t,
                                  PCT_LKR=(a/t*100) if t else 0.0)
        all_lkr[sheet] = lkr_ms

        rows_list = []
        for r in prod_rows:
            pname = str(raw.iloc[r, 1]).strip()
            for ename, tc in entity_cols.items():
                ac = tc + 1
                t = float(pd.to_numeric(raw.iloc[r, tc], errors='coerce') or 0)
                a = float(pd.to_numeric(raw.iloc[r, ac], errors='coerce') or 0) if ac < raw.shape[1] else 0.0
                if t == 0 and a == 0: continue
                rows_list.append(dict(ENTITY=ename, PRODUCT=pname, TAR=t, ACH=a,
                                      VAR=a-t, PCT=(a/t*100) if t else 0.0))
        all_prod[sheet] = pd.DataFrame(rows_list) if rows_list else pd.DataFrame()

    return all_lkr, all_units, all_hierarchy, all_eo, all_prod, all_prod_entity

# ══════════════════════════════════════════════════════
# HIERARCHY RENDERER — FIXED
# ══════════════════════════════════════════════════════
def render_rp_rows(rp_list, data_ms, fmt_fn, key_prefix):
    """Render RP rows inside a DM block."""
    valid_rps = []
    for rp in rp_list:
        d = data_ms.get(rp, {})
        t = d.get('TAR', d.get('TAR_LKR', 0))
        a = d.get('ACH', d.get('ACH_LKR', 0))
        if t > 0 or a > 0:
            valid_rps.append(rp)

    if not valid_rps:
        st.markdown('<div style="padding:10px 1.4rem;color:#94a3b8;font-size:.8rem;font-style:italic">No RP data.</div>', unsafe_allow_html=True)
        return

    header = """<div class="rp-header-row">
        <div style="width:7px"></div>
        <div style="flex:1">Sales Rep / RP</div>
        <div style="flex:1.5">Progress</div>
        <div class="rp-tar">Target</div>
        <div class="rp-ach">Achievement</div>
        <div class="rp-var">Variance</div>
        <div style="width:58px;text-align:center">Ach %</div>
    </div>"""

    rows_html = ""
    rp_tar_sum = rp_ach_sum = 0.0
    for rp in valid_rps:
        d   = data_ms.get(rp, {})
        t   = d.get('TAR', d.get('TAR_LKR', 0))
        a   = d.get('ACH', d.get('ACH_LKR', 0))
        v   = a - t
        p   = (a/t*100) if t else 0.0
        bc  = pct_color(p)
        pb  = pct_badge(p)
        vc  = "#059669" if v >= 0 else "#dc2626"
        bg  = "#f0fdf4" if p >= 100 else "#fffbeb" if p >= 80 else "#ffffff"
        rp_tar_sum += t; rp_ach_sum += a
        rows_html += f"""<div class="rp-data-row" style="background:{bg}">
            <div class="rp-bullet" style="background:{bc}"></div>
            <div class="rp-name">{rp}</div>
            <div class="rp-bar-wrap"><div class="rp-bar-fill" style="width:{min(p,100):.1f}%;background:{bc};opacity:.8"></div></div>
            <div class="rp-tar">{fmt_fn(t)}</div>
            <div class="rp-ach" style="color:{bc}">{fmt_fn(a)}</div>
            <div class="rp-var" style="color:{vc}">{"+" if v>=0 else ""}{fmt_fn(v)}</div>
            <div class="rp-pct {pb}">{p:.1f}%</div>
        </div>"""

    roll_pct = (rp_ach_sum/rp_tar_sum*100) if rp_tar_sum else 0
    totals   = f"""<div class="dm-totals">
        <div style="width:7px"></div>
        <div style="flex:1">∑ RP Rollup</div>
        <div style="flex:1.5"></div>
        <div class="rp-tar">{fmt_fn(rp_tar_sum)}</div>
        <div class="rp-ach">{fmt_fn(rp_ach_sum)}</div>
        <div class="rp-var" style="color:{'#0369a1' if rp_ach_sum>=rp_tar_sum else '#dc2626'}">
            {"+" if rp_ach_sum-rp_tar_sum>=0 else ""}{fmt_fn(rp_ach_sum-rp_tar_sum)}</div>
        <div style="width:58px;text-align:center;font-weight:800;color:#0369a1">{roll_pct:.1f}%</div>
    </div>"""

    st.markdown(header + '<div style="background:#fff">' + rows_html + '</div>' + totals,
                unsafe_allow_html=True)


def render_dm_block(dm_name, rp_list, data_ms, fmt_fn, label, color):
    """Render one DM block with its RPs."""
    d   = data_ms.get(dm_name, {})
    t   = d.get('TAR', d.get('TAR_LKR', 0))
    a   = d.get('ACH', d.get('ACH_LKR', 0))
    v   = d.get('VAR', d.get('VAR_LKR', 0))
    p   = d.get('PCT', d.get('PCT_LKR', 0))
    pb  = pct_badge(p)
    vc  = "#4ade80" if v >= 0 else "#f87171"
    formula = " + ".join(rp_list) if rp_list else "No RP sub-teams"

    st.markdown(f"""<div class="dm-block">
        <div class="dm-header" style="background:linear-gradient(135deg,#1e3a5f,#1d4ed8);border-left:5px solid {color}">
            <div>
                <div class="dm-name">👤 {dm_name}</div>
                <div class="dm-formula">= {formula}</div>
            </div>
            <div class="dm-kpis">
                <div class="dm-kpi-box">
                    <div class="dm-kpi-label">Target ({label})</div>
                    <div class="dm-kpi-value">{fmt_fn(t)}</div>
                </div>
                <div class="dm-kpi-box">
                    <div class="dm-kpi-label">Achievement ({label})</div>
                    <div class="dm-kpi-value">{fmt_fn(a)}</div>
                    <span class="{pb}" style="font-size:.72rem;font-weight:700;padding:2px 9px;border-radius:999px;display:inline-block;margin-top:3px;
                        {'background:rgba(34,197,94,.25);color:#4ade80' if p>=100 else 'background:rgba(245,158,11,.25);color:#fbbf24' if p>=80 else 'background:rgba(239,68,68,.25);color:#f87171'}">{p:.1f}%</span>
                </div>
                <div class="dm-kpi-box">
                    <div class="dm-kpi-label">Variance</div>
                    <div class="dm-kpi-value" style="color:{vc}">{"+" if v>=0 else ""}{fmt_fn(v)}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    render_rp_rows(rp_list, data_ms, fmt_fn, f"{dm_name}")
    st.markdown("</div>", unsafe_allow_html=True)


def render_hierarchy(hierarchy, data_ms, fmt_fn, label,
                     sbdm_filter="ALL", dm_filter="ALL"):
    """
    ✅ FIXED render:
    - SBDM නැති excel: DMs සියල්ලම directly render කරයි
    - SBDM ඇති excel: SBDM wrapper ඇතුළේ DMs render කරයි
    - data_ms zero-check නොකරයි (DM ලා filter out වෙන bug fix)
    """
    show_sbdm = has_sbdm(hierarchy)

    for sbdm_key, dm_dict in hierarchy.items():
        is_real_sbdm = (sbdm_key != '__NO_SBDM__')

        # SBDM filter
        if sbdm_filter != "ALL" and is_real_sbdm and sbdm_key != sbdm_filter:
            continue

        # DM filter
        if dm_filter != "ALL":
            dm_dict = {k: v for k, v in dm_dict.items() if k == dm_filter}
            if not dm_dict:
                continue

        # ── SBDM ඇති විට: SBDM wrapper render කරමු ──
        if show_sbdm and is_real_sbdm:
            d    = data_ms.get(sbdm_key, {})
            s_t  = d.get('TAR', d.get('TAR_LKR', 0))
            s_a  = d.get('ACH', d.get('ACH_LKR', 0))
            s_v  = d.get('VAR', d.get('VAR_LKR', 0))
            s_p  = d.get('PCT', d.get('PCT_LKR', 0))
            vc   = "#4ade80" if s_v >= 0 else "#f87171"
            dm_formula = " + ".join(k for k in dm_dict if k != '__STANDALONE__')

            st.markdown(f"""<div class="sbdm-block">
                <div class="sbdm-header">
                    <div>
                        <div class="sbdm-tag">⭐ Senior BDM</div>
                        <div class="sbdm-name">{sbdm_key}</div>
                        <div class="sbdm-formula">= {dm_formula}</div>
                    </div>
                    <div class="sbdm-kpis">
                        <div class="sbdm-kpi-box">
                            <div class="sbdm-kpi-label">Target ({label})</div>
                            <div class="sbdm-kpi-value">{fmt_fn(s_t)}</div>
                        </div>
                        <div class="sbdm-kpi-box">
                            <div class="sbdm-kpi-label">Achievement ({label})</div>
                            <div class="sbdm-kpi-value">{fmt_fn(s_a)}</div>
                            <span style="font-size:.72rem;font-weight:700;padding:2px 9px;border-radius:999px;display:inline-block;margin-top:3px;
                                {'background:rgba(34,197,94,.25);color:#4ade80' if s_p>=100 else 'background:rgba(245,158,11,.25);color:#fbbf24' if s_p>=80 else 'background:rgba(239,68,68,.25);color:#f87171'}">{s_p:.1f}%</span>
                        </div>
                        <div class="sbdm-kpi-box">
                            <div class="sbdm-kpi-label">Variance</div>
                            <div class="sbdm-kpi-value" style="color:{vc}">{"+" if s_v>=0 else ""}{fmt_fn(s_v)}</div>
                        </div>
                    </div>
                </div>
                <div class="sbdm-body"><div class="sbdm-dm-list">""", unsafe_allow_html=True)

            for i, (dm_k, rp_list) in enumerate(dm_dict.items()):
                if dm_k == '__STANDALONE__': continue
                render_dm_block(dm_k, rp_list, data_ms, fmt_fn, label, PALETTE[i % len(PALETTE)])

            st.markdown("</div></div></div>", unsafe_allow_html=True)

        # ── SBDM නැති විට: DMs directly render කරමු ──
        else:
            for i, (dm_k, rp_list) in enumerate(dm_dict.items()):
                if dm_k == '__STANDALONE__': continue
                render_dm_block(dm_k, rp_list, data_ms, fmt_fn, label, PALETTE[i % len(PALETTE)])
                st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div style="padding-bottom:10px">
        <h2>📊 Sales Intelligence Hub</h2>
        <p style="font-size:.78rem">Universal Dashboard · v14.0</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<span style="font-weight:700;font-size:.85rem">📂 Excel Upload</span>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload Excel files", type=["xlsx","xls"], accept_multiple_files=True
    )
    st.markdown("---")

    if uploaded_files:
        names = [f.name for f in uploaded_files]
        sel_name = st.selectbox("📁 File", names) if len(names) > 1 else names[0]
        ufile    = next(f for f in uploaded_files if f.name == sel_name)
        dash_title = sel_name.rsplit('.',1)[0].replace('_',' ').replace('-',' ').upper()

        with st.spinner("Parsing Excel…"):
            all_lkr, all_units, all_hierarchy, all_eo, all_prod, all_prod_entity = parse_excel(ufile)

        month_list = [m for m in MONTH_ORDER if m in all_lkr]
        if not month_list:
            st.error("Valid data sheets not found.")
            st.stop()

        sel_month = st.selectbox("📅 Month", month_list)
        lkr_ms   = all_lkr[sel_month]
        units_ms = all_units[sel_month]
        hier     = all_hierarchy[sel_month]
        eo       = all_eo[sel_month]

        sbdm_keys = [e for e in eo if is_sbdm(e)]
        dm_keys   = [e for e in eo if is_dm(e)]
        show_sbdm = len(sbdm_keys) > 0

        tot_lkr  = lkr_ms.get('TOTAL', {})
        tot_t    = tot_lkr.get('TAR_LKR', 0)
        tot_a    = tot_lkr.get('ACH_LKR', 0)
        tot_v    = tot_lkr.get('VAR_LKR', 0)
        tot_p    = tot_lkr.get('PCT_LKR', 0)
        tot_u    = units_ms.get('TOTAL', {})

        st.markdown("---")
        st.markdown('<span style="font-weight:700;font-size:.85rem">📌 Quick Stats</span>', unsafe_allow_html=True)
        p_col = "#4ade80" if tot_p >= 100 else "#fbbf24" if tot_p >= 80 else "#f87171"
        st.markdown(f"""
        <div style="font-size:.82rem;line-height:1.9">
        Target: {fmt_lkr(tot_t)}<br>
        Achievement: {fmt_lkr(tot_a)}<br>
        <span style="color:{p_col};font-weight:700">LKR Ach %: {tot_p:.1f}%</span><br>
        Units Target: {fmt_n(tot_u.get('TAR',0))}<br>
        Units Achievement: {fmt_n(tot_u.get('ACH',0))}<br>
        {'SBDMs: ' + str(len(sbdm_keys)) + '<br>' if show_sbdm else ''}
        DMs: {len(dm_keys)}<br>
        Months loaded: {len(month_list)}
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        if show_sbdm:
            sbdm_filter = st.selectbox("🔍 Filter SBDM", ["ALL"] + sbdm_keys)
        else:
            sbdm_filter = "ALL"
        dm_filter = st.selectbox("🔍 Filter DM", ["ALL"] + dm_keys)
    else:
        st.info("Excel file upload කරන්න.")
        dash_title = "Sales Intelligence Hub"

    st.markdown("---")
    st.markdown("<small style='color:#475569;font-size:.68rem'>v14.0 · Fixed Hierarchy</small>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# LANDING
# ══════════════════════════════════════════════════════
if not uploaded_files:
    st.markdown("""<div style="display:flex;flex-direction:column;align-items:center;padding:5rem 2rem;text-align:center">
        <div style="font-size:3.5rem;margin-bottom:1.2rem">📊</div>
        <h2 style="font-size:1.5rem;font-weight:800;color:#1e293b;margin-bottom:.6rem">Universal Sales Intelligence Hub</h2>
        <p style="font-size:.88rem;color:#64748b;max-width:480px;line-height:1.7">
        Excel file upload කරන්න. SBDM ඇත්නම් <strong>SBDM → DM → RP</strong> hierarchy පෙනේ.<br>
        SBDM නැත්නම් <strong>DM → RP</strong> directly පෙනේ.
        </p>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════
hier_label = "SBDM → DM → RP" if show_sbdm else "DM → RP"
v_sign = "▲" if tot_v >= 0 else "▼"
v_col  = "#4ade80" if tot_v >= 0 else "#f87171"

st.markdown(f"""<div class="page-header">
    <div>
        <h1>📊 {dash_title} — Sales Performance</h1>
        <p>{hier_label} hierarchy · {sel_month}</p>
    </div>
    <div class="hdr-chips">
        <span class="hdr-chip live">● LIVE</span>
        <span class="hdr-chip month">📅 {sel_month}</span>
        <span class="hdr-chip month" style="color:{v_col}">{v_sign} {fmt_lkr(abs(tot_v))} variance</span>
    </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📆 Overview",
    "📅 All Months",
    "👥 DM / SBDM Breakdown",
    "🏢 RP Detail",
    "📦 Products",
    "📊 Cumulative",
])

# ╔══════════════════════════════════════╗
# ║  TAB 1 — OVERVIEW                   ║
# ╚══════════════════════════════════════╝
with tab1:
    ov_month  = st.selectbox("Month", month_list, index=month_list.index(sel_month), key="ov_m")
    ov_lkr    = all_lkr[ov_month]
    ov_units  = all_units[ov_month]
    ov_eo     = all_eo[ov_month]

    ov_tot  = ov_lkr.get('TOTAL', {})
    ov_t    = ov_tot.get('TAR_LKR', 0)
    ov_a    = ov_tot.get('ACH_LKR', 0)
    ov_v    = ov_tot.get('VAR_LKR', 0)
    ov_p    = ov_tot.get('PCT_LKR', 0)
    ov_ut   = ov_units.get('TOTAL', {})

    section("LKR PERFORMANCE")
    c1,c2,c3,c4 = st.columns(4)
    kpi_card(c1, "Total Target (LKR)", fmt_lkr(ov_t), "🎯", "c-blue", sub=ov_month)
    kpi_card(c2, "Total Achievement (LKR)", fmt_lkr(ov_a), "💰", "c-green",
             badge_text=f"{'▲' if ov_v>=0 else '▼'} {fmt_lkr(abs(ov_v))}", badge_cls=pct_cls(ov_p))
    kpi_card(c3, "LKR Ach %", f"{ov_p:.1f}%", "📈",
             "c-green" if ov_p>=100 else "c-amber",
             badge_text="On Track" if ov_p>=100 else "Below Target", badge_cls=pct_cls(ov_p))
    kpi_card(c4, "LKR Variance", fmt_lkr(abs(ov_v)),
             "📊" if ov_v>=0 else "📉", "c-teal" if ov_v>=0 else "c-red",
             badge_text="▲ Surplus" if ov_v>=0 else "▼ Shortfall",
             badge_cls="up" if ov_v>=0 else "down")

    st.markdown("<br>", unsafe_allow_html=True)
    u1,u2,u3,u4 = st.columns(4)
    kpi_card(u1, "Unit Target", fmt_n(ov_ut.get('TAR',0)), "📦", "c-indigo", sub=ov_month)
    kpi_card(u2, "Unit Achievement", fmt_n(ov_ut.get('ACH',0)), "✅", "c-purple",
             badge_text=f"{ov_ut.get('PCT',0):.1f}%", badge_cls=pct_cls(ov_ut.get('PCT',0)))
    sbdm_cnt = len([e for e in ov_eo if is_sbdm(e)])
    dm_cnt   = len([e for e in ov_eo if is_dm(e)])
    if sbdm_cnt:
        kpi_card(u3, "SBDMs", str(sbdm_cnt), "⭐", "c-purple")
    else:
        kpi_card(u3, "Hierarchy", "DM → RP", "🏗️", "c-orange")
    kpi_card(u4, "DMs", str(dm_cnt), "👤", "c-blue")

    section("TARGET vs ACHIEVEMENT — ALL ENTITIES")
    top_ents = [e for e in ov_eo if e!='TOTAL' and ov_lkr.get(e,{}).get('TAR_LKR',0)>0]

    col_b, col_p = st.columns([3,2])
    with col_b:
        st.markdown('<div class="card"><div class="card-title">LKR TAR vs ACH — All Entities</div>', unsafe_allow_html=True)
        tars  = [ov_lkr[e]['TAR_LKR'] for e in top_ents]
        achs  = [ov_lkr[e]['ACH_LKR'] for e in top_ents]
        pcts  = [ov_lkr[e]['PCT_LKR'] for e in top_ents]
        short = [n[:14]+"…" if len(n)>14 else n for n in top_ents]
        fig_b = go.Figure()
        fig_b.add_trace(go.Bar(name="Target", x=top_ents, y=tars,
            marker=dict(color="#93c5fd",line=dict(width=0)), width=0.35, offset=-0.2))
        fig_b.add_trace(go.Bar(name="Achievement", x=top_ents, y=achs,
            marker=dict(color=[pct_color(p) for p in pcts], opacity=0.9, line=dict(width=0)),
            width=0.35, offset=0.05,
            text=[f"{p:.1f}%" for p in pcts], textposition="outside", textfont=dict(size=10)))
        fig_b.update_layout(**PLOTLY_BASE, barmode="overlay", height=360,
            margin=dict(t=20,b=100,l=80,r=20),
            xaxis=dict(tickangle=-40, tickfont=dict(size=10,color="#64748b"), showgrid=False,
                       tickmode="array", tickvals=list(range(len(top_ents))), ticktext=short),
            yaxis=dict(gridcolor="#f1f5f9", tickfont=dict(size=10,color="#94a3b8"), title="LKR"),
            legend=dict(orientation="h",y=1.05,xanchor="right",x=1,bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_p:
        grp_keys = [e for e in ov_eo if is_sbdm(e)] or [e for e in ov_eo if is_dm(e)]
        pie_lbl  = "SBDM Achievement Share" if any(is_sbdm(e) for e in ov_eo) else "DM Achievement Share"
        st.markdown(f'<div class="card"><div class="card-title">{pie_lbl} (LKR)</div>', unsafe_allow_html=True)
        items = {k: ov_lkr.get(k,{}).get('ACH_LKR',0) for k in grp_keys if ov_lkr.get(k,{}).get('ACH_LKR',0)>0}
        if items:
            labels, vals = zip(*items.items())
            fig_p = go.Figure(go.Pie(
                labels=labels, values=vals, hole=.55,
                marker=dict(colors=PALETTE[:len(labels)], line=dict(color="#fff",width=2)),
                textinfo="percent+label", textfont=dict(size=11)))
            fig_p.update_layout(**PLOTLY_BASE, height=320,
                margin=dict(t=10,b=10,l=10,r=10), showlegend=False)
            st.plotly_chart(fig_p, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    section("ENTITY SUMMARY TABLE")
    tbl = []
    for e in ov_eo:
        l = ov_lkr.get(e,{}); u = ov_units.get(e,{})
        et = "TOTAL" if e=="TOTAL" else "SBDM" if is_sbdm(e) else "DM" if is_dm(e) else "RP/Rep"
        tbl.append({"Entity":e,"Type":et,
                    "Target LKR":safe_round(l.get("TAR_LKR",0)),
                    "Achievement LKR":safe_round(l.get("ACH_LKR",0)),
                    "LKR Ach %":safe_round(l.get("PCT_LKR",0),1),
                    "LKR Variance":safe_round(l.get("VAR_LKR",0)),
                    "Target Units":safe_round(u.get("TAR",0)),
                    "Achievement Units":safe_round(u.get("ACH",0)),
                    "Unit Ach %":safe_round(u.get("PCT",0),1)})
    tbl_df = pd.DataFrame(tbl)
    num_cols = ["Target LKR","Achievement LKR","LKR Variance","Target Units","Achievement Units"]
    tbl_df = tbl_df[~(tbl_df[num_cols]==0).all(axis=1)]
    st.dataframe(tbl_df.style
        .format({"Target LKR":"{:,.0f}","Achievement LKR":"{:,.0f}","LKR Ach %":"{:.1f}%",
                 "LKR Variance":"{:+,.0f}","Target Units":"{:,.0f}",
                 "Achievement Units":"{:,.0f}","Unit Ach %":"{:.1f}%"})
        .map(lambda v: ("color:#059669;font-weight:700" if v>=0 else "color:#dc2626;font-weight:700")
             if isinstance(v,(int,float)) else "", subset=["LKR Variance"])
        .map(lambda v: ("color:#059669;font-weight:700" if v>=100 else
                        "color:#d97706;font-weight:700" if v>=80 else "color:#dc2626;font-weight:700")
             if isinstance(v,(int,float)) else "", subset=["LKR Ach %","Unit Ach %"]),
        use_container_width=True, hide_index=True, height=min(520, len(tbl_df)*42+60))
    dl,_ = st.columns([1,5])
    with dl:
        st.download_button("⬇️ Export CSV", data=tbl_df.to_csv(index=False).encode(),
            file_name=f"{dash_title}_{ov_month}.csv", mime="text/csv", use_container_width=True)


# ╔══════════════════════════════════════╗
# ║  TAB 2 — ALL MONTHS                 ║
# ╚══════════════════════════════════════╝
with tab2:
    summary = []
    for m in month_list:
        tl = all_lkr[m].get('TOTAL',{}); tu = all_units[m].get('TOTAL',{})
        eo_m = all_eo[m]
        summary.append({"Month":m,
            "Target (LKR)":tl.get("TAR_LKR",0), "Achievement (LKR)":tl.get("ACH_LKR",0),
            "LKR Ach %":tl.get("PCT_LKR",0), "LKR Variance":tl.get("VAR_LKR",0),
            "Target (Units)":tu.get("TAR",0), "Achievement (Units)":tu.get("ACH",0),
            "Unit Ach %":tu.get("PCT",0),
            "# DMs":len([e for e in eo_m if is_dm(e)]),
            "# SBDMs":len([e for e in eo_m if is_sbdm(e)])})
    sum_df = pd.DataFrame(summary)

    section("GRAND TOTAL — ALL MONTHS")
    g_tar = sum_df["Target (LKR)"].sum()
    g_ach = sum_df["Achievement (LKR)"].sum()
    g_pct = (g_ach/g_tar*100) if g_tar else 0
    g_var = g_ach - g_tar
    g1,g2,g3,g4 = st.columns(4)
    kpi_card(g1,"Grand Target (LKR)",fmt_lkr(g_tar),"🎯","c-blue",sub=f"{len(sum_df)} months")
    kpi_card(g2,"Grand Achievement (LKR)",fmt_lkr(g_ach),"💰","c-green",
             badge_text=f"{'▲' if g_var>=0 else '▼'} {fmt_lkr(abs(g_var))}", badge_cls="up" if g_var>=0 else "down")
    kpi_card(g3,"Overall Ach %",f"{g_pct:.1f}%","📈","c-green" if g_pct>=100 else "c-amber", badge_cls=pct_cls(g_pct))
    kpi_card(g4,"Total Variance",fmt_lkr(abs(g_var)),"📊" if g_var>=0 else "📉","c-teal" if g_var>=0 else "c-red",
             badge_text="▲ Surplus" if g_var>=0 else "▼ Shortfall", badge_cls="up" if g_var>=0 else "down")

    section("MONTHLY TREND")
    cl1,cl2 = st.columns([3,2])
    with cl1:
        st.markdown('<div class="card"><div class="card-title">Monthly LKR TAR vs ACH</div>', unsafe_allow_html=True)
        fig_tr = go.Figure()
        fig_tr.add_trace(go.Bar(name="Target", x=sum_df["Month"], y=sum_df["Target (LKR)"],
            marker=dict(color="#93c5fd",opacity=.9,line=dict(width=0))))
        fig_tr.add_trace(go.Bar(name="Achievement", x=sum_df["Month"], y=sum_df["Achievement (LKR)"],
            marker=dict(color=[pct_color(p) for p in sum_df["LKR Ach %"]],opacity=.9,line=dict(width=0)),
            text=[f"{p:.1f}%" for p in sum_df["LKR Ach %"]], textposition="outside", textfont=dict(size=11)))
        fig_tr.update_layout(**PLOTLY_BASE, barmode="group", height=340,
            margin=dict(t=20,b=60,l=80,r=20),
            xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
            yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),title="LKR"),
            legend=dict(orientation="h",y=1.05,xanchor="right",x=1,bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_tr, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)
    with cl2:
        st.markdown('<div class="card"><div class="card-title">Monthly Achievement Share</div>', unsafe_allow_html=True)
        items2 = {r["Month"]:r["Achievement (LKR)"] for r in summary if r["Achievement (LKR)"]>0}
        if items2:
            labels2, vals2 = zip(*items2.items())
            fig_p2 = go.Figure(go.Pie(labels=labels2, values=vals2, hole=.5,
                marker=dict(colors=PALETTE[:len(labels2)], line=dict(color="#fff",width=2)),
                textinfo="percent+label", textfont=dict(size=10)))
            fig_p2.update_layout(**PLOTLY_BASE, height=320, margin=dict(t=10,b=10,l=10,r=10), showlegend=False)
            st.plotly_chart(fig_p2, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    section("MONTH SUMMARY TABLE")
    st.dataframe(sum_df.style
        .format({"Target (LKR)":"LKR {:,.0f}","Achievement (LKR)":"LKR {:,.0f}",
                 "LKR Ach %":"{:.1f}%","LKR Variance":"LKR {:+,.0f}",
                 "Target (Units)":"{:,.0f}","Achievement (Units)":"{:,.0f}","Unit Ach %":"{:.1f}%"})
        .map(lambda v: ("color:#059669;font-weight:700" if v>=100 else
                        "color:#d97706;font-weight:700" if v>=80 else "color:#dc2626;font-weight:700")
             if isinstance(v,(int,float)) else "", subset=["LKR Ach %","Unit Ach %"]),
        use_container_width=True, hide_index=True)
    dl2,_ = st.columns([1,5])
    with dl2:
        st.download_button("⬇️ Export CSV", data=sum_df.to_csv(index=False).encode(),
            file_name=f"{dash_title}_all_months.csv", mime="text/csv", use_container_width=True)


# ╔══════════════════════════════════════╗
# ║  TAB 3 — DM / SBDM BREAKDOWN       ║
# ╚══════════════════════════════════════╝
with tab3:
    dm_month = st.selectbox("Month", month_list, index=month_list.index(sel_month), key="dm_m")
    dm_lkr   = all_lkr[dm_month]
    dm_u     = all_units[dm_month]
    dm_hier  = all_hierarchy[dm_month]
    dm_eo    = all_eo[dm_month]

    sbdm_list = [e for e in dm_eo if is_sbdm(e)]
    dm_list   = [e for e in dm_eo if is_dm(e)]

    # ── SBDM summary cards (if present) ──
    if sbdm_list:
        section("SBDM PERFORMANCE")
        cols = st.columns(max(len(sbdm_list), 1))
        for i, s in enumerate(sbdm_list):
            if sbdm_filter != "ALL" and s != sbdm_filter: continue
            d = dm_lkr.get(s,{})
            st_,sa_,sv_,sp_ = d.get("TAR_LKR",0),d.get("ACH_LKR",0),d.get("VAR_LKR",0),d.get("PCT_LKR",0)
            sc = pct_color(sp_)
            cols[i].markdown(f"""<div style="background:linear-gradient(135deg,#312e81,#4338ca);
                border-radius:16px;padding:1.2rem 1.3rem;color:#fff;border:1px solid #6366f1">
                <div style="font-size:.6rem;font-weight:700;color:#a5b4fc;text-transform:uppercase;margin-bottom:4px">⭐ Senior BDM</div>
                <div style="font-size:.95rem;font-weight:800;margin-bottom:10px">{s}</div>
                <div style="font-size:.72rem;color:#c7d2fe">Target: {fmt_lkr(st_)}</div>
                <div style="font-size:1rem;font-weight:700;color:{sc}">ACH: {fmt_lkr(sa_)}</div>
                <div style="display:flex;justify-content:space-between;margin-top:8px">
                    <span style="font-size:.72rem;color:{'#4ade80' if sv_>=0 else '#f87171'}">
                        {'▲' if sv_>=0 else '▼'} {fmt_lkr(abs(sv_))}</span>
                    <span style="font-size:.78rem;font-weight:800;padding:2px 10px;
                        border-radius:999px;background:rgba(255,255,255,.15);color:#fff">{sp_:.1f}%</span>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── DM summary cards — ALL DMs ──
    section(f"DM PERFORMANCE — {dm_month}")
    filtered_dms = [e for e in dm_list if dm_filter=="ALL" or e==dm_filter]
    if filtered_dms:
        dm_cols = st.columns(max(len(filtered_dms), 1))
        for i, dm in enumerate(filtered_dms):
            d = dm_lkr.get(dm,{})
            dt,da,dv,dp = d.get("TAR_LKR",0),d.get("ACH_LKR",0),d.get("VAR_LKR",0),d.get("PCT_LKR",0)
            bc = pct_color(dp); vc2 = "#059669" if dv>=0 else "#dc2626"
            bbg = "#d1fae5" if dp>=100 else "#fef3c7" if dp>=80 else "#fee2e2"
            bfg = "#065f46" if dp>=100 else "#92400e" if dp>=80 else "#991b1b"
            mw  = max(dt,da,1)
            dm_cols[i].markdown(f"""<div style="background:#fff;border:1px solid #e8edf5;
                border-radius:14px;padding:1.1rem 1.2rem;
                box-shadow:0 2px 8px rgba(0,0,0,.05);border-top:3px solid {bc}">
                <div style="font-size:.72rem;font-weight:700;color:#64748b;margin-bottom:6px"
                    title="{dm}">👤 {dm}</div>
                <div style="font-size:.75rem;color:#1e293b;font-weight:600">Target</div>
                <div style="font-size:.95rem;font-weight:700;color:#1e293b">{fmt_lkr(dt)}</div>
                <div style="background:#f1f5f9;border-radius:999px;height:5px;margin-bottom:8px">
                    <div style="width:{(dt/mw*100):.1f}%;height:100%;background:#3b82f6;border-radius:999px"></div>
                </div>
                <div style="font-size:.75rem;color:#1e293b;font-weight:600">Achievement</div>
                <div style="font-size:.95rem;font-weight:700;color:{bc}">{fmt_lkr(da)}</div>
                <div style="background:#f1f5f9;border-radius:999px;height:5px;margin-bottom:8px">
                    <div style="width:{(da/mw*100):.1f}%;height:100%;background:{bc};border-radius:999px"></div>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div style="font-size:.7rem;font-weight:600;color:{vc2}">{"+" if dv>=0 else ""}{fmt_lkr(dv)}</div>
                    <span style="font-size:.72rem;font-weight:700;padding:2px 10px;
                        border-radius:999px;background:{bbg};color:{bfg}">{dp:.1f}%</span>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── Full Hierarchy (FIXED) ──
    section(f"FULL HIERARCHY — {dm_month} (LKR)")
    render_hierarchy(dm_hier, dm_lkr, fmt_fn=fmt_lkr, label="LKR",
                     sbdm_filter=sbdm_filter, dm_filter=dm_filter)

    section(f"FULL HIERARCHY — {dm_month} (UNITS)")
    render_hierarchy(dm_hier, dm_u, fmt_fn=fmt_n, label="Units",
                     sbdm_filter=sbdm_filter, dm_filter=dm_filter)

    # DM trend
    trend = []
    for m in month_list:
        for e in all_eo[m]:
            if not is_dm(e): continue
            d = all_lkr[m].get(e,{})
            if d.get('TAR_LKR',0) > 0:
                trend.append(dict(Month=m, DM=e, ACH=d['ACH_LKR'], PCT=d['PCT_LKR']))
    if trend:
        section("DM LKR TREND")
        tr_df = pd.DataFrame(trend)
        if dm_filter != "ALL": tr_df = tr_df[tr_df["DM"]==dm_filter]
        fig_t = px.line(tr_df, x="Month", y="ACH", color="DM", markers=True,
                        color_discrete_sequence=PALETTE, labels={"ACH":"Achievement (LKR)"})
        fig_t.update_layout(**PLOTLY_BASE, height=300,
            margin=dict(t=10,b=40,l=80,r=20),
            xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
            yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),title="LKR"),
            legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.05,xanchor="right",x=1))
        st.plotly_chart(fig_t, use_container_width=True, config={"displayModeBar":False})


# ╔══════════════════════════════════════╗
# ║  TAB 4 — RP DETAIL                  ║
# ╚══════════════════════════════════════╝
with tab4:
    rp_month = st.selectbox("Month", month_list, index=month_list.index(sel_month), key="rp_m")
    rp_lkr   = all_lkr[rp_month]
    rp_u     = all_units[rp_month]
    rp_hier  = all_hierarchy[rp_month]
    rp_eo    = all_eo[rp_month]

    # Build RP maps
    rp_to_dm = {}; rp_to_sbdm = {}
    for sk, dm_dict in rp_hier.items():
        for dk, rps in dm_dict.items():
            for rp in rps:
                rp_to_dm[rp]   = dk
                rp_to_sbdm[rp] = sk if sk != '__NO_SBDM__' else None

    all_reps = [e for e in rp_eo if e!='TOTAL' and not is_dm(e) and not is_sbdm(e)]
    disp = [r for r in all_reps
            if (dm_filter=="ALL" or rp_to_dm.get(r)==dm_filter)
            and (sbdm_filter=="ALL" or rp_to_sbdm.get(r)==sbdm_filter)
            and (rp_lkr.get(r,{}).get('TAR_LKR',0)>0 or rp_lkr.get(r,{}).get('ACH_LKR',0)>0)]

    section(f"RP / SALES REP PERFORMANCE — {rp_month}")

    if not disp:
        st.info("No rep data for current filter.")
    else:
        groups = {}
        for rp in disp:
            groups.setdefault(rp_to_dm.get(rp,"Standalone"), []).append(rp)

        for owner, rps in groups.items():
            d = rp_lkr.get(owner,{})
            ot,oa,ov_,op_ = d.get("TAR_LKR",0),d.get("ACH_LKR",0),d.get("VAR_LKR",0),d.get("PCT_LKR",0)
            bc = pct_color(op_)
            sbdm_badge = ""
            for sk, dmd in rp_hier.items():
                if owner in dmd and sk != '__NO_SBDM__':
                    sbdm_badge = f'<span style="font-size:.6rem;background:rgba(139,92,246,.2);color:#a78bfa;padding:2px 8px;border-radius:999px;margin-left:8px">⭐ {sk}</span>'

            st.markdown(f"""<div style="border:1px solid #e2e8f0;border-radius:16px;
                overflow:hidden;box-shadow:0 3px 14px rgba(0,0,0,.07);margin-bottom:1.8rem">
                <div style="background:linear-gradient(135deg,#0a1628,#163870);
                    padding:1rem 1.4rem;border-left:5px solid {bc}">
                    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
                        <div>
                            <div style="font-size:.6rem;font-weight:700;color:rgba(255,255,255,.4);
                                text-transform:uppercase;margin-bottom:3px">District Manager</div>
                            <div style="font-size:1rem;font-weight:800;color:#f0f6ff">👤 {owner}{sbdm_badge}</div>
                        </div>
                        <div style="display:flex;gap:0;border:1px solid rgba(255,255,255,.15);border-radius:10px;overflow:hidden">
                            <div style="padding:.5rem 1rem;border-right:1px solid rgba(255,255,255,.15)">
                                <div style="font-size:.58rem;font-weight:700;color:rgba(255,255,255,.4);text-transform:uppercase;margin-bottom:2px">Target</div>
                                <div style="font-size:.9rem;font-weight:700;color:#cbd5e1">{fmt_lkr(ot)}</div>
                            </div>
                            <div style="padding:.5rem 1rem;border-right:1px solid rgba(255,255,255,.15)">
                                <div style="font-size:.58rem;font-weight:700;color:rgba(255,255,255,.4);text-transform:uppercase;margin-bottom:2px">Achievement</div>
                                <div style="font-size:.9rem;font-weight:700;color:{bc}">{fmt_lkr(oa)}</div>
                            </div>
                            <div style="padding:.5rem 1rem">
                                <div style="font-size:.58rem;font-weight:700;color:rgba(255,255,255,.4);text-transform:uppercase;margin-bottom:2px">Ach %</div>
                                <div style="font-size:.9rem;font-weight:800;color:{bc}">{op_:.1f}%</div>
                            </div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            rp_rows = sorted(
                [dict(name=r, TAR=rp_lkr.get(r,{}).get('TAR_LKR',0),
                      ACH=rp_lkr.get(r,{}).get('ACH_LKR',0),
                      PCT=rp_lkr.get(r,{}).get('PCT_LKR',0),
                      VAR=rp_lkr.get(r,{}).get('VAR_LKR',0))
                 for r in rps if rp_lkr.get(r,{}).get('TAR_LKR',0)>0],
                key=lambda x: x['PCT'], reverse=True)

            h = """<div style="display:flex;align-items:center;padding:7px 14px;
                background:#f8fafc;border-bottom:2px solid #e2e8f0;
                font-size:.63rem;font-weight:700;color:#94a3b8;text-transform:uppercase">
                <div style="width:26px">#</div>
                <div style="flex:1.8">Sales Rep</div>
                <div style="width:130px;text-align:right">Target</div>
                <div style="width:130px;text-align:right">Achievement</div>
                <div style="width:110px;text-align:right">Variance</div>
                <div style="flex:1.2;padding:0 12px">Progress</div>
                <div style="width:60px;text-align:center">Ach %</div>
            </div>"""
            for i2, r2 in enumerate(rp_rows):
                p2=r2['PCT']; c2=pct_color(p2); v2=r2['VAR']
                vc3="#059669" if v2>=0 else "#dc2626"
                bg2="#f0fdf4" if p2>=100 else "#fffbeb" if p2>=80 else "#fff"
                pbg="#d1fae5" if p2>=100 else "#fef3c7" if p2>=80 else "#fee2e2"
                pfg="#065f46" if p2>=100 else "#92400e" if p2>=80 else "#991b1b"
                h += f"""<div style="display:flex;align-items:center;padding:10px 14px;
                    background:{bg2};border-bottom:1px solid #f1f5f9">
                    <div style="width:26px;font-size:.68rem;font-weight:700;color:#94a3b8">#{i2+1}</div>
                    <div style="flex:1.8;font-size:.84rem;font-weight:600;color:#1e293b;
                        overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{r2['name']}</div>
                    <div style="width:130px;text-align:right;font-size:.85rem;color:#334155">{fmt_lkr(r2['TAR'])}</div>
                    <div style="width:130px;text-align:right;font-size:.85rem;font-weight:700;color:{c2}">{fmt_lkr(r2['ACH'])}</div>
                    <div style="width:110px;text-align:right;font-size:.82rem;font-weight:700;color:{vc3}">
                        {"+" if v2>=0 else ""}{fmt_lkr(v2)}</div>
                    <div style="flex:1.2;padding:0 12px">
                        <div style="background:#e8edf5;border-radius:999px;height:8px;overflow:hidden">
                            <div style="width:{min(p2,100):.1f}%;height:100%;background:{c2};border-radius:999px;opacity:.85"></div>
                        </div>
                    </div>
                    <div style="width:60px;text-align:center">
                        <span style="font-size:.74rem;font-weight:800;padding:3px 7px;
                            border-radius:7px;background:{pbg};color:{pfg}">{p2:.1f}%</span>
                    </div>
                </div>"""
            st.markdown(h + "</div>", unsafe_allow_html=True)

        # Summary table
        rp_tbl = [{"Rep":r, "Under DM":rp_to_dm.get(r,"—"),
                   "SBDM":rp_to_sbdm.get(r) or "—",
                   "Target LKR":safe_round(rp_lkr.get(r,{}).get('TAR_LKR',0)),
                   "Achievement LKR":safe_round(rp_lkr.get(r,{}).get('ACH_LKR',0)),
                   "LKR Ach %":safe_round(rp_lkr.get(r,{}).get('PCT_LKR',0),1),
                   "Target Units":safe_round(rp_u.get(r,{}).get('TAR',0)),
                   "Achievement Units":safe_round(rp_u.get(r,{}).get('ACH',0)),
                   "Unit Ach %":safe_round(rp_u.get(r,{}).get('PCT',0),1)}
                  for r in disp]
        if rp_tbl:
            section("REP SUMMARY TABLE")
            rp_df = pd.DataFrame(rp_tbl)
            st.dataframe(rp_df.style.format({
                "Target LKR":"{:,.0f}","Achievement LKR":"{:,.0f}","LKR Ach %":"{:.1f}%",
                "Target Units":"{:,.0f}","Achievement Units":"{:,.0f}","Unit Ach %":"{:.1f}%"}),
                use_container_width=True, hide_index=True)
            dl3,_ = st.columns([1,5])
            with dl3:
                st.download_button("⬇️ Export CSV", data=rp_df.to_csv(index=False).encode(),
                    file_name=f"{dash_title}_reps_{rp_month}.csv", mime="text/csv", use_container_width=True)


# ╔══════════════════════════════════════╗
# ║  TAB 5 — PRODUCTS                   ║
# ╚══════════════════════════════════════╝
with tab5:
    section(f"PRODUCT BREAKDOWN — {sel_month}")
    prd = all_prod.get(sel_month, pd.DataFrame())
    if prd.empty:
        st.info("No product data.")
    else:
        ent_opts = ["ALL"] + sorted(prd["ENTITY"].unique().tolist())
        sel_ent  = st.selectbox("Filter by Entity", ent_opts, key="prod_ent")
        prd_f    = prd if sel_ent=="ALL" else prd[prd["ENTITY"]==sel_ent]
        prd_f    = prd_f[prd_f["TAR"]>0].copy()

        if not prd_f.empty:
            prod_sum = prd_f.groupby("PRODUCT").agg(TAR=("TAR","sum"), ACH=("ACH","sum")).reset_index()
            prod_sum["PCT"] = prod_sum.apply(lambda r: r["ACH"]/r["TAR"]*100 if r["TAR"]>0 else 0, axis=1)
            prod_sum = prod_sum.sort_values("TAR", ascending=False)

            p1,p2,p3,p4 = st.columns(4)
            kpi_card(p1,"Products",str(prod_sum["PRODUCT"].nunique()),"📦","c-blue")
            kpi_card(p2,"Total Unit Target",fmt_n(prod_sum["TAR"].sum()),"🎯","c-indigo")
            kpi_card(p3,"Total Unit Achievement",fmt_n(prod_sum["ACH"].sum()),"✅","c-green")
            best_p = prod_sum.loc[prod_sum["PCT"].idxmax(),"PRODUCT"]
            kpi_card(p4,"Best Product",best_p,"🏆","c-amber",
                     badge_text=f"{prod_sum['PCT'].max():.1f}%", badge_cls="up")

            cp1,cp2 = st.columns(2)
            with cp1:
                st.markdown('<div class="card"><div class="card-title">Unit TAR vs ACH by Product</div>', unsafe_allow_html=True)
                fig_pb = go.Figure()
                fig_pb.add_trace(go.Bar(name="Target", x=prod_sum["PRODUCT"], y=prod_sum["TAR"],
                    marker=dict(color="#93c5fd",line=dict(width=0)), width=0.4, offset=-0.2))
                fig_pb.add_trace(go.Bar(name="Achievement", x=prod_sum["PRODUCT"], y=prod_sum["ACH"],
                    marker=dict(color=[pct_color(p) for p in prod_sum["PCT"]],opacity=.9,line=dict(width=0)),
                    width=0.4, offset=0.1,
                    text=[f"{p:.1f}%" for p in prod_sum["PCT"]], textposition="outside", textfont=dict(size=10)))
                fig_pb.update_layout(**PLOTLY_BASE, barmode="overlay", height=320,
                    margin=dict(t=10,b=80,l=60,r=10),
                    xaxis=dict(tickangle=-35,tickfont=dict(size=10,color="#64748b"),showgrid=False),
                    yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),title="Units"),
                    legend=dict(orientation="h",y=1.05,bgcolor="rgba(0,0,0,0)"))
                st.plotly_chart(fig_pb, use_container_width=True, config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

            with cp2:
                st.markdown('<div class="card"><div class="card-title">Unit Ach % by Product</div>', unsafe_allow_html=True)
                ps = prod_sum.sort_values("PCT", ascending=True)
                fig_h = go.Figure(go.Bar(
                    y=ps["PRODUCT"], x=ps["PCT"], orientation="h",
                    marker=dict(color=[pct_color(p) for p in ps["PCT"]],opacity=.85,line=dict(width=0)),
                    text=[f"{p:.1f}%" for p in ps["PCT"]], textposition="outside"))
                fig_h.add_vline(x=100, line_color="#22c55e", line_dash="dot", line_width=1.5)
                fig_h.update_layout(**PLOTLY_BASE, height=320,
                    margin=dict(t=10,b=40,l=180,r=60),
                    xaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),ticksuffix="%"),
                    yaxis=dict(tickfont=dict(size=10,color="#64748b")))
                st.plotly_chart(fig_h, use_container_width=True, config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

            section("PRODUCT DETAIL TABLE")
            prod_tbl = prod_sum.copy()
            prod_tbl["Variance"] = prod_tbl["ACH"] - prod_tbl["TAR"]
            prod_tbl.columns = ["Product","Target (Units)","Achievement (Units)","Unit Ach %","Variance (Units)"]
            st.dataframe(prod_tbl.style.format({
                "Target (Units)":"{:,.0f}","Achievement (Units)":"{:,.0f}",
                "Unit Ach %":"{:.1f}%","Variance (Units)":"{:+,.0f}"}),
                use_container_width=True, hide_index=True)

# ╔══════════════════════════════════════╗
# ║  TAB 6 — CUMULATIVE                 ║
# ╚══════════════════════════════════════╝
with tab6:
    section("📊 CUMULATIVE ACHIEVEMENT — ALL MONTHS")

    # Build cumulative data
    all_products_set = set()
    for m in month_list:
        for ent_data in all_prod_entity.get(m, {}).values():
            all_products_set.update(ent_data.keys())
    all_products_list = sorted(all_products_set)

    # Collect all entities across months
    seen_ents = []
    seen_set  = set()
    for m in month_list:
        for e in all_eo.get(m, []):
            if e not in seen_set:
                seen_ents.append(e)
                seen_set.add(e)

    # Build running cumulative
    cum_data   = {}
    running_t  = {}
    running_a  = {}
    for m in month_list:
        pe = all_prod_entity.get(m, {})
        cum_data[m] = {}
        for entity in seen_ents:
            ep = pe.get(entity, {})
            running_t.setdefault(entity, {})
            running_a.setdefault(entity, {})
            cum_data[m][entity] = {}
            for prod in all_products_list:
                mt = ep.get(prod, {}).get('TAR', 0.0)
                ma = ep.get(prod, {}).get('ACH', 0.0)
                running_t[entity][prod] = running_t[entity].get(prod, 0.0) + mt
                running_a[entity][prod] = running_a[entity].get(prod, 0.0) + ma
                ct = running_t[entity][prod]
                ca = running_a[entity][prod]
                cum_data[m][entity][prod] = dict(
                    CUM_TAR=ct, CUM_ACH=ca,
                    CUM_PCT=(ca/ct*100) if ct > 0 else 0.0,
                    MONTH_TAR=mt, MONTH_ACH=ma,
                )

    # Controls
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        cum_sel_month = st.selectbox("Cumulative up to Month", month_list,
                                      index=len(month_list)-1, key="cum_month")
    with cc2:
        ent_opts_cum  = ["ALL (TOTAL)"] + [e for e in seen_ents if e != 'TOTAL']
        cum_sel_ent   = st.selectbox("Entity", ent_opts_cum, key="cum_entity")
    with cc3:
        prod_opts_cum = ["ALL Products"] + all_products_list
        cum_sel_prod  = st.selectbox("Product", prod_opts_cum, key="cum_prod")

    months_upto    = month_list[:month_list.index(cum_sel_month)+1]
    entity_for_kpi = 'TOTAL' if cum_sel_ent == "ALL (TOTAL)" else cum_sel_ent

    # KPI totals
    cum_tar_t = cum_ach_t = 0.0
    for prod in all_products_list:
        if cum_sel_prod != "ALL Products" and prod != cum_sel_prod: continue
        d = cum_data.get(cum_sel_month, {}).get(entity_for_kpi, {}).get(prod, {})
        cum_tar_t += d.get('CUM_TAR', 0.0)
        cum_ach_t += d.get('CUM_ACH', 0.0)
    cum_pct_t = (cum_ach_t / cum_tar_t * 100) if cum_tar_t > 0 else 0.0
    cum_var_t = cum_ach_t - cum_tar_t

    section(f"CUMULATIVE KPIs — APR → {cum_sel_month}")
    ck1, ck2, ck3, ck4 = st.columns(4)
    kpi_card(ck1, "Cumulative Target (Units)", fmt_n(cum_tar_t), "🎯", "c-blue",
             sub=f"{len(months_upto)} months")
    kpi_card(ck2, "Cumulative Achievement (Units)", fmt_n(cum_ach_t), "✅", "c-green",
             badge_text=f"{'▲' if cum_var_t>=0 else '▼'} {fmt_n(abs(cum_var_t))}",
             badge_cls=pct_cls(cum_pct_t))
    kpi_card(ck3, "Cumulative Ach %", f"{cum_pct_t:.1f}%", "📈",
             "c-green" if cum_pct_t>=100 else "c-amber" if cum_pct_t>=80 else "c-red",
             badge_text="On Track" if cum_pct_t>=100 else "Below Target",
             badge_cls=pct_cls(cum_pct_t))
    kpi_card(ck4, "Months Accumulated", str(len(months_upto)), "📅", "c-indigo",
             sub=" → ".join(months_upto))

    st.markdown("<br>", unsafe_allow_html=True)

    # Cumulative trend chart by product
    chart_rows = []
    prods_to_chart = all_products_list if cum_sel_prod == "ALL Products" else [cum_sel_prod]
    for prod in prods_to_chart:
        for m in months_upto:
            d = cum_data.get(m, {}).get(entity_for_kpi, {}).get(prod, {})
            ct = d.get('CUM_TAR', 0.0); ca = d.get('CUM_ACH', 0.0); cp = d.get('CUM_PCT', 0.0)
            if ct > 0:
                chart_rows.append(dict(Month=m, Product=prod, CUM_PCT=cp, CUM_TAR=ct, CUM_ACH=ca))

    if chart_rows:
        cc_df = pd.DataFrame(chart_rows)
        col_line, col_bar = st.columns([3, 2])
        with col_line:
            st.markdown('<div class="card"><div class="card-title">Cumulative Ach % Trend by Product</div>', unsafe_allow_html=True)
            fig_cl = px.line(cc_df, x="Month", y="CUM_PCT", color="Product", markers=True,
                             color_discrete_sequence=PALETTE,
                             labels={"CUM_PCT":"Cumulative Ach %"})
            fig_cl.add_hline(y=100, line_color="#22c55e", line_dash="dot", line_width=2)
            fig_cl.update_layout(**PLOTLY_BASE, height=340,
                margin=dict(t=10,b=40,l=70,r=20),
                xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
                yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),
                           title="Cumulative Ach %", ticksuffix="%"),
                legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.05,xanchor="right",x=1,font=dict(size=10)))
            st.plotly_chart(fig_cl, use_container_width=True, config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

        with col_bar:
            last_m_df = cc_df[cc_df["Month"]==cum_sel_month].sort_values("CUM_PCT", ascending=True)
            if not last_m_df.empty:
                st.markdown(f'<div class="card"><div class="card-title">Product Ach % as of {cum_sel_month}</div>', unsafe_allow_html=True)
                fig_cb = go.Figure(go.Bar(
                    y=last_m_df["Product"], x=last_m_df["CUM_PCT"], orientation="h",
                    marker=dict(color=[pct_color(p) for p in last_m_df["CUM_PCT"]], opacity=.85, line=dict(width=0)),
                    text=[f"{p:.1f}%" for p in last_m_df["CUM_PCT"]], textposition="outside"))
                fig_cb.add_vline(x=100, line_color="#22c55e", line_dash="dot", line_width=1.5)
                fig_cb.update_layout(**PLOTLY_BASE, height=340,
                    margin=dict(t=10,b=40,l=160,r=70),
                    xaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),ticksuffix="%"),
                    yaxis=dict(tickfont=dict(size=10,color="#64748b")))
                st.plotly_chart(fig_cb, use_container_width=True, config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

    # Entity comparison
    section(f"ENTITY COMPARISON — Cumulative as of {cum_sel_month}")
    comp_prod = st.selectbox("Product for Comparison", ["ALL Products"]+all_products_list, key="cum_comp")
    comp_rows = []
    for entity in seen_ents:
        if entity == 'TOTAL': continue
        prds = all_products_list if comp_prod == "ALL Products" else [comp_prod]
        c_t = sum(cum_data.get(cum_sel_month,{}).get(entity,{}).get(p,{}).get('CUM_TAR',0.0) for p in prds)
        c_a = sum(cum_data.get(cum_sel_month,{}).get(entity,{}).get(p,{}).get('CUM_ACH',0.0) for p in prds)
        c_p = (c_a/c_t*100) if c_t > 0 else 0.0
        if c_t > 0:
            et = "SBDM" if is_sbdm(entity) else "DM" if is_dm(entity) else "RP/Rep"
            comp_rows.append(dict(Entity=entity, Type=et,
                                   CUM_TAR=c_t, CUM_ACH=c_a, CUM_PCT=c_p, CUM_VAR=c_a-c_t))

    if comp_rows:
        comp_df = pd.DataFrame(comp_rows).sort_values("CUM_PCT", ascending=False)

        # Achievement bar visual
        for _, row in comp_df.iterrows():
            p = row['CUM_PCT']; c = pct_color(p); pb = pct_badge(p)
            bg = "#f0fdf4" if p>=100 else "#fffbeb" if p>=80 else "#fff"
            vc = "#059669" if row['CUM_VAR']>=0 else "#dc2626"
            et_icon = "⭐" if row['Type']=="SBDM" else "👤" if row['Type']=="DM" else "•"
            st.markdown(f"""<div style="display:flex;align-items:center;gap:12px;
                padding:10px 16px;border-radius:12px;margin-bottom:6px;
                border:1px solid #e2e8f0;background:{bg}">
                <div style="width:20px;font-size:.9rem">{et_icon}</div>
                <div style="flex:1;font-size:.84rem;font-weight:600;color:#1e293b;
                    overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{row['Entity']}</div>
                <div style="flex:2;background:#f1f5f9;border-radius:999px;height:9px;overflow:hidden">
                    <div style="width:{min(p,100):.1f}%;height:100%;background:{c};border-radius:999px;opacity:.85"></div>
                </div>
                <div style="width:100px;text-align:right;font-size:.78rem;color:#94a3b8">{fmt_n(row['CUM_TAR'])}</div>
                <div style="width:100px;text-align:right;font-size:.78rem;font-weight:700;color:{c}">{fmt_n(row['CUM_ACH'])}</div>
                <div style="width:90px;text-align:right;font-size:.75rem;font-weight:700;color:{vc}">
                    {"+" if row['CUM_VAR']>=0 else ""}{fmt_n(row['CUM_VAR'])}</div>
                <div style="width:58px;text-align:center">
                    <span class="{pb}" style="font-size:.72rem;font-weight:800;padding:3px 9px;border-radius:999px;
                    {'background:#dcfce7;color:#15803d' if p>=100 else 'background:#fef3c7;color:#92400e' if p>=80 else 'background:#fee2e2;color:#b91c1c'}">{p:.1f}%</span>
                </div>
            </div>""", unsafe_allow_html=True)

        # Download
        comp_disp = comp_df.rename(columns={"CUM_TAR":"Cum Target","CUM_ACH":"Cum Achievement",
                                              "CUM_PCT":"Cum Ach %","CUM_VAR":"Cum Variance"})
        dl7, _ = st.columns([1,5])
        with dl7:
            st.download_button("⬇️ Export Cumulative CSV",
                data=comp_disp.to_csv(index=False).encode(),
                file_name=f"{dash_title}_cumulative_{cum_sel_month}.csv",
                mime="text/csv", use_container_width=True)

# ══════════════════════════════════════════════════════
st.markdown(f'<div style="text-align:center;font-size:.72rem;color:#94a3b8;margin-top:2.5rem;'
            f'padding-top:1rem;border-top:1px solid #e2e8f0">'
            f'Universal Sales Intelligence Hub · {dash_title} · v14.0</div>', unsafe_allow_html=True)
