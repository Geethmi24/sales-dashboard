"""
Universal Sales Intelligence Hub — v13.0
Hierarchy-aware: TOTAL → SBDM → DM → RP (SBDM optional)
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
.c-blue .kpi-icon-wrap{background:#dbeafe;}.c-green .kpi-icon-wrap{background:#dcfce7;}
.c-amber .kpi-icon-wrap{background:#fef3c7;}.c-purple .kpi-icon-wrap{background:#ede9fe;}
.c-red .kpi-icon-wrap{background:#fee2e2;}.c-teal .kpi-icon-wrap{background:#ccfbf1;}
.c-indigo .kpi-icon-wrap{background:#e0e7ff;}.c-orange .kpi-icon-wrap{background:#ffedd5;}
.kpi-label{font-size:.7rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:5px;}
.kpi-value{font-size:1.75rem;font-weight:800;color:#0f172a;line-height:1;letter-spacing:-.03em;}
.kpi-sub{font-size:.72rem;color:#94a3b8;margin-top:4px;}
.kpi-badge{display:inline-flex;align-items:center;gap:3px;font-size:.72rem;font-weight:700;padding:3px 9px;border-radius:999px;margin-top:8px;}
.kpi-badge.up{background:#dcfce7;color:#15803d;}.kpi-badge.down{background:#fee2e2;color:#b91c1c;}.kpi-badge.neu{background:#f1f5f9;color:#64748b;}

.card{background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:1.3rem 1.4rem .8rem;box-shadow:0 2px 8px rgba(0,0,0,.05);margin-bottom:1rem;}
.card-header{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:.3rem;}
.card-title{font-size:.9rem;font-weight:700;color:#1e293b;}
.card-sub{font-size:.72rem;color:#94a3b8;margin-top:2px;}
.card-badge{font-size:.68rem;font-weight:700;padding:3px 10px;border-radius:999px;background:#f1f5f9;color:#64748b;white-space:nowrap;}

.sec-div{display:flex;align-items:center;gap:12px;margin:2rem 0 1.2rem;}
.sec-div-line{flex:1;height:1px;background:#e2e8f0;}
.sec-div-text{font-size:.72rem;font-weight:800;color:#94a3b8;text-transform:uppercase;letter-spacing:.1em;white-space:nowrap;}

/* ── HIERARCHY TREE STYLES ── */
.hier-total-block{background:linear-gradient(135deg,#0f172a,#1e3a5f);border-radius:18px;padding:1.4rem 1.8rem;margin-bottom:1.5rem;border:1px solid #334155;}
.hier-total-title{font-size:.65rem;font-weight:800;color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:.14em;margin-bottom:6px;}
.hier-total-name{font-size:1.2rem;font-weight:800;color:#f0f9ff;margin-bottom:12px;}
.hier-total-kpis{display:flex;gap:24px;flex-wrap:wrap;}
.hier-kpi-lbl{font-size:.6rem;font-weight:700;color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:.1em;margin-bottom:2px;}
.hier-kpi-val{font-size:1.1rem;font-weight:800;color:#fff;}

/* SBDM block */
.sbdm-block{border:2px solid #7c3aed;border-radius:16px;margin-bottom:1.4rem;overflow:hidden;box-shadow:0 4px 16px rgba(124,58,237,.15);}
.sbdm-header{background:linear-gradient(135deg,#4c1d95,#6d28d9);padding:1rem 1.4rem;display:flex;align-items:center;justify-content:space-between;}
.sbdm-badge{font-size:.58rem;font-weight:800;padding:2px 10px;border-radius:999px;background:rgba(255,255,255,.15);color:#ddd6fe;text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px;display:inline-block;}
.sbdm-name{font-size:1rem;font-weight:800;color:#fff;}
.sbdm-kpis{display:flex;gap:16px;}
.sbdm-kpi-lbl{font-size:.6rem;font-weight:700;color:rgba(255,255,255,.5);text-transform:uppercase;margin-bottom:2px;}
.sbdm-kpi-val{font-size:.95rem;font-weight:800;color:#fff;}
.sbdm-body{background:#faf5ff;padding:.6rem 1rem 1rem;}

/* DM block */
.dm-block{border:1.5px solid #3b82f6;border-radius:12px;margin-bottom:1rem;overflow:hidden;box-shadow:0 2px 8px rgba(59,130,246,.12);}
.dm-header{background:linear-gradient(135deg,#1e3a5f,#1d4ed8);padding:.85rem 1.2rem;display:flex;align-items:center;justify-content:space-between;}
.dm-badge{font-size:.55rem;font-weight:800;padding:2px 8px;border-radius:999px;background:rgba(255,255,255,.15);color:#bfdbfe;text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px;display:inline-block;}
.dm-name{font-size:.9rem;font-weight:800;color:#fff;}
.dm-kpis{display:flex;gap:14px;}
.dm-kpi-lbl{font-size:.58rem;font-weight:700;color:rgba(255,255,255,.5);text-transform:uppercase;margin-bottom:2px;}
.dm-kpi-val{font-size:.88rem;font-weight:800;color:#fff;}
.dm-body{background:#eff6ff;padding:.4rem .8rem .8rem;}

/* RP rows */
.rp-row{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:10px;margin-bottom:6px;background:#fff;border:1px solid #e2e8f0;}
.rp-row:hover{box-shadow:0 3px 10px rgba(0,0,0,.08);}
.rp-badge{font-size:.55rem;font-weight:800;padding:1px 7px;border-radius:999px;background:#f1f5f9;color:#64748b;text-transform:uppercase;letter-spacing:.08em;flex-shrink:0;}
.rp-name{font-size:.83rem;font-weight:600;color:#1e293b;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.rp-track{flex:2;background:#f1f5f9;border-radius:999px;height:8px;overflow:hidden;min-width:60px;}
.rp-fill{height:100%;border-radius:999px;}
.rp-tar{font-size:.72rem;color:#94a3b8;width:80px;text-align:right;flex-shrink:0;}
.rp-ach{font-size:.72rem;font-weight:700;width:80px;text-align:right;flex-shrink:0;}
.rp-pct{font-size:.7rem;font-weight:800;padding:2px 8px;border-radius:999px;width:52px;text-align:center;flex-shrink:0;}
.rp-pct.green{background:#dcfce7;color:#15803d;}
.rp-pct.amber{background:#fef3c7;color:#92400e;}
.rp-pct.red{background:#fee2e2;color:#b91c1c;}

/* standalone DMs (no SBDM above) */
.dm-standalone{border-left:4px solid #3b82f6;}

/* summary bar */
.rollup-bar{display:flex;align-items:center;gap:10px;padding:8px 12px;background:#f0f9ff;border-top:2px solid #bae6fd;border-radius:0 0 10px 10px;font-size:.75rem;font-weight:700;color:#0369a1;}

.ach-row{display:flex;align-items:center;gap:12px;padding:10px 16px;border-radius:12px;margin-bottom:8px;border:1px solid #e2e8f0;background:#fff;}
.ach-row:hover{box-shadow:0 4px 12px rgba(0,0,0,.08);}
.ach-rank{font-size:.72rem;font-weight:800;color:#94a3b8;width:20px;text-align:center;flex-shrink:0;}
.ach-name{font-size:.83rem;font-weight:600;color:#1e293b;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.ach-track{flex:2;background:#f1f5f9;border-radius:999px;height:10px;overflow:hidden;}
.ach-fill{height:100%;border-radius:999px;}
.ach-tar{font-size:.7rem;color:#94a3b8;width:90px;text-align:right;flex-shrink:0;}
.ach-ach{font-size:.7rem;font-weight:700;width:90px;text-align:right;flex-shrink:0;}
.ach-pct-badge{font-size:.72rem;font-weight:800;padding:3px 10px;border-radius:999px;width:58px;text-align:center;flex-shrink:0;}
.ach-pct-badge.green{background:#dcfce7;color:#15803d;}
.ach-pct-badge.amber{background:#fef3c7;color:#92400e;}
.ach-pct-badge.red{background:#fee2e2;color:#b91c1c;}

.cum-matrix-wrap{overflow-x:auto;border-radius:14px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,.05);}
.cum-matrix-table{width:100%;border-collapse:collapse;font-size:.8rem;}
.cum-matrix-table th{background:#1e3a5f;color:#e2e8f0;font-weight:700;padding:10px 14px;text-align:center;font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap;position:sticky;top:0;}
.cum-matrix-table th.entity-col{text-align:left;background:#0f172a;min-width:160px;}
.cum-matrix-table td{padding:9px 14px;border-bottom:1px solid #f1f5f9;white-space:nowrap;}
.cum-matrix-table td.entity-name{font-weight:700;color:#1e293b;background:#fafafa;border-right:2px solid #e2e8f0;position:sticky;left:0;}
.cum-matrix-table tr:hover td{background:#f8fafc;}
.pct-green{background:#dcfce7;color:#15803d;}
.pct-amber{background:#fef3c7;color:#92400e;}
.pct-red{background:#fee2e2;color:#b91c1c;}
.pct-zero{background:#f1f5f9;color:#94a3b8;}

.landing{display:flex;flex-direction:column;align-items:center;padding:4rem 2rem 3rem;text-align:center;}
.landing-logo{font-size:3.5rem;margin-bottom:1.2rem;}
.landing h2{font-size:1.5rem;font-weight:800;color:#1e293b;margin-bottom:.6rem;}
.landing p{font-size:.88rem;color:#64748b;max-width:480px;line-height:1.7;}
.landing-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;padding:1.3rem 1.8rem;margin-top:1.8rem;text-align:left;max-width:560px;width:100%;}
.landing-card h4{font-size:.78rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.8rem;}
.landing-card li{font-size:.83rem;color:#475569;margin-bottom:.4rem;line-height:1.5;}
.landing-card code{background:#e2e8f0;padding:1px 5px;border-radius:4px;font-size:.8rem;color:#1e293b;}

.dash-footer{text-align:center;font-size:.72rem;color:#94a3b8;margin-top:2.5rem;padding-top:1.2rem;border-top:1px solid #e2e8f0;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════
PALETTE = [
    "#3b82f6","#22c55e","#f59e0b","#ef4444","#8b5cf6",
    "#ec4899","#14b8a6","#f97316","#06b6d4","#a78bfa",
    "#84cc16","#64748b",
]
PLOTLY_BASE = dict(
    font=dict(family="Plus Jakarta Sans, sans-serif", size=12),
    plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
    hoverlabel=dict(bgcolor="#0f172a", font_size=12, font_color="#f8fafc", bordercolor="#1e3a5f"),
)
SKIP_SHEETS = {'SOURCE','HO','SPC','SOURCE (2)','SIX MONTHS',
               'JAN-2','FEB-2','MAR-2','six months','DEC-2'}
MONTH_ORDER = ['APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC','JAN','FEB','MAR']

# ══════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════
def fmt_n(n, dec=0):
    try: return f"{int(round(float(n))):,}"
    except: return str(n)

def fmt_lkr(n):
    try: return f"LKR {int(round(float(n))):,}"
    except: return str(n)

def fmt_lkr_short(n):
    try:
        v = float(n)
        if abs(v) >= 1_000_000: return f"LKR {v/1_000_000:.2f}M"
        if abs(v) >= 1_000: return f"LKR {v/1_000:.1f}K"
        return f"LKR {v:,.0f}"
    except: return str(n)

def pct_cls(p):   return "up" if p >= 100 else "neu" if p >= 80 else "down"
def pct_color(p): return "#16a34a" if p >= 100 else "#d97706" if p >= 80 else "#dc2626"
def pct_badge(p): return "green" if p >= 100 else "amber" if p >= 80 else "red"

# ── Hierarchy detection ──────────────────────────────
def is_sbdm(name):
    """Senior BDM — contains SBDM (case-insensitive)"""
    return "SBDM" in str(name).upper()

def is_dm(name):
    """District Manager — contains (DM) but NOT SBDM"""
    n = str(name).upper()
    return "(DM)" in n and "SBDM" not in n

def is_rp(name):
    """Regular sales rep — neither TOTAL, SBDM, nor DM"""
    n = str(name).upper()
    return name != "TOTAL" and not is_sbdm(name) and not is_dm(name)

def get_role(name):
    if name == "TOTAL": return "TOTAL"
    if is_sbdm(name):   return "SBDM"
    if is_dm(name):     return "DM"
    return "RP"

def section(title):
    st.markdown(f"""
    <div class="sec-div">
        <div class="sec-div-line"></div>
        <div class="sec-div-text">{title}</div>
        <div class="sec-div-line"></div>
    </div>""", unsafe_allow_html=True)

def kpi_card(col, label, value, icon, color, badge_text=None, badge_cls="neu", sub=None):
    badge = f'<div class="kpi-badge {badge_cls}">{badge_text}</div>' if badge_text else ""
    sub_  = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    col.markdown(f"""
    <div class="kpi-card {color}">
        <div class="kpi-icon-wrap">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {sub_}{badge}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# HIERARCHY BUILDER  ← v13 core change
# ══════════════════════════════════════════════════════
def build_hierarchy(ordered_entities):
    """
    Build a hierarchy dict from the ordered entity list.

    Rules:
      TOTAL → SBDM → DM → RP
      If no SBDM exists → TOTAL → DM → RP
      If no DM above an RP, attach to last seen DM (or SBDM if no DM yet)

    Returns:
      {
        'has_sbdm': bool,
        'sbdm_nodes': [
            {
              'name': 'BUDDHIKA (SBDM)',
              'dms': [
                  {'name': 'NILANJANA (DM)', 'rps': ['RAVI','DASUN',...]},
                  ...
              ]
            }
        ],
        # when no SBDM, sbdm_nodes will have ONE fake node with name=None
        'all_dms': ['NILANJANA (DM)', ...],   # flat list for quick lookup
        'entity_roles': {'NILANJANA (DM)': 'DM', 'RAVI': 'RP', ...}
      }
    """
    non_total = [e for e in ordered_entities if e != "TOTAL"]

    has_sbdm = any(is_sbdm(e) for e in non_total)
    entity_roles = {e: get_role(e) for e in ordered_entities}

    sbdm_nodes = []
    cur_sbdm   = None
    cur_dm     = None

    if has_sbdm:
        for e in non_total:
            role = get_role(e)
            if role == "SBDM":
                cur_sbdm = {"name": e, "dms": []}
                sbdm_nodes.append(cur_sbdm)
                cur_dm = None
            elif role == "DM":
                if cur_sbdm is None:
                    # DM before any SBDM — create implicit node
                    cur_sbdm = {"name": None, "dms": []}
                    sbdm_nodes.append(cur_sbdm)
                cur_dm = {"name": e, "rps": []}
                cur_sbdm["dms"].append(cur_dm)
            else:  # RP
                if cur_dm is not None:
                    cur_dm["rps"].append(e)
                elif cur_sbdm is not None:
                    # RP directly under SBDM (no DM yet) — attach to last DM or make orphan
                    if cur_sbdm["dms"]:
                        cur_sbdm["dms"][-1]["rps"].append(e)
    else:
        # No SBDM — single fake top-level node
        fake = {"name": None, "dms": []}
        sbdm_nodes.append(fake)
        for e in non_total:
            role = get_role(e)
            if role == "DM":
                cur_dm = {"name": e, "rps": []}
                fake["dms"].append(cur_dm)
            else:  # RP
                if cur_dm is not None:
                    cur_dm["rps"].append(e)
                elif fake["dms"]:
                    fake["dms"][-1]["rps"].append(e)

    all_dms = []
    for sn in sbdm_nodes:
        for dm in sn["dms"]:
            if dm["name"]: all_dms.append(dm["name"])

    return {
        "has_sbdm": has_sbdm,
        "sbdm_nodes": sbdm_nodes,
        "all_dms": all_dms,
        "entity_roles": entity_roles,
    }

# ══════════════════════════════════════════════════════
# EXCEL PARSING — v13
# ══════════════════════════════════════════════════════
def find_total_row(raw):
    for i in range(2, min(80, raw.shape[0])):
        val_b = str(raw.iloc[i, 1]).strip() if pd.notna(raw.iloc[i, 1]) else ''
        if val_b != 'TOTAL': continue
        for col in range(4, min(raw.shape[1], 10)):
            val = raw.iloc[i, col]
            if pd.notna(val):
                try:
                    if float(val) > 100000: return i
                except: pass
    return None

def find_product_rows(raw, total_row):
    prod_rows = []
    skip_names = {'', 'nan', 'TOTAL', '0', 'PRODUCT', '#'}
    for r in range(2, total_row):
        pname = raw.iloc[r, 1]
        if not isinstance(pname, str): continue
        pname = pname.strip()
        if pname in skip_names: continue
        tar = pd.to_numeric(raw.iloc[r, 4], errors='coerce')
        if pd.notna(tar) and float(tar) > 0:
            prod_rows.append(r)
    return prod_rows

def parse_excel(file_obj):
    xls = pd.ExcelFile(file_obj)
    sheets = [s for s in xls.sheet_names if s.upper() not in {x.upper() for x in SKIP_SHEETS}]

    all_lkr           = {}
    all_units         = {}
    all_hierarchy     = {}   # ← replaces all_dm_rp
    all_eo            = {}
    all_prod          = {}
    all_prod_entity   = {}

    for sheet in sheets:
        try:
            raw = pd.read_excel(file_obj, sheet_name=sheet, header=None)
        except Exception: continue
        if raw.shape[0] < 6 or raw.shape[1] < 6: continue

        lkr_row_idx = find_total_row(raw)
        if lkr_row_idx is None: continue

        prod_rows = find_product_rows(raw, lkr_row_idx)
        if not prod_rows: continue

        # ── Parse entity columns ─────────────────────────────────
        entity_cols = {}
        name_count  = {}
        for j in range(4, raw.shape[1] - 1, 2):
            name_cell = raw.iloc[0, j] if j < raw.shape[1] else None
            if pd.isna(name_cell) or str(name_cell).strip() in ('', 'nan'): continue
            hdr = str(raw.iloc[1, j]).strip() if pd.notna(raw.iloc[1, j]) else ''
            if hdr not in ('TAR', ''): continue
            base_name = str(name_cell).strip()
            if base_name in name_count:
                name_count[base_name] += 1
                unique_name = f"{base_name}-{name_count[base_name]}"
            else:
                name_count[base_name] = 1
                unique_name = base_name
            entity_cols[unique_name] = j

        if not entity_cols: continue

        ordered_entities = list(entity_cols.keys())
        all_eo[sheet]       = ordered_entities
        all_hierarchy[sheet] = build_hierarchy(ordered_entities)   # ← v13

        # ── Unit data ────────────────────────────────────────────
        units_ms          = {}
        prod_entity_sheet = {}

        for ename, tc in entity_cols.items():
            ac = tc + 1
            tar_vals = raw.iloc[prod_rows, tc].apply(pd.to_numeric, errors='coerce').fillna(0)
            ach_vals = (raw.iloc[prod_rows, ac].apply(pd.to_numeric, errors='coerce').fillna(0)
                        if ac < raw.shape[1] else pd.Series([0]*len(prod_rows)))
            tar_t = float(tar_vals.sum()); ach_t = float(ach_vals.sum())
            units_ms[ename] = dict(TAR=tar_t, ACH=ach_t, VAR=ach_t-tar_t,
                                    PCT=(ach_t/tar_t*100) if tar_t else 0.0)
            prod_entity_sheet[ename] = {}
            for idx_r, r in enumerate(prod_rows):
                pname = str(raw.iloc[r, 1]).strip()
                t = float(tar_vals.iloc[idx_r]) if pd.notna(tar_vals.iloc[idx_r]) else 0.0
                a = float(ach_vals.iloc[idx_r]) if pd.notna(ach_vals.iloc[idx_r]) else 0.0
                prod_entity_sheet[ename][pname] = dict(TAR=max(t,0), ACH=max(a,0))

        all_units[sheet]       = units_ms
        all_prod_entity[sheet] = prod_entity_sheet

        # ── LKR row ──────────────────────────────────────────────
        lkr_ms = {}
        for ename, tc in entity_cols.items():
            ac = tc + 1
            tar_lkr = pd.to_numeric(raw.iloc[lkr_row_idx, tc], errors='coerce')
            ach_lkr = (pd.to_numeric(raw.iloc[lkr_row_idx, ac], errors='coerce')
                       if ac < raw.shape[1] else np.nan)
            tar_lkr = float(tar_lkr) if pd.notna(tar_lkr) else 0.0
            ach_lkr = float(ach_lkr) if pd.notna(ach_lkr) else 0.0
            lkr_ms[ename] = dict(TAR_LKR=tar_lkr, ACH_LKR=ach_lkr,
                                  VAR_LKR=ach_lkr-tar_lkr,
                                  PCT_LKR=(ach_lkr/tar_lkr*100) if tar_lkr else 0.0)
        all_lkr[sheet] = lkr_ms

        # ── Product DataFrame ────────────────────────────────────
        prod_rows_list = []
        for r in prod_rows:
            pname = str(raw.iloc[r, 1]).strip()
            for ename, tc in entity_cols.items():
                ac = tc + 1
                t = pd.to_numeric(raw.iloc[r, tc], errors='coerce')
                a = pd.to_numeric(raw.iloc[r, ac], errors='coerce') if ac < raw.shape[1] else np.nan
                t = float(t) if pd.notna(t) else 0.0
                a = float(a) if pd.notna(a) else 0.0
                if t == 0 and a == 0: continue
                prod_rows_list.append(dict(ENTITY=ename, PRODUCT=pname,
                    TAR=t, ACH=a, VAR=a-t, PCT=(a/t*100) if t else 0.0))
        all_prod[sheet] = pd.DataFrame(prod_rows_list) if prod_rows_list else pd.DataFrame()

    return all_lkr, all_units, all_hierarchy, all_eo, all_prod, all_prod_entity

# ══════════════════════════════════════════════════════
# CUMULATIVE
# ══════════════════════════════════════════════════════
def build_cumulative_data(month_list, all_prod_entity, all_eo):
    all_products = set()
    for m in month_list:
        for ent_data in all_prod_entity.get(m, {}).values():
            all_products.update(ent_data.keys())
    all_products = sorted(all_products)

    seen_entities = []
    seen_set = set()
    for m in month_list:
        for e in all_eo.get(m, []):
            if e not in seen_set:
                seen_entities.append(e); seen_set.add(e)

    cum_data = {}
    running_tar = {}; running_ach = {}

    for m in month_list:
        pe = all_prod_entity.get(m, {})
        cum_data[m] = {}
        for entity in seen_entities:
            entity_prod_data = pe.get(entity, {})
            if entity not in running_tar:
                running_tar[entity] = {}; running_ach[entity] = {}
            cum_data[m][entity] = {}
            for product in all_products:
                month_tar = entity_prod_data.get(product, {}).get('TAR', 0.0)
                month_ach = entity_prod_data.get(product, {}).get('ACH', 0.0)
                running_tar[entity][product] = running_tar[entity].get(product, 0.0) + month_tar
                running_ach[entity][product] = running_ach[entity].get(product, 0.0) + month_ach
                cum_t = running_tar[entity][product]
                cum_a = running_ach[entity][product]
                cum_data[m][entity][product] = dict(
                    CUM_TAR=cum_t, CUM_ACH=cum_a,
                    CUM_PCT=(cum_a/cum_t*100) if cum_t > 0 else 0.0,
                    MONTH_TAR=month_tar, MONTH_ACH=month_ach,
                )
    return cum_data, all_products, seen_entities

# ══════════════════════════════════════════════════════
# UI COMPONENTS
# ══════════════════════════════════════════════════════
def achievement_rows_ui(rows, fmt_fn=fmt_n):
    if not rows: st.info("No data."); return
    rows_s = sorted(rows, key=lambda x: x['PCT'], reverse=True)
    header = """<div style="display:flex;align-items:center;gap:12px;padding:6px 16px;
                             font-size:.68rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;">
        <div style="width:20px"></div>
        <div style="flex:1">Name</div>
        <div style="flex:2">Progress</div>
        <div style="width:90px;text-align:right">Target</div>
        <div style="width:90px;text-align:right">Achieved</div>
        <div style="width:58px;text-align:center">Ach %</div>
    </div>"""
    body = ""
    for i, r in enumerate(rows_s):
        p = r['PCT']; c = pct_color(p); bcl = pct_badge(p)
        bg = '#f0fdf4' if p >= 100 else '#fffbeb' if p >= 80 else '#fff'
        body += f"""
        <div class="ach-row" style="background:{bg}">
            <div class="ach-rank">#{i+1}</div>
            <div class="ach-name" title="{r['name']}">{r['name']}</div>
            <div class="ach-track">
                <div class="ach-fill" style="width:{min(p,100):.1f}%;background:{c};opacity:.85"></div>
            </div>
            <div class="ach-tar">{fmt_fn(r['TAR'])}</div>
            <div class="ach-ach" style="color:{c}">{fmt_fn(r['ACH'])}</div>
            <div class="ach-pct-badge {bcl}">{p:.1f}%</div>
        </div>"""
    st.markdown(header + body, unsafe_allow_html=True)


def _rp_rows_html(rp_list, data_ms, fmt_fn, color_accent):
    """Render individual RP rows inside a DM block."""
    if not rp_list:
        return '<div style="padding:10px 12px;font-size:.8rem;color:#94a3b8;font-style:italic">No sales reps under this DM.</div>'
    html = ""
    for rp in rp_list:
        rd  = data_ms.get(rp, {})
        t   = rd.get('TAR', rd.get('TAR_LKR', 0))
        a   = rd.get('ACH', rd.get('ACH_LKR', 0))
        v   = rd.get('VAR', rd.get('VAR_LKR', 0))
        p   = rd.get('PCT', rd.get('PCT_LKR', 0))
        c   = pct_color(p); b = pct_badge(p)
        vc  = "#059669" if v >= 0 else "#dc2626"
        bg  = "#f0fdf4" if p >= 100 else "#fffbeb" if p >= 80 else "#fff"
        html += f"""
        <div class="rp-row" style="background:{bg}">
            <div class="rp-badge">RP</div>
            <div class="rp-name" title="{rp}">{rp}</div>
            <div class="rp-track">
                <div class="rp-fill" style="width:{min(p,100):.1f}%;background:{c}"></div>
            </div>
            <div class="rp-tar">{fmt_fn(t)}</div>
            <div class="rp-ach" style="color:{c}">{fmt_fn(a)}</div>
            <div class="rp-pct {b}">{p:.1f}%</div>
        </div>"""
    return html


def render_full_hierarchy(hier, data_ms, fmt_fn=fmt_n, label="units"):
    """
    Render the full TOTAL → SBDM → DM → RP tree.
    hier = result from build_hierarchy()
    data_ms = units_ms or lkr_ms for the selected month
    """
    has_sbdm = hier["has_sbdm"]
    sbdm_nodes = hier["sbdm_nodes"]

    # ── TOTAL banner ─────────────────────────────────
    tot = data_ms.get("TOTAL", {})
    tt = tot.get("TAR", tot.get("TAR_LKR", 0))
    ta = tot.get("ACH", tot.get("ACH_LKR", 0))
    tv = tot.get("VAR", tot.get("VAR_LKR", 0))
    tp = tot.get("PCT", tot.get("PCT_LKR", 0))
    tc_col = pct_color(tp)
    st.markdown(f"""
    <div class="hier-total-block">
        <div class="hier-total-title">Division Total</div>
        <div class="hier-total-name">🏢 TOTAL</div>
        <div class="hier-total-kpis">
            <div><div class="hier-kpi-lbl">Target ({label})</div>
                 <div class="hier-kpi-val">{fmt_fn(tt)}</div></div>
            <div><div class="hier-kpi-lbl">Achievement ({label})</div>
                 <div class="hier-kpi-val" style="color:{tc_col}">{fmt_fn(ta)}</div></div>
            <div><div class="hier-kpi-lbl">Variance</div>
                 <div class="hier-kpi-val" style="color:{tc_col}">
                     {"+" if tv>=0 else ""}{fmt_fn(tv)}</div></div>
            <div><div class="hier-kpi-lbl">Ach %</div>
                 <div class="hier-kpi-val">
                     <span style="background:{'#dcfce7' if tp>=100 else '#fef3c7' if tp>=80 else '#fee2e2'};
                                  color:{'#15803d' if tp>=100 else '#92400e' if tp>=80 else '#b91c1c'};
                                  padding:3px 12px;border-radius:999px;font-size:.9rem">{tp:.1f}%</span>
                 </div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    for sbdm_node in sbdm_nodes:
        sbdm_name = sbdm_node["name"]
        dms       = sbdm_node["dms"]

        if has_sbdm and sbdm_name:
            # ── SBDM block ───────────────────────────────────────
            sd  = data_ms.get(sbdm_name, {})
            st_ = sd.get("TAR", sd.get("TAR_LKR", 0))
            sa  = sd.get("ACH", sd.get("ACH_LKR", 0))
            sv  = sd.get("VAR", sd.get("VAR_LKR", 0))
            sp  = sd.get("PCT", sd.get("PCT_LKR", 0))
            sc  = pct_color(sp); sb = pct_badge(sp)
            vc  = "#4ade80" if sv >= 0 else "#f87171"
            st.markdown(f"""
            <div class="sbdm-block">
              <div class="sbdm-header">
                <div>
                  <div class="sbdm-badge">SBDM</div>
                  <div class="sbdm-name">👤 {sbdm_name}</div>
                </div>
                <div class="sbdm-kpis">
                  <div><div class="sbdm-kpi-lbl">Target</div>
                       <div class="sbdm-kpi-val">{fmt_fn(st_)}</div></div>
                  <div><div class="sbdm-kpi-lbl">Achievement</div>
                       <div class="sbdm-kpi-val" style="color:{sc}">{fmt_fn(sa)}</div>
                       <span style="font-size:.72rem;font-weight:800;padding:2px 10px;border-radius:999px;
                                    background:{'rgba(34,197,94,.25)' if sp>=100 else 'rgba(245,158,11,.25)' if sp>=80 else 'rgba(239,68,68,.25)'};
                                    color:{'#4ade80' if sp>=100 else '#fbbf24' if sp>=80 else '#f87171'}">{sp:.1f}%</span>
                  </div>
                  <div><div class="sbdm-kpi-lbl">Variance</div>
                       <div class="sbdm-kpi-val" style="color:{vc}">{"+" if sv>=0 else ""}{fmt_fn(sv)}</div></div>
                </div>
              </div>
              <div class="sbdm-body">""", unsafe_allow_html=True)

            for dm_node in dms:
                _render_dm_node(dm_node, data_ms, fmt_fn, label)

            st.markdown('</div></div>', unsafe_allow_html=True)

        else:
            # ── No SBDM — render DMs directly ───────────────────
            for dm_node in dms:
                _render_dm_node(dm_node, data_ms, fmt_fn, label, standalone=True)


def _render_dm_node(dm_node, data_ms, fmt_fn, label, standalone=False):
    dm_name = dm_node["name"]
    rp_list = dm_node["rps"]

    dd  = data_ms.get(dm_name, {})
    dt  = dd.get("TAR", dd.get("TAR_LKR", 0))
    da  = dd.get("ACH", dd.get("ACH_LKR", 0))
    dv  = dd.get("VAR", dd.get("VAR_LKR", 0))
    dp  = dd.get("PCT", dd.get("PCT_LKR", 0))
    dc  = pct_color(dp); db = pct_badge(dp)
    vc  = "#4ade80" if dv >= 0 else "#f87171"

    rp_tar_sum = sum(data_ms.get(r,{}).get("TAR", data_ms.get(r,{}).get("TAR_LKR",0)) for r in rp_list)
    rp_ach_sum = sum(data_ms.get(r,{}).get("ACH", data_ms.get(r,{}).get("ACH_LKR",0)) for r in rp_list)
    rollup_pct = (rp_ach_sum / rp_tar_sum * 100) if rp_tar_sum else 0

    extra_class = "dm-standalone" if standalone else ""
    html = f"""
    <div class="dm-block {extra_class}">
      <div class="dm-header">
        <div>
          <div class="dm-badge">DM</div>
          <div class="dm-name">👤 {dm_name}</div>
        </div>
        <div class="dm-kpis">
          <div><div class="dm-kpi-lbl">Target ({label})</div>
               <div class="dm-kpi-val">{fmt_fn(dt)}</div></div>
          <div><div class="dm-kpi-lbl">Achievement</div>
               <div class="dm-kpi-val" style="color:{dc}">{fmt_fn(da)}</div>
               <span style="font-size:.68rem;font-weight:800;padding:2px 8px;border-radius:999px;margin-top:3px;display:inline-block;
                            background:{'rgba(34,197,94,.25)' if dp>=100 else 'rgba(245,158,11,.25)' if dp>=80 else 'rgba(239,68,68,.25)'};
                            color:{'#4ade80' if dp>=100 else '#fbbf24' if dp>=80 else '#f87171'}">{dp:.1f}%</span>
          </div>
          <div><div class="dm-kpi-lbl">Variance</div>
               <div class="dm-kpi-val" style="color:{vc}">{"+" if dv>=0 else ""}{fmt_fn(dv)}</div></div>
        </div>
      </div>
      <div class="dm-body">"""

    # RP column headers
    html += """
        <div style="display:flex;align-items:center;gap:10px;padding:4px 12px;
                    font-size:.62rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.07em;margin-bottom:4px;">
          <div style="width:32px"></div>
          <div style="flex:1">Sales Rep</div>
          <div style="flex:2">Progress</div>
          <div style="width:80px;text-align:right">Target</div>
          <div style="width:80px;text-align:right">Achievement</div>
          <div style="width:52px;text-align:center">Ach %</div>
        </div>"""

    html += _rp_rows_html(rp_list, data_ms, fmt_fn, dc)

    # Rollup footer
    match = "✓ DM = Σ RP" if abs(dt - rp_tar_sum) < 10 else f"⚠ DM {fmt_fn(dt)} ≠ Σ RP {fmt_fn(rp_tar_sum)}"
    html += f"""
      </div>
      <div class="rollup-bar">
        <div style="flex:1">∑ RP Rollup → {dm_name} &nbsp;
          <span style="font-size:.68rem;color:#0284c7">{match}</span></div>
        <div style="width:80px;text-align:right">{fmt_fn(rp_tar_sum)}</div>
        <div style="width:80px;text-align:right">{fmt_fn(rp_ach_sum)}</div>
        <div style="width:52px;text-align:center;color:#0369a1">{rollup_pct:.1f}%</div>
      </div>
    </div>"""
    st.markdown(html, unsafe_allow_html=True)


def donut_chart(label_vals, center_label, key, pal_offset=0):
    items = [(k, v) for k, v in label_vals.items() if v and v > 0]
    if not items: st.info("No data."); return
    labels, vals = zip(*items)
    colors = PALETTE[pal_offset:pal_offset+len(labels)]
    fig = go.Figure(go.Pie(
        labels=labels, values=vals, hole=.55,
        marker=dict(colors=colors, line=dict(color="#fff", width=2)),
        textinfo="percent+label", textfont=dict(size=11),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig.add_annotation(text=f"<b>{fmt_n(sum(vals))}</b>",
                       x=0.5, y=0.54, font=dict(size=14, color="#1e293b"), showarrow=False)
    fig.add_annotation(text=center_label,
                       x=0.5, y=0.42, font=dict(size=10, color="#94a3b8"), showarrow=False)
    fig.update_layout(**PLOTLY_BASE, height=320,
                      margin=dict(t=10,b=10,l=10,r=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=key)

# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding-bottom:10px">
        <h2>📊 Sales Intelligence Hub</h2>
        <p>Universal Sales Dashboard</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<span style="font-weight:bold">📂 Upload Excel Files</span>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload one or more Excel files", type=["xlsx","xls"], accept_multiple_files=True)
    st.markdown("---")

    if uploaded_files:
        file_names = [f.name for f in uploaded_files]
        selected_file_name = st.selectbox("📁 Select File", file_names) if len(file_names)>1 else file_names[0]
        uploaded_file = next(f for f in uploaded_files if f.name == selected_file_name)
        dash_title = selected_file_name.rsplit('.',1)[0].replace('_',' ').replace('-',' ').upper()

        with st.spinner("Parsing Excel…"):
            (all_lkr, all_units, all_hierarchy,
             all_eo, all_prod, all_prod_entity) = parse_excel(uploaded_file)

        month_list = [m for m in MONTH_ORDER if m in all_lkr]
        if not month_list:
            st.error("No valid data sheets found."); st.stop()

        sel_month = st.selectbox("📅 Month", month_list)
        lkr_ms    = all_lkr[sel_month]
        units_ms  = all_units[sel_month]
        hier      = all_hierarchy[sel_month]
        eo        = all_eo[sel_month]
        prd       = all_prod.get(sel_month, pd.DataFrame())

        has_sbdm  = hier["has_sbdm"]
        all_dms   = hier["all_dms"]
        all_sbdms = [e for e in eo if is_sbdm(e)]

        total_lkr     = lkr_ms.get('TOTAL', {})
        total_tar_lkr = total_lkr.get('TAR_LKR', 0)
        total_ach_lkr = total_lkr.get('ACH_LKR', 0)
        total_var_lkr = total_lkr.get('VAR_LKR', 0)
        total_pct_lkr = total_lkr.get('PCT_LKR', 0)

        total_units = units_ms.get('TOTAL', {})
        total_tar_u = total_units.get('TAR', 0)
        total_ach_u = total_units.get('ACH', 0)
        total_pct_u = total_units.get('PCT', 0)

        p_col  = "#4ade80" if total_pct_lkr>=100 else "#fbbf24" if total_pct_lkr>=80 else "#f87171"
        pu_col = "#4ade80" if total_pct_u>=100   else "#fbbf24" if total_pct_u>=80   else "#f87171"

        st.markdown("---")
        st.markdown('<span style="font-weight:bold">📌 Quick Stats</span>', unsafe_allow_html=True)
        hier_label = "TOTAL → SBDM → DM → RP" if has_sbdm else "TOTAL → DM → RP"
        st.markdown(f"""
        <div>Hierarchy: <strong>{hier_label}</strong></div>
        <div>SBDM count: {len(all_sbdms)}</div>
        <div>DM count: {len(all_dms)}</div>
        <div>Target (LKR): {fmt_lkr(total_tar_lkr)}</div>
        <div>Achievement (LKR): {fmt_lkr(total_ach_lkr)}</div>
        <div style="color:{p_col}">LKR Ach %: {total_pct_lkr:.1f}%</div>
        <div>Months loaded: {len(month_list)}</div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        # Filter: SBDM or DM
        filter_opts = ["ALL"]
        if has_sbdm: filter_opts += [f"SBDM: {s}" for s in all_sbdms]
        filter_opts += [f"DM: {d}" for d in all_dms]
        hier_filter = st.selectbox("🔍 Filter", filter_opts)

        cum_data, all_products, all_entities = build_cumulative_data(
            month_list, all_prod_entity, all_eo)
    else:
        st.info("Upload an Excel file to begin.")
        dash_title = "Sales Intelligence Hub"

    st.markdown("---")
    st.markdown("<small style='color:#334155;font-size:.68rem'>Universal Sales Hub · v13.0</small>",
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════
if not uploaded_files:
    st.markdown("""
    <div class="landing">
        <div class="landing-logo">📊</div>
        <h2>Universal Sales Intelligence Hub</h2>
        <p>Upload any Excel file in the standard sales format to instantly see the full
        <strong>TOTAL → SBDM → DM → RP</strong> hierarchy with targets and achievements.</p>
        <div class="landing-card">
            <h4>✅ Hierarchy Detection Rules</h4>
            <ul>
                <li><code>TOTAL</code> — Division grand total (always present)</li>
                <li><code>SBDM</code> in name → Senior BDM layer (optional)</li>
                <li><code>(DM)</code> in name → District Manager</li>
                <li>All others → Sales Reps (RP)</li>
                <li>Order in Excel determines who reports to whom</li>
            </ul>
        </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════
v_sign = "▲" if total_var_lkr >= 0 else "▼"
v_col  = "#4ade80" if total_var_lkr >= 0 else "#f87171"
hier_label = "TOTAL → SBDM → DM → RP" if has_sbdm else "TOTAL → DM → RP"
st.markdown(f"""
<div class="page-header">
    <div>
        <h1>📊 {dash_title} — Sales Performance</h1>
        <p style="color:#93c5fd;font-size:.8rem;margin:4px 0 0">Hierarchy: {hier_label}</p>
    </div>
    <div class="hdr-chips">
        <span class="hdr-chip live">● LIVE</span>
        <span class="hdr-chip month">📅 {sel_month}</span>
        <span class="hdr-chip month" style="color:{v_col}">
            {v_sign} {fmt_lkr(abs(total_var_lkr))} variance
        </span>
    </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
tab_hier, tab2, tab1, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🌲 Hierarchy",
    "📅 All Months",
    "📆 Overview",
    "👥 DM Breakdown",
    "🏢 RP / Rep Detail",
    "📦 Products",
    "📈 LKR Trend",
    "📊 Cumulative",
])

# ╔══════════════════════════════════════════╗
# ║  TAB — HIERARCHY (NEW — main feature)   ║
# ╚══════════════════════════════════════════╝
with tab_hier:
    hier_month = st.selectbox("Select Month", month_list,
                               index=month_list.index(sel_month), key="hier_month")
    h_lkr_ms   = all_lkr[hier_month]
    h_units_ms = all_units[hier_month]
    h_hier     = all_hierarchy[hier_month]

    view_mode = st.radio("View in", ["Units", "LKR"], horizontal=True, key="hier_view")
    data_ms_h  = h_units_ms if view_mode == "Units" else h_lkr_ms
    fmt_fn_h   = fmt_n if view_mode == "Units" else fmt_lkr
    label_h    = "units" if view_mode == "Units" else "LKR"

    section(f"FULL HIERARCHY — {hier_month} ({view_mode})")

    # Apply filter
    f = hier_filter
    if f == "ALL":
        render_full_hierarchy(h_hier, data_ms_h, fmt_fn_h, label_h)
    else:
        # Filter to just the selected SBDM or DM subtree
        filtered_nodes = []
        for sn in h_hier["sbdm_nodes"]:
            if f.startswith("SBDM: ") and sn["name"] == f[6:]:
                filtered_nodes.append(sn)
            elif f.startswith("DM: "):
                dm_target = f[4:]
                for dm_node in sn["dms"]:
                    if dm_node["name"] == dm_target:
                        filtered_nodes.append({"name": sn["name"] if h_hier["has_sbdm"] else None,
                                                "dms": [dm_node]})

        # Build a mini hierarchy for the filtered view
        mini_hier = dict(h_hier)
        mini_hier["sbdm_nodes"] = filtered_nodes
        if filtered_nodes:
            render_full_hierarchy(mini_hier, data_ms_h, fmt_fn_h, label_h)
        else:
            st.info("No data for selected filter.")

# ╔══════════════════════════════╗
# ║  TAB — OVERVIEW             ║
# ╚══════════════════════════════╝
with tab1:
    ov_month    = st.selectbox("Select Month", month_list,
                                index=month_list.index(sel_month), key="overview_month")
    ov_lkr_ms   = all_lkr[ov_month]
    ov_units_ms = all_units[ov_month]
    ov_hier     = all_hierarchy[ov_month]
    ov_eo       = all_eo[ov_month]
    ov_dm_keys  = ov_hier["all_dms"]

    ov_tot_lkr = ov_lkr_ms.get('TOTAL', {})
    ov_tar_lkr = ov_tot_lkr.get('TAR_LKR', 0)
    ov_ach_lkr = ov_tot_lkr.get('ACH_LKR', 0)
    ov_var_lkr = ov_tot_lkr.get('VAR_LKR', 0)
    ov_pct_lkr = ov_tot_lkr.get('PCT_LKR', 0)

    section("LKR PERFORMANCE")
    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1,"Total Target (LKR)",fmt_lkr(ov_tar_lkr),"🎯","c-blue",sub=f"{ov_month}")
    kpi_card(c2,"Total Achievement (LKR)",fmt_lkr(ov_ach_lkr),"💰","c-green",
             badge_text=f"{'▲' if ov_var_lkr>=0 else '▼'} {fmt_lkr(abs(ov_var_lkr))}",
             badge_cls=pct_cls(ov_pct_lkr))
    kpi_card(c3,"LKR Achievement %",f"{ov_pct_lkr:.1f}%","📈",
             "c-green" if ov_pct_lkr>=100 else "c-amber",
             badge_text="On Track" if ov_pct_lkr>=100 else "Below Target",
             badge_cls=pct_cls(ov_pct_lkr))
    kpi_card(c4,"LKR Variance",fmt_lkr(abs(ov_var_lkr)),
             "📊" if ov_var_lkr>=0 else "📉",
             "c-teal" if ov_var_lkr>=0 else "c-red",
             badge_text="▲ Surplus" if ov_var_lkr>=0 else "▼ Shortfall",
             badge_cls="up" if ov_var_lkr>=0 else "down")

    top_ents = [e for e in ov_eo if e!='TOTAL' and ov_lkr_ms.get(e,{}).get('TAR_LKR',0)>0]
    if top_ents:
        non_total = [(e, ov_lkr_ms[e]) for e in top_ents]
        best = max(non_total, key=lambda x: x[1]['PCT_LKR'])
        role_lbl = get_role(best[0])
        st.markdown(f"""<div style="display:flex;gap:12px;margin-bottom:1.5rem;flex-wrap:wrap">
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:10px 16px;
                        font-size:.78rem;color:#475569;display:flex;align-items:center;gap:8px">
                <div style="width:8px;height:8px;border-radius:50%;background:#22c55e;flex-shrink:0"></div>
                Best entity: <strong>{best[0]}</strong>
                <span style="background:#e0f2fe;color:#0369a1;font-size:.65rem;font-weight:700;
                             padding:1px 7px;border-radius:999px">{role_lbl}</span>
                at <strong>{best[1]['PCT_LKR']:.1f}%</strong>
            </div></div>""", unsafe_allow_html=True)

    section("LKR: TARGET vs ACHIEVEMENT BY ENTITY")
    col_bar, col_pie = st.columns([3, 2])
    with col_bar:
        st.markdown('<div class="card"><div class="card-title">LKR TAR vs ACH — All Entities</div>',
                    unsafe_allow_html=True)
        if top_ents:
            tars  = [ov_lkr_ms[e]['TAR_LKR'] for e in top_ents]
            achs  = [ov_lkr_ms[e]['ACH_LKR'] for e in top_ents]
            pcts  = [ov_lkr_ms[e]['PCT_LKR'] for e in top_ents]
            roles = [get_role(e) for e in top_ents]
            short = [n[:13]+"…" if len(n)>13 else n for n in top_ents]
            # Color by role
            role_colors = {"SBDM":"#8b5cf6","DM":"#3b82f6","RP":"#94a3b8"}
            bar_colors = [role_colors.get(r,"#94a3b8") for r in roles]
            fig_b = go.Figure()
            fig_b.add_trace(go.Bar(name="Target", x=top_ents, y=tars,
                marker=dict(color="#93c5fd",line=dict(width=0)), width=0.35, offset=-0.2))
            fig_b.add_trace(go.Bar(name="Achievement", x=top_ents, y=achs,
                marker=dict(color=[pct_color(p) for p in pcts], opacity=0.9, line=dict(width=0)),
                width=0.35, offset=0.05,
                text=[f"{p:.1f}%" for p in pcts], textposition="outside",
                textfont=dict(size=10, color="#475569")))
            fig_b.update_layout(**PLOTLY_BASE, barmode="overlay", height=360,
                margin=dict(t=30,b=100,l=80,r=20), bargap=0.25,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(tickangle=-40,tickfont=dict(size=10,color="#64748b"),showgrid=False,
                           tickmode="array",tickvals=list(range(len(top_ents))),ticktext=short),
                yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),title="LKR"))
            st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pie:
        st.markdown('<div class="card"><div class="card-title">DM Achievement Share (LKR)</div>',
                    unsafe_allow_html=True)
        donut_chart(
            {k: ov_lkr_ms.get(k,{}).get('ACH_LKR',0) for k in ov_dm_keys
             if ov_lkr_ms.get(k,{}).get('ACH_LKR',0)>0},
            "DM ACH LKR", key=f"dm_donut_{ov_month}")
        st.markdown('</div>', unsafe_allow_html=True)

    section("ACHIEVEMENT % RANKING (LKR)")
    col_rank, col_sc = st.columns([3, 2])
    with col_rank:
        # Show by role group
        for role_name, role_fn, role_icon in [
            ("SBDM", is_sbdm, "🟣"), ("DM", is_dm, "🔵"), ("RP", is_rp, "⚫")
        ]:
            role_ents = [e for e in top_ents if role_fn(e)]
            if not role_ents: continue
            st.markdown(f"**{role_icon} {role_name} Level**")
            achievement_rows_ui(
                [dict(name=e, TAR=ov_lkr_ms[e]['TAR_LKR'],
                      ACH=ov_lkr_ms[e]['ACH_LKR'], PCT=ov_lkr_ms[e]['PCT_LKR'])
                 for e in role_ents], fmt_fn=fmt_lkr)
            st.markdown("<br>", unsafe_allow_html=True)

    with col_sc:
        st.markdown('<div class="card"><div class="card-title">TAR vs ACH Scatter (LKR)</div></div>',
                    unsafe_allow_html=True)
        sc_rows = [dict(Entity=e, TAR=ov_lkr_ms[e]['TAR_LKR'],
                        ACH=ov_lkr_ms[e]['ACH_LKR'], PCT=ov_lkr_ms[e]['PCT_LKR'],
                        Role=get_role(e))
                   for e in top_ents]
        if sc_rows:
            sc_df = pd.DataFrame(sc_rows)
            fig_sc = px.scatter(sc_df, x="TAR", y="ACH", color="Role", size="PCT",
                hover_name="Entity",
                color_discrete_map={"SBDM":"#8b5cf6","DM":"#3b82f6","RP":"#64748b"},
                size_max=26)
            mx = max(sc_df["TAR"].max(), sc_df["ACH"].max()) * 1.1
            fig_sc.add_shape(type="line",x0=0,y0=0,x1=mx,y1=mx,
                             line=dict(color="#94a3b8",dash="dot",width=1.5))
            fig_sc.update_layout(**PLOTLY_BASE, height=320,
                margin=dict(t=10,b=50,l=70,r=10),
                legend=dict(font=dict(size=11),bgcolor="rgba(0,0,0,0)",
                            orientation="h",yanchor="bottom",y=1.01,xanchor="right",x=1),
                xaxis=dict(gridcolor="#f1f5f9",tickfont=dict(color="#94a3b8",size=10),title="Target (LKR)"),
                yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(color="#94a3b8",size=10),title="Achievement (LKR)"))
            st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})

    section("ENTITY SUMMARY TABLE")
    tbl_rows = []
    for e in ov_eo:
        lkr_d  = ov_lkr_ms.get(e, {})
        unit_d = ov_units_ms.get(e, {})
        tbl_rows.append({
            "Entity":e, "Role":get_role(e),
            "Target LKR":round(lkr_d.get("TAR_LKR",0)),
            "Achievement LKR":round(lkr_d.get("ACH_LKR",0)),
            "LKR Ach %":round(lkr_d.get("PCT_LKR",0),1),
            "LKR Variance":round(lkr_d.get("VAR_LKR",0)),
            "Target Units":round(unit_d.get("TAR",0)),
            "Achievement Units":round(unit_d.get("ACH",0)),
            "Unit Ach %":round(unit_d.get("PCT",0),1),
        })
    tbl_df = pd.DataFrame(tbl_rows)
    num_cols = ["Target LKR","Achievement LKR","LKR Variance","Target Units","Achievement Units"]
    tbl_df = tbl_df[~(tbl_df[num_cols]==0).all(axis=1)]
    st.dataframe(
        tbl_df.style
        .format({"Target LKR":"{:,.0f}","Achievement LKR":"{:,.0f}","LKR Ach %":"{:.1f}%",
                 "LKR Variance":"{:+,.0f}","Target Units":"{:,.0f}",
                 "Achievement Units":"{:,.0f}","Unit Ach %":"{:.1f}%"})
        .map(lambda v:("color:#059669;font-weight:700" if v>=0 else "color:#dc2626;font-weight:700")
             if isinstance(v,(int,float)) else "", subset=["LKR Variance"])
        .map(lambda v:("color:#059669;font-weight:700" if v>=100 else
                       "color:#d97706;font-weight:700" if v>=80 else "color:#dc2626;font-weight:700")
             if isinstance(v,(int,float)) else "", subset=["LKR Ach %","Unit Ach %"]),
        use_container_width=True, hide_index=True, height=min(520,len(tbl_df)*42+60))
    dl1,_ = st.columns([1,5])
    with dl1:
        st.download_button("⬇️ Export CSV", data=tbl_df.to_csv(index=False).encode("utf-8"),
            file_name=f"{dash_title}_{ov_month}.csv", mime="text/csv", use_container_width=True)

# ╔══════════════════════════════╗
# ║  TAB — ALL MONTHS           ║
# ╚══════════════════════════════╝
with tab2:
    summary_rows = []
    for m in month_list:
        lkr_m  = all_lkr[m]
        unit_m = all_units[m]
        h_m    = all_hierarchy[m]
        tot_l  = lkr_m.get('TOTAL', {})
        tot_u  = unit_m.get('TOTAL', {})
        summary_rows.append({
            "Month":m,
            "Target (LKR)":tot_l.get("TAR_LKR",0),
            "Achievement (LKR)":tot_l.get("ACH_LKR",0),
            "LKR Ach %":tot_l.get("PCT_LKR",0),
            "LKR Variance":tot_l.get("VAR_LKR",0),
            "Target (units)":tot_u.get("TAR",0),
            "Achievement (units)":tot_u.get("ACH",0),
            "Unit Ach %":tot_u.get("PCT",0),
            "# DMs":len(h_m["all_dms"]),
            "SBDM":("Yes" if h_m["has_sbdm"] else "No"),
        })
    sum_df = pd.DataFrame(summary_rows)

    section("OVERALL — ALL MONTHS")
    g1,g2,g3,g4 = st.columns(4)
    grand_tar = sum_df["Target (LKR)"].sum()
    grand_ach = sum_df["Achievement (LKR)"].sum()
    grand_pct = (grand_ach/grand_tar*100) if grand_tar else 0
    grand_var = grand_ach - grand_tar
    kpi_card(g1,"Grand Total Target (LKR)",fmt_lkr(grand_tar),"🎯","c-blue",sub=f"{len(sum_df)} months")
    kpi_card(g2,"Grand Total Achievement (LKR)",fmt_lkr(grand_ach),"💰","c-green",
             badge_text=f"{'▲' if grand_var>=0 else '▼'} {fmt_lkr(abs(grand_var))}",
             badge_cls="up" if grand_var>=0 else "down")
    kpi_card(g3,"Overall LKR Ach %",f"{grand_pct:.1f}%","📈",
             "c-green" if grand_pct>=100 else "c-amber", badge_cls=pct_cls(grand_pct))
    kpi_card(g4,"LKR Variance (total)",fmt_lkr(abs(grand_var)),
             "📊" if grand_var>=0 else "📉","c-teal" if grand_var>=0 else "c-red",
             badge_text="▲ Surplus" if grand_var>=0 else "▼ Shortfall",
             badge_cls="up" if grand_var>=0 else "down")

    section("MONTHLY TREND")
    cl1, cl2 = st.columns([3, 2])
    with cl1:
        fig_tr = go.Figure()
        fig_tr.add_trace(go.Bar(name="Target", x=sum_df["Month"], y=sum_df["Target (LKR)"],
            marker=dict(color="#93c5fd",opacity=0.9,line=dict(width=0))))
        fig_tr.add_trace(go.Bar(name="Achievement", x=sum_df["Month"], y=sum_df["Achievement (LKR)"],
            marker=dict(color=[pct_color(p) for p in sum_df["LKR Ach %"]],opacity=0.9,line=dict(width=0)),
            text=[f"{p:.1f}%" for p in sum_df["LKR Ach %"]],
            textposition="outside", textfont=dict(size=11)))
        fig_tr.add_trace(go.Scatter(name="Ach %", x=sum_df["Month"], y=sum_df["LKR Ach %"],
            mode="lines+markers", yaxis="y2",
            line=dict(color="#f59e0b",width=2,dash="dot"),
            marker=dict(size=7,color="#f59e0b",line=dict(color="#fff",width=1.5))))
        fig_tr.update_layout(**PLOTLY_BASE, barmode="group", height=340,
            margin=dict(t=20,b=60,l=80,r=60),
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
            yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),title="LKR"),
            yaxis2=dict(overlaying="y",side="right",showgrid=False,
                        tickfont=dict(size=10,color="#f59e0b"),ticksuffix="%"))
        st.plotly_chart(fig_tr, use_container_width=True, config={"displayModeBar": False})

    with cl2:
        donut_chart({r["Month"]:r["Achievement (LKR)"] for r in summary_rows
                     if r["Achievement (LKR)"]>0}, "All Months", key="all_months_pie")

    section("MONTH SUMMARY TABLE")
    st.dataframe(
        sum_df.style
        .format({"Target (LKR)":"LKR {:,.0f}","Achievement (LKR)":"LKR {:,.0f}",
                 "LKR Ach %":"{:.1f}%","LKR Variance":"LKR {:+,.0f}",
                 "Target (units)":"{:,.0f}","Achievement (units)":"{:,.0f}","Unit Ach %":"{:.1f}%"})
        .map(lambda v:("color:#16a34a;font-weight:700" if v>=100 else
                       "color:#d97706;font-weight:700" if v>=80 else "color:#dc2626;font-weight:700")
             if isinstance(v,(int,float)) else "", subset=["LKR Ach %","Unit Ach %"]),
        use_container_width=True, hide_index=True, height=min(500,len(sum_df)*44+60))

# ╔══════════════════════════════╗
# ║  TAB — DM BREAKDOWN         ║
# ╚══════════════════════════════╝
with tab3:
    dm_sel_month = st.selectbox("Select Month", month_list,
        index=month_list.index(sel_month), key="dm_month")
    dm_lkr_ms = all_lkr[dm_sel_month]
    dm_hier   = all_hierarchy[dm_sel_month]
    dm_eo     = all_eo[dm_sel_month]
    dm_keys   = dm_hier["all_dms"]

    section(f"DM PERFORMANCE CARDS — {dm_sel_month}")
    if dm_keys:
        dm_cols = st.columns(max(len(dm_keys),1))
        for i, dm_name in enumerate(dm_keys):
            dm_d = dm_lkr_ms.get(dm_name,{}); dm_t=dm_d.get("TAR_LKR",0)
            dm_a=dm_d.get("ACH_LKR",0); dm_p=dm_d.get("PCT_LKR",0); dm_v=dm_d.get("VAR_LKR",0)
            bc=pct_color(dm_p); bbg="#d1fae5" if dm_p>=100 else "#fef3c7" if dm_p>=80 else "#fee2e2"
            bfg="#065f46" if dm_p>=100 else "#92400e" if dm_p>=80 else "#991b1b"
            mw=max(dm_t,dm_a,1)
            dm_cols[i].markdown(f"""
            <div style="background:#fff;border:1px solid #e8edf5;border-radius:14px;
                        padding:1.1rem 1.2rem;box-shadow:0 2px 8px rgba(0,0,0,0.05);
                        border-top:3px solid {bc}">
              <div style="font-size:.62rem;font-weight:700;color:#8b5cf6;text-transform:uppercase;
                          letter-spacing:.1em;margin-bottom:2px">
                {"SBDM: "+[sn["name"] for sn in dm_hier["sbdm_nodes"] for d in sn["dms"] if d["name"]==dm_name and sn["name"]][0]
                 if any(sn["name"] and d["name"]==dm_name for sn in dm_hier["sbdm_nodes"] for d in sn["dms"]) else ""}
              </div>
              <div style="font-size:.72rem;font-weight:700;color:#64748b;overflow:hidden;
                          text-overflow:ellipsis;white-space:nowrap;margin-bottom:6px" title="{dm_name}">
                👤 {dm_name}</div>
              <div style="font-size:.78rem;color:#1e293b;font-weight:600">Target LKR</div>
              <div style="font-size:1rem;font-weight:700;color:#1e293b">{fmt_lkr(dm_t)}</div>
              <div style="background:#f1f5f9;border-radius:999px;height:6px;margin:.5rem 0">
                <div style="width:{(dm_t/mw*100):.1f}%;height:100%;background:#3b82f6;border-radius:999px"></div>
              </div>
              <div style="font-size:.78rem;color:#1e293b;font-weight:600">Achievement LKR</div>
              <div style="font-size:1rem;font-weight:700;color:{bc}">{fmt_lkr(dm_a)}</div>
              <div style="background:#f1f5f9;border-radius:999px;height:6px;margin:.5rem 0">
                <div style="width:{(dm_a/mw*100):.1f}%;height:100%;background:{bc};border-radius:999px"></div>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div style="font-size:.7rem;font-weight:600;color:{'#059669' if dm_v>=0 else '#dc2626'}">
                  {"+" if dm_v>=0 else ""}{fmt_lkr(dm_v)}</div>
                <span style="font-size:.72rem;font-weight:700;padding:2px 10px;border-radius:999px;
                             background:{bbg};color:{bfg}">{dm_p:.1f}%</span>
              </div>
            </div>""", unsafe_allow_html=True)

    section(f"DM ACHIEVEMENT RANKING (LKR) — {dm_sel_month}")
    achievement_rows_ui(
        [dict(name=e,TAR=dm_lkr_ms[e]['TAR_LKR'],ACH=dm_lkr_ms[e]['ACH_LKR'],PCT=dm_lkr_ms[e]['PCT_LKR'])
         for e in dm_keys if dm_lkr_ms.get(e,{}).get('TAR_LKR',0)>0],
        fmt_fn=fmt_lkr)

    # DM trend chart
    dm_trend = []
    for m in month_list:
        for e in all_eo[m]:
            if not is_dm(e): continue
            d = all_lkr[m].get(e,{})
            if not d.get('TAR_LKR'): continue
            dm_trend.append(dict(Month=m,DM=e,TAR=d['TAR_LKR'],ACH=d['ACH_LKR'],PCT=d['PCT_LKR']))
    if dm_trend:
        section("DM TREND")
        dt_df = pd.DataFrame(dm_trend)
        fig_dml = px.line(dt_df,x="Month",y="ACH",color="DM",markers=True,
            color_discrete_sequence=PALETTE,labels={"ACH":"Achievement (LKR)"})
        fig_dml.update_layout(**PLOTLY_BASE,height=320,margin=dict(t=10,b=40,l=80,r=20),
            legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.05,xanchor="right",x=1),
            xaxis=dict(tickfont=dict(size=10.5,color="#64748b"),showgrid=False),
            yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=9.5,color="#94a3b8"),title="LKR"))
        st.plotly_chart(fig_dml,use_container_width=True,config={"displayModeBar":False})

# ╔══════════════════════════════╗
# ║  TAB — RP / REP DETAIL      ║
# ╚══════════════════════════════╝
with tab4:
    rp_sel_month = st.selectbox("Select Month", month_list,
        index=month_list.index(sel_month), key="rp_month")
    rp_lkr_ms   = all_lkr[rp_sel_month]
    rp_units_ms = all_units[rp_sel_month]
    rp_hier     = all_hierarchy[rp_sel_month]
    rp_eo       = all_eo[rp_sel_month]

    # Build RP→DM map from hierarchy
    rp_to_dm = {}
    for sn in rp_hier["sbdm_nodes"]:
        for dm_node in sn["dms"]:
            for rp in dm_node["rps"]:
                rp_to_dm[rp] = dm_node["name"]

    all_reps  = [e for e in rp_eo if is_rp(e) and e!='TOTAL']
    disp_reps = all_reps if hier_filter=="ALL" else [
        r for r in all_reps
        if (hier_filter.startswith("DM: ") and rp_to_dm.get(r)==hier_filter[4:])
        or (hier_filter.startswith("SBDM: ") and any(
            sn["name"]==hier_filter[6:] and any(d["name"]==rp_to_dm.get(r) for d in sn["dms"])
            for sn in rp_hier["sbdm_nodes"]))
    ]
    disp_reps = [r for r in disp_reps
                 if (rp_lkr_ms.get(r,{}).get("TAR_LKR",0)!=0 or
                     rp_lkr_ms.get(r,{}).get("ACH_LKR",0)!=0)]

    section(f"SALES REP PERFORMANCE — {rp_sel_month}")
    if not disp_reps:
        st.info("No rep data for current filter.")
    else:
        groups = {}
        for rp in disp_reps:
            groups.setdefault(rp_to_dm.get(rp,"Standalone"),[]).append(rp)

        for owner, rps in groups.items():
            dm_d=rp_lkr_ms.get(owner,{}); dm_t=dm_d.get("TAR_LKR",0)
            dm_a=dm_d.get("ACH_LKR",0); dm_p=dm_d.get("PCT_LKR",0); dm_v=dm_d.get("VAR_LKR",0)
            bc=pct_color(dm_p); bbg="#d1fae5" if dm_p>=100 else "#fef3c7" if dm_p>=80 else "#fee2e2"
            bfg="#065f46" if dm_p>=100 else "#92400e" if dm_p>=80 else "#991b1b"

            rp_rows = [dict(name=r,TAR=rp_lkr_ms.get(r,{}).get('TAR_LKR',0),
                            ACH=rp_lkr_ms.get(r,{}).get('ACH_LKR',0),
                            PCT=rp_lkr_ms.get(r,{}).get('PCT_LKR',0),
                            VAR=rp_lkr_ms.get(r,{}).get('VAR_LKR',0))
                       for r in rps if rp_lkr_ms.get(r,{}).get('TAR_LKR',0)>0]
            rp_rows_s = sorted(rp_rows, key=lambda x:x['PCT'], reverse=True)

            html = f"""
            <div style="border:1px solid #e2e8f0;border-radius:16px;overflow:hidden;
                        box-shadow:0 3px 14px rgba(0,0,0,0.07);margin-bottom:1.8rem">
              <div style="background:linear-gradient(135deg,#0a1628,#0d2045,#163870);
                          padding:1.1rem 1.4rem;border-left:5px solid {bc}">
                <div style="font-size:.62rem;font-weight:700;color:rgba(255,255,255,.4);
                            text-transform:uppercase;letter-spacing:.12em;margin-bottom:3px">District Manager</div>
                <div style="font-size:1rem;font-weight:800;color:#f0f6ff">👤 {owner}</div>
                <div style="display:flex;gap:24px;margin-top:10px;flex-wrap:wrap">
                  <div><div style="font-size:.6rem;color:rgba(255,255,255,.4);text-transform:uppercase">Target</div>
                       <div style="font-size:.9rem;font-weight:700;color:#cbd5e1">{fmt_lkr(dm_t)}</div></div>
                  <div><div style="font-size:.6rem;color:rgba(255,255,255,.4);text-transform:uppercase">Achievement</div>
                       <div style="font-size:.9rem;font-weight:700;color:{bc}">{fmt_lkr(dm_a)}</div></div>
                  <div><div style="font-size:.6rem;color:rgba(255,255,255,.4);text-transform:uppercase">Variance</div>
                       <div style="font-size:.9rem;font-weight:700;color:{bc}">{"+" if dm_v>=0 else ""}{fmt_lkr(dm_v)}</div></div>
                  <div style="display:flex;align-items:flex-end">
                    <span style="font-size:.85rem;font-weight:800;padding:3px 12px;border-radius:8px;
                                 background:{bbg};color:{bfg}">{dm_p:.1f}%</span>
                  </div>
                </div>
              </div>"""

            for i, r in enumerate(rp_rows_s):
                p=r['PCT']; c=pct_color(p); var=r['VAR']
                vc2="#059669" if var>=0 else "#dc2626"
                bg="#f0fdf4" if p>=100 else "#fffbeb" if p>=80 else "#fff"
                pbg="#d1fae5" if p>=100 else "#fef3c7" if p>=80 else "#fee2e2"
                pfg="#065f46" if p>=100 else "#92400e" if p>=80 else "#991b1b"
                html += f"""
              <div style="display:flex;align-items:center;padding:11px 14px;background:{bg};
                          border-bottom:1px solid #f1f5f9;gap:12px">
                <div style="width:24px;font-size:.68rem;font-weight:700;color:#94a3b8">#{i+1}</div>
                <div style="flex:2;font-size:.85rem;font-weight:600;color:#1e293b;
                            overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{r['name']}</div>
                <div style="flex:1.5;background:#e8edf5;border-radius:999px;height:8px;overflow:hidden">
                  <div style="width:{min(p,100):.1f}%;height:100%;background:{c};border-radius:999px;opacity:.85"></div>
                </div>
                <div style="width:120px;text-align:right;font-size:.82rem;font-weight:700;color:#334155">{fmt_lkr(int(r['TAR']))}</div>
                <div style="width:120px;text-align:right;font-size:.82rem;font-weight:800;color:{c}">{fmt_lkr(int(r['ACH']))}</div>
                <div style="width:90px;text-align:right;font-size:.78rem;font-weight:700;color:{vc2}">{"+" if var>=0 else ""}{fmt_lkr(int(var))}</div>
                <div style="width:60px;text-align:center">
                  <span style="font-size:.72rem;font-weight:800;padding:3px 8px;border-radius:7px;
                               background:{pbg};color:{pfg}">{p:.1f}%</span>
                </div>
              </div>"""
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

        section("REP RANKING (LKR)")
        achievement_rows_ui(
            [dict(name=r,TAR=rp_lkr_ms.get(r,{}).get('TAR_LKR',0),
                  ACH=rp_lkr_ms.get(r,{}).get('ACH_LKR',0),
                  PCT=rp_lkr_ms.get(r,{}).get('PCT_LKR',0))
             for r in disp_reps if rp_lkr_ms.get(r,{}).get('TAR_LKR',0)>0],
            fmt_fn=fmt_lkr)

# ╔══════════════════════════════╗
# ║  TAB — PRODUCTS             ║
# ╚══════════════════════════════╝
with tab5:
    section(f"PRODUCT BREAKDOWN — {sel_month}")
    if prd.empty:
        st.info("No product data.")
    else:
        ent_opts = ["ALL"] + sorted(prd["ENTITY"].unique().tolist())
        sel_ent  = st.selectbox("Filter by Entity", ent_opts, key="prod_ent")
        prd_f    = prd if sel_ent=="ALL" else prd[prd["ENTITY"]==sel_ent]
        prd_f    = prd_f[prd_f["TAR"]>0].copy()

        if not prd_f.empty:
            prod_sum = prd_f.groupby("PRODUCT").agg(TAR=("TAR","sum"),ACH=("ACH","sum")).reset_index()
            prod_sum["PCT"] = prod_sum.apply(lambda r:r["ACH"]/r["TAR"]*100 if r["TAR"]>0 else 0,axis=1)
            prod_sum = prod_sum.sort_values("TAR",ascending=False)

            p1,p2,p3,p4 = st.columns(4)
            kpi_card(p1,"Products",str(prod_sum["PRODUCT"].nunique()),"📦","c-blue")
            kpi_card(p2,"Total Unit Target",fmt_n(prod_sum["TAR"].sum()),"🎯","c-indigo")
            kpi_card(p3,"Total Unit Achievement",fmt_n(prod_sum["ACH"].sum()),"✅","c-green")
            best_p = prod_sum.loc[prod_sum["PCT"].idxmax(),"PRODUCT"]
            kpi_card(p4,"Best Product",best_p,"🏆","c-amber",
                     badge_text=f"{prod_sum['PCT'].max():.1f}%",badge_cls="up")

            st.markdown("<br>",unsafe_allow_html=True)
            cp1,cp2 = st.columns(2)
            with cp1:
                fig_pb = go.Figure()
                fig_pb.add_trace(go.Bar(name="Target",x=prod_sum["PRODUCT"],y=prod_sum["TAR"],
                    marker=dict(color="#93c5fd",line=dict(width=0)),width=0.4,offset=-0.2))
                fig_pb.add_trace(go.Bar(name="Achievement",x=prod_sum["PRODUCT"],y=prod_sum["ACH"],
                    marker=dict(color=[pct_color(p) for p in prod_sum["PCT"]],opacity=.9,line=dict(width=0)),
                    width=0.4,offset=0.1,
                    text=[f"{p:.1f}%" for p in prod_sum["PCT"]],textposition="outside",textfont=dict(size=10)))
                fig_pb.update_layout(**PLOTLY_BASE,barmode="overlay",height=320,
                    margin=dict(t=10,b=80,l=60,r=10),
                    xaxis=dict(tickangle=-35,tickfont=dict(size=10,color="#64748b"),showgrid=False),
                    yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),title="Units"),
                    legend=dict(orientation="h",y=1.05,bgcolor="rgba(0,0,0,0)"))
                st.plotly_chart(fig_pb,use_container_width=True,config={"displayModeBar":False})

            with cp2:
                ps = prod_sum.sort_values("PCT",ascending=True)
                fig_h = go.Figure(go.Bar(y=ps["PRODUCT"],x=ps["PCT"],orientation="h",
                    marker=dict(color=[pct_color(p) for p in ps["PCT"]],opacity=.85,line=dict(width=0)),
                    text=[f"{p:.1f}%" for p in ps["PCT"]],textposition="outside"))
                fig_h.add_vline(x=100,line_color="#22c55e",line_dash="dot",line_width=1.5)
                fig_h.update_layout(**PLOTLY_BASE,height=320,
                    margin=dict(t=10,b=40,l=200,r=60),
                    xaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),ticksuffix="%"),
                    yaxis=dict(tickfont=dict(size=10,color="#64748b")))
                st.plotly_chart(fig_h,use_container_width=True,config={"displayModeBar":False})

            prod_tbl = prod_sum[["PRODUCT","TAR","ACH","PCT"]].copy()
            prod_tbl.columns = ["Product","Target (units)","Achievement (units)","Unit Ach %"]
            prod_tbl["Variance"] = prod_tbl["Achievement (units)"] - prod_tbl["Target (units)"]
            st.dataframe(prod_tbl.style.format({"Target (units)":"{:,.0f}","Achievement (units)":"{:,.0f}",
                "Unit Ach %":"{:.1f}%","Variance":"{:+,.0f}"}),
                use_container_width=True,hide_index=True)

# ╔══════════════════════════════╗
# ║  TAB — LKR TREND            ║
# ╚══════════════════════════════╝
with tab6:
    section("LKR ACHIEVEMENT TREND — ALL MONTHS × ALL ENTITIES")
    view = st.selectbox("View",["Division TOTAL","Each DM","Each SBDM","Each RP/Rep"],key="lkr_view")

    trend_rows = []
    for m in month_list:
        for e in all_eo[m]:
            d = all_lkr[m].get(e,{})
            if not d.get('TAR_LKR'): continue
            if view=="Division TOTAL" and e!="TOTAL": continue
            if view=="Each DM" and not is_dm(e): continue
            if view=="Each SBDM" and not is_sbdm(e): continue
            if view=="Each RP/Rep" and (is_dm(e) or is_sbdm(e) or e=="TOTAL"): continue
            trend_rows.append(dict(Month=m,Entity=e,TAR_LKR=d['TAR_LKR'],
                ACH_LKR=d['ACH_LKR'],PCT_LKR=d['PCT_LKR'],VAR_LKR=d['VAR_LKR'],
                Role=get_role(e)))

    if trend_rows:
        tr_df = pd.DataFrame(trend_rows)
        col_t1,col_t2 = st.columns(2)
        with col_t1:
            fig_lkr = px.line(tr_df,x="Month",y="ACH_LKR",color="Entity",markers=True,
                color_discrete_sequence=PALETTE,labels={"ACH_LKR":"Achievement (LKR)"},
                hover_data={"TAR_LKR":":.0f","PCT_LKR":":.1f","Role":True})
            fig_lkr.update_layout(**PLOTLY_BASE,height=320,margin=dict(t=10,b=40,l=80,r=20),
                legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.05,xanchor="right",x=1),
                xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
                yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),title="LKR"))
            st.plotly_chart(fig_lkr,use_container_width=True,config={"displayModeBar":False})

        with col_t2:
            fig_pct = px.line(tr_df,x="Month",y="PCT_LKR",color="Entity",markers=True,
                color_discrete_sequence=PALETTE,labels={"PCT_LKR":"LKR Ach %"})
            fig_pct.add_hline(y=100,line_color="#22c55e",line_dash="dot",line_width=1.5)
            fig_pct.update_layout(**PLOTLY_BASE,height=320,margin=dict(t=10,b=40,l=60,r=20),
                legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.05,xanchor="right",x=1),
                xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
                yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),
                           title="LKR Ach %",ticksuffix="%"))
            st.plotly_chart(fig_pct,use_container_width=True,config={"displayModeBar":False})

        full_tbl = tr_df.rename(columns={"TAR_LKR":"Target (LKR)","ACH_LKR":"Achievement (LKR)",
                                          "PCT_LKR":"Ach %","VAR_LKR":"Variance (LKR)"})
        st.dataframe(full_tbl.style.format({
            "Target (LKR)":"LKR {:,.0f}","Achievement (LKR)":"LKR {:,.0f}",
            "Ach %":"{:.1f}%","Variance (LKR)":"LKR {:+,.0f}"}),
            use_container_width=True,hide_index=True,height=min(500,len(full_tbl)*40+60))

# ╔══════════════════════════════╗
# ║  TAB — CUMULATIVE           ║
# ╚══════════════════════════════╝
with tab7:
    section("📊 CUMULATIVE ACHIEVEMENT ANALYSIS")
    cum_c1,cum_c2,cum_c3 = st.columns(3)
    with cum_c1:
        cum_sel_month = st.selectbox("Cumulative up to Month",month_list,
                                      index=len(month_list)-1,key="cum_month")
    with cum_c2:
        cum_entity_opts = ["ALL (TOTAL only)"] + [e for e in all_entities if e!='TOTAL']
        cum_sel_entity  = st.selectbox("Entity / Person",cum_entity_opts,key="cum_entity")
    with cum_c3:
        cum_product_opts = ["ALL Products"] + sorted(all_products)
        cum_sel_product  = st.selectbox("Product",cum_product_opts,key="cum_product")

    months_up_to   = month_list[:month_list.index(cum_sel_month)+1]
    entity_for_kpi = 'TOTAL' if cum_sel_entity=="ALL (TOTAL only)" else cum_sel_entity

    cum_tar_total = cum_ach_total = 0.0
    for product in all_products:
        if cum_sel_product!="ALL Products" and product!=cum_sel_product: continue
        d = cum_data.get(cum_sel_month,{}).get(entity_for_kpi,{}).get(product,{})
        cum_tar_total += d.get('CUM_TAR',0.0)
        cum_ach_total += d.get('CUM_ACH',0.0)
    cum_pct_overall = (cum_ach_total/cum_tar_total*100) if cum_tar_total>0 else 0.0
    cum_var_overall = cum_ach_total - cum_tar_total

    ck1,ck2,ck3,ck4 = st.columns(4)
    kpi_card(ck1,"Cumulative Target (units)",fmt_n(cum_tar_total),"🎯","c-blue",sub=f"{len(months_up_to)} months")
    kpi_card(ck2,"Cumulative Achievement (units)",fmt_n(cum_ach_total),"✅","c-green",
             badge_text=f"{'▲' if cum_var_overall>=0 else '▼'} {fmt_n(abs(cum_var_overall))}",
             badge_cls=pct_cls(cum_pct_overall))
    kpi_card(ck3,"Cumulative Ach %",f"{cum_pct_overall:.1f}%","📈",
             "c-green" if cum_pct_overall>=100 else "c-amber" if cum_pct_overall>=80 else "c-red",
             badge_cls=pct_cls(cum_pct_overall))
    kpi_card(ck4,"Months Accumulated",str(len(months_up_to)),"📅","c-indigo",
             sub=" → ".join(months_up_to))

    cum_chart_rows = []
    for product in (all_products if cum_sel_product=="ALL Products" else [cum_sel_product]):
        for m in months_up_to:
            d = cum_data.get(m,{}).get(entity_for_kpi,{}).get(product,{})
            pct=d.get('CUM_PCT',0.0); ct=d.get('CUM_TAR',0.0); ca=d.get('CUM_ACH',0.0)
            if ct>0:
                cum_chart_rows.append(dict(Month=m,Product=product,CUM_PCT=pct,CUM_TAR=ct,CUM_ACH=ca))

    if cum_chart_rows:
        cc_df = pd.DataFrame(cum_chart_rows)
        col_line,col_bar_cum = st.columns([3,2])
        with col_line:
            fig_cl = px.line(cc_df,x="Month",y="CUM_PCT",color="Product",markers=True,
                color_discrete_sequence=PALETTE,labels={"CUM_PCT":"Cumulative Ach %"},
                hover_data={"CUM_TAR":":,.0f","CUM_ACH":":,.0f"})
            fig_cl.add_hline(y=100,line_color="#22c55e",line_dash="dot",line_width=2)
            fig_cl.update_layout(**PLOTLY_BASE,height=360,margin=dict(t=10,b=40,l=70,r=20),
                legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.05,xanchor="right",x=1,font=dict(size=10)),
                xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
                yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),
                           title="Cumulative Ach %",ticksuffix="%"))
            st.plotly_chart(fig_cl,use_container_width=True,config={"displayModeBar":False})

        with col_bar_cum:
            last_m = cc_df[cc_df["Month"]==cum_sel_month].sort_values("CUM_PCT",ascending=True)
            if not last_m.empty:
                fig_cb = go.Figure(go.Bar(y=last_m["Product"],x=last_m["CUM_PCT"],orientation="h",
                    marker=dict(color=[pct_color(p) for p in last_m["CUM_PCT"]],opacity=0.85,line=dict(width=0)),
                    text=[f"{p:.1f}%" for p in last_m["CUM_PCT"]],textposition="outside"))
                fig_cb.add_vline(x=100,line_color="#22c55e",line_dash="dot",line_width=1.5)
                fig_cb.update_layout(**PLOTLY_BASE,height=360,margin=dict(t=10,b=40,l=200,r=70),
                    xaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),ticksuffix="%"),
                    yaxis=dict(tickfont=dict(size=10,color="#64748b")))
                st.plotly_chart(fig_cb,use_container_width=True,config={"displayModeBar":False})

    section(f"ENTITY COMPARISON — Cumulative % as of {cum_sel_month}")
    comp_product = st.selectbox("Product for Entity Comparison",
                                 ["ALL Products"]+sorted(all_products),key="cum_comp_product")
    comp_rows = []
    for entity in all_entities:
        if entity=='TOTAL': continue
        prods_c = all_products if comp_product=="ALL Products" else [comp_product]
        c_tar = sum(cum_data.get(cum_sel_month,{}).get(entity,{}).get(p,{}).get('CUM_TAR',0.0) for p in prods_c)
        c_ach = sum(cum_data.get(cum_sel_month,{}).get(entity,{}).get(p,{}).get('CUM_ACH',0.0) for p in prods_c)
        c_pct = (c_ach/c_tar*100) if c_tar>0 else 0.0
        if c_tar>0:
            comp_rows.append(dict(Entity=entity,Role=get_role(entity),
                                   CUM_TAR=c_tar,CUM_ACH=c_ach,CUM_PCT=c_pct,CUM_VAR=c_ach-c_tar))
    if comp_rows:
        comp_df = pd.DataFrame(comp_rows).sort_values("CUM_PCT",ascending=False)
        achievement_rows_ui(
            [dict(name=r["Entity"],TAR=r["CUM_TAR"],ACH=r["CUM_ACH"],PCT=r["CUM_PCT"])
             for _,r in comp_df.iterrows()],fmt_fn=fmt_n)

# ══════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════
st.markdown(
    f'<div class="dash-footer">Universal Sales Intelligence Hub · {dash_title} · {sel_month} · v13.0</div>',
    unsafe_allow_html=True)
