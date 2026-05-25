async function analyzeLead() {
    const name = document.getElementById("name").value.trim();
    const company = document.getElementById("company").value.trim();
    const industry = document.getElementById("industry").value.trim();
    const size = document.getElementById("size").value.trim();
    const budget = document.getElementById("budget").value.trim();
    const problem = document.getElementById("problem").value.trim();

    if (!name || !company || !industry || !size || !budget || !problem) {
        alert("Please fill all fields.");
        return;
    }

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("result-box").classList.add("hidden");

    const response = await fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name,
            company,
            industry,
            size,
            budget,
            problem
        })
    });

    const data = await response.json();

    document.getElementById("loading").classList.add("hidden");
    document.getElementById("result-box").classList.remove("hidden");
    document.getElementById("result").textContent = data.result;

    updateScoreBadge(data.result);
}

function updateScoreBadge(resultText) {
    const badge = document.getElementById("score-badge");

    badge.className = "";
    badge.style.display = "block";

    if (resultText.includes("Hot")) {
        badge.textContent = "🔥 HOT LEAD";
        badge.classList.add("hot");
    } else if (resultText.includes("Warm")) {
        badge.textContent = "🌤️ WARM LEAD";
        badge.classList.add("warm");
    } else {
        badge.textContent = "❄️ COLD LEAD";
        badge.classList.add("cold");
    }
}

function clearForm() {
    document.getElementById("name").value = "";
    document.getElementById("company").value = "";
    document.getElementById("industry").value = "";
    document.getElementById("size").value = "";
    document.getElementById("budget").value = "";
    document.getElementById("problem").value = "";

    document.getElementById("result-box").classList.add("hidden");
    document.getElementById("score-badge").style.display = "none";
}

function copyResult() {
    const text = document.getElementById("result").textContent;
    navigator.clipboard.writeText(text);
    alert("Copied to clipboard!");
}

function downloadReport() {
    const text = document.getElementById("result").textContent;

    const blob = new Blob([text], { type: "text/plain" });
    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);
    link.download = "lead-analysis-report.txt";

    link.click();
}