To make sure we can run python3 and not have to deal with package stupidity, it's best to work with a virtual environment. I create a virtual environment in a sibling folder with my repository.

The following instructions will install a virtual environment in a folder called venv.

	pip3 install virtualenv
	virtualenv venv

Then run the environment:

	./venv/bin/activate

Note: there is a bug in virtualenv, where things like pip will fail if you try to do this in a path with spaces. My best workaround at the moment is to remove spaces in your path. I hate this but not worth fighting.

Then cd into your repository folder. To get all the right packages, run:

	pip install -r requirements.txt

Then run the local Flask server. First you need to tell Flask what file to look at. Then here I also tell Flask to run in developer mode so as to restart the server with code changes. Last line tells it to run. 

	export FLASK_APP=server.py
	export FLASK_DEBUG=1
	flask run




