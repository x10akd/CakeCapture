document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('floatingCirclesG').style.display = 'none';
    document.querySelector('.content').style.display = 'block';
    // 避免圖表跑版
    setTimeout(() => {
        document.querySelectorAll('.plotly-graph-div').forEach(chart => {
            Plotly.Plots.resize(chart);
        });
    }, 50);
});