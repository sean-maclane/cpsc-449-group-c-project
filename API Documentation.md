User Account Microservice


-Create Account
/accounts/create   method = GET, takes no input and returns 200
                        method= POST takes in form input, upon completion. Return 201


Input needed


1. username
2. email 
3. password


Upon successful completion return 201, account created


Possible Errors for above- all return 404 status error if not fulfilled


1. No fields above are provided     “Error in creating your account”  status=404
2.  Email address is already taken   “Email already in use”
3. Username is already taken    “Username already in use”
4. Email address doesn’t contain @  “Not proper Email”






-Delete Account
/accounts/delete  method = GET, takes no input and returns 200
                        method= POST takes in form input, upon completion. Return 201 
                     
Input needed


1. username
2. password
     Upon successful completion return 201, account deleted




Possible errors- all return 404 status error if not fulfilled


1. None above are provided “ Provide Information” 
2. No username or password matches in the database  “No account to delete”


-Update email
/accounts/updateEmail 


method=GET, takes no input and returns 200


method=POST takes in username,password, and new email to be updated, upon completion, return 201


Input


1. username
2. password
3. email




Possible errors- all return 404 status error if not fulfilled

1. None above are provided “Provided information”
2. No username or password match the database, “No account to update email”
3. No new email to input  “Enter a new email for account”
4. Email already in use “Please provide a unique email”




-Increment votes
/votes/upvote


method= GET, takes no input and returns 200


method=POST takes in username and password, upon completion returns 201,
Increments vote counter


Input


1. username
2. password




Possible errors- all return 404 status if not fulfilled


1. None above provided,   “Provide information”
2. Username and password not found “Create an account








-Decrement votes
/votes/downvote


method= GET, takes no input and returns 200


method=POST takes in username and password, upon completion returns 201,
decrements vote counter


Input


3. Username
4. password




Possible errors- all return 404 status if not fulfilled


3. None above provided,   “Provide information”
4. Username and password not found “Create an account”








Posts Microservice
        
-Create Post
/posts/create


Method =GET, takes no input and returns 200
Method = POST, takes in form input and returns 201 on completion




Input
1. title
2. community
3. text
4. username
5. url




Possible errors- all return 404


1. No information provided,  “ Please fill out information”
2. Username doesn't exist to make posts,  “ Please make an account to post”






-Delete Post
/posts/delete


Method=GET, takes no input returns 200 status code
Method=POST, takes in form input, upon completion returns 201




Input


1. title
2. username
3. Password




Possible errors- all return 404 status error if not fulfilled


1. No information provided “Please provide information
2. No title provided “Please provide title”
3. No account info provided “Please provide account info”
4. Wrong title but correct user info “Provide the correct post by the correct user”
5. Correct title but wrong user info “Please provide correct use info”




-Retrieve Post
/posts/retrieve


Method=GET, takes no input returns status 200
Method=POST, checks form input upon completion returns status 201




Unique cases for post retrieval


-Input


1. title
2. community


CASE 1: No information is provided


Retrieves all posts from database


CASE 2: Title is provided


Retrieves all posts from inputted title


CASE 3: Community is provided


Retrieves all posts from the inputted community


CASE 4: Both title and community are provided


Retrieves all posts from inputted title and community 




Possible Errors - return 404 status code


1. No posts exist in the database “ Please make a post”
2. Incorrect title “Please provide a correct title:
3. Community doesn't exist “Please make a community that exists”
4. Incorrect title Incorrect community “Check information”
5. Incorrect title correct community “Check information”
6. Correct title, incorrect community “Check information” vice versa