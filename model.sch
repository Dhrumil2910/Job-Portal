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


class Job(db.Model):
	__searchable__ = ['jobtype','joblevel','position','salary', 'jobpostdate','jobdetails','jobskills', 'joblocation']
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
	
class Message(db.Model):
	message_id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer)
	receiver_id = db.Column(db.Integer)
	body = db.Column(db.Text)
	time = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	user = db.relationship('User')

	
