# TOPSIS Web Service Frontend

A complete web service for TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) analysis.

## Features

✨ **Modern Web Interface**
- Beautiful, responsive UI
- Real-time form validation
- Clean data visualization

📊 **TOPSIS Analysis**
- Upload CSV files
- Specify weights and impacts
- Automatic calculation of TOPSIS scores and ranks
- Email delivery of results

🔐 **Validation**
- Email format validation
- Weights and impacts format validation
- CSV file validation
- Numeric data verification

📧 **Email Integration**
- Automatic result delivery
- CSV attachment with results

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure Email (Optional)**

To enable email functionality, edit `app.py` and update these lines:
```python
sender_email = "your_email@gmail.com"      # Change this
sender_password = "your_app_password"      # Use Gmail app-specific password
```

For Gmail:
1. Enable 2-factor authentication
2. Generate an app-specific password: https://myaccount.google.com/apppasswords
3. Use the app password in the code above

## Usage

1. **Start the server:**
```bash
python app.py
```

2. **Open browser:**
Navigate to `http://localhost:5000`

3. **Use the web interface:**
   - Select a CSV file
   - Enter weights (comma-separated, e.g., 1,1,1,1)
   - Enter impacts (comma-separated, + for beneficial, - for non-beneficial)
   - Enter email address
   - Click "Submit Analysis"

## Input File Format

CSV file with the following structure:
- **First Column:** Alternative/Option names
- **Remaining Columns:** Numeric criteria values
- **Minimum 3 columns required**

### Example:
```csv
Fund Name,P1,P2,P3,P4
M1,0.67,0.45,6.5,42.6
M2,0.6,0.36,3.6,53.3
M3,0.82,0.67,3.8,63.1
M4,0.6,0.36,3.5,69.2
```

## Parameters

### Weights
- Numeric values separated by commas
- Example: `1,1,1,1` or `2,3,1.5,2`
- Number of weights must equal number of criteria

### Impacts
- `+` for criteria to maximize (beneficial)
- `-` for criteria to minimize (non-beneficial)
- Example: `+,+,-,+`
- Number of impacts must equal number of weights

### Email
- Valid email address format
- Results will be sent as CSV attachment

## Output

The results include:
- **Topsis Score:** Value between 0 and 1 indicating performance
- **Rank:** Position in ranking (1 = best performer)

Higher Topsis Score = Better performance

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main page |
| `/api/upload` | POST | Process TOPSIS analysis |
| `/api/download/<filename>` | GET | Download result file |
| `/api/example` | GET | Get example data |

## File Structure

```
frontend/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # CSS styles
│   └── script.js         # JavaScript functionality
├── uploads/              # Uploaded files (auto-created)
└── results/              # Result files (auto-created)
```

## Troubleshooting

**Port 5000 already in use:**
```bash
python app.py  # Add custom port
# Or modify: app.run(port=5001)
```

**Email not sending:**
- Verify sender email and password in app.py
- Check internet connection
- For Gmail, ensure app-specific password is used
- Check spam/trash folders

**File upload failed:**
- Ensure CSV file is valid
- Check file size (max 16MB)
- Verify file has proper CSV format

## Theory - TOPSIS Method

TOPSIS determines the optimal solution by finding the alternative that is:
1. **Closest to the Ideal Best solution**
2. **Farthest from the Ideal Worst solution**

The Topsis Score (also called Relative Closeness) ranges from 0 to 1:
- Score closer to 1: Better alternative
- Score closer to 0: Worse alternative

## License

This project is part of the TOPSIS implementation assignment.

## Author

Created as Part 3 of the TOPSIS Analysis Project

## Support

For issues or questions, refer to the main TOPSIS package documentation.
