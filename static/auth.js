// Common form handling for both pages
document.addEventListener('DOMContentLoaded', () => {
    // Sign Up Form Handling
    const signupForm = document.getElementById('signup-form');
    if(signupForm) {
      signupForm.addEventListener('submit', async(e) => {
        e.preventDefault();
        // Add your signup logic here
        const formData = new FormData(signupForm)
        const data = new URLSearchParams(formData)
        try{
          const request = await fetch('/auth/signup', {
            method : 'POST',
            body : data
          })
          const result = await request.json();

          if(request.ok && result.success){
            alert('Sign up successful!');
          }else{
            alert(result.message || 'Sign in failed !');
          }
        }catch (error) {
          console.error('Signup error!','error')
          alert('An error occured. Please try again !')
        }
        
      });
    }
  });
    
    
  
    // Sign In Form Handling
    const signinForm = document.getElementById('signin-form');
    if(signinForm) {
      signinForm.addEventListener('submit', async(e) => {
        e.preventDefault();

        const formData = new FormData(signinForm)
        const data = new URLSearchParams(formData)
        // Add your signin logic here
        try{
          const request = await fetch('/auth/signin', {
            method : 'POST',
            body : data
          })
          const result = await request.json();

          if(request.ok && result.success){
            alert('Sign in successful!');
          }else{
            alert(result.message || 'Sign in failed !');
          }
        }catch (error) {
          console.error('Login error!','error')
          alert('An error occured. Please try again !')
        }
        
      });
    }
  