from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
import BHStories


app = Flask(__name__)

entries = []
users = {}

@app.route('/', methods=['GET', 'POST'])
def active_story():

	if request.method == 'GET':
		return render_template('active_story.html', entries=entries)

	# Get user IP address and the word they inputted
	ip_addr = request.environ['REMOTE_ADDR']
	user_input = request.form['new_word']

	# Limit user input to one word
	word = BHStories.limit_one_word(user_input)

	# If user name is entered store with user IP, otherwise lookup. If no name is found return IP address.
	if request.form['your_name'] != '':
		name = request.form['your_name']
		users[ip_addr] = name
	elif ip_addr in users:
		name = users[ip_addr]
	else:
		name = ip_addr

	entries.append([word, name])

	return redirect(url_for('active_story'))


if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=4444)
    app.run(debug=True, port=4444)
