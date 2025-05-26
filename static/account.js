// account.js

// Form submission handler
document.getElementById('profileForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    
    // Update display name and avatar
    document.getElementById('displayName').textContent = `${firstName} ${lastName}`;
    document.getElementById('profileAvatar').textContent = `${firstName[0]}${lastName[0]}`;
    
    // Show success message
    alert('Profile updated successfully!');
});

// Toggle setting function
function toggleSetting(toggle) {
    toggle.classList.toggle('active');
}

// Reset form function
function resetForm() {
    document.getElementById('profileForm').reset();
    document.getElementById('firstName').value = 'John';
    document.getElementById('lastName').value = 'Doe';
    document.getElementById('email').value = 'john.doe@example.com';
    document.getElementById('phone').value = '+62 812-3456-7890';
    document.getElementById('dateOfBirth').value = '1990-01-15';
}

// Change password function
function changePassword() {
    const newPassword = prompt('Enter your new password:');
    if (newPassword) {
        alert('Password changed successfully!');
    }
}

// Download data function
function downloadData() {
    alert('Your data export will be sent to your email address within 24 hours.');
}

// Show logout modal
function showLogoutModal() {
    document.getElementById('logoutModal').style.display = 'block';
}

// Close modal
function closeModal() {
    document.getElementById('logoutModal').style.display = 'none';
}

// Confirm logout
function confirmLogout() {
    alert('You have been signed out successfully!');
    // In a real application, this would redirect to login page
    window.location.href = '/login';
}

// Delete account function
function deleteAccount() {
    const confirmation = confirm('Are you sure you want to delete your account? This action cannot be undone.');
    if (confirmation) {
        const finalConfirmation = prompt('Type "DELETE" to confirm account deletion:');
        if (finalConfirmation === 'DELETE') {
            alert('Account deletion request submitted. Your account will be deleted within 30 days.');
        }
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('logoutModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Update avatar when name changes
document.getElementById('firstName').addEventListener('input', updateAvatar);
document.getElementById('lastName').addEventListener('input', updateAvatar);

function updateAvatar() {
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    
    if (firstName && lastName) {
        document.getElementById('profileAvatar').textContent = `${firstName[0].toUpperCase()}${lastName[0].toUpperCase()}`;
    }
}
