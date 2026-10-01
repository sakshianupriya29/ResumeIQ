# ResumeIQ

### 🚀 Live Demo

[![Open ResumeIQ](https://img.shields.io/badge/Live%20Demo-ResumeIQ-success?style=for-the-badge)](https://resumeiq-app.streamlit.app/)

AI-powered resume intelligence and job matching platform built with Python, NLP, Scikit-learn, and Streamlit.

### AI-Powered Resume Intelligence & Job Matching Platform

ResumeIQ is a Python and Streamlit-based resume intelligence platform that analyzes resumes against job descriptions using NLP techniques.

It helps users understand resume-job similarity, identify skill gaps, analyze ATS-style keyword coverage, evaluate resume structure, and compare a resume against multiple job opportunities.

---

## 🚀 Overview

ResumeIQ combines resume parsing, natural language processing, skill extraction, keyword analysis, and job matching into a single interactive dashboard.

The platform allows users to:

- Upload a PDF resume
- Enter a target job description
- Calculate resume-job similarity
- Identify matching and missing skills
- Detect additional resume skills
- Analyze ATS-style keyword coverage
- Review resume statistics and structure
- Generate personalized recommendations
- Compare one resume against multiple jobs
- Rank jobs based on calculated text similarity
- Download analysis reports and visualizations

---

## ✨ Features

### 📄 Resume Analysis

- PDF resume upload and text extraction
- Resume statistics
- Word and character count
- Project count
- Resume section detection
- Basic resume quality checks

### 🧠 NLP-Based Job Matching

ResumeIQ uses:

- TF-IDF vectorization
- Cosine similarity

to calculate similarity between the resume and a job description.

The resulting score represents **text similarity between the provided resume and job description**.

---

### 🎯 Skill Gap Analysis

The platform identifies:

- ✅ Matching Skills
- ❌ Missing Skills
- ➕ Additional Skills

It combines a structured skills database with dynamically detected professional requirements.

---

### 🤖 ATS-Style Keyword Analysis

ResumeIQ provides ATS-style keyword coverage based on detected job requirements.

It displays:

- Total job keywords
- Matched keywords
- Missing keywords
- Keyword coverage percentage

> **Note:** This is an ATS-style keyword analysis and is not a proprietary ATS score.

---

### 📊 Visual Analytics

ResumeIQ provides visual representations of:

- Matching skills
- Missing skills
- Additional skills
- Resume skill coverage
- Resume-to-job similarity

Charts can also be downloaded from the application.

---

### 💼 Multiple Job Comparison

Users can compare a resume against multiple job descriptions.

The platform:

1. Calculates a similarity score for each job
2. Sorts jobs by calculated similarity
3. Displays the ranking
4. Visualizes the comparison

The ranking represents calculated text similarity among the jobs entered by the user.

---

### 📑 Downloadable Reports

ResumeIQ generates downloadable:

- Resume analysis reports
- Job comparison reports
- Skill coverage charts
- Job comparison charts

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Streamlit | Interactive web application |
| Scikit-learn | TF-IDF and cosine similarity |
| Pandas | Data processing |
| Matplotlib | Data visualization |
| pypdf | PDF text extraction |
| Regular Expressions | Text processing and requirement extraction |
| Git | Version control |

---

## 🧠 How ResumeIQ Works

```text
                 ┌─────────────────────┐
                 │    Upload Resume    │
                 │       PDF           │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    PDF Parsing      │
                 │      pypdf          │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Text Processing   │
                 │  Cleaning & NLP     │
                 └──────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │   Skill    │ │    TF-IDF  │ │    ATS     │
       │ Extraction │ │ Similarity │ │  Analysis  │
       └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                 ┌─────────────────────┐
                 │  Analysis Dashboard │
                 └──────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        Skill Gaps      Reports       Job Ranking
