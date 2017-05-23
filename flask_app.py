from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)

words = []

@app.route('/', methods=['GET', 'POST'])
def active_story():

	if request.method == 'GET':
		return render_template('active_story.html', words=words)

	words.append(request.form['new_word'])
	return redirect(url_for('active_story'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4444)
    #app.run(debug=True, port=4444)
