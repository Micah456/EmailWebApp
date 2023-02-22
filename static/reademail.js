//Need to check login first!
const emailPreviewEl = document.getElementById("email-preview")
const currentUserEl = document.getElementById("current-user")
const inboxBtnEl = document.getElementById("inbox-btn")
const sentBtnEl = document.getElementById("sent-btn")
const draftsBtnEl = document.getElementById("drafts-btn")
const newMailBtnEl = document.getElementById("new-mail-btn")
const logoutBtnEl = document.getElementById("logout-btn")
const pageTitle = document.getElementById("page-title")
const h1PageTitleEl = document.getElementById("h1-page-title")

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



function convertDate(dateInMs){
    return new Date(dateInMs)
}

function getLongDate(date){
    return `${(date.getDate()).toString().padStart(2,0)}/${(date.getMonth()).toString().padStart(2,0)}/${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}`
}

function getEmailHTML(emailData){
    if (emailData == null){
        return `<p>Email not found</p>`
    }
    let fromInitials = emailData['From Name'].split(" ")
    fromInitials = fromInitials[0][0] + fromInitials[1][0]
    let dateSent = convertDate(emailData['Date Sent'])
    dateSent = getLongDate(dateSent)
    let emailHTML = `
    <div class="email-header">
        <h2>${emailData['Subject']}</h2>
        <div class="email-subheader">
            <div class="from-user-tile">
                <div id="from-user-icon" class="from-user-icon"><span>${fromInitials}</span>
                </div>
                <p id="from-email"><span class="bolder">${emailData['From Name']}</span><br>{${emailData['From Email']}}</p>
            </div>
            <p id="date-sent">${dateSent}</p>
        </div>
        <p id="to-email">To: ${emailData['To Name']} {${emailData['To Email']}}</p>
    </div>
    <p id="message">${emailData['Message']}</p>
    `
    return emailHTML
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

function setPageTitle(email){
    if(email == null){
        pageTitle.innerHTML = "Email not found - " + userEmailAddress
    }
    else{
        pageTitle.innerHTML = email['Subject'] + " - " + userEmailAddress
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
let pageURL = window.location.href
let i = pageURL.lastIndexOf("/")
let emailID = Number(pageURL.substring(i+1,pageURL.length))
console.log(`Email ID: ${emailID}`)
let view = pageURL.substring(0,i)
let indexOfPage = view.lastIndexOf("/")
view = view.substring(indexOfPage+1)
h1PageTitleEl.textContent = view.substring(0,1).toUpperCase() + view.substring(1)
console.log(`View: ${view}`)
let userDetails = null
fetch(`http://127.0.0.1:5000/exp-api/load_dashboard?email=${userEmailAddress}`)
    .then(response => response.json())
    .then(data => {
        //console.log(data)
        userDetails = data['User Details']
        emailList = []
        switch(view) {
            case "inbox":
                emailArray = data['User Emails']['Inbox Emails']
                break
            case "sent":
                emailArray = data['User Emails']['Sent Emails']
                break
            default: // drafts
                emailArray = data['User Emails']['Draft Emails']
                break
            
        }
        let selectedEmail = getEmailFromList(emailArray, emailID)
        emailPreviewEl.innerHTML = getEmailHTML(selectedEmail)
        setPageTitle(selectedEmail)
    })

//


//Buttons
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