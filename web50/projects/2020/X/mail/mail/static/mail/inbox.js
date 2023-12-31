document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Remove any existing event listener to avoid multiple bindings
  document.querySelector('#compose-form').removeEventListener('submit', handleComposeSubmit);

  // Add a new event listener to the compose form
  document.querySelector('#compose-form').addEventListener('submit', handleComposeSubmit);
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch emails for the selected mailbox
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Display each email in the mailbox
      emails.forEach(email => display_email(email, mailbox));
    });
}

function display_email(email, mailbox) {
  // Create a new div for the email
  const emailDiv = document.createElement('div');
  emailDiv.className = 'email-box';
  emailDiv.innerHTML = `
    <strong>${email.sender}</strong>: ${email.subject}
    <span class="timestamp">${email.timestamp}</span>
  `;

  // Set background color based on read status
  if (!email.read) {
    emailDiv.style.backgroundColor = 'white';
  } else {
    emailDiv.style.backgroundColor = 'lightgray';
  }

  // Add event listener to view the email details
  emailDiv.addEventListener('click', () => view_email(email.id, mailbox));

  // Append the email div to the emails-view
  document.querySelector('#emails-view').appendChild(emailDiv);
}

function view_email(email_id, mailbox) {
  // Fetch the details of the selected email
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Show the email details in the view
      document.querySelector('#emails-view').innerHTML = `
        <h3>Subject: ${email.subject}</h3>
        <p><strong>From:</strong> ${email.sender}</p>
        <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
        <p><strong>Timestamp:</strong> ${email.timestamp}</p>
        <hr>
        <p>${email.body}</p>
        <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
      `;

      // Add event listener for the reply button
      document.querySelector('#reply').addEventListener('click', () => reply_to_email(email));
      
      // Mark the email as read
      mark_email_as_read(email_id);

      // If the email is in the inbox, add buttons for archiving and unarchiving
      if (mailbox === 'inbox') {
        const archiveButton = document.createElement('button');
        archiveButton.className = 'btn btn-sm btn-outline-primary';
        archiveButton.innerHTML = email.archived ? 'Unarchive' : 'Archive';
        archiveButton.addEventListener('click', () => toggle_archive(email_id, email.archived));
        document.querySelector('#emails-view').appendChild(archiveButton);
      }
    });
}

function reply_to_email(email) {
  // Show the compose view
  compose_email();

  // Pre-fill the composition form
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = email.subject.startsWith('Re: ') ? email.subject : `Re: ${email.subject}`;
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
}

function toggle_archive(email_id, is_archived) {
  // Send a PUT request to toggle the archived status of the email
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !is_archived
    })
  })
  .then(() => load_mailbox('inbox')); // Reload the inbox after archiving or unarchiving
}

function mark_email_as_read(email_id) {
  // Send a PUT request to mark the email as read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });
}

function send_email() {
  console.log('send_email function called'); 	
  // Get form data
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send a POST request to the compose endpoint
  fetch('/emails', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token in the headers
    },
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Email composition failed');
      }
      return response.json();
    })
    .then(data => {
      console.log(data.message); // Log the success message
      // Optionally, load the sent mailbox or perform other actions

      // Show a script alert for a brief message
      alert('Message sent successfully!');
    })
    .catch(error => {
      console.error('Error:', error);
      // Optionally, display an error message to the user
    });
}


// Function to get CSRF token from cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function handleComposeSubmit(event) {
  event.preventDefault(); // Prevent the default form submission
	console.log('send_email function called');
  // Get form data
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send a POST request to the compose endpoint
  fetch('/emails', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token in the headers
    },
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Email composition failed');
      }
      return response.json();
    })
    .then(data => {
      console.log(data.message); // Log the success message
      // Optionally, load the sent mailbox or perform other actions
	  alert('Message sent successfully!');
      load_mailbox('sent'); // Example: Load the sent mailbox after composing
    })
    .catch(error => {
      console.error('Error:', error);
      // Optionally, display an error message to the user
    });
}
