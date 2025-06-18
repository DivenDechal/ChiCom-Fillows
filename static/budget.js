/**
 * Budget Tracker JavaScript
 * Fillow Application
 */

document.addEventListener('DOMContentLoaded', function () {
  // Parse chart data from embedded script
  const categoryDataScript = document.getElementById('category-data');
  let chartData = {};
  if (categoryDataScript) {
    try {
      chartData = JSON.parse(categoryDataScript.textContent);
    } catch (e) {
      console.error('Invalid category data:', e);
    }
  }

  // Chart.js Doughnut Chart
  const ctx = document.getElementById('budgetChart').getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: chartData.labels || [],
      datasets: [{
        data: chartData.values || [],
        backgroundColor: [
          '#3465A4',
          '#5e17eb',
          '#FCBF49',
          '#103778',
          '#ffc154',
          '#333333'
        ],
        borderWidth: 0,
        cutout: '70%'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function (context) {
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

  // Add hover pointer to categories
  document.querySelectorAll('.category').forEach(category => {
    category.addEventListener('mouseenter', () => {
      category.style.cursor = 'pointer';
    });
  });

  // Modal open buttons (Add / View)
  document.querySelectorAll('.add-btn, .view-btn').forEach(button => {
    button.addEventListener('click', () => {
      const modalId = button.getAttribute('data-modal');
      const modal = document.getElementById(modalId);
      if (modal) {
        modal.style.display = 'block';
      }
    });
  });

  // Modal close buttons
  document.querySelectorAll('.close-btn').forEach(button => {
    button.addEventListener('click', () => {
      const modalId = button.getAttribute('data-modal');
      const modal = document.getElementById(modalId);
      if (modal) {
        modal.style.display = 'none';
      }
    });
  });

  // Close modal when clicking outside the modal-content
  window.addEventListener('click', e => {
    if (e.target.classList.contains('modal')) {
      e.target.style.display = 'none';
    }
  });
});
