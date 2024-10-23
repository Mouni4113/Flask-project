from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(10), nullable=False)  # Phone number with 10 digits
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

# Home route to display the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        # Create new User object
        new_user = User(name=name, phone=phone, email=email)

        # Add it to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('success'))
        except:
            return "There was an issue adding your data to the database."

    return render_template('index.html')

# Success route after submission
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == "__main__":
    # Create the database before running the app
    with app.app_context():
        db.create_all()
    app.run(debug=True)
