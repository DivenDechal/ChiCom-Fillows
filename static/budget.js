document.addEventListener('DOMContentLoaded', function () {
  const rawData = document.getElementById('category-data');
  let categoryData = null;

  try {
    categoryData = JSON.parse(rawData.textContent);
  } catch (e) {
    console.error('Failed to parse category data:', e);
    return;
  }

  if (!categoryData || !categoryData.labels || !categoryData.values) {
    console.error('categoryData is missing labels or values.');
    return;
  }

  const chartContainer = document.querySelector('.chart-container');
  const chartCanvas = document.getElementById('budgetChart');
  const noDataMessage = document.getElementById('no-data-message');

  // Show no-data message & hide chart if data is the fallback "No Data"
  if (categoryData.labels.length === 1 && categoryData.labels[0] === "No Data") {
    chartCanvas.style.display = 'none';
    noDataMessage.style.display = 'block';
    chartContainer.classList.remove('has-chart');
    chartContainer.classList.add('no-chart');
    return;
  } else {
    chartCanvas.style.display = 'block';
    noDataMessage.style.display = 'none';
    chartContainer.classList.add('has-chart');
    chartContainer.classList.remove('no-chart');
  }

  // Prepare chart data
  const chartData = {
    labels: categoryData.labels,
    datasets: [{
      data: categoryData.values,
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

  // Create doughnut chart
  const ctx = chartCanvas.getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: chartData,
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

  // Hover effect on categories
  document.querySelectorAll('.category').forEach(category => {
    category.addEventListener('mouseenter', function () {
      this.style.cursor = 'pointer';
    });
  });

  // Navigation active state toggling
  document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelectorAll('nav a').forEach(l => l.classList.remove('active'));
      this.classList.add('active');
      window.location.href = this.getAttribute('href') || this.getAttribute('onclick').match(/'(.*)'/)[1];
    });
  });

  // Log out button placeholder
  const logOutBtn = document.querySelector('.log-out');
  if (logOutBtn) {
    logOutBtn.addEventListener('click', function () {
      alert('Logging out...');
      // Add logout logic here
    });
  }
});
