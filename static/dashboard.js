const emailDisplay = document.getElementById('email-display')
const currentUserEl = document.getElementById("current-user")
const inboxBtnEl = document.getElementById("inbox-btn")
const sentBtnEl = document.getElementById("sent-btn")
const draftsBtnEl = document.getElementById("drafts-btn")
const newMailBtnEl = document.getElementById("new-mail-btn")
const logoutBtnEl = document.getElementById("logout-btn")
const settingsBtnEl = document.getElementById("settings-btn")
const closeSettingsBtnEl = document.getElementById("close-settings-btn")
const slideSidebarEl = document.getElementById("slide-sidebar")
const updateDetailsBtnEl = document.getElementById("update-details-btn")
emailDisplay.innerHTML = "";

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



function getEmailHTML(emailData){
    let fromInitials = emailData['From Name'].split(" ")
    fromInitials = fromInitials[0][0] + fromInitials[1][0]
    let dateSent = convertDate(emailData['Date Sent'])
    dateSent = getShortDate(dateSent)
    if(view == "drafts"){
        dateSent = `<span class="red-font">Draft</span>`
    }
    let emailHTML = `
        <div class="email-tile" onclick="loadEmail(${emailData['ID']})">
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

function setDashBoardData(emailArray){
    displayAllEmails(emailArray)
}

function convertDate(dateInMs){
    return new Date(dateInMs)
}

function getShortDate(date){
    return `${(date.getDate()).toString().padStart(2,0)}/${(date.getMonth()).toString().padStart(2,0)}/${date.getFullYear()}`
}

function loadEmail(id){
    console.log(id)
    window.location.replace(`http://127.0.0.1:5000/web-app/${view}/${id}`)
}

let isLoggedIn = getCookie("is_logged_in")
if(isLoggedIn == "False"){
    console.log("Need to login. Redirecting...")
    window.location.replace("http://127.0.0.1:5000/web-app/login")
}
let userEmailAddress = getCookie('email')
//Removes quotes on email
userEmailAddress = userEmailAddress.substring(1,userEmailAddress.length-1)
currentUserEl.textContent = `Welcome: ${userEmailAddress}`
//Get view of page (e.g. inbox, sent, etc.)
let view = window.location.href
indexOfPage = view.lastIndexOf("/")
view = view.substring(indexOfPage+1)
console.log(`View: ${view}`)
let userDetails = null
let inboxEmails = []
let sentEmails = []
fetch(`http://127.0.0.1:5000/exp-api/load_dashboard?email=${userEmailAddress}`)
    .then(response => response.json())
    .then(data => {
        //console.log(data)
        userDetails = data['User Details']
        switch(view) {
            case "inbox":
                setDashBoardData(data['User Emails']['Inbox Emails'])
                break
            case "sent":
                setDashBoardData(data['User Emails']['Sent Emails'])
                break
            default: // drafts
                setDashBoardData(data['User Emails']['Draft Emails'])
                break
        }

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
settingsBtnEl.addEventListener('click', function(){
    slideSidebarEl.classList.remove("slide-sidebar-closed")
    slideSidebarEl.classList.add("slide-sidebar-open")
    console.log("open!")
})
closeSettingsBtnEl.addEventListener('click', function(){
    slideSidebarEl.classList.remove("slide-sidebar-open")
    slideSidebarEl.classList.add("slide-sidebar-closed")
    console.log("closed!")
})
updateDetailsBtnEl.addEventListener('click', function(){
    window.location.replace("http://127.0.0.1:5000/web-app/update-user")
})