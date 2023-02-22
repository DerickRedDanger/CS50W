document.addEventListener('DOMContentLoaded', function() {


//event listener to send the composed email
  document.querySelector('form').onsubmit = () => {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body,
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        // create return to inbox
        load_mailbox('sent');
    });
    
    return false
  };

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
  document.querySelector('#email-view').innerHTML="";

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  

  //Load the emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);

    // show the basic information of the emails
    emails.forEach(mail => {
      const element = document.createElement('div');
      // change background color if it was read
      if (mail.read == true){
        var color = "Gray"
      } else{
        var color = "GhostWhite"
      }

      element.innerHTML = `<p style="background-color:${color}; border-style: solid;">
      From: ${mail.sender}<br>
      Subject:${mail.subject}<br>
      Time: ${mail.timestamp}</p>`;
            //when the email is clicked, open it.
            element.addEventListener('click', function() {
              fetch(`/emails/${mail.id}`)
              .then(response => response.json())
              .then(email => {
              // Print email
              console.log(email);
            
              // showing the full email
              const element = document.createElement('div');
              element.innerHTML = ` <p style="border-style: solid;">From: ${mail.sender}<br> 
              Recipients: ${mail.recipients} <br>
              Subject:${mail.subject}<br>
              Time: ${mail.timestamp}<br>
              Body: ${mail.body}<br>`;
              document.querySelector('#email-view').append(element);
              document.querySelector('#emails-view').style.display = 'none';
              
              // uptade the read to true
              fetch(`/emails/${mail.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true,
                })
                `Count is now ${counter}`
              })
      
              
});

});
// un/archive button
const button = document.createElement('div');

if (mail.archived == true){
  var arch = "Unachive"
  var arc = 0
  } else{
  var arch = "Archive"
  var arc = 1
  }
  
  button.innerHTML = `<button style="background-color:${color}; border-style: solid;">
  <input type="submit" class="btn btn-primary " value="${arch}"> </button>`;
  
  button.addEventListener('click', function() {
    fetch(`/emails/${mail.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: arc,})
    })
    .then (email => {
    console.log(email);
    // after un/archiving load inbox
    load_mailbox('inbox');
    
    
    })
    })
 
  

// reply button
const reply = document.createElement('div');
  reply.innerHTML = `<button style=" background-color:${color}; border-style: solid;">
  <input type="submit" class="btn btn-primary " value="Reply"> </button><br><br>`;
  
  reply.addEventListener('click', function() {
     // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').innerHTML="";

  // Fill out composition fields
  document.querySelector('#compose-recipients').value = `${mail.sender}`;
  if (mail.subject.charAt(0) =="R" && mail.subject.charAt(1) =="e" && mail.subject.charAt(2) ==":" && mail.subject.charAt(3) ==" "){
    document.querySelector('#compose-subject').value = `${mail.subject}`;
  } else{
    document.querySelector('#compose-subject').value = `Re: ${mail.subject}`;
  }
  
  document.querySelector('#compose-body').value = `On ${mail.timestamp} ${mail.sender} wrote: ${mail.body}`;
  })


 
document.querySelector('#emails-view').append(element);
if (mailbox != "sent"){
document.querySelector('#emails-view').append(button);}
document.querySelector('#emails-view').append(reply);


    });

});


  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').innerHTML="";

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}


