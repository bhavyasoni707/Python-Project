/**
 * PriceSnap — Main UI Application Controller
 * Handles search, pipeline animation, card rendering, stock display, and charts.
 */

document.addEventListener('DOMContentLoaded', () => { initApp(); });

async function initApp() {
    setupEventListeners();
    await loadPopularPills();
    await refreshAnalytics();
    await loadRecentComparisons();
    // Fire initial search
    performSearch("Apple iPhone 15 128GB", false);
}

function setupEventListeners() {
    document.getElementById('searchForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const q = document.getElementById('searchInput').value.trim();
        if (q.length >= 3) performSearch(q, document.getElementById('liveScrapeToggle').checked);
    });
}

async function loadPopularPills() {
    try {
        const { popular } = await API.getPopular();
        const container = document.getElementById('popularPills');
        container.innerHTML = popular.map(p => `
            <button type="button" onclick="quickSearch('${p.query}')"
                class="px-3.5 py-1.5 rounded-full text-xs font-semibold bg-white/10 hover:bg-white/20 text-white/80 hover:text-white border border-white/20 hover:border-white/40 transition-all backdrop-blur-sm">
                ${p.name}
            </button>
        `).join('');
    } catch (e) { console.error(e); }
}

function quickSearch(query) {
    document.getElementById('searchInput').value = query;
    performSearch(query, document.getElementById('liveScrapeToggle').checked);
}

// ============ Pipeline Animator ============
async function animatePipeline(telemetry) {
    for (let i = 1; i <= 5; i++) {
        const step = document.getElementById(`pipelineStep${i}`);
        const status = document.getElementById(`stepStatus${i}`);
        if (step) { step.className = 'pipeline-step px-4 py-3'; }
        if (status) status.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-gray-300 inline-block"></span>Waiting`;
    }

    for (const item of telemetry) {
        const step = document.getElementById(`pipelineStep${item.stage}`);
        const status = document.getElementById(`stepStatus${item.stage}`);
        const time = document.getElementById(`stepTime${item.stage}`);

        if (step) step.classList.add('active');
        if (status) status.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-ping inline-block"></span><span class="text-indigo-600 font-medium">Processing</span>`;

        await new Promise(r => setTimeout(r, 100));

        if (step) { step.classList.remove('active'); step.classList.add('completed'); }
        if (status) status.innerHTML = `<svg class="w-3 h-3 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg><span class="text-green-600 font-semibold">Done</span>`;
        if (time) time.innerText = `${item.duration_ms}ms`;
    }
}

// ============ Stock Badge Renderer ============
function stockBadge(status) {
    if (status === 'IN_STOCK') {
        return `<span class="badge-in-stock"><span class="w-1.5 h-1.5 rounded-full bg-green-500 inline-block"></span>In Stock</span>`;
    } else if (status === 'OUT_OF_STOCK') {
        return `<span class="badge-out-of-stock"><span class="w-1.5 h-1.5 rounded-full bg-red-500 inline-block"></span>Out of Stock</span>`;
    } else if (status === 'NOT_FOUND') {
        return `<span class="badge-not-found"><span class="w-1.5 h-1.5 rounded-full bg-slate-400 inline-block"></span>Not Found</span>`;
    } else {
        return `<span class="badge-unavailable"><span class="w-1.5 h-1.5 rounded-full bg-amber-500 inline-block"></span>Unavailable</span>`;
    }
}

// ============ Price Section Renderer ============
function renderPriceSection(product, platform) {
    if (!product || product.stock_status === 'NOT_FOUND') {
        return `
            <div class="oos-overlay rounded-xl p-6 text-center border-2 border-dashed border-gray-200">
                <div class="text-4xl mb-2">🔍</div>
                <div class="text-sm font-bold text-gray-500">Not Found on ${platform === 'amazon' ? 'Amazon India' : 'Flipkart'}</div>
                <div class="text-xs text-gray-400 mt-1">This exact variant was not listed</div>
            </div>`;
    }

    if (product.stock_status === 'OUT_OF_STOCK') {
        return `
            <div class="oos-overlay rounded-xl p-5 border-2 border-dashed border-red-200 text-center">
                <div class="text-4xl mb-2">❌</div>
                <div class="text-sm font-bold text-red-600">Out of Stock</div>
                <div class="text-xs text-gray-400 mt-1 mb-3">${product.stock_message}</div>
                ${product.price ? `<div class="text-lg font-black text-gray-300 line-through">₹${Number(product.price).toLocaleString('en-IN')}</div>
                <div class="text-xs text-gray-400">Last known price</div>` : ''}
            </div>`;
    }

    if (product.stock_status === 'CURRENTLY_UNAVAILABLE') {
        return `
            <div class="oos-overlay rounded-xl p-5 border-2 border-dashed border-amber-200 text-center">
                <div class="text-4xl mb-2">⚠️</div>
                <div class="text-sm font-bold text-amber-700">Currently Unavailable</div>
                <div class="text-xs text-gray-400 mt-1">${product.stock_message}</div>
            </div>`;
    }

    // In Stock — show full price block
    const price = Number(product.price).toLocaleString('en-IN');
    const mrp = product.mrp ? Number(product.mrp).toLocaleString('en-IN') : null;
    const discount = product.discount_percent ? `${product.discount_percent}%` : null;

    return `
        <div class="flex items-end justify-between">
            <div>
                <div class="text-xs text-gray-400 font-medium mb-1">Selling Price</div>
                <div class="text-4xl font-black text-gray-900">₹${price}</div>
                ${mrp ? `<div class="flex items-center gap-2 mt-1">
                    <span class="text-sm text-gray-400 line-through">₹${mrp}</span>
                    ${discount ? `<span class="text-xs font-bold text-green-600 bg-green-50 border border-green-200 px-2 py-0.5 rounded-full">${discount} OFF</span>` : ''}
                </div>` : ''}
            </div>
        </div>`;
}

// ============ Spec Table Renderer ============
function renderSpecTable(amazon, flipkart, analysis) {
    const table = document.getElementById('specTable');
    const tbody = document.getElementById('specTableBody');
    if (!amazon && !flipkart) { table.classList.add('hidden'); return; }

    const amzPrice = amazon?.price;
    const fpkPrice = flipkart?.price;
    const cheaper = analysis?.cheaper_platform;

    const rows = [
        {
            label: 'Selling Price', 
            amz: amzPrice ? `₹${Number(amzPrice).toLocaleString('en-IN')}` : '—',
            fpk: fpkPrice ? `₹${Number(fpkPrice).toLocaleString('en-IN')}` : '—',
            winAmz: cheaper === 'amazon', winFpk: cheaper === 'flipkart'
        },
        {
            label: 'MRP / List Price',
            amz: amazon?.mrp ? `₹${Number(amazon.mrp).toLocaleString('en-IN')}` : '—',
            fpk: flipkart?.mrp ? `₹${Number(flipkart.mrp).toLocaleString('en-IN')}` : '—',
            winAmz: false, winFpk: false
        },
        {
            label: 'Discount %',
            amz: amazon?.discount_percent ? `${amazon.discount_percent}%` : '—',
            fpk: flipkart?.discount_percent ? `${flipkart.discount_percent}%` : '—',
            winAmz: (amazon?.discount_percent || 0) > (flipkart?.discount_percent || 0),
            winFpk: (flipkart?.discount_percent || 0) > (amazon?.discount_percent || 0)
        },
        {
            label: 'Stock Status',
            amz: amazon?.stock_status?.replace('_', ' ') || '—',
            fpk: flipkart?.stock_status?.replace('_', ' ') || '—',
            winAmz: amazon?.stock_status === 'IN_STOCK' && flipkart?.stock_status !== 'IN_STOCK',
            winFpk: flipkart?.stock_status === 'IN_STOCK' && amazon?.stock_status !== 'IN_STOCK'
        },
        {
            label: 'Rating',
            amz: amazon?.rating ? `${amazon.rating} ★` : '—',
            fpk: flipkart?.rating ? `${flipkart.rating} ★` : '—',
            winAmz: (amazon?.rating || 0) > (flipkart?.rating || 0),
            winFpk: (flipkart?.rating || 0) > (amazon?.rating || 0)
        },
        {
            label: 'Reviews',
            amz: amazon?.reviews_count ? Number(amazon.reviews_count).toLocaleString('en-IN') : '—',
            fpk: flipkart?.reviews_count ? Number(flipkart.reviews_count).toLocaleString('en-IN') : '—',
            winAmz: (amazon?.reviews_count || 0) > (flipkart?.reviews_count || 0),
            winFpk: (flipkart?.reviews_count || 0) > (amazon?.reviews_count || 0)
        },
        {
            label: 'Price Difference',
            amz: analysis?.abs_price_diff ? `₹${Number(analysis.abs_price_diff).toLocaleString('en-IN')} cheaper` : '—',
            fpk: analysis?.abs_price_diff ? `₹${Number(analysis.abs_price_diff).toLocaleString('en-IN')} cheaper` : '—',
            winAmz: cheaper === 'amazon', winFpk: cheaper === 'flipkart'
        }
    ];

    tbody.innerHTML = rows.map(r => `
        <tr>
            <td class="text-gray-500 font-medium">${r.label}</td>
            <td class="text-center ${r.winAmz ? 'winner-cell' : ''}">${r.amz}</td>
            <td class="text-center ${r.winFpk ? 'winner-cell' : ''}">${r.fpk}</td>
        </tr>
    `).join('');

    table.classList.remove('hidden');
}

// ============ Main Render ============
function renderUI(data) {
    const { analysis, amazon: amz, flipkart: fpk } = data;

    // Winner Banner
    const banner = document.getElementById('winnerBanner');
    const winnerText = document.getElementById('winnerText');
    const winnerSub = document.getElementById('winnerSub');
    const winnerBadge = document.getElementById('winnerBadge');

    if (analysis.cheaper_platform === 'flipkart' && analysis.savings_amount > 0) {
        banner.className = 'rounded-2xl p-5 bg-blue-50 border border-blue-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3';
        winnerText.innerHTML = `<span class="text-blue-700">🎉 <strong>Flipkart</strong> is ₹${Number(analysis.savings_amount).toLocaleString('en-IN')} cheaper (${analysis.savings_percent}% off Amazon's price)</span>`;
        winnerBadge.className = 'px-4 py-2 rounded-xl text-sm font-bold bg-blue-600 text-white shadow-sm';
        winnerBadge.innerText = '✓ Best Deal: Flipkart';
    } else if (analysis.cheaper_platform === 'amazon' && analysis.savings_amount > 0) {
        banner.className = 'rounded-2xl p-5 bg-amber-50 border border-amber-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3';
        winnerText.innerHTML = `<span class="text-amber-800">🎉 <strong>Amazon</strong> is ₹${Number(analysis.savings_amount).toLocaleString('en-IN')} cheaper (${analysis.savings_percent}% off Flipkart's price)</span>`;
        winnerBadge.className = 'px-4 py-2 rounded-xl text-sm font-bold bg-amber-500 text-white shadow-sm';
        winnerBadge.innerText = '✓ Best Deal: Amazon';
    } else if (analysis.cheaper_platform === 'equal') {
        banner.className = 'rounded-2xl p-5 bg-emerald-50 border border-emerald-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3';
        winnerText.innerHTML = `<span class="text-emerald-700">🤝 <strong>Same price</strong> on both platforms — ₹${Number(analysis.amazon_price || 0).toLocaleString('en-IN')}</span>`;
        winnerBadge.className = 'px-4 py-2 rounded-xl text-sm font-bold bg-emerald-600 text-white';
        winnerBadge.innerText = '⚖ Equal Price';
    } else {
        banner.className = 'rounded-2xl p-5 bg-gray-50 border border-gray-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3';
        winnerText.innerHTML = `<span class="text-gray-700">${analysis.deal_summary}</span>`;
        winnerBadge.className = 'px-4 py-2 rounded-xl text-sm font-bold bg-gray-200 text-gray-600';
        winnerBadge.innerText = analysis.deal_badge;
    }
    winnerSub.innerText = `${analysis.stock_summary} · Match confidence: ${data.match_confidence}%`;

    // Amazon Card
    document.getElementById('amzStock').innerHTML = stockBadge(amz?.stock_status || 'NOT_FOUND');
    document.getElementById('amzTitle').innerText = amz?.title || 'Not found on Amazon India';
    document.getElementById('amzStockMsg').innerText = amz?.stock_message || '';
    document.getElementById('amzImg').src = amz?.image_url || 'https://via.placeholder.com/120x120?text=📱';
    document.getElementById('amzPriceSection').innerHTML = renderPriceSection(amz, 'amazon');
    document.getElementById('amzRating').innerHTML = amz?.rating ? `<span class="text-amber-400">★</span> ${amz.rating} (${Number(amz.reviews_count || 0).toLocaleString('en-IN')} reviews)` : '<span class="text-amber-400">★</span> —';
    document.getElementById('amzBuyBtn').href = amz?.product_url || '#';

    const amzCard = document.getElementById('amazonCard');
    amzCard.classList.remove('winner-card-amazon', 'winner-card-flipkart');
    if (analysis.cheaper_platform === 'amazon') amzCard.classList.add('winner-card-amazon');

    // Flipkart Card
    document.getElementById('fpkStock').innerHTML = stockBadge(fpk?.stock_status || 'NOT_FOUND');
    document.getElementById('fpkTitle').innerText = fpk?.title || 'Not found on Flipkart';
    document.getElementById('fpkStockMsg').innerText = fpk?.stock_message || '';
    document.getElementById('fpkImg').src = fpk?.image_url || 'https://via.placeholder.com/120x120?text=📱';
    document.getElementById('fpkPriceSection').innerHTML = renderPriceSection(fpk, 'flipkart');
    document.getElementById('fpkRating').innerHTML = fpk?.rating ? `<span class="text-amber-400">★</span> ${fpk.rating} (${Number(fpk.reviews_count || 0).toLocaleString('en-IN')} reviews)` : '<span class="text-amber-400">★</span> —';
    document.getElementById('fpkBuyBtn').href = fpk?.product_url || '#';

    const fpkCard = document.getElementById('flipkartCard');
    fpkCard.classList.remove('winner-card-amazon', 'winner-card-flipkart');
    if (analysis.cheaper_platform === 'flipkart') fpkCard.classList.add('winner-card-flipkart');

    // Spec Comparison Table
    renderSpecTable(amz, fpk, analysis);
}

// ============ performSearch ============
async function performSearch(query, live = false) {
    const btn = document.getElementById('searchBtn');
    const spinner = document.getElementById('searchSpinner');
    const btnText = document.getElementById('searchBtnText');

    btn.disabled = true;
    spinner.classList.remove('hidden');
    btnText.innerText = 'Analyzing...';

    try {
        const result = await API.compare(query, live);
        if (result.pipeline_telemetry) await animatePipeline(result.pipeline_telemetry);
        renderUI(result);
        Charts.renderPriceComparisonChart('priceComparisonChart', result);
        Charts.renderPriceHistoryChart('priceHistoryChart', result.price_history);
        await refreshAnalytics();
        await loadRecentComparisons();
    } catch (err) {
        console.error(err);
        document.getElementById('winnerText').innerText = `Error: ${err.message}`;
    } finally {
        btn.disabled = false;
        spinner.classList.add('hidden');
        btnText.innerText = 'Compare';
    }
}

async function refreshAnalytics() {
    try {
        const stats = await API.getAnalytics();
        document.getElementById('kpiTotalQueries').innerText = stats.total_comparisons || 0;
        document.getElementById('kpiAvgSavings').innerText = `₹${Number(stats.average_savings || 0).toLocaleString('en-IN')}`;
        document.getElementById('kpiMaxSavings').innerText = `₹${Number(stats.max_savings || 0).toLocaleString('en-IN')}`;
        document.getElementById('kpiStockRate').innerText = `${stats.in_stock_rate ?? '—'}%`;
        Charts.renderAdvantageChart('advantageChart', stats.cheaper_counts);
    } catch (e) { console.error(e); }
}

async function loadRecentComparisons() {
    try {
        const { recent } = await API.getRecent();
        const tbody = document.getElementById('recentTableBody');
        if (!recent || recent.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" class="text-center py-8 text-gray-400 text-sm">No comparisons yet. Search above to start!</td></tr>`;
            return;
        }
        tbody.innerHTML = recent.map(row => {
            const time = row.created_at ? new Date(row.created_at).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) : '—';
            const amzPrice = row.amazon_price ? `₹${Number(row.amazon_price).toLocaleString('en-IN')}` : '—';
            const fpkPrice = row.flipkart_price ? `₹${Number(row.flipkart_price).toLocaleString('en-IN')}` : '—';
            const diff = row.price_diff != null ? `₹${Math.abs(row.price_diff).toLocaleString('en-IN')}` : '—';

            let dealPill = `<span class="px-2 py-0.5 rounded-full text-xs bg-gray-100 text-gray-500 font-medium">N/A</span>`;
            if (row.cheaper_platform === 'flipkart') {
                dealPill = `<span class="px-2 py-0.5 rounded-full text-xs bg-blue-100 text-blue-700 font-semibold border border-blue-200">Flipkart wins</span>`;
            } else if (row.cheaper_platform === 'amazon') {
                dealPill = `<span class="px-2 py-0.5 rounded-full text-xs bg-amber-100 text-amber-700 font-semibold border border-amber-200">Amazon wins</span>`;
            } else if (row.cheaper_platform === 'equal') {
                dealPill = `<span class="px-2 py-0.5 rounded-full text-xs bg-emerald-100 text-emerald-700 font-semibold border border-emerald-200">Equal</span>`;
            }

            return `<tr class="hover:bg-gray-50 cursor-pointer transition-colors" onclick="quickSearch('${row.query}')">
                <td class="py-3 px-5 font-semibold text-gray-800 text-sm">${row.product_name}</td>
                <td class="py-3 px-4 text-gray-600">${amzPrice}</td>
                <td class="py-3 px-4 text-gray-600">${fpkPrice}</td>
                <td class="py-3 px-4 font-bold text-gray-800">${diff}</td>
                <td class="py-3 px-4">${dealPill}</td>
                <td class="py-3 px-4 text-xs text-gray-400">${time}</td>
            </tr>`;
        }).join('');
    } catch (e) { console.error(e); }
}
