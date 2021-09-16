from random import choice
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # # Method 2. Alternatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/random')
def random():
    cafe = db.session.query(Cafe).all()
    random_cafe = choice(cafe)
    return jsonify(cafe=random_cafe.to_dict())
    # return jsonify(cafe={
    #         "name": random_cafe.name,
    #         "map_url": random_cafe.map_url,
    #         "img_url": random_cafe.img_url,
    #         "location": random_cafe.location,
    #         # "seats": random_cafe.seats,
    #         # "has_toilet": random_cafe.has_toilet,
    #         # "has_wifi": random_cafe.has_wifi,
    #         # "has_sockets": random_cafe.has_sockets,
    #         # "can_take_calls": random_cafe.can_take_calls,
    #         # "coffee_price": random_cafe.coffee_price
    #         "amenities": {
    #             "seats": random_cafe.seats,
    #             "has_toilet": random_cafe.has_toilet,
    #             "has_wifi": random_cafe.has_wifi,
    #             "has_sockets": random_cafe.has_sockets,
    #             "can_take_calls": random_cafe.can_take_calls,
    #             "coffee_price": random_cafe.coffee_price,
    #         }
    #     }
    # )

@app.route('/all')
def all_cafes():
    cafes_list = []
    cafes = db.session.query(Cafe).all()
    for cafe in cafes:
        cafes_list.append(cafe.to_dict())
    return jsonify(cafe=cafes_list)


@app.route('/search')
def search():
    query_location = request.args.get('location')
    cafe = Cafe.query.filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


@app.route('/add', methods=["POST"])
def add():
    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('location'),
        seats=request.form.get('seats'),
        has_toilet=int(request.form.get('has_toilet')),
        has_wifi=int(request.form.get('has_wifi')),
        has_sockets=int(request.form.get('has_sockets')),
        can_take_calls=int(request.form.get('can_take_calls')),
        coffee_price=request.form.get('coffee_price')
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={
        "success": "Successfully added the new cafe."
        }
    )

@app.route('/update-price/<int:cafe_id>', methods=["PATCH"])
def update_price(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    if cafe:
        new_price = request.args.get('new_price')
        coffee_to_update = Cafe.query.get(cafe_id)
        coffee_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(success="Successfully updated the price")
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})










# HTTP GET - Read Record


# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
