// Series management functionality

function openSeriesModal() {
    document.getElementById('series-modal').style.display = 'block';
    document.getElementById('series-form').reset();
    document.getElementById('modal-title').textContent = 'Create New Series';
}

function closeSeriesModal() {
    document.getElementById('series-modal').style.display = 'none';
}

function viewSeriesDetails(seriesId) {
    // Fetch series details via AJAX
    fetch(`/api/series/${seriesId}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById('detail-series-code').textContent = data.series_code;
            document.getElementById('detail-code').textContent = data.series_code;
            document.getElementById('detail-name').textContent = data.name;
            document.getElementById('detail-status').textContent = data.is_active ? '✓ Active' : '✗ Inactive';
            document.getElementById('detail-created').textContent = new Date(data.created_at).toLocaleDateString();
            document.getElementById('detail-description').textContent = data.description || 'N/A';
            
            document.getElementById('details-modal').style.display = 'block';
        });
}

function closeDetailsModal() {
    document.getElementById('details-modal').style.display = 'none';
}

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

function editSeries(seriesId) {
    // Load series data and populate form for editing
    fetch(`/api/series/${seriesId}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById('series-code').value = data.series_code;
            document.getElementById('series-name').value = data.name;
            document.getElementById('series-description').value = data.description;
            document.getElementById('series-status').value = data.is_active;
            document.getElementById('modal-title').textContent = `Edit Series: ${data.series_code}`;
            document.getElementById('series-form').action = `/api/series/${seriesId}/update`;
            document.getElementById('series-modal').style.display = 'block';
        });
}

function deleteSeries(seriesId) {
    if (confirm('Are you sure you want to delete this series? This action cannot be undone.')) {
        fetch(`/api/series/${seriesId}/delete`, { method: 'POST' })
            .then(r => {
                if (r.ok) {
                    location.reload();
                } else {
                    alert('Error deleting series');
                }
            });
    }
}

document.getElementById('add-series-btn')?.addEventListener('click', openSeriesModal);
window.onclick = function(event) {
    const modal = document.getElementById('series-modal');
    if (event.target == modal) modal.style.display = 'none';
};