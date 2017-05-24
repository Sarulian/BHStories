from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
import BHStories


app = Flask(__name__)

entries = []
users = {}

@app.route('/', methods=['GET', 'POST'])
def active_story():

	# Just show page if user accesses for first time/refreshes
	if request.method == 'GET':
		return render_template('active_story.html', entries=entries)
	# Otherwise user has inputted a new word

	# Get user IP address and the word they inputted
	ip_addr = request.environ['REMOTE_ADDR']
	user_input = request.form['new_word']

	# Limit user input to one word
	word = BHStories.limit_one_word(user_input)

	# If user name is entered, save with user IP, otherwise lookup. If no name is found return IP address.
	if request.form['your_name'] != '':
		name = request.form['your_name']
		users[ip_addr] = name
	elif ip_addr in users:
		name = users[ip_addr]
	else:
		name = ip_addr

	# Save new word and name to display
	entries.append([word, name])

	# Refresh page
	return redirect(url_for('active_story'))


if __name__ == '__main__':
    app.run(debug=True, port=4444)
