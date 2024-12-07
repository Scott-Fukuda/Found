# Found
A Cornell Lost and Found App

Link to frontend: https://github.com/chelsea-she/Found-Frontend-App
Link to backend: https://github.com/Scott-Fukuda/Found-Backend-App

![Lost Request, pt 1](https://github.com/user-attachments/assets/86b57444-ec35-46b4-b14a-a2311d30969e)
![Lost Request, pt 2](https://github.com/user-attachments/assets/99e32613-f8df-4a63-bbff-5a22c5e27a1e)
![Found Post, pt 1](https://github.com/user-attachments/assets/e7c3d754-5114-4f89-a93e-a5e06fcd73d9)
![Found Post, pt 2](https://github.com/user-attachments/assets/ef8dcfbe-4497-4aa9-af1f-274c43d1463d)
![Found Post, pt 3](https://github.com/user-attachments/assets/357149e4-c52c-424d-8f6a-8350eae39489)
![Found Post Submission, pt 4](https://github.com/user-attachments/assets/46fb3dd7-9346-4eb3-902e-deea727c2da4)

**Description**
Found is a forum where users can post lost items and other users can create requests to retrieve said items. When a user finds a lost item, they can create a "found post".
Users can navigate to the "found post" tab, where they will be prompted with several questions about the item they've found. This post is then added to a database of posts.
When another user realizes they've lost an item, they can submit a "lost request" containing information about their lost item. This "lost request" is matched up against the
different "found posts" and the "found posts" that match certain specifications are displayed to the user. This acts as a security measure against malicious users attempting
to claim items that do not belong to them. Once a user identifies their lost item, they can claim this item and receive information about where it is located. As additional
security measures, users can only make 3 "lost requests" per week, and each user can only create an account with a Cornell email through Google login.

**How Requirements Are Met**
iOS
We have 9 views that we navigate through. 
AuthView is the sign in page. Users can sign in with either an email or google account through Firebase.
SignupView is for first time users, to finish creating their account including a password, displayName, phone and a bio TextField.
GoogleSignupView is for first time Google users that is the same as SignupView but doesn’t have a password TextField.
ProfileView is the tab that displays the user’s account information and allows them to logout.
FoundView is the tab to post a found lost item.
The FoundPushSuccessPage view will display the successful post of the found item after a user submitted.
LostView is a tab to request a lost item.
The ViewLostQueries view will display the related posts of found items that a user requested as lost.
ReceivedView is a tab to confirm receiving a found item.
Our ViewLostQueries view will be scrollable so the user can scroll through multiple related posts of their lost item.
We deployed our backend API on Google Cloud and integrated networking to access user information, lost requests, received requests, and found posts.

**Backend:**
At least 4 routes (1 must be GET, 1 must be POST, 1 must be DELETE)
GET:
"/api/users/" (gets all users from User table)
"/api/users/<int:user_id>/" (Get specific users from User table by user_id)
"/api/users/<int:user_id>/saved/" (Get all saved items from a user)
"/api/items/" (Gets all found items)
"/api/items/<int:item_id>/" (Gets a specific item)
"/api/requests/" (Get all requests from Request table)
"/api/requests/<int:request_id>/" (Get specific requests from Request table by request_id)

POST:
"/api/lost-request/<int:user_id>/" (creates lost-request and returns item posts matching description
"/api/users/" (create new user)
("/api/users/<int:user_id>/" (Updates specific users from User table by user_id with the attributes in post body. Returns updated user serialized.)
"/api/users/<int:user_id>/saved/" (Adds item ids user wants to save to user profile. Post should give the item id that should be saved.)
"/api/users/<int:user_id>/items/" (Creates a post for a found item)
"/api/users/<int:user_id>/requests/" (Create request)

DELETE:
"/api/users/<int:user_id>/" (Delete specific users from User table by user_id)
"/api/items/<int:item_id>/" (Deletes an item)
"/api/requests/<int:request_id>/" (Delete specific request from Request table by request_id)

At least 2 tables in database with a relationship between them
User: one-to-many relationship with Request 
Many-to-many relationship between Items and User 

API specification 
@app.route("/api/lost-request/<int:user_id>/", methods=["POST"])
Creates a lost request and returns all of items that match 
    the attributes of the post body provided
    Request has to match at least 2 attributes
@app.route("/api/users/")
Get all users from User table
@app.route("/api/users/<int:user_id>/")
Get specific users from User table by user_id
@app.route("/api/user-login/<string:an_email>/")
Get specific user from User table by email
@app.route("/api/users/", methods=["POST"])
Create user
@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
Delete specific users from User table by user_id
@app.route("/api/users/<int:user_id>/", methods=["POST"])
Updates specific users from User table by user_id with the attributes in post body. 
Returns updated user serialized.
@app.route("/api/users/<int:user_id>/saved/", methods = ["POST"])
Adds item ids user wants to save to user profile.
Post should give the item id that should be saved.
@app.route("/api/users/<int:user_id>/saved/")
Get all saved items from a user
@app.route("/api/items/")
Gets all found items
@app.route("/api/users/<int:user_id>/items/", methods = ["POST"])
Creates a post for a found item
@app.route("/api/items/<int:item_id>/", methods = ["DELETE"])
Deletes an item
@app.route("/api/items/<int:item_id>/")
Gets a specific item
@app.route("/api/requests/")
Get all requests from Request table
@app.route("/api/requests/<int:request_id>/")
Get specific requests from Request table by request_id
@app.route("/api/users/<int:user_id>/requests/", methods=["POST"])
Create request
@app.route("/api/requests/<int:request_id>/", methods=["DELETE"])
Delete specific request from Request table by request_id

