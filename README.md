# EmailWebApp
Email web application prototype to practice frontend, python, and perhaps sql

Design:
database (csv for now) - sysapi - processapi - expapi - html/css/js

*Current task:*
-Load emails into dashboard and set resulting inbox array 
Note: The response from the exp-api should be two arrays: inboxEmails[] and sentEmails[]
Should be split by Pro-api. Consider using similar filtering technique to user but accounting
for whether inbox or sent email. Splitting into 2 arrays should be done at filtering stage

*Remaining tasks:*
-Implement log out (remember to update/remove cookies- see expapi in ewa_server)
-Implement read emails
-Implement write emails
-Implement send emails (including creating drafts)
-Implement update user details
-Implement create new user
-Refactor

*Previous tasks:*
-Load user details to dashboard - DONE
-Build login page and implement login using front end, exp api and sys api - DONE
-Start building sysapi - DONE
-Review storage and format of data from prev project - DONE

*Possible future tasks (stretch goals- please branch):*
-Enable deletion of draft emails - involves trash folder
-Enable deletion of sent emails - involves trash folder - email has TrashFrom and TrashTo boolean attributes
-Connect to database and rework sysapi
-Media queries
-Running apis as separate scripts on different ports

*Notes:*
-Output folder is used for testing purposes only