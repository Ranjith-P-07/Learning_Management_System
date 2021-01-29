from django.core.mail import EmailMessage


class Email:
    @staticmethod
    def addingMailBody(data):
        domainURL = "http://" + data['domain'] + '/' + 'user/login'
        email_body = f"Hi {data['username']} You were added as a {data['role']}, and please do login by using below credentials \n" \
                     f" Username: {data['username']}, Password: {data['password']} \n" \
                     f"Link: {domainURL}"
        email_data = {'email_body': email_body, 'email_subject': "Login to your account", 'to_email': data['email']}
        return email_data

    @staticmethod
    def sendEmail(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=(data['to_email'], )
        )
        email.send()
