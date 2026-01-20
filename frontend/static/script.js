// DOM Elements
const form = document.getElementById('topsisForm');
const fileInput = document.getElementById('fileInput');
const submitBtn = document.getElementById('submitBtn');
const messageBox = document.getElementById('messageBox');
const resultsSection = document.getElementById('resultsSection');
const resultsContent = document.getElementById('resultsContent');

// File input label update
fileInput.addEventListener('change', (e) => {
    const label = document.querySelector('.file-input-label');
    if (e.target.files.length > 0) {
        label.textContent = '✓ ' + e.target.files[0].name;
        label.style.color = '#27ae60';
        label.style.borderColor = '#27ae60';
    } else {
        label.textContent = '📁 Choose CSV File';
        label.style.color = '#667eea';
        label.style.borderColor = '#667eea';
    }
});

// Make label clickable to trigger file input
document.addEventListener('DOMContentLoaded', () => {
    const label = document.querySelector('.file-input-label');
    const fileInput = document.getElementById('fileInput');
    if (label && fileInput) {
        label.addEventListener('click', (e) => {
            e.preventDefault();
            fileInput.click();
        });
    }
});

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Validate form
    if (!validateForm()) {
        return;
    }
    
    // Show loading state
    submitBtn.disabled = true;
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<div class="spinner"></div><span class="btn-text">Processing...</span>';
    
    try {
        // Prepare form data
        const formData = new FormData(form);
        
        // Send request
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(data.message, 'success');
            displayResults(data);
            form.reset();
            const label = document.querySelector('.file-input-label');
            label.textContent = '📁 Choose CSV File';
            label.style.color = '#667eea';
            label.style.borderColor = '#667eea';
        } else {
            showMessage(data.message, 'error');
        }
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
});

// Form validation
function validateForm() {
    const weights = document.getElementById('weightsInput').value.trim();
    const impacts = document.getElementById('impactsInput').value.trim();
    const email = document.getElementById('emailInput').value.trim();
    const file = fileInput.files[0];
    
    // Check file
    if (!file) {
        showMessage('Please select a CSV file', 'error');
        return false;
    }
    
    if (!file.name.endsWith('.csv')) {
        showMessage('Please select a CSV file', 'error');
        return false;
    }
    
    // Check weights
    if (!weights) {
        showMessage('Please enter weights', 'error');
        return false;
    }
    
    const weightsArray = weights.split(',').map(w => w.trim());
    if (weightsArray.some(w => isNaN(parseFloat(w)) || w === '')) {
        showMessage('Weights must be numeric values separated by commas', 'error');
        return false;
    }
    
    // Check impacts
    if (!impacts) {
        showMessage('Please enter impacts', 'error');
        return false;
    }
    
    const impactsArray = impacts.split(',').map(i => i.trim());
    if (impactsArray.some(i => i !== '+' && i !== '-')) {
        showMessage('Impacts must be "+" or "-" separated by commas', 'error');
        return false;
    }
    
    // Check if weights and impacts count match
    if (weightsArray.length !== impactsArray.length) {
        showMessage('Number of weights and impacts must be equal', 'error');
        return false;
    }
    
    // Check email
    if (!email) {
        showMessage('Please enter an email address', 'error');
        return false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showMessage('Please enter a valid email address', 'error');
        return false;
    }
    
    return true;
}

// Show message
function showMessage(message, type) {
    messageBox.textContent = message;
    messageBox.className = `message-box ${type}`;
    messageBox.style.display = 'block';
    
    // Auto-hide message after 5 seconds (for success)
    if (type === 'success') {
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, 5000);
    }
    
    // Scroll to message
    messageBox.scrollIntoView({ behavior: 'smooth' });
}

// Display results
function displayResults(data) {
    let html = '';
    
    // Summary
    html += `<div class="result-item">
                <h4>✓ Analysis Complete</h4>
                <p><strong>Total Records Processed:</strong> ${data.total_rows}</p>
                <p><strong>Result File:</strong> ${data.result_file}</p>
                <p><strong>Email Status:</strong> ${data.email_status}</p>
                <a href="/api/download/${data.result_file}" class="download-btn">📥 Download Results</a>
            </div>`;
    
    // Data preview
    if (data.data_preview && data.data_preview.length > 0) {
        html += `<div class="result-item">
                    <h4>📊 Data Preview (First 5 Records)</h4>
                    ${buildTable(data.data_preview)}
                </div>`;
    }
    
    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Build table HTML
function buildTable(data) {
    if (!data || data.length === 0) return '<p>No data available</p>';
    
    const columns = Object.keys(data[0]);
    let html = '<table class="data-table"><thead><tr>';
    
    // Header
    columns.forEach(col => {
        html += `<th>${escapeHtml(col)}</th>`;
    });
    html += '</tr></thead><tbody>';
    
    // Rows
    data.forEach(row => {
        html += '<tr>';
        columns.forEach(col => {
            const value = row[col];
            const displayValue = typeof value === 'number' ? value.toFixed(4) : value;
            html += `<td>${escapeHtml(displayValue)}</td>`;
        });
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    return html;
}

// Escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

// Load example data on page load
window.addEventListener('DOMContentLoaded', () => {
    // You can add additional initialization here if needed
});
