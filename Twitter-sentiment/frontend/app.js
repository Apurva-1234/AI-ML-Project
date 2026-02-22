const API_URL = "http://127.0.0.1:8000/predict";


document.getElementById('tweetInput').addEventListener('input', function () {
    const count = this.value.length;
    document.getElementById('charCount').textContent = count;

    if (count > 500) {
        this.style.borderColor = '#ef4444';
    } else {
        this.style.borderColor = '#e0e0e0';
    }
});

async function predictSentiment() {
    const tweet = document.getElementById("tweetInput").value.trim();
    const result = document.getElementById("result");
    const resultContent = document.getElementById("resultContent");
    const analyzeBtn = document.getElementById("analyzeBtn");

    if (!tweet) {
        showNotification("Please enter some text to analyze.", "error");
        return;
    }

    if (tweet.length > 500) {
        showNotification("Tweet exceeds maximum length of 500 characters.", "error");
        return;
    }


    analyzeBtn.classList.add("loading");
    analyzeBtn.disabled = true;
    result.classList.add("hidden");

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tweet })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();


        let sentimentClass = '';
        let sentimentIcon = '';

        if (data.sentiment === "Positive") {
            sentimentClass = 'sentiment-positive';
            sentimentIcon = '😊';
        } else if (data.sentiment === "Neutral") {
            sentimentClass = 'sentiment-neutral';
            sentimentIcon = '😐';
        } else {
            sentimentClass = 'sentiment-negative';
            sentimentIcon = '😞';
        }

        resultContent.innerHTML = `
            <div style="text-align: center">
                <div style="font-size: 4rem; margin-bottom: 1rem">${sentimentIcon}</div>
                <div class="${sentimentClass}">${data.sentiment}</div>
                <div style="margin-top: 1rem; color: #666">
                    Confidence: ${(data.confidence * 100).toFixed(1)}%
                </div>
                <div style="margin-top: 0.5rem; color: #999; font-size: 0.9rem">
                    Response time: ${data.latency_ms}ms
                </div>
            </div>
        `;

        result.classList.remove("hidden");
        showNotification("Analysis complete!", "success");

    } catch (error) {
        console.error('Error:', error);
        resultContent.innerHTML = `
            <div style="text-align: center; color: #ef4444">
                <div style="font-size: 3rem; margin-bottom: 1rem">❌</div>
                <div>Failed to connect to backend.</div>
                <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #999">
                    Make sure the server is running at ${API_URL}
                </div>
            </div>
        `;
        result.classList.remove("hidden");
        showNotification("Backend connection failed", "error");
    } finally {

        analyzeBtn.classList.remove("loading");
        analyzeBtn.disabled = false;
    }
}

function showNotification(message, type) {
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">${type === 'success' ? '✅' : '❌'}</span>
            <span class="notification-message">${message}</span>
        </div>
    `;

    document.body.appendChild(notification);


    setTimeout(() => notification.classList.add("show"), 10);


    setTimeout(() => {
        notification.classList.remove("show");
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('tweetInput').focus();
});