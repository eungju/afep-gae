import datetime
import os
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class Task(db.Model):
    owner = db.UserProperty(required=True)
    subject = db.StringProperty(required=True)
    created_at = db.DateTimeProperty(required=True, auto_now_add=True)
    started_at = db.DateTimeProperty()
    completed_at = db.DateTimeProperty()

class CloseMark(db.Model):
    owner = db.UserProperty(required=True)
    task = db.ReferenceProperty(Task, required=True)
    created_at = db.DateTimeProperty(required=True, auto_now_add=True)
    @classmethod
    def last(cls, n):
        return CloseMark.all().order("-created_at").fetch(n)
        
class TasksHandler(webapp.RequestHandler):
    def get(self):
        close_marks = CloseMark.last(3)
        tasks = Task.all().order("-created_at")
        if len(close_marks) > 0:
            tasks.filter("created_at >", close_marks[0].task.create_at)
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {'tasks': tasks}))
    def post(self):
        task = Task(owner=users.get_current_user(), subject=self.request.get("subject"))
        task.put()
        self.redirect("/tasks")

application = webapp.WSGIApplication(
    [('/tasks', TasksHandler)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


#Backlog
#ActiveList
