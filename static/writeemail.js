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
const settingsBtnEl = document.getElementById("settings-btn")
const closeSettingsBtnEl = document.getElementById("close-settings-btn")
const slideSidebarEl = document.getElementById("slide-sidebar")
const updateDetailsBtnEl = document.getElementById("update-details-btn")


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
    else{
        toEmail = toEmail.toLowerCase()
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
    if(emailData.ID == -1){//new emails should not be sent with an ID
        delete emailData.ID
    }
    return emailData
    //Make sure to handle if email exists or not then fill in name from there. If toemail is {No Recipient Email} - API should ignore this
}

function sendEmail(isDraft){
    console.log(subjectInputEl.value)
    if(messageInputEl.value){
        let emailToSend = getEmailDetails(isDraft)
        console.log(emailToSend)
        let mymethod = ""
        if(view){//If updating draft (view only set if email is draft)
            mymethod = "put"
        }
        else{//Sending NEW mail
            mymethod = "post"
        }
        fetch("http://127.0.0.1:5000/exp-api/save_email", {
        method: mymethod,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        //make sure to serialize your JSON body
        body: JSON.stringify(emailToSend)
        })
        .then(response => {
            if(response.ok){
                console.log("Success!")
                if(view){
                    window.location.replace("http://127.0.0.1:5000/web-app/" + view)
                }
                else{
                    window.location.replace("http://127.0.0.1:5000/web-app/inbox")
                }
                
            }
            else{
                alert("Error: email not sent/saved: " + response.statusText)
            }
        })
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
    if(view){
        confirmExit("http://127.0.0.1:5000/web-app/" + view + "/" + emailID)
    }
    else{
        confirmExit("http://127.0.0.1:5000/web-app/inbox")
    }
})
saveBtnEl.addEventListener('click', function(){
    sendEmail(true)
})
sendBtnEl.addEventListener('click', function(){
    sendEmail(false)
})

function confirmLogout(func){
    console.log("Email empty: " + isEmptyEmail())
    if(isEmptyEmail()){
        func()
    }
    else{
        let cont = confirm("Do you want to leave? (Your changes will not be saved)");
        if (cont) {
            func()
        } else {
            console.log("Not leaving page")
        } 
    }
    
}

function confirmExit(targetUrl) {
    console.log("Email empty: " + isEmptyEmail())
    if(isEmptyEmail()){
        window.location.replace(targetUrl)
    }
    else{
        let cont = confirm("Do you want to leave? (Your changes will not be saved)");
        if (cont) {
            console.log("Leaving page!")
            window.location.replace(targetUrl)
        } else {
            console.log("Not leaving page")
        }
    }
    
}
function isEmptyEmail(){
    if(toEmailInputEl.value || subjectInputEl.value || messageInputEl.value) return false
    else return true
}

inboxBtnEl.addEventListener('click', function(){
    confirmExit("http://127.0.0.1:5000/web-app/inbox")
})
sentBtnEl.addEventListener('click', function(){
    confirmExit("http://127.0.0.1:5000/web-app/sent")
})
draftsBtnEl.addEventListener('click', function(){
    confirmExit("http://127.0.0.1:5000/web-app/drafts")
})
newMailBtnEl.addEventListener('click', function(){
    confirmExit("http://127.0.0.1:5000/web-app/new_mail")
})
logoutBtnEl.addEventListener('click', function(){
    confirmLogout(function(){
        fetch("http://127.0.0.1:5000/exp-api/logout")
        .then(response => {
            if(response.ok){
                console.log(response.json())
            }
            window.location.replace("http://127.0.0.1:5000/web-app/login")
        })
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