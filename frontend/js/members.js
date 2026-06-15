// js/members.js
requireAuth();
let editingMemberId = null;

async function loadMembers() {
  const res = await apiCall('/members/');
  const tbody = document.getElementById('members-table');
  if (!res || res.status !== 'success') { tbody.innerHTML = '<tr><td colspan="6">Failed to load</td></tr>'; return; }
  tbody.innerHTML = res.data.length ? res.data.map(m => `
    <tr>
      <td>${m.id}</td>
      <td><strong>${m.full_name}</strong></td>
      <td>${m.email}</td>
      <td>${m.phone || '–'}</td>
      <td><span class="badge badge-${m.status === 'active' ? 'success' : 'danger'}">${m.status}</span></td>
      <td>
        <button class="btn btn-sm btn-outline" onclick="openEditMember(${m.id})">Edit</button>
        <button class="btn btn-sm btn-danger"  onclick="deleteMember(${m.id})">Delete</button>
      </td>
    </tr>`).join('') : '<tr><td colspan="6">No members</td></tr>';
}

function openAddMember() {
  editingMemberId = null;
  document.getElementById('modal-title').textContent = 'Add Member';
  document.getElementById('member-form').reset();
  document.getElementById('member-modal').classList.add('open');
}

async function openEditMember(id) {
  const res = await apiCall('/members/' + id);
  if (!res || res.status !== 'success') return;
  const m = res.data;
  editingMemberId = id;
  document.getElementById('modal-title').textContent = 'Edit Member';
  ['full_name','email','phone','address'].forEach(f => {
    const el = document.getElementById('f-'+f);
    if (el) el.value = m[f] || '';
  });
  document.getElementById('member-modal').classList.add('open');
}

function closeModal() { document.getElementById('member-modal').classList.remove('open'); }

document.getElementById('member-form')?.addEventListener('submit', async function(e) {
  e.preventDefault();
  const body = {
    full_name: document.getElementById('f-full_name').value,
    email:     document.getElementById('f-email').value,
    phone:     document.getElementById('f-phone').value,
    address:   document.getElementById('f-address').value
  };
  const res = editingMemberId
    ? await apiCall('/members/' + editingMemberId, 'PUT', body)
    : await apiCall('/members/', 'POST', body);
  if (res?.status === 'success') { closeModal(); showAlert('#alert-area', editingMemberId ? 'Member updated!' : 'Member added!'); loadMembers(); }
  else showAlert('#alert-area', res?.message || 'Error', 'error');
});

async function deleteMember(id) {
  if (!confirm('Delete this member?')) return;
  const res = await apiCall('/members/' + id, 'DELETE');
  if (res?.status === 'success') { showAlert('#alert-area', 'Member deleted'); loadMembers(); }
  else showAlert('#alert-area', res?.message || 'Error', 'error');
}

loadMembers();
