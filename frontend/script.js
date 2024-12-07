document.getElementById("fetch-data").addEventListener("click", async () => {
    const response = await fetch("http://127.0.0.1:5000/collect");
    const data = await response.json();
    document.getElementById("data-display").textContent = JSON.stringify(data, null, 4);
});
