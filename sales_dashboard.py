"""
Universal Sales Intelligence Hub — v12.0
Works with ANY Excel file sharing the HIMALAYA / MEGA DERMA format.
"""

import re
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
.card-title{font-size:.9rem;font-weight:700;color:#1e293b;margin-bottom:.5rem;}

.sec-div{display:flex;align-items:center;gap:12px;margin:2rem 0 1.2rem;}
.sec-div-line{flex:1;height:1px;background:#e2e8f0;}
.sec-div-text{font-size:.72rem;font-weight:800;color:#94a3b8;text-transform:uppercase;letter-spacing:.1em;white-space:nowrap;}

.ach-row{display:flex;align-items:center;gap:12px;padding:10px 16px;border-radius:12px;margin-bottom:8px;border:1px solid #e2e8f0;background:#fff;}
.ach-rank{font-size:.72rem;font-weight:800;color:#94a3b8;width:20px;text-align:center;flex-shrink:0;}
.ach-name{font-size:.83rem;font-weight:600;color:#1e293b;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.ach-track{flex:2;background:#f1f5f9;border-radius:999px;height:10px;overflow:hidden;}
.ach-fill{height:100%;border-radius:999px;}
.ach-tar{font-size:.7rem;color:#94a3b8;width:110px;text-align:right;flex-shrink:0;}
.ach-ach{font-size:.7rem;font-weight:700;width:110px;text-align:right;flex-shrink:0;}
.ach-pct-badge{font-size:.72rem;font-weight:800;padding:3px 10px;border-radius:999px;width:58px;text-align:center;flex-shrink:0;}
.ach-pct-badge.green{background:#dcfce7;color:#15803d;}.ach-pct-badge.amber{background:#fef3c7;color:#92400e;}.ach-pct-badge.red{background:#fee2e2;color:#b91c1c;}

.dm-block{border:1px solid #e2e8f0;border-radius:16px;margin-bottom:1.5rem;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05);}
.dm-header{background:linear-gradient(135deg,#1e3a5f,#1d4ed8);padding:1rem 1.4rem;display:flex;align-items:center;justify-content:space-between;}
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

.landing{display:flex;flex-direction:column;align-items:center;padding:4rem 2rem 3rem;text-align:center;}
.landing-logo{font-size:3.5rem;margin-bottom:1.2rem;}
.landing h2{font-size:1.5rem;font-weight:800;color:#1e293b;margin-bottom:.6rem;}
.landing p{font-size:.88rem;color:#64748b;max-width:480px;line-height:1.7;}
.landing-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;padding:1.3rem 1.8rem;margin-top:1.8rem;text-align:left;max-width:560px;width:100%;}
.landing-card h4{font-size:.78rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.8rem;}
.landing-card li{font-size:.83rem;color:#475569;margin-bottom:.4rem;line-height:1.5;}

.dash-footer{text-align:center;font-size:.72rem;color:#94a3b8;margin-top:2.5rem;padding-top:1.2rem;border-top:1px solid #e2e8f0;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════
# CONSTANTS
# ══════════════════════════════
PALETTE = ["#3b82f6","#22c55e","#f59e0b","#ef4444","#8b5cf6",
           "#ec4899","#14b8a6","#f97316","#06b6d4","#a78bfa","#84cc16","#64748b"]
PLOTLY_BASE = dict(
    font=dict(family="Plus Jakarta Sans, sans-serif", size=12),
    plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
    hoverlabel=dict(bgcolor="#0f172a", font_size=12, font_color="#f8fafc", bordercolor="#1e3a5f"),
)
SKIP_SHEETS = {'SOURCE','HO','SPC','SOURCE (2)','SIX MONTHS','JAN-2','FEB-2','MAR-2','DEC-2','six months'}
MONTH_ORDER = ['APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC','JAN','FEB','MAR']

# ══════════════════════════════
# HELPERS
# ══════════════════════════════
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

def pct_cls(p): return "up" if p >= 100 else "neu" if p >= 80 else "down"
def pct_color(p): return "#16a34a" if p >= 100 else "#d97706" if p >= 80 else "#dc2626"
def pct_badge(p): return "green" if p >= 100 else "amber" if p >= 80 else "red"
def is_dm(name): return "(DM)" in str(name).upper()

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

# ══════════════════════════════
# EXCEL PARSING
# ══════════════════════════════
def find_total_row(raw):
    """Find the LKR TOTAL row — col B == 'TOTAL' and col E is large."""
    for i in range(5, min(80, raw.shape[0])):
        val_b = str(raw.iloc[i, 1]).strip() if pd.notna(raw.iloc[i, 1]) else ''
        val_e = raw.iloc[i, 4] if raw.shape[1] > 4 else None
        if val_b == 'TOTAL' and pd.notna(val_e):
            try:
                if float(val_e) > 10000:
                    return i
            except: pass
    return None

def find_product_rows(raw, total_row):
    rows = []
    for r in range(2, total_row):
        pname = raw.iloc[r, 1]
        if not isinstance(pname, str) or pname.strip() in ('', 'nan', 'TOTAL', '0'):
            continue
        tar4 = pd.to_numeric(raw.iloc[r, 4], errors='coerce')
        if pd.isna(tar4) or tar4 <= 0:
            continue
        rows.append(r)
    return rows

def parse_excel(file_obj):
    xls = pd.ExcelFile(file_obj)
    sheets = [s for s in xls.sheet_names if s.upper() not in {x.upper() for x in SKIP_SHEETS}]

    all_lkr, all_units, all_dm_rp, all_eo, all_prod = {}, {}, {}, {}, {}

    for sheet in sheets:
        try:
            raw = pd.read_excel(file_obj, sheet_name=sheet, header=None)
        except: continue
        if raw.shape[0] < 6 or raw.shape[1] < 6: continue

        row0 = raw.iloc[0]
        row1 = raw.iloc[1]

        lkr_row_idx = find_total_row(raw)
        if lkr_row_idx is None: continue

        prod_rows = find_product_rows(raw, lkr_row_idx)
        if not prod_rows: continue

        # Parse entity columns
        entity_cols = {}
        name_count = {}
        for j in range(4, raw.shape[1] - 1, 2):
            name_cell = row0.iloc[j] if j < len(row0) else None
            if pd.isna(name_cell) or str(name_cell).strip() in ('', 'nan'): continue
            hdr = str(row1.iloc[j]).strip() if j < len(row1) and pd.notna(row1.iloc[j]) else ''
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
        all_eo[sheet] = ordered_entities

        # Unit data
        units_ms = {}
        for ename, tc in entity_cols.items():
            ac = tc + 1
            tar_vals = raw.iloc[prod_rows, tc].apply(pd.to_numeric, errors='coerce').fillna(0)
            ach_vals = raw.iloc[prod_rows, ac].apply(pd.to_numeric, errors='coerce').fillna(0) if ac < raw.shape[1] else pd.Series([0]*len(prod_rows))
            t, a = float(tar_vals.sum()), float(ach_vals.sum())
            units_ms[ename] = dict(TAR=t, ACH=a, VAR=a-t, PCT=(a/t*100) if t else 0.0)
        all_units[sheet] = units_ms

        # LKR data
        lkr_ms = {}
        for ename, tc in entity_cols.items():
            ac = tc + 1
            t = float(pd.to_numeric(raw.iloc[lkr_row_idx, tc], errors='coerce') or 0)
            a_val = raw.iloc[lkr_row_idx, ac] if ac < raw.shape[1] else np.nan
            a = float(pd.to_numeric(a_val, errors='coerce') or 0)
            lkr_ms[ename] = dict(TAR_LKR=t, ACH_LKR=a, VAR_LKR=a-t, PCT_LKR=(a/t*100) if t else 0.0)
        all_lkr[sheet] = lkr_ms

        # DM → RP hierarchy
        dm_rp = {}
        cur_dm = None
        for ename in ordered_entities:
            if ename == 'TOTAL': continue
            if is_dm(ename):
                cur_dm = ename
                dm_rp[cur_dm] = []
            elif cur_dm is not None:
                dm_rp[cur_dm].append(ename)
        all_dm_rp[sheet] = dm_rp

        # Product rows
        prod_rows_list = []
        for r in prod_rows:
            pname = str(raw.iloc[r, 1]).strip()
            for ename, tc in entity_cols.items():
                ac = tc + 1
                t = float(pd.to_numeric(raw.iloc[r, tc], errors='coerce') or 0)
                a = float(pd.to_numeric(raw.iloc[r, ac] if ac < raw.shape[1] else 0, errors='coerce') or 0)
                if t == 0 and a == 0: continue
                prod_rows_list.append(dict(ENTITY=ename, PRODUCT=pname, TAR=t, ACH=a,
                    VAR=a-t, PCT=(a/t*100) if t else 0.0))
        all_prod[sheet] = pd.DataFrame(prod_rows_list) if prod_rows_list else pd.DataFrame()

    return all_lkr, all_units, all_dm_rp, all_eo, all_prod

# ══════════════════════════════
# UI COMPONENTS
# ══════════════════════════════
def achievement_rows_ui(rows, fmt_fn=fmt_n):
    if not rows: st.info("No data."); return
    rows_s = sorted(rows, key=lambda x: x['PCT'], reverse=True)
    header = """<div style="display:flex;align-items:center;gap:12px;padding:6px 16px;font-size:.68rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;">
        <div style="width:20px"></div><div style="flex:1">Name</div>
        <div style="flex:2">Progress</div><div style="width:110px;text-align:right">Target</div>
        <div style="width:110px;text-align:right">Achieved</div><div style="width:58px;text-align:center">Ach %</div></div>"""
    body = ""
    for i, r in enumerate(rows_s):
        p = r['PCT']; c = pct_color(p); bcl = pct_badge(p)
        bg = '#f0fdf4' if p >= 100 else '#fffbeb' if p >= 80 else '#fff'
        body += f"""
        <div class="ach-row" style="background:{bg}">
            <div class="ach-rank">#{i+1}</div>
            <div class="ach-name" title="{r['name']}">{r['name']}</div>
            <div class="ach-track"><div class="ach-fill" style="width:{min(p,100):.1f}%;background:{c};opacity:.85"></div></div>
            <div class="ach-tar">{fmt_fn(r['TAR'])}</div>
            <div class="ach-ach" style="color:{c}">{fmt_fn(r['ACH'])}</div>
            <div class="ach-pct-badge {bcl}">{p:.1f}%</div>
        </div>"""
    st.markdown(header + body, unsafe_allow_html=True)

def render_dm_hierarchy(dm_rp_sheet, data_ms, fmt_fn=fmt_n, label="units"):
    if not dm_rp_sheet: st.info("No DM → RP mapping found."); return
    for idx, (dm, rp_list) in enumerate(dm_rp_sheet.items()):
        dm_d = data_ms.get(dm, {})
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
            <div><div class="dm-name">👤 {dm}</div><div class="dm-formula">= {rp_formula}</div></div>
            <div class="dm-kpis">
              <div class="dm-kpi"><div class="dm-kpi-label">Target ({label})</div><div class="dm-kpi-value">{fmt_fn(dm_tar)}</div></div>
              <div class="dm-kpi"><div class="dm-kpi-label">Achievement ({label})</div><div class="dm-kpi-value">{fmt_fn(dm_ach)}</div>
                <span class="dm-kpi-pct {pct_c}">{dm_pct:.1f}%</span></div>
              <div class="dm-kpi"><div class="dm-kpi-label">Variance</div>
                <div class="dm-kpi-value" style="color:{'#4ade80' if dm_var>=0 else '#f87171'}">
                  {'+' if dm_var>=0 else ''}{fmt_fn(dm_var)}</div></div>
            </div>
          </div>"""
        if rp_list:
            html += """<div class="dm-rp-header">
              <div style="width:10px"></div><div style="flex:1">RP / Sales Rep</div>
              <div style="flex:1.5">Progress</div>
              <div style="width:110px;text-align:right">Target</div>
              <div style="width:110px;text-align:right">Achievement</div>
              <div style="width:100px;text-align:right">Variance</div>
              <div style="width:54px;text-align:center">Ach %</div></div>
            <div class="dm-rp-list">"""
            rp_tar_sum = rp_ach_sum = 0
            for rp in rp_list:
                rd = data_ms.get(rp, {})
                rp_t = rd.get('TAR', rd.get('TAR_LKR', 0))
                rp_a = rd.get('ACH', rd.get('ACH_LKR', 0))
                rp_v = rd.get('VAR', rd.get('VAR_LKR', 0))
                rp_p = rd.get('PCT', rd.get('PCT_LKR', 0))
                rc = pct_color(rp_p); rb = pct_badge(rp_p)
                rp_tar_sum += rp_t; rp_ach_sum += rp_a
                html += f"""<div class="dm-rp-row">
                  <div class="rp-bullet" style="background:{rc}"></div>
                  <div class="rp-name">{rp}</div>
                  <div class="rp-track"><div class="rp-fill" style="width:{min(rp_p,100):.1f}%;background:{rc};opacity:.8"></div></div>
                  <div class="rp-tar">{fmt_fn(rp_t)}</div>
                  <div class="rp-ach" style="color:{rc}">{fmt_fn(rp_a)}</div>
                  <div class="rp-var" style="color:{rc}">{'+' if rp_v>=0 else ''}{fmt_fn(rp_v)}</div>
                  <div class="rp-pct-badge {rb}">{rp_p:.1f}%</div></div>"""
            roll_pct = (rp_ach_sum / rp_tar_sum * 100) if rp_tar_sum else 0
            match_note = "✓ DM = Σ RP" if abs(dm_tar - rp_tar_sum) < 10 else f"⚠ DM {fmt_fn(dm_tar)} ≠ Σ RP {fmt_fn(rp_tar_sum)}"
            html += f"""</div><div class="dm-totals-row">
              <div style="width:10px"></div>
              <div style="flex:1">∑ RP Rollup → {dm} &nbsp; <span style="color:#0284c7;font-size:.7rem">{match_note}</span></div>
              <div style="flex:1.5"></div>
              <div style="width:110px;text-align:right">{fmt_fn(rp_tar_sum)}</div>
              <div style="width:110px;text-align:right">{fmt_fn(rp_ach_sum)}</div>
              <div style="width:100px;text-align:right;color:{'#0369a1' if rp_ach_sum>=rp_tar_sum else '#dc2626'}">
                {'+' if rp_ach_sum-rp_tar_sum>=0 else ''}{fmt_fn(rp_ach_sum-rp_tar_sum)}</div>
              <div style="width:54px;text-align:center;font-weight:800;color:#0369a1">{roll_pct:.1f}%</div></div>"""
        else:
            html += '<div class="dm-rp-list"><div class="dm-rp-row" style="color:#94a3b8;font-size:.8rem;font-style:italic">No RP sub-teams.</div></div>'
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

def donut_chart(label_vals, center_label, key):
    items = [(k, v) for k, v in label_vals.items() if v and v > 0]
    if not items: st.info("No data."); return
    labels, vals = zip(*items)
    fig = go.Figure(go.Pie(labels=labels, values=vals, hole=.55,
        marker=dict(colors=PALETTE[:len(labels)], line=dict(color="#fff", width=2)),
        textinfo="percent+label", textfont=dict(size=11),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>"))
    fig.add_annotation(text=f"<b>{fmt_n(sum(vals))}</b>", x=0.5, y=0.54,
                       font=dict(size=14, color="#1e293b"), showarrow=False)
    fig.add_annotation(text=center_label, x=0.5, y=0.42,
                       font=dict(size=10, color="#94a3b8"), showarrow=False)
    fig.update_layout(**PLOTLY_BASE, height=320, margin=dict(t=10,b=10,l=10,r=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=key)

# ══════════════════════════════
# SIDEBAR
# ══════════════════════════════
with st.sidebar:
    st.markdown("""<div style="padding-bottom:10px">
        <h2>📊 Sales Intelligence Hub</h2>
        <p style="font-size:.8rem;color:#64748b">Universal Sales Dashboard</p></div>""",
        unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<span style="font-weight:bold">📂 Excel Files Upload කරන්න</span>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Excel file(s) upload කරන්න",
        type=["xlsx", "xls"],
        accept_multiple_files=True
    )

    st.markdown("---")

    if uploaded_files:
        file_names = [f.name for f in uploaded_files]
        if len(file_names) > 1:
            selected_file_name = st.selectbox("📁 File Select කරන්න", file_names)
        else:
            selected_file_name = file_names[0]

        uploaded_file = next(f for f in uploaded_files if f.name == selected_file_name)
        dash_title = selected_file_name.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').upper()

        with st.spinner("Excel parse කරමින්..."):
            all_lkr, all_units, all_dm_rp, all_eo, all_prod = parse_excel(uploaded_file)

        month_list = [m for m in MONTH_ORDER if m in all_lkr]
        if not month_list:
            st.error("Valid sheets හොයාගන්නට බැරිවිය.")
            st.stop()

        st.markdown('<span style="font-weight:bold">📅 Month</span>', unsafe_allow_html=True)
        sel_month = st.selectbox("Month", month_list)

        lkr_ms   = all_lkr[sel_month]
        units_ms = all_units[sel_month]
        drm      = all_dm_rp[sel_month]
        eo       = all_eo[sel_month]
        prd      = all_prod.get(sel_month, pd.DataFrame())

        dm_keys = [e for e in eo if is_dm(e)]
        total_lkr = lkr_ms.get('TOTAL', {})
        total_tar_lkr = total_lkr.get('TAR_LKR', 0)
        total_ach_lkr = total_lkr.get('ACH_LKR', 0)
        total_var_lkr = total_lkr.get('VAR_LKR', 0)
        total_pct_lkr = total_lkr.get('PCT_LKR', 0)

        total_units = units_ms.get('TOTAL', {})
        total_tar_u = total_units.get('TAR', 0)
        total_ach_u = total_units.get('ACH', 0)
        total_pct_u = total_units.get('PCT', 0)

        p_col  = "#4ade80" if total_pct_lkr >= 100 else "#fbbf24" if total_pct_lkr >= 80 else "#f87171"
        pu_col = "#4ade80" if total_pct_u >= 100 else "#fbbf24" if total_pct_u >= 80 else "#f87171"

        st.markdown("---")
        st.markdown('<span style="font-weight:bold">📌 Quick Stats</span>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:.82rem;line-height:1.8">
        <div>Target (LKR): {fmt_lkr(total_tar_lkr)}</div>
        <div>Achievement (LKR): {fmt_lkr(total_ach_lkr)}</div>
        <div style="color:{p_col}">LKR Ach %: {total_pct_lkr:.1f}%</div>
        <div>Target (units): {fmt_n(total_tar_u)}</div>
        <div>Achievement (units): {fmt_n(total_ach_u)}</div>
        <div style="color:{pu_col}">Unit Ach %: {total_pct_u:.1f}%</div>
        <div>DMs: {len(dm_keys)}</div>
        <div>Months loaded: {len(month_list)}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        dm_filter = st.selectbox("🔍 DM Filter", ["ALL"] + dm_keys)
    else:
        st.info("Excel file upload කරන්න.")
        dash_title = "Sales Intelligence Hub"

    st.markdown("---")
    st.markdown("<small style='color:#334155;font-size:.68rem'>Universal Sales Hub · v12.0</small>", unsafe_allow_html=True)

# ══════════════════════════════
# LANDING PAGE
# ══════════════════════════════
if not uploaded_files:
    st.markdown("""
    <div class="landing">
        <div class="landing-logo">📊</div>
        <h2>Universal Sales Intelligence Hub</h2>
        <p>ඔයාගේ Excel file sidebar එකේ upload කරන්න. HIMALAYA, MEGA DERMA, හෝ ඒ format ටම ගැලපෙන ඕනෑම Excel file එකක් upload කළොත් data automatically show වෙනවා.</p>
        <div class="landing-card">
            <h4>✅ Compatible Format</h4>
            <ul>
                <li><strong>Sheets:</strong> APR, MAY, JUN … MAR (monthly)</li>
                <li><strong>Row 0:</strong> TOTAL, DMs (with "(DM)"), RPs</li>
                <li><strong>Row 1:</strong> TAR / ACH headers per entity</li>
                <li><strong>Rows 2+:</strong> Product rows — auto detected</li>
                <li><strong>TOTAL row:</strong> Auto detected — LKR values</li>
                <li><strong>Multiple files:</strong> Upload කරලා switch කරන්නත් පුළුවන්</li>
            </ul>
        </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════
# PAGE HEADER
# ══════════════════════════════
v_sign = "▲" if total_var_lkr >= 0 else "▼"
v_col  = "#4ade80" if total_var_lkr >= 0 else "#f87171"
st.markdown(f"""
<div class="page-header">
    <div><h1>📊 {dash_title} — Sales Performance</h1></div>
    <div class="hdr-chips">
        <span class="hdr-chip live">● LIVE</span>
        <span class="hdr-chip month">📅 {sel_month}</span>
        <span class="hdr-chip month" style="color:{v_col}">{v_sign} {fmt_lkr(abs(total_var_lkr))} variance</span>
    </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════
# TABS
# ══════════════════════════════
tab_all, tab_ov, tab_dm, tab_rp, tab_prod, tab_trend = st.tabs([
    "📅 සියලු Months",
    "📆 Overview",
    "👥 DM Breakdown",
    "🏢 RP Detail",
    "📦 Products",
    "📈 LKR Trend",
])

# ╔══════════════════╗
# ║ TAB: OVERVIEW   ║
# ╚══════════════════╝
with tab_ov:
    ov_month = st.selectbox("Month Select", month_list, index=month_list.index(sel_month), key="ov_m")
    ov_lkr   = all_lkr[ov_month]
    ov_units = all_units[ov_month]
    ov_drm   = all_dm_rp[ov_month]
    ov_eo    = all_eo[ov_month]
    ov_dm_keys = [e for e in ov_eo if is_dm(e)]

    ov_tot  = ov_lkr.get('TOTAL', {})
    ov_t    = ov_tot.get('TAR_LKR', 0)
    ov_a    = ov_tot.get('ACH_LKR', 0)
    ov_v    = ov_tot.get('VAR_LKR', 0)
    ov_p    = ov_tot.get('PCT_LKR', 0)
    ov_ut   = ov_units.get('TOTAL', {})

    section("LKR PERFORMANCE")
    c1,c2,c3,c4 = st.columns(4)
    kpi_card(c1,"Total Target (LKR)",fmt_lkr(ov_t),"🎯","c-blue",sub=ov_month)
    kpi_card(c2,"Total Achievement (LKR)",fmt_lkr(ov_a),"💰","c-green",
             badge_text=f"{'▲' if ov_v>=0 else '▼'} {fmt_lkr(abs(ov_v))}",badge_cls=pct_cls(ov_p))
    kpi_card(c3,"LKR Ach %",f"{ov_p:.1f}%","📈","c-green" if ov_p>=100 else "c-amber",
             badge_text="On Track" if ov_p>=100 else "Below Target",badge_cls=pct_cls(ov_p))
    kpi_card(c4,"Unit Ach %",f"{ov_ut.get('PCT',0):.1f}%","📦","c-indigo",
             sub=f"TAR: {fmt_n(ov_ut.get('TAR',0))} | ACH: {fmt_n(ov_ut.get('ACH',0))}")

    top_ents = [e for e in ov_eo if e != 'TOTAL' and ov_lkr.get(e,{}).get('TAR_LKR',0) > 0]

    section("LKR TARGET vs ACHIEVEMENT BY ENTITY")
    col_bar, col_pie = st.columns([3,2])
    with col_bar:
        st.markdown('<div class="card"><div class="card-title">LKR TAR vs ACH — All Entities</div>', unsafe_allow_html=True)
        if top_ents:
            tars = [ov_lkr[e]['TAR_LKR'] for e in top_ents]
            achs = [ov_lkr[e]['ACH_LKR'] for e in top_ents]
            pcts = [ov_lkr[e]['PCT_LKR'] for e in top_ents]
            short = [n[:13]+"…" if len(n) > 13 else n for n in top_ents]
            fig_b = go.Figure()
            fig_b.add_trace(go.Bar(name="Target", x=top_ents, y=tars,
                marker=dict(color="#93c5fd",line=dict(width=0)), width=0.35, offset=-0.2))
            fig_b.add_trace(go.Bar(name="Achievement", x=top_ents, y=achs,
                marker=dict(color=[pct_color(p) for p in pcts],opacity=0.9,line=dict(width=0)),
                width=0.35, offset=0.05,
                text=[f"{p:.1f}%" for p in pcts], textposition="outside",
                textfont=dict(size=10,color="#475569")))
            fig_b.update_layout(**PLOTLY_BASE, barmode="overlay", height=360,
                margin=dict(t=30,b=100,l=80,r=20), bargap=0.25,
                legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(tickangle=-40,tickfont=dict(size=10,color="#64748b"),showgrid=False,
                           tickmode="array",tickvals=list(range(len(top_ents))),ticktext=short),
                yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),title="LKR"))
            st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pie:
        st.markdown('<div class="card"><div class="card-title">DM Achievement Share (LKR)</div>', unsafe_allow_html=True)
        donut_chart({k: ov_lkr.get(k,{}).get('ACH_LKR',0) for k in ov_dm_keys if ov_lkr.get(k,{}).get('ACH_LKR',0)>0},
                    "DM ACH LKR", key=f"dm_donut_{ov_month}")
        st.markdown('</div>', unsafe_allow_html=True)

    section("ACHIEVEMENT % RANKING")
    achievement_rows_ui(
        [dict(name=e, TAR=ov_lkr[e]['TAR_LKR'], ACH=ov_lkr[e]['ACH_LKR'], PCT=ov_lkr[e]['PCT_LKR'])
         for e in top_ents], fmt_fn=fmt_lkr)

    section("ENTITY SUMMARY TABLE")
    tbl_rows = []
    for e in ov_eo:
        l = ov_lkr.get(e,{}); u = ov_units.get(e,{})
        tbl_rows.append({"Entity":e,"Type":"TOTAL" if e=="TOTAL" else "DM" if is_dm(e) else "RP/Rep",
            "Target LKR":round(l.get("TAR_LKR",0)),"Achievement LKR":round(l.get("ACH_LKR",0)),
            "LKR Ach %":round(l.get("PCT_LKR",0),1),"LKR Variance":round(l.get("VAR_LKR",0)),
            "Target Units":round(u.get("TAR",0)),"Achievement Units":round(u.get("ACH",0)),
            "Unit Ach %":round(u.get("PCT",0),1)})
    tbl_df = pd.DataFrame(tbl_rows)
    st.dataframe(tbl_df.style.format({
        "Target LKR":"{:,.0f}","Achievement LKR":"{:,.0f}","LKR Ach %":"{:.1f}%",
        "LKR Variance":"{:+,.0f}","Target Units":"{:,.0f}","Achievement Units":"{:,.0f}","Unit Ach %":"{:.1f}%"}),
        use_container_width=True, hide_index=True)
    st.download_button("⬇️ Export CSV", data=tbl_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{dash_title}_{ov_month}.csv", mime="text/csv")

# ╔══════════════════════╗
# ║ TAB: ALL MONTHS     ║
# ╚══════════════════════╝
with tab_all:
    summary_rows = []
    for m in month_list:
        l = all_lkr[m]; u = all_units[m]; e_m = all_eo[m]
        tl = l.get('TOTAL',{}); tu = u.get('TOTAL',{})
        summary_rows.append({"Month":m,
            "Target (LKR)":tl.get("TAR_LKR",0),"Achievement (LKR)":tl.get("ACH_LKR",0),
            "LKR Ach %":tl.get("PCT_LKR",0),"LKR Variance":tl.get("VAR_LKR",0),
            "Target (units)":tu.get("TAR",0),"Achievement (units)":tu.get("ACH",0),
            "Unit Ach %":tu.get("PCT",0),"# DMs":len([e for e in e_m if is_dm(e)])})
    sum_df = pd.DataFrame(summary_rows)

    section("GRAND TOTALS")
    g_tar = sum_df["Target (LKR)"].sum(); g_ach = sum_df["Achievement (LKR)"].sum()
    g_pct = (g_ach/g_tar*100) if g_tar else 0; g_var = g_ach - g_tar
    g1,g2,g3,g4 = st.columns(4)
    kpi_card(g1,"Grand Target (LKR)",fmt_lkr(g_tar),"🎯","c-blue",sub=f"{len(sum_df)} months")
    kpi_card(g2,"Grand Achievement (LKR)",fmt_lkr(g_ach),"💰","c-green",
             badge_text=f"{'▲' if g_var>=0 else '▼'} {fmt_lkr(abs(g_var))}",
             badge_cls="up" if g_var>=0 else "down")
    kpi_card(g3,"Overall LKR Ach %",f"{g_pct:.1f}%","📈","c-green" if g_pct>=100 else "c-amber",
             badge_cls=pct_cls(g_pct))
    kpi_card(g4,"Months Loaded",str(len(month_list)),"📅","c-indigo",sub=" → ".join(month_list))

    section("MONTHLY TREND")
    cl1, cl2 = st.columns([3,2])
    with cl1:
        st.markdown('<div class="card"><div class="card-title">Monthly LKR TAR vs ACH</div>', unsafe_allow_html=True)
        fig_tr = go.Figure()
        fig_tr.add_trace(go.Bar(name="Target",x=sum_df["Month"],y=sum_df["Target (LKR)"],
            marker=dict(color="#93c5fd",opacity=0.9,line=dict(width=0))))
        fig_tr.add_trace(go.Bar(name="Achievement",x=sum_df["Month"],y=sum_df["Achievement (LKR)"],
            marker=dict(color=[pct_color(p) for p in sum_df["LKR Ach %"]],opacity=0.9,line=dict(width=0)),
            text=[f"{p:.1f}%" for p in sum_df["LKR Ach %"]],textposition="outside",textfont=dict(size=11)))
        fig_tr.add_trace(go.Scatter(name="Ach %",x=sum_df["Month"],y=sum_df["LKR Ach %"],
            mode="lines+markers",yaxis="y2",line=dict(color="#f59e0b",width=2,dash="dot"),
            marker=dict(size=7,color="#f59e0b")))
        fig_tr.update_layout(**PLOTLY_BASE,barmode="group",height=340,
            margin=dict(t=20,b=60,l=80,r=60),
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
            yaxis=dict(gridcolor="#f1f5f9",tickfont=dict(size=10,color="#94a3b8"),title="LKR"),
            yaxis2=dict(overlaying="y",side="right",showgrid=False,
                        tickfont=dict(size=10,color="#f59e0b"),ticksuffix="%"))
        st.plotly_chart(fig_tr,use_container_width=True,config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    with cl2:
        st.markdown('<div class="card"><div class="card-title">Month-wise ACH Share</div>', unsafe_allow_html=True)
        donut_chart({r["Month"]:r["Achievement (LKR)"] for r in summary_rows if r["Achievement (LKR)"]>0},
                    "All Months", key="all_months_pie")
        st.markdown('</div>', unsafe_allow_html=True)

    section("MONTH SUMMARY TABLE")
    st.dataframe(sum_df.style.format({
        "Target (LKR)":"LKR {:,.0f}","Achievement (LKR)":"LKR {:,.0f}",
        "LKR Ach %":"{:.1f}%","LKR Variance":"LKR {:+,.0f}",
        "Target (units)":"{:,.0f}","Achievement (units)":"{:,.0f}","Unit Ach %":"{:.1f}%"}),
        use_container_width=True, hide_index=True)
    st.download_button("⬇️ Export CSV",data=sum_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{dash_title}_all_months.csv",mime="text/csv")

# ╔══════════════════════╗
# ║ TAB: DM BREAKDOWN   ║
# ╚══════════════════════╝
with tab_dm:
    dm_sel_m = st.selectbox("Month",month_list,index=month_list.index(sel_month),key="dm_m")
    dm_lkr   = all_lkr[dm_sel_m]
    dm_drm   = all_dm_rp[dm_sel_m]
    dm_eo    = all_eo[dm_sel_m]

    section("DM PERFORMANCE CARDS")
    dm_keys_m = [e for e in dm_eo if is_dm(e)]
    if dm_filter != "ALL":
        dm_keys_m = [d for d in dm_keys_m if d == dm_filter]

    dm_cols = st.columns(max(len(dm_keys_m), 1))
    for i, dm_name in enumerate(dm_keys_m):
        d = dm_lkr.get(dm_name, {})
        t,a,v,p = d.get("TAR_LKR",0),d.get("ACH_LKR",0),d.get("VAR_LKR",0),d.get("PCT_LKR",0)
        bc = pct_color(p); bg = "#d1fae5" if p>=100 else "#fef3c7" if p>=80 else "#fee2e2"
        fg = "#065f46" if p>=100 else "#92400e" if p>=80 else "#991b1b"
        dm_cols[i].markdown(f"""
        <div style="background:#fff;border:1px solid #e8edf5;border-radius:14px;padding:1.1rem 1.2rem;
                    box-shadow:0 2px 8px rgba(0,0,0,0.05);border-top:3px solid {bc}">
          <div style="font-size:.85rem;font-weight:700;color:#1e293b;margin-bottom:8px">👤 {dm_name}</div>
          <div style="font-size:.72rem;color:#94a3b8">Target</div>
          <div style="font-size:1rem;font-weight:700;color:#1e293b">{fmt_lkr(t)}</div>
          <div style="background:#f1f5f9;border-radius:999px;height:5px;margin:5px 0">
            <div style="width:{min((t/max(t,a,1))*100,100):.1f}%;height:100%;background:#3b82f6;border-radius:999px"></div></div>
          <div style="font-size:.72rem;color:#94a3b8">Achievement</div>
          <div style="font-size:1rem;font-weight:700;color:{bc}">{fmt_lkr(a)}</div>
          <div style="background:#f1f5f9;border-radius:999px;height:5px;margin:5px 0">
            <div style="width:{min(p,100):.1f}%;height:100%;background:{bc};border-radius:999px"></div></div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px">
            <div style="font-size:.72rem;color:{'#059669' if v>=0 else '#dc2626'}">{"+" if v>=0 else ""}{fmt_lkr(v)}</div>
            <span style="font-size:.75rem;font-weight:800;padding:3px 10px;border-radius:999px;background:{bg};color:{fg}">{p:.1f}%</span>
          </div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section(f"DM → RP HIERARCHY — {dm_sel_m} (LKR)")
    filtered_drm = {k:v for k,v in dm_drm.items() if dm_filter=="ALL" or k==dm_filter}
    filtered_drm = {d:[r for r in rps if dm_lkr.get(r,{}).get("TAR_LKR",0)!=0 or dm_lkr.get(r,{}).get("ACH_LKR",0)!=0]
                    for d,rps in filtered_drm.items()
                    if dm_lkr.get(d,{}).get("TAR_LKR",0)!=0 or dm_lkr.get(d,{}).get("ACH_LKR",0)!=0}
    render_dm_hierarchy(filtered_drm, dm_lkr, fmt_fn=fmt_lkr, label="LKR")

# ╔══════════════════╗
# ║ TAB: RP DETAIL  ║
# ╚══════════════════╝
with tab_rp:
    rp_sel_m = st.selectbox("Month",month_list,index=month_list.index(sel_month),key="rp_m")
    rp_lkr   = all_lkr[rp_sel_m]
    rp_units = all_units[rp_sel_m]
    rp_drm   = all_dm_rp[rp_sel_m]
    rp_eo    = all_eo[rp_sel_m]

    rp_to_dm = {rp: dm for dm, rps in rp_drm.items() for rp in rps}
    all_reps = [e for e in rp_eo if e != 'TOTAL' and not is_dm(e)]
    disp_reps = all_reps if dm_filter == "ALL" else [r for r in all_reps if rp_to_dm.get(r)==dm_filter]
    disp_reps = [r for r in disp_reps if rp_lkr.get(r,{}).get("TAR_LKR",0)>0 or rp_units.get(r,{}).get("TAR",0)>0]

    section(f"SALES REP PERFORMANCE — {rp_sel_m}")
    if not disp_reps:
        st.info("Filter ට ගැලපෙන rep data නැත.")
    else:
        achievement_rows_ui(
            [dict(name=r, TAR=rp_lkr.get(r,{}).get('TAR_LKR',0),
                  ACH=rp_lkr.get(r,{}).get('ACH_LKR',0), PCT=rp_lkr.get(r,{}).get('PCT_LKR',0))
             for r in disp_reps if rp_lkr.get(r,{}).get('TAR_LKR',0)>0], fmt_fn=fmt_lkr)

        rp_tbl = [{"Rep":r,"Under DM":rp_to_dm.get(r,"—"),
                   "Target LKR":round(rp_lkr.get(r,{}).get('TAR_LKR',0)),
                   "Achievement LKR":round(rp_lkr.get(r,{}).get('ACH_LKR',0)),
                   "LKR Ach%":round(rp_lkr.get(r,{}).get('PCT_LKR',0),1),
                   "LKR Variance":round(rp_lkr.get(r,{}).get('VAR_LKR',0)),
                   "Target Units":round(rp_units.get(r,{}).get('TAR',0)),
                   "Achievement Units":round(rp_units.get(r,{}).get('ACH',0)),
                   "Unit Ach%":round(rp_units.get(r,{}).get('PCT',0),1)} for r in disp_reps]
        if rp_tbl:
            rp_df = pd.DataFrame(rp_tbl)
            st.dataframe(rp_df.style.format({
                "Target LKR":"{:,.0f}","Achievement LKR":"{:,.0f}","LKR Ach%":"{:.1f}%",
                "LKR Variance":"{:+,.0f}","Target Units":"{:,.0f}","Achievement Units":"{:,.0f}","Unit Ach%":"{:.1f}%"}),
                use_container_width=True, hide_index=True)
            st.download_button("⬇️ Export CSV",data=rp_df.to_csv(index=False).encode("utf-8"),
                file_name=f"{dash_title}_reps_{rp_sel_m}.csv",mime="text/csv")

# ╔══════════════════╗
# ║ TAB: PRODUCTS   ║
# ╚══════════════════╝
with tab_prod:
    section(f"PRODUCT BREAKDOWN — {sel_month}")
    if prd.empty:
        st.info("Product data නැත.")
    else:
        ent_opts = ["ALL"] + sorted(prd["ENTITY"].unique().tolist())
        sel_ent = st.selectbox("Entity Filter", ent_opts, key="prod_ent")
        prd_f = (prd if sel_ent == "ALL" else prd[prd["ENTITY"] == sel_ent]).copy()
        prd_f = prd_f[prd_f["TAR"] > 0]

        if not prd_f.empty:
            prod_sum = prd_f.groupby("PRODUCT").agg(TAR=("TAR","sum"),ACH=("ACH","sum")).reset_index()
            prod_sum["PCT"] = prod_sum.apply(lambda r: r["ACH"]/r["TAR"]*100 if r["TAR"]>0 else 0, axis=1)
            prod_sum = prod_sum.sort_values("TAR", ascending=False)

            p1,p2,p3,p4 = st.columns(4)
            kpi_card(p1,"Products",str(prod_sum["PRODUCT"].nunique()),"📦","c-blue")
            kpi_card(p2,"Total Unit Target",fmt_n(prod_sum["TAR"].sum()),"🎯","c-indigo")
            kpi_card(p3,"Total Unit Achievement",fmt_n(prod_sum["ACH"].sum()),"✅","c-green")
            best_p = prod_sum.loc[prod_sum["PCT"].idxmax(),"PRODUCT"]
            kpi_card(p4,"Best Product",best_p,"🏆","c-amber",
                     badge_text=f"{prod_sum['PCT'].max():.1f}%",badge_cls="up")

            st.markdown("<br>", unsafe_allow_html=True)
            cp1,cp2 = st.columns(2)
            with cp1:
                st.markdown('<div class="card"><div class="card-title">Unit TAR vs ACH by Product</div>', unsafe_allow_html=True)
                fig_pb = go.Figure()
                fig_pb.add_trace(go.Bar(name="Target",x=prod_sum["PRODUCT"],y=prod_sum["TAR"],
                    marker=dict(color="#93c5fd",line=dict(width=0)),width=0.4,offset=-0.2))
                fig_pb.add_trace(go.Bar(name="Achievement",x=prod_sum["PRODUCT"],y=prod_sum["ACH"],
                    marker=dict(color=[pct_color(p) for p in prod_sum["PCT"]],opacity=.9,line=dict(width=0)),
                    width=0.4,offset=0.1,text=[f"{p:.1f}%" for p in prod_sum["PCT"]],textposition="outside"))
                fig_pb.update_layout(**PLOTLY_BASE,barmode="overlay",height=320,
                    margin=dict(t=10,b=80,l=60,r=10),
                    xaxis=dict(tickangle=-35,tickfont=dict(size=10,color="#64748b"),showgrid=False),
                    yaxis=dict(gridcolor="#f1f5f9",title="Units"),
                    legend=dict(orientation="h",y=1.05,bgcolor="rgba(0,0,0,0)"))
                st.plotly_chart(fig_pb,use_container_width=True,config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

            with cp2:
                st.markdown('<div class="card"><div class="card-title">Achievement % by Product</div>', unsafe_allow_html=True)
                ps = prod_sum.sort_values("PCT",ascending=True)
                fig_h = go.Figure(go.Bar(y=ps["PRODUCT"],x=ps["PCT"],orientation="h",
                    marker=dict(color=[pct_color(p) for p in ps["PCT"]],opacity=.85,line=dict(width=0)),
                    text=[f"{p:.1f}%" for p in ps["PCT"]],textposition="outside"))
                fig_h.add_vline(x=100,line_color="#22c55e",line_dash="dot",line_width=1.5)
                fig_h.update_layout(**PLOTLY_BASE,height=320,
                    margin=dict(t=10,b=40,l=160,r=60),
                    xaxis=dict(gridcolor="#f1f5f9",ticksuffix="%"),
                    yaxis=dict(tickfont=dict(size=10,color="#64748b")))
                st.plotly_chart(fig_h,use_container_width=True,config={"displayModeBar":False})
                st.markdown('</div>', unsafe_allow_html=True)

            section("PRODUCT DETAIL TABLE")
            prod_tbl = prod_sum[["PRODUCT","TAR","ACH","PCT"]].copy()
            prod_tbl.columns = ["Product","Target (units)","Achievement (units)","Unit Ach %"]
            prod_tbl["Variance"] = prod_tbl["Achievement (units)"] - prod_tbl["Target (units)"]
            st.dataframe(prod_tbl.style.format({
                "Target (units)":"{:,.0f}","Achievement (units)":"{:,.0f}",
                "Unit Ach %":"{:.1f}%","Variance":"{:+,.0f}"}),
                use_container_width=True,hide_index=True)

# ╔════════════════════╗
# ║ TAB: LKR TREND    ║
# ╚════════════════════╝
with tab_trend:
    section("LKR ACHIEVEMENT TREND — ALL MONTHS")
    view = st.selectbox("View",["Division TOTAL","Each DM","Each RP/Rep"],key="trend_view")
    trend_rows = []
    for m in month_list:
        for e in all_eo[m]:
            d = all_lkr[m].get(e,{})
            if not d.get('TAR_LKR'): continue
            if view=="Division TOTAL" and e!="TOTAL": continue
            if view=="Each DM" and not is_dm(e): continue
            if view=="Each RP/Rep" and (is_dm(e) or e=="TOTAL"): continue
            trend_rows.append(dict(Month=m,Entity=e,TAR_LKR=d['TAR_LKR'],
                                   ACH_LKR=d['ACH_LKR'],PCT_LKR=d['PCT_LKR']))
    if trend_rows:
        tr_df = pd.DataFrame(trend_rows)
        col_t1,col_t2 = st.columns(2)
        with col_t1:
            fig_l = px.line(tr_df,x="Month",y="ACH_LKR",color="Entity",markers=True,
                color_discrete_sequence=PALETTE,labels={"ACH_LKR":"Achievement (LKR)"})
            fig_l.update_layout(**PLOTLY_BASE,height=320,margin=dict(t=10,b=40,l=80,r=20),
                legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.05,xanchor="right",x=1),
                xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
                yaxis=dict(gridcolor="#f1f5f9",title="LKR"))
            st.plotly_chart(fig_l,use_container_width=True,config={"displayModeBar":False})
        with col_t2:
            fig_p = px.line(tr_df,x="Month",y="PCT_LKR",color="Entity",markers=True,
                color_discrete_sequence=PALETTE,labels={"PCT_LKR":"LKR Ach %"})
            fig_p.add_hline(y=100,line_color="#22c55e",line_dash="dot",line_width=1.5)
            fig_p.update_layout(**PLOTLY_BASE,height=320,margin=dict(t=10,b=40,l=60,r=20),
                legend=dict(bgcolor="rgba(0,0,0,0)",orientation="h",y=1.05,xanchor="right",x=1),
                xaxis=dict(tickfont=dict(size=11,color="#64748b"),showgrid=False),
                yaxis=dict(gridcolor="#f1f5f9",title="LKR Ach %",ticksuffix="%"))
            st.plotly_chart(fig_p,use_container_width=True,config={"displayModeBar":False})

        section("FULL LKR TABLE")
        ft = tr_df.rename(columns={"TAR_LKR":"Target (LKR)","ACH_LKR":"Achievement (LKR)","PCT_LKR":"Ach %"})
        st.dataframe(ft.style.format({"Target (LKR)":"LKR {:,.0f}","Achievement (LKR)":"LKR {:,.0f}","Ach %":"{:.1f}%"}),
            use_container_width=True,hide_index=True)
        st.download_button("⬇️ Export CSV",data=ft.to_csv(index=False).encode("utf-8"),
            file_name=f"{dash_title}_lkr_trend.csv",mime="text/csv")

st.markdown(f'<div class="dash-footer">Universal Sales Intelligence Hub · {dash_title} · {sel_month} · v12.0</div>',
            unsafe_allow_html=True)
