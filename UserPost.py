from app import create_app,db
from app.models import User,Post,Comment
from flask_migrate import Migrate
import os,sys
import click
import coverage


app =  create_app( "development")
migrate = Migrate(app,db)

cov = None

if os.getenv("RUN_TEST_COVERAGE"):
	cov = coverage.coverage(branch=True,include="app/*")
	cov.start()

#make certain variable in the flask shell
@app.shell_context_processor
def shell__context():
	return dict(db=db,User=User,Post=Post,Comment=Comment)

#run test under test coverage
#restart if RUN_TEST_COVERAGE not defined
@app.cli.command()
@click.option("--coverage",default=False)
def tests(coverage):
	if coverage and not os.getenv("RUN_TEST_COVERAGE"):
		app.config["RUN_TEST_COVERAGE"] = "1"
		os.execvp(sys.executable,[sys.executable]+sys.argv)
	import unittest
	tests = unittest.TestLoader().discover("tests")
	unittest.TextTestRunner(verbosity=5).run(tests)
	if cov:
		cov.stop()
		cov.save()
		cov.report()

		path = os.path.abspath(".")
		tmp = os.path.join(path,"tmp")
		cov.html_report(directory=tmp)

		cov.erase()
