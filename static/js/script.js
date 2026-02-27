// Add Farmer
document.getElementById("farmerForm").addEventListener("submit", function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    fetch("/add_farmer", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        this.reset();
		location.reload();
    });
});

// Predict Yield
function predictYield() {
    let soil = document.getElementById("soil").value;
    let rainfall = document.getElementById("rainfall").value;

    fetch("/predict_yield", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ soil: soil, rainfall: rainfall })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText =
            "Predicted Yield: " + data.yield_prediction;
    });
}
function recommendCrop() {
    let soil = document.getElementById("soil_type").value;
    let rainfall = document.getElementById("rainfall_crop").value;
    let temperature = document.getElementById("temperature").value;

    fetch("/recommend_crop", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            soil_type: soil,
            rainfall: rainfall,
            temperature: temperature
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("crop_result").innerText =
            "Recommended Crop: " + data.recommended_crop;
    });
}
function fertilizerAdvice() {
    let nitrogen = document.getElementById("nitrogen").value;

    fetch("/fertilizer_advice", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ nitrogen: nitrogen })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("fertilizer_result").innerText =
            data.fertilizer_advice;
    });
}