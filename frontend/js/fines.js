// js/fines.js
requireAuth();
async function loadFines() {
  const res = await apiCall('/fines/');
  const tbody = document.getElementById('fines-table');
  if (!res || res.status !== 'success') { tbody.innerHTML = '<tr><td colspan="5">Failed to load</td></tr>'; return; }
  tbody.innerHTML = res.data.length ? res.data.map(f => `
    <tr>
      <td>${f.id}</td>
      <td>${f.member_name}</td>
      <td>${f.title}</td>
      <td>₹${parseFloat(f.amount).toFixed(2)}</td>
      <td>${f.paid
        ? '<span class="badge badge-success">Paid</span>'
        : `<button class="btn btn-sm btn-warning" onclick="payFine(${f.id})">Pay</button>`}
      </td>
    </tr>`).join('') : '<tr><td colspan="5">No fines</td></tr>';
}
async function payFine(id) {
  const res = await apiCall('/fines/pay/' + id, 'POST');
  if (res?.status === 'success') { showAlert('#alert-area', 'Fine paid!'); loadFines(); }
  else showAlert('#alert-area', 'Error', 'error');
}
loadFines();
