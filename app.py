from turtle import title
from unicodedata import name
from flask import Flask, redirect, render_template, request, redirect
import _tkinter


from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

from sqlalchemy import null

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///ToDo.db"
db=SQLAlchemy(app)

class ToDo(db.Model):
    SrNo=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(20))
    desc=db.Column(db.String(500))
    dateTime=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(Self) -> str:
        return f"{Self.title}-{Self.desc}"

@app.route('/delete/<int:SrNo>')
def delete(SrNo):
    todo=ToDo.query.filter_by(SrNo=SrNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:SrNo>', methods=['GET',"POST"])
def update(SrNo):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=ToDo.query.filter_by(SrNo=SrNo).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=ToDo.query.filter_by(SrNo=SrNo).first()
    return render_template('update.html', todo=todo)
@app.route("/", methods=['GET',"POST"])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        entry=ToDo(title=title, desc=desc)
        db.session.add(entry)
        db.session.commit()
    alldetails=ToDo.query.all()
    return render_template('index.html', alldet=alldetails)


if __name__=="__main__":
    app.run(debug=False)
