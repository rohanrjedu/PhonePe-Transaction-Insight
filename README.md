# PhonePe Pulse Insights Dashboard

An interactive Streamlit dashboard for analyzing PhonePe's Pulse data across payments, users, and insurance. 

## Features
- **9 Strategic Case Studies**: Deep-dive analysis on market trends, device dominance, and growth strategies.
- **Dynamic Leaderboards**: Top performing states, districts, and pincodes.
- **Professional UI**: Clean, corporate-ready interface with interactive Plotly visualizations.

## Project Structure
- `main.py`: Entry point for the Streamlit application.
- `src/`: Core logic and analysis modules.
  - `case_studies.py`: Implementation of the 9 analysis scenarios.
  - `etl.py`: Data ingestion pipeline (JSON to SQL).
  - `db.py`: Database connection and utility functions.
  - `config.py`: Central configuration and data paths.
- `data/`: Extracted Pulse data (Aggregated, Map, Top).

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd PhonePe-Transaction-Insight
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database**:
   The project now uses an embedded SQLite database. No external MySQL server is required!
   Run the ETL script once to populate the database from the raw data:
   ```bash
   python -m src.etl
   ```

4. **Launch Dashboard**:
   ```bash
   streamlit run main.py
   ```
