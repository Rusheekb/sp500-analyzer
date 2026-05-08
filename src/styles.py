def load_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap');

.stApp { background-color: #0a0a0a; color: #e0e0e0; font-family: 'IBM Plex Sans', sans-serif; }

[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #ff6600; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p { color: #ff6600 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 12px !important; text-transform: uppercase; letter-spacing: 1px; }
[data-testid="stSidebar"] input { background-color: #1a1a1a !important; color: #ffffff !important; border: 1px solid #ff6600 !important; border-radius: 2px !important; font-family: 'IBM Plex Mono', monospace !important; }

/* Sidebar nav links */
[data-testid="stSidebarNav"] a { color: #888888 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 12px !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
[data-testid="stSidebarNav"] a:hover { color: #ff6600 !important; }
[data-testid="stSidebarNav"] [aria-selected="true"] { color: #ff6600 !important; }

/* ALL buttons — fix orange on orange */
.stButton button {
    background-color: #1a1a1a !important;
    color: #ff6600 !important;
    border: 1px solid #ff6600 !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
.stButton button:hover {
    background-color: #ff6600 !important;
    color: #000000 !important;
}

/* ALL buttons */
.stButton button {
    background-color: #1a1a1a !important;
    color: #ff6600 !important;
    border: 1px solid #ff6600 !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
.stButton button:hover {
    background-color: #ff6600 !important;
    color: #000000 !important;
}

/* Sidebar buttons specifically — black text on orange */
[data-testid="stSidebar"] .stButton > button {
    background-color: #ff6600 !important;
    color: #000000 !important;
    font-weight: 700 !important;
    border: none !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #ff8800 !important;
    color: #000000 !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background-color: #ff8800 !important;
}

h1 { color: #ff6600 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 24px !important; text-transform: uppercase !important; letter-spacing: 3px !important; border-bottom: 1px solid #ff6600; padding-bottom: 10px; }
h2, h3, h4 { color: #ff6600 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 13px !important; text-transform: uppercase !important; letter-spacing: 2px !important; }

hr { border-color: #222222 !important; }

.stTabs [data-baseweb="tab-list"] { background-color: #111111; border-bottom: 1px solid #ff6600; }
.stTabs [data-baseweb="tab"] { color: #888888 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
.stTabs [aria-selected="true"] { color: #ff6600 !important; border-bottom: 2px solid #ff6600 !important; }

.stSelectbox > div > div { background-color: #1a1a1a !important; border: 1px solid #333333 !important; color: #e0e0e0 !important; border-radius: 2px !important; }

[data-testid="stMetric"] { background-color: #111111; border: 1px solid #222222; padding: 10px; border-radius: 2px; }
[data-testid="stMetricLabel"] { color: #888888 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'IBM Plex Mono', monospace !important; }

.stSuccess { background-color: #0a1f0a !important; border-left: 3px solid #00ff88 !important; color: #00ff88 !important; }
.stError { background-color: #1f0a0a !important; border-left: 3px solid #ff4444 !important; }

/* Radio buttons */
.stRadio label { color: #888888 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 12px !important; text-transform: uppercase !important; }
.stRadio [data-checked="true"] label { color: #ff6600 !important; }

/* Slider */
.stSlider [data-baseweb="slider"] div { background-color: #ff6600 !important; }

/* Number input */
.stNumberInput input { background-color: #1a1a1a !important; color: #ffffff !important; border: 1px solid #333 !important; font-family: 'IBM Plex Mono', monospace !important; }

/* Expander */
.streamlit-expanderHeader { color: #ff6600 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 12px !important; text-transform: uppercase !important; background-color: #111111 !important; border: 1px solid #333 !important; }
</style>
"""