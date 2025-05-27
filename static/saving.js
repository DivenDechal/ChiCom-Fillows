document.addEventListener('DOMContentLoaded', function() {
    // Initialize savings data
    let savingsData = {
        currentSavings: 100272421.10,
        savingsGoal: 100000000.00,
        transactions: [
            {
                type: 'save',
                category: 'Account Transfer',
                amount: 1000000.00,
                date: new Date()
            },
            {
                type: 'spend',
                category: 'Accommodation and Utilities',
                amount: 2564425.00,
                date: new Date()
            },
            {
                type: 'spend',
                category: 'Debts',
                amount: 15000000.00,
                date: new Date()
            }
        ]
    };

    // Format currency function
    function formatCurrency(amount) {
        return 'Rp ' + amount.toLocaleString('id-ID', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    // Update savings display
    function updateSavingsDisplay() {
        document.getElementById('currentSavings').textContent = formatCurrency(savingsData.currentSavings);
        document.getElementById('savingsGoal').textContent = formatCurrency(savingsData.savingsGoal);
    }

    // Create transaction element
    function createTransactionElement(transaction) {
        const transactionItem = document.createElement('div');
        transactionItem.className = `transaction-item ${transaction.type === 'save' ? 'income' : 'expense'}`;
        
        transactionItem.innerHTML = `
            <div class="transaction-details">
                <div class="transaction-category">${transaction.category}</div>
                <div class="transaction-amount">${transaction.type === 'save' ? '+ ' : '- '}${formatCurrency(transaction.amount)}</div>
            </div>
        `;
        
        return transactionItem;
    }

    // Update transaction list
    function updateTransactionList() {
        const transactionList = document.getElementById('transactionList');
        // Clear existing transactions
        transactionList.innerHTML = '';
        
        // Sort transactions by date (newest first)
        const sortedTransactions = [...savingsData.transactions].sort((a, b) => b.date - a.date);
        
        // Add transactions to the list
        sortedTransactions.forEach(transaction => {
            transactionList.appendChild(createTransactionElement(transaction));
        });
    }

    // New feature: Add Transaction function
    function addTransaction(type, category, amount) {
        if (isNaN(amount) || amount <= 0) {
            alert('Please enter a valid amount');
            return false;
        }

        const newTransaction = {
            type: type,
            category: category,
            amount: amount,
            date: new Date()
        };

        // Update savings amount
        if (type === 'save') {
            savingsData.currentSavings += amount;
        } else {
            savingsData.currentSavings -= amount;
        }

        // Add transaction to data
        savingsData.transactions.push(newTransaction);

        // Update UI
        updateSavingsDisplay();
        updateTransactionList();

        return true;
    }

    // Handle form submission using addTransaction feature
    document.getElementById('transactionForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form values
        const type = document.getElementById('transactionType').value;
        const category = document.getElementById('category').value;
        const amount = parseFloat(document.getElementById('amount').value);

        const success = addTransaction(type, category, amount);
        if (success) {
            // Reset form only if the transaction was successfully added
            document.getElementById('transactionForm').reset();
        }
    });

    // Initialize UI
    updateSavingsDisplay();
    updateTransactionList();

    // Show/hide appropriate categories based on transaction type
    document.getElementById('transactionType').addEventListener('change', function() {
        const transactionType = this.value;
        const categorySelect = document.getElementById('category');
        const options = categorySelect.options;
        
        if (transactionType === 'save') {
            // For saving, only show Account Transfer and Others
            for (let i = 0; i < options.length; i++) {
                const option = options[i];
                if (option.value === 'Account Transfer' || option.value === 'Others') {
                    option.style.display = '';
                } else {
                    option.style.display = 'none';
                }
            }
            // Set default to Account Transfer
            categorySelect.value = 'Account Transfer';
        } else {
            // For spending, show all except Account Transfer
            for (let i = 0; i < options.length; i++) {
                options[i].style.display = '';
            }
            // Set default to first non-Account Transfer option
            if (categorySelect.value === 'Account Transfer') {
                categorySelect.value = 'Accommodation and Utilities';
            }
        }
    });

    // Log out button functionality
    document.querySelector('.log-out').addEventListener('click', function() {
        alert('Logging out...');
        // In a real application, this would redirect to a logout endpoint
    });
});
