from django.core.mail import EmailMessage

def send_mail(applicant, collaborator):
    applicant_name = applicant.full_name
    email = collaborator.user.email

    message = EmailMessage(
                "Chronus: nueva colaboración",
                f"{applicant_name} acaba de aceptar tu ofrecimiento de colaboración.",
                "ernestodtv@gmail.com",
                [email]
            )

    message.send()
   