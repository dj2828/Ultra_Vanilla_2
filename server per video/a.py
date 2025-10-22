from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, jsonify
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

@app.route('/')
def index():
    return 404

@app.route('/intro')
def intro():
    return send_from_directory('C:/Users/dj28p/Desktop/UV2/', 'Intro Vanilla 2-yt.mp4')

@app.route('/q')
def q():
    return send_from_directory('C:/Users/dj28p/Desktop/UV2/', 'intro quasimodo-yt.mp4')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
