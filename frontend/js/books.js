// js/books.js
requireAuth();
let editingId = null;

async function loadBooks(q = '') {
  const path = q ? `/books/?q=${encodeURIComponent(q)}` : '/books/';
  const res = await apiCall(path);
  const tbody = document.getElementById('books-table');
  if (!res || res.status !== 'success') { tbody.innerHTML = '<tr><td colspan="7">Failed to load books</td></tr>'; return; }
  tbody.innerHTML = res.data.length ? res.data.map(b => `
    <tr>
      <td>${b.id}</td>
      <td><strong>${b.title}</strong></td>
      <td>${b.author}</td>
      <td>${b.category || '–'}</td>
      <td>${b.isbn || '–'}</td>
      <td>
        <span class="badge ${b.available_copies > 0 ? 'badge-success' : 'badge-danger'}">
          ${b.available_copies}/${b.total_copies}
        </span>
      </td>
      <td>
        <button class="btn btn-sm btn-outline" onclick="openEdit(${b.id})">Edit</button>
        <button class="btn btn-sm btn-danger"  onclick="deleteBook(${b.id})">Delete</button>
      </td>
    </tr>`).join('') : '<tr><td colspan="7">No books found</td></tr>';
}

function openAdd() {
  editingId = null;
  document.getElementById('modal-title').textContent = 'Add Book';
  document.getElementById('book-form').reset();
  document.getElementById('book-modal').classList.add('open');
}

async function openEdit(id) {
  const res = await apiCall('/books/' + id);
  if (!res || res.status !== 'success') return;
  const b = res.data;
  editingId = id;
  document.getElementById('modal-title').textContent = 'Edit Book';
  ['title','author','isbn','category','publisher','year','copies'].forEach(f => {
    const el = document.getElementById('f-'+f);
    if (el) el.value = b[f === 'copies' ? 'total_copies' : f] || '';
  });
  document.getElementById('book-modal').classList.add('open');
}

function closeModal() { document.getElementById('book-modal').classList.remove('open'); }

document.getElementById('book-form')?.addEventListener('submit', async function(e) {
  e.preventDefault();
  const body = {
    title:     document.getElementById('f-title').value,
    author:    document.getElementById('f-author').value,
    isbn:      document.getElementById('f-isbn').value,
    category:  document.getElementById('f-category').value,
    publisher: document.getElementById('f-publisher').value,
    year:      +document.getElementById('f-year').value || null,
    copies:    +document.getElementById('f-copies').value || 1
  };
  const res = editingId
    ? await apiCall('/books/' + editingId, 'PUT', body)
    : await apiCall('/books/', 'POST', body);
  if (res?.status === 'success') {
    closeModal();
    showAlert('#alert-area', editingId ? 'Book updated!' : 'Book added!');
    loadBooks();
  } else {
    showAlert('#alert-area', res?.message || 'Error', 'error');
  }
});

async function deleteBook(id) {
  if (!confirm('Delete this book?')) return;
  const res = await apiCall('/books/' + id, 'DELETE');
  if (res?.status === 'success') { showAlert('#alert-area', 'Book deleted'); loadBooks(); }
  else showAlert('#alert-area', res?.message || 'Error', 'error');
}

document.getElementById('search-input')?.addEventListener('input', function() {
  loadBooks(this.value);
});

loadBooks();
