from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>Tomato Disease Detector</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .upload-box { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; cursor: pointer; }
        .result { background: #f5f5f5; padding: 20px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍅 Tomato Disease Detection</h1>
        <p>Using your deployed ML model</p>
        
        <div class="upload-box" onclick="document.getElementById('fileInput').click()">
            <h3>Click to Upload Tomato Leaf Image</h3>
            <input type="file" id="fileInput" hidden accept="image/*">
        </div>
        
        <div id="result" class="result">
            <p>Upload an image to see detection results</p>
        </div>
    </div>

    <script>
    document.getElementById('fileInput').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            analyzeImage(file);
        }
    });

    async function analyzeImage(file) {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '<p>🔍 Analyzing image...</p>';
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            resultDiv.innerHTML = `
                <h3>✅ Detection Result:</h3>
                <p><strong>Disease:</strong> ${data.prediction.class}</p>
                <p><strong>Confidence:</strong> ${(data.prediction.confidence * 100).toFixed(2)}%</p>
                <p><strong>Status:</strong> ${data.status}</p>
            `;
            
        } catch (error) {
            resultDiv.innerHTML = '<p>❌ Error: API not responding</p>';
        }
    }
    </script>
</body>
</html>
"""

@app.get("/")
async def home():
    return HTMLResponse(HTML_CODE)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Tera existing prediction code yahan rahega
    return {"prediction": {"class": "Tomato_Healthy", "confidence": 0.95}, "status": "success"}

@app.get("/health")
def health():
    return {"status": "healthy"}