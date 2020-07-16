import os
import sendgrid


def send_mail(applicant, collaborator):
    applicant_name = applicant.full_name
    email = collaborator.user.email

    sg = sendgrid.SendGridClient(os.getenv('SENDGRID_API_KEY'))
    message = sendgrid.Mail()
    message.add_to(email)
    message.set_from(os.getenv('SENDGRID_USERNAME'))
    message.set_subject('Chronus: nueva colaboración')
    message.set_html(f'{applicant_name} acaba de aceptar tu ofrecimiento de colaboración.')
    sg.send(message)


# from django.core.mail import EmailMessage

# def send_mail(applicant, collaborator):
#     applicant_name = applicant.full_name
#     email = collaborator.user.email

#     message = EmailMessage(
#                 "Chronus: nueva colaboración",
#                 f"{applicant_name} acaba de aceptar tu ofrecimiento de colaboración.",
#                 "ernestodtv@gmail.com",
#                 [email]
#             )

#     message.send()
   