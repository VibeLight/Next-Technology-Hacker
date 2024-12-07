// ボタンを押すとAPIを呼び出して結果を取得
function runTool(tool) {
    fetch(`/run_tool/${tool}`)
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById(`${tool}_result`);
            resultDiv.textContent = JSON.stringify(data, null, 4);
        })
        .catch(error => {
            console.error("Error:", error);
        });
}
