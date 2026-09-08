/**
 * Chart.js Visualization Managers
 */

let comparisonChartInstance = null;
let historyChartInstance = null;
let advantageChartInstance = null;

const Charts = {
    // 1. Bar Chart: Selling Price vs MRP comparison
    renderPriceComparisonChart(canvasId, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        if (comparisonChartInstance) {
            comparisonChartInstance.destroy();
        }

        const amzPrice = data.amazon?.price || 0;
        const amzMrp = data.amazon?.mrp || amzPrice;
        const fpkPrice = data.flipkart?.price || 0;
        const fpkMrp = data.flipkart?.mrp || fpkPrice;

        comparisonChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Amazon India', 'Flipkart'],
                datasets: [
                    {
                        label: 'Selling Price (₹)',
                        data: [amzPrice, fpkPrice],
                        backgroundColor: ['#f59e0b', '#3b82f6'],
                        borderRadius: 8,
                        barThickness: 45
                    },
                    {
                        label: 'MRP List Price (₹)',
                        data: [amzMrp, fpkMrp],
                        backgroundColor: ['rgba(245, 158, 11, 0.25)', 'rgba(59, 130, 246, 0.25)'],
                        borderColor: ['#f59e0b', '#3b82f6'],
                        borderWidth: 1,
                        borderRadius: 8,
                        barThickness: 45
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans' } }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ₹${context.raw.toLocaleString('en-IN')}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', weight: 'bold' } },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    },
                    y: {
                        ticks: {
                            color: '#94a3b8',
                            callback: value => '₹' + (value >= 1000 ? (value / 1000).toFixed(0) + 'k' : value)
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    }
                }
            }
        });
    },

    // 2. Line Chart: Price History Timeline
    renderPriceHistoryChart(canvasId, historyData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        if (historyChartInstance) {
            historyChartInstance.destroy();
        }

        if (!historyData || historyData.length === 0) {
            // Render placeholder empty state
            historyData = [
                { platform: 'amazon', price: 69999, recorded_at: 'Day 1' },
                { platform: 'flipkart', price: 68999, recorded_at: 'Day 1' },
                { platform: 'amazon', price: 67999, recorded_at: 'Day 2' },
                { platform: 'flipkart', price: 65999, recorded_at: 'Day 2' },
            ];
        }

        // Group points by platform
        const amzPoints = historyData.filter(h => h.platform === 'amazon');
        const fpkPoints = historyData.filter(h => h.platform === 'flipkart');

        const labels = historyData.map((h, i) => {
            const date = new Date(h.recorded_at);
            return isNaN(date.getTime()) ? `Point ${i + 1}` : date.toLocaleDateString('en-IN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
        });

        // Deduplicate labels while preserving order
        const uniqueLabels = [...new Set(labels)].slice(-8);

        historyChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: uniqueLabels.length > 0 ? uniqueLabels : ['Check 1', 'Check 2', 'Current'],
                datasets: [
                    {
                        label: 'Amazon Price',
                        data: amzPoints.map(p => p.price).slice(-8),
                        borderColor: '#ff9900',
                        backgroundColor: 'rgba(255, 153, 0, 0.1)',
                        fill: true,
                        tension: 0.35,
                        pointRadius: 5,
                        pointHoverRadius: 7
                    },
                    {
                        label: 'Flipkart Price',
                        data: fpkPoints.map(p => p.price).slice(-8),
                        borderColor: '#2874f0',
                        backgroundColor: 'rgba(40, 116, 240, 0.1)',
                        fill: true,
                        tension: 0.35,
                        pointRadius: 5,
                        pointHoverRadius: 7
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans' } }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ₹${Number(context.raw || 0).toLocaleString('en-IN')}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: '#94a3b8', font: { size: 10 } },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    },
                    y: {
                        ticks: {
                            color: '#94a3b8',
                            callback: value => '₹' + (value >= 1000 ? (value / 1000).toFixed(0) + 'k' : value)
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    }
                }
            }
        });
    },

    // 3. Doughnut Chart: Platform Advantage / Win Rate
    renderAdvantageChart(canvasId, cheaperCounts) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        if (advantageChartInstance) {
            advantageChartInstance.destroy();
        }

        const amazonWins = cheaperCounts?.amazon || 1;
        const flipkartWins = cheaperCounts?.flipkart || 2;
        const equalWins = cheaperCounts?.equal || 0;

        advantageChartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Flipkart Cheaper', 'Amazon Cheaper', 'Equal Price'],
                datasets: [
                    {
                        data: [flipkartWins, amazonWins, equalWins],
                        backgroundColor: ['#2874f0', '#ff9900', '#10b981'],
                        borderWidth: 2,
                        borderColor: '#111827'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#94a3b8', padding: 15, font: { family: 'Plus Jakarta Sans', size: 11 } }
                    }
                }
            }
        });
    }
};
