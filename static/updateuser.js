//Remember to verify login
const currentUserEl = document.getElementById("current-user")

const logoutBtnEl = document.getElementById("logout-btn")
const settingsBtnEl = document.getElementById("settings-btn")
const closeSettingsBtnEl = document.getElementById("close-settings-btn")
const slideSidebarEl = document.getElementById("slide-sidebar")
const submitUserDetailsBtnEl = document.getElementById("submit-user-details-btn")
const submitPasswordBtnEl = document.getElementById("submit-password-btn")

const oldPasswordEl = document.getElementById("old-password")
const newPasswordEl = document.getElementById("new-password")
const repeatPasswordEl = document.getElementById("repeat-password")
const firstNameEl = document.getElementById("first-name")
const lastNameEl = document.getElementById("last-name")
const genderSelectorEl = document.getElementById("gender-selector")
const cancelBtnEl = document.getElementById("cancel-btn")

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

let userEmailAddress = getCookie('email')
//Removes quotes on email
userEmailAddress = userEmailAddress.substring(1,userEmailAddress.length-1)
currentUserEl.textContent = `Welcome: ${userEmailAddress}`
//Get user details
let userDetails = null
fetch(expapi + `/load_dashboard?email=${userEmailAddress}`)
    .then(response => response.json())
    .then(data => {
        //console.log(data)
        userDetails = data['User Details']
        updateNamePlaceholders()
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

function prepUserDetailsForm(){
    let fname = firstNameEl.value;
    let lname = lastNameEl.value;
    let gender = genderSelectorEl.value;
    if(fname == ""){
        fname = userDetails['First Name']
    }
    if(lname == ""){
        lname = userDetails['Last Name']
    }
    form = {
        "ID": userDetails['ID'],
        "Email Address": userDetails['Email Address'],
        "First Name": fname,
        "Last Name": lname,
        "Gender": gender,
        "Password": userDetails['Password']
    }
    return form
}
function submitUserDetails(form){
    if(form){
        //submit details only
        console.log("submitting details without new password")
        userDetails = form
        console.log(userDetails)
        sendDetailsToDB("User Details Updated Successfully","details")
    }
    else{
        //submit password only
        console.log("Verifying passwords for submission")
        if(verifyPasswords()){
            console.log("submitting new password only")
            userDetails.Password = newPasswordEl.value
            console.log(userDetails)
            sendDetailsToDB("Password Updated Successfully", "password")
        }
        else{
            alert("Error: passwords incorrectly entered.")
        }
    }
}
function verifyPasswords(){
    let oldPass = oldPasswordEl.value;
    let newPass = newPasswordEl.value;
    let repeatPass = repeatPasswordEl.value;
    
    let oldPassBool = oldPass == userDetails.Password;
    console.log("old password: " + oldPassBool)
    let newPassBool = newPass.length > 4 && newPass != oldPass
    console.log("new password: " + newPassBool)
    let repeatPassBool = newPass == repeatPass
    console.log("repeat password: " + repeatPassBool)
    return oldPassBool && newPassBool && repeatPassBool
}
function updateNamePlaceholders(){
    firstNameEl.setAttribute('placeholder', userDetails['First Name'])
    lastNameEl.setAttribute('placeholder', userDetails['Last Name'])
    genderSelectorEl.value = userDetails['Gender']
}
function clearForm(type){
    if(type == "details"){
        firstNameEl.value = ""
        lastNameEl.value = ""
    }
    else{
        oldPasswordEl.value = ""
        newPasswordEl.value = ""
        repeatPasswordEl.value = ""
    }
}
function sendDetailsToDB(message, type){
    let url = expapi + "/update-user/" + userDetails['ID']
    fetch(url, {
        method: "put",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        //make sure to serialize your JSON body
        body: JSON.stringify(userDetails)
        })
        .then(response => {
            if(response.ok){
                console.log("Success!")
                updateNamePlaceholders()
                alert(message)
                clearForm(type)
            }
            else{
                alert("Error: user details not saved: " + response.statusText)
            }
        })
}

submitUserDetailsBtnEl.addEventListener('click', function(){
    submitUserDetails(prepUserDetailsForm())
})
submitPasswordBtnEl.addEventListener('click', function(){
    submitUserDetails()
    
})
cancelBtnEl.addEventListener('click', function(){
    window.location.replace(webapp + "/inbox")
})
