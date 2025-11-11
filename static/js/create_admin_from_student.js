// Admin creation from student account

let selectedStudent = null;

async function loadApprovedStudents() {
    try {
        const response = await fetch('/api/students/approved');
        const students = await response.json();
        displayStudents(students);
    } catch (error) {
        console.error('Error loading students:', error);
    }
}

function displayStudents(students) {
    const grid = document.getElementById('student-grid');
    grid.innerHTML = '';

    if (students.length === 0) {
        grid.innerHTML = '<p class="no-data">No approved students found.</p>';
        return;
    }

    students.forEach(student => {
        const card = document.createElement('div');
        card.className = 'student-card';
        card.innerHTML = `
            <div class="card-header">
                <h4>${student.name}</h4>
                <span class="badge badge-success">Approved</span>
            </div>
            <div class="card-body">
                <p><strong>Email:</strong> ${student.email}</p>
                <p><strong>Reg #:</strong> ${student.reg_number}</p>
                <p><strong>Department:</strong> ${student.department}</p>
                <p><strong>Series:</strong> <span class="series-badge">${student.series_code}</span></p>
            </div>
            <button class="btn-primary" onclick="selectStudent(${student.id}, '${student.name}', '${student.email}', '${student.reg_number}', '${student.department}', '${student.series_code}')">
                Select
            </button>
        `;
        grid.appendChild(card);
    });
}

function selectStudent(id, name, email, reg, dept, series) {
    selectedStudent = { id, name, email, reg, dept, series };
    
    document.getElementById('selected-student-id').value = id;
    document.getElementById('display-name').textContent = name;
    document.getElementById('display-email').textContent = email;
    document.getElementById('display-reg').textContent = reg;
    document.getElementById('display-dept').textContent = dept;
    document.getElementById('display-series').textContent = series;
    
    document.getElementById('summary-name').textContent = name;
    document.getElementById('summary-email').textContent = email;
    document.getElementById('summary-series').textContent = series;
    
    document.querySelector('.form-section').style.display = 'none';
    document.getElementById('admin-form').style.display = 'block';
}

function backToStudentSelection() {
    document.querySelector('.form-section').style.display = 'block';
    document.getElementById('admin-form').style.display = 'none';
    selectedStudent = null;
}

function updateDepartmentField() {
    const role = document.querySelector('input[name="role"]:checked').value;
    const deptGroup = document.getElementById('department-group');
    const deptSelect = document.getElementById('admin-department');
    
    if (role === 'admin') {
        deptGroup.style.display = 'block';
        deptSelect.required = true;
        document.getElementById('summary-dept').style.display = 'block';
    } else {
        deptGroup.style.display = 'none';
        deptSelect.required = false;
        document.getElementById('summary-dept').style.display = 'none';
    }
    
    updateSummary();
}

function togglePassword() {
    const input = document.getElementById('admin-password');
    input.type = input.type === 'password' ? 'text' : 'password';
}

function checkPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    
    return strength;
}

document.getElementById('admin-password')?.addEventListener('input', function() {
    const strength = checkPasswordStrength(this.value);
    const fill = document.getElementById('strength-fill');
    const text = document.getElementById('strength-text');
    
    const levels = ['Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];
    const colors = ['#f44336', '#ff9800', '#ffc107', '#4caf50', '#2e7d32'];
    
    fill.style.width = (strength * 25) + '%';
    fill.style.backgroundColor = colors[strength];
    text.textContent = levels[strength];
});

function validatePasswordMatch() {
    const pass = document.getElementById('admin-password').value;
    const confirm = document.getElementById('confirm-password').value;
    const mismatch = document.getElementById('password-mismatch');
    
    if (pass !== confirm) {
        mismatch.style.display = 'block';
    } else {
        mismatch.style.display = 'none';
    }
}

function updateSummary() {
    const role = document.querySelector('input[name="role"]:checked')?.value;
    const dept = document.getElementById('admin-department').value;
    
    document.getElementById('summary-role').textContent = role === 'super_admin' ? 'Super Admin' : 'Regular Admin';
    if (role === 'admin') {
        document.getElementById('summary-dept-value').textContent = dept || 'Not selected';
    }
}

// Search functionality
document.getElementById('student-search')?.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    document.querySelectorAll('.student-card').forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(searchTerm) ? 'block' : 'none';
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', loadApprovedStudents);