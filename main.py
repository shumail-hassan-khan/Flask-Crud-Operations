from flask import Flask
from flask import render_template
from flask import request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False,name='firstName')
    last_name = db.Column(db.String(80), nullable=False, name='lastName')
    age = db.Column(db.Integer, nullable=False,name='age')
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    def _repr_(self):
        return f"{self.sno} - {self.first_name}"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        todo = Todo(first_name=request.form.get("first"),last_name=request.form.get('last'),age=request.form.get('age'))
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html",alltodo=alltodo)


@app.route('/products')
def alltodo():
    alltodo = Todo.query.all()
    print(alltodo)

@app.route('/update/<int:sno>',methods=["GET", "POST"])
def update(sno):
    if request.method=="POST":
        first = request.form['first']
        last = request.form['last']
        age = request.form['age']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.first_name = first
        todo.last_name = last
        todo.age = age
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)