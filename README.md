<div align="center">
   <img src="https://img.icons8.com/fluency/96/shield.png" alt="Guard My Bills Logo" width="96"/>
  
   # <span style="color:#2d89ef">Guard My Bills</span>
  
   <b>Your AI-powered financial guardian 🛡️</b>
  
   <a href="https://guard-my-bills.vercel.app/" target="_blank"><img src="https://img.shields.io/badge/Live%20Demo-Visit%20Now-brightgreen?style=for-the-badge" alt="Live Demo"/></a>
   <br/>
   <a href="mailto:aryanprahraj@gmail.com">aryanprahraj@gmail.com</a> · <a href="https://www.linkedin.com/in/aryan-prahraj-89545160/">LinkedIn</a>
</div>

---

> "Guard your bills, guard your future!"

---

## 🚀 What is Guard My Bills?

Guard My Bills is a fun, modern, and powerful web app that helps you spot fraud and understand your spending—instantly! Upload your bank statement, get AI-powered fraud analysis, and enjoy beautiful charts and reports. No sign-up, no hassle, just peace of mind.

🌐 **Website:** [https://guard-my-bills.vercel.app/](https://guard-my-bills.vercel.app/)

## ✨ Features

- 🕵️‍♂️ **Fraud Detection:** Upload your bank statement (CSV/XLSX) and let our ML models flag suspicious transactions.
- 🔍 **Manual Transaction Check:** Compare transactions for impossible travel and anomalies.
- 📊 **Interactive Dashboard:** Visualize risk, spending, and merchant analytics.
- 📝 **PDF Reports:** Download beautiful fraud analysis reports.
- 💡 **No sign-up required:** Just open and use!
- 🎨 **Modern UI:** Built with Next.js, Tailwind CSS, and Recharts.

## 🏗️ Tech Stack

- **Frontend:** Next.js (React, TypeScript, Tailwind CSS)
- **Backend:** FastAPI (Python), pandas, scikit-learn, geopy
- **ML:** IsolationForest, rules-based risk scoring

## 🛠️ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/aryanprahraj/Guard-My-Bills.git
cd Guard-My-Bills

# 2. Start the backend (Python 3.8+)
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002

# 3. Start the frontend (Node.js 16+)
cd ../frontend
npm install
npm run dev

# 4. Open your browser
open http://localhost:3000
```

## 🗂️ Project Structure

```
Guard-My-Bills/
├── backend/      # FastAPI backend
├── frontend/     # Next.js frontend
├── model/        # ML models and data
├── ...
```

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

[MIT](LICENSE)

---

<div align="center">
   <b>Made with ❤️ by Aryan Prahraj</b><br/>
   <a href="mailto:aryanprahraj@gmail.com">aryanprahraj@gmail.com</a> · <a href="https://www.linkedin.com/in/aryan-prahraj-89545160/">LinkedIn</a>
</div>
# Guard My Bills

![Guard My Bills Logo](https://img.icons8.com/fluency/96/shield.png)

**Your Financial Guardian**

Guard My Bills is a modern web application that helps you detect fraudulent transactions and analyze your bank statements for suspicious activity. With a beautiful, intuitive interface and robust backend logic, you can:

- 🕵️‍♂️ **Upload your bank statement** (CSV, XLSX, or PDF) and get instant fraud analysis
- 🔍 **Check if a transaction is fraud** by comparing it with reference transactions
- 🚀 Enjoy a seamless, privacy-first experience—your data never leaves your machine

## Features

- **Fraud Detection**: Upload your bank statement and let our AI-powered backend flag risky transactions.
- **Manual Transaction Check**: Enter a transaction and compare it with two references to see if it's likely fraud, using smart rules and geolocation.
- **Modern UI**: Clean, responsive design built with Next.js and Tailwind CSS.
- **No sign-up required**: Just open and use!

## Getting Started

### Prerequisites
- Node.js (v16+ recommended)
- Python 3.8+

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/guard-my-bills.git
   cd guard-my-bills
   ```
2. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```
3. **Install backend dependencies:**
   ```bash
   cd ../backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Run the backend:**
   ```bash
   PYTHONPATH=. uvicorn backend.main:app --reload --host 0.0.0.0 --port 8002
   ```
5. **Run the frontend:**
   ```bash
   cd ../frontend
   npm run dev
   ```
6. **Open your browser:**
   Go to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
GuardMyBills/
├── backend/      # FastAPI backend
├── frontend/     # Next.js frontend
├── model/        # ML models and data
├── sample_bank_statement.csv
├── ...
```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)

---

> "Guard your bills, guard your future!"
