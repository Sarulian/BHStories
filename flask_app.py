from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
#import pymysql
from datetime import datetime
import BHStories
import json
import mysql


app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="sarulian",
    password="br0therhood",
    hostname="sarulian.mysql.pythonanywhere-services.com",
    databasename="sarulian$BHStories",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)

class Doodles(db.Model):

    __tablename__ = "doodles"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(32))
    rounds = db.Column(db.Integer)
    text = db.Column(db.String(250))
    drawing = db.Column(db.String(200000))

# [word1,word2,word3,...]
entries = []

# {IP address:[name, time since last input]}
users = {}

# {
# 	'prev_image': 'prev_image',
# 	'prev_text': 'prev_text'
# }
prev_doodle = ['prev_image', 'prev_text']


# Returns only the first word of a series of words
def limit_one_word(user_input):

	return user_input.split()[0]


# Returns the time since the last input was made by this user
def get_time_limit(ip_addr):

	if ip_addr in users:
		now = datetime.now()
		last_input = users[ip_addr][1]
		return now - last_input
	else:
		return 0


# If user name is entered, save with user IP, otherwise lookup. If no name is found return IP address.
def get_name(name_input, ip_addr):

	name = ip_addr

	if name_input != '':
		name = name_input
		users[ip_addr][0] = name
	elif ip_addr in users:
		name = users[ip_addr][0]

	return name


@app.route('/active_story', methods=['GET', 'POST'])
def active_story():

	# Just show page if user accesses for first time/refreshes
	if request.method == 'GET':
		return render_template('active_story.html', entries=entries)
	# Otherwise user has inputted a new word

	# Get user IP address and the word they inputted
	ip_addr = request.environ['REMOTE_ADDR']
	user_input = request.form['new_word']

	# Limit user input to one word
	word = limit_one_word(user_input)

	# If user name is entered, save with user IP, otherwise lookup. If no name is found return IP address.
	name = get_name(request.form['your_name'], ip_addr)

	print(get_time_limit(ip_addr))

	# Save new word and name to display
	entries.append([word, name])

	# Record time of input
	# users[ip_addr][1] = datetime.now()

	# Refresh page
	return redirect(url_for('active_story'))


@app.route('/playing', methods=['GET','POST'])
def in_game():
	global prev_doodle

	if request.method == 'GET':

		print(prev_doodle[1])
		print(len(prev_doodle[0]))

		return render_template('ingame.html', prevdoodle=prev_doodle)

	elif request.method == 'POST':

		next_image = request.form['next_image']
		next_text = request.form['next_text']

		#TODO Send [next_image, next_text] to database
		#TODO Receive [prev_image, prev_text] from database
		#Below is a workaround for testing now

		prev_doodle[0] = next_image
		prev_doodle[1] = next_text

		#return render_template('ingame.html', prevdoodle=prev_doodle)
		return redirect(url_for('in_game'))


@app.route('/', methods=['GET'])
def start_menu():

	return render_template('start_menu.html')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=4444)
