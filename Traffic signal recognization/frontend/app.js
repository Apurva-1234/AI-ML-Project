const API_URL = 'http://127.0.0.1:8000';


const imageUpload = document.getElementById('imageUpload');
const imagePreview = document.getElementById('imagePreview');
const previewContainer = document.getElementById('previewContainer');
const uploadPlaceholder = document.getElementById('uploadPlaceholder');
const resultsContent = document.getElementById('resultsContent');
const noResults = document.getElementById('noResults');
const loadingResults = document.getElementById('loadingResults');
const predictedClass = document.getElementById('predictedClass');
const confidenceText = document.getElementById('confidenceText');
const confidenceBar = document.getElementById('confidenceBar');


const webcamVideo = document.getElementById('webcamVideo');
const webcamCanvas = document.getElementById('webcamCanvas');
const webcamContainer = document.getElementById('webcamContainer');
const webcamBtnText = document.getElementById('webcamBtnText');

let isWebcamActive = false;
let webcamInterval = null;


imageUpload.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    
    const reader = new FileReader();
    reader.onload = (event) => {
        stopWebcam(); // Stop webcam if active
        imagePreview.src = event.target.result;
        imagePreview.classList.remove('hidden');
        uploadPlaceholder.classList.add('hidden');
        webcamContainer.classList.add('hidden');

        predictImage(file);
    };
    reader.readAsDataURL(file);
});

async function predictImage(file) {
    showLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            displayResults(data);
        } else {
            alert(data.message || 'Error predicting image');
            showLoading(false);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Could not connect to backend server. Make sure FastAPI is running.');
        showLoading(false);
    }
}

function displayResults(data) {
    showLoading(false);
    noResults.classList.add('hidden');
    resultsContent.classList.remove('hidden');

    predictedClass.innerText = data.class_name;
    const confScore = (data.confidence * 100).toFixed(1);
    confidenceText.innerText = `${confScore}%`;
    confidenceBar.style.width = `${confScore}%`;

    // Animate color based on confidence
    if (confScore < 50) {
        confidenceBar.className = 'bg-red-500 h-full transition-all duration-500';
    } else if (confScore < 80) {
        confidenceBar.className = 'bg-yellow-500 h-full transition-all duration-500';
    } else {
        confidenceBar.className = 'bg-blue-500 h-full transition-all duration-500';
    }
}

function showLoading(isLoading) {
    if (isLoading) {
        loadingResults.classList.remove('hidden');
        resultsContent.classList.add('hidden');
        noResults.classList.add('hidden');
    } else {
        loadingResults.classList.add('hidden');
    }
}


async function toggleWebcam() {
    if (isWebcamActive) {
        stopWebcam();
    } else {
        startWebcam();
    }
}

async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        webcamVideo.srcObject = stream;

        isWebcamActive = true;
        webcamBtnText.innerText = 'Stop Webcam';

        imagePreview.classList.add('hidden');
        uploadPlaceholder.classList.add('hidden');
        webcamContainer.classList.remove('hidden');

        
        webcamInterval = setInterval(captureWebcamFrame, 1000); // 1 frame per second
    } catch (err) {
        console.error('Error accessing webcam:', err);
        alert('Could not access webcam. Please check permissions.');
    }
}

function stopWebcam() {
    if (webcamVideo.srcObject) {
        webcamVideo.srcObject.getTracks().forEach(track => track.stop());
    }
    isWebcamActive = false;
    webcamBtnText.innerText = 'Start Webcam';
    clearInterval(webcamInterval);
    webcamContainer.classList.add('hidden');
    uploadPlaceholder.classList.remove('hidden');
}

async function captureWebcamFrame() {
    if (!isWebcamActive) return;

    const context = webcamCanvas.getContext('2d');
    webcamCanvas.width = webcamVideo.videoWidth;
    webcamCanvas.height = webcamVideo.videoHeight;
    context.drawImage(webcamVideo, 0, 0, webcamCanvas.width, webcamCanvas.height);

    const base64Image = webcamCanvas.toDataURL('image/jpeg');

    try {
        const response = await fetch(`${API_URL}/predict_base64`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: base64Image })
        });

        const data = await response.json();
        if (response.ok) {
            displayResults(data);
        }
    } catch (error) {
        console.error('Webcam prediction error:', error);
    }
}


async function startTraining() {
    if (!confirm('This will start the model training process on the server. It may take several minutes. Continue?')) return;

    try {
        const response = await fetch(`${API_URL}/train`, { method: 'POST' });
        const data = await response.json();
        alert(data.message);
        pollTrainingStatus();
    } catch (error) {
        alert('Error starting training');
    }
}

function pollTrainingStatus() {
    const statusDiv = document.getElementById('trainingStatus');
    const label = document.getElementById('statusLabel');
    const progress = document.getElementById('statusProgress');
    const progressFill = document.getElementById('trainingProgress');

    statusDiv.classList.remove('hidden');

    const interval = setInterval(async () => {
        try {
            const response = await fetch(`${API_URL}/train/status`);
            const data = await response.json();

            label.innerText = `Status: ${data.status.charAt(0).toUpperCase() + data.status.slice(1)}`;

            if (data.status === 'completed') {
                progressFill.style.width = '100%';
                progress.innerText = '100%';
                clearInterval(interval);
                alert('Training finished successfully!');
                if (data.history) updateChart(data.history);
            } else if (data.status === 'training') {
                
                let p = parseInt(progress.innerText) || 0;
                if (p < 95) p += 1;
                progress.innerText = `${p}%`;
                progressFill.style.width = `${p}%`;
            } else if (data.status === 'failed') {
                clearInterval(interval);
                alert('Training failed: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Status poll error:', error);
        }
    }, 3000);
}

function updateChart(history) {
    const ctx = document.getElementById('metricsChart').getContext('2d');
    document.getElementById('chartPlaceholder').classList.add('hidden');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: history.accuracy.length }, (_, i) => i + 1),
            datasets: [{
                label: 'Training Accuracy',
                data: history.accuracy,
                borderColor: '#60a5fa',
                tension: 0.1
            }, {
                label: 'Validation Accuracy',
                data: history.val_accuracy,
                borderColor: '#c084fc',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: false, grid: { color: 'rgba(255,255,255,0.05)' } },
                x: { grid: { color: 'rgba(255,255,255,0.05)' } }
            },
            plugins: {
                legend: { labels: { color: '#f8fafc' } }
            }
        }
    });
}
