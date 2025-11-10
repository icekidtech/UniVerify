document.addEventListener('DOMContentLoaded', function() {
  const regenerateBtn = document.getElementById('regenerate-passcode-btn');
  const settingsForm = document.getElementById('settings-form');
  const feedbackDiv = document.getElementById('passcode-feedback');

  // Handle settings form submission
  if (settingsForm) {
    settingsForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const formData = new FormData(settingsForm);
      
      fetch(settingsForm.action, {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (response.ok) {
          showFeedback('Settings saved successfully!', 'success', feedbackDiv);
          setTimeout(() => {
            location.reload();
          }, 2000);
        } else {
          showFeedback('Error saving settings. Please try again.', 'error', feedbackDiv);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showFeedback('An error occurred. Please try again.', 'error', feedbackDiv);
      });
    });
  }

  // Handle passcode regeneration (Students only)
  if (regenerateBtn) {
    regenerateBtn.addEventListener('click', function() {
      if (confirm('Are you sure you want to regenerate your passcode? Your old passcode will no longer work.')) {
        fetch('/settings/regenerate-passcode', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            showFeedback(
              `New passcode generated: ${data.passcode}. Please save it in a safe place!`, 
              'success', 
              feedbackDiv
            );
            regenerateBtn.textContent = 'Passcode Regenerated ✓';
            regenerateBtn.disabled = true;
          } else {
            showFeedback(data.message || 'Error regenerating passcode', 'error', feedbackDiv);
          }
        })
        .catch(error => {
          console.error('Error:', error);
          showFeedback('An error occurred. Please try again.', 'error', feedbackDiv);
        });
      }
    });
  }

  function showFeedback(message, type, element) {
    if (!element) return;
    
    element.textContent = message;
    element.className = `feedback-message feedback-${type}`;
    element.style.display = 'block';
    
    if (type === 'success') {
      setTimeout(() => {
        element.style.display = 'none';
      }, 5000);
    }
  }
});