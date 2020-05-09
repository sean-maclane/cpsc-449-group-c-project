*Note that when it is said a field is not provided, this means that an empty string was sent. It is assumed that the correct key/value pairs are always sent to the API.*

# User Account Microservice

### Create Account
/accounts/create

method= POST takes in form input, upon completion. Return 201

Input needed
1. username
2. email 
3. password

Possible Errors for above- all return 404 status error if not fulfilled
1. No fields above are provided    "Error in creating your account"
2. Email address doesn’t contain @ "Not proper Email"


### Delete Account
/accounts/delete

method= POST takes in form input, upon completion. Return 201 
                     
Input needed
1. username
2. password

Possible errors- all return 404 status error if not fulfilled
1. None above are provided "Provide Information" 
2. No username or password matches in the database  "No account to delete"


### Update email
/accounts/updateEmail 

method=POST takes in username,password, and new email to be updated, upon completion, return 201

Input
1. username
2. password
3. email

Possible errors- all return 404 status error if not fulfilled
1. None above are provided "Provided information"
2. No username or password match the database, "No account to update email"
3. No new email to input  "Enter a new email for account"


### Increment votes
/accounts/upvote

method=POST takes in username and password, upon completion returns 201, Increments vote counter

Input
1. username
2. password

Possible errors- all return 404 status if not fulfilled
1. None above provided,   "Provide information"
2. Username and password not found "Create an account"


### Decrement votes
/accounts/downvote

method=POST takes in username and password, upon completion returns 201, decrements vote counter

Input
1. username
2. password

Possible errors- all return 404 status if not fulfilled
3. None above provided,   "Provide information"
4. Username and password not found "Create an account"


------------------
Posts Microservice
------------------

### Create Post
/posts/create

Method = POST, takes in form input and returns 201 on completion

Input
1. title
2. community
3. text
4. username

Possible errors- all return 404
1. No information provided,  "Please fill out information"


### Delete Post
/posts/delete

Method=POST, takes in form input, upon completion returns 201

Input
1. title
2. username
3. password

Possible errors- all return 404 status error if not fulfilled
1. No username provided "Please provide username"
2. No title provided "Please provide title"
3. No password provided "Please provide password"


### Retrieve Post
/posts/retrieve

Method=POST, checks form input upon completion returns status 201

-Input
1. title
2. community

Possible Errors - return 404 status code
1. Title not provided "Provide a title"
2. Community not provided "Provide a community"
3. Title and community not provided "Provide a title and community"



------------------
Message Microservice
------------------

### Send Message
/message/send

method=GET, POST takes in form input, upon completion. Return 201

-Input needed:

  1) userfrom
  2) userto
  3) messagecontent
  4) flag

Possible Errors for above- all return 404 status error if not fulfilled

  1) No user from provided
  2) No user to provided
  3) No message provided

### Delete Message
/message/delete
method=GET, POST,DELETE takes in form input, upon completion. Return 201

-Input needed:

  1) userfrom
  2) messagecontent

=Possible Errors for above- all return 404 status error if not fulfilled
  1) User not provided
  2) Message not provided

### Flag Message
/message/flag

method=GET, POST takes in form input, upon completion. Return 201


-Input needed:
  1) messagecontent
  2) flag
  
  Possible Errors for above- all return 404 status error if not fulfilled

  1) Message can’t be found


------------------
Voting Microservice
------------------
TODO