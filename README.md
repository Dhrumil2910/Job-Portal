# Job-Portal
An online job searching and posting website

## How to run
Install Flask, Flask-SqlAlchemy, Flask-Admin, Flask-marshmallow, Flask-Login, Flask-flask_whooshee using pip
and run 

```
python app.py
```

One example of install is as follows [make sure that pip is installed]
```
pip install Flask
```

Open the browser and enter localhost:5000/login

If there is no user in the database, go to "Create an Account" and register an applicant and a recruiter.

## The code structure is as follows:
<ul>
  <li> db -> database folder </li>
  <li> static -> contains all the jquery, css and image files </li>
  <li> templates  -> contains all the HTML files</li>
  <li> app.py -> Server </li>
</ul>

All the URL endpoints:
```
/login
/register
/home
/details?job_id=1
/logout
/search
/replytomessage
/appliedjobs
/rechome
/recdeletejob
/downloadresume
/recdetails
/acceptApp
/applyforjob?job_id=1
/schedule?appId=1
/recommjobs
/profile
```
Following are the database tables
```
User
Applicant
Company
Application
Job
Education
Experience
Message
```

