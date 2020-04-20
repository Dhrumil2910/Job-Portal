from flask import Flask, render_template, url_for, redirect, flash, request, jsonify, send_file
import requests
from datetime import datetime, date
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_whooshee import Whooshee
from io import BytesIO, StringIO

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

@whooshee.register_model('searchable_tags', 'email', 'name')
class User(UserMixin, db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), unique=True, nullable=False)
	name = db.Column(db.String(50))
	mobile = db.Column(db.String(50))
	password = db.Column(db.String(50))
	resume = db.Column(db.LargeBinary)
	searchable_tags = db.Column(db.Text)

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
	application_status = db.Column(db.String(50))
	meeting_schedule = db.Column(db.String(50))
	jobopening_id = db.Column(db.Integer, db.ForeignKey('job.jobopening_id'))
	job = db.relationship('Job')
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
				elif user.email == 'poojan@gmail.com':
					return redirect(url_for('rechome'))
				return redirect(url_for('home'))
		return '<h1>Invalid Email Id or password</h1>'
	return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(email=request.form['email'], name=request.form['name'],
                        mobile=request.form['mobile'], password=request.form['password'], resume=request.files['resume'].read(), searchable_tags=request.form['tags'])
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
	return render_template('search.html', data=result)


@app.route('/replytomessage')
def replytomessage():
	apply_id = request.args.get('appId')
	#get the application
	application = Application.query.filter_by(apply_id=apply_id).first()
	application.meeting_schedule = application.meeting_schedule + "\nApplicant: Ok!"
	db.session.commit()
	return redirect(url_for('appliedjobs'))

#return all the applied job based on the current logged in user
@app.route('/appliedjobs')
def appliedjobs():
    #Query the database
	jobPostings = []
	appliedjobs = Application.query.filter_by(user_id=current_user.user_id).all()
	application_schema = ApplicationSchema(many=True)
	applications = application_schema.dump(appliedjobs).data
	for application in appliedjobs:
		JobPosting = Job.query.filter_by(jobopening_id=application.jobopening_id).first()
		jobPostings.append(JobPosting)
	job_schema = JobSchema(many=True)
	data = job_schema.dump(jobPostings).data
	return render_template('appliedjobs.html', data=data, applications=applications)

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

@app.route('/rechome')
@login_required
def rechome():
	#Query the database for all the jobs
	query = request.args.get('query')
	if query is None:
		jobPostings = Job.query.all()
	else:
		jobPostings = Job.query.whooshee_search(query).all()
	job_schema = JobSchema(many=True)
	data = job_schema.dump(jobPostings).data
	return render_template('rechome.html', data=data)

@app.route('/recdeletejob')
@login_required
def recDeleteJob():
	#get the job id to be deleted
	deletejobid = request.args.get('deletejobid')
	if deletejobid is not None:
		#find the job with this Id
		jobPosting = Job.query.filter_by(jobopening_id=deletejobid).delete()
		db.session.commit()
	#redirect it to the same page after delete
	return redirect(url_for('rechome'))

@app.route('/downloadresume')
def downloadresume():
	#get the user id from the requests
	user_id = request.args.get('userId')
	#Find the user in the db
	UserResume = User.query.filter_by(name=user_id).first()
	return send_file(BytesIO(UserResume.resume), attachment_filename='resume.pdf', as_attachment=True)

# @app.route('/seeresume')
# def seeresume():
# 	#get the user id from the requests
# 	user_id = request.args.get('userId')
# 	#Find the user in the db
# 	UserResume = User.query.filter_by(user_id=user_id).first()
# 	sio = StringIO()
# 	# f = open(send_file(BytesIO(UserResume.resume), attachment_filename='resume.pdf', as_attachment=True), "rb")
# 	# imag = f.read()
# 	# print(imag)
# 	# f.close()
# 	# sio.write(BytesIO(UserResume.resume))
# 	# sio.seek(0)
# 	return UserResume.resume


@app.route('/recdetails')
@login_required
def recdetails():
	#Query the job from the database from the job Id
	job_id = request.args.get('job_id')
	jobPosting = Job.query.filter_by(jobopening_id=job_id).first()
	job_schema = JobSchema()
	dataJob = job_schema.dump(jobPosting).data
	#Query the Applicants who applied for this job
	Applications = Application.query.filter_by(jobopening_id=job_id).all()
	application_schema = ApplicationSchema(many=True)
	dataApplications = application_schema.dump(Applications).data
	data = {
		'dataJob': dataJob,
		'dataApplications': dataApplications
	}
	for i in range(len(data['dataApplications'])):
		userId = data['dataApplications'][i]['user']
		#get the user from the database
		UserAp = User.query.filter_by(user_id=userId).first()
		#just change the name in the list
		data['dataApplications'][i]['user'] = {
			'name': UserAp.name,
			'searchable_tags': UserAp.searchable_tags
		}
	if request.args.get('query') is None:
		return render_template('recdetails.html', data=data)
	return render_template('recdetails.html', data=data, query=request.args.get('query'))

@app.route('/acceptApp')
def acceptApp():
	#get the application id from the requests
	application_id = request.args.get('appId')
	#Find the application in the db
	ApplicationAc = Application.query.filter_by(apply_id=application_id).first()
	ApplicationAc.application_status = "Accepted"
	db.session.commit()
	return redirect(url_for('recdetails', job_id=ApplicationAc.jobopening_id))


@app.route('/applyforjob')
def applyforjob():
	#get the job id
	job= Job.query.filter_by(jobopening_id=request.args.get('jobid')).first()

	#make the application
	user = User.query.filter_by(user_id=current_user.user_id).first()
	applydate = date.today()
	newApplication = Application(applydate=applydate, user=user, job=job, application_status="Applied", meeting_schedule=None)
	db.session.add(newApplication)
	db.session.commit()
	return redirect(url_for('appliedjobs'))

@app.route('/schedule')
def schedule():
	#get the application id from the requests
	application_id = request.args.get('appId')
	#Find the application in the db
	ApplicationAc = Application.query.filter_by(apply_id=application_id).first()
	ApplicationAc.meeting_schedule = "The meeting is schedule after 10 days from now. Please be ready"
	db.session.commit()
	return redirect(url_for('recdetails', job_id=ApplicationAc.jobopening_id))

@app.route('/details')
def details():
	job_id = request.args.get('job_id')
	jobPosting = Job.query.filter_by(jobopening_id=job_id).first()
	job_schema = JobSchema()
	data = job_schema.dump(jobPosting).data
	return render_template('details.html', data=data)

@app.route('/recommjobs')
def recommjobs():
	#query the database for jobs
	currUser = User.query.filter_by(user_id=current_user.user_id).first()
	searchable_tags = currUser.searchable_tags.replace(',', '')
	jobPostings = Job.query.whooshee_search(searchable_tags).all()
	job_schema = JobSchema(many=True)
	data = job_schema.dump(jobPostings).data
	return render_template('recommjobs.html', data=data)


@app.route('/application')
def application():
    return render_template('application.html')


@app.route('/profile')
def profile():
	return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
