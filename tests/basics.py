import unittest
from app import create_app,db

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testconfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    
    def tearDown(self):
        db.session.remove()
        self.app_context.pop()
        db.drop_all()
        
    

