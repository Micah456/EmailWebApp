const emailInputEl = document.getElementById("email-input")
const passwordInputEl = document.getElementById("password-input")
const loginBtnEl = document.getElementById("login-btn")
const errorMessageEl = document.getElementById("error-message")
const webapp = "http://127.0.0.1:5000/web-app"
const expapi = "http://127.0.0.1:5000/exp-api"

function loginBtnEvent(){
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
}

loginBtnEl.addEventListener('click', loginBtnEvent)

passwordInputEl.addEventListener('keyup', function(){
    if (event.keyCode === 13){
        loginBtnEvent()
    }
})

emailInputEl.addEventListener('keyup', function(){
    if (event.keyCode === 13){
        loginBtnEvent()
    }
})

function login(email,password){
    document.body.style.cursor = 'wait'
    fetch(expapi + "/login", {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        //make sure to serialize your JSON body
        body: JSON.stringify({
            email : email.toLowerCase(),
            password: password
            })
        })
        .then(response => {
            if(response.ok){
                console.log("Success!")
                window.location.replace(webapp + "/inbox")
            }
            else{
                errorMessageEl.textContent = "Email or password is incorrect."
                errorMessageEl.style.display = "block"
                document.body.style.cursor = 'default'
            }
        })
}