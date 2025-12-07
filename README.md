<div align="center">
   <img src="https://img.icons8.com/fluency/192/shield.png" alt="Guard My Bills Logo" width="120"/>
  
   # ⚔️ Guard My Bills
  
   ### *Your AI-Powered Financial Guardian*
  
   [![Live Demo](https://img.shields.io/badge/🌐%20Live%20Demo-Visit%20Now-brightgreen?style=for-the-badge&logo=vercel)](https://guard-my-bills.vercel.app/)
   [![GitHub](https://img.shields.io/badge/GitHub-aryanprahraj-black?style=for-the-badge&logo=github)](https://github.com/aryanprahraj/Guard-My-Bills)
   [![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
   
   **🚀 Instantly detect fraud • 📊 Visualize spending • 🛡️ Protect your finances**
   
</div>

---

## 💡 What Problem Does It Solve?

Ever wonder if your bank statement is trustworthy? 🤔 **Guard My Bills** uses **Machine Learning** to automatically scan your transactions and flag suspicious activity that humans might miss.

### Real Example: Impossible Travel
- Transaction 1: Jersey City at 1:36 PM
- Transaction 2: New York City at 1:35 PM (1 minute apart, 10 miles away)
- ❌ **HIGH RISK** → Impossible to travel that distance in 1 minute!

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🕵️‍♂️ **Fraud Detection** | Upload CSV/XLSX/PDF bank statements and get AI-powered fraud analysis instantly |
| 🔍 **Manual Transaction Check** | Compare any transaction with 2 references to spot anomalies & impossible travel |
| 📊 **Interactive Charts** | Beautiful visualizations of spending patterns, merchant analysis, and risk timeline |
| 📄 **PDF Reports** | Download detailed fraud analysis reports |
| ⚡ **No Sign-up** | Privacy-first: just upload and analyze—your data stays private |
| 🎨 **Modern UI** | Sleek, responsive design that works on all devices |

---

## 🤖 AI & Machine Learning

Guard My Bills uses **cutting-edge ML techniques**:

```python
┌─────────────────────────────────────────────────┐
│ Upload Bank Statement (CSV/XLSX/PDF)            │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ Feature Engineering (20+ features)              │
│ • Velocity, distance, time delta                │
│ • Amount statistics, z-scores                   │
│ • Temporal patterns, merchant history           │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ Isolation Forest Model (Anomaly Detection)      │
│ Scikit-learn's unsupervised learning            │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ Rules Engine (Fraud Rules)                      │
│ • Impossible travel (>800 km/h)                 │
│ • Nighttime anomalies                           │
│ • Unusual spending patterns                     │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ Risk Classification: HIGH / MEDIUM / LOW         │
└─────────────────────────────────────────────────┘
```

---

## 🏗️ Tech Stack

<table>
<tr>
  <td align="center">
    <img src="https://img.icons8.com/color/96/000000/react-native.png" width="80"/>
    <br/><b>Frontend</b><br/>
    <small>Next.js 14<br/>React 18<br/>TypeScript<br/>Tailwind CSS</small>
  </td>
  <td align="center">
    <img src="https://img.icons8.com/color/96/000000/python.png" width="80"/>
    <br/><b>Backend</b><br/>
    <small>FastAPI<br/>Uvicorn<br/>Pandas<br/>NumPy</small>
  </td>
  <td align="center">
    <img src="https://img.icons8.com/color/96/000000/artificial-intelligence.png" width="80"/>
    <br/><b>ML/Data</b><br/>
    <small>Scikit-learn<br/>Isolation Forest<br/>Geopy<br/>Haversine</small>
  </td>
  <td align="center">
    <img src="https://img.icons8.com/color/96/000000/cloud.png" width="80"/>
    <br/><b>Deployment</b><br/>
    <small>Vercel<br/>Render<br/>GitHub<br/>Docker Ready</small>
  </td>
</tr>
</table>

---

## 🚀 Quick Start

### Option 1: Try the Live Demo
**[👉 Visit Guard My Bills](https://guard-my-bills.vercel.app/)** - No setup required!

### Option 2: Run Locally

#### Prerequisites
```bash
✓ Node.js 16+ (for frontend)
✓ Python 3.8+ (for backend)
```

#### Installation
```bash
# 1️⃣ Clone the repository
git clone https://github.com/aryanprahraj/Guard-My-Bills.git
cd Guard-My-Bills

# 2️⃣ Setup Backend
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3️⃣ Start Backend Server
uvicorn main:app --reload --host 0.0.0.0 --port 8002
# ✓ Backend running at http://localhost:8002

# 4️⃣ Setup Frontend (new terminal)
cd frontend
npm install
npm run dev
# ✓ Frontend running at http://localhost:3000
```

**Done!** 🎉 Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📁 Project Structure

```
Guard-My-Bills/
├── 📂 backend/                    # FastAPI Backend
│   ├── core/                      # ML & Feature Engineering
│   │   ├── ml_model.py           # Isolation Forest
│   │   ├── feature_engineering.py # Feature extraction
│   │   └── rules_engine.py       # Fraud rules
│   ├── routers/                   # API endpoints
│   ├── services/                  # PDF, comparison logic
│   ├── models/                    # Pydantic schemas
│   ├── main.py                   # FastAPI app
│   └── requirements-prod.txt      # Dependencies
│
├── 📂 frontend/                   # Next.js Frontend
│   ├── pages/                     # Routes
│   ├── components/                # React components
│   ├── services/                  # API client
│   └── styles/                    # Tailwind CSS
│
├── 📂 model/                      # ML Model & Cache
└── README.md                      # This file
```

---

## 📊 How to Use

### 1️⃣ Fraud Detection from Bank Statement
```
📤 Upload CSV/XLSX/PDF
   ↓
🤖 AI analyzes transactions
   ↓
📋 See results:
   • HIGH RISK transactions
   • Detailed explanations
   • Fraud probability score
   ↓
📄 Download PDF report
```

### 2️⃣ Manual Transaction Comparison
```
🔍 Enter a suspicious transaction
🔄 Add 2 reference transactions
📍 Get instant fraud verdict
💡 See detailed explanation
```

---

## 🎯 Example Fraud Detection

**Input:** 3 transactions
| Date | Time | City | Amount | Status |
|------|------|------|--------|--------|
| 08/12/2025 | 01:36 PM | Jersey City | $12 | 🔍 Checking |
| 08/12/2025 | 01:35 PM | New York City | $15 | Reference 1 |
| 08/12/2025 | 05:09 PM | Jersey City | $18 | Reference 2 |

**Output:** 
```
⚠️ HIGH RISK - Impossible Travel
├─ Velocity: 960 km/h (max human transport: ~900 km/h)
├─ Distance: 10 km
├─ Time delta: 1 minute
└─ Verdict: LIKELY FRAUD ❌
```

---

## 🔒 Privacy & Security

✅ **100% Private**
- No account creation needed
- Your data is NOT stored on servers
- All processing happens in your browser
- Completely open source

---

## 📈 Model Performance

- **Algorithm:** Isolation Forest (Unsupervised Anomaly Detection)
- **Features:** 20+ engineered features
- **Detection Rules:** 8+ fraud patterns
- **Hybrid Approach:** ML scores + domain-specific rules

---

## 🚢 Deployment

### Backend (Render)
```bash
Build Command: pip install -r requirements-prod.txt
Start Command: bash start.sh
Live at: https://guard-my-bills.onrender.com
```

### Frontend (Vercel)
```bash
Framework: Next.js
Deployment: Automatic on git push
Live at: https://guard-my-bills.vercel.app
```

---

## 🤝 Contributing

We ❤️ contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact & Links

<div align="center">

**Made with ❤️ by [Aryan Prahraj](https://www.linkedin.com/in/aryan-prahraj-89545160/)**

[![Email](https://img.shields.io/badge/📧%20Email-aryanprahraj@gmail.com-red?style=flat-square)](mailto:aryanprahraj@gmail.com)
[![LinkedIn](https://img.shields.io/badge/💼%20LinkedIn-Aryan%20Prahraj-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/aryan-prahraj-89545160/)
[![Portfolio](https://img.shields.io/badge/🌐%20Portfolio-aryan-portfolio-orange?style=flat-square&logo=vercel)](https://aryan-portfolio-amber.vercel.app/)
[![GitHub](https://img.shields.io/badge/🐙%20GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/aryanprahraj)

---

### 🌟 If you found this helpful, please give us a star! ⭐

<img src="https://img.icons8.com/fluency/96/star.png" width="40"/>

</div>
