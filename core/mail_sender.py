import os
from django.core.mail import send_mail


def send(applicant, collaborator):
    applicant_name = applicant.full_name
    email = collaborator.user.email

    send_mail(
        'Chronus: aceptación de ofrecimiento de colaboración', 
        f'{applicant_name} acaba de aceptar tu ofrecimiento de colaboración.', 
        os.getenv('SENDGRID_USERNAME'), 
        [email], 
        fail_silently=False
    )
