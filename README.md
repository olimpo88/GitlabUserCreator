# GitlabUserCreator
Bulk, create users with CSV
<br>
### Prerequisites
You need python v3.x
<br>
## Quick Start
1. Complete the CSV file, a line per user and each attribute separated by comma. The last parameter is the type of user (admin, user)
2. Login to Gitlab with your Administrator account, in your profile -> Access Token, you must generate a Token for your account. <br>
   <b>Important</b>, in the scopes you must check the options API and SUDO.
4. Run the script to create users: ```python3 create_user.py https://YourURL.com YourToken```
