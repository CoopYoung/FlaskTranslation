'''
I want to build a translator between French and English using Flask.
I want to have a saved database with all the words I have added.
   Requirements
    1. Have a menu that says insert english and insert French
    2. Save it all in the sqlite3 database
    3. Have a command to list all previous words
    4. Use Flask for it all 
    5. Eventually, scrape from google translate to translate for me
'''
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from apiflask import HTTPError
from googletrans import Translator, constants
from pprint import pprint
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

translator = Translator()
pprint(constants.LANGUAGES)
# Define the database model
class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(100), nullable=True)
    french = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Translation {self.english} : {self.french}>'

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        english_word = request.form.get('english')
        french_word = request.form.get('french')
        if english_word and french_word:
            new_translation = Translation(english=english_word, french=french_word)
            
        else:
            raise HTTPError(400, message='Must insert both words!')
        
        db.session.add(new_translation)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('insert.html')

@app.route('/list', methods=['GET'])
def list_words():
    translations = Translation.query.all()
    return render_template('list.html', translations=translations)

@app.route('/clear', methods=['POST'])
def clear_translations():
    Translation.query.delete()
    db.session.commit()
    return redirect(url_for('list_words'))
if __name__ == '__main__':
    app.run(debug=True)

