import smtplib
from email.message import EmailMessage

def send_email(subject, body):
    # 邮件发送者和接收者
    sender = "yuandongx@126.com"
    app_password  = "YSRHF3FNBybkEHaV"
    receiver = "786018072@qq.com"
    smtp_server = "smtp.126.com"
    port = 465

    # 构造邮件
    msg = EmailMessage()
    msg["Subject"] = "Report with Attachment"
    msg["From"] = sender
    msg["To"] = receiver

    # 正文
    msg.set_content(body)
    msg.add_alternative(
        f"""\
        <html>
            <body>
                <h1>{subject}</h1>
                <p>{body}</p>
            </body>
        </html>
        """,
        subtype="html",
    )


    server =  smtplib.SMTP_SSL(smtp_server, port) 
    server.login(sender, app_password)
    server.send_message(msg)


if __name__ == "__main__":
    subject = "Test Email"
    body = "This is a test email sent from Python."
    send_email(subject, body)
    print("Email sent successfully.")