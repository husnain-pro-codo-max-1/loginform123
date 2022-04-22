from flask import Flask , render_template , redirect , url_for,request
from flask_sqlalchemy import SQLAlchemy
import os

db_path = os.path.join(os.path.dirname(__file__))
db_uri = 'sqlite:///'+os.path.join(db_path,  ' dbfile.sqlite ')


app = Flask(__name__, template_folder='template')

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    city = db.Column(db.String(80))


#db.create_all()

@app.route('/add', methods = ['GET' , 'POST'])
def add():
        if request.method == 'POST':
                 name = request.form.get('username')
                 password = request.form.get('pass')
                 city = request.form.get('city')
                 entry = User(name=name, password=password, city=city)
                 db.session.add(entry)
                 db.session.commit()
        return render_template('signup.html')


@app.errorhandler(404)
def pagenotfound(e):
    return  render_template('eror.html'), 404



@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/view')
def view():
    users = User.query.all()
    return render_template('view.html',  userr=users)



@app.route('/update' , methods=['GET' ,'POST'])
def update():
    if   request.method == 'POST':
        user_id = request.form.get('target_id')
        user_name = request.form.get('target_name')
        user_city = request.form.get('target_city')
        user_found = User.query.filter_by(id=user_id).first()
        user_found.name = user_name
        user_found.city = user_city
        db.session.add(user_found)
        db.session.commit()

    users = User.query.all()
    return render_template('view.html',  userr=users)


# @app.route('/Delete' , methods= ['GET' , 'POST'])
# def delete():
#     if request.method=="POST":
#         user_id = request.form.get('target_id')
#         user_found= User.query.filter_by(id=user_id).first()
#         db.session.delete(user_found)
#         db.session.commit()
#
#     users=User.query.all()
#     return render_template('view.html',  userr=users)




if __name__ == 'main':
    app.run(debug=True)






