import tkinter
import time
from  email.mime.text import MIMEText
import smtplib
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import pymysql

HOST = 'my-database.c7u2kc6sgxm7.ca-central-1.rds.amazonaws.com'
USER = 'admin'
PASSWORD = '12121212'
DB = 'email_management'

db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
csr = db.cursor()

class EmailSend:
    def __init__(self):
        # 进行gui部分的窗口搭建实现可视化操作
        # 窗口创建
        window=tkinter.Tk()
        # 大小设定
        window.geometry("500x400")
        # 窗口缩放禁止
        window.resizable(width=True,height=True)
        # 定义title
        window.title("邮件收发")
        # 主题定义标签
        label=tkinter.Label(window,text="邮件主题")
        # 把文本放入窗口
        label.pack()
        #文本框 主题
        self.title=tkinter.Entry(window,width=50)
        self.title.pack()

        # 定义内容标签
        label = tkinter.Label(window, text="邮件内容")
        # 把文本放入窗口
        label.pack()
        # 文本框 内容
        self.con = tkinter.Entry(window, width=50)
        self.con.pack()

        # 定义内容标签
        label = tkinter.Label(window, text="发件人账号")
        # 把文本放入窗口
        label.pack()
        # 文本框 账号
        self.user = tkinter.Entry(window, width=50)
        self.user.pack()

        # 定义内容标签
        label = tkinter.Label(window, text="授权码（密码）")
        # 把文本放入窗口
        label.pack()
        # 文本框 授权码
        self.pwd = tkinter.Entry(window, width=50)
        self.pwd.pack()

        # 定义内容标签
        label = tkinter.Label(window, text="收件人")
        # 把文本放入窗口
        label.pack()
        # 文本框 收件人
        self.to = tkinter.Entry(window, width=50)
        self.to.pack()

        # 发送按钮
        button=tkinter.Button(window,text="点击发送",command=self.send)
        button.pack(side="top",pady=20,ipady=10,ipadx=10)
        button = tkinter.Button(window, text="邮件管理", command=self.manage)
        button.pack(side="right", pady=20, ipady=10, ipadx=10)
        button = tkinter.Button(window, text="暂存", command=self.save)
        button.pack(side="left", pady=20, ipady=10, ipadx=10)
        timetxt=time.strftime('%Y-%m-%d-%H:%M')
        label_time=tkinter.Label(window,text="发送时间：【%s】"%timetxt)
        label_time.pack()
        # 显示
        window.mainloop()
        pass
    def send(self):
        # 当触发发送按钮的时候来调用
        # SMTP 邮件发送方法
        # 邮件发送所需：邮件主题，邮件内容，邮件发件人账号，授权码，收件人
        # 服务
        server="smtp.163.com"
        # 账号
        user=self.user.get()
        # 授权码
        pwd=self.pwd.get()
        # 内容
        content=self.con.get()
        # 内容先去转成邮件形式
        content=MIMEText(content)
        #发件人
        content["From"]=user
        # 收件人
        to=self.to.get()
        # 标题
        content["subject"]=self.title.get()
        # 定义邮件对象
        email_obj=smtplib.SMTP(server,25)
        # 登录
        email_obj.login(user=user,password=pwd)
        # 发送
        email_obj.sendmail(user,to,content.as_string())
        # 断开连接
        email_obj.quit()
        # 弹框提示发送成功
        messagebox.showinfo("发送成功","发送成功")
        title = self.title.get()
        content = self.con.get()
        sql4 = 'INSERT INTO email VALUES(0,"' + title + '","' + content + '","' + user + '","' \
               + to + '")'
        csr.execute(sql4)
        db.commit()
        pass
    def save(self):
        title = self.title.get()
        content = self.con.get()
        user = self.user.get()
        to = self.to.get()
        sql3 = 'INSERT INTO email VALUES(0,"' + title + '","' + content + '","' + user + '","' \
               + to + '")'
        csr.execute(sql3)
        db.commit()
    def manage(self):
        top = Toplevel()
        top.title("邮件管理")
        Label(top, width=5).grid(row=0, column=0, sticky=E)
        Label(top, text="题目", width=10).grid(row=0, column=1, sticky=W)
        e1 = Entry(top, textvariable="fook", width=30)
        e1.grid(row=0, column=2, padx=1, pady=1)
        e2 = Button(top, text='浏览', command=lambda: searchall(tv), width=10)
        e2.grid(row=0, column=3, padx=1, pady=1)
        e3 = Button(top, text='删除', command=lambda: delrow(tv), width=10)
        e3.grid(row=0, column=4, padx=1, pady=1)
        Label(top, width=5).grid(row=0, column=5, sticky=E)
        columns = ("序号", "邮件主题", "邮件内容", "发件人", "接收人")
        tv = ttk.Treeview(top, height=18, show="headings", columns=columns)
        tv.column("序号", width=100, anchor='center')
        tv.column("邮件主题", width=100, anchor='center')
        tv.column("邮件内容", width=200, anchor='center')
        tv.column("发件人", width=100, anchor='center')
        tv.column("接收人", width=100, anchor='center')
        tv.heading("序号", text="序号")  # 显示表头
        tv.heading("邮件主题", text="题目")
        tv.heading("邮件内容", text="发送内容")
        tv.heading("发件人", text="发件人")
        tv.heading("接收人", text="接收人")
        tv.grid(row=1, columnspan=5, padx=1, pady=1)
        def searchall(tv):  # tv为treeview
            # 查询所有内容
            sql1 = "SELECT * FROM email"
            csr.execute(sql1)
            results = csr.fetchall()
            k = 0
            # 写入数据
            for row in results:
                tv.insert('', k, values=(row[0], row[1], row[2], row[3], row[4]))
                k = k + 1

        def delrow(tv):
            a = tkinter.messagebox.askokcancel('提示', '要执行此操作吗')
            if a:
                item = tv.selection()
                item_text = tv.item(item, "values")
                sql2 = "DELETE FROM email WHERE id='" + item_text[0] + "'"
                csr.execute(sql2)
                db.commit()
            else:
                return

if __name__ == '__main__':
    wind= EmailSend()
    pass
#arcticadventure@163.com XBBUMERMDAGLHGZR 543352990@qq.com