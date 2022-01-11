from flask_login.utils import login_user
from werkzeug.utils import redirect
from app.auth.email import send_server_activation_email
from app.auth.models.user import User
from app.main.models.company import Company
from app.main.models.database import Database
from app.main.models.module import Module
from app.main.routes import generate_unique_domainname
from app.main.utils import updating
from automate import launch
from rq import get_current_job
from app.models import Task
from app import create_app, db
import time
from flask import session, flash, current_app
from flask_babel import _

app = create_app()
app.app_context().push()


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification(
            'task_progress', {'task_id': job.get_id(), 'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()


def _update_job_progress():
    job = get_current_job()
    if job:
        task = Task.query.filter_by(id=job.get_id()).first()
        task.complete = True
        db.session.commit()


def launch_instance(user_id, email, domain_name):
    try:
        # launch.new_tenant_playbook()
        seconds = 10
        print('Starting task')
        for i in range(seconds):
            print(i)
            time.sleep(1)
        print('Task completed')
        _update_job_progress()
        # launch.ami_launch_config
    except:
        pass
