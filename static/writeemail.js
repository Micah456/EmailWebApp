//MAJOR BUG: need to remove ID in new emails before sent
const currentUserEl = document.getElementById("current-user")
const inboxBtnEl = document.getElementById("inbox-btn")
const sentBtnEl = document.getElementById("sent-btn")
const draftsBtnEl = document.getElementById("drafts-btn")
const newMailBtnEl = document.getElementById("new-mail-btn")
const logoutBtnEl = document.getElementById("logout-btn")
const toEmailInputEl = document.getElementById("to-email-input")
const subjectInputEl = document.getElementById("subject-input")
const messageInputEl = document.getElementById("message-input")
const cancelBtnEl = document.getElementById("cancel-btn")
const saveBtnEl = document.getElementById("save-btn")
const sendBtnEl = document.getElementById("send-btn")
const errorMessageEl = document.getElementById("error-message")

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
function getEmailDetails(isDraft){
    let dateSent = (new Date()).getTime()
    let toEmail = toEmailInputEl.value
    let subject = subjectInputEl.value
    if(toEmail == ""){
        toEmail = `{No Recipient Email}`
    }
    if(subject == ""){
        subject = `{No Subject}`
    }
    let emailData = {
        ID : emailID,
        "Subject": subject,
        "Date Sent": dateSent,
        "Message": messageInputEl.value,
        "From Email": userDetails['Email Address'],
        "From Name": userDetails['First Name'] + " " + userDetails['Last Name'],
        "To Email": toEmail,
        "To Name": "{No Recipient Name}",
        "Draft": isDraft
    }
    return emailData
    //Make sure to handle if email exists or not then fill in name from there. If toemail is {No Recipient Email} - API should ignore this
}

function sendEmail(isDraft){
    console.log(subjectInputEl.value)
    if(messageInputEl.value){
        console.log(getEmailDetails(isDraft))
    }
    else{
        errorMessageEl.style.display = "block"
        console.log("error")
    }
}
function getEmailFromList(emailArray, emailID){
    for(let i = 0; i<emailArray.length; i++){
        let email = emailArray[i]
        if(email['ID'] == emailID){
            return email
        }
    }
    return null
}
function displayDraft(email){
    console.log(email)
    if(email){
        toEmailInputEl.value = email['To Email']
        subjectInputEl.value = email['Subject']
        messageInputEl.value = email['Message']
    }
    else{
        console.log("Email not found")
        emailID = -1
        view = null
    }
    
}

//Check if logged in
let isLoggedIn = getCookie("is_logged_in")
if(isLoggedIn == "False"){
    console.log("Need to login. Redirecting...")
    window.location.replace("http://127.0.0.1:5000/web-app/login")
}

let userEmailAddress = getCookie('email')
//Removes quotes on email
userEmailAddress = userEmailAddress.substring(1,userEmailAddress.length-1)
currentUserEl.textContent = `Welcome: ${userEmailAddress}`
//Get view of page (e.g. inbox, sent, etc.) and Email ID and setting title to view
//Check if draft
let pageURL = window.location.href
let view = ""
let emailID = -1; //Indicates new mail - will be changed if editing draft
if(pageURL.substring(pageURL.length-10) == "?edit=True"){
    //Editing draft
    let i = pageURL.lastIndexOf("/")
    emailID = Number(pageURL.substring(i+1,pageURL.length-10))
    console.log(`Email ID: ${emailID}`)
    view = pageURL.substring(0,i)
    let indexOfPage = view.lastIndexOf("/")
    view = view.substring(indexOfPage+1)
    console.log(`View: ${view}`)
}
else{
    //Writing new mail
    console.log("Writing new email")
}

let userDetails = null
fetch(`http://127.0.0.1:5000/exp-api/load_dashboard?email=${userEmailAddress}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        userDetails = data['User Details']
        if(view){ //draft
            let emailArray = data['User Emails']['Draft Emails']
            let selectedEmail = getEmailFromList(emailArray, emailID)
            displayDraft(selectedEmail)
        }
        
    })


cancelBtnEl.addEventListener('click', function(){
    window.location.replace("http://127.0.0.1:5000/web-app/inbox")
})
saveBtnEl.addEventListener('click', function(){
    sendEmail(true)
})
sendBtnEl.addEventListener('click', function(){
    sendEmail(false)
})


inboxBtnEl.addEventListener('click', function(){
    window.location.replace("http://127.0.0.1:5000/web-app/inbox")
})
sentBtnEl.addEventListener('click', function(){
    window.location.replace("http://127.0.0.1:5000/web-app/sent")
})
draftsBtnEl.addEventListener('click', function(){
    window.location.replace("http://127.0.0.1:5000/web-app/drafts")
})
newMailBtnEl.addEventListener('click', function(){
    window.location.replace("http://127.0.0.1:5000/web-app/new_mail")
})
logoutBtnEl.addEventListener('click', function(){
    fetch("http://127.0.0.1:5000/exp-api/logout")
        .then(response => {
            if(response.ok){
                console.log(response.json())
            }
            window.location.replace("http://127.0.0.1:5000/web-app/login")
        })

})
