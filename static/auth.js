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

// Form validation function (Signup)
function validate() {
  const form = document.getElementById('signup-form');
  const username = document.getElementById('username');
  const email = document.getElementById('email');
  const password = document.getElementById('password');
  const confirm = document.getElementById('confirm_password');
  const income = document.getElementById('monthly_income');
  const saving = document.getElementById('saving_percentage');

  // Map each field to its error <p>
  const errs = {
    username: document.getElementById('usernameError'),
    email: document.getElementById('emailError'),
    password: document.getElementById('passwordError'),
    confirm: document.getElementById('confirmError'),
    income: document.getElementById('incomeError'),
    saving: document.getElementById('savingError'),
  };

  let valid = true;

  // Username > 8 chars
  if (username.value.trim().length <= 8) {
    errs.username.textContent = "Username must be longer than 8 characters.";
    errs.username.style.display = 'block';
    valid = false;
  } else {
    errs.username.style.display = 'none';
  }

  // Email must include '@' and '.'
  if (!/.+@.+\..+/.test(email.value.trim())) {
    errs.email.textContent = "Email must include '@' and '.'.";
    errs.email.style.display = 'block';
    valid = false;
  } else {
    errs.email.style.display = 'none';
  }

  // Password ≥ 8 chars
  if (password.value.length < 8) {
    errs.password.textContent = "Password must be at least 8 characters.";
    errs.password.style.display = 'block';
    valid = false;
  } else {
    errs.password.style.display = 'none';
  }

  // Confirm password matches
  if (confirm.value !== password.value) {
    errs.confirm.textContent = "Passwords do not match.";
    errs.confirm.style.display = 'block';
    valid = false;
  } else {
    errs.confirm.style.display = 'none';
  }

  // Monthly income must be integer
  if (!/^\d+$/.test(income.value.trim())) {
    errs.income.textContent = "Monthly income must be an integer.";
    errs.income.style.display = 'block';
    valid = false;
  } else {
    errs.income.style.display = 'none';
  }

  // Saving percentage integer between 0 and 100
  const sp = saving.value.trim();
  if (!/^\d+$/.test(sp) || +sp < 0 || +sp > 100) {
    errs.saving.textContent = "Saving % must be an integer between 0 and 100.";
    errs.saving.style.display = 'block';
    valid = false;
  } else {
    errs.saving.style.display = 'none';
  }

  return valid;
}

// Form validation function (Signin)
function validateSignIn() {
  const email = document.getElementById('email');
  const password = document.getElementById('password');
  const emailError = document.getElementById('emailError');
  const passwordError = document.getElementById('passwordError');
  
  let valid = true;

  // Email validation
  if (!/.+@.+\..+/.test(email.value.trim())) {
    emailError.textContent = "Please enter a valid email address.";
    emailError.style.display = 'block';
    valid = false;
  } else {
    emailError.style.display = 'none';
  }

  // Password validation
  if (password.value.length < 1) {
    passwordError.textContent = "Please enter your password.";
    passwordError.style.display = 'block';
    valid = false;
  } else {
    passwordError.style.display = 'none';
  }

  return valid;
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
  autoCloseFlashes();
  
  // Signup Form Handling
  const signupForm = document.getElementById('signup-form');
  if (signupForm) {
    signupForm.addEventListener('submit', function(e) {
      if (!validate()) {
        e.preventDefault();
      }
    });

    // Enter key validation for signup
    ['username','email','password','confirm_password','monthly_income','saving_percentage'].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('keypress', e => {
          if (e.key === 'Enter') {
            e.preventDefault();
            if (validate()) {
              signupForm.submit();
            }
          }
        });
      }
    });
  }

  // Signin Form Handling
  const signinForm = document.getElementById('signin-form');
  if (signinForm) {
    signinForm.addEventListener('submit', function(e) {
      if (!validateSignIn()) {
        e.preventDefault();
      }
    });

    // Enter key validation for signin
    ['email', 'password'].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('keypress', e => {
          if (e.key === 'Enter') {
            e.preventDefault();
            if (validateSignIn()) {
              signinForm.submit();
            }
          }
        });
      }
    });
  }
});