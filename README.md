# 🛡️ Reply Fraud Detection System (Masala Techii)

A multi-agent, LLM-assisted fraud detection pipeline built for the **Reply / ReplyMirror Challenge**.

---

# 🚀 Quick Start (Run in 4 steps)

```bash
pip install -r requirements.txt
cp .env.example .env.py        # then fill in your key (see below)
# edit .env.py and set OPENROUTER_API_KEY=sk-or-v1-...
python main.py --data ./data --output ./output/predictions.txt
```

👉 Output will be generated in: `./output/predictions.txt`

---

# 🔑 Getting a Free OpenRouter API Key

1. Sign up at **https://openrouter.ai** (free, no credit card required for free-tier models)
2. Go to **Dashboard → API Keys → Create key**
3. Paste the key into your `.env.py` file as `OPENROUTER_API_KEY=sk-or-v1-...`

The default model (`google/gemini-2.0-flash-exp:free`) is **permanently free** — no billing needed.

---

# ⚠️ IMPORTANT

* This project **requires an OpenRouter API key** (free tier works fine)
* Copy `.env.example` → `.env.py` and fill in your key before running
* Never commit `.env.py` — it is listed in `.gitignore`

---

# 🧠 Overview

The system detects fraudulent transactions using a combination of:

* Behavioral anomaly detection
* Rule-based heuristics
* LLM-based text risk analysis (SMS + emails)

Fraud signals are derived from:

* transaction patterns (amount, time, velocity)
* user behavior drift
* geographic inconsistencies
* phishing-style text

---

# 🏗️ Architecture

```
Data → FeatureAgent ↔ TextAgent (LLM)
         ↓
     ProfileAgent
         ↓
      RiskAgent
         ↓
    DecisionAgent
         ↓
   predictions.txt
```

---

# 📁 Project Structure

```
fraud_project/
├── agents/
├── data/
├── models/
├── output/
├── utils/
├── main.py
├── llm_client.py
├── train_model.py
├── trace_langfuse.py
├── requirements.txt
└── README.md
```

---

# 📂 Input Data

Place files inside `./data/`:

Required:

* `transactions.csv`

Recommended:

* `users.json`
* `locations.json`
* `sms.json`
* `mails.json`

---

# ⚙️ Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API key

Linux / Mac:

```bash
export OPENROUTER_API_KEY=sk-or-...
```

Windows (PowerShell):

```powershell
setx OPENROUTER_API_KEY "sk-or-..."
```

---

# 🚀 Running the Pipeline

```bash
python main.py --data ./data --output ./output/predictions.txt
```

Optional parameters:

```bash
python main.py \
  --data ./data \
  --output ./output/predictions.txt \
  --threshold 0.45 \
  --flag-rate 0.15
```

---

# ⚙️ How It Works

1. Load all datasets
2. Build features (amount, time, geo, text)
3. Track user behavior (ProfileAgent)
4. Train anomaly model (IsolationForest)
5. Score each transaction
6. Apply adaptive threshold (~15% flagged)
7. Output fraud IDs

---

# 🤖 LLM Integration

* Model: `openai/gpt-4.1-mini` (via OpenRouter)
* Used in:

  * `TextAgent` → SMS/email fraud detection
  * Training pipeline → description scoring

The LLM:

* detects phishing patterns
* outputs a risk score (0–1)
* uses strict prompting + fallback handling

---

# 📊 Observability (Langfuse)

To generate session ID for submission:

```bash
python trace_langfuse.py
```

This:

* creates valid session ID
* tracks LLM usage
* logs traces to dashboard

---

# 🧪 Training (Optional)

```bash
python train_model.py
```

This:

* builds weak labels
* adds LLM risk features
* trains RandomForest model
* saves model to `models/`

---

# 📤 Output Format (IMPORTANT)

File:

```text
output/predictions.txt
```

Format:

```
TX000123
TX000456
TX000789
```

Rules:

* One transaction ID per line
* No spaces
* No empty lines
* File name must remain `predictions.txt`

---

# 📤 Submission Instructions

1. Run the pipeline
2. Upload `predictions.txt`
3. Provide Langfuse session ID (from `trace_langfuse.py`)

---

# ⚠️ Common Issues

### ❌ Missing pandas / sklearn

```bash
pip install -r requirements.txt
```

---

### ❌ API key error

Set:

```bash
export OPENROUTER_API_KEY=your_key
```

---

### ❌ Output rejected

Check:

* correct format
* no blank lines
* valid transaction IDs

---

# ⚙️ Key Configuration

| Parameter     | Default      | Description               |
| ------------- | ------------ | ------------------------- |
| `--threshold` | 0.45         | base risk threshold       |
| `--flag-rate` | 0.15         | % of transactions flagged |
| LLM model     | gpt-4.1-mini | text risk scoring         |

---

# 🧰 Tech Stack

* Python 3.10+
* pandas / numpy
* scikit-learn
* lightgbm
* OpenRouter (LLM)
* Langfuse (tracing)

---

# 👥 **Masala Techii**
Owes Mehboob<br>
Sanya Khan<br>
Honi Arora
