// script.js

// 1) Alert on successful registration
function registration_successful() {
  alert("Registration successful! Please check your email for confirmation.");
}

// 2) Perform all field checks; return true if valid, false otherwise
function validate() {
  const form     = document.getElementById('signup-form');
  const username = document.getElementById('username');
  const email    = document.getElementById('email');
  const password = document.getElementById('password');
  const confirm  = document.getElementById('confirm_password');
  const income   = document.getElementById('monthly_income');
  const saving   = document.getElementById('saving_percentage');

  // Map each field to its error <p>
  const errs = {
    username: document.getElementById('usernameError'),
    email:    document.getElementById('emailError'),
    password: document.getElementById('passwordError'),
    confirm:  document.getElementById('confirmError'),
    income:   document.getElementById('incomeError'),
    saving:   document.getElementById('savingError'),
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

// 3) Wire it all up on DOM load
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('signup-form');

  // On real submit, validate first
  form.addEventListener('submit', function(e) {
    if (!validate()) {
      // Prevent navigation if invalid
      e.preventDefault();
    } else {
      // All good: show alert, then allow form to submit
      registration_successful();
      // no need to call form.submit() manually
    }
  });

  // Optional: if you still want Enter in inputs to trigger validation
  ['username','email','password','confirm_password','monthly_income','saving_percentage']
    .forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('keypress', e => {
          if (e.key === 'Enter') {
            // Prevent double-submit
            e.preventDefault();
            if (validate()) {
              registration_successful();
              form.submit();
            }
          }
        });
      }
    });
});
