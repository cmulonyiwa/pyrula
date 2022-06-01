from flask_migrate import Migrate
from app import create_app, db
from app.models import Role

app = create_app('devconfig')

migrate = Migrate(app,db)


@app.shell_context_processor
def py_auto_import():
    return dict(db=db , Role=Role)

@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
