"""Global CSS injection for SUCHNA AI — premium dark theme only."""

from pydoc import text

from ui.theme import get_theme_tokens


def build_stylesheet(logged_in=True):
    """Builds the full CSS string for the premium dark theme."""
    t = get_theme_tokens()
    if logged_in:
        sidebar_rules = """
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        transform: translateX(0) !important;
        min-width: 18rem !important;
        width: 18rem !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        width: 100% !important;
    }
    [data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: 0 !important;
        transform: translateX(0) !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
        """
    else:
        sidebar_rules = """
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="stAppViewContainer"] > .main {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
    }
    .main .block-container {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
        max-width: 560px !important;
        padding: 2rem 1.25rem !important;
    }
        """
    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {{
        --bg: {t['bg']};
        --sidebar: {t['sidebar']};
        --card: {t['card']};
        --card-glass: {t['card_glass']};
        --border: {t['border']};
        --border-hover: {t['border_hover']};
        --primary: {t['primary']};
        --secondary: {t['secondary']};
        --accent: {t['accent']};
        --success: {t['success']};
        --warning: {t['warning']};
        --danger: {t['danger']};
        --text: {t['text']};
        --text-muted: {t['text_muted']};
        --text-subtle: {t['text_subtle']};
        --shadow: {t['shadow']};
        --shadow-lg: {t['shadow_lg']};
        --shadow-glow: {t['shadow_glow']};
        --primary-soft: rgba(139, 92, 246, 0.15);
        --primary-glow: rgba(139, 92, 246, 0.35);
        --radius-sm: 10px;
        --radius-md: 14px;
        --radius-lg: 18px;
        --radius-xl: 24px;
    }}

    * {{ box-sizing: border-box; }}

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    .stApp {{
        background: {t['app_gradient']};
        background-attachment: fixed;
        color: var(--text);
    }}

    #MainMenu, footer, header[data-testid="stHeader"] {{
        visibility: hidden;
        height: 0;
    }}

    {sidebar_rules}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: {t['sidebar']} !important;
        border-right: 1px solid var(--border) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3);
    }}

    [data-testid="stSidebar"] > div:first-child {{
        padding: 1.75rem 1rem 2rem !important;
    }}

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        gap: 0.35rem;
    }}

    .block-container {{
        padding-top: 0.75rem;
        padding-bottom: 3rem;
        max-width: 1320px;
    }}

    /* ── Auth Page ── */
   .auth-page {{
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 0;
    margin: 0;
}}
.auth-hero {{
    text-align: center;
    margin-bottom: 1.25rem;
    animation: fadeUp 0.7s cubic-bezier(0.16, 1, 0.3, 1);

    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}}
    .auth-brand {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: {t['hero_gradient']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.6rem;
        letter-spacing: -0.04em;
        line-height: 1.1;
    }}
    .auth-tagline {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.45rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 0.4rem;
        letter-spacing: -0.02em;
    }}
    .auth-sub {{
        color: var(--text-muted);
        font-size: 1.05rem;
        margin-bottom: 1.75rem;
    }}
    .feature-badges {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        justify-content: center;
        margin-top: 0.5rem;
    }}
    .feature-badge {{
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.4rem 0.95rem;
        border-radius: 999px;
        background: rgba(139, 92, 246, 0.12);
        color: #C4B5FD;
        border: 1px solid rgba(139, 92, 246, 0.28);
        transition: transform 0.25s ease, border-color 0.25s ease, background 0.25s ease;
        letter-spacing: 0.02em;
    }}
    .feature-badge:hover {{
        transform: translateY(-2px);
        border-color: var(--primary);
        background: rgba(139, 92, 246, 0.22);
    }}
    .auth-card {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        -webkit-backdrop-filter: {t['glass_blur']};
        border: 1px solid var(--border);
        border-radius: var(--radius-xl);
       padding: 1.75rem 2rem;
        box-shadow: var(--shadow-lg);
        max-width: 700px;
        width: 100%;
        margin: 0 auto;
        animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.1s both;
    }}

    /* ── Sidebar Brand ── */
    .sidebar-brand {{
        padding: 0 0.65rem 1.5rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.25rem;
    }}
    .sidebar-brand-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
        font-weight: 800;
        background: {t['hero_gradient']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.03em;
    }}
    .sidebar-brand-tag {{
        font-size: 0.75rem;
        color: var(--text-muted);
        margin: 0.35rem 0 0;
        font-weight: 500;
    }}
    .nav-label {{
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--text-subtle);
        padding: 0.75rem 0.65rem 0.5rem;
        margin: 0;
    }}
    .profile-card {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem 1.1rem;
        margin-top: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.85rem;
        transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }}
    .profile-card:hover {{
        border-color: var(--border-hover);
        box-shadow: var(--shadow-glow);
    }}
    .profile-avatar {{
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: {t['nav_active']};
        border: 1px solid rgba(139, 92, 246, 0.35);
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        color: #C4B5FD;
        flex-shrink: 0;
    }}
    .profile-info {{ flex: 1; min-width: 0; }}
    .profile-name {{
        font-weight: 700;
        font-size: 0.92rem;
        color: var(--text);
        margin: 0 0 0.1rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .profile-role {{
        font-size: 0.72rem;
        color: var(--text-muted);
        text-transform: capitalize;
        margin: 0;
        font-weight: 500;
    }}
    .sidebar-divider {{
        height: 1px;
        background: var(--border);
        margin: 1.25rem 0.65rem;
    }}

    /* ── Sidebar Nav Radio ── */
    [data-testid="stSidebar"] div[data-testid="stRadio"] > div {{
        gap: 0.2rem !important;
        flex-direction: column !important;
    }}
    [data-testid="stSidebar"] div[data-testid="stRadio"] label {{
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.65rem 0.85rem !important;
        margin: 0 !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        color: var(--text-muted) !important;
        transition: all 0.22s ease !important;
        width: 100%;
    }}
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
        background: rgba(139, 92, 246, 0.08) !important;
        color: var(--text) !important;
        border-color: rgba(139, 92, 246, 0.15) !important;
        transform: translateX(3px);
    }}
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"],
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {{
        background: {t['nav_active']} !important;
        border-color: rgba(139, 92, 246, 0.35) !important;
        color: var(--text) !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 12px rgba(139, 92, 246, 0.15);
    }}
    [data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child {{
        display: none !important;
    }}

    /* ── Top Navbar ── */
    .top-nav-shell {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        -webkit-backdrop-filter: {t['glass_blur']};
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 0.55rem 1rem 0.55rem 1.25rem;
        margin-bottom: 1.75rem;
        box-shadow: var(--shadow);
    }}
    .nav-search-wrap {{
        position: relative;
    }}
    .nav-icon-btn {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: var(--radius-sm);
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid var(--border);
        font-size: 1.15rem;
        cursor: default;
        transition: border-color 0.22s ease, background 0.22s ease, transform 0.22s ease;
        position: relative;
    }}
    .nav-icon-btn:hover {{
        border-color: var(--border-hover);
        background: rgba(139, 92, 246, 0.1);
        transform: scale(1.04);
    }}
    .notif-badge {{
        position: absolute;
        top: -4px;
        right: -4px;
        min-width: 18px;
        height: 18px;
        padding: 0 5px;
        border-radius: 999px;
        background: linear-gradient(135deg, var(--accent), var(--primary));
        color: white;
        font-size: 0.62rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid {t['sidebar']};
    }}
    .nav-user-chip {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.35rem 0.75rem 0.35rem 0.35rem;
        border-radius: var(--radius-sm);
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid var(--border);
        transition: border-color 0.22s ease;
    }}
    .nav-user-chip:hover {{
        border-color: var(--border-hover);
    }}
    .nav-user-avatar {{
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: {t['nav_active']};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.78rem;
        font-weight: 700;
        color: #C4B5FD;
    }}

    /* ── Hero ── */
    .welcome-hero {{
        background: {t['hero_mesh']};
        padding: 2.75rem 3rem;
        border-radius: var(--radius-xl);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg), 0 0 80px rgba(139, 92, 246, 0.2);
        position: relative;
        overflow: hidden;
        animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        border: 1px solid rgba(139, 92, 246, 0.25);
    }}
    .welcome-hero::before {{
        content: '';
        position: absolute;
        inset: 0;
        background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
        pointer-events: none;
        opacity: 0.5;
    }}
    .welcome-hero::after {{
        content: '';
        position: absolute;
        top: -60%;
        right: -15%;
        width: 55%;
        height: 220%;
        background: linear-gradient(135deg, rgba(255,255,255,0.08), transparent);
        transform: rotate(20deg);
        pointer-events: none;
    }}
    .welcome-hero > * {{ position: relative; z-index: 1; }}
    .welcome-greeting {{
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.75);
        margin-bottom: 0.5rem;
        font-weight: 500;
        letter-spacing: 0.01em;
    }}
    .welcome-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.75rem;
        font-weight: 800;
        color: white;
        margin: 0 0 0.35rem;
        letter-spacing: -0.04em;
        line-height: 1.1;
        text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
    }}
    .welcome-tagline {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.95);
        margin: 0 0 0.25rem;
        font-weight: 600;
        letter-spacing: -0.01em;
    }}
    .welcome-subtitle {{
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.65);
        margin: 0 0 1.35rem;
        font-weight: 400;
    }}
    .welcome-features {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
    }}
    .welcome-feature {{
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.38rem 0.9rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        transition: transform 0.22s ease, background 0.22s ease;
        letter-spacing: 0.02em;
    }}
    .welcome-feature:hover {{
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.18);
    }}

    /* ── Stats ── */
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.15rem;
        margin-bottom: 2rem;
    }}
    @media (max-width: 960px) {{ .stats-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 520px) {{ .stats-grid {{ grid-template-columns: 1fr; }} }}

    .stat-card {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        -webkit-backdrop-filter: {t['glass_blur']};
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem 1.6rem;
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1),
                    box-shadow 0.3s ease, border-color 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    .stat-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
        opacity: 0.85;
    }}
    .stat-card-1::before {{ background: linear-gradient(90deg, var(--primary), var(--secondary)); }}
    .stat-card-2::before {{ background: linear-gradient(90deg, var(--accent), var(--primary)); }}
    .stat-card-3::before {{ background: linear-gradient(90deg, var(--secondary), var(--success)); }}
    .stat-card-4::before {{ background: linear-gradient(90deg, var(--warning), var(--accent)); }}
    .stat-card:hover {{
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg), var(--shadow-glow);
        border-color: var(--border-hover);
    }}
    .stat-card-1 {{ background: {t['stat_grad_1']}; }}
    .stat-card-2 {{ background: {t['stat_grad_2']}; }}
    .stat-card-3 {{ background: {t['stat_grad_3']}; }}
    .stat-card-4 {{ background: {t['stat_grad_4']}; }}
    .stat-icon {{
        font-size: 1.75rem;
        margin-bottom: 0.75rem;
        filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.3));
    }}
    .stat-label {{
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
    }}
    .stat-value {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.75rem;
        font-weight: 800;
        line-height: 1;
        color: var(--text);
        letter-spacing: -0.03em;
    }}

    /* ── Page headers ── */
    .page-header {{
        margin-bottom: 1.75rem;
        animation: fadeUp 0.5s ease;
    }}
    .page-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        margin: 0 0 0.4rem;
        letter-spacing: -0.03em;
        color: var(--text);
    }}
    .page-subtitle {{
        color: var(--text-muted);
        font-size: 1rem;
        margin: 0;
        line-height: 1.6;
        max-width: 640px;
    }}

    /* ── Section titles ── */
    .section-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 2rem 0 1.25rem;
        gap: 1rem;
    }}
    .section-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0;
        color: var(--text);
        letter-spacing: -0.02em;
    }}
    .section-badge {{
        font-size: 0.68rem;
        font-weight: 700;
        padding: 0.3rem 0.75rem;
        border-radius: 999px;
        background: var(--primary-soft);
        color: #C4B5FD;
        border: 1px solid rgba(139, 92, 246, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    .priority-section-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.55rem;
        font-weight: 800;
        background: linear-gradient(90deg, #F59E0B, #EF4444, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1.75rem 0 1.25rem;
        letter-spacing: -0.02em;
    }}

    /* ── Search ── */
    .search-panel {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow);
    }}
    .search-panel-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.4rem;
    }}
    .search-hint {{
        font-size: 0.82rem;
        color: var(--text-subtle);
        margin-bottom: 1rem;
        line-height: 1.5;
    }}
    .search-scope-tags {{ display: flex; flex-wrap: wrap; gap: 0.45rem; }}
    .search-scope-tag {{
        font-size: 0.68rem;
        font-weight: 600;
        padding: 0.28rem 0.65rem;
        border-radius: 999px;
        background: rgba(59, 130, 246, 0.12);
        color: #93C5FD;
        border: 1px solid rgba(59, 130, 246, 0.25);
    }}
    .search-results-bar {{
        font-size: 0.88rem;
        color: var(--text-muted);
        background: rgba(139, 92, 246, 0.08);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: var(--radius-sm);
        padding: 0.75rem 1.1rem;
        margin-bottom: 1.25rem;
    }}

    /* ── Notice cards ── */
    .glass-card {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        -webkit-backdrop-filter: {t['glass_blur']};
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1),
                    border-color 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }}
    .glass-card:hover {{
        transform: translateY(-5px);
        border-color: var(--border-hover);
        box-shadow: var(--shadow-lg), 0 0 30px rgba(139, 92, 246, 0.1);
    }}

    .priority-zone-card {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-left: 4px solid #F59E0B;
        border-radius: var(--radius-lg);
        padding: 1.75rem 2rem;
        margin-bottom: 1.15rem;
        box-shadow: var(--shadow), 0 0 24px rgba(245, 158, 11, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    .priority-zone-card::before {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, rgba(245, 158, 11, 0.12), transparent 70%);
        pointer-events: none;
    }}
    .priority-zone-card:hover {{
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg), 0 0 40px rgba(245, 158, 11, 0.12);
    }}
    .priority-zone-card.high-priority {{
        border-color: rgba(239, 68, 68, 0.4);
        border-left-color: var(--danger);
        box-shadow: var(--shadow), 0 0 32px rgba(239, 68, 68, 0.12);
    }}
    .priority-zone-card.high-priority::before {{
        background: radial-gradient(circle, rgba(239, 68, 68, 0.12), transparent 70%);
    }}
    .priority-zone-card.pinned-card {{
        border-color: rgba(139, 92, 246, 0.4);
        border-left-color: var(--primary);
        box-shadow: var(--shadow), 0 0 32px rgba(139, 92, 246, 0.15);
    }}

    .notice-card-header {{
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 0.5rem;
        margin-bottom: 0.85rem;
    }}
    .notice-meta-row {{ display: flex; flex-wrap: wrap; gap: 0.45rem; align-items: center; }}
    .notice-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0 0 0.65rem;
        line-height: 1.35;
        color: var(--text);
        letter-spacing: -0.02em;
    }}
    .priority-zone-card .notice-title {{
        font-size: 1.35rem;
    }}
    .notice-summary {{
        color: var(--text-muted);
        line-height: 1.65;
        margin: 0 0 1rem;
        font-size: 0.9rem;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }}
    .notice-footer {{
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        font-size: 0.78rem;
        color: var(--text-subtle);
        padding-top: 0.85rem;
        border-top: 1px solid var(--border);
    }}
    .notice-footer span {{
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }}

    /* ── Badges ── */
    .badge {{
        display: inline-block;
        padding: 0.28rem 0.65rem;
        border-radius: 999px;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .badge-exams {{ background: rgba(239,68,68,0.15); color: #FCA5A5; border: 1px solid rgba(239,68,68,0.35); }}
    .badge-placements {{ background: rgba(59,130,246,0.15); color: #93C5FD; border: 1px solid rgba(59,130,246,0.35); }}
    .badge-events {{ background: rgba(139,92,246,0.15); color: #C4B5FD; border: 1px solid rgba(139,92,246,0.35); }}
    .badge-assignments {{ background: rgba(245,158,11,0.15); color: #FCD34D; border: 1px solid rgba(245,158,11,0.35); }}
    .badge-workshops {{ background: rgba(16,185,129,0.15); color: #6EE7B7; border: 1px solid rgba(16,185,129,0.35); }}
    .badge-general {{ background: rgba(100,116,139,0.15); color: var(--text-muted); border: 1px solid var(--border); }}
    .priority-badge {{
        display: inline-block;
        padding: 0.28rem 0.65rem;
        border-radius: 999px;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .priority-badge-high {{ background: rgba(239,68,68,0.18); color: #FCA5A5; border: 1px solid rgba(239,68,68,0.4); }}
    .priority-badge-medium {{ background: rgba(245,158,11,0.18); color: #FCD34D; border: 1px solid rgba(245,158,11,0.4); }}
    .priority-badge-low {{ background: rgba(16,185,129,0.18); color: #6EE7B7; border: 1px solid rgba(16,185,129,0.4); }}
    .pin-badge {{
        display: inline-block;
        padding: 0.28rem 0.65rem;
        border-radius: 999px;
        font-size: 0.65rem;
        font-weight: 700;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.25), rgba(245, 158, 11, 0.2));
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.45);
        animation: pulseGlow 2.5s ease-in-out infinite;
    }}
    .match-badge {{
        display: inline-block;
        font-size: 0.62rem;
        font-weight: 700;
        padding: 0.2rem 0.5rem;
        border-radius: 999px;
        background: rgba(59,130,246,0.15);
        color: #93C5FD;
        border: 1px solid rgba(59,130,246,0.35);
    }}

    /* ── AI Assistant ── */
    .assistant-shell {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        border: 1px solid var(--border);
        border-radius: var(--radius-xl);
        overflow: hidden;
        box-shadow: var(--shadow-lg);
        margin-bottom: 1.25rem;
    }}
    .assistant-header-bar {{
        padding: 1.25rem 1.75rem;
        background: {t['nav_active']};
        border-bottom: 1px solid var(--border);
    }}
    .assistant-header-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text);
        margin: 0;
    }}
    .assistant-header-sub {{
        font-size: 0.82rem;
        color: var(--text-muted);
        margin: 0.25rem 0 0;
    }}
    .chat-container {{
        padding: 1.75rem;
        min-height: 340px;
        max-height: 480px;
        overflow-y: auto;
    }}
    .chat-empty-state {{
        text-align: center;
        padding: 3rem 2rem;
        color: var(--text-muted);
    }}
    .chat-empty-icon {{
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        opacity: 0.8;
    }}
    .chat-empty-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 0.35rem;
    }}
    .chat-bubble-user {{
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.22), rgba(59, 130, 246, 0.15));
        border: 1px solid rgba(139, 92, 246, 0.35);
        border-radius: 18px 18px 4px 18px;
        padding: 14px 18px;
        margin-left: 15%;
        margin-bottom: 14px;
        color: var(--text);
        animation: fadeUp 0.3s ease;
    }}
    .chat-bubble-bot {{
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid var(--border);
        border-radius: 18px 18px 18px 4px;
        padding: 14px 18px;
        margin-right: 15%;
        margin-bottom: 14px;
        color: var(--text);
        animation: fadeUp 0.3s ease;
    }}
    .chat-bubble-label {{
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-muted);
        margin-bottom: 0.35rem;
    }}
    .prompts-section {{
        margin: 1.25rem 0;
    }}
    .prompts-label {{
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-subtle);
        margin-bottom: 0.65rem;
    }}

    /* ── Recommendations ── */
    .rec-featured {{
        background: {t['hero_mesh']};
        border-radius: var(--radius-xl);
        padding: 2.25rem 2.5rem;
        margin-bottom: 1.75rem;
        box-shadow: var(--shadow-lg), 0 0 60px rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.3);
        position: relative;
        overflow: hidden;
    }}
    .rec-featured::after {{
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 50%;
        height: 200%;
        background: rgba(255,255,255,0.04);
        transform: rotate(15deg);
        pointer-events: none;
    }}
    .rec-featured > * {{ position: relative; z-index: 1; }}
    .rec-featured h2 {{
        font-family: 'Space Grotesk', sans-serif;
        color: white;
        font-weight: 800;
        font-size: 1.65rem;
        margin: 0.65rem 0 0.5rem;
        letter-spacing: -0.02em;
    }}
    .rec-featured p {{
        color: rgba(255,255,255,0.85);
        margin: 0;
        line-height: 1.65;
        font-size: 0.95rem;
    }}
    .rec-top-badge {{
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 0.35rem 0.85rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.15);
        color: white;
        border: 1px solid rgba(255,255,255,0.25);
        letter-spacing: 0.04em;
    }}
    .rec-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.15rem;
    }}
    @media (max-width: 768px) {{ .rec-grid {{ grid-template-columns: 1fr; }} }}
    .rec-card {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }}
    .rec-card:hover {{
        transform: translateY(-4px);
        border-color: var(--border-hover);
        box-shadow: var(--shadow-glow);
    }}

    /* ── Admin & Upload ── */
    .admin-manage-card {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.4rem;
        margin-bottom: 0.85rem;
        transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
    }}
    .admin-manage-card:hover {{
        border-color: var(--border-hover);
        transform: translateY(-2px);
        box-shadow: var(--shadow-glow);
    }}
    .admin-manage-card.pinned {{
        border-left: 4px solid var(--primary);
    }}
    .admin-manage-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.08rem;
        font-weight: 700;
        margin: 0 0 0.45rem;
        color: var(--text);
    }}
    .admin-manage-summary {{
        color: var(--text-muted);
        font-size: 0.88rem;
        line-height: 1.6;
        margin: 0 0 0.7rem;
    }}
    .admin-manage-meta {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.85rem;
        font-size: 0.76rem;
        color: var(--text-subtle);
    }}
    .upload-panel {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        box-shadow: var(--shadow);
    }}
    .settings-card {{
        background: {t['card_glass']};
        backdrop-filter: {t['glass_blur']};
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.25rem;
    }}
    .settings-row {{
        display: flex;
        justify-content: space-between;
        padding: 0.65rem 0;
        border-bottom: 1px solid var(--border);
        font-size: 0.9rem;
    }}
    .settings-row:last-child {{ border-bottom: none; }}
    .settings-label {{ color: var(--text-muted); font-weight: 500; }}
    .settings-value {{ color: var(--text); font-weight: 600; }}

    /* ── Empty states ── */
    .empty-state {{
        text-align: center;
        padding: 3rem 2rem;
        background: {t['card_glass']};
        border: 1px dashed var(--border);
        border-radius: var(--radius-lg);
        color: var(--text-muted);
    }}
    .empty-state-icon {{ font-size: 2.5rem; margin-bottom: 0.75rem; opacity: 0.7; }}

    /* ── Streamlit widget overrides ── */
    .stTextInput input, .stTextArea textarea {{
        background: {t['input_bg']} !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text) !important;
        font-size: 0.9rem !important;
        transition: border-color 0.22s ease, box-shadow 0.22s ease !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.18) !important;
    }}
    .stTextInput input::placeholder {{
        color: var(--text-subtle) !important;
    }}

    div[data-testid="stRadio"]:not([data-testid="stSidebar"] *) > div {{
        gap: 0.35rem;
    }}
    div[data-testid="stRadio"]:not([data-testid="stSidebar"] *) label {{
        background: transparent;
        border-radius: var(--radius-sm);
        padding: 0.5rem 0.85rem !important;
        transition: background 0.22s ease;
        font-weight: 500 !important;
    }}
    div[data-testid="stRadio"]:not([data-testid="stSidebar"] *) label:hover {{
        background: var(--primary-soft);
    }}

    .stButton > button {{
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease !important;
        border: 1px solid var(--border) !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }}
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.35) !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        box-shadow: 0 6px 28px rgba(139, 92, 246, 0.45) !important;
    }}

    [data-testid="stExpander"] {{
        background: rgba(17, 24, 39, 0.5) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }}

    [data-testid="stSelectbox"] > div > div {{
        background: {t['input_bg']} !important;
        border-color: var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }}

    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(16px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.3); }}
        50% {{ box-shadow: 0 0 12px 2px rgba(245, 158, 11, 0.2); }}
    }}
</style>
"""


def inject_styles(logged_in=True):
    """Inject global stylesheet via Streamlit markdown."""
    import streamlit as st
    st.markdown(build_stylesheet(logged_in), unsafe_allow_html=True)
