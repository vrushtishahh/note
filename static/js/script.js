$(document).ready(function() {
    // Toggle Sidebar
    $(".toggleSidebar").on("click", function() {
        $("#sidebar").toggleClass("hidden");
    });

    // Handle click event on .database elements
    $(".database").on("click", function() {
        var title = $(this).data('title');

        // Send an AJAX request to the server to get data for the clicked title
        $.ajax({
            url: '/get_note_data',
            type: 'POST',
            data: { 'title': title },
            success: function(data) {
                // Update the content in the 'input' div with the fetched data
                $("#input").html(`
                    <div>Title: ${data.title}</div>
                    <div>Description: ${data.description}</div>
                `);

                // If the sidebar is open, hide it after selecting a database item
                $("#sidebar").addClass("hidden");
            },
            error: function(xhr, status, error) {
                console.error('Error fetching data:');
                console.log('Status:', status);
                console.log('Error:', error);
                console.log('Response Text:', xhr.responseText);
            }
        });
    });

    // Handle click event on .edit-note elements
$(".edit-note").on("click", function() {
    var title = $(this).data('title');

    // Send an AJAX request to the server to get data for the clicked title
    $.ajax({
        url: '/get_note_data',
        type: 'POST',
        data: { 'title': title },
        success: function(data) {
            // Pre-fill the form with existing note data for editing
            $("#title").val(data.title);
            $("#description").val(data.description);

            // If the sidebar is open, hide it after selecting an edit button
            $("#sidebar").addClass("hidden");
        },
        error: function(xhr, status, error) {
            console.error('Error fetching data:');
            console.log('Status:', status);
            console.log('Error:', error);
            console.log('Response Text:', xhr.responseText);
        }
    });
});

// Handle click event on #new-note-button
$(".new-note-button").on("click", function() {
    // Clear the form fields for a new note
    $("#title").val("");
    $("#description").val("");

    // If the sidebar is open, hide it after clicking the new note button
    $("#sidebar").addClass("hidden");
});

/// script.js

// Handle click event on #account-dropdown
$(document).on("click", "#account-dropdown", function() {
    // Toggle the visibility of the dropdown menu
    $("#account-menu").toggleClass("hidden");

    // Fetch user email from the backend
    $.ajax({
        url: '/get_user_email',  // Update the endpoint based on your Flask route
        type: 'GET',
        success: function(data) {
            // Update the user email in the dropdown
            $("#user-email").text(data.email);
        },
        error: function(xhr, status, error) {
            console.error('Error fetching user email:');
            console.log('Status:', status);
            console.log('Error:', error);
            console.log('Response Text:', xhr.responseText);
        }
    });
});

// Close the dropdown if the user clicks outside of it
$(document).on("click", function(event) {
    if (!event.target.matches('#account-dropdown')) {
        var dropdown = $("#account-menu");
        if (dropdown.hasClass('hidden') === false) {
            dropdown.addClass('hidden');
        }
    }
});



  
  





   // Handle click event on .delete-note elements
$(".delete-note").on("click", function() {
    var title = $(this).data('title');
    var noteElement = $(this).closest('.chat');  // Get the parent element of the note for removal

    // Send an AJAX request to the server to delete the note
    $.ajax({
        url: '/delete_note',
        type: 'POST',
        data: { 'title': title },
        success: function(data) {
            // Remove the deleted note from the DOM
            noteElement.remove();
            
            
        },
        error: function(xhr, status, error) {
            console.error('Error deleting note:');
            console.log('Status:', status);
            console.log('Error:', error);
            console.log('Response Text:', xhr.responseText);
        }
    });
});
});
