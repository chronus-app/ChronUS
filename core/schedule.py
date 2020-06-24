from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler

from core.models import Collaboration, Student


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_collaborations, 'interval', seconds=10)
    scheduler.start()

def check_collaborations():
    today = date.today()

    collaborations = Collaboration.objects.all()
    for collaboration in collaborations:
        if collaboration.deadline < today:
            requested_time = collaboration.requested_time
            collaborator = Student.objects.get(user=collaboration.collaborator)
            collaborator.available_time += requested_time
            collaborator.save()
            collaboration.delete()

    print('Success')
