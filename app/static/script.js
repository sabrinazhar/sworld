// script.js

document.addEventListener('DOMContentLoaded', function () {
    var fontSizeSelect = document.getElementById('font-size-select');
    var prevFontSizeInput = document.getElementById('prev-font-size');

    // Set the default selected option based on the previous font size
    fontSizeSelect.value = prevFontSizeInput.value;

    // Add tabindex and keyboard event handlers to make sections navigable
    const followingSection = document.getElementById('following-section');
    const followersSection = document.getElementById('followers-section');

    followingSection.setAttribute('tabindex', '0');
    followingSection.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') {
            toggleSection('following');
        }
    });

    followersSection.setAttribute('tabindex', '0');
    followersSection.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') {
            toggleSection('followers');
        }
    });
});

// Function to toggle the display of sections
function toggleSection(section) {
    const sectionElement = document.getElementById(`${section}-section`);
    sectionElement.style.display = sectionElement.style.display === 'none' ? 'block' : 'none';
}

$(document).ready(function() {
    // Handle like/unlike actions
    $(".like-btn").click(function(e) {
        e.preventDefault();

        var post_id = $(this).data("post-id");
        var is_liked = $(this).hasClass("btn-primary");

        // Send AJAX request to like/unlike post
        $.ajax({
            type: "POST",
            url: "/like_post/" + post_id,
            success: function(data) {
                // Update the like button and like count
                if (is_liked) {
                    $(`.like-btn[data-post-id=${post_id}]`).removeClass("btn-primary").addClass("btn-secondary");
                } else {
                    $(`.like-btn[data-post-id=${post_id}]`).removeClass("btn-secondary").addClass("btn-primary");
                }

                // Update the like count
                var likesCount = data.likes_count || 0;
                $(`.like-count[data-post-id=${post_id}]`).text("Likes: " + likesCount);
            },
            error: function(error) {
                console.log("Error:", error);
            }
        });
    });
});


// password toggle for signup
function togglePassword() {
    var passwordInput = document.getElementById("password");
    var confirmInput = document.getElementById("confirm_password");
    
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        confirmInput.type = "text";
    } else {
        passwordInput.type = "password";
        confirmInput.type = "password";
    }
}

// password toggle for login
function togglePasswordLogin() {
    var passwordInput = document.getElementById("password");
    
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

// password toggle for edit password
function toggleNewPassword() {
    var newPasswordInput = document.getElementById("new_password");
    var confirmNewPasswordInput = document.getElementById("confirm_new_password");

    if (newPasswordInput.type === "password") {
        newPasswordInput.type = "text";
        confirmNewPasswordInput.type = "text";
    } else {
        newPasswordInput.type = "password";
        confirmNewPasswordInput.type = "password";
    }
}

// toggle to setFontSize
function setFontSize(size) {
    document.documentElement.className = size;
}

// sesction toggle
function toggleSection(sectionId) {
    var section = document.getElementById(sectionId + '-section');
    if (section.style.display === 'none') {
        section.style.display = 'block';
    } else {
        section.style.display = 'none';
    }
}

// handling like button
function handleLikeButtonClick(button) {
    // Simulate a form submission when the like button is clicked
    button.closest('form').submit();
}
