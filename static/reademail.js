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
const editBtnEl = document.getElementById("edit-btn")
const deleteBtnEl = document.getElementById("delete-btn")
const settingsBtnEl = document.getElementById("settings-btn")
const closeSettingsBtnEl = document.getElementById("close-settings-btn")
const slideSidebarEl = document.getElementById("slide-sidebar")
const updateDetailsBtnEl = document.getElementById("update-details-btn")

const webapp = "http://127.0.0.1:5000/web-app"
const expapi = "http://127.0.0.1:5000/exp-api"


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
    return `${(date.getDate()).toString().padStart(2,0)}/${(date.getMonth() + 1).toString().padStart(2,0)}/${date.getFullYear()} ${date.getHours().toString().padStart(2,0)}:${date.getMinutes().toString().padStart(2,0)}`
}

function getEmailHTML(emailData){
    if (emailData == null){
        return `<p>Email not found</p>`
    }
    let fromInitials = emailData['From Name'].split(" ")
    fromInitials = fromInitials[0][0] + fromInitials[1][0]
    let dateSent = convertDate(emailData['Date Sent'])
    dateSent = getLongDate(dateSent)
    if(view == "drafts"){
        dateSent = `<span class="red-font">Draft</span>`
    }
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
fetch(expapi + `/load_dashboard?email=${userEmailAddress}`)
    .then(response => response.json())
    .then(data => {
        userDetails = data['User Details']
        switch(view) {
            case "inbox":
                emailArray = data['User Emails']['Inbox Emails']
                editBtnEl.classList.add("disabled")
                break
            case "sent":
                emailArray = data['User Emails']['Sent Emails']
                editBtnEl.classList.add("disabled")
                break
            default: // drafts
                emailArray = data['User Emails']['Draft Emails']
                editBtnEl.classList.remove("disabled")
                break
            
        }
        let selectedEmail = getEmailFromList(emailArray, emailID)
        emailPreviewEl.innerHTML = getEmailHTML(selectedEmail)
        setPageTitle(selectedEmail)
    })

//


//Buttons
inboxBtnEl.addEventListener('click', function(){
    window.location.replace(webapp + "/inbox")
})
sentBtnEl.addEventListener('click', function(){
    window.location.replace(webapp + "/sent")
})
draftsBtnEl.addEventListener('click', function(){
    window.location.replace(webapp + "/drafts")
})
newMailBtnEl.addEventListener('click', function(){
    window.location.replace(webapp + "/new_mail")
})
logoutBtnEl.addEventListener('click', function(){
    fetch(expapi + "/logout")
        .then(response => {
            if(response.ok){
                console.log(response.json())
            }
            window.location.replace(webapp + "/login")
        })

})
editBtnEl.addEventListener('click', function(){
    if(view == "drafts"){
        window.location.replace(pageURL + "?edit=True")
    }
})
deleteBtnEl.addEventListener('click', function(){
    
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
    window.location.replace(webapp + "/update-user")
})