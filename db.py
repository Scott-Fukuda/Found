from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

EST_TIMEZONE = datetime.timezone(offset = -datetime.timedelta(hours=5))

item_user = db.Table(
    "item_user",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("items_id", db.Integer, db.ForeignKey("items.id"))
)

class User(db.Model):
    """
    User model
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    profile_image = db.Column(db.String, nullable=True)
    username = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    license_approve = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.String, nullable=True)
    requests = db.relationship("Request", cascade="delete")
    
    items = db.relationship("Items", cascade="delete",back_populates="owner")
    added_items = db.relationship("Items", secondary = item_user, back_populates="user_items")

    def __init__(self, **kwargs):
        self.profile_image = kwargs.get("profile_image")
        self.username = kwargs.get("username")
        self.bio = kwargs.get("bio")
        self.email = kwargs.get("email")
        self.phone = kwargs.get("phone")
        self.license_approve = kwargs.get("license_approve")
        self.timestamp = datetime.datetime.now(tz=EST_TIMEZONE) 

    def serialize(self):
        return {
            "id": self.id,
            "profile_image": self.profile_image,
            "username": self.username,
            "bio": self.bio,
            "email": self.email,
            "phone": self.phone,
            "license_approve": self.license_approve,
            "timestamp": self.timestamp,
            "requests":[l.serialize() for l in self.requests],
            "items": [i.serialize() for i in self.items],
            "added_items": [a.serialize() for a in self.added_items]
        }


class Request(db.Model):  
    """
    Request model
    """
    __tablename__ = "request"    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    item_name = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    category = db.Column(db.String, nullable=False)   
    color = db.Column(db.String, nullable=False)
    location_lost = db.Column(db.String, nullable=True)
    fulfilled = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    def __init__(self, **kwargs):
        self.item_name = kwargs.get("item_name", "")
        self.timestamp = datetime.datetime.now(tz=EST_TIMEZONE) 
        self.category = kwargs.get("category", "")
        self.color = kwargs.get("color", "")
        self.description = kwargs.get("description", "")
        self.location_lost = kwargs.get("location_lost", "")
        self.fulfilled = kwargs.get("fulfilled", False)
        self.user_id = kwargs.get("user_id", "")


    def serialize(self):
        return {
            "id": self.id,
            "item_name": self.item_name,
            "timestamp": self.timestamp,
            "category": self.category,
            "color": self.color,
            "description": self.description,
            "location_lost": self.location_lost,
            "fulfilled": self.fulfilled,
            "user_id": self.user_id
        }
    

class Items(db.Model):
    """
    Items Model
    """
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    item_name = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = True) 
    category = db.Column(db.String, nullable = False)
    color = db.Column(db.String, nullable = False)
    location_found = db.Column(db.String, nullable = False) 
    drop_location = db.Column(db.String, nullable = False) 
    image = db.Column(db.String, nullable = False) 
    fulfilled = db.Column(db.Boolean, nullable = False) 
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), \
                         nullable=False)
    
    owner = db.relationship("User", back_populates="items")
    user_items = db.relationship("User", secondary = item_user, back_populates = "added_items")

    def __init__(self, **kwargs):
        """
        Initialized Items entry
        """
        self.item_name = kwargs.get("item_name", "")
        self.description = kwargs.get("description","")
        self.timestamp = datetime.datetime.now(tz=EST_TIMEZONE) 
        self.location_found = kwargs.get("location_found", "")
        self.drop_location = kwargs.get("drop_location","")
        self.color = kwargs.get("color","")
        self.category = kwargs.get("category","")
        self.image = kwargs.get("image", "")
        self.fulfilled = kwargs.get("fulfilled",False)
        self.user_id = kwargs.get("user_id")


    def serialize(self):
        """"
        Serializes a item object
        """
        return {
            "id": self.id,
            "item_name": self.item_name,
            "description": self.description,
            "timestamp": self.timestamp,
            "location_found": self.location_found,
            "drop_location": self.drop_location,
            "color": self.color,
            "category": self.category,
            "image": self.image,
            "fulfilled": self.fulfilled,
            "user_id": self.user_id
        } 
