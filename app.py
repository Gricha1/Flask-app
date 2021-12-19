import os
import mysql.connector
import json
from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import MySQLdb


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)

class NameForm(FlaskForm):
    name = StringField('Wirte your name', validators=[DataRequired()])
    title = StringField('Wirte your title', validators=[DataRequired()])
    text = TextAreaField('Wirte your text', validators=[DataRequired()])
    submit = SubmitField('Save the story')

class ShowDeleteForm(FlaskForm):
    name1 = StringField('Write name', validators=[DataRequired()])
    title1 = StringField('Write title of story', validators=[DataRequired()])
    show = SubmitField('Show the story')
    delete = SubmitField('Delete the story')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def hello_world(): 
	form = NameForm()
	form1 = ShowDeleteForm()
	message = "sucesfully set up"
	
	mydb = mysql.connector.connect(
	host="mysqldb",
	user="root",
	password="p@ssw0rd1",
	database="stories"
	)
	cursor = mydb.cursor()


	if form.validate_on_submit():
		name = form.name.data
		title = form.title.data
		text = form.text.data

		story_query = ("INSERT INTO new_table "
	       "(name, title, text) "
	       "VALUES (%s, %s, %s)")

		story_info = (name, title, text)

		cursor.execute(story_query, story_info)	

		mydb.commit()
	       
	if form1.validate_on_submit():
		name = form1.name1.data
		title = form1.title1.data

		cursor.execute("SELECT * FROM new_table WHERE (name=%s and title=%s)", (name, title))		
		row_headers=[x[0] for x in cursor.description] #this will extract row headers
		results = cursor.fetchall()
		json_data=[]
		for result in results:
			json_data.append(dict(zip(row_headers,results)))
		
		try:
			text = json_data[0]['name'][2]
			if form1.show.data:
				return render_template('show_story.html', name=name, title=title, text=text)
			else:
				cursor.execute("DELETE FROM new_table WHERE (name=%s and title=%s)", (name, title))				
				mydb.commit()
			
		except:
			return render_template('not_founded.html')

	cache = []
	cursor.execute("SELECT * FROM new_table")
	row_headers=[x[0] for x in cursor.description] #this will extract row headers
	results = cursor.fetchall()
	json_data=[]
	for result in results:
		json_data.append(dict(zip(row_headers,result)))

	for sample in json_data:
		cache.append((sample["name"], sample["title"]))
		
	cursor.close()
	mydb.close()

	return render_template('index.html', form=form, form1=form1, cache=cache, message=message)	

@app.route('/show')
def show_database() :
	mydb = mysql.connector.connect(
	host="mysqldb",
	user="root",
	password="p@ssw0rd1",
	database="stories"
	)
	cursor = mydb.cursor()


	cursor.execute("SELECT * FROM new_table")
	row_headers=[x[0] for x in cursor.description] #this will extract row headers
	results = cursor.fetchall()
	json_data=[]
	for result in results:
		json_data.append(dict(zip(row_headers,result)))

	cursor.close()	
	return json.dumps(json_data)

	
@app.route('/start')
def init_database():
	mydb = mysql.connector.connect(
	host="mysqldb",
	user="root",
	password="p@ssw0rd1"
	)
	cursor = mydb.cursor()

	cursor.execute("DROP DATABASE IF EXISTS stories")
	cursor.execute("CREATE DATABASE stories")
	cursor.close()

	mydb = mysql.connector.connect(
	host="mysqldb",
	user="root",
	password="p@ssw0rd1",
	database="stories"
	)
	cursor = mydb.cursor()

	cursor.execute("DROP TABLE IF EXISTS new_table")
	cursor.execute("CREATE TABLE new_table (name VARCHAR(255), title VARCHAR(255), text VARCHAR(255))")
	
	mydb.commit()
	mydb.close()

	return redirect("/index")

if __name__ == "__main__":
  app.run(host ='0.0.0.0')
