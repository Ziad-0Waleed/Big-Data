async function analyzeWebsite() {
    const urlInput = document.getElementById('urlInput').value.trim();
    const resultCard = document.getElementById('resultCard');
    const verdictBox = document.getElementById('verdictBox');
    const verdictText = document.getElementById('verdictText');
    const confidenceScore = document.getElementById('confidenceScore');

    if (!urlInput) {
        alert("Please enter a valid URL.");
        return;
    }

    resultCard.style.display = 'block';
    verdictText.textContent = "Analyzing URL structure and network signatures...";
    verdictBox.className = "verdict-box";

    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            // We now send the URL directly in the JSON payload
            body: JSON.stringify({ url: urlInput })
        });

        if (!response.ok) throw new Error(`Server error`);

        const data = await response.json();

        verdictText.textContent = data.verdict;
        const percentage = (data.confidenceScore * 100).toFixed(2);
        confidenceScore.textContent = `${percentage}%`;

        if (data.verdict === "Legitimate") {
            verdictBox.classList.add("verdict-safe");
        } else {
            verdictBox.classList.add("verdict-danger");
            verdictText.textContent = "⚠️ PHISHING DETECTED";
        }

    } catch (error) {
        console.error('Error:', error);
        verdictText.textContent = "Error connecting to scanning engine.";
        confidenceScore.textContent = "--";
    }
}