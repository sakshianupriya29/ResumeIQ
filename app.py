import sys
import tempfile
import hashlib
from pathlib import Path
from io import BytesIO

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ============================================================
# BACKEND IMPORTS
# ============================================================

from pipeline import analyze_resume_against_job
from resume_parser import extract_text_from_pdf
from job_ranker import rank_jobs
from report_generator import generate_analysis_report
from job_report_generator import generate_job_comparison_report


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResumeIQ",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
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
        background-color: #0b0f14;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ========================================================
       HEADER
       ======================================================== */

    .hero-box {
        background-color: #141a22;
        border: 1px solid #293341;
        border-radius: 18px;
        padding: 38px 30px;
        margin-bottom: 30px;
        text-align: center;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        letter-spacing: -2px;
        color: #f5f7fa;
    }

    .hero-title-accent {
        color: #4da3ff;
    }

    .hero-subtitle {
        color: #aab4c0;
        font-size: 19px;
        margin-top: 8px;
    }

    .hero-tags {
        color: #7f8b99;
        font-size: 14px;
        margin-top: 15px;
    }

    /* ========================================================
       SECTION LABELS
       ======================================================== */

    .section-label {
        font-size: 28px;
        font-weight: 750;
        color: #f5f7fa;
        margin-top: 25px;
        margin-bottom: 8px;
    }

    .section-description {
        color: #8f9baa;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background-color: #141a22;
        border: 1px solid #293341;
        border-radius: 14px;
        padding: 18px;
    }

    div[data-testid="stMetricLabel"] {
        color: #8f9baa !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f5f7fa !important;
        font-weight: 750 !important;
    }

    /* ========================================================
       INPUTS
       ======================================================== */

    .stTextArea textarea,
    .stTextInput input {
        background-color: #141a22 !important;
        color: #f5f7fa !important;
        border-radius: 10px !important;
    }

    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    section[data-testid="stFileUploaderDropzone"] {
        background-color: #141a22;
        border-radius: 12px;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        min-height: 46px;
        border-radius: 10px;
        font-weight: 650;
    }

    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {
        font-weight: 600;
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;
        color: #657180;
        font-size: 13px;
        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "resume_bytes" not in st.session_state:
    st.session_state["resume_bytes"] = None

if "resume_name" not in st.session_state:
    st.session_state["resume_name"] = None

if "resume_hash" not in st.session_state:
    st.session_state["resume_hash"] = None

if "analysis_results" not in st.session_state:
    st.session_state["analysis_results"] = None

if "ranked_jobs" not in st.session_state:
    st.session_state["ranked_jobs"] = None


# ============================================================
# HEADER
# ============================================================

st.title("📄 ResumeIQ")

st.subheader(
    "AI-Powered Resume Intelligence & Job Matching Platform"
)

st.caption(
    "Analyze • Match • Identify • Improve"
)

st.write(
    "Analyze your resume, identify skill gaps, measure ATS-style "
    "keyword coverage, and compare your resume with multiple jobs."
)


# ============================================================
# RESUME ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-label">📄 Resume Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Upload your resume and compare it against a target job description.'
    '</div>',
    unsafe_allow_html=True
)


uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
    help="Upload a PDF resume for analysis."
)


# ============================================================
# HANDLE RESUME UPLOAD
# ============================================================

if uploaded_file is not None:

    current_bytes = uploaded_file.getvalue()

    current_hash = hashlib.md5(
        current_bytes
    ).hexdigest()

    if current_hash != st.session_state["resume_hash"]:

        st.session_state["resume_bytes"] = current_bytes
        st.session_state["resume_name"] = uploaded_file.name
        st.session_state["resume_hash"] = current_hash

        # Clear old analysis when a new resume is uploaded
        st.session_state["analysis_results"] = None
        st.session_state["ranked_jobs"] = None

    st.success(
        f"Resume uploaded successfully: "
        f"{st.session_state['resume_name']}"
    )

else:

    # Clear stored resume when the uploader is empty
    if st.session_state["resume_bytes"] is not None:

        st.session_state["resume_bytes"] = None
        st.session_state["resume_name"] = None
        st.session_state["resume_hash"] = None
        st.session_state["analysis_results"] = None
        st.session_state["ranked_jobs"] = None

# ============================================================
# JOB DESCRIPTION
# ============================================================

job_description = st.text_area(
    "💼 Job Description",
    height=220,
    placeholder="Paste the complete job description here..."
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.button(
    "🔍 Analyze Resume",
    type="primary",
    width="stretch"
)


# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze_button:

    if st.session_state["resume_bytes"] is None:

        st.error(
            "Please upload a PDF resume first."
        )

    elif not job_description.strip():

        st.error(
            "Please enter a job description."
        )

    else:

        temp_path = None

        try:

            with st.spinner(
                "Analyzing your resume..."
            ):

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(
                        st.session_state["resume_bytes"]
                    )

                    temp_path = temp_file.name

                results = analyze_resume_against_job(
                    temp_path,
                    job_description
                )

                st.session_state["analysis_results"] = results

                st.session_state["ranked_jobs"] = None

        except Exception as error:

            st.error(
                f"Analysis failed: {error}"
            )

        finally:

            if temp_path:

                temp_file_path = Path(temp_path)

                if temp_file_path.exists():
                    temp_file_path.unlink()


# ============================================================
# LOAD RESULTS
# ============================================================

results = st.session_state["analysis_results"]


# ============================================================
# DISPLAY ANALYSIS RESULTS
# ============================================================

if results is not None:

    st.divider()

    # ========================================================
    # MATCH OVERVIEW
    # ========================================================

    st.markdown(
        '<div class="section-label">📊 Match Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Summary of how the resume compares with the target job.'
        '</div>',
        unsafe_allow_html=True
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:

        st.metric(
            "Overall Match",
            f"{results['match_score']}%"
        )

    with metric2:

        st.metric(
            "Skill Match",
            f"{results['skill_match_percentage']}%"
        )

    with metric3:

        st.metric(
            "ATS-Style Coverage",
            f"{results['ats_keyword_coverage']}%"
        )


    # ========================================================
    # SKILL ANALYSIS
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">🧠 Skill Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Skills detected in your resume and compared with the job.'
        '</div>',
        unsafe_allow_html=True
    )

    tab_matching, tab_missing, tab_additional = st.tabs(
        [
            "✅ Matching Skills",
            "❌ Missing Skills",
            "➕ Additional Skills"
        ]
    )

    with tab_matching:

        matching_skills = results["matching_skills"]

        if matching_skills:

            for skill in matching_skills:
                st.write(f"✅ **{skill}**")

        else:

            st.info(
                "No matching skills were detected."
            )


    with tab_missing:

        missing_skills = results["missing_skills"]

        if missing_skills:

            for skill in missing_skills:
                st.write(f"❌ **{skill}**")

        else:

            st.success(
                "No missing skills were detected."
            )


    with tab_additional:

        additional_skills = results["additional_skills"]

        if additional_skills:

            for skill in additional_skills:
                st.write(f"➕ **{skill}**")

        else:

            st.info(
                "No additional skills were detected."
            )


    # ========================================================
    # SKILL COVERAGE CHART
    # ========================================================

    st.subheader("📈 Skill Coverage")

    skill_categories = [
        "Matching Skills",
        "Missing Skills",
        "Additional Skills"
    ]

    skill_values = [
        len(results["matching_skills"]),
        len(results["missing_skills"]),
        len(results["additional_skills"])
    ]

    fig, ax = plt.subplots(
        figsize=(10, 4.5)
    )

    fig.patch.set_facecolor("#0b0f14")
    ax.set_facecolor("#141a22")

    bars = ax.barh(
        skill_categories,
        skill_values
    )

    ax.set_xlabel(
        "Number of Skills",
        color="#c8d0da"
    )

    ax.set_title(
        "Resume Skill Coverage",
        color="#f5f7fa",
        fontsize=15,
        fontweight="bold",
        pad=15
    )

    ax.tick_params(
        axis="x",
        colors="#aab4c0"
    )

    ax.tick_params(
        axis="y",
        colors="#aab4c0"
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#394452")

    ax.grid(
        axis="x",
        alpha=0.15
    )

    ax.set_axisbelow(True)

    for bar, value in zip(
        bars,
        skill_values
    ):

        ax.text(
            value + 0.1,
            bar.get_y() + bar.get_height() / 2,
            str(value),
            va="center",
            color="#f5f7fa",
            fontweight="bold"
        )

    if max(skill_values) == 0:

        ax.set_xlim(
            0,
            1
        )

    else:

        ax.set_xlim(
            0,
            max(skill_values) + 2
        )

    plt.tight_layout()

    st.pyplot(
        fig,
        width="stretch"
    )

    skill_chart_image = BytesIO()

    fig.savefig(
        skill_chart_image,
        format="png",
        dpi=200,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )

    skill_chart_image.seek(0)

    st.download_button(
        "📥 Download Skill Coverage Chart",
        data=skill_chart_image,
        file_name="ResumeIQ_Skill_Coverage.png",
        mime="image/png"
    )

    plt.close(fig)


    # ========================================================
    # ATS ANALYSIS
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">'
        '🎯 ATS-Style Keyword Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Keyword coverage based on the skills detected in the job description. '
        'This is an ATS-style analysis, not a proprietary ATS score.'
        '</div>',
        unsafe_allow_html=True
    )

    ats1, ats2, ats3 = st.columns(3)

    with ats1:

        st.metric(
            "Total Job Keywords",
            results["ats_total_keywords"]
        )

    with ats2:

        st.metric(
            "Matched Keywords",
            len(results["ats_matched_keywords"])
        )

    with ats3:

        st.metric(
            "Missing Keywords",
            len(results["ats_missing_keywords"])
        )

    st.subheader("Matched Keywords")

    if results["ats_matched_keywords"]:

        st.write(
            ", ".join(
                results["ats_matched_keywords"]
            )
        )

    else:

        st.info(
            "No matched keywords detected."
        )

    st.subheader("Missing Keywords")

    if results["ats_missing_keywords"]:

        st.write(
            ", ".join(
                results["ats_missing_keywords"]
            )
        )

    else:

        st.success(
            "No missing keywords detected."
        )


    # ========================================================
    # RESUME PROFILE
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">📄 Resume Profile</div>',
        unsafe_allow_html=True
    )

    profile1, profile2, profile3 = st.columns(3)

    with profile1:

        st.metric(
            "Word Count",
            results["word_count"]
        )

    with profile2:

        st.metric(
            "Character Count",
            results["character_count"]
        )

    with profile3:

        st.metric(
            "Projects",
            results["project_count"]
        )


    # ========================================================
    # RESUME SECTIONS
    # ========================================================

    st.subheader("Resume Sections")

    sections = results["detected_sections"]

    section_columns = st.columns(3)

    for index, (section, detected) in enumerate(
        sections.items()
    ):

        with section_columns[index % 3]:

            if detected:

                st.success(
                    f"✓ {section}"
                )

            else:

                st.warning(
                    f"✗ {section}"
                )


    # ========================================================
    # QUALITY CHECKS
    # ========================================================

    st.subheader("Resume Quality Checks")

    for check in results["quality_checks"]:

        st.write(
            f"• {check}"
        )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">💡 Recommendations</div>',
        unsafe_allow_html=True
    )

    for index, recommendation in enumerate(
        results["recommendations"],
        start=1
    ):

        st.write(
            f"**{index}.** {recommendation}"
        )


    # ========================================================
    # ANALYSIS REPORT
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-label">'
        '⬇️ Download Analysis Report'
        '</div>',
        unsafe_allow_html=True
    )

    analysis_report = generate_analysis_report(
        results
    )

    st.download_button(
        label="📥 Download Resume Analysis Report",
        data=analysis_report,
        file_name="ResumeIQ_Analysis_Report.txt",
        mime="text/plain",
        width="stretch"
    )


# ============================================================
# MULTIPLE JOB COMPARISON
# ============================================================

st.divider()

st.markdown(
    '<div class="section-label">💼 Compare Multiple Jobs</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Compare your uploaded resume against multiple job descriptions.'
    '</div>',
    unsafe_allow_html=True
)


if st.session_state["resume_bytes"] is None:

    st.info(
        "Upload your resume above to enable multiple-job comparison."
    )

else:

    number_of_jobs = st.number_input(
        "Number of jobs to compare",
        min_value=2,
        max_value=5,
        value=3,
        step=1
    )

    jobs = []

    for index in range(
        int(number_of_jobs)
    ):

        st.subheader(
            f"Job {index + 1}"
        )

        title = st.text_input(
            "Job Title",
            key=f"comparison_title_{index}",
            placeholder="Example: Data Analyst"
        )

        description = st.text_area(
            "Job Description",
            key=f"comparison_description_{index}",
            height=150,
            placeholder="Paste the complete job description..."
        )

        jobs.append(
            {
                "title": title,
                "description": description
            }
        )


    compare_button = st.button(
        "📊 Compare Jobs",
        type="primary",
        width="stretch"
    )


    # ========================================================
    # RUN JOB COMPARISON
    # ========================================================

    if compare_button:

        valid_jobs = [
            job
            for job in jobs
            if job["title"].strip()
            and job["description"].strip()
        ]

        if len(valid_jobs) < 2:

            st.error(
                "Please enter at least two complete jobs."
            )

        else:

            temp_path = None

            try:

                with st.spinner(
                    "Comparing jobs..."
                ):

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:

                        temp_file.write(
                            st.session_state["resume_bytes"]
                        )

                        temp_path = temp_file.name

                    resume_text = extract_text_from_pdf(
                        temp_path
                    )

                    ranked_jobs = rank_jobs(
                        resume_text,
                        valid_jobs
                    )

                    st.session_state["ranked_jobs"] = (
                        ranked_jobs
                    )

            except Exception as error:

                st.error(
                    f"Job comparison failed: {error}"
                )

            finally:

                if temp_path:

                    temp_file_path = Path(temp_path)

                    if temp_file_path.exists():
                        temp_file_path.unlink()


    # ========================================================
    # JOB COMPARISON RESULTS
    # ========================================================

    ranked_jobs = st.session_state["ranked_jobs"]


    if ranked_jobs is not None:

        st.divider()

        st.subheader(
            "📊 Job Comparison Results"
        )

        comparison_table = pd.DataFrame(
            {
                "Rank": [
                    index
                    for index in range(
                        1,
                        len(ranked_jobs) + 1
                    )
                ],
                "Job Title": [
                    job["title"]
                    for job in ranked_jobs
                ],
                "Match Score": [
                    f"{job['score']}%"
                    for job in ranked_jobs
                ]
            }
        )

        st.dataframe(
            comparison_table,
            hide_index=True,
            width="stretch"
        )


        # ====================================================
        # VISUAL JOB COMPARISON
        # ====================================================

        st.subheader(
            "📈 Match Score Comparison"
        )

        job_titles = [
            job["title"]
            for job in ranked_jobs
        ]

        job_scores = [
            job["score"]
            for job in ranked_jobs
        ]

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        fig.patch.set_facecolor("#0b0f14")
        ax.set_facecolor("#141a22")

        bars = ax.barh(
            job_titles,
            job_scores
        )

        ax.set_xlabel(
            "Match Score (%)",
            color="#c8d0da"
        )

        ax.set_title(
            "Resume-to-Job Similarity",
            color="#f5f7fa",
            fontsize=15,
            fontweight="bold",
            pad=15
        )

        ax.tick_params(
            axis="x",
            colors="#aab4c0"
        )

        ax.tick_params(
            axis="y",
            colors="#aab4c0"
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_color("#394452")

        ax.grid(
            axis="x",
            alpha=0.15
        )

        ax.set_axisbelow(True)

        for bar, score in zip(
            bars,
            job_scores
        ):

            ax.text(
                score + 0.5,
                bar.get_y() + bar.get_height() / 2,
                f"{score:.2f}%",
                va="center",
                color="#f5f7fa",
                fontweight="bold"
            )

        max_score = max(
            job_scores
        ) if job_scores else 0

        ax.set_xlim(
            0,
            max(10, max_score + 8)
        )

        plt.tight_layout()

        st.pyplot(
            fig,
            width="stretch"
        )


        # ====================================================
        # DOWNLOAD JOB CHART
        # ====================================================

        job_chart_image = BytesIO()

        fig.savefig(
            job_chart_image,
            format="png",
            dpi=200,
            bbox_inches="tight",
            facecolor=fig.get_facecolor()
        )

        job_chart_image.seek(0)

        st.download_button(
            "📥 Download Match Score Chart",
            data=job_chart_image,
            file_name="ResumeIQ_Job_Match_Comparison.png",
            mime="image/png"
        )

        plt.close(fig)


        # ====================================================
        # DOWNLOAD JOB COMPARISON REPORT
        # ====================================================

        st.subheader(
            "⬇️ Download Comparison"
        )

        comparison_report = (
            generate_job_comparison_report(
                ranked_jobs
            )
        )

        st.download_button(
            label="📥 Download Job Comparison Report",
            data=comparison_report,
            file_name="ResumeIQ_Job_Comparison_Report.txt",
            mime="text/plain",
            width="stretch"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        ResumeIQ · AI-Powered Resume Intelligence & Job Matching
    </div>
    """,
    unsafe_allow_html=True
)