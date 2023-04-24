document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#read-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function compose_reply(emailId) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#read-view').style.display = 'none';

  //get info from previous email
  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
    console.log(emailId);
    console.log(email.subject[0]);
    // Auto-fill composition fields
    document.querySelector('#compose-recipients').value = `${email.sender}`;
    if (email.subject.split(' ',1)[0] == "Re:") {
      document.querySelector('#compose-subject').value = `${email.subject}`;
    }
    else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }  
    document.querySelector('#compose-body').value = `"on ${email.timestamp} ${email.sender} wrote: ${email.body}"` ;

  })

};

function view_email(emailId){
  // display read-view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'block';
  //clear read-view
  document.querySelector('#read-view').innerHTML = '';
  // Get info from email clicked on
  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
  console.log(email);
  if (!email.read){
    // Change read status to read
    fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
      })
    })
  }

  const emailElement = document.createElement('div');
  emailElement.className = "readView";
  emailElement.innerHTML = 
  `<p class="emailIntro"><strong>Sender:</strong> ${email['sender']}
  <br/>
  <strong>Recipients:</strong> ${email['recipients']}
  <br/>
  <strong>Subject:</strong> ${email['subject']}
  <br/>
  <strong>Recieved:</strong> ${email['timestamp']}
  <br/>
  <button class="btn btn-info" id="reply">Reply</button></p>
  <p class="emailBody"> ${email['body']}</p>`;
  document.querySelector('#read-view').append(emailElement);

  // allow reply function
  const buttonElement = document.getElementById("reply");
  buttonElement.addEventListener('click', function() {
    compose_reply(email.id)
  });
  
  // Check archived status
  const btn_archived = document.createElement('button');
  btn_archived.innerHTML = email.archived ? "Unarchive" : "Archive";
  btn_archived.className = email.archived ? "btn btn-success" : "btn btn-danger";
  btn_archived.addEventListener('click', function() {
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !email.archived
      })
    })
    .then(() => {load_mailbox('inbox')});
  });
  document.querySelector('#read-view').append(btn_archived);
})  
};

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // get emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);
    // print each email in a div
    emails.forEach(email =>{ 
        // Create a new div for email
        const element = document.createElement('div');
        element.innerHTML = `Sender: ${email['sender']}
        <br/>
        Subject: ${email['subject']}
        <br/>
        Received: ${email['timestamp']}`;  
        // Determine if read
        element.className = email.read ? 'emailBoxRead': 'emailBoxUnread';
        // Create listener for email click
        element.addEventListener('click', function() {
          view_email(email.id);
        }); 
        // add new element
        document.querySelector('#emails-view').append(element);
    })
  })
}
       
function send_email(event){
  event.preventDefault();
  const recipient = document.querySelector('#compose-recipients').value
  const subject = document.querySelector('#compose-subject').value
  const body =  document.querySelector('#compose-body').value
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: `${recipient}`,
        subject: `${subject}`,
        body: `${body}`
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  })
  };

