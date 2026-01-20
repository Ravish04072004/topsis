# 🚀 Installation & Deployment Guide

## System Requirements

- **Python:** 3.7 or higher
- **RAM:** 512 MB minimum
- **Storage:** 100 MB available
- **OS:** Windows, macOS, or Linux

---

## 📦 Installation Steps

### Step 1: Navigate to Frontend Folder

**Windows:**
```cmd
cd frontend
```

**Mac/Linux:**
```bash
cd frontend
```

### Step 2: Install Dependencies

**Automatic (Recommended):**

Windows - Just double-click:
```
run_server.bat
```

Mac/Linux - Run:
```bash
chmod +x run_server.sh
./run_server.sh
```

**Manual Installation:**

Windows:
```cmd
pip install -r requirements.txt
```

Mac/Linux:
```bash
pip3 install -r requirements.txt
```

### Step 3: Run the Server

**Using Script (Easiest):**
- Windows: Double-click `run_server.bat`
- Mac/Linux: Run `./run_server.sh`

**Using Python Directly:**

Windows:
```cmd
python app.py
```

Mac/Linux:
```bash
python3 app.py
```

### Step 4: Access the Application

Open your browser and go to:
```
http://localhost:5000
```

---

## 🔧 Optional: Configure Email

To enable automatic email delivery of results:

1. **Open `app.py`** in a text editor
2. **Find lines 28-29:**
   ```python
   sender_email = "your_email@gmail.com"
   sender_password = "your_app_password"
   ```

3. **For Gmail users:**
   - Enable 2-factor authentication: https://myaccount.google.com/security
   - Go to App Passwords: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or your OS)
   - Copy the generated password
   - Paste in `sender_password` above

4. **For other email providers:**
   - Use SMTP credentials
   - Modify SMTP server and port if needed (lines 140-141)

---

## 🧪 Testing

### Test with Sample Data

1. Open the web application
2. Click "Choose File" and select `sample_data.csv`
3. Enter Weights: `1,1,1,1`
4. Enter Impacts: `+,+,-,+`
5. Enter Email: (your email to test)
6. Click "Submit Analysis"
7. See results on page

### Expected Results

You should see:
- ✓ Analysis completion message
- ✓ Data preview table
- ✓ Download button
- ✓ Email status
- ✓ Results file with Topsis Score and Rank columns

---

## 📋 First Run Troubleshooting

### Issue: "Python not found"

**Solution:**
- Ensure Python 3.7+ is installed
- Add Python to PATH (Windows)
- Use `python3` instead of `python` (Mac/Linux)

### Issue: "Port 5000 already in use"

**Solution:**
Edit `app.py`, find the last line:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

Change to:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

Then access: `http://localhost:5001`

### Issue: "Module not found"

**Solution:**
Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Issue: "Email not sending"

**Solution:**
- Verify sender_email and sender_password in `app.py`
- Check internet connection
- For Gmail: Ensure using app-specific password, not regular password
- Check spam/trash folders for test emails

---

## 🎯 Using the Application

### Basic Workflow

1. **Prepare Data**
   - CSV file with options in column 1
   - Numeric criteria in columns 2+
   - Minimum 3 columns required

2. **Upload & Configure**
   - Upload your CSV file
   - Enter weights (comma-separated)
   - Enter impacts (+ or -, comma-separated)
   - Enter recipient email

3. **Analyze**
   - Click "Submit Analysis"
   - Wait for processing (usually < 5 seconds)

4. **Get Results**
   - View preview on page
   - Download CSV file
   - Check email for results (if configured)

### Input Format Example

**CSV File (data.csv):**
```csv
Fund Name,P1,P2,P3,P4
M1,0.67,0.45,6.5,42.6
M2,0.6,0.36,3.6,53.3
M3,0.82,0.67,3.8,63.1
```

**Form Inputs:**
- Weights: `1,1,1,1`
- Impacts: `+,+,-,+`
- Email: `user@example.com`

**Output CSV (result_YYYYMMDD_HHMMSS.csv):**
```csv
Fund Name,P1,P2,P3,P4,Topsis Score,Rank
M1,0.67,0.45,6.5,42.6,0.7832,2
M2,0.6,0.36,3.6,53.3,0.5421,3
M3,0.82,0.67,3.8,63.1,0.8945,1
```

---

## 💾 File Management

### Uploaded Files
- Stored in: `uploads/` folder
- Automatically created on first upload
- Safe to delete old files

### Result Files
- Stored in: `results/` folder
- Named with timestamp: `result_YYYYMMDD_HHMMSS.csv`
- Keep important results backed up

---

## 🌐 Network Access

### Local Only (Default)
Server runs on: `http://localhost:5000`
- Only accessible from your computer

### Network Access (Optional)
To allow other computers on your network to access:

Edit last line of `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
(Already set to allow network access)

Find your computer's IP:
- Windows: `ipconfig` (look for IPv4 Address)
- Mac/Linux: `ifconfig` (look for inet)

Other users can access: `http://YOUR_IP:5000`

---

## 📊 Advanced Usage

### Batch Processing
Process multiple files by uploading them sequentially through the web interface.

### Different Criteria
Adjust weights and impacts for different scenarios:
- Equal weights: `1,1,1,1`
- Priority weights: `3,2,1,1`
- All maximize: `+,+,+,+`
- All minimize: `-,-,-,-`

### Result Analysis
- Downloaded CSV can be opened in Excel
- Import into other analysis tools
- Use Rank column for decision making

---

## 🔐 Security Notes

- Files are validated before processing
- Invalid data is rejected with clear error messages
- Uploaded files are temporary
- Email credentials should be kept private
- Use app-specific passwords, not actual account password

---

## 📝 Logs & Debugging

### Enable Debug Mode
Edit `app.py`, last line:
```python
app.run(debug=True, ...)  # Currently enabled
```

### View Logs
- Run in terminal to see real-time logs
- Error messages appear in terminal and on page

---

## 🚀 Deployment

### For Production

Replace in `app.py`:
```python
# Before (development)
app.run(debug=True, host='0.0.0.0', port=5000)

# After (production)
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Using Gunicorn (Production Server)

Install:
```bash
pip install gunicorn
```

Run:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t topsis-web .
docker run -p 5000:5000 topsis-web
```

---

## ✅ Verification

After installation, verify everything works:

1. ✓ Server starts without errors
2. ✓ Web interface loads at localhost:5000
3. ✓ Sample file uploads successfully
4. ✓ Results display with Topsis Score and Rank
5. ✓ Download button works
6. ✓ Email sends (if configured)

---

## 📞 Support

- Check **QUICKSTART.md** for quick start
- Check **README.md** for detailed docs
- Check **IMPLEMENTATION_REPORT.md** for technical details
- Review error messages carefully
- Ensure all dependencies are installed

---

## 🎉 You're Ready!

The TOPSIS Web Service is now installed and ready to use.

**Start with:** `run_server.bat` or `./run_server.sh`

**Access at:** `http://localhost:5000`

**Happy analyzing! 📊**
