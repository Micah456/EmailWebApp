const emailInputEl = document.getElementById("email-input")
const passwordInputEl = document.getElementById("password-input")
const loginBtnEl = document.getElementById("login-btn")
const errorMessageEl = document.getElementById("error-message")

loginBtnEl.addEventListener('click', function(){
    errorMessageEl.style.display = "none"
    email = emailInputEl.value
    password = passwordInputEl.value
    if(email && password){
        //If both email and password given
        login(email, password)
    }
    else{
        //Email and/or password missing
        errorMessageEl.textContent = "Email or password is missing."
        errorMessageEl.style.display = "block"
    }
})


function login(email,password){
    fetch("http://127.0.0.1:5000/exp-api/login", {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        //make sure to serialize your JSON body
        body: JSON.stringify({
            email : email,
            password: password
            })
        })
        .then(response => {
            if(response.ok){
                console.log("Success!")
                window.location.replace("http://127.0.0.1:5000/web-app/inbox")
            }
            else{
                errorMessageEl.textContent = "Email or password is incorrect."
                errorMessageEl.style.display = "block"
            }
        })
}

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

let isLoggedIn = getCookie("is_logged_in")
if(isLoggedIn == "True"){
    console.log("Already logged in: redirecting...")
    window.location.replace("http://127.0.0.1:5000/web-app/dashboard")
}