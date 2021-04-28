from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

app.config['SECRET_KEY'] = ''
# db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Navaneeth@2230'
app.config['MYSQL_DB'] = 'blog'

mysql = MySQL(app)


posts = [
    {
    'author' : 'Navaneeth Mv',
    'title' : 'Blog Post 1',
    'content' : 'First Post Content',
    'date_posted' : '28-02-2021'
    },

    {
    'author' : 'Tommy Shelby',
    'title' : 'Blog Post 2',
    'content' : 'Second Post Content',
    'date_posted' : '30-03-2021'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html',title = 'About')


@app.route('/register', methods = ['POST', 'GET'])
def register():
    form = RegistrationForm()
    cur = mysql.connection.cursor()
    if form.validate_on_submit():

        cur.execute("insert into users values('2', %s, %s, '1.jpeg', %s)",(form.username.data, form.email.data, form.password.data))
        mysql.connection.commit()
        cur.close()

        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    cur = mysql.connection.cursor()
    if form.validate_on_submit():
        password = cur.execute("select password from users where email = %s",(form.email.data))
        priint(password)
        if form.password.data == password:
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)


if __name__ == "__main__":
    app.run(debug=True)

