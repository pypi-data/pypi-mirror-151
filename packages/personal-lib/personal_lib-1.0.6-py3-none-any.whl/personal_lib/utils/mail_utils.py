import yagmail


def send_mail(user, password, host, port, subject, to, contents=None, cc=None, attachments=None):
    yag = yagmail.SMTP(user=user, password=password, host=host, port=port)
    yag.send(
        to=to,  # 如果多个收件人的话，写成list就行了，如果只是一个账号，就直接写字符串就行to='123@qq.com'
        cc=cc,  # 抄送
        subject=subject,  # 邮件标题
        contents=contents,  # 邮件正文
        attachments=attachments)  # 附件如果只有一个的话，用字符串就行，attachments=r'd://baidu_img.jpg'
    yag.close()
