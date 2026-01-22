# 🚀 Momentum: Adaptive Procrastination Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 19](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://reactjs.org/)
[![Tailwind CSS v4](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Groq Llama 3](https://img.shields.io/badge/AI-Groq_Llama_3-f34f29)](https://groq.com/)

**Break the cycle of avoidance with adaptive, context-aware micro-tasks.**

Procrastination often stems from tasks feeling too big or overwhelming. **Momentum** is an intelligent agent designed to bridge the gap between intention and action by breaking down complex goals into hyper-approachable micro-steps that adapt to your success and energy levels.

---

## ✨ Key Features

- **🧠 Intelligent Decomposition**: Uses the Groq Llama 3.3 model to break any task into actionable, logical steps.
- **⚡ Adaptive Feedback Loop**: 
  - **Done ✓**: Move seamlessly to the next logical step.
  - **Too Hard 🔨**: If a step still feels overwhelming, the agent breaks *that specific step* into even tinier micro-tasks.
- **🕒 Context-Aware Reasoning**: Adjusts task sizing (Small/Medium) based on time of day (e.g., smaller tasks for late evenings when energy is lower).
- **💾 Memory System**: Logs every interaction in a local SQLite database to track progress and identify patterns.
- **🎨 Modern UI**: A responsive React interface styled with Tailwind CSS v4, featuring smooth animations and a structured output layout for maximum clarity.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, Flask (REST API), SQLite3, `python-dotenv`
- **AI Core**: Groq SDK (Llama 3.3 70B Versatile)
- **Frontend**: React 19, Vite, Tailwind CSS v4, PostCSS
- **Styling**: Modern gradients, glassmorphism-inspired components, and responsive grid layouts.

---

## 📂 Project Structure

```text
adaptive-procrastination-agent/
├── src/                     # Backend Logic
│   ├── app.py               # Flask API & Session Flow
│   ├── groq_client.py       # AI Orchestrator
│   ├── decision_engine.py   # Context Logic
│   ├── db.py                # SQL Storage
│   └── demo_agent.py        # Terminal Demo
├── frontend/                # React Web App
│   ├── src/                 # Components & Styles
│   ├── vite.config.js       
│   └── package.json         
├── prompts/                 # Prompt Engineering Templates
│   ├── decompose.txt        # Task break-down logic
│   └── phrase.txt           # Persona & Tone logic
├── data/                    # Local Storage (SQLite DB)
├── README.md                # Documentation
└── requirements.txt         # Python Dependencies
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Groq API Key** (Get yours at [console.groq.com](https://console.groq.com/keys))

### 2. Backend Setup
```bash
# Clone the repository
git clone https://github.com/your-username/momentum-agent.git
cd momentum-agent

# Install dependencies
pip install -r requirements.txt

# Configure Environment
# Create a .env file in the root directory
# Add: GROQ_API_KEY=your_key_here
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Run the Application
In one terminal, start the Python server:
```bash
python src/app.py
```
In another terminal, start the Vite dev server:
```bash
cd frontend && npm run dev
```
Open your browser to `http://localhost:5173`.

---

## 🤖 Agent Contract

- **Observation**: The agent observes the user's task input, category, and current time context.
- **Reasoning**: It determines if the user is in a "high energy" (Day) or "low energy" (Evening) window and adjusts task complexity accordingly.
- **Decision**: Orchestrates multiple LLM calls to decompose tasks and rephrase them into encouraging, actionable language.
- **Learning**: Records success/struggle feedback via the "Done" and "Too Hard" buttons to maintain user momentum.

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.
