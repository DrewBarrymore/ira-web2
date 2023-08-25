function validateForm(event) {
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var tel = document.getElementById("tel").value;
    var checkboxes = document.querySelectorAll('input[name="sender_type"]:checked');

    // Check for at least one checkbox selected and empty fields
    if (name === "" || email === "" || tel === "" || checkboxes.length === 0) {
        // Display error message for empty fields and unchecked checkboxes
        var errorMessage = "You missed filling the below required fields:\n\n";
        if (name === "") errorMessage += "Field 'Name' is required.\n";
        if (email === "") errorMessage += "Field 'Email' is required.\n";
        if (tel === "") errorMessage += "Field 'Telephone' is required.\n";
        if (checkboxes.length === 0) errorMessage += "Please click on one of the options about who you are.";

        window.alert(errorMessage)
        // event.preventDefault(); // Prevent form submission
        return false;
    }

    // If all fields are filled and at least one checkbox is selected, allow form submission
    window.alert('Thank you for your interest. We will be in touch shortly.');
    return true;
}