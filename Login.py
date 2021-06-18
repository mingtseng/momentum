
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from view import MainPage
import requests
from lxml import html

class LoginPage(object):
    def __init__(self, master=None):
        self.root = master
        self.root.geometry("300x180")
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.createPage()

    def createPage(self):
        self.page = tk.Frame(self.root)
        self.page.pack()
        ttk.Label(self.page).grid(row=0, stick=tk.W)
        ttk.Label(self.page, text='username: ').grid(row=1, stick=tk.W, pady=10)
        ttk.Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=tk.E)
        ttk.Label(self.page, text='password: ').grid(row=2, stick=tk.W, pady=10)
        ttk.Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=tk.E)
        ttk.Button(self.page, text='Login', command=self.loginCheck).grid(row=3, stick=tk.W, pady=10)
        ttk.Button(self.page, text='Quit', command=self.page.quit).grid(row=3, column=1, stick=tk.E)

    def loginCheck(self):
        re_session = requests.session()
        url_login = "http://10.20.2.73:8082/login"
        result1 = re_session.get(url_login, headers=dict(referer=url_login))
        tree = html.fromstring(result1.text)
        authenticity_token = tree.xpath("//input[@name='_token']/@value")[0]
        payload = {
            'username': self.username.get(),
            'password': self.password.get(),
            '_token': authenticity_token
        }
        url_dologin = "http://10.20.2.73:8082/system/dologin"
        rp = re_session.post(url_dologin, data=payload, headers=dict(referer=url_dologin))
        if eval(rp.text)["status"] == "1":
            MainPage.username = self.username.get()
            MainPage.re_session = re_session
            self.page.destroy()
            MainPage(self.root)

        else:
            tk.messagebox.showinfo(title="提示", message="用户名或密码输入错误")

if __name__ == '__main__':
    myroot = tk.Tk()
    myroot.geometry("+400+400")
    myroot.resizable(0, 0)
    myroot.iconphoto(False, tk.PhotoImage(file="clt_png.png"))
    myroot.title("TFL")
    mygui = LoginPage(myroot)
    myroot.mainloop()
    # pyinstaller -w -D -i clt.ico -n TFL Login.py
