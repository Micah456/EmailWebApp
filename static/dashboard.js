const emailDisplay = document.getElementById('email-display')
const currentUserEl = document.getElementById("current-user")
const getCookie = (cookieKey) => {
  let cookieName = `${cookieKey}=`;

  let cookieArray = document.cookie.split(';');

  for (let cookie of cookieArray) {

    while (cookie.charAt(0) == ' ') {
          cookie = cookie.substring(1, cookie.length);
      }

    if (cookie.indexOf(cookieName) == 0) {
          return cookie.substring(cookieName.length, cookie.length);
      }
  }
}
let exampleEmail = {
        "ID": 1,
        "Subject": "RE: First Email",
        "Date Sent": "20/02/2023 23:21:52",
        "Message": "Hey sis!",
        "From Email": "duanevaughn@hotmail.com",
        "From Name": "Duane Vaughn",
        "To Email": "marleevaughn@outlook.com",
        "To Name": "Marlee Vaughn",
        "Draft": false
}
emailDisplay.innerHTML = "";
let examples = [exampleEmail, exampleEmail]
function getEmailHTML(emailData){
    let fromInitials = emailData['From Name'].split(" ")
    fromInitials = fromInitials[0][0] + fromInitials[1][0]
    let dateSent = convertDate(emailData['Date Sent'])
    dateSent = getShortDate(dateSent)
    let emailHTML = `
        <div class="email-tile">
            <div class="email-sub-tile">
                <div id="from-user-icon" class="from-user-icon"><span>${fromInitials}</span>
                </div>
                <div class="email-details">
                    <h3 .class='from-name'>${emailData['From Name']}</h3>
                    <h4 .class='subject'>${emailData['Subject']}</h4>
                    <p class="email-date">${dateSent}</p>
                </div>
            </div>
            <p class='message-summary'>${emailData['Message']}</p>
        </div>
    `
    return emailHTML
}
function displayAllEmails(emailArray){
    let emailDisplayHTML = ""
    for(let i = 0; i<emailArray.length; i++){
        emailDisplayHTML += getEmailHTML(emailArray[i])
    }
    emailDisplay.innerHTML = emailDisplayHTML
}

let userEmailAddress = getCookie('email')
userEmailAddress = userEmailAddress.substring(1,userEmailAddress.length-1)
let userDetails = null
let inboxEmails = []
let sentEmails = []
fetch(`http://127.0.0.1:5000/exp-api/load_dashboard?email=${userEmailAddress}`)
    .then(response => response.json())
    .then(data => {
        //console.log(data)
        userDetails = data['User Details']
        inboxEmails = data['User Emails']['Inbox Emails']
        sentEmails = data['User Emails']['Sent Emails']
        setDashBoardData()
    })
currentUserEl.textContent = `Welcome: ${userEmailAddress}`
//Add code to exp api etc to extract emails- I want it to return an object containing two objects
//1st points to array of inbox emails(to user)
//2nd points to array of sent emails (from user)
//Add INBOX emails to inboxEmails
//Then run displayAllEmails for the INBOX emails for this page

//displayAllEmails(inboxEmails) //Change to inboxEmails once above api feature created
function setDashBoardData(){
    displayAllEmails(inboxEmails)
}

function convertDate(dateInMs){
    return new Date(dateInMs)
}

function getShortDate(date){
    return `${(date.getDate()).toString().padStart(2,0)}/${(date.getMonth()).toString().padStart(2,0)}/${date.getFullYear()}`
}