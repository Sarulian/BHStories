from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
import BHStories


app = Flask(__name__)

# [word1,word2,word3,...]
entries = []

# {IP address:[name, time since last input]}
users = {}


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


@app.route('/paint', methods=['GET', 'POST'])
def paintapp():
    if request.method == 'GET':
        return render_template("base.html")
    if request.method == 'POST':
        filename = request.form['save_fname']
        data = request.form['save_cdata']
        canvas_image = request.form['save_image']
    #     conn = psycopg2.connect(database="paintmyown", user = "nidhin")
    #     cur = conn.cursor()
    #     cur.execute("INSERT INTO files (name, data, canvas_image) VALUES (%s, %s, %s)", [filename, data, canvas_image])
    #     conn.commit()
    #     conn.close()
    #     return redirect(url_for('save'))  


@app.route('/', methods=['GET'])
def start_menu():

	return render_template('start_menu.html')


if __name__ == '__main__':
    app.run(debug=True, port=4444)
