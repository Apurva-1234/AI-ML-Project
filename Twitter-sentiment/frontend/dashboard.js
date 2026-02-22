let sentimentChart;
let updateInterval;


function initChart() {
    const ctx = document.getElementById("sentimentChart").getContext("2d");
    
    sentimentChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [
                {
                    label: "Positive %",
                    data: [],
                    borderColor: "#10b981",
                    backgroundColor: "rgba(16, 185, 129, 0.1)",
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: "Neutral %",
                    data: [],
                    borderColor: "#f59e0b",
                    backgroundColor: "rgba(245, 158, 11, 0.1)",
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: "Negative %",
                    data: [],
                    borderColor: "#ef4444",
                    backgroundColor: "rgba(239, 68, 68, 0.1)",
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Percentage (%)'
                    }
                }
            }
        }
    });
}


function updateStats(data) {
    let positive = 0, neutral = 0, negative = 0;
    
    data.forEach(item => {
        positive += item.positive_count || 0;
        neutral += item.neutral_count || 0;
        negative += item.negative_count || 0;
    });

    const total = positive + neutral + negative;

    document.getElementById("positiveCount").textContent = positive;
    document.getElementById("neutralCount").textContent = neutral;
    document.getElementById("negativeCount").textContent = negative;
    document.getElementById("totalCount").textContent = total;
}


function updateRecentTable(predictions) {
    const tbody = document.getElementById("recentTableBody");
    
    if (!predictions || predictions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="2" class="loading-message">No data available</td></tr>';
        return;
    }

    // Get last 10 predictions
    const recent = predictions.slice(-10).reverse();
    
    tbody.innerHTML = recent.map(p => {
        let sentimentClass = '';
        let icon = '';
        
        if (p.sentiment === "Positive") {
            sentimentClass = 'sentiment-positive';
            icon = '😊';
        } else if (p.sentiment === "Neutral") {
            sentimentClass = 'sentiment-neutral';
            icon = '😐';
        } else {
            sentimentClass = 'sentiment-negative';
            icon = '😞';
        }
        
        return `
            <tr>
                <td>${new Date(p.time).toLocaleTimeString()}</td>
                <td><span class="${sentimentClass}">${icon} ${p.sentiment}</span></td>
            </tr>
        `;
    }).join('');
}


async function loadStats() {
    try {
        const response = await fetch("http://127.0.0.1:8000/stats");
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();

        if (data && data.length > 0) {
            
            sentimentChart.data.labels = data.map(d => d.time);
            sentimentChart.data.datasets[0].data = data.map(d => d.positive_pct);
            sentimentChart.data.datasets[1].data = data.map(d => d.neutral_pct || 0);
            sentimentChart.data.datasets[2].data = data.map(d => d.negative_pct);
            sentimentChart.update();

           
            updateStats(data);
        }

        
        try {
            const recentResponse = await fetch("http://127.0.0.1:8000/recent");
            if (recentResponse.ok) {
                const recentData = await recentResponse.json();
                updateRecentTable(recentData);
            } else {
                document.getElementById("recentTableBody").innerHTML = 
                    '<tr><td colspan="2" class="loading-message">Make a prediction to see results</td></tr>';
            }
        } catch (recentError) {
            console.log("Recent endpoint not available:", recentError);
            document.getElementById("recentTableBody").innerHTML = 
                '<tr><td colspan="2" class="loading-message">Connect to backend to see recent data</td></tr>';
        }

    } catch (error) {
        console.error("Error loading dashboard:", error);
        // FIXED: Don't add duplicate error messages
        const chartContainer = document.querySelector('.chart-container');
        // Check if error message already exists
        if (!chartContainer.querySelector('.error-message')) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.style.cssText = 'text-align: center; color: #ef4444; padding: 2rem;';
            errorDiv.textContent = 'Failed to connect to backend. Make sure the server is running.';
            chartContainer.appendChild(errorDiv);
        }
    }
}


document.addEventListener('DOMContentLoaded', function() {
    initChart();
    loadStats();
    
    
    updateInterval = setInterval(loadStats, 5000);
});


window.addEventListener('beforeunload', function() {
    if (updateInterval) {
        clearInterval(updateInterval);
    }
});