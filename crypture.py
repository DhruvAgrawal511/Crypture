from tkinter import *
from customtkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from Crypto.Cipher import AES

set_appearance_mode("dark")

def get_size_format(b):
    for unit in ["B", "KB", "MB", "GB"]:
        if b < 1024:
            return f"{b:.2f} {unit}"
        b /= 1024

def files():
    loc = filedialog.askopenfilenames(filetypes=(("Image files",("*.jpg","*.png","*.jpeg")),))
    file_size = sum(os.path.getsize(i) for i in loc)
    if file_size < 2 * 1024 * 1024:
        get_key_enc(loc, 32)
    elif file_size < 10 * 1024 * 1024:
        get_key_enc(loc, 24)
    else:
        get_key_enc(loc, 16)

def get_key_enc(loc, byte):
    gk = CTk()
    gk.geometry('500x250')
    gk.title('Crypture - Set Encryption Key')
    k = StringVar()

    def key_enc():
        key = bytes(k.get(), 'utf-16')
        encrypt(loc, key)
        gk.destroy()

    char = {16: 7, 24: 11, 32: 15}[byte]

    CTkLabel(gk, text=f'Enter a {char}-character key', font=('Arial', 22)).pack(pady=20)
    CTkEntry(gk, textvariable=k, fg_color='white', text_color='black', width=250).pack(pady=10)
    CTkButton(gk, text='Encrypt', command=key_enc).pack(pady=10)
    gk.mainloop()

def encrypt(loc, key):
    count = 1
    files = []
    for i in loc:
        with open(i, 'rb') as f:
            img = base64.b64encode(f.read())
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(img)
        eloc = os.path.join(os.path.dirname(i), f"Encrypted_Image_{count}.bin")
        with open(eloc, "wb") as f:
            f.write(cipher.nonce)
            f.write(tag)
            f.write(ciphertext)
        files.append(eloc)
        count += 1
    en_successful(files)

def get_key_dec():
    gk = CTk()
    gk.geometry('500x250')
    gk.title('Crypture - Set Decryption Key')
    k = StringVar()

    def key_dec():
        key = bytes(k.get(), 'utf-16')
        decrypt(key)
        gk.destroy()

    CTkLabel(gk, text='Enter Key', font=('Arial', 22)).pack(pady=20)
    CTkEntry(gk, textvariable=k, fg_color='white', text_color='black', width=250).pack(pady=10)
    CTkButton(gk, text='Decrypt', command=key_dec).pack(pady=10)
    gk.mainloop()

def decrypt(key):
    loc = filedialog.askopenfilenames(filetypes=(("Bin files","*.bin"),))
    count = 1
    files = []
    for i in loc:
        try:
            with open(i, "rb") as f:
                nonce = f.read(16)
                tag = f.read(16)
                ciphertext = f.read()
                cipher = AES.new(key, AES.MODE_EAX, nonce)
                img = base64.b64decode(cipher.decrypt_and_verify(ciphertext, tag))
            deloc = os.path.join(os.path.dirname(i), f"Decrypted_Image_{count}.jpg")
            with open(deloc, "wb") as f:
                f.write(img)
            files.append(deloc)
            count += 1
        except:
            error()
            return
    dec_successful(files)

def email(loc):
    em = CTk()
    em.geometry('600x400')
    em.title('Crypture - Email Encrypted Files')

    sen, pas, rec = StringVar(), StringVar(), StringVar()

    def send():
        try:
            mail = MIMEMultipart()
            mail['From'], mail['To'], mail['Subject'] = sen.get(), rec.get(), "Encrypted File"
            for i in loc:
                with open(i ,"rb") as f:
                    part = MIMEBase('application','octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition","attachment; filename=Encrypted_File.bin")
                    mail.attach(part)
            smtp = smtplib.SMTP('smtp.gmail.com',587)
            smtp.starttls()
            smtp.login(sen.get(), pas.get())
            smtp.sendmail(sen.get(), rec.get(), mail.as_string())
            smtp.quit()
            em_successful()
            em.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    CTkLabel(em, text='Send Encrypted Files via Email', font=('Arial', 22)).pack(pady=10)
    CTkLabel(em, text='Sender Email:').pack(pady=5)
    CTkEntry(em, textvariable=sen, fg_color='white', text_color='black').pack()
    CTkLabel(em, text='App Password:').pack(pady=5)
    CTkEntry(em, textvariable=pas, fg_color='white', text_color='black').pack()
    CTkLabel(em, text='Recipient Email:').pack(pady=5)
    CTkEntry(em, textvariable=rec, fg_color='white', text_color='black').pack()
    CTkButton(em, text='Send', command=send).pack(pady=15)
    em.mainloop()

def en_successful(loc):
    suc = CTk()
    suc.geometry('500x250')
    suc.title('Crypture - Success')
    CTkLabel(suc, text='Encryption Successful!', font=('Arial', 24)).pack(pady=20)
    CTkButton(suc, text='Save Locally', command=suc.destroy).pack(pady=5)
    CTkButton(suc, text='Send via Email', command=lambda: [suc.destroy(), email(loc)]).pack(pady=5)
    CTkButton(suc, text='Exit', command=lambda: os._exit(0)).pack(pady=5)
    suc.mainloop()

def dec_successful(loc):
    suc = CTk()
    suc.geometry('500x250')
    suc.title('Crypture - Success')
    CTkLabel(suc, text='Decryption Successful!', font=('Arial', 24)).pack(pady=20)
    CTkButton(suc, text='View Images', command=lambda: [suc.destroy(), display(loc)]).pack(pady=5)
    CTkButton(suc, text='Exit', command=lambda: os._exit(0)).pack(pady=5)
    suc.mainloop()

def display(loc):
    for i in loc:
        Image.open(i).show()
    os._exit(0) 

def em_successful():
    suc = CTk()
    suc.geometry('400x200')
    suc.title('Crypture - Email Sent')
    CTkLabel(suc, text='Email Sent Successfully!', font=('Arial', 22)).pack(pady=30)
    CTkButton(suc, text='Exit', command=lambda: os._exit(0)).pack(pady=10)
    suc.mainloop()

def error():
    err = CTk()
    err.geometry('400x250')
    err.title('Crypture - Error')
    CTkLabel(err, text='Error Occurred', font=('Arial', 24), text_color='red').pack(pady=20)
    CTkLabel(err, text='Invalid Key or Corrupted File').pack(pady=10)
    CTkButton(err, text='Home', command=lambda: [err.destroy(), main()]).pack(pady=5)
    CTkButton(err, text='Exit', command=lambda: os._exit(0)).pack(pady=5)
    err.mainloop()

def main():
    win = CTk()
    win.geometry('600x400')
    win.title('Crypture - Image Encryption Tool')

    CTkLabel(win, text='Crypture', font=('Arial', 45)).pack(pady=30)
    CTkButton(win, text='Encrypt Images', font=('Arial', 24), command=lambda: [win.destroy(), files()]).pack(pady=10)
    CTkButton(win, text='Decrypt Images', font=('Arial', 24), command=lambda: [win.destroy(), get_key_dec()]).pack(pady=10)
    CTkButton(win, text='Exit', font=('Arial', 24), command=lambda: os._exit(0)).pack(pady=30)
    win.mainloop()

main()
