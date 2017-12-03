## Setup

To make sure we can run python3 and not have to deal with package stupidity, it's best to work with a virtual environment. I create a virtual environment in a sibling folder with my repository.

The following instructions will install a virtual environment in a folder called venv.

	pip3 install virtualenv
	virtualenv venv

Then run the environment:

	./venv/bin/activate

Note: there is a bug in virtualenv, where things like pip will fail if you try to do this in a path with spaces. My best workaround at the moment is to remove spaces in your path. I hate this but not worth fighting.

Then cd into your repository folder. To get all the right packages, run:

	pip install -r requirements.txt

To run locally you need to set up a few small things. First set up the database:

	python manage.py initDB

Similarly to delete the database you would run:

	python manage.py dropDB

Then set up variables that tell our app whether it's in a dev environment, tells Flask to automatically reload on a change, and also where our app is. Then tell flask to run:

	export APP_ENV=dev
	export FLASK_DEBUG=1
	export FLASK_APP=server.py
	flask run

## File layout

The root folder has all the server code (as the .py files), the server config (.wsgi) and the package requirements (requirements.txt). 

The server code is in three parts. The main server code remains in the server.py file. It has all the views, and all the setup. manage.py just has a bunch of utility commands that you might need such as setting up the database. And config.py is the file that contains configuration for the app that is used in server.py.

The templates and static files are in their respective folders. 

All the static files are in the static folder

	\static
		\css
		\js
		\articles
	\templates
	server.py
	manage.py
	config.py
	279akz.wsgi
	requirements.txt

## Article Text File Format

For each article, the text is limited to the first ~350 words, or the first sentence ending past 350 words. The first line is the headline. A subheading is added with an em dash (–) to the same line. The second line is contains 'by AUTHOR, PUBLICATION, DATE'. Each subsequent line is a paragraph.




