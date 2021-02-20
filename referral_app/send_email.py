import os
import smtplib
import email.message

email_from = os.environ.get('EMAIL_FROM')
email_password = os.environ.get('EMAIL_PASSWORD')
server_dns = 'smtp.gmail.com'
server_port = 587


def send_referral_code_email(email_to, referrer, signup_url):
    """
    Send referral code via smtp gmail server
    :param email_to: email address to send referral code
    :param signup_url: signup url
    :param referrer: referrer whose code belongs to
    :return: None
    """
    content = f"Hi,You have got a referral code '{referrer.referral_code}'.\nClick on link {signup_url} to get reward points."
    msg = email.message.Message()
    msg['Subject'] = 'Referral code'
    msg['From'] = referrer.email
    msg['To'] = email_to
    msg.set_payload(content)

    server = smtplib.SMTP("smtp.gmail.com", server_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_from, email_password)
    server.sendmail(from_addr=email_from, to_addrs=email_to, msg=msg.as_string())
