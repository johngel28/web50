document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to the submit button of the compose form
    document.querySelector('#compose-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission behavior
        send_email(); // Call the function to send the email
    });
});

function send_email() {
    // Get values from the compose form
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    // Perform any necessary validation

    // Use fetch to send a POST request to the server to compose and send the email
    fetch('/emails', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body,
        }),
    })
    .then(response => response.json())
    .then(result => {
        console.log(result); // Log the result from the server
        // Optionally, you can handle the result, update UI, etc.
    })
    .catch(error => {
        console.error('Error:', error);
        // Optionally, handle errors
    });
}
