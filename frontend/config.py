import streamlit as st

API_URL = "http://127.0.0.1:8000"

# Colours
GOLD           = "#E9C46A"
GOLD_DIM       = "#C9A44A"
BG_BASE        = "#080808"
BG_SURFACE     = "#101010"
BG_RAISED      = "#171717"
BG_HOVER       = "#1e1e1e"
TEXT_PRIMARY   = "#f0f0f0"
TEXT_SECONDARY = "#888888"
TEXT_MUTED     = "#484848"
BORDER         = "rgba(255,255,255,0.07)"
BORDER_HOVER   = "rgba(255,255,255,0.13)"
SUCCESS        = "#52c48a"
DANGER         = "#e06060"
WARNING        = "#e0a060"
INFO           = "#6098e0"
PRIMARY        = GOLD


def page_setup(title="NitaRefund", layout="wide"):
    st.set_page_config(
        page_title=title,
        page_icon="💛",
        layout=layout,
        initial_sidebar_state="collapsed",
    )
    inject_css()


def require_auth():
    """Put this at the top of every protected page."""
    if not st.session_state.get("token"):
        st.switch_page("app.py")

def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif !important;
        background-color: {BG_BASE} !important;
        color: {TEXT_PRIMARY} !important;
    }}
    .stApp {{ background-color: {BG_BASE} !important; }}
    #MainMenu, footer, header {{ visibility: hidden !important; }}
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    [data-testid="collapsedControl"] {{ display: none !important; }}

    section[data-testid="stSidebar"] {{
        background-color: {BG_BASE} !important;
        border-right: 1px solid {BORDER} !important;
    }}

    .main .block-container {{
        padding: 2rem 2.5rem !important;
        max-width: 1260px !important;
    }}

    /* Stat cards */
    .pl-stat {{
        background: {BG_RAISED};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 18px 20px;
    }}
    .pl-stat.accent {{
        background: rgba(233,196,106,0.06);
        border-color: rgba(233,196,106,0.20);
    }}
    .pl-stat .stat-label {{
        font-size: 11px;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
    }}
    .pl-stat .stat-value {{
        font-size: 22px;
        font-family: 'DM Serif Display', Georgia, serif;
        letter-spacing: -0.02em;
        line-height: 1;
    }}
    .pl-stat.accent .stat-value {{ color: {GOLD}; }}
    .pl-stat .stat-sub {{
        font-size: 12px;
        color: {TEXT_MUTED};
        margin-top: 6px;
    }}

    /* Badges */
    .badge {{
        display: inline-flex;
        align-items: center;
        padding: 2px 9px;
        font-size: 11.5px;
        font-weight: 500;
        border-radius: 9999px;
        white-space: nowrap;
    }}
    .badge-pending               {{ background:rgba(224,160,96,0.10); color:{WARNING}; border:1px solid rgba(224,160,96,0.22); }}
    .badge-awaiting_confirmation {{ background:rgba(233,196,106,0.10); color:{GOLD};    border:1px solid rgba(233,196,106,0.22); }}
    .badge-approved              {{ background:rgba(96,152,224,0.10);  color:{INFO};    border:1px solid rgba(96,152,224,0.22); }}
    .badge-settled               {{ background:rgba(82,196,138,0.10);  color:{SUCCESS}; border:1px solid rgba(82,196,138,0.22); }}
    .badge-rejected              {{ background:rgba(224,96,96,0.10);   color:{DANGER};  border:1px solid rgba(224,96,96,0.22); }}
    .badge-cancelled             {{ background:rgba(120,120,120,0.10); color:#777;      border:1px solid rgba(120,120,120,0.22); }}
    .badge-disputed              {{ background:rgba(224,96,96,0.10);   color:{DANGER};  border:1px solid rgba(224,96,96,0.22); }}

    /* Trust badges */
    .trust-high {{ background:rgba(82,196,138,0.10);  color:{SUCCESS}; border:1px solid rgba(82,196,138,0.22);  border-radius:9999px; padding:2px 9px; font-size:11.5px; font-weight:500; }}
    .trust-mid  {{ background:rgba(233,196,106,0.10); color:{GOLD};    border:1px solid rgba(233,196,106,0.22); border-radius:9999px; padding:2px 9px; font-size:11.5px; font-weight:500; }}
    .trust-low  {{ background:rgba(224,96,96,0.10);   color:{DANGER};  border:1px solid rgba(224,96,96,0.22);   border-radius:9999px; padding:2px 9px; font-size:11.5px; font-weight:500; }}

    /* Buttons */
    .stButton > button {{
        background: {GOLD} !important;
        color: #0a0a0a !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
        width: 100% !important;
        transition: all 160ms ease !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(233,196,106,0.22) !important;
    }}
    .btn-ghost > button {{
        background: {BG_RAISED} !important;
        color: {TEXT_PRIMARY} !important;
        border: 1px solid {BORDER_HOVER} !important;
    }}
    .btn-danger > button {{
        background: rgba(224,96,96,0.12) !important;
        color: {DANGER} !important;
        border: 1px solid rgba(224,96,96,0.28) !important;
    }}

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > textarea {{
        background: {BG_RAISED} !important;
        border: 1px solid {BORDER} !important;
        color: {TEXT_PRIMARY} !important;
        border-radius: 9px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: rgba(233,196,106,0.40) !important;
        box-shadow: 0 0 0 3px rgba(233,196,106,0.07) !important;
    }}
    .stTextInput label, .stNumberInput label,
    .stTextArea label, .stSelectbox label {{
        font-size: 13px !important;
        font-weight: 500 !important;
        color: {TEXT_PRIMARY} !important;
    }}

    /* Selectbox */
    .stSelectbox > div > div {{
        background: {BG_RAISED} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 9px !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: transparent !important;
        border-bottom: 1px solid {BORDER} !important;
        gap: 0 !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        color: {TEXT_SECONDARY} !important;
        border-radius: 0 !important;
        padding: 10px 20px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: {TEXT_PRIMARY} !important;
        border-bottom: 2px solid {GOLD} !important;
    }}
    .stTabs [data-baseweb="tab-panel"] {{ padding: 0 !important; }}

    /* Expander */
    .streamlit-expanderHeader {{
        background: {BG_SURFACE} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        color: {TEXT_PRIMARY} !important;
        font-size: 14px !important;
    }}
    .streamlit-expanderContent {{
        background: {BG_SURFACE} !important;
        border: 1px solid {BORDER} !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 16px 20px !important;
    }}

    /* Alerts */
    .stSuccess, .stError, .stWarning, .stInfo {{
        border-radius: 9px !important;
    }}

    /* Page titles */
    .pl-title {{
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 30px;
        letter-spacing: -0.01em;
        line-height: 1.1;
        margin-bottom: 4px;
    }}
    .pl-subtitle {{
        font-size: 14px;
        color: {TEXT_SECONDARY};
        margin-bottom: 1.5rem;
    }}
    .pl-divider {{
        border: none;
        border-top: 1px solid {BORDER};
        margin: 1.25rem 0;
    }}

    ::-webkit-scrollbar       {{ width: 4px; height: 4px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: {BORDER_HOVER}; border-radius: 2px; }}
    </style>
    """, unsafe_allow_html=True)

def stat_card(label, value, sub="", accent=False):
    cls = "pl-stat accent" if accent else "pl-stat"
    sub_html = f'<div class="stat-sub">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div class="{cls}">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def trust_badge(score: float) -> str:
    s = round(score)
    if score >= 70:
        return f'<span class="trust-high">↑ {s}</span>'
    elif score >= 40:
        return f'<span class="trust-mid">◆ {s}</span>'
    else:
        return f'<span class="trust-low">↓ {s}</span>'


def status_badge(status: str) -> str:
    label = status.replace("_", " ").capitalize()
    return f'<span class="badge badge-{status}">{label}</span>'


def trust_color(score: float) -> str:
    if score >= 70:   return SUCCESS
    elif score >= 40: return GOLD
    else:             return DANGER


def trust_ring_svg(score: float, size: int = 120) -> str:
    stroke = 8
    r      = (size - stroke) / 2
    circ   = 2 * 3.14159 * r
    offset = circ - (score / 100) * circ
    color  = trust_color(score)
    label  = "Excellent" if score >= 70 else "Good" if score >= 50 else "Fair" if score >= 25 else "Poor"
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;gap:8px;">
      <div style="position:relative;width:{size}px;height:{size}px;">
        <svg width="{size}" height="{size}" style="transform:rotate(-90deg);">
          <circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none"
            stroke="{BORDER}" stroke-width="{stroke}"/>
          <circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none"
            stroke="{color}" stroke-width="{stroke}"
            stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}"
            stroke-linecap="round"/>
        </svg>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;
                    align-items:center;justify-content:center;">
          <span style="font-size:24px;font-weight:500;color:{color};
                       font-family:'DM Serif Display',Georgia,serif;line-height:1;">
            {score:.0f}
          </span>
          <span style="font-size:11px;color:{TEXT_MUTED};margin-top:2px;">/100</span>
        </div>
      </div>
      <span style="font-size:13px;font-weight:500;color:{color};">{label}</span>
    </div>
    """


def fmt(amount) -> str:
    amount = float(amount or 0)
    return f"KES {int(amount):,}" if amount == int(amount) else f"KES {amount:,.2f}"


def page_title(title: str, subtitle: str = ""):
    sub_html = f'<p class="pl-subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(f'<h1 class="pl-title">{title}</h1>{sub_html}', unsafe_allow_html=True)


def divider():
    st.markdown('<hr class="pl-divider">', unsafe_allow_html=True)