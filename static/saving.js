document.addEventListener('DOMContentLoaded', function () {
    // Format currency (optional, unused in this version)
    function formatCurrency(amount) {
        return 'Rp ' + amount.toLocaleString('id-ID', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    
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