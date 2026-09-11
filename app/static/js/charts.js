/**
 * PriceSnap — Chart Renderers
 * Dark-themed charts using Chart.js 4
 */

// Dark theme defaults applied globally
Chart.defaults.color = '#8b8fa8';
Chart.defaults.borderColor = '#22252f';
Chart.defaults.font.family = "'Inter', system-ui, sans-serif";

const Charts = (() => {
    let priceCompChart = null;
    let advantageChart = null;
    let historyChart = null;

    // ----------------------------------------------------------------
    // Price Comparison Bar Chart (Selling Price vs MRP)
    // ----------------------------------------------------------------
    function renderPriceComparisonChart(canvasId, data) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        const amz = data.amazon;
        const fpk = data.flipkart;

        const labels = [];
        const priceData = [];
        const mrpData = [];
        const bgColors = [];
        const mrpColors = [];

        if (amz && amz.price) {
            labels.push('Amazon India');
            priceData.push(amz.price);
            mrpData.push(amz.mrp || amz.price);
            bgColors.push('rgba(255,153,0,0.85)');
            mrpColors.push('rgba(255,153,0,0.25)');
        }

        if (fpk && fpk.price) {
            labels.push('Flipkart');
            priceData.push(fpk.price);
            mrpData.push(fpk.mrp || fpk.price);
            bgColors.push('rgba(40,116,240,0.85)');
            mrpColors.push('rgba(40,116,240,0.25)');
        }

        if (priceCompChart) priceCompChart.destroy();

        if (labels.length === 0) {
            priceCompChart = null;
            return;
        }

        priceCompChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels,
                datasets: [
                    {
                        label: 'Selling Price',
                        data: priceData,
                        backgroundColor: bgColors,
                        borderRadius: 8,
                        borderSkipped: false,
                        barPercentage: 0.55,
                    },
                    {
                        label: 'MRP',
                        data: mrpData,
                        backgroundColor: mrpColors,
                        borderRadius: 8,
                        borderSkipped: false,
                        barPercentage: 0.55,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 16,
                            usePointStyle: true,
                            pointStyle: 'circle',
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1c1f28',
                        borderColor: '#22252f',
                        borderWidth: 1,
                        callbacks: {
                            label: ctx => ` ₹${Number(ctx.raw).toLocaleString('en-IN')}`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { font: { size: 12, weight: '600' } }
                    },
                    y: {
                        grid: { color: '#22252f' },
                        ticks: {
                            font: { size: 11 },
                            callback: v => '₹' + Number(v).toLocaleString('en-IN')
                        }
                    }
                }
            }
        });
    }

    // ----------------------------------------------------------------
    // Platform Win Rate Doughnut
    // ----------------------------------------------------------------
    function renderAdvantageChart(canvasId, counts) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        const amzCount = counts?.amazon || 0;
        const fpkCount = counts?.flipkart || 0;
        const eqCount = counts?.equal || 0;
        const total = amzCount + fpkCount + eqCount;

        if (advantageChart) advantageChart.destroy();

        if (total === 0) {
            advantageChart = null;
            // Draw empty state text
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#4a4f66';
            ctx.font = '13px Inter';
            ctx.textAlign = 'center';
            ctx.fillText('No data yet', canvas.width / 2, canvas.height / 2);
            return;
        }

        advantageChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Amazon', 'Flipkart', 'Equal'],
                datasets: [{
                    data: [amzCount, fpkCount, eqCount],
                    backgroundColor: [
                        'rgba(255,153,0,0.85)',
                        'rgba(40,116,240,0.85)',
                        'rgba(34,197,94,0.7)',
                    ],
                    borderColor: '#16181f',
                    borderWidth: 3,
                    hoverOffset: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '68%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 14,
                            usePointStyle: true,
                            pointStyle: 'circle',
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1c1f28',
                        borderColor: '#22252f',
                        borderWidth: 1,
                        callbacks: {
                            label: ctx => ` ${ctx.label}: ${ctx.raw} searches (${Math.round((ctx.raw / total) * 100)}%)`
                        }
                    }
                }
            }
        });
    }

    // ----------------------------------------------------------------
    // Price History Line Chart
    // ----------------------------------------------------------------
    function renderPriceHistoryChart(canvasId, history) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        if (historyChart) historyChart.destroy();

        if (!history || history.length === 0) {
            historyChart = null;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#4a4f66';
            ctx.font = '13px Inter';
            ctx.textAlign = 'center';
            ctx.fillText('No price history yet for this product', canvas.width / 2, canvas.height / 2);
            return;
        }

        const amzPoints = history.filter(h => h.platform === 'amazon' && h.price);
        const fpkPoints = history.filter(h => h.platform === 'flipkart' && h.price);

        const allTimes = [...new Set(history.map(h => h.recorded_at))].sort();

        const amzMap = Object.fromEntries(amzPoints.map(h => [h.recorded_at, h.price]));
        const fpkMap = Object.fromEntries(fpkPoints.map(h => [h.recorded_at, h.price]));

        const shortLabels = allTimes.map(t => {
            const d = new Date(t);
            return d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
        });

        historyChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: shortLabels,
                datasets: [
                    {
                        label: 'Amazon India',
                        data: allTimes.map(t => amzMap[t] ?? null),
                        borderColor: '#FF9900',
                        backgroundColor: 'rgba(255,153,0,0.08)',
                        borderWidth: 2.5,
                        pointRadius: 4,
                        pointBackgroundColor: '#FF9900',
                        fill: true,
                        tension: 0.35,
                        spanGaps: true,
                    },
                    {
                        label: 'Flipkart',
                        data: allTimes.map(t => fpkMap[t] ?? null),
                        borderColor: '#2874F0',
                        backgroundColor: 'rgba(40,116,240,0.08)',
                        borderWidth: 2.5,
                        pointRadius: 4,
                        pointBackgroundColor: '#2874F0',
                        fill: true,
                        tension: 0.35,
                        spanGaps: true,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 16,
                            usePointStyle: true,
                            pointStyle: 'circle',
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1c1f28',
                        borderColor: '#22252f',
                        borderWidth: 1,
                        callbacks: {
                            label: ctx => ` ${ctx.dataset.label}: ₹${Number(ctx.raw).toLocaleString('en-IN')}`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { font: { size: 11 }, maxRotation: 0 }
                    },
                    y: {
                        grid: { color: '#22252f' },
                        ticks: {
                            font: { size: 11 },
                            callback: v => '₹' + Number(v).toLocaleString('en-IN')
                        }
                    }
                }
            }
        });
    }

    return { renderPriceComparisonChart, renderAdvantageChart, renderPriceHistoryChart };
})();
