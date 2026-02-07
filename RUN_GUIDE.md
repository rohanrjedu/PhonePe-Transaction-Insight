# PhonePe Transaction Insight - Run Guide

## Prerequisites

Before running the application, ensure you have the following installed and configured:

### 1. MySQL Database
- MySQL server must be running
- Database name: `phonepe`
- Default credentials (configured in `src/config.py`):
  - Host: `localhost`
  - User: `root`
  - Password: `Rakesh@181969`

### 2. Python Environment
- Python 3.12 or higher
- Required packages (see `requirements.txt`):
  - streamlit >= 1.28.0
  - pandas >= 1.5.0
  - sqlalchemy >= 2.0.0
  - plotly >= 5.0.0
  - pymysql >= 1.1.0
  - cryptography >= 45.0.0
  - streamlit-option-menu >= 0.3.0

## Installation Steps

### Step 1: Install Dependencies

```bash
# Navigate to the project directory
cd /Users/rohanraj/GUVIPROJECTS/PhonePe-Transaction-Insight

# Install required Python packages
/usr/local/bin/python3 -m pip install -r requirements.txt
```

### Step 2: Verify MySQL Database

```bash
# Check if MySQL is running
pgrep mysql

# Verify the phonepe database exists
/usr/local/mysql-8.0.40-macos14-arm64/bin/mysql -u root -pRakesh@181969 -e "SHOW DATABASES;"

# Check if tables are populated
/usr/local/mysql-8.0.40-macos14-arm64/bin/mysql -u root -pRakesh@181969 -e "USE phonepe; SHOW TABLES;"
```

### Step 3: (Optional) Load/Reload Data

If you need to reload the data from JSON files into the database:

```bash
# Run the ETL script
/usr/local/bin/python3 -m src.etl
```

This will:
- Extract data from JSON files in the `data/` directory
- Transform the data into structured format
- Load it into the MySQL `phonepe` database

## Running the Application

### Start the Streamlit Dashboard

```bash
# Navigate to the project directory
cd /Users/rohanraj/GUVIPROJECTS/PhonePe-Transaction-Insight

# Run the Streamlit app
/usr/local/bin/python3 -m streamlit run main.py
```

The application will start and display:
```
Local URL: http://localhost:8501
Network URL: http://192.168.29.134:8501
```

### Access the Dashboard

Open your web browser and navigate to:
- **Local access**: http://localhost:8501
- **Network access** (from other devices): http://192.168.29.134:8501

## Dashboard Features

The dashboard provides 9 analytical scenarios:

1. **Decoding Transaction Dynamics** - Analyze transaction growth, stagnation, and decline
2. **Device Dominance & Engagement** - Device brand analysis and user engagement
3. **Insurance Penetration & Growth** - Insurance adoption trends
4. **Market Expansion Strategy** - Identify growth opportunities by state and district
5. **User Engagement & Growth** - Registered users and app opens analysis
6. **Insurance Engagement (Uptake)** - Insurance policy counts and amounts
7. **Top Transaction Performers** - Top pincodes by transaction volume
8. **Top User Registration** - Top pincodes by user registrations
9. **Top Insurance Performers** - Top pincodes by insurance policies

### Navigation

Use the **sidebar radio buttons** to select the scenario you want to analyze. Each scenario provides:
- Interactive filters (Year, Quarter, State, etc.)
- Dynamic visualizations (charts, maps, tables)
- Key metrics and insights

## Troubleshooting

### Issue: Command not found (pip, python)
**Solution**: Use the full path to Python:
```bash
/usr/local/bin/python3 -m pip install <package>
```

### Issue: MySQL connection error
**Solution**: 
1. Verify MySQL is running: `pgrep mysql`
2. Check credentials in `src/config.py`
3. Ensure the `phonepe` database exists

### Issue: Empty visualizations
**Solution**: 
1. Check if database tables have data:
   ```bash
   /usr/local/mysql-8.0.40-macos14-arm64/bin/mysql -u root -pRakesh@181969 -e "USE phonepe; SELECT COUNT(*) FROM aggregated_transaction;"
   ```
2. If empty, run the ETL script: `/usr/local/bin/python3 -m src.etl`

### Issue: Port already in use
**Solution**: 
- Stop the existing Streamlit process or use a different port:
  ```bash
  /usr/local/bin/python3 -m streamlit run main.py --server.port 8502
  ```

## Project Structure

```
PhonePe-Transaction-Insight/
├── main.py                    # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── RUN_GUIDE.md              # This file
├── data/                      # JSON data files
│   ├── aggregated/
│   ├── map/
│   └── top/
└── src/                       # Source code
    ├── __init__.py
    ├── config.py              # Database configuration
    ├── db.py                  # Database connection
    ├── etl.py                 # ETL pipeline
    └── case_studies.py        # Scenario implementations
```

## Quick Start (One Command)

For a quick start, run:

```bash
cd /Users/rohanraj/GUVIPROJECTS/PhonePe-Transaction-Insight && /usr/local/bin/python3 -m streamlit run main.py
```

## Notes

- The application uses a **dark theme** by default
- All visualizations are interactive (hover, zoom, pan)
- Data is refreshed from the database on each scenario selection
- For optimal performance, ensure your MySQL server has adequate resources

## Support

For issues or questions:
1. Check the console output for error messages
2. Verify all prerequisites are met
3. Review the troubleshooting section above
