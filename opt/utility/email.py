import smtplib, ssl

def send_email(sender, password, receiver):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    message = """\
    Subject: Hi there
    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
        print("success")

# if __name__ == "__main__":
sender = "yuyuanwang1999@gmail.com"
password = "ytpuqhpomlekpeqh"
receiver = "kaiwen_li@ucsb.edu"
send_email(sender, password, receiver)
