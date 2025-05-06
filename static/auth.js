// Common form handling for both pages
document.addEventListener('DOMContentLoaded', () => {
    // Sign Up Form Handling
    const signupForm = document.getElementById('signup-form');
    if(signupForm) {
      signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        // Add your signup logic here
        alert('Sign up successful!');
        window.location.href = 'index.html';
      });
    }
  
    // Sign In Form Handling
    const signinForm = document.getElementById('signin-form');
    if(signinForm) {
      signinForm.addEventListener('submit', (e) => {
        e.preventDefault();
        // Add your signin logic here
        alert('Sign in successful!');
        window.location.href = 'index.html';
      });
    }
  });