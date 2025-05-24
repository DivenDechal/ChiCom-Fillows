document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('signup-form');
  const errorBox = document.getElementById('signup-form-error');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (errorBox) errorBox.textContent = '';

    const formData = new FormData(form);
    const username = formData.get('username');
    const password = formData.get('password');
    const confirmPassword = formData.get('confirm_password');
    const monthlyIncome = formData.get('monthly_income');
    const savingPercentage = formData.get('saving_percentage');

    // Basic Validation
    if (!username || !password || !confirmPassword || !monthlyIncome || !savingPercentage) {
      return showError('All fields are required.');
    }

    if (password !== confirmPassword) {
      return showError('Passwords do not match.');
    }

    if (password.length < 6) {
      return showError('Password must be at least 6 characters long.');
    }

    const income = parseFloat(monthlyIncome);
    const saving = parseInt(savingPercentage);

    if (isNaN(income) || income < 0) {
      return showError('Monthly income must be a positive number.');
    }

    if (isNaN(saving) || saving < 0 || saving > 100) {
      return showError('Saving percentage must be between 0 and 100.');
    }

    try {
      const data = new URLSearchParams(formData);

      const response = await fetch('/auth/signup', {
        method: 'POST',
        body: data,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      const result = await response.json();

      if (response.ok && result.success) {
        alert('Sign up successful!');
        // Optional: Redirect after signup
        // window.location.href = '/login';
      } else {
        showError(result.message || 'An error occurred.');
      }
    } catch (error) {
      console.error('Signup error:', error);
      showError('An unexpected error occurred. Please try again.');
    }

    function showError(message) {
      if (errorBox) {
        errorBox.textContent = message;
      } else {
        alert(message);
      }
    }
  });
});
