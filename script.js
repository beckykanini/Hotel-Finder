document.addEventListener('DOMContentLoaded', function () {
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    const profileBtn = document.getElementById('profileBtn');
  
    loginBtn.addEventListener('click', function () {
      alert('Login button clicked');
      // Add login functionality here
    });
  
    signupBtn.addEventListener('click', function () {
      alert('Sign up button clicked');
      // Add sign up functionality here
    });
  
    profileBtn.addEventListener('click', function () {
      alert('Profile button clicked');
      // Add profile functionality here
    });
  });

  const signUpButton = document.getElementById('signUp');
  const signInButton = document.getElementById('signIn');
  const container = document.getElementById('container');
  
  signUpButton.addEventListener('click', () => {
      container.classList.add("right-panel-active");
  });
  
  signInButton.addEventListener('click', () => {
      container.classList.remove("right-panel-active");
  });