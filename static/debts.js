// debt.js
class LoanTracker {
    constructor() {
        this.loans = [];
        this.initializeEventListeners();
        this.renderLoans();
    }

    initializeEventListeners() {
        const form = document.getElementById('loanForm');
        form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    handleSubmit(e) {
        e.preventDefault();
        const amount = document.getElementById('loanAmount').value.replace(/\D/g, '');
        const details = document.getElementById('loanDetails').value;
        const rate = parseFloat(document.getElementById('interestRate').value);

        if (amount && details && rate >= 0) {
            const loan = {
                id: Date.now(),
                amount: parseInt(amount),
                details: details.trim(),
                interestRate: rate,
                dateAdded: new Date().toLocaleDateString('id-ID')
            };
            this.loans.push(loan);
            this.renderLoans();
            e.target.reset();
        }
    }

    renderLoans() {
        const loanList = document.getElementById('loanList');
        if (this.loans.length === 0) {
            loanList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-piggy-bank"></i>
                    <h3>No loans yet</h3>
                    <p>Add your first loan to start tracking your debts</p>
                </div>
            `;
            return;
        }
        const totalDebt = this.loans.reduce((sum, loan) => sum + loan.amount, 0);
        loanList.innerHTML = `
            <div class="transaction-item" style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); border-left: 4px solid #dc2626;">
                <div class="transaction-details">
                    <div class="transaction-category">Total Debt</div>
                    <div class="transaction-meta">Across ${this.loans.length} loan${this.loans.length > 1 ? 's' : ''}</div>
                </div>
                <div class="transaction-amount" style="color: #dc2626; font-size: 20px;">
                    Rp ${totalDebt.toLocaleString('id-ID')}
                </div>
            </div>
            ${this.loans.map(loan => this.renderLoanItem(loan)).join('')}
        `;
        // Attach toggle and calculation listeners
        this.loans.forEach(loan => {
            document.getElementById(`toggle-btn-${loan.id}`).onclick = () => this.toggleCalculator(loan.id);
            document.getElementById(`calc-btn-${loan.id}`).onclick = () => this.calculateLoan(loan.id, loan.amount, loan.interestRate);
            document.getElementById(`delete-btn-${loan.id}`).onclick = () => this.deleteLoan(loan.id);
        });
    }

    renderLoanItem(loan) {
        return `
            <div class="transaction-item">
                <div class="transaction-details">
                    <div class="transaction-category">${loan.details}</div>
                    <div class="transaction-meta">
                        ${loan.interestRate}% annual interest • Added ${loan.dateAdded}
                    </div>
                    <div class="loan-calc-anim" id="calc-${loan.id}">
                        <div class="loan-calc-content">
                            <span>Calculate for</span>
                            <input type="number" id="months-${loan.id}" placeholder="12" min="1" max="360" value="12">
                            <span>months</span>
                            <button id="calc-btn-${loan.id}">
                                Calculate
                            </button>
                        </div>
                        <div class="monthly-result" id="result-${loan.id}"></div>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
                    <div class="transaction-amount">
                        Rp ${loan.amount.toLocaleString('id-ID')}
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button id="toggle-btn-${loan.id}" 
                                style="background: #1a56bb; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; transition: all 0.3s ease;">
                            <i class="fas fa-calculator"></i> Calculate
                        </button>
                        <button id="delete-btn-${loan.id}" 
                                style="background: #ef4444; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; transition: all 0.3s ease;">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    toggleCalculator(loanId) {
        const calcElement = document.getElementById(`calc-${loanId}`);
        calcElement.classList.toggle('open');
    }

    calculateLoan(loanId, amount, interestRate) {
        const months = parseInt(document.getElementById(`months-${loanId}`).value) || 1;
        const years = months / 12;
        const interestAmount = amount * (interestRate / 100) * years;
        const totalAmount = amount + interestAmount;
        const perMonth = totalAmount / months;
        document.getElementById(`result-${loanId}`).textContent =
            `Total: Rp ${totalAmount.toLocaleString('id-ID', {minimumFractionDigits:2})} | Per Month: Rp ${perMonth.toLocaleString('id-ID', {minimumFractionDigits:2})}`;
    }

    deleteLoan(id) {
        if (confirm('Are you sure you want to delete this loan?')) {
            this.loans = this.loans.filter(loan => loan.id !== id);
            this.renderLoans();
        }
    }
}

// Initialize Loan Tracker globally for button onclick refs
const loanTracker = new LoanTracker();
