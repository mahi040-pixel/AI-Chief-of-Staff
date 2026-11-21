import streamlit as st

def apply_styles():

    st.markdown("""
    <style>

    /* APP BACKGROUND */
    .stApp {
        background: #F5F7FC;
        color: #202B45;
        font-family: Arial, sans-serif;
    }

    /* MAIN CONTENT */
    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: #17243B;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    /* SIDEBAR CODE BLOCKS */
    [data-testid="stSidebar"] [data-testid="stCodeBlock"] {
        background: #263954 !important;
        border: 1px solid #40516D;
        border-radius: 10px;
    }

    [data-testid="stSidebar"] [data-testid="stCodeBlock"] pre,
    [data-testid="stSidebar"] [data-testid="stCodeBlock"] code {
        color: #EAF0FF !important;
        white-space: pre-wrap !important;
        overflow-wrap: anywhere !important;
    }

    /* HEADINGS */
    h1 {
        color: #1D2B48 !important;
        font-weight: 750 !important;
    }

    h2, h3 {
        color: #263858 !important;
        font-weight: 700 !important;
    }

    /* BUTTONS */
    .stButton > button {
        background: white;
        color: #263858;
        border: 1px solid #DDE4F0;
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: #EEEAFE;
        color: #6548E8;
        border-color: #8C7CF5;
    }

    /* DASHBOARD CARDS */
    .dashboard-card {
        background: white;
        border: 1px solid #E7EAF2;
        border-radius: 16px;
        padding: 22px;
        min-height: 135px;
        box-shadow: 0 4px 15px rgba(30, 50, 90, 0.04);
    }

    .card-label {
        color: #78849A;
        font-size: 14px;
        font-weight: 600;
    }

    .card-value {
        color: #253653;
        font-size: 32px;
        font-weight: 750;
        margin-top: 12px;
    }

    .card-icon {
        font-size: 23px;
    }

    /* CHAT */
    [data-testid="stChatMessage"] {
        background: white;
        border: 1px solid #E9EDF5;
        border-radius: 14px;
        padding: 15px;
        margin-bottom: 12px;
    }

    [data-testid="stChatInput"] {
        border-radius: 14px;
    }

    /* ALERTS */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* DIVIDERS */
    hr {
        border-color: #E4E9F2;
    }
    /* Better sidebar typography */

[data-testid="stSidebar"] p {
    font-size: 14px;
    line-height: 1.6;
}

/* Metric cards */

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E5EAF3;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(30, 50, 90, 0.04);
}

/* Workspace spacing */

[data-testid="stHorizontalBlock"] {
    gap: 18px;
}

/* Better chat input */

[data-testid="stChatInput"] {
    border: 1px solid #DCE3F0;
    border-radius: 14px;
}
    </style>
    """, unsafe_allow_html=True)