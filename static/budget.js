/**
 * Budget Tracker JavaScript
 * Fillow Application
 * Filename: /static/budget.js
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
                legend: {
                    display: false
                },
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


    // Log out button functionality
    const logOutBtn = document.querySelector('.log-out');
    logOutBtn.addEventListener('click', function() {
        alert('Logging out...');
        // In a real application, this would redirect to a logout endpoint
    });
});