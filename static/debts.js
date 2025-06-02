document.addEventListener('DOMContentLoaded', function() {
    let loanData = {
        loans: []
    };

    function formatCurrency(amount) {
        return 'Rp ' + amount.toLocaleString('id-ID', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    function createLoanElement(loan, index) {
        const loanItem = document.createElement('div');
        loanItem.className = "transaction-item expense";
        loanItem.innerHTML = `
            <div class="transaction-details" style="display: flex; flex-direction: column;">
                <div>
                    <div class="transaction-category">${loan.details}</div>
                    <div class="loan-details">${formatCurrency(loan.amount)} (${loan.interest}% interest)</div>
                    <button class="submit-btn" style="width:auto; padding:6px 12px; font-size:14px; margin-top:8px;" data-index="${index}">Calculate</button>
                </div>
                <div class="loan-calc-anim">
                    <div class="loan-calc-content">
                        <label>Months to pay: 
                            <input type="number" class="months-input" min="1" value="12" style="width:60px; margin-left:10px;">
                        </label>
                        <button class="submit-btn calc-monthly-btn" style="width:auto; padding:4px 10px; font-size:13px; margin-left:8px;">Calculate Monthly</button>
                    </div>
                    <div class="monthly-result"></div>
                </div>
            </div>
        `;
        return loanItem;
    }


    function updateLoanList() {
        const loanList = document.getElementById('loanList');
        loanList.innerHTML = '';
        loanData.loans.forEach((loan, idx) => {
            const el = createLoanElement(loan, idx);
            loanList.appendChild(el);
        });

        // Accordion Animation logic
        document.querySelectorAll('.submit-btn[data-index]').forEach(btn => {
            btn.addEventListener('click', function() {
                const loanItem = this.closest('.transaction-item');
                const calcDiv = loanItem.querySelector('.loan-calc-anim');
                // Close others if you want only one open at a time (optional)
                document.querySelectorAll('.loan-calc-anim.open').forEach(openDiv => {
                    if (openDiv !== calcDiv) openDiv.classList.remove('open');
                });
                // Toggle current
                calcDiv.classList.toggle('open');
            });
        });

        document.querySelectorAll('.calc-monthly-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const loanItem = this.closest('.transaction-item');
                const idx = Array.from(loanItem.parentNode.children).indexOf(loanItem);
                const loan = loanData.loans[idx];
                const monthsInput = loanItem.querySelector('.months-input');
                const months = parseInt(monthsInput.value) || 1;
                const totalAmount = loan.amount + (loan.amount * loan.interest / 100);
                const perMonth = totalAmount / months;
                loanItem.querySelector('.monthly-result').textContent =
                    `Total: ${formatCurrency(totalAmount)} | Per Month: ${formatCurrency(perMonth)}`;
            });
        });
    }

    document.getElementById('loanForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const amount = parseFloat(document.getElementById('loanAmount').value);
        const details = document.getElementById('loanDetails').value;
        const interest = parseFloat(document.getElementById('interestRate').value);
        if (isNaN(amount) || amount <= 0 || isNaN(interest) || interest < 0 || details.trim() === '') {
            alert('Please enter valid loan details.');
            return;
        }
        loanData.loans.push({ amount, details, interest });
        updateLoanList();
        this.reset();
    });

    updateLoanList();
});
