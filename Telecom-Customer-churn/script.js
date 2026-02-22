// Tab Switching Logic
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();

        // Update active link
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');

        // Switch section
        const targetSection = link.getAttribute('data-section');
        document.querySelectorAll('.tab-content').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(`${targetSection}-section`).classList.add('active');
    });
});

document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // Convert logic for numbers
    data.tenure = parseInt(data.tenure);
    data.SeniorCitizen = parseInt(data.SeniorCitizen);
    data.MonthlyCharges = parseFloat(data.MonthlyCharges);
    data.TotalCharges = data.MonthlyCharges * data.tenure; // Simple approximation for TotalCharges

    const btn = e.target.querySelector('button');
    const btnText = btn.querySelector('span');
    const originalText = btnText.textContent;

    try {
        btnText.textContent = 'Analyzing...';
        btn.disabled = true;

        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Prediction request failed');
        }

        const result = await response.json();
        displayResult(result);
    } catch (error) {
        console.error('Error:', error);
        alert('Could not connect to the Prediction API. Make sure the backend is running at localhost:8000');
    } finally {
        btnText.textContent = originalText;
        btn.disabled = false;
    }
});

function displayResult(result) {
    const card = document.getElementById('result-card');
    card.classList.remove('hidden');
    card.scrollIntoView({ behavior: 'smooth' });

    const probValue = result.churn_probability;
    const probPercent = Math.round(probValue * 100);

    // Update Text
    document.getElementById('probability-text').textContent = `${probPercent}%`;
    document.getElementById('churn-val').textContent = result.churn_prediction;
    document.getElementById('priority-val').textContent = result.risk_level === 'High' ? 'Critical' : result.risk_level === 'Medium' ? 'Moderate' : 'Low';

    const badge = document.getElementById('risk-level-badge');
    const alertBox = document.getElementById('churn-alert');
    const msg = document.getElementById('prediction-msg');
    const fill = document.getElementById('gauge-fill');

    // Styling based on risk
    let color = '#6366f1'; // primary
    if (probValue > 0.7) {
        color = '#ef4444'; // danger
        msg.textContent = "High risk of churn detected. Immediate retention campaign recommended.";
    } else if (probValue > 0.3) {
        color = '#f59e0b'; // warning
        msg.textContent = "Moderate risk. Consider loyalty offers or feedback surveys.";
    } else {
        color = '#22c55e'; // success
        msg.textContent = "Low risk. Customer is stable and likely to stay.";
    }

    badge.textContent = `${result.risk_level} Risk`;
    alertBox.style.borderLeftColor = color;
    fill.style.stroke = color;

    // Gauge Animation
    // Circumference of semi-circle: 125.6 (Pi * r where r=40)
    // We update stroke-dasharray
    const circumference = 125.6;
    const dash = (probValue * circumference);
    fill.style.strokeDasharray = `${dash}, ${circumference}`;
}
