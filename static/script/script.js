async function analyzeWebsite() {
    const inputField = document.getElementById('featureInput').value;
    const resultCard = document.getElementById('resultCard');
    const verdictBox = document.getElementById('verdictBox');
    const verdictText = document.getElementById('verdictText');
    const confidenceScore = document.getElementById('confidenceScore');

    // 1. Parse the input string into an array of integers
    // Example input: "1, -1, 0, 1..."
    const featuresArray = inputField.split(',').map(item => parseInt(item.trim(), 10));

    // Validate we have exactly 30 features
    if (featuresArray.length !== 30 || featuresArray.some(isNaN)) {
        alert("Please enter exactly 30 valid comma-separated numbers (-1, 0, or 1).");
        return;
    }

    resultCard.style.display = 'block';
    verdictText.textContent = "Analyzing network traffic...";
    verdictBox.className = "verdict-box";

    try {
        // 2. Call the FastAPI backend
        // Make sure your FastAPI server is running on port 8000
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ features: featuresArray })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // 3. Update the UI with the backend's response
        verdictText.textContent = data.verdict;

        // Convert confidence from decimal (e.g., 0.96) to percentage (96%)
        const percentage = (data.confidenceScore * 100).toFixed(2);
        confidenceScore.textContent = `${percentage}%`;

        // Apply dynamic styling based on the verdict
        if (data.verdict === "Legitimate") {
            verdictBox.classList.add("verdict-safe");
        } else {
            verdictBox.classList.add("verdict-danger");
            verdictText.textContent = "⚠️ PHISHING DETECTED";
        }

    } catch (error) {
        console.error('Error:', error);
        verdictText.textContent = "Error connecting to backend";
        confidenceScore.textContent = "--";
    }
}