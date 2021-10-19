from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='template') #create an instance of the Flask class and assign it to the app variable. The first argument is the name of the application. The second argument is the path to the templates folder.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #configure the database URI.

#create an instance of the SQLAlchemy class and assign it to the db variable.
db = SQLAlchemy(app)

#create a class to represent a table in the database.
class Todo_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #create a __repr__ method to print the object's state when it is evaluated. __repr__ is a special method that returns a string representation of the object in a precised content. In this case, it returns the object's content. note that __str__ is a special method that returns a string representation of the object in human-readable form.
    def __repr__(self):
        return '<Task %r>' % self.id

# create a route for the root of the site
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #create a new task
        task_content = request.form['Task_content'] #get the task content from the form identified by the name attribute in the input tag.

        new_task = Todo_List(content=task_content) #create a new task object with the task content and assign it to the "new_task" variable.

        try:
            db.session.add(new_task)  #add the new task to the database
            db.session.commit() #commit the changes to the database
            return redirect('/') #redirect the user to the root of the site
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo_List.query.order_by(Todo_List.date_created).all() #get all the tasks from the database and assign them to the "tasks" variable.

        return render_template('index.html', tasks=tasks) #render the index.html template and pass the tasks variable to it.


#create a route for deleting tasks
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo_List.query.get_or_404(id) #get the task identified by the id parameter and assign it to the "task_to_delete" variable if it exists. If it doesn't exist, return a 404 error.

    try:
        db.session.delete(task_to_delete) #delete the task from the database
        db.session.commit() #commit the changes to the database
        return redirect('/') #redirect the user to the root of the site
    except:
        return 'There was a problem deleting that task'

#create a route for editing tasks
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Todo_List.query.get_or_404(id)
    print(task)
    if request.method == 'POST':
        task.content = request.form['Task_content'] #get the task content from the update form identified by the name attribute in the input tag.

        try:
            db.session.commit() #commit the changes to the database
            return redirect('/') #redirect the user to the root of the site
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('edit.html', task=task)


# run the application on debug mode
if __name__ == "__main__": #if this file is run directly, run the code below it (and not the code above it)
    app.run(debug=True)