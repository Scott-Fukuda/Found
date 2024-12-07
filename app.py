import json
from flask import Flask, request
from db import db, User, Request, Items

# define db filename
db_filename = "found.db"
app = Flask(__name__)

# setup config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# initialize app
db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

    # NOTE: DON'T UNCOMMENT UNLESS YOU WANT TO DELETE TABLES
    # User.__table__.drop(db.engine)
    # Request.__table__.drop(db.engine)
    # Items.__table__.drop(db.engine)

# generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

############# SPECIALIZED ROUTES #############
@app.route("/")
def welcome():
    return 'Hi'


@app.route("/api/user-login/<string:an_email>/")
def user_login(an_email):
    """
    Returns a serialized User based on the email provided. This is acceptable, as each 
    email can only be assigned to one User.
    """
    print("soft",repr(an_email))
    user = User.query.filter_by(email=an_email).first()
    print('sof', user)
    if user is None:
        return failure_response('User not found!')
    return success_response(user.serialize())


@app.route("/api/lost-request/<int:user_id>/", methods=["POST"])
def lost_request(user_id):
    """
    Creates a lost request and returns all of items that match 
    the attributes of the post body provided
    Request has to match at least 2 attributes
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response('User not found!')
    # load body and add new request to database
    body = json.loads(request.data)
    category = body.get("category")
    color = body.get("color")
    new_request = Request(
            item_name = body.get("item_name"),
            category = category,
            color = color,
            description = body.get("description"),
            location_lost = body.get("location_lost"),
            fulfilled = False,
            user_id = user_id
    )
    db.session.add(new_request)
    db.session.commit()

    matched_items = []
    ocolor_list = listify(color)
    items = Items.query.all()
    for item in items:
        matched = 0
        if item.category == category:
            matched += 1 
        icolor_list = listify(item.color)
        for icolor in icolor_list:
            for ocolor in ocolor_list:
                if icolor == ocolor:
                    matched += 1 
        if matched >= 2:
            matched_items.append(item)
    
    ser_items = [i.serialize() for i in matched_items]
    return success_response(ser_items)


def sort_by_color(lst, clrs):
    """
    Returns a list of items in lst that contain the colors in the string clrs

    Precondition: list is a list of serialized items.

    Precondition: clrs is a string of a list of colors in 
    the following format '["color1", "color2", etc.]'
    """
    query_colors_list = listify(clrs)
    new_items_list = []
    for item in lst:
        color = item.get("color")
        color_list = listify(color)
        for clr in color_list:
            if clr in query_colors_list:
                new_items_list.append(item)
                break # if one color matches, it moves onto the next item in the list
    return new_items_list
         

def listify(clr):
    """
    Returns a list version of a color string

    Precondition: clrs is a string of a list of colors in 
    the following format '["color1", "color2", etc.]' or "['color1', 'color2', etc.]"
    """
    list = []
    if clr =='[]':
        return []
    clr = clr[1:-1] # remove brackets
    i = 0
    while i < len(clr):
        if clr[i] == '"':
            start = clr.find('"', i)
            end = clr.find('"', start+1)
            color = clr[start+1:end] # does not include quotes
            list.append(color)
            i = clr.find('"', end+1)
            if i == -1:
                break
        elif clr[i] == "'":
            start = clr.find("'", i)
            end = clr.find("'", start+1)
            color = clr[start+1:end] # does not include quotes
            list.append(color)
            i = clr.find("'", end+1)
            if i == -1:
                break
    return list
        

############# USER ROUTES #############

@app.route("/api/users/")
def get_all_users():
    """
    Get all users from User table
    """
    users = [u.serialize() for u in User.query.all()]
    return success_response(users)


@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Get specific users from User table by user_id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response('User not found!')
    return success_response(user.serialize())


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Create user
    """
    body = json.loads(request.data)
    user = User(
        profile_image = body.get("profile_image"),
        username = body.get("username"),
        bio = body.get("bio"),
        email = body.get("email"),
        phone = body.get("phone"),
        license_approve = body.get("license_approve")
    )
    db.session.add(user)
    db.session.commit()
    return success_response(user.serialize(), 201)


@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete specific users from User table by user_id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response('User not found!')
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())


@app.route("/api/users/<int:user_id>/", methods=["POST"])
def updates_user(user_id):
    """
    Updates specific users from User table by user_id with the attributes in post body. 

    Returns updated user serialized.
    """
    user = User.query.filter_by(id=user_id).first()
    body = json.loads(request.data)
    if user is None:
        return failure_response('User not found!')
    profile_image = body.get("profile_image")
    username = body.get("username")
    bio = body.get("bio")
    email = body.get("email")
    phone = body.get("phone")
    license_approve = body.get("license_approve")
    if not profile_image is None:
        user.profile_image = profile_image
    if not username is None:
        user.username = username 
    if not bio is None:
        user.bio = bio
    if not email is None:
        user.email = email
    if not phone is None:
        user.phone = phone
    if not license_approve is None:
        user.license_approve = license_approve
    db.session.commit()
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/saved/", methods = ["POST"])
def saved_items(user_id):
    """
    Adds item ids user wants to save to user profile.
    Post should give the item id that should be saved.
    """
    body = json.loads(request.data)
    item_id = body.get("item_id")
    user = User.query.filter_by(id = user_id).first() 
    item = Items.query.filter_by(id = item_id).first()
    if user is None or item is None:
        return failure_response("Item/User not found")
    user.added_items.append(item)
    db.session.commit() 
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/saved/")
def get_all_saved_items(user_id):
    """
    Get all saved items from a user
    """
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        return failure_response("User not found") 
    saved = [s.serialize() for s in user.added_items]
    return success_response(saved)

@app.route("/api/users/<int:user_id>/saved/<int:item_id>", methods = ["DELETE"])
def delete_saved_item(user_id,item_id):
    """
    Deletes a saved item from the added_items list based on ID
    """
    user = User.query.filter_by(id=user_id).first()
    item = Items.query.filter_by(id=item_id).first()
    if user is None:
        return failure_response('User not found!')
    if item is None:
        return failure_response('Item not found!')
    if item not in user.added_items:
        return failure_response('Item not saved!')
    user.added_items.remove(item)
    db.session.commit()
    return success_response(item.serialize())

############ ITEMS ROUTES #############

@app.route("/api/items/")
def get_items():
    """
    Gets all found items
    """
    return success_response({"items": [i.serialize() for i in Items.query.all()]})

@app.route("/api/users/<int:user_id>/items/", methods = ["POST"])
def create_item(user_id):
    """
    Creates a post for a found item
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response('User not found!')
    body = json.loads(request.data)
    item_name = body.get("item_name")
    description = body.get("description")
    location_found = body.get("location_found")
    drop_location = body.get("drop_location")
    color = body.get("color")
    category = body.get("category")
    image = body.get("image")
    fulfilled = body.get("fulfilled")
    if None in [item_name, description, location_found, drop_location, color, category, image, fulfilled]:
        return failure_response("Not enough information provided", 400)
    new_item = Items(
        item_name = item_name,
        description = description,
        location_found = location_found,
        drop_location = drop_location,
        color = color,
        category = category,
        image = image,
        fulfilled = fulfilled,
        user_id = user_id
        )
    db.session.add(new_item)
    db.session.commit()
    return success_response(new_item.serialize(), 201)

@app.route("/api/items/<int:item_id>/", methods = ["DELETE"])
def delete_item(item_id):
    """
    Deletes an item
    """
    item = Items.query.filter_by(id = item_id).first()
    if item is None:
        return failure_response("Item not found")
    db.session.delete(item)
    db.session.commit()
    return success_response(item.serialize())

@app.route("/api/items/<int:item_id>/")
def get_item(item_id):
    """
    Gets a specific item
    """
    item = Items.query.filter_by(id = item_id).first()
    if item is None:
        return failure_response("Item not found")
    return success_response(item.serialize())

############# LOST_REQUEST ROUTES #############

@app.route("/api/requests/")
def get_all_requests():
    """
    Get all requests from Request table
    """
    requests = [r.serialize() for r in Request.query.all()]
    return success_response(requests)


@app.route("/api/requests/<int:request_id>/")
def get_request(request_id):
    """
    Get specific requests from Request table by request_id
    """
    request = Request.query.filter_by(id=request_id).first()
    if request is None:
        return failure_response('Request not found!')
    return success_response(request.serialize())


@app.route("/api/users/<int:user_id>/requests/", methods=["POST"])
def create_request(user_id):
    """
    Create request
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response('User not found!')
    body = json.loads(request.data)
    new_request = Request(
        item_name = body.get("item_name"),
        category = body.get("category"),
        color = body.get("color"),
        description = body.get("description"),
        location_lost = body.get("location_lost"),
        fulfilled = False,
        user_id = user_id,
    )
    db.session.add(new_request)
    db.session.commit()
    return success_response(new_request.serialize(), 201)


@app.route("/api/requests/<int:request_id>/", methods=["DELETE"])
def delete_request(request_id):
    """
    Delete specific request from Request table by request_id
    """
    request = Request.query.filter_by(id=request_id).first()
    if request is None:
        return failure_response('Request not found!')
    db.session.delete(request)
    db.session.commit()
    return success_response(request.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
