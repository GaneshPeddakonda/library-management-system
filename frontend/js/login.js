// js/login.js
document.getElementById('loginForm')?.addEventListener('submit', async function(e) {
  e.preventDefault();
  const btn = this.querySelector('button[type="submit"]');
  const errEl = document.getElementById('login-error');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Logging in…';
  errEl.textContent = '';

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;

  try {
    const res = await fetch('http://localhost:5000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (data.status === 'success') {
      localStorage.setItem('lms_token', data.data.token);
      localStorage.setItem('lms_user', JSON.stringify(data.data.user));
      window.location.href = 'dashboard.html';
    } else {
      errEl.textContent = data.message || 'Login failed';
    }
  } catch {
    errEl.textContent = 'Cannot connect to server. Is the backend running?';
  } finally {
    btn.disabled = false;
    btn.textContent = 'Login';
  }
});
