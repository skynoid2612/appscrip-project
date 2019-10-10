from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
class quiz_db(db.Model):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    id = db.Column(db.Integer, primary_key = True)
    player_name = db.Column(db.String(200), nullable = False)
    q1 = db.Column(db.String(50), nullable = False)
    q2 = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.String(100), default = datetime.now().strftime("%d %B %Y, %I:%M %p")) #datetime.utcnow)

#    def __repr__(self):
#        return  self.id   #'<Task %r>' %

dummy_data = {}
#Main Page
@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        dummy_data['player_name'] = player_name
        return redirect(url_for('question1'))   
    return render_template('index.html')

#second Page: Question 1
@app.route('/question1', methods = ['POST', 'GET'])
def question1():
    if request.method == 'POST':
        q1 = request.form.get('q1')
        dummy_data['q1'] = q1
        return redirect(url_for('question2'))
    return render_template('question1.html')

#Third page: Question2
@app.route('/question2', methods  = ['POST', 'GET'])
def question2():
    if request.method == 'POST':
        q2 = request.form.getlist('q2')
        q2 = ', '.join(q2)
        dummy_data['q2'] = q2
        return redirect(url_for('Summary'))
    return render_template('question2.html')

#Forth page: Summary
@app.route('/Summary', methods = ['POST', 'GET'])
def Summary():
    player_name = str(dummy_data['player_name'])
    q1 = str(dummy_data['q1'])
    q2 = str(dummy_data['q2'])
    #Storing the value in an database
    if request.method == 'POST':        
        if request.form.get('action') == 'Finish': 
            return redirect('/')
        elif request.form.get('action') == 'History':
            return redirect('/history')
    
    new_entry = quiz_db(player_name = player_name, q1 = q1, q2 = q2)
    db.session.add(new_entry)
    db.session.commit()
    return render_template('Summary.html', player_name = player_name, q1 = q1, q2 = q2) 

# fifth page: history
@app.route('/history', methods = ['POST', 'GET'])
def history():
    tasks = quiz_db.query.all()
    if request.method == 'POST': return redirect('/')
    return render_template('history.html', tasks = tasks)



if __name__ == '__main__':
    app.run(debug=True)