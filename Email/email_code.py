import smtplib

EMAIL_ADDR = str(input('Email kamu : '))
EMAIL_PASSWD = str(input('Password : '))

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    # identifikasi dengan email server yang kita gunakan
    # harusnya ini dijalankan di background(?), tapi just in case. Dan ya, di tulis aja
    smtp.ehlo()

    # enkrip lalu lintas data
    smtp.starttls()

    # dijalankan ulang untuk re-identification dengan trafic yang sudah di enkrip
    smtp.ehlo()

    # LOGIN
    smtp.login(EMAIL_ADDR, EMAIL_PASSWD)

    EMAIL_TO = str(input('kirim email ke : '))
    subject = str(input('Masukkan subject : '))
    body = str(input('Masukkan isi email : '))

    msg = f'Subject : {subject}\n\n{body}'

    smtp.sendmail(EMAIL_ADDR, EMAIL_TO, msg)




