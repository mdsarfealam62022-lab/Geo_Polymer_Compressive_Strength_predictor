document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("predictionForm");
    const resultDiv = document.getElementById("predictionResult");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = parseFloat(value);
        });

        resultDiv.style.display = "block";
        resultDiv.innerHTML = "🔄 Predicting...";

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok && result.prediction !== undefined) {
                resultDiv.innerHTML = `✅ Predicted Strength: <strong>${result.prediction.toFixed(2)} MPa</strong>`;
                resultDiv.className = "success";
            } else {
                resultDiv.innerHTML = `❌ Error: ${result.error || "Unknown error"}`;
                resultDiv.className = "error";
            }

        } catch (err) {
            resultDiv.innerHTML = "❌ Could not connect to server.";
            resultDiv.className = "error";
            console.error(err);
        }
    });

   form.addEventListener("reset", () => {
    const inputs = form.querySelectorAll("input[type='number']");
    inputs.forEach(input => input.value = input.dataset.default || 0);
    resultDiv.style.display = "none";
    resultDiv.innerHTML = "";
    resultDiv.className = "";
});

    });

    
