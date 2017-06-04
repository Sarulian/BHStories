from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
import json


app = Flask(__name__)

# [
#	[user1.index, 'user1.name'],
# 	[user2.index, 'user2.name']
# ]
users = []

i=0

# {
# 	'prev_image': 'prev_image',
# 	'prev_text': 'prev_text'
# }
prev_doodle = ['prev_image', 'prev_text']


class User:

	def __init__(self, name, index):
		self.name = name
		self.index = index

	def set_name(self, name):
		self.name = name

	def set_index(self, index):
		self.index = index

	def get_name(self):
		return self.name

	def get_index(self):
		return self.index


@app.route('/login', methods=['GET', 'POST'])
def login():
	global users
	global i

	if request.method == 'GET':

		return render_template('login.html')

	elif request.method == 'POST':

		new_user_name = request.form['username']

		new_user = User(new_user_name, i)
		i+=1

		users.append([new_user.get_index(), new_user.get_name()])

		return redirect(url_for('lobby'))


@app.route('/lobby', methods=['GET','POST'])
def lobby():
	global users

	if request.method == 'GET':

		return render_template('lobby.html', users=users)

	if request.method == 'POST':

		return redirect(url_for('in_game'))


@app.route('/playing', methods=['GET','POST'])
def in_game():
	global prev_doodle

	if request.method == 'GET':

		#print(prev_doodle[1])
		#print(len(prev_doodle[0]))

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

	return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=4444)
