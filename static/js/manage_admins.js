document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('admin-modal');
  const addAdminBtn = document.getElementById('add-admin-btn');
  const closeBtn = document.querySelector('.close');
  const cancelBtn = document.querySelector('.btn-cancel');
  const adminForm = document.getElementById('admin-form');
  const passwordHint = document.getElementById('password-hint');
  const modalTitle = document.getElementById('modal-title');
  const passwordInput = document.getElementById('admin-password');

  let editingAdminId = null;

  // Open modal for new admin
  addAdminBtn.addEventListener('click', function() {
    editingAdminId = null;
    modalTitle.textContent = 'Add New Admin';
    adminForm.reset();
    passwordHint.style.display = 'none';
    passwordInput.required = true;
    adminForm.action = '/admin/add-admin';
    modal.style.display = 'block';
  });

  // Close modal
  closeBtn.addEventListener('click', () => modal.style.display = 'none');
  cancelBtn.addEventListener('click', () => modal.style.display = 'none');
  window.addEventListener('click', (e) => {
    if (e.target === modal) modal.style.display = 'none';
  });

  // Handle edit buttons
  document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const adminId = this.href.split('/').pop();
      editingAdminId = adminId;
      
      fetch(`/admin/get-admin/${adminId}`)
        .then(res => res.json())
        .then(admin => {
          document.getElementById('admin-name').value = admin.name;
          document.getElementById('admin-email').value = admin.email;
          document.getElementById('admin-role').value = admin.role;
          document.getElementById('admin-department').value = admin.department || '';
          document.getElementById('admin-status').value = admin.is_active;
          
          modalTitle.textContent = 'Edit Admin';
          passwordInput.required = false;
          passwordHint.style.display = 'block';
          adminForm.action = `/admin/update-admin/${adminId}`;
          modal.style.display = 'block';
        })
        .catch(error => console.error('Error:', error));
    });
  });

  // Handle form submission
  adminForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(adminForm);
    
    fetch(adminForm.action, {
      method: 'POST',
      body: formData
    })
    .then(response => {
      if (response.ok) {
        location.reload();
      } else {
        alert('Error saving admin. Please try again.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    });
  });

  // Handle toggle status
  document.querySelectorAll('.btn-toggle-status').forEach(btn => {
    btn.addEventListener('click', function() {
      const adminId = this.dataset.adminId;
      const currentStatus = this.dataset.status === 'True' || this.dataset.status === 'true';
      
      fetch(`/admin/toggle-admin-status/${adminId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ is_active: !currentStatus })
      })
      .then(response => {
        if (response.ok) {
          location.reload();
        } else {
          alert('Error updating admin status');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred');
      });
    });
  });

  // Handle delete
  document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', function() {
      if (confirm('Are you sure you want to delete this admin? This action cannot be undone.')) {
        const adminId = this.dataset.adminId;
        
        fetch(`/admin/delete-admin/${adminId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => {
          if (response.ok) {
            location.reload();
          } else {
            alert('Error deleting admin');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('An error occurred');
        });
      }
    });
  });
});