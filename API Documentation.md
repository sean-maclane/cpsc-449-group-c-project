User Account Microservice

-Create Account
/accounts/create   method = GET, takes no input and returns 200
		        method= POST takes in form input, upon completion. Return 201

Input needed

username
email 
password

Upon successful completion return 201, account created

Possible Errors for above- all return 404 status error if not fulfilled

No fields above are provided     “Error in creating your account”  status=404
 Email address is already taken   “Email already in use”
Username is already taken    “Username already in use”
Email address doesn’t contain @  “Not proper Email”



-Delete Account
/accounts/delete  method = GET, takes no input and returns 200
		        method= POST takes in form input, upon completion. Return 201 
		     
Input needed

username
password
     Upon successful completion return 201, account deleted


Possible errors- all return 404 status error if not fulfilled

None above are provided “ Provide Information” 
No username or password matches in the database  “No account to delete”

-Update email
/accounts/updateEmail 

method=GET, takes no input and returns 200

method=POST takes in username,password, and new email to be updated, upon completion, return 201

Input

username
password
email


Possible errors- all return 404 status error if not fulfilled


None above are provided “Provided information”
No username or password match the database, “No account to update email”
No new email to input  “Enter a new email for account”
Email already in use “Please provide a unique email”


-Increment votes
/votes/upvote

method= GET, takes no input and returns 200

method=POST takes in username and password, upon completion returns 201,
Increments vote counter

Input

username
password


Possible errors- all return 404 status if not fulfilled

None above provided,   “Provide information”
Username and password not found “Create an account




-Decrement votes
/votes/downvote

method= GET, takes no input and returns 200

method=POST takes in username and password, upon completion returns 201,
decrements vote counter

Input

Username
password


Possible errors- all return 404 status if not fulfilled

None above provided,   “Provide information”
Username and password not found “Create an account”




Posts Microservice
	
-Create Post
/posts/create

Method =GET, takes no input and returns 200
Method = POST, takes in form input and returns 201 on completion


Input
title
community
text
username
url


Possible errors- all return 404

No information provided,  “ Please fill out information”
Username doesn't exist to make posts,  “ Please make an account to post”



-Delete Post
/posts/delete

Method=GET, takes no input returns 200 status code
Method=POST, takes in form input, upon completion returns 201


Input

title
username
Password


Possible errors- all return 404 status error if not fulfilled

No information provided “Please provide information
No title provided “Please provide title”
No account info provided “Please provide account info”
Wrong title but correct user info “Provide the correct post by the correct user”
Correct title but wrong user info “Please provide correct use info”


-Retrieve Post
/posts/retrieve

Method=GET, takes no input returns status 200
Method=POST, checks form input upon completion returns status 201


Unique cases for post retrieval

-Input

title
community

CASE 1: No information is provided

Retrieves all posts from database

CASE 2: Title is provided

Retrieves all posts from inputted title

CASE 3: Community is provided

Retrieves all posts from the inputted community

CASE 4: Both title and community are provided

Retrieves all posts from inputted title and community 


Possible Errors - return 404 status code

No posts exist in the database “ Please make a post”
Incorrect title “Please provide a correct title:
Community doesn't exist “Please make a community that exists”
Incorrect title Incorrect community “Check information”
Incorrect title correct community “Check information”
Correct title, incorrect community “Check information” vice versa


