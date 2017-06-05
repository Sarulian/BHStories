from flask import Flask, redirect, render_template, request, url_for, session, escape
from datetime import datetime
import json
import time


app = Flask(__name__)
app.secret_key = 'brotherh00d'

# [
#	[user1.index, 'user1.name'],
# 	[user2.index, 'user2.name']
# ]
users = []
doodles = []
sending_to = {}
getting_from = {}
playing = False
initial_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAfQAAAH0CAYAAADL1t+KAAAgAElEQVR4Xu3dTcx13VkX8ItWtK9SKQXaJnxqCyJG0yZGE03AoIEYHQAGHIMx7cRhawID4wBi2pGzNjE6FiIw0BiIqBA10QlExSi0yodEWqAUqPQNti/mlOe82e/pOWd/rb3W2tf6dULLs89e6/pda6//2fvc97k/L/yHAAECBAgQOL3A552+AgUQIECAAAECIdAtAgIECBAgkEBAoCdoohIIECBAgIBAtwYIECBAgEACAYGeoIlKIECAAAECAt0aIECAAAECCQQEeoImKoEAAQIECAh0a4AAAQIECCQQEOgJmqgEAgQIECAg0K0BAgQIECCQQECgJ2iiEggQIECAgEC3BggQIECAQAIBgZ6giUogQIAAAQIC3RogQIAAAQIJBAR6giYqgQABAgQICHRrgAABAgQIJBAQ6AmaqAQCBAgQICDQrQECBAgQIJBAQKAnaKISCBAgQICAQLcGCBAgQIBAAgGBnqCJSiBAgAABAgLdGiBAgAABAgkEBHqCJiqBAAECBAgIdGuAAAECBAgkEBDoCZqoBAIECBAgINCtAQIECBAgkEBAoCdoohIIECBAgIBAtwYIECBAgEACAYGeoIlKIECAAAECAt0aIECAAAECCQQEeoImKoEAAQIECAh0a4AAAQIECCQQEOgJmqgEAgQIECAg0K0BAgQIECCQQECgJ2iiEggQIECAgEC3BggQIECAQAIBgZ6giUogQIAAAQIC3RogQIAAAQIJBAR6giYqgQABAgQICHRrgAABAgQIJBAQ6AmaqAQCBAgQICDQrQECBAgQIJBAQKAnaKISCBAgQICAQLcGCBAgQIBAAgGBnqCJSiBAgAABAgLdGiBAgAABAgkEBHqCJiqBAAECBAgIdGuAAAECBAgkEBDoCZqoBAIECBAgINCtAQIECBAgkEBAoCdoohIIECBAgIBAtwYIECBAgEACAYGeoIlKIECAAAECAt0aIECAAAECCQQEeoImKoEAAQIECAh0a4AAAQIECCQQEOgJmqgEAgQIECAg0K0BAgQIECCQQECgJ2iiEggQIECAgEC3BggQIECAQAIBgZ6giUogQIAAAQIC3RogQIAAAQIJBAR6giYqgQABAgQICHRrgAABAgQIJBAQ6AmaqAQCBAgQICDQrQECBAgQ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"

round_index = 0
i=0


def order_users():

	for user in users:

		next_index = user[0]+1
		if next_index > len(users)-1:
			next_index = 0

		prev_index = user[0]-1
		if prev_index < 0:
			prev_index = len(users)-1

		sending_to[user[1]] = users[next_index][1]
		getting_from[user[1]] = users[prev_index][1]


def next_doodle():

	from_user = getting_from[session['username']]
	next_image = initial_image
	next_text = 'Draw a picture!'

	for doodle in doodles:
		if doodle.get_name() == from_user and doodle.get_round() == round_index-1:
			next_image = doodle.get_imageURL()
			next_text = doodle.get_text()

	return [next_image, next_text]


class User:

	def __init__(self, name, order, current_page):
		self.name = name
		self.order = order
		self.current_page = current_page

	def set_name(self, name):
		self.name = name

	def go_to_page(self, page):
		self.current_page = page

	def get_name(self):
		return self.name

	def on_page(self):
		return self.current_page


class Doodle:

	def __init__(self, name, order, round, image, text):
		self.game_id = 1
		self.round = round
		self.user_name = name
		self.image = image
		self.text = text
		self.order = order

	def set_name(self, name):
		self.user_name = name

	def set_round(self, index):
		self.round = index

	def set_imageURL(self, image):
		self.image = image

	def set_text(self, text):
		self.text = text

	def get_name(self):
		return self.user_name

	def get_round(self):
		return self.round

	def get_imageURL(self):
		return self.image

	def get_text(self):
		return self.text


@app.route('/login', methods=['GET', 'POST'])
def login():
	global users
	global playing
	global i

	if request.method == 'GET':

		if 'username' in session:
			if playing:
				return redirect(url_for('in_game'))
			else:
				return render_template('lobby.html', users=users, currUser=escape(session['username']))
		else:
			if playing:
				return "Sorry a game is in session already."
			else:
				return render_template('login.html')
		
	if request.method == 'POST':

		session['username'] = request.form['username']
		session['index'] = i

		i+=1

		users.append([session['index'], session['username']])

		return redirect(url_for('lobby'))


@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
	global users
	global users_waiting
	global playing
	global i

	if request.method == 'GET':

		in_users = False
		for user in users:
			if session['username'] in user:
				in_users = True
		if not in_users:
			session['index'] = i
			users.append([session['index'], session['username']])
			i+=1

		if 'username' in session:
			if playing:
				return redirect(url_for('in_game'))
			else:
				in_users = False
				for user in users:
					if session['username'] in user:
						in_users = True
				if not in_users:
					users.append([session['index'], session['username']])

				return render_template('lobby.html', users=users, currUser=escape(session['username']))
		else:
			if playing:
				return "Sorry a game is in session already."
			else:
				return redirect(url_for('login'))

	if request.method == 'POST':

		users_waiting += 1

		if users_waiting >= len(users):

			order_users()
			playing = True

			return redirect(url_for('in_game'))
		else:
			return redirect(url_for('waiting'))


@app.route('/waiting', methods=['GET'])
def waiting():
	global users_waiting

	if users_waiting >= len(users):
		return redirect(url_for('in_game'))
	else:
		return render_template('waiting.html', users=users, currUser=escape(session['username']))

@app.route('/waiting2', methods=['GET'])
def waiting2():
	global users_waiting2
	global users

	print(len(users))
	print(users_waiting2)
	if users_waiting2 >= len(users):
		print("WHYYYYY")
		return redirect(url_for('in_game'))
	else:
		print("Huh?")
		return render_template('waiting2.html')


@app.route('/playing', methods=['GET','POST'])
def in_game():
	global doodles
	global playing
	global users_waiting2
	global round_index

	if request.method == 'GET':

		if 'username' in session:
			if playing:

				return render_template('ingame.html', prevdoodle=next_doodle())

			else:
				return redirect(url_for('lobby'))
		else:
			if playing:
				return "Sorry a game is in session already."
			else:
				return redirect(url_for('login'))

	elif request.method == 'POST':

		users_waiting2 += 1
		image = request.form['next_image']
		text = request.form['next_text']

		#TODO Send [next_image, next_text] to database
		#TODO Receive [prev_image, prev_text] from database
		#Below is a workaround for testing now

		new_doodle = Doodle(session['username'], session['index'], round_index, image, text)

		if len(doodles) < len(users):
			doodles.append(new_doodle)
		else:
			doodles = []

		if users_waiting2 >= len(users):
			round_index += 1
			return redirect(url_for('in_game'))
		else:
			return redirect(url_for('waiting2'))


# Logs out user
@app.route('/clear')
def clear():
	global playing
	global i

	try:
		del users[session['index']]
		i-=1
	except (IndexError, KeyError) as e:
		print("Out of range")

	session.clear()
	playing = False
	print(i)

	return redirect(url_for('login'))


@app.route('/', methods=['GET'])
def start_menu():

	return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=4444, threaded=True)

	# users = [
	# 	[0, 'Ted'],
	# 	[1, 'Scott'],
	# 	[2, 'James'],
	# 	[3, 'Jordan']
	# ]

	# order_users()

	# print(sending_to)
	# print(getting_from)
