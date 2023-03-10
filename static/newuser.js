const firstNameEl = document.getElementById("first-name")
const lastNameEl = document.getElementById("last-name")
const emailAddressEl = document.getElementById("email-address")
const genderSelectorEl = document.getElementById("gender-selector")
const passwordEl = document.getElementById("password")
const repeatPasswordEl = document.getElementById("repeat-password")
const submitBtnEl = document.getElementById("submit-btn")
const newUserForm = document.getElementById("new-user-form")

function createUserObject(){
    return {
        "Email Address": emailAddressEl.value,
        "First Name": firstNameEl.value,
        "Last Name": lastNameEl.value,
        "Gender": genderSelectorEl.value,
        "Password": password.value
    }
}

submitBtnEl.addEventListener('click', function(e){
    e.preventDefault();
    console.log(newUserForm.checkValidity())
    if(newUserForm.checkValidity()){
        let userDetails = createUserObject()
        console.log(userDetails)
        fetch("http://127.0.0.1:5000/exp-api/create-user", {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            //make sure to serialize your JSON body
            body: JSON.stringify(userDetails)
        })
             .then(async response => {
                if(response.ok){
                    console.log("Success!")
                    alert("User Created!")
                    window.location.replace("http://127.0.0.1:5000/web-app/login")
                }
                else{
                    alert("Error: user not created: " + response.statusText)
                }
            })
    }
})
repeatPasswordEl.addEventListener('keyup',function(){
    if(passwordEl.value == repeatPasswordEl.value){
        repeatPasswordEl.setCustomValidity("")
    }
    else{
        repeatPasswordEl.setCustomValidity("Passwords do not match.")
    }
})