document.addEventListener('DOMContentLoaded', function () {
    // Format currency (optional, unused in this version)
    function formatCurrency(amount) {
        return 'Rp ' + amount.toLocaleString('id-ID', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    // Handle form submission via AJAX
    document.getElementById('transactionForm').addEventListener('submit', async function (e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const amount = parseFloat(formData.get('amount'));
        const submitBtn = form.querySelector('.submit-btn');

        if (isNaN(amount) || amount <= 0) {
            alert('Please enter a valid amount');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const result = await response.json(); // may throw if not JSON

            if (response.ok) {
                if (result.success) {
                    window.location.reload();
                } else {
                    alert(result.message || 'Transaction failed');
                }
            } else {
                alert(result.message || 'Transaction failed');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during transaction: ' + error.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Add Transaction';
        }
    });

    // Show/hide category based on transaction type
    function updateCategoryVisibility() {
        const transactionType = document.getElementById('transactionType').value;
        const categoryGroup = document.getElementById('categoryGroup');
        const categorySelect = document.getElementById('category');

        if (transactionType === 'save') {
            categoryGroup.style.display = 'none';
            categorySelect.required = false;
            categorySelect.value = '';
        } else {
            categoryGroup.style.display = 'block';
            categorySelect.required = true;
            if (!categorySelect.value) {
                categorySelect.value = 'Accommodation and Utilities';
            }
        }
    }

    document.getElementById('transactionType').addEventListener('change', updateCategoryVisibility);
    updateCategoryVisibility();

    const logoutBtn = document.querySelector('.log-out');
    if (logoutBtn && logoutBtn.hasAttribute('data-url')) {
        logoutBtn.addEventListener('click', function () {
            window.location.href = logoutBtn.getAttribute('data-url');
        });
    }
});
