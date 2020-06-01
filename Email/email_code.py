import smtplib
from email.message import EmailMessage

EMAIL_ADDR = str(input('Email kamu : '))
EMAIL_PASSWD = str(input('Password : '))

msg = EmailMessage()
msg['From'] = EMAIL_ADDR
msg['To'] = EMAIL_TO = str(input('kirim email ke : '))
msg['Subject'] = str(input('Masukkan subject : '))
body = str(input('Masukkan isi email : '))

msg.set_content(body)

msg.add_alternative(f"""\
    <!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>HTML Email</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>

<body style="margin: 0; padding: 0;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;">
        <tr>
            <td align="center" bgcolor="#767c91"
                style="padding: 40px 0 30px 0; font-family: 'Montserrat', sans-serif; color: white; font-weight: bold; font-size: 25px;">
                You have a new message!
            </td>
        </tr>
        <tr>
            <td bgcolor="#f7f7f7" style="padding: 40px 30px 40px 30px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                        <td 
                            style="letter-spacing: .5px; color: #3f4b81; font-family: Arial, Helvetica, sans-serif, sans-serif; font-size: 20px; font-weight: bold;">
                            {msg['Subject']}
                        </td>
                    </tr>
                    <tr>
                        <td align="right"
                            style="padding-top: 20px ; color: #3f4b81; font-family: Arial, Helvetica, sans-serif; font-size: 15px;">
                            {msg['From']}
                            <hr>
                        </td>
                    </tr>
                    <tr>
                        <td style="letter-spacing: .5px; padding: 20px 0 30px 0; font-size: 15px;">
                            {body}
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>

</html>
    """, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    # LOGIN
    smtp.login(EMAIL_ADDR, EMAIL_PASSWD)

    smtp.send_message(msg)
