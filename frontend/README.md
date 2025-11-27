# Guard My Bills Frontend

This is the Next.js (TypeScript) frontend for Guard My Bills, a modern ML-powered credit/debit card fraud detection and spending analysis platform.

## Features
- Upload credit/debit card statements (CSV/XLSX) for fraud analysis
- Visualize risk, spending, and merchant analytics
- Manually compare two transactions for fraud risk
- Download PDF fraud reports
- Modern UI with TailwindCSS and Recharts

## Getting Started

1. Install dependencies:
   ```sh
   npm install
   ```
2. Run the development server:
   ```sh
   npm run dev
   ```
3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure
- `pages/` — Next.js pages (routes)
- `components/` — Reusable React components
- `services/` — API client for backend integration
- `styles/` — TailwindCSS and global styles
- `utils/` — Formatters and validators

## Environment Variables
- `NEXT_PUBLIC_API_BASE` — Set to your backend API base URL (default: `http://localhost:8000`)

---

For backend and full-stack integration, see the main project README.
