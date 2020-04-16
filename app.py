from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
import requests
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_whooshee import Whooshee

app = Flask(__name__)

# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]

app.secret_key = "Dhrumil Patel"

#Database connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/job.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config['DEBUG'] = True
whooshee = Whooshee(app)

# Database model creation started


class User(UserMixin, db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), unique=True, nullable=False)
	name = db.Column(db.String(50))
	mobile = db.Column(db.String(50))
	password = db.Column(db.String(50))

	def get_id(self):
           return (self.user_id)


class Applicant(db.Model):
	applicant_id = db.Column(db.Integer, primary_key=True)
	skills = db.Column(db.Text)
	preferred_location = db.Column(db.Text)
	expected_salary = db.Column(db.String(50))
	projects = db.Column(db.Text)
	achievements = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	user = db.relationship('User')


class Company(db.Model):
	company_id = db.Column(db.Integer, primary_key=True)
	address = db.Column(db.Text)
	description = db.Column(db.Text)
	website = db.Column(db.String(50))
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	user = db.relationship('User')

@whooshee.register_model('jobtype', 'joblevel','position','salary', 'jobpostdate','jobdetails','jobskills', 'joblocation')
class Job(db.Model):
	jobopening_id = db.Column(db.Integer, primary_key=True)
	jobtype = db.Column(db.String(50))
	joblevel = db.Column(db.String(50))
	position = db.Column(db.String(50))
	salary = db.Column(db.String(50))
	jobpostdate = db.Column(db.DateTime, default=datetime.now)
	deadline = db.Column(db.DateTime)
	jobdetails = db.Column(db.Text)
	jobskills = db.Column(db.Text)
	joblocation = db.Column(db.String(50))
	requirements = db.Column(db.Text)
	responsibilities = db.Column(db.Text)
	onlyforemployee = db.Column(db.Boolean, default=False)
	status = db.Column(db.String(50))
	company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'))
	company = db.relationship('Company')

class JobSchema(ma.ModelSchema):
    class Meta:
        model = Job


class Application(db.Model):
	apply_id = db.Column(db.Integer, primary_key=True)
	applydate = db.Column(db.DateTime)
	jobopening_id = db.Column(db.Integer, db.ForeignKey('job.jobopening_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	user = db.relationship('User')


class ApplicationSchema(ma.ModelSchema):
    class Meta:
        model = Application


class Education(db.Model):
	education_id = db.Column(db.Integer, primary_key=True)
	level = db.Column(db.String(50))
	major = db.Column(db.String(50))
	cgpa = db.Column(db.Float)
	year = db.Column(db.Integer)
	instituation = db.Column(db.String(50))
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	user = db.relationship('User')
	


class Experience(db.Model):
	experience_id = db.Column(db.Integer, primary_key=True)
	position = db.Column(db.String(50))
	organization = db.Column(db.String(100))
	duration = db.Column(db.Float)
	key_responsibility = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	user = db.relationship('User')

# Database model creation end


# Admin View
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='Job Portal', template_mode='bootstrap3')
#add admin views
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Applicant, db.session))
admin.add_view(ModelView(Company, db.session))
admin.add_view(ModelView(Job, db.session))
admin.add_view(ModelView(Application, db.session))
admin.add_view(ModelView(Experience, db.session))
admin.add_view(ModelView(Education, db.session))

#Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		attempted_email = request.form['email']
		attempted_password = request.form['password']
		user = User.query.filter_by(email=attempted_email).first()
        #check if such user exists or not
		if user:
			#check password
			if user.password == attempted_password:
				login_user(user)
				if user.email == 'admin@gmail.com':
					return redirect(url_for('admin.index'))
				return redirect(url_for('home'))
		return '<h1>Invalid Email Id or password</h1>'
	return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(email=request.form['email'], name=request.form['name'],
                        mobile=request.form['mobile'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    #remove the session first and then redirect it to login
	logout_user()
	return redirect(url_for('login'))


@app.route('/search')
def search():
	result = Job.query.whooshee_search('Blockchain').all()
	print result
	return render_template('search.html', data=result)

#return all the applied job based on the current logged in user
@app.route('/appliedjobs')
def appliedjobs():
    #Query the database
    appliedjobs = Application.query.filter_by(user_id=current_user.user_id)

    return render_template('appliedjobs.html')

# Home page function
# return all the job postings
@app.route('/home')
@login_required
def home():
    #Query the database
	query = request.args.get('query')
	if query is None:
		jobPostings = Job.query.all()
	else:
		jobPostings = Job.query.whooshee_search(query).all()
	job_schema = JobSchema(many=True)
	data = job_schema.dump(jobPostings).data
	return render_template('home.html', data=data)


@app.route('/details')
def details():
	job_id = request.args.get('job_id')
	jobPosting = Job.query.filter_by(jobopening_id=job_id).first()
	job_schema = JobSchema()
	data = job_schema.dump(jobPosting).data
	return render_template('details.html', data=data)


@app.route('/application')
def application():
    return render_template('application.html')


@app.route('/profile')
def profile():
	return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
