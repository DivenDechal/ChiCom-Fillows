/**
 * Savings Tracker JavaScript
 * Fillow Application
 * Filename: saving.js
 */

function closeFlash(button) {
  const flashMessage = button.parentElement;
  flashMessage.style.animation = 'slideOut 0.3s ease-in forwards';
  setTimeout(() => {
    flashMessage.remove();
  }, 300);
}

// Auto-close flash messages after 4 seconds
function autoCloseFlashes() {
  const flashMessages = document.querySelectorAll('.flash-message');
  flashMessages.forEach((flash, index) => {
    setTimeout(() => {
      if (flash.parentElement) {
        flash.style.animation = 'slideOut 0.3s ease-in forwards';
        setTimeout(() => {
          if (flash.parentElement) {
            flash.remove();
          }
        }, 300);
      }
    }, 4000 + (index * 200)); // Stagger the auto-close
  });
}

// Initialize auto-close when page loads
document.addEventListener('DOMContentLoaded', function() {
  autoCloseFlashes();
});

// Demo button to test flash messages
function addDemoFlash() {
  const container = document.getElementById('flashContainer');
  const messages = [
    { type: 'success', icon: '✓', text: 'Operation completed successfully!' },
    { type: 'error', icon: '!', text: 'An error occurred. Please try again.' },
    { type: 'warning', icon: '⚠', text: 'Please check your input values.' },
    { type: 'info', icon: 'i', text: 'New feature available in settings.' }
  ];
      
  const randomMessage = messages[Math.floor(Math.random() * messages.length)];
      
  const flashDiv = document.createElement('div');
  flashDiv.className = `flash-message ${randomMessage.type}`;
  flashDiv.innerHTML = `
    <div class="flash-content">
      <div class="flash-icon">${randomMessage.icon}</div>
      <div class="flash-text">${randomMessage.text}</div>
    </div>
    <button class="flash-close" onclick="closeFlash(this)">&times;</button>
  `;
      
  container.appendChild(flashDiv);
      
  // Auto-close this message
  setTimeout(() => {
    if (flashDiv.parentElement) {
      flashDiv.style.animation = 'slideOut 0.3s ease-in forwards';
      setTimeout(() => {
        if (flashDiv.parentElement) {
          flashDiv.remove();
        }
      }, 300);
    }
  }, 4000);
}

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

    // Handle form submission
    document.getElementById('transactionForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form values
        const type = document.getElementById('transactionType').value;
        const category = document.getElementById('category').value;
        const amount = parseFloat(document.getElementById('amount').value);
        
        if (isNaN(amount) || amount <= 0) {
            alert('Please enter a valid amount');
            return;
        }
        
        // Create new transaction
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
        
        // Reset form
        document.getElementById('transactionForm').reset();
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