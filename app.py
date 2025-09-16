import streamlit as st
import pandas as pd
import io
from unstructured.partition.auto import partition
from docx import Document
import google.generativeai as genai
import os
import traceback # Import traceback for detailed error information
import random # Import random for placeholder scoring

# Configure Google API Key
# Ensure you have GOOGLE_API_KEY set in your environment variables or Streamlit secrets
# In a Colab environment, you might use userdata.get('GOOGLE_API_KEY')
# For local development, set this in your environment variables or a .env file
# For Cloud Run deployment, you will configure this as a secret

#GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
#if not GOOGLE_API_KEY:
#    st.error("Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
#else:
#    try:
#        genai.configure(api_key=GOOGLE_API_KEY)
#    except Exception as e:
#        st.error(f"Error configuring Google API: {e}")

# --------------------------
# Session State (navigation)
# --------------------------
if "show_screen2" not in st.session_state:
    st.session_state["show_screen2"] = False

#if "extracted_text" not in st.session_state:
#    st.session_state["extracted_text"] = {}

#if "analysis_results" not in st.session_state:
#    st.session_state["analysis_results"] = None

# Small helper for colored badges
BADGE_OK = "✅"
BADGE_WARN = "⚠️"
BADGE_RISK = "❌"

# ======================================================
# SCREEN 1 – Upload Founder Material
# ======================================================
def screen1():
    st.set_page_config(
        page_title="AI Analyst – Startup Evaluation",
        page_icon="✨",
        layout="wide",
    )

    # Apply some basic styling for a more colorful look
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff; /* Changed background color to white */
            font-family: 'Arial', sans-serif; /* Changed to one font family */
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stMarkdown h1 {
            color: #FF4B4B;
            font-family: 'Arial', sans-serif; /* Changed to one font family */
        }
        .stMarkdown h3 {
            color: #586e75;
            font-family: 'Arial', sans-serif; /* Changed to one font family */
        }
        .stMarkdown div {
            color: #005f73;
            font-family: 'Arial', sans-serif; /* Changed to one font family */
        }
         .stFileUploader, .stTextArea {
            border: 2px solid #0077b6; /* Blue border */
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 20px;
            font-family: 'Arial', sans-serif; /* Changed to one font family */
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("✨ 📈 DevGEN: AI Analyst for Startup Evaluation")
    st.markdown("<p style='color: #0077b6; font-family: 'Arial', sans-serif;'>Upload founder material and get <strong>investor-ready deal notes</strong> with benchmarks and risks.</p>", unsafe_allow_html=True)

    # File upload & text input with some styling
    st.markdown("<h3 style='color: #023e8a;'>📂 Upload Pitch Deck or Transcript (PDF/TXT)</h3>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("", type=["pdf", "txt", "docx"], accept_multiple_files=True) # Added docx and accept_multiple_files

    st.markdown("<h3 style='color: #023e8a;'>Or paste founder email / call transcript:</h3>", unsafe_allow_html=True)
    manual_text = st.text_area("", height=300) # Added height for text area

    # Action button → Show Screen 2
    if st.button("🔎 Analyze Startup"):
        st.session_state["show_screen2"] = True
        st.rerun()
        """
        st.session_state["extracted_text"] = {} # Clear previous extractions
        st.session_state["analysis_results"] = None # Reset analysis results
        all_files_processed = True

        if uploaded_files:
            with st.spinner("Processing uploaded files..."): # Added spinner
                for uploaded_file in uploaded_files:
                    file_name = uploaded_file.name
                    file_type = uploaded_file.type

                    st.write(f"Processing file: {file_name}")

                    try:
                        if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document": # .docx
                            doc = Document(uploaded_file)
                            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                            st.session_state["extracted_text"][file_name] = text
                        elif file_type == "text/plain": # .txt
                            text = uploaded_file.getvalue().decode("utf-8")
                            st.session_state["extracted_text"][file_name] = text
                        elif file_type == "application/pdf": # .pdf - using unstructured for more robust extraction
                            # Need to save to a temporary file for unstructured to read
                            with open(f"/tmp/{file_name}", "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            elements = partition(f"/tmp/{file_name}")
                            text = "\n".join([str(el) for el in elements])
                            st.session_state["extracted_text"][file_name] = text
                        else:
                            st.warning(f"File type not supported for {file_name}: {file_type}")
                            all_files_processed = False
                            continue

                except Exception as e:
                    st.error(f"Error processing file {file_name}: {e}")
                    st.error(traceback.format_exc()) # Display traceback for debugging
                    all_files_processed = False
                    continue # Continue to the next file even if one fails

        if manual_text:
            st.session_state["extracted_text"]["manual_input.txt"] = manual_text

        if st.session_state["extracted_text"] and all_files_processed:
            st.session_state["show_screen2"] = True
            st.experimental_rerun()
        elif not all_files_processed:
            st.warning("Some files could not be processed. Please check the error messages above.")
        else:
            st.warning("Please upload a file or paste text to analyze.")
        """
# ======================================================
# SCREEN 2 – Analysis Results
# ======================================================
def screen2():
    st.set_page_config(
        page_title="AI Analyst – Startup Deal Notes",
        page_icon="📈",
        layout="wide",
    )

    # Apply some basic styling for a more colorful look
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff; /* Changed background color to white */
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stMarkdown h1 {
            color: #FF4B4B;
        }
        .stMarkdown h3 {
            color: #586e75;
        }
        .stMarkdown div {
            color: #007f73; /* Adjusted color for text */
        }
        /* Styling for the sidebar Controls section */
        .sidebar .sidebar-content {
            background-color: #34495e; /* A different dark background */
            color: #ecf0f1; /* Light text */
            padding: 20px; /* Padding */
            border-radius: 10px; /* Rounded corners */
            font-family: 'Roboto', sans-serif; /* Another professional font */
            box-shadow: 0 2px 5px rgba(0,0,0,0.2); /* Subtle shadow */
        }
        .sidebar .sidebar-content .stMarkdown h3 {
            color: #5dade2; /* Lighter blue for headings */
            font-family: 'Roboto', sans-serif; /* Consistent font for headings */
            margin-bottom: 12px;
            border-bottom: 1px solid #5e7d8a; /* Lighter separator line */
            padding-bottom: 6px;
        }
        .sidebar .sidebar-content label {
            color: #bdc3c7; /* Lighter grey for input labels */
            font-weight: normal;
            margin-bottom: 4px;
            display: block;
        }
        .sidebar .sidebar-content .stTextInput input,
        .sidebar .sidebar-content .stNumberInput input,
        .sidebar .sidebar-content .stSlider div,
        .sidebar .sidebar-content .stSelectbox div {
             background-color: #5e7d8a; /* Darker background for inputs */
             color: #ecf0f1 !important; /* Light text color for inputs */
        }

        .sidebar .sidebar-content .stSlider [data-baseweb="slider"] > div:first-child > div {
            background-color: #ecf0f1; /* Slider thumb color */
         }

        .stDataFrame {
            border: 1px solid #0077b6;
            border-radius: 5px;
        }
        .stMarkdown h2 {
            color: #03045e;
        }
        .stMarkdown strong {
            color: #0077b6;
        }
        .stMarkdown ul {
            color: #001d3d;
        }
        .stMarkdown pre {
            background-color: #e9ecef;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Courier New', Courier, monospace;
        }

        /* Styling for the Investor-Ready Deal Note section */
        .deal-note-container {
            background-color: #fff3cd; /* Light yellow background */
            padding: 30px; /* Increased padding */
            border-radius: 15px; /* More rounded corners */
            border: 3px solid #ffc107; /* Yellow border */
            box-shadow: 0 8px 16px rgba(0,0,0,0.2); /* More prominent shadow */
            font-family: 'Roboto', sans-serif; /* Different font */
            color: #343a40; /* Dark text color */
        }
        .deal-note-container h1 {
            color: #dc3545; /* Red heading */
            border-bottom: 3px solid #ffc107; /* Yellow underline */
            padding-bottom: 15px;
            margin-bottom: 25px;
            font-family: 'Georgia', serif; /* Different font for heading */
        }
        .deal-note-container h2 {
            color: #007bff; /* Blue subheadings */
            margin-top: 20px;
            margin-bottom: 12px;
            font-family: 'Arial', sans-serif; /* Different font for subheadings */
        }
        .deal-note-container strong {
            color: #6c757d; /* Grey text for strong elements */
        }
         .deal-note-container ul {
            margin-bottom: 20px;
            padding-left: 25px; /* Add padding to list */
        }
         .deal-note-container ul li {
            margin-bottom: 8px;
         }
        </style>
        """, unsafe_allow_html=True)

    # -----------------------------
    # Sidebar – Inputs
    # -----------------------------
    st.sidebar.title("⚙️ Controls")

    with st.sidebar:
        st.markdown("<h3>Company Overview</h3>", unsafe_allow_html=True)
        company = st.text_input("Company Name", value="FoodDash")
        sector = st.text_input("Sector", value="Food Delivery / Tech")
        founded = st.text_input("Founded", value="2023")
        stage = st.selectbox("Stage", ["Pre-Seed", "Seed", "Series A", "Series B"], index=1)
        founder = st.text_input("Founder", value="Barsha Rani")

        st.markdown("---")
        st.markdown("<h3>Last-Month Metrics</h3>", unsafe_allow_html=True)
        users_start = st.number_input("Users (start of month)", min_value=0, value=5000, step=100)
        users_end = st.number_input("Users (end of month)", min_value=0, value=7500, step=100)
        revenue = st.number_input("Monthly Revenue ($)", min_value=0, value=30000, step=1000)
        churn_pct = st.slider("Monthly Churn (%)", 0, 100, 20)
        new_hires = st.number_input("New Hires (last month)", min_value=0, value=3, step=1)

        st.markdown("---")
        st.markdown("<h3>Peer Benchmarks (Typical)</h3>", unsafe_allow_html=True)
        bench_growth_low, bench_growth_high = st.slider("User Growth % range", 0, 200, (30, 40))
        bench_revenue_low, bench_revenue_high = st.slider("Monthly Revenue range ($)", 0, 200000, (35000, 50000), step=5000)
        bench_churn = st.slider("Churn target % (lower is better)", 0, 100, 12)
        bench_hiring_low, bench_hiring_high = st.slider("New Hires range", 0, 50, (2, 4))

        st.markdown("---")
        st.markdown("<h3>Weightages (what you care about)</h3>", unsafe_allow_html=True)
        w_growth = st.slider("Growth importance", 0.0, 1.0, 0.35, 0.05)
        w_churn = st.slider("Churn importance", 0.0, 1.0, 0.30, 0.05)
        w_competition = st.slider("Competition pressure importance", 0.0, 1.0, 0.20, 0.05)
        w_revenue = st.slider("Revenue traction importance", 0.0, 1.0, 0.15, 0.05)

        # Normalize weights to sum to 1
        total_w = max(w_growth + w_churn + w_competition + w_revenue, 1e-6)
        w_growth, w_churn, w_competition, w_revenue = [w/total_w for w in (w_growth, w_churn, w_competition, w_revenue)]

        # --- Calculations based on sidebar inputs ---
        user_growth_pct = 0.0
        if users_start > 0:
            user_growth_pct = (users_end - users_start) / users_start * 100.0

    # Simple competitive pressure toggle (mock)
    competition_recent_raise = st.toggle("📰 Competitor raised a large round recently", value=True, help="If ON, we assume higher competitive pressure.")
    competition_pressure = 0.7 if competition_recent_raise else 0.3  # 0 (low) .. 1 (high)

        # Status helpers
        def status_for_growth(growth_pct: float) -> str:
            if growth_pct >= bench_growth_high:
                return BADGE_OK
            if growth_pct >= bench_growth_low:
                return BADGE_WARN
            return BADGE_RISK

        def status_for_revenue(rev: float) -> str:
            if rev >= bench_revenue_high:
                return BADGE_OK
            if rev >= bench_revenue_low:
                return BADGE_WARN
            return BADGE_RISK

        def status_for_churn(churn: float) -> str:
            if churn <= bench_churn:
                return BADGE_OK
            if churn <= bench_churn * 1.5:
                return BADGE_WARN
            return BADGE_RISK

        def status_for_hiring(h: int) -> str:
            if h >= bench_hiring_low and h <= bench_hiring_high:
                return BADGE_OK
            if h > bench_hiring_high:
                return BADGE_WARN  # fast hiring could be okay but watch burn
            return BADGE_WARN if h > 0 else BADGE_RISK

        # --- Placeholder Scoring and Verdict (Replace with actual logic) ---
        # These are simple random scores for demonstration.
        # You would replace this with logic that uses the extracted text analysis
        # and the metrics/benchmarks to calculate meaningful scores.
        score_growth = random.uniform(0.1, 0.9)
        score_churn = random.uniform(0.1, 0.9)
        score_revenue = random.uniform(0.1, 0.9)
        score_competition = random.uniform(0.1, 0.9)

        # Simple composite score and verdict based on random scores and weights
        composite = (score_growth * w_growth + (1 - score_churn) * w_churn + score_revenue * w_revenue + (1 - score_competition) * w_competition) / (w_growth + w_churn + w_revenue + w_competition) # Simple weighted average (churn and competition are inverted)

        if composite >= 0.7:
            verdict_tone = "success"
            verdict = "Proceed (Strong)"
        elif composite >= 0.4:
            verdict_tone = "warning"
            verdict = "Proceed with Caution"
        else:
            verdict_tone = "error"
            verdict = "Pass for now"

        # --- End of Placeholder ---

    #st.title("Startup Evaluation AI Analyst - Analysis Results")
    
    # -----------------------------
    # Header
    # -----------------------------
    left, right = st.columns([0.65, 0.35])
    with left:
        st.title("✨ 📈 DevGEN's Report")
        st.caption("Concise, actionable deal notes generated from founder materials & public data (mock demo)")
    with right:
        st.metric(label="Composite Score", value=f"{composite*100:.0f}%", delta=f"Growth {user_growth_pct:.0f}% | Churn {churn_pct}%")

    # -----------------------------
    # Company Overview + Key Metrics
    # -----------------------------
    col1, col2 = st.columns([0.38, 0.62])

    with col1:
        st.markdown("<h2 style='color: #0077b6;'>Company Overview</h2>", unsafe_allow_html=True)
        st.write(f"**Name:** {company}")
        st.write(f"**Sector:** {sector}")
        st.write(f"**Founded:** {founded}")
        st.write(f"**Stage:** {stage}")
        st.write(f"**Founder:** {founder}")

    with col2:
        st.markdown("<h2 style='color: #0077b6;'>Key Metrics (Last Month)</h2>", unsafe_allow_html=True)
        metrics_df = pd.DataFrame(
            [
                {"Metric": "User Growth", "Value": f"{user_growth_pct:.1f}%  ({users_start:,} → {users_end:,})", "Benchmark": f"{bench_growth_low}–{bench_growth_high}%", "Status": status_for_growth(user_growth_pct)},
                {"Metric": "Monthly Revenue", "Value": f"${revenue:,}", "Benchmark": f"${bench_revenue_low:,}–${bench_revenue_high:,}", "Status": status_for_revenue(revenue)},
                {"Metric": "Churn (Users Leaving)", "Value": f"{churn_pct}%", "Benchmark": f"≤ {bench_churn}%", "Status": status_for_churn(churn_pct)},
                {"Metric": "Hiring (New)", "Value": f"{new_hires}", "Benchmark": f"{bench_hiring_low}–{bench_hiring_high}", "Status": status_for_hiring(new_hires)},
            ]
        )
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)

    st.divider()

    # -----------------------------
    # Strengths & Risks (derived)
    # -----------------------------
    strengths = []
    risks = []

    # Strengths
    if status_for_growth(user_growth_pct) == BADGE_OK:
        strengths.append("Rapid user growth above peer range")
    if status_for_revenue(revenue) != BADGE_RISK:
        strengths.append("Meaningful early revenue traction")
    if status_for_hiring(new_hires) in (BADGE_OK, BADGE_WARN) and new_hires > 0:
        strengths.append("Active hiring indicates momentum")

    # Risks
    if status_for_churn(churn_pct) == BADGE_RISK:
        risks.append("High churn – users are leaving too quickly")
    if competition_recent_raise:
        risks.append("Competitor recently raised a large round recently – elevated pressure")
    if status_for_revenue(revenue) == BADGE_RISK:
        risks.append("Revenue below peer range – watch monetization and pricing")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<h2 style='color: #4CAF50;'>✅ Strengths</h2>", unsafe_allow_html=True)
        if strengths:
            for s in strengths:
                st.markdown(f"- <span style='color: #001d3d;'>{s}</span>", unsafe_allow_html=True)
        else:
            st.markdown("- <span style='color: #001d3d;'>None detected yet (adjust inputs in the sidebar)</span>", unsafe_allow_html=True)

    with c2:
        st.markdown("<h2 style='color: #FF4B4B;'>⚠️ Risks / Red Flags</h2>", unsafe_allow_html=True)
        if risks:
            for r in risks:
                st.markdown(f"- <span style='color: #001d3d;'>{r}</span>", unsafe_allow_html=True)
        else:
            st.markdown("- <span style='color: #001d3d;'>None detected yet (adjust inputs in the sidebar)</span>", unsafe_allow_html=True)

    st.divider()

    # -----------------------------
    # Benchmarks & Recommendation
    # -----------------------------
    colA, colB = st.columns([0.55, 0.45])

    with colA:
        st.markdown("<h2 style='color: #0077b6;'>📊 Benchmark vs. Peers</h2>", unsafe_allow_html=True)
        bench_df = pd.DataFrame(
            {
                "Dimension": ["Growth", "Churn", "Revenue", "Hiring"],
                "Company": [f"{user_growth_pct:.1f}%", f"{churn_pct}%", f"${revenue:,}", f"{new_hires}"],
                "Peers": [f"{bench_growth_low}–{bench_growth_high}%", f"≤ {bench_churn}%", f"${bench_revenue_low:,}–${bench_revenue_high:,}", f"{bench_hiring_low}–{bench_hiring_high}"],
            }
        )
        st.dataframe(bench_df, use_container_width=True, hide_index=True)

    with colB:
        st.markdown("<h2 style='color: #0077b6;'>💡 Recommendation</h2>", unsafe_allow_html=True)
        if verdict_tone == "success":
            st.success(f"**{verdict}:** Attractive profile across growth, churn, and revenue relative to peers.")
        elif verdict_tone == "warning":
            st.warning(f"**{verdict}:** Mixed signals – monitor churn and competitive dynamics before scaling exposure.")
        else:
            st.error(f"**{verdict}:** Key metrics trail peers or risk flags are elevated. Revisit after improvement.")

        st.markdown(
            f"**Why:**\n\n- Growth score: {score_growth:.2f} | Churn score: {score_churn:.2f}\n\n- Revenue score: {score_revenue:.2f} | Competition score: {score_competition:.2f}\n\n- Weighting → Growth {w_growth:.2f}, Churn {w_churn:.2f}, Revenue {w_revenue:.2f}, Competition {w_competition:.2f}"
        )

    st.divider()

    # -----------------------------
    # Investor-Ready Deal Note (exportable)
    # -----------------------------
    st.markdown("<h2 style='color: #0077b6;'>📋 Investor-Ready Deal Note</h2>", unsafe_allow_html=True)
    # Build the HTML content inside styled container
    deal_note_html = f"""
    <div class="deal-note-container">
        <h1>Investor-Ready Deal Note</h1>
        <h2>📌 Company Overview</h2>
        <p><strong>Name:</strong> {company}<br>
        <strong>Sector:</strong> {sector}<br>
        <strong>Founded:</strong> {founded}<br>
        <strong>Stage:</strong> {stage}<br>
        <strong>Founder:</strong> {founder}</p>
        <h2>📈 Summary</h2>
        <ul>
            <li><strong>User Growth:</strong> {user_growth_pct:.1f}% ({users_start:,} → {users_end:,})</li>
            <li><strong>Monthly Revenue:</strong> ${revenue:,}</li>
            <li><strong>Churn:</strong> {churn_pct}%</li>
            <li><strong>New Hires:</strong> {new_hires}</li>
        </ul>
        <h2>📊 Benchmarks vs Peers</h2>
        <ul>
            <li>Growth: {bench_growth_low}–{bench_growth_high}%</li>
            <li>Revenue: ${bench_revenue_low:,}–${bench_revenue_high:,}</li>
            <li>Churn target: ≤ {bench_churn}%</li>
            <li>Hiring: {bench_hiring_low}–{bench_hiring_high}</li>
        </ul>
        <h2>✅ Strengths</h2>
        <ul>
            {''.join([f'<li>{s}</li>' for s in strengths]) if strengths else '<li>(none)</li>'}
        </ul>
        <h2>⚠️ Risks / Red Flags</h2>
        <ul>
            {''.join([f'<li>{r}</li>' for r in risks]) if risks else '<li>(none)</li>'}
        </ul>
        <h2>💡 Recommendation</h2>
        <p><strong>{verdict}</strong><br>
        Composite Score: {composite*100:.0f}%</p>
        <p><em>Weights → Growth {w_growth:.2f}, Churn {w_churn:.2f},
        Revenue {w_revenue:.2f}, Competition {w_competition:.2f}</em></p>
    </div>
    """

    # Render styled HTML
    st.markdown(deal_note_html, unsafe_allow_html=True)

    # Download button (still in Markdown format for portability)
    deal_note_bytes = deal_note_html.encode("utf-8")
    st.download_button(
        label="⬇️ Download Deal Note (HTML)",
        data=deal_note_bytes,
        file_name=f"{company.replace(' ', '_').lower()}_deal_notes.html",
        mime="text/html",
    )

    # st.caption("This is a mock demo to illustrate how an AI analyst dashboard could look and behave. All these inputs are fully adjustable at runtime through the ⚙️ Controls section, allowing you to instantly explore different scenarios and outcomes.")
    st.markdown("""
    <p style='color: red;
              font-family: "Bell MT", serif;
              font-size: 20px;
              font-weight: bold;
              text-align: center;'>
    🔧 This is a mock demo to illustrate how an AI analyst dashboard could look and behave. All these inputs are fully adjustable at runtime through the ⚙️ Controls section, allowing you to instantly explore different scenarios and outcomes.
    </p>
    """, unsafe_allow_html=True)

    # --- end original Screen 2 code (unchanged) ---

    if st.button("Upload More Materials"):
        st.session_state["extracted_text"] = {} # Clear extracted text on going back
        st.session_state["analysis_results"] = None # Clear analysis results on going back
        st.session_state["show_screen2"] = False
        st.experimental_rerun()

# ======================================================
# Main app logic
# ======================================================
if st.session_state["show_screen2"]:
    screen2()
else:
    screen1()
