from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from flask import Flask, render_template, request, redirect
from datetime import datetime

app=Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///base.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
db=SQLAlchemy(app)

class MyTask(db.Model):
    content = db.Column(db.String(40), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    complete = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task{self.id}"

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET","POST"])

def index():
    if request.method == "POST":
        CurrentTask=request.form['content']
        newTask=MyTask(content=CurrentTask)
        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR {e}")
            return f"ERROR {e}"
    else:
        tasks=MyTask.query.order_by(MyTask.created).all()
        return render_template('test.html', tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task=MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR {e}")
        return f"ERROR {e}"

@app.route("/update/<int:id>", methods=["GET","POST"])
def edit(id:int):
    task=MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR {e}")
            return f"ERROR {e}"
    else:
        return render_template("edit.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)