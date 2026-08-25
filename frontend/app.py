import sys
from pathlib import Path
from html import escape

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from gateway.server import search_all_nodes


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EduShare | Distributed Learning",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            linear-gradient(
                180deg,
                #f7f9fc 0%,
                #eef3f9 100%
            );
        color: #172033;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    /* Hide Streamlit default decoration */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ========================================================
       TOP BRAND BAR
       ======================================================== */

    .brand-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;

        padding: 0.65rem 0 1.4rem 0;

        border-bottom: 1px solid #dbe3ee;

        margin-bottom: 1.6rem;
    }

    .brand-name {
        font-size: 1.05rem;
        font-weight: 800;
        color: #173b7a;
        letter-spacing: 0.2px;
    }

    .brand-label {
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 600;
        letter-spacing: 0.3px;
    }


    /* ========================================================
       HERO SECTION
       ======================================================== */

    .hero {
        position: relative;

        padding: 3.2rem 3.2rem 3rem 3.2rem;

        border-radius: 26px;

        background:
            linear-gradient(
                135deg,
                #102f63 0%,
                #173f82 48%,
                #285da8 100%
            );

        color: white;

        margin-bottom: 1.8rem;

        box-shadow:
            0 18px 45px rgba(16, 47, 99, 0.20);

        overflow: hidden;
    }

    .hero::after {
        content: "";

        position: absolute;

        width: 280px;
        height: 280px;

        right: -90px;
        top: -120px;

        border-radius: 50%;

        background: rgba(255, 255, 255, 0.07);
    }

    .hero::before {
        content: "";

        position: absolute;

        width: 180px;
        height: 180px;

        right: 120px;
        bottom: -120px;

        border-radius: 50%;

        background: rgba(255, 255, 255, 0.05);
    }

    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 800px;
    }

    .hero-overline {
        font-size: 0.75rem;

        font-weight: 700;

        letter-spacing: 1.8px;

        text-transform: uppercase;

        color: #b9d2f5;

        margin-bottom: 0.85rem;
    }

    .hero-title {
        font-size: 3.25rem;

        font-weight: 850;

        line-height: 1.05;

        letter-spacing: -1.2px;

        margin-bottom: 0.7rem;
    }

    .hero-subtitle {
        font-size: 1.35rem;

        font-weight: 600;

        line-height: 1.4;

        color: #e5edf9;

        margin-bottom: 1rem;
    }

    .hero-description {
        font-size: 0.98rem;

        line-height: 1.7;

        color: #cbd9ed;

        max-width: 720px;
    }


    /* ========================================================
       FEATURE SECTION
       ======================================================== */

    .feature-card {
        background: rgba(255, 255, 255, 0.96);

        border: 1px solid #dfe7f1;

        border-radius: 18px;

        padding: 1.45rem 1.5rem;

        min-height: 150px;

        box-shadow:
            0 5px 18px rgba(15, 23, 42, 0.045);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-3px);

        border-color: #c5d5eb;

        box-shadow:
            0 12px 28px rgba(15, 23, 42, 0.08);
    }

    .feature-number {
        font-size: 0.72rem;

        font-weight: 800;

        color: #3970b8;

        letter-spacing: 1.4px;

        margin-bottom: 0.7rem;
    }

    .feature-title {
        font-size: 1.05rem;

        font-weight: 750;

        color: #173b7a;

        margin-bottom: 0.45rem;
    }

    .feature-text {
        color: #64748b;

        font-size: 0.88rem;

        line-height: 1.55;
    }


    /* ========================================================
       SECTION HEADINGS
       ======================================================== */

    .section-header {
        margin-top: 2.8rem;

        margin-bottom: 1.2rem;
    }

    .section-eyebrow {
        font-size: 0.72rem;

        text-transform: uppercase;

        letter-spacing: 1.5px;

        color: #3970b8;

        font-weight: 800;

        margin-bottom: 0.35rem;
    }

    .section-title {
        font-size: 1.65rem;

        font-weight: 800;

        color: #172033;

        line-height: 1.2;

        margin-bottom: 0.35rem;
    }

    .section-description {
        color: #64748b;

        font-size: 0.92rem;

        line-height: 1.55;
    }


    /* ========================================================
       SEARCH PANEL
       ======================================================== */

    .search-panel {
        background: white;

        border: 1px solid #dce5f0;

        border-radius: 20px;

        padding: 1.4rem;

        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.055);

        margin-bottom: 1rem;
    }

    .search-label {
        font-size: 0.78rem;

        font-weight: 750;

        color: #334155;

        margin-bottom: 0.45rem;
    }

    div[data-testid="stTextInput"] {
        margin-bottom: 0 !important;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 11px;

        border: 1px solid #cbd5e1;

        padding: 0.78rem 1rem;

        font-size: 0.94rem;

        background: #ffffff;

        color: #172033;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-testid="stTextInput"] input:hover {
        border-color: #94a9c5;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #2857a8;

        box-shadow:
            0 0 0 3px rgba(40, 87, 168, 0.10);
    }


    /* ========================================================
       SEARCH HINT
       ======================================================== */

    .search-hint {
        margin-top: 0.9rem;

        padding: 0.7rem 0.9rem;

        background: #f5f8fc;

        border: 1px solid #e1e8f1;

        border-radius: 10px;

        color: #64748b;

        font-size: 0.82rem;

        line-height: 1.5;
    }

    .search-hint strong {
        color: #2857a8;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    div.stButton > button {
        border-radius: 11px;

        min-height: 44px;

        font-weight: 750;

        font-size: 0.9rem;

        border: none;

        background:
            linear-gradient(
                135deg,
                #173b7a,
                #2857a8
            );

        box-shadow:
            0 5px 14px rgba(23, 59, 122, 0.18);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 8px 18px rgba(23, 59, 122, 0.25);
    }


    /* ========================================================
       RESULT HEADER
       ======================================================== */

    .result-summary {
        display: flex;

        align-items: center;

        justify-content: space-between;

        background: #f4f7fb;

        border: 1px solid #dfe7f1;

        border-radius: 12px;

        padding: 0.8rem 1rem;

        margin-bottom: 1rem;
    }

    .result-count {
        color: #173b7a;

        font-size: 0.88rem;

        font-weight: 750;
    }

    .result-label {
        color: #64748b;

        font-size: 0.8rem;
    }


    /* ========================================================
       RESOURCE CARD
       ======================================================== */

    .resource-card {
        background: white;

        border: 1px solid #dce5ef;

        border-radius: 18px;

        padding: 1.45rem 1.55rem;

        margin-bottom: 1rem;

        box-shadow:
            0 5px 18px rgba(15, 23, 42, 0.045);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease;
    }

    .resource-card:hover {
        transform: translateY(-2px);

        border-color: #c5d5e8;

        box-shadow:
            0 12px 28px rgba(15, 23, 42, 0.075);
    }

    .resource-top {
        display: flex;

        align-items: center;

        justify-content: space-between;

        gap: 1rem;

        margin-bottom: 0.75rem;
    }

    .resource-type {
        display: inline-block;

        background: #eaf1fb;

        color: #2857a8;

        padding: 0.28rem 0.7rem;

        border-radius: 999px;

        font-size: 0.68rem;

        font-weight: 800;

        letter-spacing: 0.6px;

        text-transform: uppercase;
    }

    .resource-node {
        font-size: 0.72rem;

        color: #15803d;

        font-weight: 750;

        background: #f0fdf4;

        border: 1px solid #bbf7d0;

        padding: 0.28rem 0.65rem;

        border-radius: 999px;
    }

    .resource-title {
        font-size: 1.22rem;

        font-weight: 800;

        color: #172033;

        line-height: 1.3;

        margin-bottom: 0.45rem;
    }

    .resource-description {
        color: #64748b;

        font-size: 0.9rem;

        line-height: 1.6;

        margin-bottom: 1rem;
    }

    .resource-divider {
        height: 1px;

        background: #edf1f5;

        margin: 0.8rem 0 0.9rem 0;
    }

    .resource-meta {
        display: grid;

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

        gap: 0.8rem;
    }

    .meta-item {
        background: #f8fafc;

        border: 1px solid #edf1f5;

        border-radius: 9px;

        padding: 0.6rem 0.7rem;
    }

    .meta-label {
        display: block;

        font-size: 0.66rem;

        text-transform: uppercase;

        letter-spacing: 0.7px;

        color: #94a3b8;

        font-weight: 750;

        margin-bottom: 0.18rem;
    }

    .meta-value {
        display: block;

        color: #334155;

        font-size: 0.78rem;

        font-weight: 650;

        word-break: break-word;
    }


    /* ========================================================
       NETWORK ARCHITECTURE
       ======================================================== */

    .network-card {
        background:
            linear-gradient(
                135deg,
                #f8fbff,
                #eef4fb
            );

        border: 1px solid #d8e3f0;

        border-radius: 20px;

        padding: 1.5rem;

        margin-top: 2.5rem;

        box-shadow:
            0 6px 20px rgba(15, 23, 42, 0.045);
    }

    .network-title {
        font-size: 1.05rem;

        font-weight: 800;

        color: #173b7a;

        margin-bottom: 0.25rem;
    }

    .network-description {
        color: #64748b;

        font-size: 0.82rem;

        margin-bottom: 1.1rem;
    }

    .network-flow {
        display: flex;

        align-items: center;

        justify-content: center;

        flex-wrap: wrap;

        gap: 0.55rem;
    }

    .network-node {
        background: white;

        border: 1px solid #d7e1ed;

        color: #334155;

        padding: 0.5rem 0.85rem;

        border-radius: 9px;

        font-size: 0.76rem;

        font-weight: 700;

        box-shadow:
            0 2px 7px rgba(15, 23, 42, 0.035);
    }

    .network-arrow {
        color: #8aa2c0;

        font-size: 0.85rem;

        font-weight: 700;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;

        color: #94a3b8;

        font-size: 0.78rem;

        padding: 3rem 0 1rem;

        line-height: 1.8;
    }

    .footer-brand {
        color: #64748b;

        font-weight: 750;
    }


    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 768px) {

        .hero {
            padding: 2.2rem 1.6rem;
        }

        .hero-title {
            font-size: 2.4rem;
        }

        .hero-subtitle {
            font-size: 1.1rem;
        }

        .resource-meta {
            grid-template-columns: 1fr;
        }

        .network-flow {
            justify-content: flex-start;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TOP BRAND BAR
# ============================================================

st.html(
    """
    <div class="brand-bar">

        <div class="brand-name">
            EduShare
        </div>

        <div class="brand-label">
            DISTRIBUTED LEARNING PLATFORM
        </div>

    </div>
    """
)


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-content">

            <div class="hero-overline">
                Distributed Educational Resource Network
            </div>

            <div class="hero-title">
                EduShare
            </div>

            <div class="hero-subtitle">
                One gateway. Multiple academic resource nodes.
            </div>

            <div class="hero-description">
                Discover, access and share educational resources
                distributed across independent academic nodes.
                EduShare provides a unified search interface
                for discovering learning material across the
                distributed network.
            </div>

        </div>

    </div>
    """
)


# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3 = st.columns(
    3,
    gap="medium"
)


with col1:

    st.html(
        """
        <div class="feature-card">

            <div class="feature-number">
                01
            </div>

            <div class="feature-title">
                Educational Resources
            </div>

            <div class="feature-text">
                Find notes, assignments and learning
                materials from multiple academic sources
                through a unified search interface.
            </div>

        </div>
        """
    )


with col2:

    st.html(
        """
        <div class="feature-card">

            <div class="feature-number">
                02
            </div>

            <div class="feature-title">
                Distributed Network
            </div>

            <div class="feature-text">
                Resources are maintained across
                independent academic nodes and
                discovered through a central gateway.
            </div>

        </div>
        """
    )


with col3:

    st.html(
        """
        <div class="feature-card">

            <div class="feature-number">
                03
            </div>

            <div class="feature-title">
                Fast Discovery
            </div>

            <div class="feature-text">
                Submit one search request and retrieve
                relevant resources from the distributed
                network through gRPC communication.
            </div>

        </div>
        """
    )


# ============================================================
# SEARCH SECTION
# ============================================================

st.html(
    """
    <div class="section-header">

        <div class="section-eyebrow">
            Resource Discovery
        </div>

        <div class="section-title">
            Search Educational Resources
        </div>

        <div class="section-description">
            Search the distributed network using a topic,
            subject or keyword.
        </div>

    </div>
    """
)


# ============================================================
# SEARCH PANEL
# ============================================================

st.html(
    """
    <div class="search-panel">

        <div class="search-label">
            SEARCH QUERY
        </div>

    </div>
    """
)


query = st.text_input(
    "Search",
    placeholder="Try: Distributed Systems, RPC, Database, AI...",
    label_visibility="collapsed",
)


st.html(
    """
    <div class="search-hint">

        <strong>Suggested topics:</strong>

        Distributed Systems
        &nbsp;&nbsp;•&nbsp;&nbsp;
        RPC
        &nbsp;&nbsp;•&nbsp;&nbsp;
        Database
        &nbsp;&nbsp;•&nbsp;&nbsp;
        Artificial Intelligence

    </div>
    """
)


st.write("")


search_button = st.button(
    "Search Resources",
    type="primary",
    use_container_width=True,
)


# ============================================================
# SEARCH LOGIC
# ============================================================

if search_button:

    if not query.strip():

        st.warning(
            "Please enter a topic or keyword to search."
        )

    else:

        with st.spinner(
            "Searching across distributed nodes..."
        ):

            resources = search_all_nodes(query)


        # ====================================================
        # NO RESULTS
        # ====================================================

        if not resources:

            st.info(
                "No resources found for this search. "
                "Try another topic or keyword."
            )


        # ====================================================
        # RESULTS
        # ====================================================

        else:

            st.html(
                f"""
                <div class="section-header">

                    <div class="section-eyebrow">
                        Search Complete
                    </div>

                    <div class="section-title">
                        Search Results
                    </div>

                </div>

                <div class="result-summary">

                    <span class="result-count">
                        {len(resources)}
                        resource(s) discovered
                    </span>

                    <span class="result-label">
                        Distributed network response
                    </span>

                </div>
                """
            )


            for resource in resources:

                resource_type = escape(
                    str(
                        resource.resource_type
                        if resource.resource_type
                        else "Resource"
                    )
                )

                title = escape(
                    str(
                        resource.title
                        if resource.title
                        else "Untitled Resource"
                    )
                )

                description = escape(
                    str(
                        resource.description
                        if resource.description
                        else "No description available."
                    )
                )

                subject = escape(
                    str(
                        resource.subject
                        if resource.subject
                        else "Unknown"
                    )
                )

                author = escape(
                    str(
                        resource.author
                        if resource.author
                        else "Unknown"
                    )
                )

                resource_id = escape(
                    str(
                        resource.resource_id
                        if resource.resource_id
                        else "N/A"
                    )
                )

                node_id = escape(
                    str(
                        resource.node_id
                        if resource.node_id
                        else "Unknown Node"
                    )
                )


                st.html(
                    f"""
                    <div class="resource-card">

                        <div class="resource-top">

                            <span class="resource-type">
                                {resource_type}
                            </span>

                            <span class="resource-node">
                                {node_id}
                            </span>

                        </div>

                        <div class="resource-title">
                            {title}
                        </div>

                        <div class="resource-description">
                            {description}
                        </div>

                        <div class="resource-divider"></div>

                        <div class="resource-meta">

                            <div class="meta-item">

                                <span class="meta-label">
                                    Subject
                                </span>

                                <span class="meta-value">
                                    {subject}
                                </span>

                            </div>

                            <div class="meta-item">

                                <span class="meta-label">
                                    Author
                                </span>

                                <span class="meta-value">
                                    {author}
                                </span>

                            </div>

                            <div class="meta-item">

                                <span class="meta-label">
                                    Resource ID
                                </span>

                                <span class="meta-value">
                                    {resource_id}
                                </span>

                            </div>

                        </div>

                    </div>
                    """
                )


# ============================================================
# NETWORK ARCHITECTURE
# ============================================================

st.html(
    """
    <div class="network-card">

        <div class="network-title">
            Distributed Network Architecture
        </div>

        <div class="network-description">
            EduShare coordinates resource discovery through
            a gateway, registry and distributed academic nodes.
        </div>

        <div class="network-flow">

            <span class="network-node">
                Gateway
            </span>

            <span class="network-arrow">
                →
            </span>

            <span class="network-node">
                gRPC
            </span>

            <span class="network-arrow">
                →
            </span>

            <span class="network-node">
                Node Registry
            </span>

            <span class="network-arrow">
                →
            </span>

            <span class="network-node">
                CSE Node
            </span>

            <span class="network-node">
                Library Node
            </span>

            <span class="network-node">
                Community Node
            </span>

        </div>

    </div>
    """
)


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">

        <span class="footer-brand">
            EduShare
        </span>

        &nbsp;&nbsp;•&nbsp;&nbsp;

        Distributed Educational Resource Network

        <br>

        Powered by
        <strong>gRPC</strong>
        &nbsp;&nbsp;•&nbsp;&nbsp;
        <strong>Node Registry</strong>
        &nbsp;&nbsp;•&nbsp;&nbsp;
        <strong>Distributed Resource Nodes</strong>

    </div>
    """
)