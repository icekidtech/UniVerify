// Passcode Backup Page Functions

function copyToClipboard() {
    const passcodeElement = document.querySelector('.passcode-code');
    const passcode = passcodeElement.textContent.trim();
    
    navigator.clipboard.writeText(passcode).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    }).catch(() => {
        alert('Failed to copy passcode. Please try again.');
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const confirmCheckbox = document.getElementById('confirmCheckbox');
    const continueBtn = document.getElementById('continueBtn');

    if (confirmCheckbox && continueBtn) {
        // Set initial state
        continueBtn.disabled = true;

        confirmCheckbox.addEventListener('change', function() {
            continueBtn.disabled = !this.checked;
        });
    }

    // Add copy button functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', copyToClipboard);
    });
});
