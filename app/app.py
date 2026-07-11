from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import os




app = Flask(__name__)

@app.route('/')
def home():
    return "flask is running inside docker"


    
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://root:{os.environ['MYSQL_ROOT_PASSWORD']}"
    f"@{os.environ['DB_HOST']}:3306/{os.environ['MYSQL_DATABASE']}"
)
db.init_app(app)
with app.app_context():
    db.engine.connect()
    print("Database connection successful!")

@app.route("/register",methods=["POST"])
def register():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"message":"User already exists"}),400
    
    hashed_password = generate_password_hash(password)

    new_user = User(username=username, password = hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message":"User registered Successfully"}),201

@app.route("/login",methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message":"Invalid Details"}),401
    
    if check_password_hash(
        user.password, password
    ):
        return jsonify({"message":"Login Successful","user_id":user.id})
    else:
        return jsonify({"message":"Invalid Details"}),401
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)