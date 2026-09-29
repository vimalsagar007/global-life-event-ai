# Global Life Event AI Orchestrator

> **"One life event. Every task. Any country. One intelligent plan."**

Production-grade, globally deployable AI application built on Google Cloud, Gemini 2.5, Agent-to-Agent (A2A) protocol, Model Context Protocol (MCP), and Advanced Multilingual RAG.

---

## 🌍 Global Architecture

```text
                         GLOBAL USER
                              |
                              v
                       WEB APPLICATION
                              |
                              v
                   FASTAPI REST / SSE API
                              |
                              v
                   LIFE EVENT ORCHESTRATOR
                              |
        ┌─────────────────────┼──────────────────────┐
        |                     |                      |
        v                     v                      v
 JURISDICTION              A2A                    RAG
    AGENT                    |                      |
        |             SPECIALIST AGENTS       KNOWLEDGE
        |                     |                 SOURCES
        └─────────────────────┼──────────────────────┘
                              |
                              v
                        GEMINI / VERTEX AI
                              |
             ┌────────────────┼─────────────────┐
             |                |                 |
            MCP            PUB/SUB           MEMORY
             |                |                 |
        External APIs       Events          Firestore
             |
             v
      LOCAL / GOVERNMENT /
      BUSINESS SERVICES
```

---

## ✨ Key Features

1. **Zero Country Assumptions**: Dynamically resolves geographic boundaries down to `Country → Region → City → Postal Code`.
2. **Cross-Border Relocation Engine**: Detects multi-country events (e.g., Toronto, Canada to London, UK) and coordinates immigration, customs, banking, healthcare, schooling, and vehicle transfer.
3. **A2A Inter-Agent Protocol**: 20+ specialized agents with Agent Cards operating over A2A communication contracts.
4. **MCP Tool Integration & Human-in-the-Loop**: Safe execution registry enforcing human approval for `ACTION` calls (`create_calendar_event`, `send_notification`).
5. **Multilingual & Temporal RAG**: Documents filtered by jurisdiction and authority level (`OFFICIAL_GOVERNMENT`), with citation verification and freshness checks.
6. **Event-Driven Re-planning (Pub/Sub)**: Real-time re-planning when regulatory sources change, generating OLD PLAN vs NEW PLAN diffs.
7. **Interactive Dashboard**: Modern glassmorphism UI featuring visual dependency flow graphs, agent activity trace stream, and a 50-scenario benchmark suite.

---

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional)

### 2. Run Locally with Mock Adapters
```bash
git clone https://github.com/example/global-life-event-ai.git
cd global-life-event-ai

# Install dependencies
pip install -r requirements.txt

# Run backend & web app
./scripts/run_demo.sh
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🧪 Running Evaluation Benchmark

Run the full 50-scenario international life event test suite:
```bash
python3 scripts/run_tests.py
```

---

## ☁️ Google Cloud Deployment (Terraform)

Deploy to Google Cloud Run, Firestore, BigQuery, Pub/Sub, and GCS:

```bash
cd infrastructure/terraform
terraform init
terraform apply -var="project_id=YOUR_GCP_PROJECT_ID"
```

---

## 🛡️ Safety & Compliance

- **Non-Advisory Disclaimer**: All legal, tax, medical, and immigration tasks automatically carry disclaimers directing users to official authorities or licensed professionals.
- **Prompt Injection Defense**: Sanitizes all input text against injection patterns.
- **PII Minimization**: Redacts sensitive numbers (SSN/SIN/Card numbers) prior to storage.
