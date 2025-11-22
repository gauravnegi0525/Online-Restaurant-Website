const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const switchToSignup = document.getElementById('switch-to-signup');
const switchToLogin = document.getElementById('switch-to-login');

// Switch to Signup Form
switchToSignup.addEventListener('click', () => {
    loginForm.style.display = 'none';
    signupForm.style.display = 'block';
});

// Switch to Login Form
switchToLogin.addEventListener('click', () => {
    signupForm.style.display = 'none';
    loginForm.style.display = 'block';
});

// Handle Login
loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(loginForm);
    const data = Object.fromEntries(formData);
    // Perform login action (e.g., API call)
    console.log('Logging in:', data);
});

// Handle Signup
signupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(signupForm);
    const data = Object.fromEntries(formData);
    // Perform signup action (e.g., API call)
    console.log('Signing up:', data);
});