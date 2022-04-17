# RUN YOUR WAY

The live link can be found here - [site link](https://milestone4-sclarkstone.herokuapp.com/)

## setup
'pip3 install Django==3.2' to install Django
'django-admin startproject milestone4 .' to set up basic folder structure and files for Django
'touch .gitignore' to create ignore file and then add to file *.sqlite3, *.pyc

'python3 manage.py runserver' to check it is runner as expected. a Django screen will appear on the browser with the message 'The install worked successfully! Congratulations!
You are seeing this page because DEBUG=True is in your settings file and you have not configured any URLs.'

stop the server then 'python3 manage.py migrate'
'python3 manage.py createsuperuser', input a username (sclarkstone7153), email (samclarkstone@hotmail.com) and password (Unicorn2001)

git add .
git commit -m "commit message"
git push

## authentication set up

'pip3 install django-allauth==0.41.0'
add 'import os' to top of settings.py file

go to https://django-allauth.readthedocs.io/en/latest/installation.html and copy and paste AUTHENTICATION_BACKENDS plus 'SITE_ID = 1' and add any missing required apps to INSTALLED_APPS.

python3 manage.py migrate
'python3 manage.py runserver' to check it is runner as expected.

'pip3 freeze > requirements.txt'

## templates
cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates/allauth/

python3 manage.py startapp home

## font awesome
sign up for free account and get kit code. put this in the base.html template corejs block. 

## database
pip3 install pillow to allow url image use
add products to installed apps in settings.py
python3 manage.py makemigrations --dry-run
python3 manage.py makemigrations
python3 manage.py migrate --plan
python3 manage.py migrate
python3 manage.py loaddata categories
python3 manage.py loaddata products
tables can now be seen in admin area and data can be manually added



## photos
https://www.pexels.com/

ccs tricks

checkout forms
pip3 install django-crispy-forms
pip3 install django-countries - for drop down of country codes

checkout payment
pip3 install stripe

set environment variables
export STRIPE_PUBLIC_KEY=pk_test_51KRfdfDe1QIHYXng2t6CgZWkRXFUlsboPHbBv69k34W7UqqsWFGbaw9orO2jq6Ttufizc8XVUBrnHLfkPS0o68hI00LFO8BzEI
export STRIPE_SECRET_KEY=sk_test_51KRfdfDe1QIHYXngUwFlxFjissqNiIwkrncvaG2OU9akgMk1bKnT3pbyTW1bB5DtUx5dq8gdme6MpuBjNb2dJudF00qBV5tT0a

export STRIPE_WH_SECRET=whsec_vQBjhnLPA6FjFzFWfZxRizJebmNinPLc

not permananent and would need to be re exported everytime the workspace is started. so save them in gotpod (settings, variables)

test card details
name - test
email - test@test.com
phone - 1234567890
address - anywhere
card number - 4242 4242 4242 4242
card date - 04/24
CVC - 242
zip - 42424
---------------
card number - 4000 0025 0000 3155
card date - 04/24
CVC - 242
zip - 44242


# deployment
heroku - new app. provisipn postgres free
pip3 install dj_database_url
pip3 install psycopg2-binary
pip3 install gunicorn

heroku login -i
email address and use api key for password (get from heroku,account settings, reveal api key)
heroku config:set DISABLE_COLLECTSTATIC=1 --app milestone4-sclarkstone
heroku git:remote -a milestone4-sclarkstone
git checkout -b master
git push heroku master
https://miniwebtool.com/django-secret-key-generator/ to get secrete key for heroku

for static files set up cloudinary account and pip3 install cloudinary,pip3 install django-cloudinary-storage
then add cloud_name, CLOUDINARY_URL, api_key and api_secret to git pod and heroku variables
python3 manage.py collectstatic to push static files


During development deployment method changed;
a number of user login tokens for Heroku had been compromised in a security attack. In response, Heroku have removed the automatic deployment method. 
new mthod
heroku login -i
email address and use api key for password (get from heroku,account settings, reveal api key)
Run the following command: 'heroku git:remote -a milestone4-sclarkstone'. This will link the app to your Gitpod terminal.
git push heroku main


# testing
to see all errors in all files - python3 -m flake8


# bugs
chrome error - jquery must be before bootstrap. the CDN link had stopped working.

deploying to heroku - ModuleNotFoundError: No module named 'application'. amended procfile to fix
deploying to heroku - Failed to find attribute 'app' in 'milestone4'. amended procfile to fix
heroku - admin css not showing. in seetings file STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] corrected to STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),


django error 'Reverse for 'add_review' with no arguments not found'. Although i had the product_id parameter in the url.py, views.py and reviews.html template i had not got it in the form POST action on the add_review template itself.

using the search - local variable 'plans' referenced before assignment error. needed the 'plans' if inside the search if

when live on heroku - 'MIME type ('text/html') is not a supported stylesheet MIME type, and strict MIME checking is enabled' - corrected link on base template to use cloudinary and not local static file.

'operator does not exist: bigint = character varying LINE 1: ...d" = 2) AND "checkout_orderlineitem"."product_id" IN (SELECT'


# first mentor meeting

# second mentor meeting
- compress images
- change 'products' to 'plans for plans page
- add a footer
