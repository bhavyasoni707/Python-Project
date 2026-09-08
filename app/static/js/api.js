/**
 * API Client Module for Smartphone Price Analyzer
 */

const API = {
    async compare(query, live = false) {
        const url = `/api/compare?q=${encodeURIComponent(query)}&live=${Boolean(live)}`;
        const response = await fetch(url);
        if (!response.ok) {
            const err = await response.json().catch(() => ({ detail: 'Network request failed' }));
            throw new Error(err.detail || 'Failed to compare smartphones');
        }
        return await response.json();
    },

    async getAnalytics() {
        const response = await fetch('/api/analytics/overview');
        if (!response.ok) throw new Error('Failed to load analytics summary');
        return await response.json();
    },

    async getRecent() {
        const response = await fetch('/api/recent');
        if (!response.ok) throw new Error('Failed to load recent comparisons');
        return await response.json();
    },

    async getPopular() {
        const response = await fetch('/api/popular');
        if (!response.ok) throw new Error('Failed to load popular presets');
        return await response.json();
    },

    async getHistory(productName) {
        const url = `/api/history/${encodeURIComponent(productName)}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to load price history');
        return await response.json();
    }
};
