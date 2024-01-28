import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()


print(os.environ.get("MY_SECRET_USER"))

def send_mail(customer, dealer, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = os.getenv('MY_SECRET_USER')
    password = os.getenv('MY_SECRET_PASSWORD')
    message = (
        f"<h3>New feedback!</h3><ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li>"
        f"<li>Comments: {comments}</li></ul>")

    sender_email = 'email1example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Lexus feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # send email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(login, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")
