# EmailWebApp
Email web application prototype to practice frontend, python, and perhaps sql

Design:
database (csv for now) - sysapi - processapi - expapi - html/css/js

*Current task:*
-Use env variables for all base urls

*Remaining tasks: *Refactor tasks:*
-Automatically convert emails entered to lowercase
-Create sql db for email and user data
-Connect to databases
-Update html to use more semantic tags - e.g. nav, section, article, aside, etc
-Update writeemail to use forms and use types/required fields etc. to validate input client side
-Improve accessibility of pages

*Previous tasks:*
-Make ewa_expapi_func dry - DONE
-Make ewa_server dry - DONE
-Make ewa_proapi_func dry - DONE
-Make ewa_sysapi_func dry - DONE
-Make css code dry - DONE
-Prevent addition of commas to user details and passwords - DONE
-Implement cancel button on writeemail - DONE
-Implement create new user - DONE
-Create newuser.html + css and initial js - DONE
-Implement update user details - DONE
-Create update user html page - DONE
-Implement Open Settings (as sliding sidebar) - DONE
-Add warning dialogue if closing/going to different page without saving/sending - DONE
-Remove edit button from inbox and sent reademails - DONE
-Add button animation and css clickable curser icon - DONE
-Implement edit button - DONE
-Redirect when sending emails/saving drafts - DONE
-Implement sending/updating emails on js side - DONE
-Fixed bug- login redirects to non-existent dashboard instead of inbox - DONE
-Fixed writeemail.js so that sending new emails does not include ID - DONE
-Fixed update email date sent bug in sys-api - DONE
-Fixed create email bug that sets date to 1970 in new emails in sys-api - DONE
-Implement write emails and edit drafts - DONE
-Implement clicking of emails on dashboard to load reademail.html with appropriate email - DONE
-Implement reademail.html page including rendering emails from rest api requests - DONE
-Implement log out (remember to update/remove cookies- see expapi in ewa_server) - DONE
-Implement sent and draft pages AND get buttons to work so you can switch between the two - DONE
-Change dashboard to inbox page- have login direct user to this pagesent emails display AND get sidebar button to work - DONE
Load emails into dashboard and set resulting inbox array - DONE
-Load user details to dashboard - DONE
-Build login page and implement login using front end, exp api and sys api - DONE
-Start building sysapi - DONE
-Review storage and format of data from prev project - DONE

*Possible future tasks (stretch goals- please branch):*
-Implement print button for emails
-Password rules
-Change date displayed on emails to time or day of the week if within given time period
-Implement forward and replies
-Enable deletion of draft emails - involves trash folder
-Enable deletion of sent emails - involves trash folder - email has TrashFrom and TrashTo boolean attributes
-Connect to database and rework sysapi
-Media queries
-Running apis as separate scripts on different ports

*Notes:*
-Output folder is used for testing purposes only