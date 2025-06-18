// DOM Elements
const profileForm = document.getElementById('profileForm');
const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const incomeInput = document.getElementById('income');
const savingRatioInput = document.getElementById('savingRatio');
const profileAvatar = document.getElementById('profileAvatar');
const displayName = document.getElementById('displayName');

// Modal Elements
const passwordModal = document.getElementById('passwordModal');
const passwordForm = document.getElementById('passwordForm');
const newPasswordInput = document.getElementById('newPassword');
const deleteModal = document.getElementById('deleteModal');
const deleteConfirmInput = document.getElementById('deleteConfirmInput');

// Buttons
const changePasswordBtn = document.getElementById('changePasswordBtn');
const cancelPasswordBtn = document.getElementById('cancelPasswordBtn');
const deleteAccountBtn = document.getElementById('deleteAccountBtn');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
const logoutBtn = document.getElementById('logoutBtn');

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Initialize event listeners
    initEventListeners();
});

function initEventListeners() {
    // Profile form submission
    if (profileForm) {
        profileForm.addEventListener('submit', handleProfileSubmit);
    }
    
    // Username input for real-time updates
    if (usernameInput) {
        usernameInput.addEventListener('input', updateAvatar);
    }
    
    // Password modal buttons
    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', openPasswordModal);
    }
    if (cancelPasswordBtn) {
        cancelPasswordBtn.addEventListener('click', closePasswordModal);
    }
    
    // Password form submission
    if (passwordForm) {
        passwordForm.addEventListener('submit', handlePasswordSubmit);
    }
    
    // Delete account buttons
    if (deleteAccountBtn) {
        deleteAccountBtn.addEventListener('click', openDeleteModal);
    }
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', deleteAccount);
    }
    if (cancelDeleteBtn) {
        cancelDeleteBtn.addEventListener('click', closeDeleteModal);
    }
    
    // Logout button
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
    
    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === passwordModal) {
            closePasswordModal();
        }
        if (event.target === deleteModal) {
            closeDeleteModal();
        }
    });
}

// Update avatar when username changes
function updateAvatar() {
    const username = usernameInput.value.trim();
    if (displayName) displayName.textContent = username;
    if (profileAvatar) {
        profileAvatar.textContent = username.length >= 2 
            ? `${username[0].toUpperCase()}${username[username.length-1].toUpperCase()}`
            : username[0].toUpperCase();
    }
}

// Profile form submit handler
async function handleProfileSubmit(e) {
    e.preventDefault();
    const data = {
        username: usernameInput.value,
        email: emailInput.value,
        income: incomeInput.value,
        savingRatio: savingRatioInput.value
    };
    
    try {
        const response = await fetch('/update_profile', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        const res = await response.json();
        alert(res.message);
        if (res.success) {
            // Update display without reloading
            if (displayName) displayName.textContent = data.username;
            if (profileAvatar) {
                profileAvatar.textContent = data.username.length >= 2 
                    ? `${data.username[0].toUpperCase()}${data.username[data.username.length-1].toUpperCase()}`
                    : data.username[0].toUpperCase();
            }
        }
    } catch (error) {
        alert('An error occurred. Please try again.');
    }
}

// Password modal functions
function openPasswordModal() {
    if (passwordModal) passwordModal.style.display = 'block';
}

function closePasswordModal() {
    if (passwordModal) passwordModal.style.display = 'none';
    if (newPasswordInput) newPasswordInput.value = '';
}

// Password form submit handler
async function handlePasswordSubmit(e) {
    e.preventDefault();
    const data = {
        newPassword: newPasswordInput.value
    };
    
    try {
        const response = await fetch('/change_password', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        const res = await response.json();
        alert(res.message);
        if (res.success) {
            closePasswordModal();
        }
    } catch (error) {
        alert('An error occurred. Please try again.');
    }
}

// Delete modal functions
function openDeleteModal() {
    if (deleteModal) deleteModal.style.display = 'block';
    if (deleteConfirmInput) deleteConfirmInput.value = '';
}

function closeDeleteModal() {
    if (deleteModal) deleteModal.style.display = 'none';
}

// Delete account function
async function deleteAccount() {
    const confirmation = deleteConfirmInput ? deleteConfirmInput.value : '';
    
    if (confirmation !== 'DELETE') {
        alert('Please type "DELETE" to confirm account deletion.');
        return;
    }
    
    try {
        const response = await fetch('/delete_account', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ confirmation: confirmation })
        });
        
        const res = await response.json();
        alert(res.message);
        if (res.success) {
            window.location.href = '/';
        }
    } catch (error) {
        alert('An error occurred. Please try again.');
    }
}

// Logout function
function logout() {
    window.location.href = '/logout';
}