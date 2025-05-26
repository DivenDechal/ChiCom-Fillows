/**
 * Budget Tracker JavaScript
 * Fillow Application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Budget data
    const budgetData = {
        labels: [
            'Accommodation and Utilities',
            'Entertainment',
            'Food and Clothes',
            'Transportation',
            'Subscription',
            'Others'
        ],
        datasets: [{
            data: [6000000, 1500000, 3000000, 2250000, 1500000, 750000],
            backgroundColor: [
                '#3465A4',  // Accommodation
                '#5e17eb',  // Entertainment
                '#FCBF49',  // Food
                '#103778',  // Transportation
                '#ffc154',  // Subscription
                '#333333'   // Others
            ],
            borderWidth: 0,
            cutout: '70%'
        }]
    };

    // Create the doughnut chart
    const ctx = document.getElementById('budgetChart').getContext('2d');
    const budgetChart = new Chart(ctx, {
        type: 'doughnut',
        data: budgetData,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.raw;
                            return 'Rp ' + value.toLocaleString('id-ID', {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            });
                        }
                    }
                }
            }
        }
    });

    // Add hover effect to categories
    const categories = document.querySelectorAll('.category');
    categories.forEach(category => {
        category.addEventListener('mouseenter', function() {
            this.style.cursor = 'pointer';
        });
    });

    // ---------------------------
    // CATEGORY TRANSACTIONS FEATURE
    // ---------------------------
    // In-memory storage for transactions by category
    const transactions = {
        accommodation: [],
        entertainment: [],
        food: [],
        transportation: [],
        subscription: [],
        others: []
    };

    // Helper to get modal elements
    const addModal = document.getElementById('addModal');
    const viewModal = document.getElementById('viewModal');
    const closeAddModalBtn = document.getElementById('closeAddModal');
    const closeViewModalBtn = document.getElementById('closeViewModal');
    const addTransactionForm = document.getElementById('addTransactionForm');
    const transactionList = document.getElementById('transactionList');
    const addCategoryInput = document.getElementById('addCategory');

    // Open Add Transaction modal
    document.querySelectorAll('.add-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const category = this.getAttribute('data-category');
            addCategoryInput.value = category;
            addTransactionForm.reset();
            addModal.classList.add('active');
            setTimeout(() => document.getElementById('transactionDetail').focus(), 200);
        });
    });

    // Open View Transactions modal
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const category = this.getAttribute('data-category');
            showTransactionHistory(category);
            viewModal.classList.add('active');
        });
    });

    // Add Transaction logic
    addTransactionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const cat = addCategoryInput.value;
        const detail = document.getElementById('transactionDetail').value.trim();
        const cost = Number(document.getElementById('transactionCost').value);
        if (!detail || isNaN(cost)) return;

        if (!transactions[cat]) transactions[cat] = [];
        transactions[cat].push({ detail, cost, time: new Date() });

        alert('Transaction added!');
        addModal.classList.remove('active');
    });

    // Show transaction history for a category
    function showTransactionHistory(category) {
    const container = document.getElementById('transactionList');
    container.innerHTML = '';
    if (transactions[category] && transactions[category].length > 0) {
        transactions[category].forEach(tr => {
            const card = document.createElement('div');
            card.className = 'transaction-history-card';

            // Transaction title/desc
            const title = document.createElement('div');
            title.className = 'history-title';
            title.textContent = tr.detail;

            // Transaction amount (no color, formatted)
            const amount = document.createElement('div');
            amount.className = 'history-amount';
            amount.textContent = 'Rp ' + tr.cost.toLocaleString('id-ID');

            card.appendChild(title);
            card.appendChild(amount);
            container.appendChild(card);
        });
    } else {
        container.innerHTML = '<div class="transaction-history-card">No transactions yet.</div>';
    }
}


    // Modal close buttons
    closeAddModalBtn.onclick = () => addModal.classList.remove('active');
    closeViewModalBtn.onclick = () => viewModal.classList.remove('active');

    // Close modal when clicking outside modal-content
    window.addEventListener('mousedown', function(e) {
        if (e.target === addModal) addModal.classList.remove('active');
        if (e.target === viewModal) viewModal.classList.remove('active');
    });
});
