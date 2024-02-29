import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import threading
import time
import os

def send_email(receiver_email, attachment_path=None, html_path=None):
    sender_email = "your@mail.com" #your hotmail email
    password = "your_hotmail_password" #your hotmail password ( must be your hotmail password, not your app password)

    # Create MIME message
    msg = MIMEMultipart('alternative')  # Use 'alternative' to support both plain text and HTML
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "HTML Email from Hotmail"

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
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"Email sent successfully to {receiver_email}!")
    except Exception as e:
        print(f"Failed to send email to {receiver_email}. Error: {e}")

    # Delay before sending the next email
    time.sleep(2)  # Adjust the delay as needed

def main():
    # Ask user if they want to attach a file
    attach_file = input("Do you want to attach a file? (yes/no): ").strip().lower()
    attachment_path = None
    if attach_file == 'yes':
        attachment_path = input("Enter the file path of the attachment: ").strip()

    # Optionally, specify the path to your HTML file
    html_path = "path/to/your/html_file.html"  # Adjust this path or your html file name if already in the same directory

    # Read email addresses from file
    with open('emails.txt', 'r') as file:
        email_list = file.read().splitlines()

    threads = []
    for email in email_list:
        thread = threading.Thread(target=send_email, args=(email, attachment_path if attach_file == 'yes' else None, html_path))
        threads.append(thread)
        thread.start()
        time.sleep(2)  # Adjust the delay of the threads

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
