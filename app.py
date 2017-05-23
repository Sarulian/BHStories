from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def active_story():
    return render_template('active_story.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4444)
