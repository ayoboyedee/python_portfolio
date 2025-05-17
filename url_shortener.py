from flask import Flask, request, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SECRET_KEY'] = 'your-secret-key'  # Needed for flash messages
db = SQLAlchemy(app)

class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)

def generate_short_code(num_chars=6):
    characters = string.ascii_letters + string.digits
    while True:
        rand_code = ''.join(random.choices(characters, k=num_chars))
        if not URLMap.query.filter_by(short_url=rand_code).first():
            return rand_code

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('original_url')
        custom_code = request.form.get('custom_code').strip()

        if not original_url:
            flash("Please enter the original URL.", "error")
            return redirect(url_for('index'))

        if custom_code:
            if URLMap.query.filter_by(short_url=custom_code).first():
                flash("Custom short URL already taken. Try another.", "error")
                return redirect(url_for('index'))
            short_code = custom_code
        else:
            short_code = generate_short_code()

        url_map = URLMap(original_url=original_url, short_url=short_code)
        db.session.add(url_map)
        db.session.commit()
        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_code>')
def redirect_short_url(short_code):
    url_map = URLMap.query.filter_by(short_url=short_code).first_or_404()
    return redirect(url_map.original_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
