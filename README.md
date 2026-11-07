# 🩹 Scar Tissue
### AI-Powered Incident Investigation with Persistent Organizational Memory

**Learn from previous incidents. Investigate smarter. Prevent repeated mistakes.**

## 📌 Overview

Scar Tissue is an AI-assisted incident investigation system that helps engineers investigate technical failures by learning from previous incident experiences.

Traditional incident investigation often depends on engineers remembering how similar problems were solved in the past. When that knowledge is lost or overlooked, teams may repeat the same investigation steps and waste valuable time.

Scar Tissue addresses this problem by combining **AI-powered reasoning with persistent organizational memory**.

It retrieves relevant historical experiences using Hindsight and uses Groq-powered AI to analyze current evidence, identify possible investigation paths, and recommend practical next steps.

Importantly, historical incidents are treated as clues rather than confirmed explanations for new incidents.

## 🎯 Problem Statement

During technical incidents:
- Engineers may repeatedly investigate problems that have occurred before.
- Valuable troubleshooting knowledge can be lost between incidents.
- Similar symptoms do not always have the same root cause.
- Existing incident records may not provide actionable investigation guidance.

## 💡 Our Solution

Scar Tissue creates a continuous learning loop:

1. **Report:** An engineer enters the affected service, problem description, and current observations or logs.
2. **Recall:** Hindsight retrieves relevant experiences from previous incidents.
3. **Investigate:** Groq AI analyzes the current evidence alongside historical memories.
4. **Recommend:** The system generates investigation steps and explains why they are useful.
5. **Record:** The engineer records the action attempted and its actual outcome.
6. **Retain:** The outcome is stored in SQLite and retained in Hindsight for future investigations.

## ✨ Key Features

- **AI-Assisted Investigation:** Generates structured investigation reports using current incident evidence.
- **Persistent Organizational Memory:** Uses Hindsight to retain and retrieve experiences across sessions.
- **Context-Aware Recommendations:** Uses historical experiences without blindly repeating previous diagnoses.
- **Contradictory Evidence Handling:** Recognizes when current observations conflict with historical incidents.
- **Engineer-Verified Outcomes:** Separates AI-generated hypotheses from engineer-confirmed causes.
- **Incident Tracking:** Stores incident details and investigation outcomes in SQLite.
- **Memory Synchronization:** Tracks whether an outcome was successfully synchronized with Hindsight.

## 🏗️ System Architecture

```text
             Engineer
                 |
                 v
        Streamlit Dashboard
                 |
                 v
          Incident Details
                 |
          +------+------+
          |             |
          v             v
     Hindsight        Groq AI
   Memory Recall    Investigation
          |             |
          +------+------+
                 |
                 v
        Investigation Report
                 |
                 v
        Engineer Action
                 |
                 v
         Record Outcome
                 |
          +------+------+
          |             |
          v             v
        SQLite       Hindsight
     Incident Ledger  Memory Retention
```

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive dashboard |
| Groq | AI-powered investigation |
| Hindsight | Persistent memory and experience retrieval |
| SQLite | Incident and outcome storage |
| python-dotenv | Environment variable management |

## 📂 Project Structure

```text
scar-tissue/
│
├── app.py              # Streamlit dashboard
├── investigator.py    # AI investigation logic
├── memory.py           # Hindsight integration
├── database.py         # SQLite database operations
├── sample_data.py      # Sample data module
├── requirements.txt    # Python dependencies
├── .gitignore          # Excluded files and secrets
├── README.md           # Project documentation
└── scar_tissue.db      # Local database (generated)
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/SPANDANA-10/scar-tissue.git
cd scar-tissue
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root directory.

Add the following configuration:

```env
HINDSIGHT_API_URL=your_hindsight_api_url
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BANK_ID=scar-tissue

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Replace the placeholder values with your own API credentials.

**Important:** Never upload your `.env` file or expose API credentials publicly.

### 5. Run the application

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## 🧪 Example Investigation Scenarios

### Scenario 1: Database Connection Timeouts

A Checkout API experiences request timeouts alongside increasing database connection counts.

The system retrieves a previous incident where restarting the service provided only temporary relief.

It recommends investigating connection usage and related database behavior instead of assuming a restart is a permanent solution.

### Scenario 2: Contradictory Evidence

A Checkout API experiences request timeouts, but database connection metrics are normal and database health checks are passing.

Current logs indicate repeated timeouts from an external payment provider.

Scar Tissue prioritizes investigating the external dependency rather than blindly repeating the historical database diagnosis.

## 🔐 Design Principles

- Current evidence takes priority over historical assumptions.
- Similar symptoms do not guarantee identical root causes.
- AI recommendations are hypotheses, not confirmed diagnoses.
- Only engineer-reported outcomes are recorded as actual investigation results.
- Missing information must not be treated as evidence of normal operation.

## 🚀 Future Enhancements

- Advanced incident correlation and deduplication.
- Improved memory organization and retrieval.
- Integration with monitoring and observability platforms.
- Support for additional incident sources and log formats.
- Enhanced investigation analytics and visualizations.

## 👩‍💻 Project

**Scar Tissue — AI-Powered Incident Investigation and Persistent Organizational Memory**

GitHub Repository: https://github.com/SPANDANA-10/scar-tissue

---

*Built to help engineering teams turn past incidents into reusable knowledge and make future investigations smarter.*