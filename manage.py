from flask_script import Manager, prompt_bool, Server
from server import app, db

manager = Manager(app)

@manager.command
def initDB():
	db.create_all()

@manager.command
def dropDB():
	if prompt_bool('Are you sure you want to lose all your SQL data?'):
		db.drop_all()

@manager.command
def hello():
    print("hello")

manager.add_command('runserver', Server())

if __name__ == '__main__':
   manager.run()