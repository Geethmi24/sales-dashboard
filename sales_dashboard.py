"""
MEGA DERMA Sales Intelligence Hub — v10.0 (Cumulative Tab Added)
"""

import re
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="MEGA DERMA Sales Hub",
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
[data-testid="stSidebar"] .sb-brand{background:linear-gradient(135deg,#1d4ed8,#0ea5e9);margin:0 -1rem 1.5rem;padding:1.4rem 1.5rem;border-bottom:1px solid #1e3a5f;}
[data-testid="stSidebar"] .sb-brand h2{color:#fff !important;font-size:1.05rem !important;font-weight:700 !important;margin:0 !important;}
[data-testid="stSidebar"] .sb-brand p{color:#93c5fd !important;font-size:.72rem !important;margin:2px 0 0 !important;}
[data-testid="stSidebar"] .stSelectbox>div>div{background:#162032 !important;border:1px solid #1e3a5f !important;border-radius:9px !important;}
[data-testid="stSidebar"] hr{border-color:#1e3a5f !important;margin:1rem 0 !important;}
[data-testid="stSidebar"] .sb-label{font-size:.68rem !important;font-weight:700 !important;color:#475569 !important;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.5rem;display:block;}
[data-testid="stSidebar"] .stat-pill{background:#162032;border:1px solid #1e3a5f;border-radius:8px;padding:10px 14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;}
[data-testid="stSidebar"] .stat-pill .sp-label{font-size:.72rem;color:#64748b !important;}
[data-testid="stSidebar"] .stat-pill .sp-value{font-size:.88rem;font-weight:700;color:#e2e8f0 !important;}

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
.kpi-icon-wrap{width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;margin-bottom:12px;}
.c-blue .kpi-icon-wrap{background:#dbeafe;}.c-green .kpi-icon-wrap{background:#dcfce7;}.c-amber .kpi-icon-wrap{background:#fef3c7;}
.c-purple .kpi-icon-wrap{background:#ede9fe;}.c-red .kpi-icon-wrap{background:#fee2e2;}.c-teal .kpi-icon-wrap{background:#ccfbf1;}
.c-indigo .kpi-icon-wrap{background:#e0e7ff;}
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

.insight-strip{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:1.5rem;}
.insight-pill{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:10px 16px;font-size:.78rem;color:#475569;display:flex;align-items:center;gap:8px;flex:1;min-width:160px;}
.insight-pill strong{color:#1e293b;font-weight:700;}
.insight-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}

.ach-row{display:flex;align-items:center;gap:12px;padding:10px 16px;border-radius:12px;margin-bottom:8px;border:1px solid #e2e8f0;background:#fff;}
.ach-row:hover{box-shadow:0 4px 12px rgba(0,0,0,.08);}
.ach-rank{font-size:.72rem;font-weight:800;color:#94a3b8;width:20px;text-align:center;flex-shrink:0;}
.ach-name{font-size:.83rem;font-weight:600;color:#1e293b;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.ach-track{flex:2;background:#f1f5f9;border-radius:999px;height:10px;overflow:hidden;}
.ach-fill{height:100%;border-radius:999px;}
.ach-tar{font-size:.7rem;color:#94a3b8;width:90px;text-align:right;flex-shrink:0;}
.ach-ach{font-size:.7rem;font-weight:700;width:90px;text-align:right;flex-shrink:0;}
.ach-pct-badge{font-size:.72rem;font-weight:800;padding:3px 10px;border-radius:999px;width:58px;text-align:center;flex-shrink:0;}
.ach-pct-badge.green{background:#dcfce7;color:#15803d;}.ach-pct-badge.amber{background:#fef3c7;color:#92400e;}.ach-pct-badge.red{background:#fee2e2;color:#b91c1c;}
.ach-header{display:flex;align-items:center;gap:12px;padding:6px 16px;margin-bottom:4px;font-size:.68rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;}

.dm-block{border:1px solid #e2e8f0;border-radius:16px;margin-bottom:1.5rem;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05);}
.dm-header{background:linear-gradient(135deg,#1e3a5f,#1d4ed8);padding:1rem 1.4rem;display:flex;align-items:center;justify-content:space-between;}
.dm-header-left{display:flex;align-items:center;gap:12px;}
.dm-name{font-size:1rem;font-weight:800;color:#fff;}
.dm-formula{font-size:.72rem;color:#93c5fd;margin-top:2px;font-family:monospace;}
.dm-kpis{display:flex;gap:16px;}
.dm-kpi{text-align:right;}
.dm-kpi-label{font-size:.65rem;font-weight:700;color:#93c5fd;text-transform:uppercase;}
.dm-kpi-value{font-size:1rem;font-weight:800;color:#fff;}
.dm-kpi-pct{font-size:.75rem;font-weight:700;padding:2px 8px;border-radius:999px;display:inline-block;margin-top:2px;}
.dm-kpi-pct.green{background:rgba(34,197,94,.25);color:#4ade80;}.dm-kpi-pct.amber{background:rgba(245,158,11,.25);color:#fbbf24;}.dm-kpi-pct.red{background:rgba(239,68,68,.25);color:#f87171;}
.dm-rp-list{background:#fff;}
.dm-rp-row{display:flex;align-items:center;gap:12px;padding:10px 1.4rem;border-bottom:1px solid #f8fafc;}
.dm-rp-row:last-child{border-bottom:none;}
.dm-rp-row:hover{background:#f8fafc;}
.rp-bullet{width:6px;height:6px;border-radius:50%;flex-shrink:0;}
.rp-name{font-size:.83rem;font-weight:600;color:#1e293b;flex:1;}
.rp-tar{font-size:.78rem;color:#94a3b8;width:110px;text-align:right;flex-shrink:0;}
.rp-ach{font-size:.78rem;font-weight:700;width:110px;text-align:right;flex-shrink:0;}
.rp-var{font-size:.78rem;font-weight:700;width:100px;text-align:right;flex-shrink:0;}
.rp-pct-badge{font-size:.7rem;font-weight:800;padding:2px 8px;border-radius:999px;width:54px;text-align:center;flex-shrink:0;}
.rp-pct-badge.green{background:#dcfce7;color:#15803d;}.rp-pct-badge.amber{background:#fef3c7;color:#92400e;}.rp-pct-badge.red{background:#fee2e2;color:#b91c1c;}
.rp-track{flex:1.5;background:#f1f5f9;border-radius:999px;height:6px;overflow:hidden;min-width:60px;}
.rp-fill{height:100%;border-radius:999px;}
.dm-rp-header{display:flex;align-items:center;gap:12px;padding:6px 1.4rem;background:#f8fafc;border-bottom:1px solid #e2e8f0;font-size:.65rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;}
.dm-totals-row{display:flex;align-items:center;gap:12px;padding:10px 1.4rem;background:#f0f9ff;border-top:2px solid #bae6fd;font-size:.78rem;font-weight:700;color:#0369a1;}

.tbl-wrap{background:#fff;border:1px solid #e2e8f0;border-radius:16px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05);}
.tbl-toolbar{display:flex;align-items:center;justify-content:space-between;padding:1rem 1.3rem;border-bottom:1px solid #f1f5f9;background:#fafafa;}
.tbl-toolbar-title{font-size:.88rem;font-weight:700;color:#1e293b;}
.tbl-toolbar-meta{font-size:.72rem;color:#94a3b8;}

.info-box{background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;padding:10px 16px;margin-bottom:1.2rem;font-size:.8rem;color:#1e40af;}
.info-box-green{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:10px 16px;margin-bottom:1.2rem;font-size:.8rem;color:#15803d;}

.cum-matrix-wrap{overflow-x:auto;border-radius:14px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,.05);}
.cum-matrix-table{width:100%;border-collapse:collapse;font-size:.8rem;}
.cum-matrix-table th{background:#1e3a5f;color:#e2e8f0;font-weight:700;padding:10px 14px;text-align:center;font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap;position:sticky;top:0;}
.cum-matrix-table th.entity-col{text-align:left;background:#0f172a;min-width:160px;}
.cum-matrix-table td{padding:9px 14px;border-bottom:1px solid #f1f5f9;white-space:nowrap;}
.cum-matrix-table td.entity-name{font-weight:700;color:#1e293b;background:#fafafa;border-right:2px solid #e2e8f0;position:sticky;left:0;}
.cum-matrix-table tr:hover td{background:#f8fafc;}
.cum-matrix-table tr:hover td.entity-name{background:#f1f5f9;}
.cum-matrix-table td.pct-cell{text-align:center;font-weight:700;border-radius:6px;}
.pct-green{background:#dcfce7;color:#15803d;}
.pct-amber{background:#fef3c7;color:#92400e;}
.pct-red{background:#fee2e2;color:#b91c1c;}
.pct-zero{background:#f1f5f9;color:#94a3b8;}
.cum-matrix-table .total-row td{background:#dbeafe !important;font-weight:800;color:#1e40af;border-top:2px solid #93c5fd;}
.cum-matrix-table .total-row td.entity-name{background:#bfdbfe !important;}

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
    hoverlabel=dict(bgcolor="#0f172a", font_size=12,
                    font_color="#f8fafc", bordercolor="#1e3a5f"),
)
SKIP_SHEETS = {'SOURCE', 'HO', 'SPC', 'SOURCE (2)', 'SIX MONTHS',
               'JAN-2', 'FEB-2', 'MAR-2', 'six months', 'DEC-2'}
MONTH_ORDER = ['APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC','JAN','FEB','MAR']

# ══════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════
def fmt_n(n, dec=0):
    """Plain number with commas, whole numbers only"""
    try:
        return f"{int(round(float(n))):,}"
    except:
        return str(n)


def fmt_lkr(n):
    """LKR value — whole numbers, no decimals"""
    try:
        return f"LKR {int(round(float(n))):,}"
    except:
        return str(n)


def fmt_lkr_short(n):
    """Short LKR for KPI cards"""
    try:
        v = float(n)
        if abs(v) >= 1_000_000:
            return f"LKR {v / 1_000_000:.2f}M"
        if abs(v) >= 1_000:
            return f"LKR {v / 1_000:.1f}K"
        return f"LKR {v:,.0f}"
    except:
        return str(n)

def pct_cls(p):   return "up" if p >= 100 else "neu" if p >= 80 else "down"
def pct_color(p): return "#16a34a" if p >= 100 else "#d97706" if p >= 80 else "#dc2626"
def pct_badge(p): return "green"   if p >= 100 else "amber"   if p >= 80 else "red"
def is_dm(name):  return "(DM)" in str(name).upper()

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
# EXCEL PARSING
# ══════════════════════════════════════════════════════
def parse_excel(file_obj):
    xls = pd.ExcelFile(file_obj)
    sheets = [s for s in xls.sheet_names if s.upper() not in {x.upper() for x in SKIP_SHEETS}]

    all_lkr    = {}
    all_units  = {}
    all_dm_rp  = {}
    all_eo     = {}
    all_prod   = {}
    all_prices = {}
    # NEW: store raw product-level unit data per sheet: {sheet: {entity: {product: {TAR, ACH}}}}
    all_prod_entity = {}

    for sheet in sheets:
        try:
            raw = pd.read_excel(file_obj, sheet_name=sheet, header=None)
        except Exception:
            continue
        if raw.shape[0] < 13 or raw.shape[1] < 6:
            continue

        row0 = raw.iloc[0]
        row1 = raw.iloc[1]

        entity_cols = {}
        for j in range(4, raw.shape[1] - 1, 2):
            name_cell = row0.iloc[j] if j < len(row0) else None
            if pd.isna(name_cell) or str(name_cell).strip() in ('', 'nan'):
                continue
            hdr = str(row1.iloc[j]).strip() if j < len(row1) and pd.notna(row1.iloc[j]) else ''
            if hdr not in ('TAR', ''):
                continue
            entity_cols[str(name_cell).strip()] = j

        if not entity_cols:
            continue

        ordered_entities = list(entity_cols.keys())
        all_eo[sheet]    = ordered_entities

        prod_rows = []
        for r in range(2, 14):
            if r >= raw.shape[0]: break
            pname = raw.iloc[r, 1]
            if not isinstance(pname, str) or pname.strip() in ('', 'nan', 'TOTAL', '0'):
                continue
            pname = pname.strip()
            tar4  = pd.to_numeric(raw.iloc[r, 4], errors='coerce')
            if pd.isna(tar4) or tar4 <= 0:
                continue
            prod_rows.append(r)

            price_cell = raw.iloc[r, 3] if raw.shape[1] > 3 else None
            if pd.notna(price_cell) and isinstance(price_cell, (int, float)) and price_cell > 1:
                all_prices[pname] = float(price_cell)

        units_ms = {}
        prod_entity_sheet = {}  # {entity: {product: {TAR, ACH}}}
        for ename, tc in entity_cols.items():
            ac = tc + 1
            tar_s = raw.iloc[prod_rows, tc].apply(pd.to_numeric, errors='coerce').fillna(0)
            ach_s = raw.iloc[prod_rows, ac].apply(pd.to_numeric, errors='coerce').fillna(0) if ac < raw.shape[1] else pd.Series([0]*len(prod_rows))
            tar_t = float(pd.to_numeric(tar_s, errors='coerce').fillna(0).sum())
            ach_t = float(pd.to_numeric(ach_s, errors='coerce').fillna(0).sum())
            var   = ach_t - tar_t
            pct   = (ach_t / tar_t * 100) if tar_t else 0.0
            units_ms[ename] = dict(TAR=tar_t, ACH=ach_t, VAR=var, PCT=pct)

            # Per-product per-entity data
            prod_entity_sheet[ename] = {}
            for idx_r, r in enumerate(prod_rows):
                pname = str(raw.iloc[r, 1]).strip()
                t = float(raw.iloc[prod_rows, tc].iloc[idx_r]) if pd.notna(raw.iloc[prod_rows, tc].iloc[idx_r]) else 0.0
                a = float(raw.iloc[prod_rows, ac].iloc[idx_r]) if ac < raw.shape[1] and pd.notna(raw.iloc[prod_rows, ac].iloc[idx_r]) else 0.0
                prod_entity_sheet[ename][pname] = dict(TAR=max(t,0), ACH=max(a,0))

        all_units[sheet] = units_ms
        all_prod_entity[sheet] = prod_entity_sheet

        lkr_row_idx = None
        for r in range(13, min(25, raw.shape[0])):
            val1 = str(raw.iloc[r, 1]).strip() if pd.notna(raw.iloc[r, 1]) else ''
            val4 = raw.iloc[r, 4] if raw.shape[1] > 4 else None
            if val1 == 'TOTAL' and pd.notna(val4) and isinstance(val4, (int, float)) and val4 > 10000:
                lkr_row_idx = r
                break

        lkr_ms = {}
        if lkr_row_idx is not None:
            for ename, tc in entity_cols.items():
                ac = tc + 1
                tar_lkr = pd.to_numeric(raw.iloc[lkr_row_idx, tc], errors='coerce')
                ach_lkr = pd.to_numeric(raw.iloc[lkr_row_idx, ac], errors='coerce') if ac < raw.shape[1] else np.nan
                tar_lkr = float(tar_lkr) if pd.notna(tar_lkr) else 0.0
                ach_lkr = float(ach_lkr) if pd.notna(ach_lkr) else 0.0
                var_lkr = ach_lkr - tar_lkr
                pct_lkr = (ach_lkr / tar_lkr * 100) if tar_lkr else 0.0
                lkr_ms[ename] = dict(TAR_LKR=tar_lkr, ACH_LKR=ach_lkr, VAR_LKR=var_lkr, PCT_LKR=pct_lkr)
        all_lkr[sheet] = lkr_ms

        dm_rp = {}
        cur_dm = None
        for ename in ordered_entities:
            if ename == 'TOTAL':
                continue
            if is_dm(ename):
                cur_dm = ename
                dm_rp[cur_dm] = []
            elif cur_dm is not None:
                dm_rp[cur_dm].append(ename)
        all_dm_rp[sheet] = dm_rp

        prod_rows_list = []
        for r in prod_rows:
            pname = str(raw.iloc[r, 1]).strip()
            price = all_prices.get(pname, 0.0)
            for ename, tc in entity_cols.items():
                ac = tc + 1
                t = pd.to_numeric(raw.iloc[r, tc], errors='coerce')
                a = pd.to_numeric(raw.iloc[r, ac], errors='coerce') if ac < raw.shape[1] else np.nan
                t = float(t) if pd.notna(t) else 0.0
                a = float(a) if pd.notna(a) else 0.0
                if t == 0 and a == 0:
                    continue
                prod_rows_list.append(dict(
                    ENTITY=ename, PRODUCT=pname,
                    TAR=t, ACH=a,
                    VAR=a - t,
                    PCT=(a / t * 100) if t else 0.0,
                    PRICE=price,
                    TAR_LKR=t * price,
                    ACH_LKR=a * price,
                ))
        all_prod[sheet] = pd.DataFrame(prod_rows_list) if prod_rows_list else pd.DataFrame()

    return all_lkr, all_units, all_dm_rp, all_eo, all_prod, all_prices, all_prod_entity


# ══════════════════════════════════════════════════════
# CUMULATIVE COMPUTATION
# ══════════════════════════════════════════════════════
def build_cumulative_data(month_list, all_prod_entity, all_eo, all_dm_rp):
    """
    Returns:
      cum_by_month_product_entity:
        {month: {entity: {product: {CUM_TAR, CUM_ACH, CUM_PCT}}}}

      For April (first month): CUM_TAR = TAR_APR, CUM_ACH = ACH_APR → real %
      For May:  CUM_TAR = TAR_APR + TAR_MAY, CUM_ACH = ACH_APR + ACH_MAY → real %
      ...

      Also returns:
      all_products: sorted list of all product names across all months
      all_entities: ordered list of entities (from first available month)
    """
    # Collect all products
    all_products = set()
    for m in month_list:
        pe = all_prod_entity.get(m, {})
        for ent_data in pe.values():
            all_products.update(ent_data.keys())
    all_products = sorted(all_products)

    # Collect all entities (from all months, preserving first-seen order)
    seen_entities = []
    seen_set = set()
    for m in month_list:
        for e in all_eo.get(m, []):
            if e not in seen_set:
                seen_entities.append(e)
                seen_set.add(e)

    # Build cumulative: running totals per entity per product
    cum_by_month_product_entity = {}
    running_tar = {}  # {entity: {product: cumulative_TAR}}
    running_ach = {}  # {entity: {product: cumulative_ACH}}

    for m in month_list:
        pe = all_prod_entity.get(m, {})
        cum_by_month_product_entity[m] = {}

        for entity in seen_entities:
            entity_prod_data = pe.get(entity, {})
            if entity not in running_tar:
                running_tar[entity] = {}
                running_ach[entity] = {}

            cum_by_month_product_entity[m][entity] = {}

            for product in all_products:
                month_tar = entity_prod_data.get(product, {}).get('TAR', 0.0)
                month_ach = entity_prod_data.get(product, {}).get('ACH', 0.0)

                # Add to running totals
                running_tar[entity][product] = running_tar[entity].get(product, 0.0) + month_tar
                running_ach[entity][product] = running_ach[entity].get(product, 0.0) + month_ach

                cum_t = running_tar[entity][product]
                cum_a = running_ach[entity][product]
                cum_p = (cum_a / cum_t * 100) if cum_t > 0 else 0.0

                cum_by_month_product_entity[m][entity] = cum_by_month_product_entity[m].get(entity, {})
                cum_by_month_product_entity[m][entity][product] = dict(
                    CUM_TAR=cum_t,
                    CUM_ACH=cum_a,
                    CUM_PCT=cum_p,
                    MONTH_TAR=month_tar,
                    MONTH_ACH=month_ach,
                )

    return cum_by_month_product_entity, all_products, seen_entities


# ══════════════════════════════════════════════════════
# UI COMPONENTS
# ══════════════════════════════════════════════════════
def achievement_rows_ui(rows: list, value_label="Value", fmt_fn=fmt_n):
    if not rows: st.info("No data."); return
    rows_s = sorted(rows, key=lambda x: x['PCT'], reverse=True)
    header = f"""
    <div class="ach-header">
        <div style="width:20px"></div>
        <div class="ach-name">Name</div>
        <div style="flex:2">Progress</div>
        <div class="ach-tar">Target</div>
        <div class="ach-ach">Achieved</div>
        <div style="width:58px;text-align:center">Ach %</div>
    </div>"""
    body = ""
    for i, r in enumerate(rows_s):
        p   = r['PCT']
        c   = pct_color(p)
        bcl = pct_badge(p)
        bg  = '#f0fdf4' if p >= 100 else '#fffbeb' if p >= 80 else '#fff'
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


def render_dm_hierarchy(dm_rp_sheet, data_ms, fmt_fn=fmt_n, label="units"):
    if not dm_rp_sheet:
        st.info("No DM → RP mapping found."); return
    for idx, (dm, rp_list) in enumerate(dm_rp_sheet.items()):
        dm_d   = data_ms.get(dm, {})
        dm_tar = dm_d.get('TAR', dm_d.get('TAR_LKR', 0))
        dm_ach = dm_d.get('ACH', dm_d.get('ACH_LKR', 0))
        dm_var = dm_d.get('VAR', dm_d.get('VAR_LKR', 0))
        dm_pct = dm_d.get('PCT', dm_d.get('PCT_LKR', 0))
        dm_col = PALETTE[idx % len(PALETTE)]
        pct_c  = pct_badge(dm_pct)
        rp_formula = " + ".join(rp_list) if rp_list else "No RP sub-teams"

        html = f"""
        <div class="dm-block">
          <div class="dm-header" style="border-left:5px solid {dm_col}">
            <div class="dm-header-left">
              <div>
                <div class="dm-name">👤 {dm}</div>
                <div class="dm-formula">= {rp_formula}</div>
              </div>
            </div>
            <div class="dm-kpis">
              <div class="dm-kpi">
                <div class="dm-kpi-label">Target ({label})</div>
                <div class="dm-kpi-value">{fmt_fn(dm_tar)}</div>
              </div>
              <div class="dm-kpi">
                <div class="dm-kpi-label">Achievement ({label})</div>
                <div class="dm-kpi-value">{fmt_fn(dm_ach)}</div>
                <span class="dm-kpi-pct {pct_c}">{dm_pct:.1f}%</span>
              </div>
              <div class="dm-kpi">
                <div class="dm-kpi-label">Variance</div>
                <div class="dm-kpi-value" style="color:{'#4ade80' if dm_var>=0 else '#f87171'}">
                  {'+' if dm_var>=0 else ''}{fmt_fn(dm_var)}
                </div>
              </div>
            </div>
          </div>"""

        if rp_list:
            html += """
          <div class="dm-rp-header">
            <div style="width:10px"></div>
            <div style="flex:1">RP / Sales Rep</div>
            <div style="flex:1.5">Progress</div>
            <div style="width:110px;text-align:right">Target</div>
            <div style="width:110px;text-align:right">Achievement</div>
            <div style="width:100px;text-align:right">Variance</div>
            <div style="width:54px;text-align:center">Ach %</div>
          </div>
          <div class="dm-rp-list">"""
            rp_tar_sum = rp_ach_sum = 0
            for rp in rp_list:
                rd  = data_ms.get(rp, {})
                rp_t = rd.get('TAR', rd.get('TAR_LKR', 0))
                rp_a = rd.get('ACH', rd.get('ACH_LKR', 0))
                rp_v = rd.get('VAR', rd.get('VAR_LKR', 0))
                rp_p = rd.get('PCT', rd.get('PCT_LKR', 0))
                rc   = pct_color(rp_p)
                rb   = pct_badge(rp_p)
                rp_tar_sum += rp_t
                rp_ach_sum += rp_a
                html += f"""
            <div class="dm-rp-row">
              <div class="rp-bullet" style="background:{rc}"></div>
              <div class="rp-name">{rp}</div>
              <div class="rp-track">
                <div class="rp-fill" style="width:{min(rp_p,100):.1f}%;background:{rc};opacity:.8"></div>
              </div>
              <div class="rp-tar">{fmt_fn(rp_t)}</div>
              <div class="rp-ach" style="color:{rc}">{fmt_fn(rp_a)}</div>
              <div class="rp-var" style="color:{rc}">{'+' if rp_v>=0 else ''}{fmt_fn(rp_v)}</div>
              <div class="rp-pct-badge {rb}">{rp_p:.1f}%</div>
            </div>"""
            roll_pct  = (rp_ach_sum / rp_tar_sum * 100) if rp_tar_sum else 0
            match_note = "✓ DM = Σ RP" if abs(dm_tar - rp_tar_sum) < 10 else f"⚠ DM {fmt_fn(dm_tar)} ≠ Σ RP {fmt_fn(rp_tar_sum)}"
            html += f"""
          </div>
          <div class="dm-totals-row">
            <div style="width:10px"></div>
            <div style="flex:1">∑ RP Rollup → {dm} &nbsp; <span style="color:#0284c7;font-size:.7rem">{match_note}</span></div>
            <div style="flex:1.5"></div>
            <div style="width:110px;text-align:right">{fmt_fn(rp_tar_sum)}</div>
            <div style="width:110px;text-align:right">{fmt_fn(rp_ach_sum)}</div>
            <div style="width:100px;text-align:right;color:{'#0369a1' if rp_ach_sum>=rp_tar_sum else '#dc2626'}">
              {'+' if rp_ach_sum-rp_tar_sum>=0 else ''}{fmt_fn(rp_ach_sum-rp_tar_sum)}
            </div>
            <div style="width:54px;text-align:center;font-weight:800;color:#0369a1">{roll_pct:.1f}%</div>
          </div>"""
        else:
            html += '<div class="dm-rp-list"><div class="dm-rp-row" style="color:#94a3b8;font-size:.8rem;font-style:italic">No RP sub-teams.</div></div>'
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)


def donut_chart(label_vals, center_label, key, pal_offset=0):
    items = [(k, v) for k, v in label_vals.items() if v and v > 0]
    if not items: st.info("No data."); return
    labels, vals = zip(*items)
    colors = PALETTE[pal_offset:pal_offset + len(labels)]
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
                      margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=key)


# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
st.markdown("""
 <div style="padding-bottom:10px">
     <h2>📊 MEGA DERMA Sales Hub</h2>
     <p>Performance Dashboard</p>
 </div>
 """, unsafe_allow_html=True)

st.markdown("---")
st.markdown('<span style="font-weight:bold">📂 Upload Excel</span>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["xlsx", "xls"])
st.markdown("---")
st.markdown('<span style="font-weight:bold">📅 Month</span>', unsafe_allow_html=True)

if uploaded_file:
    with st.spinner("Parsing Excel…"):
        (all_lkr, all_units, all_dm_rp,
         all_eo, all_prod, global_prices, all_prod_entity) = parse_excel(uploaded_file)

    month_list = [m for m in MONTH_ORDER if m in all_lkr]
    if not month_list:
        st.error("No valid sheets found.")
        st.stop()

    sel_month = st.selectbox("Month", month_list)

    lkr_ms   = all_lkr[sel_month]
    units_ms = all_units[sel_month]
    drm      = all_dm_rp[sel_month]
    eo       = all_eo[sel_month]
    prd      = all_prod.get(sel_month, pd.DataFrame())

    dm_keys = [e for e in eo if is_dm(e)]
    all_sub_rps = {rp for rps in drm.values() for rp in rps}
    standalone_rps = [e for e in eo if e != 'TOTAL' and not is_dm(e) and e not in all_sub_rps]

    total_lkr     = lkr_ms.get('TOTAL', {})
    total_tar_lkr = total_lkr.get('TAR_LKR', 0)
    total_ach_lkr = total_lkr.get('ACH_LKR', 0)
    total_var_lkr = total_lkr.get('VAR_LKR', 0)
    total_pct_lkr = total_lkr.get('PCT_LKR', 0)

    total_units = units_ms.get('TOTAL', {})
    total_tar_u = total_units.get('TAR', 0)
    total_ach_u = total_units.get('ACH', 0)
    total_pct_u = total_units.get('PCT', 0)
    total_var_u = total_units.get('VAR', 0)

    p_col  = "#4ade80" if total_pct_lkr >= 100 else "#fbbf24" if total_pct_lkr >= 80 else "#f87171"
    pu_col = "#4ade80" if total_pct_u >= 100 else "#fbbf24" if total_pct_u >= 80 else "#f87171"

    st.markdown("---")
    st.markdown('<span style="font-weight:bold">📌 Quick Stats</span>', unsafe_allow_html=True)
    st.markdown(f"""
     <div>Target (LKR): {fmt_lkr(total_tar_lkr)}</div>
     <div>Achievement (LKR): {fmt_lkr(total_ach_lkr)}</div>
     <div style="color:{p_col}">LKR Ach %: {total_pct_lkr:.1f}%</div>
     <div>Target (units): {fmt_n(total_tar_u)}</div>
     <div>Achievement (units): {fmt_n(total_ach_u)}</div>
     <div style="color:{pu_col}">Unit Ach %: {total_pct_u:.1f}%</div>
     <div>DMs: {len(dm_keys)}</div>
     <div>Months loaded: {len(month_list)}</div>
     """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span style="font-weight:bold">🔍 Filter DM</span>', unsafe_allow_html=True)
    dm_filter = st.selectbox("DM", ["ALL"] + dm_keys)

    # Build cumulative data (once per session)
    cum_data, all_products, all_entities = build_cumulative_data(
        month_list, all_prod_entity, all_eo, all_dm_rp
    )

else:
    st.info("Upload the MEGA DERMA Excel file.")

st.markdown("---")
st.markdown("<small style='color:#334155;font-size:.68rem'>MEGA DERMA Sales Hub · v10.0</small>",
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# LANDING
# ══════════════════════════════════════════════════════
if not uploaded_file:
    st.markdown("""
     <div class="landing">
         <div class="landing-logo">📊</div>
         <h2>MEGA DERMA Sales Intelligence Hub</h2>
         <p>Upload your MEGA DERMA Excel file to instantly see targets, achievements
         and the DM → RP hierarchy — all figures read directly from your Excel.</p>
         <div class="landing-card">
             <h4>What the dashboard reads from your Excel</h4>
             <ul>
                 <li><strong>Row 17 (TOTAL row):</strong> LKR Target &amp; Achievement per entity (exactly as in Excel)</li>
                 <li><strong>Rows 2–12:</strong> 11 product unit counts per entity</li>
                 <li><strong>Row 0:</strong> Entity names (TOTAL, DMs, RPs)</li>
                 <li><strong>Col 3 (some sheets):</strong> Product prices for LKR computation</li>
                 <li><strong>DM detection:</strong> any entity name containing <code>(DM)</code></li>
                 <li><strong>Skipped:</strong> JAN-2, FEB-2, MAR-2, SOURCE, HO, SPC, six months</li>
             </ul>
         </div>
     </div>""", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════
v_sign = "▲" if total_var_lkr >= 0 else "▼"
v_col  = "#4ade80" if total_var_lkr >= 0 else "#f87171"
st.markdown(f"""
<div class="page-header">
    <div>
        <h1>📊 MEGA DERMA Sales Performance</h1>
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
tab2, tab1, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📅 All Months",
    "📆 Overview",   # ✅ static
    "👥 DM Breakdown",
    "🏢 RP / Rep Detail",
    "📦 Products",
    "📈 LKR Trend",
    "📊 Cumulative",
])

# ╔══════════════════════════════╗
# ║  TAB 2 — MONTH OVERVIEW     ║
# ╚══════════════════════════════╝
with tab1:
    # ✅ Month dropdown — drives ALL data in this tab
    ov_month = st.selectbox(
        "Select Month",
        month_list,
        index=month_list.index(sel_month),  # default = sidebar selection
        key="overview_month"
    )

    # Re-derive all data for the chosen overview month
    ov_lkr_ms = all_lkr[ov_month]
    ov_units_ms = all_units[ov_month]
    ov_drm = all_dm_rp[ov_month]
    ov_eo = all_eo[ov_month]
    ov_prd = all_prod.get(ov_month, pd.DataFrame())
    ov_dm_keys = [e for e in ov_eo if is_dm(e)]

    ov_total_lkr = ov_lkr_ms.get('TOTAL', {})
    ov_total_tar_lkr = ov_total_lkr.get('TAR_LKR', 0)
    ov_total_ach_lkr = ov_total_lkr.get('ACH_LKR', 0)
    ov_total_var_lkr = ov_total_lkr.get('VAR_LKR', 0)
    ov_total_pct_lkr = ov_total_lkr.get('PCT_LKR', 0)

    ov_total_units = ov_units_ms.get('TOTAL', {})
    ov_total_tar_u = ov_total_units.get('TAR', 0)
    ov_total_ach_u = ov_total_units.get('ACH', 0)
    ov_total_pct_u = ov_total_units.get('PCT', 0)
    ov_total_var_u = ov_total_units.get('VAR', 0)

    section("LKR PERFORMANCE (from Excel row 17)")
    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, "Total Target (LKR)", fmt_lkr(ov_total_tar_lkr), "🎯", "c-blue",
             sub=f"Row 17, TOTAL col · {ov_month}")
    kpi_card(c2, "Total Achievement (LKR)", fmt_lkr(ov_total_ach_lkr), "💰", "c-green",
             badge_text=f"{'▲' if ov_total_var_lkr >= 0 else '▼'} {fmt_lkr(abs(ov_total_var_lkr))}",
             badge_cls=pct_cls(ov_total_pct_lkr))
    kpi_card(c3, "LKR Achievement %", f"{ov_total_pct_lkr:.1f}%", "📈",
             "c-green" if ov_total_pct_lkr >= 100 else "c-amber",
             badge_text="On Track" if ov_total_pct_lkr >= 100 else "Below Target",
             badge_cls=pct_cls(ov_total_pct_lkr))
    kpi_card(c4, "LKR Variance",
             fmt_lkr(abs(ov_total_var_lkr)),
             "📊" if ov_total_var_lkr >= 0 else "📉",
             "c-teal" if ov_total_var_lkr >= 0 else "c-red",
             badge_text="▲ Surplus" if ov_total_var_lkr >= 0 else "▼ Shortfall",
             badge_cls="up" if ov_total_var_lkr >= 0 else "down")

    non_total_ents = [(e, ov_lkr_ms[e]) for e in ov_eo
                      if e != 'TOTAL' and ov_lkr_ms.get(e, {}).get('TAR_LKR', 0) > 0]
    if non_total_ents:
        best = max(non_total_ents, key=lambda x: x[1]['PCT_LKR'])
        above = sum(1 for _, d in non_total_ents if d['PCT_LKR'] >= 100)
        st.markdown(f"""
        <div class="insight-strip">
            <div class="insight-pill">
                <div class="insight-dot" style="background:#22c55e"></div>
                Best entity: <strong>{best[0]}</strong> at <strong>{best[1]['PCT_LKR']:.1f}%</strong>
            </div>
        </div>""", unsafe_allow_html=True)

    section("LKR: TARGET vs ACHIEVEMENT BY ENTITY")
    top_ents = [e for e in ov_eo if e != 'TOTAL' and ov_lkr_ms.get(e, {}).get('TAR_LKR', 0) > 0]

    col_bar, col_pie = st.columns([3, 2])
    with col_bar:
        st.markdown('<div class="card"><div class="card-header"><div>'
                    '<div class="card-title">LKR TAR vs ACH — All Entities</div>'
                    '<div class="card-sub">From row 17 of Excel · Achievement % annotated</div>'
                    '</div><span class="card-badge">Bar</span></div>', unsafe_allow_html=True)
        if top_ents:
            tars = [ov_lkr_ms[e]['TAR_LKR'] for e in top_ents]
            achs = [ov_lkr_ms[e]['ACH_LKR'] for e in top_ents]
            pcts = [ov_lkr_ms[e]['PCT_LKR'] for e in top_ents]
            short = [n[:13] + "…" if len(n) > 13 else n for n in top_ents]
            fig_b = go.Figure()
            fig_b.add_trace(go.Bar(
                name="Target", x=top_ents, y=tars,
                marker=dict(color="#93c5fd", line=dict(width=0)), width=0.35, offset=-0.2,
                hovertemplate="<b>%{x}</b><br>TAR: LKR %{y:,.0f}<extra></extra>"))
            fig_b.add_trace(go.Bar(
                name="Achievement", x=top_ents, y=achs,
                marker=dict(color=[pct_color(p) for p in pcts], opacity=0.9, line=dict(width=0)),
                width=0.35, offset=0.05,
                text=[f"{p:.1f}%" for p in pcts],
                textposition="outside", textfont=dict(size=10, color="#475569"),
                hovertemplate="<b>%{x}</b><br>ACH: LKR %{y:,.0f} (%{text})<extra></extra>"))
            fig_b.update_layout(
                **PLOTLY_BASE, barmode="overlay", height=360,
                margin=dict(t=30, b=100, l=80, r=20), bargap=0.25,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                            bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(tickangle=-40, tickfont=dict(size=10, color="#64748b"), showgrid=False,
                           tickmode="array", tickvals=list(range(len(top_ents))), ticktext=short),
                yaxis=dict(gridcolor="#f1f5f9", tickfont=dict(size=10, color="#94a3b8"), title="LKR"))
            st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pie:
        st.markdown('<div class="card"><div class="card-header"><div>'
                    '<div class="card-title">DM Achievement Share (LKR)</div>'
                    '</div><span class="card-badge">Pie</span></div>', unsafe_allow_html=True)
        donut_chart(
            {k: ov_lkr_ms.get(k, {}).get('ACH_LKR', 0)
             for k in ov_dm_keys if ov_lkr_ms.get(k, {}).get('ACH_LKR', 0) > 0},
            "DM ACH LKR", key=f"dm_donut_{ov_month}")
        st.markdown('</div>', unsafe_allow_html=True)

    section("LKR ACHIEVEMENT % RANKING")
    col_rank, col_sc = st.columns([3, 2])
    with col_rank:
        st.markdown('<div class="card"><div class="card-header"><div>'
                    '<div class="card-title">Achievement % by Entity (LKR)</div>'
                    '<div class="card-sub">Green ≥100% · Amber ≥80% · Red &lt;80%</div>'
                    '</div></div>', unsafe_allow_html=True)
        achievement_rows_ui(
            [dict(name=e, TAR=ov_lkr_ms[e]['TAR_LKR'],
                  ACH=ov_lkr_ms[e]['ACH_LKR'], PCT=ov_lkr_ms[e]['PCT_LKR'])
             for e in top_ents],
            fmt_fn=fmt_lkr
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_sc:
        st.markdown('<div class="card"><div class="card-header"><div>'
                    '<div class="card-title">TAR vs ACH Scatter (LKR)</div>'
                    '<div class="card-sub">Above diagonal = on/over target</div>'
                    '</div></div>', unsafe_allow_html=True)
        sc_rows = [dict(Entity=e, TAR=ov_lkr_ms[e]['TAR_LKR'],
                        ACH=ov_lkr_ms[e]['ACH_LKR'],
                        PCT=ov_lkr_ms[e]['PCT_LKR'],
                        Type="DM" if is_dm(e) else "RP/Rep")
                   for e in top_ents]
        if sc_rows:
            sc_df = pd.DataFrame(sc_rows)
            fig_sc = px.scatter(sc_df, x="TAR", y="ACH", color="Type", size="PCT",
                                hover_name="Entity",
                                hover_data={"TAR": ":.0f", "ACH": ":.0f", "PCT": ":.1f", "Type": False},
                                color_discrete_map={"DM": "#3b82f6", "RP/Rep": "#8b5cf6"},
                                size_max=26)
            mx = max(sc_df["TAR"].max(), sc_df["ACH"].max()) * 1.1
            fig_sc.add_shape(type="line", x0=0, y0=0, x1=mx, y1=mx,
                             line=dict(color="#94a3b8", dash="dot", width=1.5))
            fig_sc.update_layout(
                **PLOTLY_BASE, height=320, margin=dict(t=10, b=50, l=70, r=10),
                legend=dict(font=dict(size=11), bgcolor="rgba(0,0,0,0)",
                            orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1),
                xaxis=dict(gridcolor="#f1f5f9", tickfont=dict(color="#94a3b8", size=10),
                           title="Target (LKR)"),
                yaxis=dict(gridcolor="#f1f5f9", tickfont=dict(color="#94a3b8", size=10),
                           title="Achievement (LKR)"))
            st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    section("ENTITY SUMMARY TABLE")
    tbl_rows = []
    for e in ov_eo:
        lkr_d = ov_lkr_ms.get(e, {})
        unit_d = ov_units_ms.get(e, {})
        etype = "TOTAL" if e == "TOTAL" else "DM" if is_dm(e) else "RP/Rep"
        tbl_rows.append({
            "Entity": e, "Type": etype,
            "Target LKR": round(lkr_d.get("TAR_LKR", 0), 0),
            "Achievement LKR": round(lkr_d.get("ACH_LKR", 0), 0),
            "LKR Ach %": round(lkr_d.get("PCT_LKR", 0), 1),
            "LKR Variance": round(lkr_d.get("VAR_LKR", 0), 0),
            "Target Units": round(unit_d.get("TAR", 0), 0),
            "Achievement Units": round(unit_d.get("ACH", 0), 0),
            "Unit Ach %": round(unit_d.get("PCT", 0), 1),
            "Unit Variance": round(unit_d.get("VAR", 0), 0),
        })
    tbl_df = pd.DataFrame(tbl_rows)
    numeric_cols = ["Target LKR", "Achievement LKR", "LKR Variance",
                    "Target Units", "Achievement Units", "Unit Variance"]
    tbl_df = tbl_df[~(tbl_df[numeric_cols] == 0).all(axis=1)]
    st.dataframe(
        tbl_df.style
        .format({
            "Target LKR": "{:,.0f}", "Achievement LKR": "{:,.0f}",
            "LKR Ach %": "{:.1f}%", "LKR Variance": "{:+,.0f}",
            "Target Units": "{:,.0f}", "Achievement Units": "{:,.0f}",
            "Unit Ach %": "{:.1f}%", "Unit Variance": "{:+,.0f}",
        })
        .map(lambda v: ("color:#059669;font-weight:700" if v >= 0 else "color:#dc2626;font-weight:700")
        if isinstance(v, (int, float)) else "",
             subset=["LKR Variance", "Unit Variance"])
        .map(lambda v: (
            "color:#059669;font-weight:700" if v >= 100
            else "color:#d97706;font-weight:700" if v >= 80
            else "color:#dc2626;font-weight:700")
        if isinstance(v, (int, float)) else "",
             subset=["LKR Ach %", "Unit Ach %"]),
        use_container_width=True, hide_index=True,
        height=min(520, len(tbl_df) * 42 + 60))
    dl1, _ = st.columns([1, 5])
    with dl1:
        st.download_button(
            "⬇️ Export CSV",
            data=tbl_df.to_csv(index=False).encode("utf-8"),
            file_name=f"megaderma_{ov_month}.csv",
            mime="text/csv",
            use_container_width=True)
# ╔══════════════════════════════╗
# ║  TAB 1 — ALL MONTHS         ║
# ╚══════════════════════════════╝
with tab2:
    summary_rows = []
    for m in month_list:
        lkr_m  = all_lkr[m]
        unit_m = all_units[m]
        eo_m   = all_eo[m]
        drm_m  = all_dm_rp[m]
        dm_k   = [e for e in eo_m if is_dm(e)]

        tot_lkr  = lkr_m.get('TOTAL', {})
        tot_unit = unit_m.get('TOTAL', {})

        summary_rows.append({
            "Month": m,
            "Target (LKR)":       tot_lkr.get("TAR_LKR", 0),
            "Achievement (LKR)":  tot_lkr.get("ACH_LKR", 0),
            "LKR Ach %":          tot_lkr.get("PCT_LKR", 0),
            "LKR Variance":       tot_lkr.get("VAR_LKR", 0),
            "Target (units)":     tot_unit.get("TAR", 0),
            "Achievement (units)":tot_unit.get("ACH", 0),
            "Unit Ach %":         tot_unit.get("PCT", 0),
            "# DMs":              len(dm_k),
        })
    sum_df = pd.DataFrame(summary_rows)

    section("OVERALL — ALL MONTHS")
    g1,g2,g3,g4 = st.columns(4)
    grand_tar_lkr = sum_df["Target (LKR)"].sum()
    grand_ach_lkr = sum_df["Achievement (LKR)"].sum()
    grand_pct_lkr = (grand_ach_lkr / grand_tar_lkr * 100) if grand_tar_lkr else 0
    grand_var_lkr = grand_ach_lkr - grand_tar_lkr
    kpi_card(g1, "Grand Total Target (LKR)", fmt_lkr(grand_tar_lkr), "🎯", "c-blue", sub=f"{len(sum_df)} months")
    kpi_card(g2, "Grand Total Achievement (LKR)", fmt_lkr(grand_ach_lkr), "💰", "c-green",
             badge_text=f"{'▲' if grand_var_lkr>=0 else '▼'} {fmt_lkr(abs(grand_var_lkr))}",
             badge_cls="up" if grand_var_lkr>=0 else "down")
    kpi_card(g3, "Overall LKR Ach %", f"{grand_pct_lkr:.1f}%", "📈",
             "c-green" if grand_pct_lkr>=100 else "c-amber",
             badge_cls=pct_cls(grand_pct_lkr))
    kpi_card(g4, "LKR Variance (total)", fmt_lkr(abs(grand_var_lkr)),
             "📊" if grand_var_lkr>=0 else "📉",
             "c-teal" if grand_var_lkr>=0 else "c-red",
             badge_text="▲ Surplus" if grand_var_lkr>=0 else "▼ Shortfall",
             badge_cls="up" if grand_var_lkr>=0 else "down")

    st.markdown("<br>", unsafe_allow_html=True)
    section("MONTHLY TREND")
    cl1, cl2 = st.columns([3, 2])
    with cl1:
        st.markdown('<div class="card"><div class="card-header"><div>'
                    '<div class="card-title">Monthly LKR TAR vs ACH</div>'
                    '<div class="card-sub">Ach % line on right axis</div>'
                    '</div></div>', unsafe_allow_html=True)
        fig_tr = go.Figure()
        fig_tr.add_trace(go.Bar(name="Target", x=sum_df["Month"], y=sum_df["Target (LKR)"],
            marker=dict(color="#93c5fd", opacity=0.9, line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>TAR: LKR %{y:,.0f}<extra></extra>"))
        fig_tr.add_trace(go.Bar(name="Achievement", x=sum_df["Month"], y=sum_df["Achievement (LKR)"],
            marker=dict(color=[pct_color(p) for p in sum_df["LKR Ach %"]], opacity=0.9, line=dict(width=0)),
            text=[f"{p:.1f}%" for p in sum_df["LKR Ach %"]],
            textposition="outside", textfont=dict(size=11),
            hovertemplate="<b>%{x}</b><br>ACH: LKR %{y:,.0f}<extra></extra>"))
        fig_tr.add_trace(go.Scatter(name="Ach %", x=sum_df["Month"], y=sum_df["LKR Ach %"],
            mode="lines+markers", yaxis="y2",
            line=dict(color="#f59e0b", width=2, dash="dot"),
            marker=dict(size=7, color="#f59e0b", line=dict(color="#fff", width=1.5)),
            hovertemplate="<b>%{x}</b><br>Ach %%: %{y:.1f}%%<extra></extra>"))
        fig_tr.update_layout(**PLOTLY_BASE, barmode="group", height=340,
            margin=dict(t=20, b=60, l=80, r=60),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(tickfont=dict(size=11, color="#64748b"), showgrid=False),
            yaxis=dict(gridcolor="#f1f5f9", tickfont=dict(size=10, color="#94a3b8"), title="LKR"),
            yaxis2=dict(overlaying="y", side="right", showgrid=False,
                        tickfont=dict(size=10, color="#f59e0b"), ticksuffix="%"))
        st.plotly_chart(fig_tr, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with cl2:
        st.markdown('<div class="card"><div class="card-header"><div>'
                    '<div class="card-title">ACH share by month</div>'
                    '</div></div>', unsafe_allow_html=True)
        donut_chart({r["Month"]: r["Achievement (LKR)"] for r in summary_rows if r["Achievement (LKR)"]>0},
                    "All Months", key="all_months_pie")
        st.markdown('</div>', unsafe_allow_html=True)

    section("MONTH SUMMARY TABLE")
    styled_s = (sum_df.style
        .format({
            "Target (LKR)":"LKR {:,.0f}","Achievement (LKR)":"LKR {:,.0f}",
            "LKR Ach %":"{:.1f}%","LKR Variance":"LKR {:+,.0f}",
            "Target (units)":"{:,.0f}","Achievement (units)":"{:,.0f}",
            "Unit Ach %":"{:.1f}%",
        })
        .map(lambda v: ("color:#16a34a;font-weight:700" if v>=100
                        else "color:#d97706;font-weight:700" if v>=80
                        else "color:#dc2626;font-weight:700")
             if isinstance(v,(int,float)) else "", subset=["LKR Ach %","Unit Ach %"])
        .set_table_styles([
            {"selector":"th","props":[("background","#f8fafc"),("color","#64748b"),
                ("font-size","0.74rem"),("font-weight","700"),("text-transform","uppercase"),
                ("padding","10px 14px"),("border-bottom","2px solid #e2e8f0")]},
            {"selector":"td","props":[("padding","10px 14px"),("font-size","0.83rem")]},
        ]))
    st.dataframe(styled_s, use_container_width=True, hide_index=True, height=min(500, len(sum_df)*44+60))
    dl2,_ = st.columns([1,5])
    with dl2:
        st.download_button("⬇️ Export CSV",
            data=sum_df.to_csv(index=False).encode("utf-8"),
            file_name="megaderma_all_months.csv", mime="text/csv",
            use_container_width=True)
            # ╔══════════════════════════════╗
# ║  TAB 3 — DM BREAKDOWN       ║
# ╚══════════════════════════════╝
with tab3:
    dm_sel_month = st.selectbox(
        "Select Month", month_list,
        index=month_list.index(sel_month),
        key="dm_month"
    )
    dm_lkr_ms = all_lkr[dm_sel_month]
    dm_drm    = all_dm_rp[dm_sel_month]
    dm_eo     = all_eo[dm_sel_month]

    section("DM MONTHLY TREND (LKR)")
    dm_trend = []
    for m in month_list:
        for e in all_eo[m]:
            if not is_dm(e): continue
            d = all_lkr[m].get(e, {})
            if not d.get('TAR_LKR'): continue
            dm_trend.append(dict(Month=m, DM=e, TAR=d['TAR_LKR'], ACH=d['ACH_LKR'], PCT=d['PCT_LKR']))

    if dm_trend:
        dt_df = pd.DataFrame(dm_trend)
        if dm_filter != "ALL": dt_df = dt_df[dt_df["DM"] == dm_filter]
        dt_df_month = dt_df[dt_df["Month"] == dm_sel_month]

        # ── DM Target & Achievement summary cards — selected month only ──
        active_dms = sorted(dt_df_month["DM"].unique()) if not dt_df_month.empty else sorted(dt_df["DM"].unique())
        dm_cols = st.columns(len(active_dms))

        for i, dm_name in enumerate(active_dms):
            dm_d = dm_lkr_ms.get(dm_name, {})
            dm_t = dm_d.get("TAR_LKR", 0)
            dm_a = dm_d.get("ACH_LKR", 0)
            dm_p = dm_d.get("PCT_LKR", 0)
            dm_v = dm_d.get("VAR_LKR", 0)

            bar_color = pct_color(dm_p)

            badge_bg = "#d1fae5" if dm_p >= 100 else "#fef3c7" if dm_p >= 80 else "#fee2e2"
            badge_fg = "#065f46" if dm_p >= 100 else "#92400e" if dm_p >= 80 else "#991b1b"

            var_color = "#059669" if dm_v >= 0 else "#dc2626"
            var_sign = "+" if dm_v >= 0 else ""

            # 🔥 NEW: separate bar widths
            max_val = max(dm_t, dm_a, 1)
            tar_w = (dm_t / max_val) * 100
            ach_w = (dm_a / max_val) * 100

            dm_cols[i].markdown(f"""
                <div style="background:#fff;border:1px solid #e8edf5;border-radius:14px;
                            padding:1.1rem 1.2rem;box-shadow:0 2px 8px rgba(0,0,0,0.05);
                            border-top:3px solid {bar_color}">

                  <div style="font-size:1 rem;font-weight:700;color:#64748b;
                              text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;
                              overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
                       title="{dm_name}">👤 {dm_name}</div>

                  <!-- TARGET -->
                  <div style="font-size:0.80rem; color:#1e293b;font-weight:600;">Target</div>
                  <div style="font-size:1rem;font-weight:700;color:#1e293b;
                              font-family:'DM Mono',monospace">{fmt_lkr(dm_t)}</div>
                  <div style="background:#f1f5f9;border-radius:999px;height:6px;margin-bottom:8px">
                    <div style="width:{tar_w:.1f}%;height:100%;background:#3b82f6;border-radius:999px"></div>
                  </div>

                  <!-- ACHIEVEMENT -->
                  <div style="font-size:0.80rem; color:#1e293b;font-weight:600;">Achievement</div>
                  <div style="font-size:1rem;font-weight:700;color:{bar_color};
                              font-family:'DM Mono',monospace">{fmt_lkr(dm_a)}</div>
                  <div style="background:#f1f5f9;border-radius:999px;height:6px;margin-bottom:8px">
                    <div style="width:{ach_w:.1f}%;height:100%;background:{bar_color};border-radius:999px"></div>
                  </div>

                  <div style="display:flex;justify-content:space-between;align-items:center">
                    <div style="font-size:0.7rem;font-weight:600;color:{var_color};
                                font-family:'DM Mono',monospace">
                      {var_sign}{fmt_lkr(dm_v)}
                    </div>
                    <span style="font-size:0.72rem;font-weight:700;padding:2px 10px;border-radius:999px;
                                 background:{badge_bg};color:{badge_fg}">{dm_p:.1f}%</span>
                  </div>

                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # बाकी code (UNCHANGED)
    # ─────────────────────────────────────────────

    section(f"DM → RP HIERARCHY — {dm_sel_month} (LKR)")
    st.markdown(
        '<div class="info-box">All LKR values read directly from <strong>row 17</strong> of the Excel sheet. DM total = sum of its RP sub-columns.</div>',
        unsafe_allow_html=True)

    filtered_drm = {k: v for k, v in dm_drm.items()
                    if (dm_filter == "ALL" or k == dm_filter)
                    and (dm_lkr_ms.get(k, {}).get("TAR_LKR", 0) != 0
                         or dm_lkr_ms.get(k, {}).get("ACH_LKR", 0) != 0)}
    filtered_drm = {dm: [rp for rp in rps
                         if dm_lkr_ms.get(rp, {}).get("TAR_LKR", 0) != 0
                         or dm_lkr_ms.get(rp, {}).get("ACH_LKR", 0) != 0]
                    for dm, rps in filtered_drm.items()}
    render_dm_hierarchy(filtered_drm, dm_lkr_ms, fmt_fn=fmt_lkr, label="LKR")

    fig_dml = px.line(dt_df, x="Month", y="ACH", color="DM", markers=True,
                      color_discrete_sequence=PALETTE, labels={"ACH": "Achievement (LKR)"},
                      hover_data={"TAR": ":.0f", "PCT": ":.1f"})

    for i, dm_name in enumerate(active_dms):
        sub = dt_df[dt_df["DM"] == dm_name]
        fig_dml.add_trace(go.Scatter(
            x=sub["Month"], y=sub["TAR"], mode="lines",
            name=f"{dm_name} — Target",
            line=dict(color=PALETTE[i % len(PALETTE)], width=1.5, dash="dot"),
            showlegend=True,
            hovertemplate=f"<b>{dm_name}</b><br>Target: LKR %{{y:,.0f}}<extra></extra>"))

    fig_dml.update_layout(**PLOTLY_BASE, height=320, margin=dict(t=10, b=40, l=80, r=20),
                          legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.05, xanchor="right", x=1,
                                      font=dict(size=10)),
                          xaxis=dict(tickfont=dict(size=10.5, color="#64748b"), showgrid=False),
                          yaxis=dict(gridcolor="#f1f5f9", tickfont=dict(size=9.5, color="#94a3b8"), title="LKR"))

    st.markdown(
        '<div class="card-wrap"><div class="card-title">Monthly ACH vs Target Trend</div><div class="card-sub">Solid = Achievement · Dashed = Target</div>',
        unsafe_allow_html=True)

    st.plotly_chart(fig_dml, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
    # ══════════════════════════════════════════════════
    # TAB 4 — RP / REP DETAIL
    # ══════════════════════════════════════════════════
with tab4:
    section(f"SALES REP PERFORMANCE — {sel_month} (LKR)")
    rp_to_dm = {rp: dm for dm, rps in drm.items() for rp in rps}
    all_reps = [e for e in eo if e != 'TOTAL' and not is_dm(e)]
    disp_reps = all_reps if dm_filter == "ALL" else [r for r in all_reps if rp_to_dm.get(r) == dm_filter]
    # Hide RPs with all-zero LKR and unit values
    disp_reps = [r for r in disp_reps
                 if lkr_ms.get(r, {}).get("TAR_LKR", 0) != 0
                 or lkr_ms.get(r, {}).get("ACH_LKR", 0) != 0
                 or units_ms.get(r, {}).get("TAR", 0) != 0
                 or units_ms.get(r, {}).get("ACH", 0) != 0]

    if not disp_reps:
        st.info("No rep data for current filter.")
    else:
        groups = {}
        for rp in disp_reps:
            owner = rp_to_dm.get(rp, "Standalone")
            groups.setdefault(owner, []).append(rp)

        for owner, rps in groups.items():
            dm_d = lkr_ms.get(owner, {})
            dm_t = dm_d.get("TAR_LKR", 0)
            dm_a = dm_d.get("ACH_LKR", 0)
            dm_p = dm_d.get("PCT_LKR", 0)
            dm_v = dm_d.get("VAR_LKR", 0)
            dm_bc = pct_color(dm_p)
            dm_bg = "#d1fae5" if dm_p >= 100 else "#fef3c7" if dm_p >= 80 else "#fee2e2"
            dm_fg = "#065f46" if dm_p >= 100 else "#92400e" if dm_p >= 80 else "#991b1b"
            dm_bar = min(dm_p, 100)

            rp_rows = [dict(name=r,
                            TAR=lkr_ms.get(r, {}).get('TAR_LKR', 0),
                            ACH=lkr_ms.get(r, {}).get('ACH_LKR', 0),
                            PCT=lkr_ms.get(r, {}).get('PCT_LKR', 0),
                            VAR=lkr_ms.get(r, {}).get('VAR_LKR', 0))
                       for r in rps if lkr_ms.get(r, {}).get('TAR_LKR', 0) > 0]
            rp_rows_s = sorted(rp_rows, key=lambda x: x['PCT'], reverse=True)

            # ── Build the full DM block as one HTML chunk ─────────────────
            html = f"""
             <div style="border:1px solid #e2e8f0;border-radius:16px;overflow:hidden;
                         box-shadow:0 3px 14px rgba(0,0,0,0.07);margin-bottom:1.8rem">

               <!-- DM HEADER -->
               <div style="background:linear-gradient(135deg,#0a1628 0%,#0d2045 50%,#163870 100%);
                           padding:1.1rem 1.4rem;border-left:5px solid {dm_bc}">
                 <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
                   <div>
                     <div style="font-size:0.6rem;font-weight:700;color:rgba(255,255,255,0.4);
                                 text-transform:uppercase;letter-spacing:0.12em;margin-bottom:3px">District Manager</div>
                     <div style="font-size:1.05rem;font-weight:800;color:#f0f6ff;letter-spacing:-0.01em">👤 {owner}</div>
                   </div>
                   <!-- TAR / ACH / VAR / PCT -->
                   <div style="display:flex;gap:0;border:1px solid rgba(255,255,255,0.1);
                               border-radius:10px;overflow:hidden">
                     <div style="padding:0.6rem 1.1rem;border-right:1px solid rgba(255,255,255,0.1)">
                       <div style="font-size:0.58rem;font-weight:700;color:rgba(255,255,255,0.4);
                                   text-transform:uppercase;letter-spacing:0.09em;margin-bottom:3px">Target</div>
                       <div style="font-size:0.95rem;font-weight:700;color:#cbd5e1;
                                   font-family:'DM Mono',monospace;white-space:nowrap">{fmt_n(int(dm_t))}</div>
                     </div>
                     <div style="padding:0.6rem 1.1rem;border-right:1px solid rgba(255,255,255,0.1);
                                 background:rgba(255,255,255,0.04)">
                       <div style="font-size:0.58rem;font-weight:700;color:rgba(255,255,255,0.4);
                                   text-transform:uppercase;letter-spacing:0.09em;margin-bottom:3px">Achievement</div>
                       <div style="font-size:0.95rem;font-weight:700;color:{dm_bc};
                                   font-family:'DM Mono',monospace;white-space:nowrap">{fmt_n(int(dm_a))}</div>
                     </div>
                     <div style="padding:0.6rem 1.1rem;border-right:1px solid rgba(255,255,255,0.1)">
                       <div style="font-size:0.58rem;font-weight:700;color:rgba(255,255,255,0.4);
                                   text-transform:uppercase;letter-spacing:0.09em;margin-bottom:3px">Variance</div>
                       <div style="font-size:0.95rem;font-weight:700;color:{dm_bc};
                                   font-family:'DM Mono',monospace;white-space:nowrap">{"+" if dm_v >= 0 else ""}{fmt_n(int(dm_v))}</div>
                     </div>
                     <div style="padding:0.6rem 1.1rem;display:flex;align-items:center">
                       <span style="font-size:0.9rem;font-weight:800;padding:4px 14px;border-radius:8px;
                                    background:{dm_bg};color:{dm_fg};white-space:nowrap">{dm_p:.1f}%</span>
                     </div>
                   </div>
                 </div>
                 <!-- DM progress bar -->
                 <div style="margin-top:10px;background:rgba(255,255,255,0.1);border-radius:999px;height:5px;overflow:hidden">
                   <div style="width:{dm_bar:.1f}%;height:100%;background:{dm_bc};border-radius:999px"></div>
                 </div>
               </div>

               <!-- COLUMN HEADERS -->
               <div style="display:flex;align-items:center;gap:0;padding:7px 14px;
                           background:#f8fafc;border-bottom:2px solid #e2e8f0">
                 <div style="width:28px;font-size:0.6rem;font-weight:700;color:#94a3b8;text-transform:uppercase">#</div>
                 <div style="flex:1.8;font-size:0.6rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.07em">Sales Rep</div>
                 <div style="width:140px;text-align:right;font-size:0.6rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.07em">🎯 Target</div>
                 <div style="width:140px;text-align:right;font-size:0.6rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.07em">✅ Achievement</div>
                 <div style="width:110px;text-align:right;font-size:0.6rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.07em">Variance</div>
                 <div style="flex:1.2;padding:0 12px;font-size:0.6rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.07em">Progress</div>
                 <div style="width:62px;text-align:center;font-size:0.6rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.07em">Ach %</div>
               </div>"""

            # ── Rep rows ──────────────────────────────────────────────────
            for i, r in enumerate(rp_rows_s):
                p = r['PCT']
                c = pct_color(p)
                var = r['VAR']
                vc = "#059669" if var >= 0 else "#dc2626"
                bg = '#f0fdf4' if p >= 100 else '#fffbeb' if p >= 80 else '#ffffff'
                bdr = '1px solid #d1fae5' if p >= 100 else '1px solid #fef3c7' if p >= 80 else '1px solid #f8fafc'
                pbg = '#d1fae5' if p >= 100 else '#fef3c7' if p >= 80 else '#fee2e2'
                pfg = '#065f46' if p >= 100 else '#92400e' if p >= 80 else '#991b1b'
                html += f"""
               <div style="display:flex;align-items:center;gap:0;padding:11px 14px;
                           background:{bg};border-bottom:{bdr}">
                 <div style="width:28px;font-size:0.68rem;font-weight:700;color:#94a3b8">#{i + 1}</div>
                 <div style="flex:1.8;font-size:0.85rem;font-weight:600;color:#1e293b;
                             overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
                             padding-right:10px" title="{r['name']}">{r['name']}</div>
                 <!-- TARGET — large, plain whole number -->
                 <div style="width:140px;text-align:right;padding-right:6px">
                   <div style="font-size:0.65rem;color:#94a3b8;font-weight:600;text-transform:uppercase;
                               letter-spacing:0.05em;margin-bottom:1px">Target</div>
                   <div style="font-size:0.92rem;font-weight:700;color:#334155;
                               font-family:'DM Mono',monospace">{fmt_n(int(r['TAR']))}</div>
                 </div>
                 <!-- ACHIEVEMENT — large, colour-coded whole number -->
                 <div style="width:140px;text-align:right;padding-right:6px">
                   <div style="font-size:0.65rem;color:#94a3b8;font-weight:600;text-transform:uppercase;
                               letter-spacing:0.05em;margin-bottom:1px">Achievement</div>
                   <div style="font-size:0.92rem;font-weight:800;color:{c};
                               font-family:'DM Mono',monospace">{fmt_n(int(r['ACH']))}</div>
                 </div>
                 <!-- VARIANCE -->
                 <div style="width:110px;text-align:right;padding-right:6px">
                   <div style="font-size:0.65rem;color:#94a3b8;font-weight:600;text-transform:uppercase;
                               letter-spacing:0.05em;margin-bottom:1px">Variance</div>
                   <div style="font-size:0.88rem;font-weight:700;color:{vc};
                               font-family:'DM Mono',monospace">{"+" if var >= 0 else ""}{fmt_n(int(var))}</div>
                 </div>
                 <!-- PROGRESS BAR -->
                 <div style="flex:1.2;padding:0 12px">
                   <div style="background:#e8edf5;border-radius:999px;height:9px;overflow:hidden">
                     <div style="width:{min(p, 100):.1f}%;height:100%;background:{c};
                                 border-radius:999px;opacity:0.85"></div>
                   </div>
                 </div>
                 <!-- ACH % BADGE -->
                 <div style="width:62px;text-align:center">
                   <span style="font-size:0.75rem;font-weight:800;padding:3px 8px;border-radius:7px;
                                background:{pbg};color:{pfg};display:inline-block">{p:.1f}%</span>
                 </div>
               </div>"""

            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        section("REP ACHIEVEMENT % RANKING (LKR)")
        st.markdown(
            '<div class="card-wrap"><div class="card-title">All Reps — Ranked by Achievement %</div><div class="card-sub">Across all DMs · sorted highest to lowest</div>',
            unsafe_allow_html=True)
        achievement_rows_ui(
            [dict(name=r, TAR=lkr_ms.get(r, {}).get('TAR_LKR', 0),
                  ACH=lkr_ms.get(r, {}).get('ACH_LKR', 0),
                  PCT=lkr_ms.get(r, {}).get('PCT_LKR', 0))
             for r in disp_reps if lkr_ms.get(r, {}).get('TAR_LKR', 0) > 0],
            fmt_fn=fmt_lkr)
        st.markdown('</div>', unsafe_allow_html=True)

        section("REP MONTHLY TREND (LKR)")
        rp_trend = []
        for m in month_list:
            drm_m = all_dm_rp[m]
            for e in all_eo[m]:
                if is_dm(e) or e == 'TOTAL': continue
                d = all_lkr[m].get(e, {})
                if not d.get('TAR_LKR'): continue
                if dm_filter != "ALL":
                    rp_dm = {rp: dm for dm, rps in drm_m.items() for rp in rps}.get(e)
                    if rp_dm != dm_filter: continue
                rp_trend.append(dict(Month=m, Rep=e, TAR=d['TAR_LKR'], ACH=d['ACH_LKR'], PCT=d['PCT_LKR']))
        if rp_trend:
            rt_df = pd.DataFrame(rp_trend)
            fig_rt = px.line(rt_df, x="Month", y="ACH", color="Rep", markers=True,
                             color_discrete_sequence=PALETTE[2:], labels={"ACH": "Achievement (LKR)"},
                             hover_data={"TAR": ":.0f", "PCT": ":.1f"})
            fig_rt.update_layout(**PLOTLY_BASE, height=300, margin=dict(t=10, b=40, l=80, r=20),
                                 legend=dict(bgcolor="rgba(0,0,0,0)"),
                                 xaxis=dict(tickfont=dict(size=10.5, color="#64748b"), showgrid=False),
                                 yaxis=dict(gridcolor="#f1f5f9", tickfont=dict(size=9.5, color="#94a3b8"), title="LKR"))
            st.markdown('<div class="card-wrap">', unsafe_allow_html=True)
            st.plotly_chart(fig_rt, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        rp_tbl = [{"Rep": r, "Under DM": rp_to_dm.get(r, "—"),
                   "Target LKR": round(lkr_ms.get(r, {}).get('TAR_LKR', 0)),
                   "Achievement LKR": round(lkr_ms.get(r, {}).get('ACH_LKR', 0)),
                   "LKR Ach%": round(lkr_ms.get(r, {}).get('PCT_LKR', 0), 1),
                   "LKR Variance": round(lkr_ms.get(r, {}).get('VAR_LKR', 0)),
                   "Target Units": round(units_ms.get(r, {}).get('TAR', 0)),
                   "Achievement Units": round(units_ms.get(r, {}).get('ACH', 0)),
                   "Unit Ach%": round(units_ms.get(r, {}).get('PCT', 0), 1)}
                  for r in disp_reps]
        if rp_tbl:
            rp_df = pd.DataFrame(rp_tbl)
            st.dataframe(rp_df.style.format({
                "Target LKR": "{:,.0f}", "Achievement LKR": "{:,.0f}",
                "LKR Ach%": "{:.1f}%", "LKR Variance": "{:+,.0f}",
                "Target Units": "{:,.0f}", "Achievement Units": "{:,.0f}", "Unit Ach%": "{:.1f}%"}),
                use_container_width=True, hide_index=True)
            dl3, _ = st.columns([1, 5])
            with dl3:
                st.download_button("⬇️ Export CSV", data=rp_df.to_csv(index=False).encode("utf-8"),
                                   file_name=f"megaderma_reps_{sel_month}.csv", mime="text/csv",
                                   use_container_width=True)

# ╔══════════════════════════════╗
# ║  TAB 5 — PRODUCTS           ║
# ╚══════════════════════════════╝
with tab5:
    section(f"PRODUCT BREAKDOWN — {sel_month}")
    if prd.empty:
        st.info("No product data.")
    else:
        ent_opts = ["ALL"] + sorted(prd["ENTITY"].unique().tolist())
        sel_ent = st.selectbox("Filter by Entity", ent_opts, key="prod_ent")
        prd_f = prd if sel_ent == "ALL" else prd[prd["ENTITY"] == sel_ent]
        prd_f = prd_f[prd_f["TAR"] > 0].copy()

        if not prd_f.empty:
            prod_sum = prd_f.groupby("PRODUCT").agg(
                TAR=("TAR","sum"), ACH=("ACH","sum"),
                TAR_LKR=("TAR_LKR","sum"), ACH_LKR=("ACH_LKR","sum")
            ).reset_index()
            prod_sum["PCT"]     = prod_sum.apply(lambda r: r["ACH"]/r["TAR"]*100 if r["TAR"]>0 else 0, axis=1)
            prod_sum["PCT_LKR"] = prod_sum.apply(lambda r: r["ACH_LKR"]/r["TAR_LKR"]*100 if r["TAR_LKR"]>0 else 0, axis=1)
            prod_sum = prod_sum.sort_values("TAR", ascending=False)

            p1,p2,p3,p4 = st.columns(4)
            kpi_card(p1, "Products", str(prod_sum["PRODUCT"].nunique()), "📦", "c-blue")
            kpi_card(p2, "Total Unit Target", fmt_n(prod_sum["TAR"].sum()), "🎯", "c-indigo")
            kpi_card(p3, "Total Unit Achievement", fmt_n(prod_sum["ACH"].sum()), "✅", "c-green")
            best_p = prod_sum.loc[prod_sum["PCT"].idxmax(), "PRODUCT"]
            kpi_card(p4, "Best Product (units)", best_p, "🏆", "c-amber",
                     badge_text=f"{prod_sum['PCT'].max():.1f}%", badge_cls="up")

            st.markdown("<br>", unsafe_allow_html=True)
            cp1, cp2 = st.columns(2)
            with cp1:
                st.markdown('<div class="card"><div class="card-header"><div>'
                            '<div class="card-title">Unit TAR vs ACH by Product</div>'
                            '</div></div>', unsafe_allow_html=True)
                fig_pb = go.Figure()
                fig_pb.add_trace(go.Bar(name="Target", x=prod_sum["PRODUCT"], y=prod_sum["TAR"],
                    marker=dict(color="#93c5fd",line=dict(width=0)), width=0.4, offset=-0.2))
                fig_pb.add_trace(go.Bar(name="Achievement", x=prod_sum["PRODUCT"], y=prod_sum["ACH"],
                    marker=dict(color=[pct_color(p) for p in prod_sum["PCT"]],opacity=.9,line=dict(width=0)),
                    width=0.4, offset=0.1,
                    text=[f"{p:.1f}%" for p in prod_sum["PCT"]],
                    textposition="outside", textfont=dict(size=10)))
                fig_pb.update_layout(**PLOTLY_BASE, barmode="overlay", height=320,
                    margin=dict(t=10,b=80,l=60,r=10),
                    xaxis=dict(tickangle=-35,tickfont=dict(size=10,color="#64748b"),showgrid=False),
                    yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),title="Units"),
                    legend=dict(orientation="h",y=1.05,bgcolor="rgba(0,0,0,0)"))
                st.plotly_chart(fig_pb, use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)

            with cp2:
                st.markdown('<div class="card"><div class="card-header"><div>'
                            '<div class="card-title">Unit Achievement % by Product</div>'
                            '</div></div>', unsafe_allow_html=True)
                ps = prod_sum.sort_values("PCT", ascending=True)
                fig_h = go.Figure(go.Bar(
                    y=ps["PRODUCT"], x=ps["PCT"], orientation="h",
                    marker=dict(color=[pct_color(p) for p in ps["PCT"]],opacity=.85,line=dict(width=0)),
                    text=[f"{p:.1f}%" for p in ps["PCT"]], textposition="outside",
                    hovertemplate="<b>%{y}</b><br>Ach %%: %{x:.1f}%%<extra></extra>"))
                fig_h.add_vline(x=100, line_color="#22c55e", line_dash="dot", line_width=1.5)
                fig_h.update_layout(**PLOTLY_BASE, height=320,
                    margin=dict(t=10,b=40,l=130,r=60),
                    xaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),
                               ticksuffix="%",title="Achievement %"),
                    yaxis=dict(tickfont=dict(size=10,color="#64748b")))
                st.plotly_chart(fig_h, use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)

            section("PRODUCT DETAIL TABLE")
            prod_tbl = prod_sum[["PRODUCT","TAR","ACH","PCT","TAR_LKR","ACH_LKR","PCT_LKR"]].copy()
            prod_tbl.columns = ["Product","Target (units)","Achievement (units)","Unit Ach %",
                                 "Target (LKR)","Achievement (LKR)","LKR Ach %"]
            prod_tbl["Variance (units)"] = prod_tbl["Achievement (units)"] - prod_tbl["Target (units)"]
            st.dataframe(prod_tbl.style.format({
                "Target (units)":"{:,.0f}","Achievement (units)":"{:,.0f}","Unit Ach %":"{:.1f}%",
                "Target (LKR)":"LKR {:,.0f}","Achievement (LKR)":"LKR {:,.0f}","LKR Ach %":"{:.1f}%",
                "Variance (units)":"{:+,.0f}"}),
                use_container_width=True, hide_index=True)


# ╔══════════════════════════════╗
# ║  TAB 6 — LKR TREND          ║
# ╚══════════════════════════════╝
with tab6:
    section("LKR ACHIEVEMENT TREND — ALL MONTHS × ALL ENTITIES")
    st.markdown("""<div class="info-box">
    All values from <strong>row 17</strong> of each sheet. Each dot = that sheet's ACH_LKR for that entity.
    </div>""", unsafe_allow_html=True)

    view = st.selectbox("View", ["Division TOTAL", "Each DM", "Each RP/Rep"], key="lkr_view")

    trend_rows = []
    for m in month_list:
        for e in all_eo[m]:
            d = all_lkr[m].get(e, {})
            if not d.get('TAR_LKR'): continue
            if view == "Division TOTAL" and e != "TOTAL": continue
            if view == "Each DM" and not is_dm(e): continue
            if view == "Each RP/Rep" and (is_dm(e) or e == "TOTAL"): continue
            trend_rows.append(dict(Month=m, Entity=e,
                TAR_LKR=d['TAR_LKR'], ACH_LKR=d['ACH_LKR'],
                PCT_LKR=d['PCT_LKR'], VAR_LKR=d['VAR_LKR']))
    if trend_rows:
        tr_df = pd.DataFrame(trend_rows)

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown('<div class="card"><div class="card-header"><div>'
                        '<div class="card-title">ACH_LKR across months</div>'
                        '</div></div>', unsafe_allow_html=True)
            fig_lkr = px.line(tr_df, x="Month", y="ACH_LKR", color="Entity", markers=True,
                color_discrete_sequence=PALETTE,
                labels={"ACH_LKR":"Achievement (LKR)"},
                hover_data={"TAR_LKR":":.0f","PCT_LKR":":.1f"})
            fig_lkr.update_layout(**PLOTLY_BASE, height=320,
                margin=dict(t=10,b=40,l=80,r=20),
                legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.05,xanchor="right",x=1),
                xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
                yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),title="LKR"))
            st.plotly_chart(fig_lkr, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with col_t2:
            st.markdown('<div class="card"><div class="card-header"><div>'
                        '<div class="card-title">LKR Ach % across months</div>'
                        '<div class="card-sub">Green dashed = 100% target</div>'
                        '</div></div>', unsafe_allow_html=True)
            fig_pct = px.line(tr_df, x="Month", y="PCT_LKR", color="Entity", markers=True,
                color_discrete_sequence=PALETTE,
                labels={"PCT_LKR":"LKR Ach %"},
                hover_data={"ACH_LKR":":.0f","TAR_LKR":":.0f"})
            fig_pct.add_hline(y=100, line_color="#22c55e", line_dash="dot", line_width=1.5,
                              annotation_text="100%", annotation_position="bottom right")
            fig_pct.update_layout(**PLOTLY_BASE, height=320,
                margin=dict(t=10,b=40,l=60,r=20),
                legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.05,xanchor="right",x=1),
                xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
                yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),
                           title="LKR Ach %",ticksuffix="%"))
            st.plotly_chart(fig_pct, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        section("FULL LKR TABLE")
        full_tbl = tr_df.rename(columns={
            "Month":"Month","Entity":"Entity",
            "TAR_LKR":"Target (LKR)","ACH_LKR":"Achievement (LKR)",
            "PCT_LKR":"Ach %","VAR_LKR":"Variance (LKR)"})
        st.dataframe(full_tbl.style.format({
            "Target (LKR)":"LKR {:,.0f}","Achievement (LKR)":"LKR {:,.0f}",
            "Ach %":"{:.1f}%","Variance (LKR)":"LKR {:+,.0f}"}),
            use_container_width=True, hide_index=True,
            height=min(500, len(full_tbl)*40+60))
        dl6,_ = st.columns([1,5])
        with dl6:
            st.download_button("⬇️ Export LKR CSV",
                data=full_tbl.to_csv(index=False).encode("utf-8"),
                file_name="megaderma_lkr_trend.csv", mime="text/csv",
                use_container_width=True)
    else:
        st.info("No data for selected view.")


# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 7 — CUMULATIVE                                     ║
# ╚══════════════════════════════════════════════════════════╝
with tab7:
    section("📊 CUMULATIVE ACHIEVEMENT ANALYSIS — ALL PRODUCTS × ALL MONTHS")

    st.markdown("""<div class="info-box-green">
    <strong>How Cumulative % is calculated:</strong><br>
    • <strong>April:</strong> CUM % = APR_ACH ÷ APR_TAR × 100 &nbsp;(first month, no prior history)<br>
    • <strong>May:</strong> CUM % = (APR_ACH + MAY_ACH) ÷ (APR_TAR + MAY_TAR) × 100<br>
    • <strong>June:</strong> CUM % = (APR_ACH + MAY_ACH + JUN_ACH) ÷ (APR_TAR + MAY_TAR + JUN_TAR) × 100<br>
    • And so on for each subsequent month — rolling totals from the start of the year.
    </div>""", unsafe_allow_html=True)

    # ── Controls ─────────────────────────────────────────────────
    cum_c1, cum_c2, cum_c3 = st.columns(3)
    with cum_c1:
        cum_sel_month = st.selectbox("View Cumulative up to Month", month_list,
                                      index=len(month_list)-1, key="cum_month")
    with cum_c2:
        cum_entity_opts = ["ALL (TOTAL only)"] + [e for e in all_entities if e != 'TOTAL']
        cum_sel_entity = st.selectbox("Entity / Person", cum_entity_opts, key="cum_entity")
    with cum_c3:
        cum_product_opts = ["ALL Products"] + sorted(all_products)
        cum_sel_product = st.selectbox("Product", cum_product_opts, key="cum_product")

    # Months to consider: all months up to and including cum_sel_month
    months_up_to = month_list[:month_list.index(cum_sel_month) + 1]

    # ── Determine entities to show ────────────────────────────────
    if cum_sel_entity == "ALL (TOTAL only)":
        show_entities = ['TOTAL']
    else:
        show_entities = [cum_sel_entity]

    # ── Summary KPI cards for selected entity × all products ──────
    section(f"CUMULATIVE KPIs — Up to {cum_sel_month}")

    # Compute cumulative for the entity across all products
    entity_for_kpi = show_entities[0] if show_entities else 'TOTAL'
    cum_tar_total = 0.0
    cum_ach_total = 0.0
    for product in all_products:
        if cum_sel_product != "ALL Products" and product != cum_sel_product:
            continue
        d = cum_data.get(cum_sel_month, {}).get(entity_for_kpi, {}).get(product, {})
        cum_tar_total += d.get('CUM_TAR', 0.0)
        cum_ach_total += d.get('CUM_ACH', 0.0)

    cum_pct_overall = (cum_ach_total / cum_tar_total * 100) if cum_tar_total > 0 else 0.0
    cum_var_overall = cum_ach_total - cum_tar_total
    months_count    = len(months_up_to)

    ck1, ck2, ck3, ck4 = st.columns(4)
    kpi_card(ck1, f"Cumulative Target (units)", fmt_n(cum_tar_total), "🎯", "c-blue",
             sub=f"APR → {cum_sel_month} · {months_count} months")
    kpi_card(ck2, f"Cumulative Achievement (units)", fmt_n(cum_ach_total), "✅", "c-green",
             badge_text=f"{'▲' if cum_var_overall>=0 else '▼'} {fmt_n(abs(cum_var_overall))}",
             badge_cls=pct_cls(cum_pct_overall))
    kpi_card(ck3, "Cumulative Ach %", f"{cum_pct_overall:.1f}%", "📈",
             "c-green" if cum_pct_overall >= 100 else "c-amber" if cum_pct_overall >= 80 else "c-red",
             badge_text="On Track" if cum_pct_overall >= 100 else "Below Target",
             badge_cls=pct_cls(cum_pct_overall))
    kpi_card(ck4, "Months Accumulated", str(months_count), "📅", "c-indigo",
             sub=f"{' → '.join(months_up_to)}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # MATRIX VIEW: Rows = Products, Columns = Months
    # Each cell shows Cumulative % for that product up to that month
    # ══════════════════════════════════════════════════════════════
    section(f"CUMULATIVE % MATRIX — {entity_for_kpi} · Products × Months")
    st.markdown(f"""<div class="info-box">
    Each cell = cumulative ACH ÷ cumulative TAR from <strong>APR</strong> up to that month column.
    &nbsp;🟢 ≥100% &nbsp;🟡 80–99% &nbsp;🔴 &lt;80% &nbsp;⬜ 0% (no target in that product)
    </div>""", unsafe_allow_html=True)

    # Build matrix: products (rows) × months (cols)
    products_to_show = all_products if cum_sel_product == "ALL Products" else [cum_sel_product]

    # Table header
    month_headers = "".join([f'<th>{m}</th>' for m in months_up_to])
    matrix_html = f"""
    <div class="cum-matrix-wrap">
    <table class="cum-matrix-table">
      <thead>
        <tr>
          <th class="entity-col">Product</th>
          {month_headers}
        </tr>
      </thead>
      <tbody>
    """

    for product in products_to_show:
        row_html = f'<tr><td class="entity-name">{product}</td>'
        for m in months_up_to:
            d   = cum_data.get(m, {}).get(entity_for_kpi, {}).get(product, {})
            pct = d.get('CUM_PCT', 0.0)
            cum_t = d.get('CUM_TAR', 0.0)
            cum_a = d.get('CUM_ACH', 0.0)

            if cum_t == 0:
                row_html += f'<td class="pct-cell pct-zero" title="No target">—</td>'
            else:
                cls = "pct-green" if pct >= 100 else "pct-amber" if pct >= 80 else "pct-red"
                row_html += (f'<td class="pct-cell {cls}" '
                             f'title="CUM TAR: {cum_t:,.0f} | CUM ACH: {cum_a:,.0f}">'
                             f'{pct:.1f}%</td>')
        row_html += '</tr>'
        matrix_html += row_html

    # Totals row (all products combined)
    matrix_html += '<tr class="total-row"><td class="entity-name">∑ ALL PRODUCTS</td>'
    for m in months_up_to:
        tot_tar = sum(cum_data.get(m, {}).get(entity_for_kpi, {}).get(p, {}).get('CUM_TAR', 0.0) for p in products_to_show)
        tot_ach = sum(cum_data.get(m, {}).get(entity_for_kpi, {}).get(p, {}).get('CUM_ACH', 0.0) for p in products_to_show)
        tot_pct = (tot_ach / tot_tar * 100) if tot_tar > 0 else 0.0
        if tot_tar == 0:
            matrix_html += '<td class="pct-cell pct-zero">—</td>'
        else:
            cls = "pct-green" if tot_pct >= 100 else "pct-amber" if tot_pct >= 80 else "pct-red"
            matrix_html += f'<td class="pct-cell {cls}" title="CUM TAR: {tot_tar:,.0f} | CUM ACH: {tot_ach:,.0f}">{tot_pct:.1f}%</td>'
    matrix_html += '</tr>'

    matrix_html += "</tbody></table></div>"
    st.markdown(matrix_html, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # LINE CHART: Cumulative % trend per product across months
    # ══════════════════════════════════════════════════════════════
    section("CUMULATIVE % TREND BY PRODUCT")
    cum_chart_rows = []
    for product in products_to_show:
        for m in months_up_to:
            d   = cum_data.get(m, {}).get(entity_for_kpi, {}).get(product, {})
            pct = d.get('CUM_PCT', 0.0)
            cum_t = d.get('CUM_TAR', 0.0)
            cum_a = d.get('CUM_ACH', 0.0)
            if cum_t > 0:
                cum_chart_rows.append(dict(
                    Month=m, Product=product,
                    CUM_PCT=pct, CUM_TAR=cum_t, CUM_ACH=cum_a
                ))

    if cum_chart_rows:
        cc_df = pd.DataFrame(cum_chart_rows)
        col_line, col_bar_cum = st.columns([3, 2])

        with col_line:
            st.markdown('<div class="card"><div class="card-header"><div>'
                        f'<div class="card-title">Cumulative Ach % — {entity_for_kpi}</div>'
                        '<div class="card-sub">Each line = cumulative ACH/TAR from APR onwards · Green dashed = 100%</div>'
                        '</div></div>', unsafe_allow_html=True)
            fig_cum_line = px.line(cc_df, x="Month", y="CUM_PCT", color="Product",
                markers=True,
                color_discrete_sequence=PALETTE,
                labels={"CUM_PCT": "Cumulative Ach %"},
                hover_data={"CUM_TAR": ":,.0f", "CUM_ACH": ":,.0f"})
            fig_cum_line.add_hline(y=100, line_color="#22c55e", line_dash="dot", line_width=2,
                                   annotation_text="100% target", annotation_position="bottom right")
            fig_cum_line.update_layout(
                **PLOTLY_BASE, height=360,
                margin=dict(t=10, b=40, l=70, r=20),
                legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h",
                            y=1.05, xanchor="right", x=1, font=dict(size=10)),
                xaxis=dict(tickfont=dict(size=11, color="#64748b"), showgrid=False),
                yaxis=dict(gridcolor="#f1f5f9", tickfont=dict(size=10, color="#94a3b8"),
                           title="Cumulative Ach %", ticksuffix="%"))
            st.plotly_chart(fig_cum_line, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with col_bar_cum:
            st.markdown('<div class="card"><div class="card-header"><div>'
                        f'<div class="card-title">Cumulative % as of {cum_sel_month}</div>'
                        '<div class="card-sub">Final cumulative % per product at selected month</div>'
                        '</div></div>', unsafe_allow_html=True)
            last_month_df = cc_df[cc_df["Month"] == cum_sel_month].sort_values("CUM_PCT", ascending=True)
            if not last_month_df.empty:
                fig_cum_bar = go.Figure(go.Bar(
                    y=last_month_df["Product"],
                    x=last_month_df["CUM_PCT"],
                    orientation="h",
                    marker=dict(
                        color=[pct_color(p) for p in last_month_df["CUM_PCT"]],
                        opacity=0.85, line=dict(width=0)
                    ),
                    text=[f"{p:.1f}%" for p in last_month_df["CUM_PCT"]],
                    textposition="outside",
                    hovertemplate="<b>%{y}</b><br>Cumulative Ach %%: %{x:.1f}%%<extra></extra>"
                ))
                fig_cum_bar.add_vline(x=100, line_color="#22c55e", line_dash="dot", line_width=1.5)
                fig_cum_bar.update_layout(
                    **PLOTLY_BASE, height=360,
                    margin=dict(t=10, b=40, l=130, r=70),
                    xaxis=dict(gridcolor="#f1f5f9", tickfont=dict(size=10, color="#94a3b8"),
                               ticksuffix="%", title="Cumulative Ach %"),
                    yaxis=dict(tickfont=dict(size=10, color="#64748b")))
                st.plotly_chart(fig_cum_bar, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # ALL ENTITIES COMPARISON — same product, same month, all entities
    # ══════════════════════════════════════════════════════════════
    section(f"ENTITY COMPARISON — Cumulative % as of {cum_sel_month}")
    st.markdown(f"""<div class="info-box">
    Compare cumulative performance across <strong>all entities</strong> for a selected product up to <strong>{cum_sel_month}</strong>.
    </div>""", unsafe_allow_html=True)

    comp_product = st.selectbox("Select Product for Entity Comparison",
                                 ["ALL Products"] + sorted(all_products),
                                 key="cum_comp_product")

    comp_rows = []
    for entity in all_entities:
        if entity == 'TOTAL':
            continue
        products_for_comp = all_products if comp_product == "ALL Products" else [comp_product]
        c_tar = sum(cum_data.get(cum_sel_month, {}).get(entity, {}).get(p, {}).get('CUM_TAR', 0.0) for p in products_for_comp)
        c_ach = sum(cum_data.get(cum_sel_month, {}).get(entity, {}).get(p, {}).get('CUM_ACH', 0.0) for p in products_for_comp)
        c_pct = (c_ach / c_tar * 100) if c_tar > 0 else 0.0
        if c_tar > 0:
            comp_rows.append(dict(
                Entity=entity,
                Type="DM" if is_dm(entity) else "RP/Rep",
                CUM_TAR=c_tar,
                CUM_ACH=c_ach,
                CUM_PCT=c_pct,
                CUM_VAR=c_ach - c_tar,
            ))

    if comp_rows:
        comp_df = pd.DataFrame(comp_rows).sort_values("CUM_PCT", ascending=False)

        # Achievement rows UI
        st.markdown('<div class="card"><div class="card-header"><div>'
                    f'<div class="card-title">Cumulative Achievement % Ranking — {comp_product} · up to {cum_sel_month}</div>'
                    '<div class="card-sub">🟢 ≥100% · 🟡 ≥80% · 🔴 &lt;80%</div>'
                    '</div></div>', unsafe_allow_html=True)
        achievement_rows_ui(
            [dict(name=r["Entity"], TAR=r["CUM_TAR"], ACH=r["CUM_ACH"], PCT=r["CUM_PCT"])
             for _, r in comp_df.iterrows()],
            fmt_fn=fmt_n
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Detailed table
        section("CUMULATIVE DETAIL TABLE")
        comp_display = comp_df.rename(columns={
            "Entity": "Entity", "Type": "Type",
            "CUM_TAR": f"Cum Target (units)",
            "CUM_ACH": f"Cum Achievement (units)",
            "CUM_PCT": "Cum Ach %",
            "CUM_VAR": "Cum Variance (units)",
        })
        styled_comp = comp_display.style.format({
            "Cum Target (units)": "{:,.0f}",
            "Cum Achievement (units)": "{:,.0f}",
            "Cum Ach %": "{:.1f}%",
            "Cum Variance (units)": "{:+,.0f}",
        }).map(
            lambda v: ("color:#16a34a;font-weight:700" if v >= 100
                       else "color:#d97706;font-weight:700" if v >= 80
                       else "color:#dc2626;font-weight:700")
            if isinstance(v, (int, float)) else "",
            subset=["Cum Ach %"]
        ).map(
            lambda v: ("color:#16a34a;font-weight:700" if v >= 0 else "color:#dc2626;font-weight:700")
            if isinstance(v, (int, float)) else "",
            subset=["Cum Variance (units)"]
        )
        st.dataframe(styled_comp, use_container_width=True, hide_index=True,
                     height=min(500, len(comp_display) * 42 + 60))

        dl7, _ = st.columns([1, 5])
        with dl7:
            st.download_button("⬇️ Export Cumulative CSV",
                data=comp_display.to_csv(index=False).encode("utf-8"),
                file_name=f"megaderma_cumulative_{cum_sel_month}.csv",
                mime="text/csv",
                use_container_width=True)
    else:
        st.info("No cumulative data available for this selection.")


# ══════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════
st.markdown(
    f'<div class="dash-footer">MEGA DERMA Sales Intelligence Hub · {sel_month} · Streamlit + Plotly · v10.0</div>',
    unsafe_allow_html=True)
