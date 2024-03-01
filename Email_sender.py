import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import threading
import time
import os

def send_email(receiver_email, sender_email, password, attachment_path=None, html_path=None):
    # Determine the SMTP server and port based on the sender's email domain
    if "@gmail.com" in sender_email:
        smtp_server = "smtp.gmail.com"
        port = 587
    elif "@hotmail.com" in sender_email or "@outlook.com" in sender_email:
        smtp_server = "smtp.office365.com"
        port = 587
    else:
        print("Unsupported email service")
        return

    sender_name = "Your Name Here"  # Add your name here
    msg = MIMEMultipart('alternative')
    msg['From'] = f"{sender_name} <{sender_email}>"
    msg['To'] = receiver_email
    msg['Subject'] = "HTML Email"

    # Email body - you could include a plain text version here as well
    if html_path:
        with open(html_path, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()
        msg.attach(MIMEText(html_content, 'html'))
    else:
        body = "This is a fallback plain text email body."
        msg.attach(MIMEText(body, 'plain'))

    # Attach the file if path is provided
    if attachment_path:
        file_name = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as file:
            if any(file_name.lower().endswith(ext) for ext in ['.jpeg', '.jpg', '.png', '.gif']):
                mime = MIMEImage(file.read(), name=file_name)
            else:
                mime = MIMEApplication(file.read(), Name=file_name)
        mime.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(mime)

    # Setup the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"Email sent successfully to {receiver_email}!")
    except Exception as e:
        print(f"Failed to send email to {receiver_email}. Error: {e}")

    # Delay before sending the next email
    time.sleep(2)

def main():
    sender_email = input("Enter your email address: ").strip()
    # Check if the email is a Gmail account and remind the user accordingly
    if "@gmail.com" in sender_email:
        print("Since you're using Gmail, please make sure to use your App Password if 2-Step Verification is enabled.")
    password = input("Enter your email password or App Password: ").strip()

    attach_file = input("Do you want to attach a file? (yes/no): ").strip().lower()
    attachment_path = None
    if attach_file == 'yes':
        attachment_path = input("Enter the file path of the attachment: ").strip()

    html_include = input("Do you want to include an HTML file? (yes/no): ").strip().lower()
    html_path = None
    if html_include == 'yes':
        html_path = input("Enter the file path of the HTML file: ").strip()

    with open('emails.txt', 'r') as file:
        email_list = file.read().splitlines()

    threads = []
    for email in email_list:
        thread = threading.Thread(target=send_email, args=(email, sender_email, password, attachment_path if attach_file == 'yes' else None, html_path))
        threads.append(thread)
        thread.start()
        time.sleep(2)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
