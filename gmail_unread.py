from google.oauth2.credentials import Credentials
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Quyền truy cập vào Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    # Kiểm tra nếu có tệp token.json (token lưu trữ chứng thực người dùng)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Nếu không có token hoặc token không hợp lệ, yêu cầu người dùng đăng nhập
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Lưu token để sử dụng lần sau
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def check_new_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])
    return messages

def send_notification(subject, body):
    sender_email = "your_email@gmail.com"
    receiver_email = "your_email@gmail.com"  # Email nhận thông báo
    password = "your_email_password"  # Đặt mật khẩu ứng dụng của bạn

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"Notification sent: {subject}")
    except Exception as e:
        print(f"Error sending notification: {e}")

def main():
    service = authenticate_gmail()

    while True:
        messages = check_new_emails(service)
        if messages:
            print(f"Found {len(messages)} new emails.")
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                email_subject = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject')
                email_from = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'From')

                # Gửi thông báo qua email
                send_notification(f"New Email from {email_from}", f"Subject: {email_subject}\nFrom: {email_from}")
        else:
            print("No new emails.")
        time.sleep(10)  # Kiểm tra lại sau mỗi 10 giây

if __name__ == '__main__':
    main()
