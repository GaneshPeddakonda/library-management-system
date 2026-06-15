// js/dashboard.js
requireAuth();
async function loadStats() {
  const res = await apiCall('/reports/stats');
  if (!res || res.status !== 'success') return;
  const s = res.data;
  document.getElementById('stat-books').textContent   = s.total_books   ?? 0;
  document.getElementById('stat-members').textContent = s.total_members  ?? 0;
  document.getElementById('stat-issued').textContent  = s.active_issues  ?? 0;
  document.getElementById('stat-overdue').textContent = s.overdue_books  ?? 0;
  document.getElementById('stat-fines').textContent   = '₹' + (s.fines_due ?? 0).toFixed(2);
}
loadStats();
