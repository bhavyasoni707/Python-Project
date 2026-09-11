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
    // Fire initial search on load
    performSearch("Apple iPhone 15 128GB", false);
}

function setupEventListeners() {
    document.getElementById('searchForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const q = document.getElementById('searchInput').value.trim();
        if (q.length >= 2) performSearch(q, document.getElementById('liveScrapeToggle').checked);
    });
}

// ============================================================
// Popular Pills
// ============================================================
async function loadPopularPills() {
    try {
        const { popular } = await API.getPopular();
        const container = document.getElementById('popularPills');
        container.innerHTML = popular.map(p => `
            <button type="button" onclick="quickSearch('${p.query}')" class="popular-pill">
                ${p.name}
            </button>
        `).join('');
    } catch (e) { console.error(e); }
}

function quickSearch(query) {
    document.getElementById('searchInput').value = query;
    performSearch(query, document.getElementById('liveScrapeToggle').checked);
}

// ============================================================
// Pipeline Animator
// ============================================================
async function animatePipeline(telemetry) {
    // Reset all stages
    for (let i = 1; i <= 5; i++) {
        const step = document.getElementById(`pipelineStep${i}`);
        const status = document.getElementById(`stepStatus${i}`);
        const time = document.getElementById(`stepTime${i}`);
        if (step) step.className = 'pipeline-stage';
        if (status) status.innerHTML = `<span class="status-dot"></span> Waiting`;
        if (time) time.innerText = '—';
    }

    for (const item of telemetry) {
        const step = document.getElementById(`pipelineStep${item.stage}`);
        const status = document.getElementById(`stepStatus${item.stage}`);
        const time = document.getElementById(`stepTime${item.stage}`);

        if (step) { step.className = 'pipeline-stage'; step.classList.add('active'); }
        if (status) status.innerHTML = `<span class="status-dot active"></span><span style="color:var(--accent-bright);font-weight:600;">Processing</span>`;

        await new Promise(r => setTimeout(r, 120));

        if (step) { step.className = 'pipeline-stage'; step.classList.add('completed'); }
        if (status) status.innerHTML = `<span class="status-dot done"></span><span style="color:var(--green);font-weight:600;">Done</span>`;
        if (time) time.innerText = `${item.duration_ms}ms`;
    }
}

// ============================================================
// Stock Badge Renderer
// ============================================================
function stockBadge(status) {
    if (status === 'IN_STOCK') {
        return `<span class="stock-badge badge-in-stock"><span style="width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block;"></span>In Stock</span>`;
    } else if (status === 'OUT_OF_STOCK') {
        return `<span class="stock-badge badge-out-of-stock"><span style="width:6px;height:6px;border-radius:50%;background:var(--red);display:inline-block;"></span>Out of Stock</span>`;
    } else if (status === 'NOT_FOUND') {
        return `<span class="stock-badge badge-not-found"><span style="width:6px;height:6px;border-radius:50%;background:var(--slate);display:inline-block;"></span>Not Found</span>`;
    } else {
        return `<span class="stock-badge badge-unavailable"><span style="width:6px;height:6px;border-radius:50%;background:var(--amber);display:inline-block;"></span>Unavailable</span>`;
    }
}

// ============================================================
// Price Section Renderer
// KEY: If product is NOT_FOUND / OUT_OF_STOCK / UNAVAILABLE
//      show locked overlay — never show a price comparison for wrong phones
// ============================================================
function renderPriceSection(product, platform) {
    const platformLabel = platform === 'amazon' ? 'Amazon India' : 'Flipkart';

    // Not Found on this platform
    if (!product || product.stock_status === 'NOT_FOUND') {
        return `
            <div class="oos-overlay not-found">
                <div class="oos-icon">🔍</div>
                <div class="oos-title" style="color:var(--text-secondary);">Not Found on ${platformLabel}</div>
                <div class="oos-subtitle">This exact variant is not listed on ${platformLabel}</div>
            </div>`;
    }

    // Out of Stock
    if (product.stock_status === 'OUT_OF_STOCK') {
        return `
            <div class="oos-overlay out-of-stock">
                <div class="oos-icon">❌</div>
                <div class="oos-title" style="color:var(--red);">Out of Stock</div>
                <div class="oos-subtitle">${product.stock_message || 'Currently out of stock on ' + platformLabel}</div>
                ${product.price ? `
                    <div class="oos-last-price">₹${Number(product.price).toLocaleString('en-IN')}</div>
                    <div class="oos-last-label">Last known price</div>
                ` : ''}
            </div>`;
    }

    // Currently Unavailable
    if (product.stock_status === 'CURRENTLY_UNAVAILABLE') {
        return `
            <div class="oos-overlay unavailable">
                <div class="oos-icon">⚠️</div>
                <div class="oos-title" style="color:var(--amber);">Currently Unavailable</div>
                <div class="oos-subtitle">${product.stock_message || 'Temporarily unavailable on ' + platformLabel}</div>
            </div>`;
    }

    // In Stock — full price block
    const price = Number(product.price).toLocaleString('en-IN');
    const mrp = product.mrp ? Number(product.mrp).toLocaleString('en-IN') : null;
    const discount = product.discount_percent ? `${product.discount_percent}% OFF` : null;

    return `
        <div>
            <div class="price-label">Selling Price</div>
            <div class="price-main">₹${price}</div>
            ${mrp ? `
            <div class="price-meta">
                <span class="price-mrp">₹${mrp}</span>
                ${discount ? `<span class="discount-badge">${discount}</span>` : ''}
            </div>` : ''}
        </div>`;
}

// ============================================================
// Spec Table Renderer
// ============================================================
function renderSpecTable(amazon, flipkart, analysis) {
    const table = document.getElementById('specTable');
    const tbody = document.getElementById('specTableBody');

    // Hide table if neither product found
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
            label: 'Discount',
            amz: amazon?.discount_percent ? `${amazon.discount_percent}%` : '—',
            fpk: flipkart?.discount_percent ? `${flipkart.discount_percent}%` : '—',
            winAmz: (amazon?.discount_percent || 0) > (flipkart?.discount_percent || 0),
            winFpk: (flipkart?.discount_percent || 0) > (amazon?.discount_percent || 0)
        },
        {
            label: 'Stock Status',
            amz: amazon?.stock_status?.replace(/_/g, ' ') || '—',
            fpk: flipkart?.stock_status?.replace(/_/g, ' ') || '—',
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
            amz: cheaper === 'amazon' && analysis?.abs_price_diff ? `₹${Number(analysis.abs_price_diff).toLocaleString('en-IN')} cheaper` : '—',
            fpk: cheaper === 'flipkart' && analysis?.abs_price_diff ? `₹${Number(analysis.abs_price_diff).toLocaleString('en-IN')} cheaper` : '—',
            winAmz: cheaper === 'amazon',
            winFpk: cheaper === 'flipkart'
        }
    ];

    tbody.innerHTML = rows.map(r => `
        <tr>
            <td>${r.label}</td>
            <td class="${r.winAmz ? 'winner-cell' : ''}">${r.amz}</td>
            <td class="${r.winFpk ? 'winner-cell' : ''}">${r.fpk}</td>
        </tr>
    `).join('');

    table.classList.remove('hidden');
}

// ============================================================
// Main Render — Called after each search completes
// ============================================================
function renderUI(data) {
    const { analysis, amazon: amz, flipkart: fpk } = data;

    // ---- Winner Banner ----
    const banner = document.getElementById('winnerBanner');
    const winnerText = document.getElementById('winnerText');
    const winnerSub = document.getElementById('winnerSub');
    const winnerBadge = document.getElementById('winnerBadge');

    banner.className = 'winner-banner slide-up';
    winnerBadge.className = 'winner-badge';

    if (analysis.cheaper_platform === 'flipkart' && analysis.savings_amount > 0) {
        banner.classList.add('winner-flipkart');
        winnerText.innerHTML = `🎉 <strong>Flipkart</strong> is ₹${Number(analysis.savings_amount).toLocaleString('en-IN')} cheaper <span style="color:var(--text-secondary);font-weight:400;">(${analysis.savings_percent}% less than Amazon)</span>`;
        winnerBadge.className = 'winner-badge badge-flipkart';
        winnerBadge.innerText = '✓ Best Deal: Flipkart';
    } else if (analysis.cheaper_platform === 'amazon' && analysis.savings_amount > 0) {
        banner.classList.add('winner-amazon');
        winnerText.innerHTML = `🎉 <strong>Amazon</strong> is ₹${Number(analysis.savings_amount).toLocaleString('en-IN')} cheaper <span style="color:var(--text-secondary);font-weight:400;">(${analysis.savings_percent}% less than Flipkart)</span>`;
        winnerBadge.className = 'winner-badge badge-amazon';
        winnerBadge.innerText = '✓ Best Deal: Amazon';
    } else if (analysis.cheaper_platform === 'equal') {
        banner.classList.add('winner-equal');
        winnerText.innerHTML = `🤝 <strong>Same price</strong> on both platforms — ₹${Number(analysis.amazon_price || 0).toLocaleString('en-IN')}`;
        winnerBadge.className = 'winner-badge badge-equal';
        winnerBadge.innerText = '⚖ Equal Price';
    } else {
        winnerText.innerHTML = `<span style="color:var(--text-secondary)">${escHtml(analysis.deal_summary)}</span>`;
        winnerBadge.innerText = analysis.deal_badge;
    }

    winnerSub.innerText = `${analysis.stock_summary}  ·  Match confidence: ${data.match_confidence}%`;

    // ---- Amazon Card ----
    document.getElementById('amzStock').innerHTML = stockBadge(amz?.stock_status || 'NOT_FOUND');
    document.getElementById('amzTitle').innerText = amz?.title || 'Not found on Amazon India';
    document.getElementById('amzStockMsg').innerText = amz?.stock_message || '';
    const amzImgEl = document.getElementById('amzImg');
    if (amz?.image_url) { amzImgEl.src = amz.image_url; amzImgEl.style.display = 'block'; }
    else { amzImgEl.style.display = 'none'; }
    document.getElementById('amzPriceSection').innerHTML = renderPriceSection(amz, 'amazon');
    document.getElementById('amzRating').innerHTML = amz?.rating
        ? `<span class="rating-stars">★</span> ${amz.rating} <span style="color:var(--text-muted)">(${Number(amz.reviews_count || 0).toLocaleString('en-IN')} reviews)</span>`
        : `<span class="rating-stars">★</span> —`;
    document.getElementById('amzBuyBtn').href = amz?.product_url || '#';

    const amzCard = document.getElementById('amazonCard');
    amzCard.classList.remove('winner-card-amazon', 'winner-card-flipkart');
    if (analysis.cheaper_platform === 'amazon' && analysis.savings_amount > 0) amzCard.classList.add('winner-card-amazon');

    // ---- Flipkart Card ----
    document.getElementById('fpkStock').innerHTML = stockBadge(fpk?.stock_status || 'NOT_FOUND');
    document.getElementById('fpkTitle').innerText = fpk?.title || 'Not found on Flipkart';
    document.getElementById('fpkStockMsg').innerText = fpk?.stock_message || '';
    const fpkImgEl = document.getElementById('fpkImg');
    if (fpk?.image_url) { fpkImgEl.src = fpk.image_url; fpkImgEl.style.display = 'block'; }
    else { fpkImgEl.style.display = 'none'; }
    document.getElementById('fpkPriceSection').innerHTML = renderPriceSection(fpk, 'flipkart');
    document.getElementById('fpkRating').innerHTML = fpk?.rating
        ? `<span class="rating-stars">★</span> ${fpk.rating} <span style="color:var(--text-muted)">(${Number(fpk.reviews_count || 0).toLocaleString('en-IN')} reviews)</span>`
        : `<span class="rating-stars">★</span> —`;
    document.getElementById('fpkBuyBtn').href = fpk?.product_url || '#';

    const fpkCard = document.getElementById('flipkartCard');
    fpkCard.classList.remove('winner-card-amazon', 'winner-card-flipkart');
    if (analysis.cheaper_platform === 'flipkart' && analysis.savings_amount > 0) fpkCard.classList.add('winner-card-flipkart');

    // ---- Spec Table ----
    renderSpecTable(amz, fpk, analysis);
}

// ============================================================
// Main Search Function
// ============================================================
async function performSearch(query, live = false) {
    const btn = document.getElementById('searchBtn');
    const spinner = document.getElementById('searchSpinner');
    const btnText = document.getElementById('searchBtnText');

    btn.disabled = true;
    spinner.classList.remove('hidden');
    btnText.innerText = 'Analyzing…';

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
        const banner = document.getElementById('winnerBanner');
        document.getElementById('winnerText').innerText = `Error: ${err.message}`;
        banner.className = 'winner-banner';
    } finally {
        btn.disabled = false;
        spinner.classList.add('hidden');
        btnText.innerText = 'Compare';
    }
}

// ============================================================
// Analytics
// ============================================================
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

// ============================================================
// Recent Comparisons Table
// ============================================================
async function loadRecentComparisons() {
    try {
        const { recent } = await API.getRecent();
        const tbody = document.getElementById('recentTableBody');
        if (!recent || recent.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:32px;color:var(--text-muted);">No comparisons yet. Search above to get started!</td></tr>`;
            return;
        }
        tbody.innerHTML = recent.map(row => {
            const dt = row.created_at ? new Date(row.created_at) : null;
            const time = dt ? dt.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) : '—';
            const amzPrice = row.amazon_price ? `₹${Number(row.amazon_price).toLocaleString('en-IN')}` : '—';
            const fpkPrice = row.flipkart_price ? `₹${Number(row.flipkart_price).toLocaleString('en-IN')}` : '—';
            const diff = row.price_diff != null ? `₹${Math.abs(row.price_diff).toLocaleString('en-IN')}` : '—';

            let dealPill = `<span class="deal-pill deal-na">N/A</span>`;
            if (row.cheaper_platform === 'flipkart') {
                dealPill = `<span class="deal-pill deal-flipkart">Flipkart wins</span>`;
            } else if (row.cheaper_platform === 'amazon') {
                dealPill = `<span class="deal-pill deal-amazon">Amazon wins</span>`;
            } else if (row.cheaper_platform === 'equal') {
                dealPill = `<span class="deal-pill deal-equal">Equal</span>`;
            }

            const query = row.query.replace(/'/g, "\\'");
            return `<tr onclick="quickSearch('${query}')">
                <td><span class="recent-product-name">${escHtml(row.product_name)}</span></td>
                <td>${amzPrice}</td>
                <td>${fpkPrice}</td>
                <td style="font-weight:700;color:var(--text-primary);">${diff}</td>
                <td>${dealPill}</td>
                <td style="font-size:12px;color:var(--text-muted);">${time}</td>
            </tr>`;
        }).join('');
    } catch (e) { console.error(e); }
}

// ============================================================
// Utility
// ============================================================
function escHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
