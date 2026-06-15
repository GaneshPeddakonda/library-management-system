// js/api.js  –  API base config & shared helpers
const API_BASE = 'http://localhost:5000/api';

function getToken() { return localStorage.getItem('lms_token'); }
function getUser()  { try { return JSON.parse(localStorage.getItem('lms_user')); } catch { return null; } }

function authHeader() {
  const t = getToken();
  return t ? { 'Authorization': `Bearer ${t}`, 'Content-Type': 'application/json' }
           : { 'Content-Type': 'application/json' };
}

async function apiCall(path, method = 'GET', body = null) {
  const opts = { method, headers: authHeader() };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API_BASE + path, opts);
  const data = await res.json();
  if (res.status === 401) { logout(); return; }
  return data;
}

function logout() {
  localStorage.removeItem('lms_token');
  localStorage.removeItem('lms_user');
  window.location.href = 'login.html';
}

function requireAuth() {
  if (!getToken()) { window.location.href = 'login.html'; }
}

function showAlert(container, msg, type = 'success') {
  const el = document.querySelector(container);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
  setTimeout(() => { if (el) el.innerHTML = ''; }, 4000);
}

// Highlight active nav link
document.addEventListener('DOMContentLoaded', () => {
  const page = window.location.pathname.split('/').pop();
  document.querySelectorAll('nav a').forEach(a => {
    if (a.getAttribute('href') === page) a.classList.add('active');
  });
  const user = getUser();
  const nameEl = document.getElementById('user-name');
  if (nameEl && user) nameEl.textContent = user.full_name;
});
