// js/issue.js
requireAuth();

async function loadIssues() {
  const res = await apiCall('/issues/');
  const tbody = document.getElementById('issues-table');
  if (!res || res.status !== 'success') { tbody.innerHTML = '<tr><td colspan="6">Failed to load</td></tr>'; return; }
  tbody.innerHTML = res.data.length ? res.data.map(i => {
    // FIX: compare date strings directly (YYYY-MM-DD) to avoid UTC/local timezone
    // mismatch where new Date("2026-06-11") is parsed as UTC midnight and
    // compared against local time — causing false "overdue" on the due day itself.
    const todayStr = new Date().toLocaleDateString('en-CA'); // "YYYY-MM-DD" in local time
    const overdue = i.due_date < todayStr;
    return `<tr>
      <td>${i.id}</td>
      <td>${i.title}</td>
      <td>${i.member_name}</td>
      <td>${i.issue_date}</td>
      <td><span class="badge badge-${overdue ? 'danger' : 'warning'}">${i.due_date}${overdue ? ' ⚠' : ''}</span></td>
      <td><button class="btn btn-sm btn-success" onclick="returnBook(${i.id})">Return</button></td>
    </tr>`;
  }).join('') : '<tr><td colspan="6">No active issues</td></tr>';
}

document.getElementById('issue-form')?.addEventListener('submit', async function(e) {
  e.preventDefault();
  const body = {
    book_id:   +document.getElementById('f-book_id').value,
    member_id: +document.getElementById('f-member_id').value
  };
  const res = await apiCall('/issues/', 'POST', body);
  if (res?.status === 'success') {
    showAlert('#alert-area', `Book issued! Due: ${res.data.due_date}`);
    this.reset();
    loadIssues();
  } else showAlert('#alert-area', res?.message || 'Error', 'error');
});

async function returnBook(issue_id) {
  if (!confirm('Mark this book as returned?')) return;
  const res = await apiCall('/issues/return/' + issue_id, 'POST');
  if (res?.status === 'success') {
    const fine = res.data?.fine;
    showAlert('#alert-area', fine > 0 ? `Returned. Fine: ₹${fine}` : 'Book returned successfully!');
    loadIssues();
  } else showAlert('#alert-area', res?.message || 'Error', 'error');
}

loadIssues();
