import streamlit as st
from config import (
    page_setup, GOLD, BG_SURFACE, BORDER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    trust_color,
)
import api

page_setup("NitaRefund · Sign In")
st.markdown("""
<style>
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"]  { display: none !important; }
</style>
""", unsafe_allow_html=True)

if st.session_state.get("token"):
    st.switch_page("pages/1_Dashboard.py")

@st.cache_data(ttl=60, show_spinner=False)
def load_leaderboard():
    return api.get_leaderboard()

board  = load_leaderboard()
MEDALS = ["🥇", "🥈", "🥉"]

def get_error(e) -> str:
    """Pull a readable message out of a requests HTTPError."""
    try:
        body = e.response.json()
        detail = body.get("detail", "An error occurred.")
        # Validation errors come back as a list of dicts
        if isinstance(detail, list):
            return detail[0].get("msg", str(detail))
        return str(detail)
    except Exception:
        return "Username or email already in use!!Try a different one"

left, right = st.columns([10, 11], gap="large")

# ═════════════════════════════════════════════════════════════
# LEFT
# ═════════════════════════════════════════════════════════════
with left:

    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'DM Serif Display',Georgia,serif;
                  font-size:40px;letter-spacing:-0.02em;
                  color:{GOLD};line-height:1;margin-bottom:6px;">
        NitaRefund
      </div>
      <div style="font-size:13px;color:{TEXT_SECONDARY};">
        A spreadsheet records. NitaRefund models.
      </div>
    </div>
    """, unsafe_allow_html=True)

    login_tab, reg_tab = st.tabs(["Login", "Register"])

    # ── LOGIN ─────────────────────────────────────────────────
    with login_tab:
        st.markdown(
            f'<p style="font-size:13px;color:{TEXT_SECONDARY};margin:12px 0 16px;">'
            'Use your username and password to sign in.</p>',
            unsafe_allow_html=True,
        )
        username = st.text_input("Username", key="li_user", placeholder="your_username")
        password = st.text_input("Password", key="li_pass",
                                 placeholder="••••••••", type="password")

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("Login", key="btn_login"):
            if not username or not password:
                st.error("Please fill in both fields.")
            else:
                with st.spinner(""):
                    try:
                        data = api.login(username, password)
                        st.session_state.token    = data["access_token"]
                        st.session_state.username = username
                        st.rerun()
                    except Exception as e:
                        st.error(get_error(e))

        # ── Forgot password lives here, under Login only ──────
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        with st.expander("Forgot password?"):
            fp_email = st.text_input("Your Email",      key="fp_email",
                                     placeholder="you@example.com")
            fp_ans   = st.text_input("Security Answer", key="fp_ans",
                                     placeholder="Your security answer")
            fp_new   = st.text_input("New Password",    key="fp_new",
                                     placeholder="••••••••", type="password")

            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

            if st.button("Reset Password", key="btn_reset"):
                if not all([fp_email, fp_ans, fp_new]):
                    st.error("All three fields are required.")
                else:
                    with st.spinner(""):
                        try:
                            api.reset_password(fp_email, fp_ans, fp_new)
                            st.success("Password reset. You can now log in.")
                        except Exception as e:
            
                            st.error(get_error(e))

    # ── REGISTER ──────────────────────────────────────────────
    with reg_tab:
        st.markdown(
            f'<p style="font-size:13px;color:{TEXT_SECONDARY};margin:12px 0 16px;">'
            'Create your account to start tracking transactions.</p>',
            unsafe_allow_html=True,
        )
        r_user  = st.text_input("Username", key="re_user",  placeholder="your_username")
        r_email = st.text_input("Email",    key="re_email", placeholder="you@example.com")
        r_pass  = st.text_input("Password", key="re_pass",
                                placeholder="••••••••", type="password")
        r_sec   = st.text_input("Security Answer", key="re_sec",
                                placeholder="Used for password reset",
                                help="e.g. your mother's maiden name")

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("Create Account", key="btn_register"):
            if not all([r_user, r_email, r_pass, r_sec]):
                st.error("Username, email , security answer and password are required.")
            else:
                with st.spinner(""):
                    try:
                        data = api.register(r_user, r_email, r_pass, r_sec)
                        st.session_state.token    = data["access_token"]
                        st.session_state.username = r_user
                        st.rerun()
                    except Exception as e:
                        st.error(get_error(e))




# ═════════════════════════════════════════════════════════════
# RIGHT — leaderboard
# ═════════════════════════════════════════════════════════════
with right:
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'DM Serif Display',Georgia,serif;
                  font-size:26px;letter-spacing:-0.01em;
                  color:{TEXT_PRIMARY};margin-bottom:4px;">
        Trust Leaderboard
      </div>
      <div style="font-size:13px;color:{TEXT_SECONDARY};">
        Top users ranked by peer trust score
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not board:
        st.markdown(
            f'<p style="color:{TEXT_MUTED};padding:2rem 0;">'
            'No data yet — be the first to transact.</p>',
            unsafe_allow_html=True,
        )
    else:
        rows_html = ""
        for i, entry in enumerate(board):
            score  = round(float(entry.get("score", 0)))
            uname  = entry.get("username", "—")
            tx_cnt = entry.get("transaction_count", 0)
            color  = trust_color(score)
            rank   = (f'<span style="font-size:20px">{MEDALS[i]}</span>'
                      if i < 3 else
                      f'<span style="font-size:13px;color:{TEXT_MUTED};">#{i+1}</span>')

            rows_html += f"""
            <div style="display:flex;align-items:center;gap:14px;padding:14px 18px;
                        margin-bottom:6px;background:{BG_SURFACE};
                        border:1px solid {BORDER};border-radius:12px;">
              <div style="width:32px;text-align:center;">{rank}</div>
              <div style="flex:1;min-width:0;">
                <div style="font-size:14px;font-weight:500;color:{TEXT_PRIMARY};">
                  {uname}
                </div>
                <div style="font-size:12px;color:{TEXT_MUTED};margin-top:2px;">
                  {tx_cnt} transaction{"s" if tx_cnt != 1 else ""}
                </div>
              </div>
              <div style="font-family:'DM Serif Display',Georgia,serif;
                          font-size:22px;color:{color};line-height:1;">
                {score}
              </div>
            </div>
            """
        st.markdown(rows_html, unsafe_allow_html=True)