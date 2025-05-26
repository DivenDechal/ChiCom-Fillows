/**
 * Savings Tracker JavaScript
 * Fillow Application
 * Filename: saving.js
 */

document.addEventListener('DOMContentLoaded', function() {
    // Format currency function
    function formatCurrency(amount) {
        return 'Rp ' + amount.toLocaleString('id-ID', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    // Handle form submission with AJAX
    document.getElementById('transactionForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        const amount = parseFloat(formData.get('amount'));
        
        if (isNaN(amount) || amount <= 0) {
            alert('Please enter a valid amount');
            return;
        }
        
        try {
            const submitBtn = form.querySelector('.submit-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (response.redirected) {
                window.location.href = response.url;
            } else if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    window.location.reload(); // Refresh to get updated data
                } else {
                    alert(data.message || 'Transaction failed');
                }
            } else {
                const errorData = await response.json();
                alert(errorData.message || 'Transaction failed');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during transaction');
        } finally {
            const submitBtn = form.querySelector('.submit-btn');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Add Transaction';
        }
    });

    // Show/hide appropriate categories based on transaction type
    function updateCategoryVisibility() {
        const transactionType = document.getElementById('transactionType').value;
        const categorySelect = document.getElementById('category');
        
        Array.from(categorySelect.options).forEach(option => {
            if (transactionType === 'save') {
                option.hidden = !(option.value === 'Account Transfer' || option.value === 'Others');
            } else {
                option.hidden = option.value === 'Account Transfer';
            }
        });
        
        // Set default value
        if (transactionType === 'save') {
            categorySelect.value = 'Account Transfer';
        } else if (categorySelect.value === 'Account Transfer') {
            categorySelect.value = 'Accommodation and Utilities';
        }
    }

    document.getElementById('transactionType').addEventListener('change', updateCategoryVisibility);
    
    // Initialize category visibility
    updateCategoryVisibility();

    // Log out button functionality
    document.querySelector('.log-out').addEventListener('click', function() {
        window.location.href = "{{ url_for('BP_auth.logout') }}";
    });
});