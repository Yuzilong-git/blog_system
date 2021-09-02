import re
import json
import socket
import prettytable as pt
from utils import send_func, recv_func
from config import settings


class BlogClient(object):
    def __init__(self):
        self.ip = settings.IP
        self.port = settings.PORT
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None

    def run(self):
        self.conn.connect((self.ip, self.port))
        welcome = """
        注册：register
        登录：login
        显示博客列表：show
        发博客：post
        显示博客详情：show_details
        评论指定博客：comment 
        """
        print(welcome)

        method_map = {
            "register": self.register,
            "login": self.log_in,
            "show": self.show_blog,
            "post": self.post_blog,
            "show_details": self.show_details,
            "comment": self.comment,
            "attitude": self.attitude
        }

        while True:
            hint = "({})>>> ".format(self.username or "未登录")
            info = input(hint).strip()
            if not info:
                print("输入不能为空，请重新输入。")
                continue

            if info.upper() == "Q":
                print("退出成功")
                send_func.send_data(self.conn, "q")
                recv_res = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
                if recv_res['status']:
                    return

            cmd, *arg_list = re.split(r"\s+", info)

            method = method_map.get(cmd)
            if not method:
                print("命令不存在，请重新输入。")
                continue
            method(*arg_list)

        self.conn.close()

    @staticmethod
    def user_input():
        user_name = input("请输入用户名：")
        if len(user_name) > 16:
            print("用户名长度过长，请重试！")
            return
        nickname = input("请输入昵称：")
        if len(nickname) > 16:
            print("昵称长度过长，请重试！")
            return
        mobile = input("请输入手机号码：")
        if not re.findall("1[3-9]\d{9}", mobile):
            print("手机号码格式有误，请重试！")
            return
        pass_word = input("请输入密码：")
        twice_pass_word = input("请重复输入密码：")
        if pass_word != twice_pass_word:
            print("两次密码输入不一致，请重试！")
            return
        email = input("请输入邮箱：")
        if not re.findall("\w+@\w+\.\w+", email):
            print("邮箱格式有误，请重试：")
            return

        register_info = "{} {} {} {} {}".format(user_name, nickname, mobile, pass_word, email)
        return register_info

    def register(self):
        register_info = self.user_input()
        if not register_info:
            return
        send_str = "register {}".format(register_info)
        # 发送注册信息给服务端
        send_func.send_data(self.conn, send_str)
        # 接收服务端对注册的响应信息
        reply_dict = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
        if reply_dict['status']:
            print("用户 {} 注册成功！".format(register_info.split(' ')[0]))
            return
        else:
            print(reply_dict['error'])

    def log_in(self):
        user_name = input("请输入用户名：")
        password = input("请输入密码：")
        send_str = "login {} {}".format(user_name, password)
        # 发送注册信息给服务端
        send_func.send_data(self.conn, send_str)
        # 接收服务端对注册的响应信息
        reply_dict = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
        if reply_dict['status']:
            self.username = user_name
            print("{}，欢迎回来！！".format(user_name))
            return
        else:
            print(reply_dict['error'])

    def post_blog(self):
        title = input("请输入标题：")
        content = input("请输入内容：")
        send_str = "post_blog {} {}".format(title, content)
        # 发送注册信息给服务端
        send_func.send_data(self.conn, send_str)
        # 接收服务端对注册的响应信息
        reply_dict = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
        if reply_dict['status']:
            blog_dict = reply_dict['data']
            print(blog_dict["text"])
            for key in blog_dict["blog_dick"]:
                print(key, blog_dict["blog_dick"][key])
            return
        else:
            print(reply_dict['error'])

    def show_blog(self):
        choice = input("显示自己的博客输入Y/y，显示所有请输入其他：")
        if choice.upper() == "Y":
            send_str = "show_blog_y"
        else:
            send_str = "show_blog"
        # 发送注册信息给服务端
        send_func.send_data(self.conn, send_str)
        # 接收服务端对注册的响应信息
        reply_dict = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
        if reply_dict['status']:
            show_list = reply_dict['data']
            title_list = ['标题', '用户', '文章发布时间', '阅读', '评论', '点赞', '点踩']
            tb = pt.PrettyTable()
            tb.set_style(pt.PLAIN_COLUMNS)
            tb.field_names = title_list
            for blog in show_list:
                tb.add_row(blog)
            print(tb)
            return
        else:
            print(reply_dict['error'])

    def show_details(self):
        title = input("请输入要查看文章的标题：")
        send_str = "show_details {}".format(title)
        # 发送注册信息给服务端
        send_func.send_data(self.conn, send_str)
        # 接收服务端对注册的响应信息
        reply_dict = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
        if reply_dict['status']:
            article_list = reply_dict['data']
            for blog in article_list:
                print("该文章内容为：", blog[0])
            return
        else:
            print(reply_dict['error'])

    def comment(self):
        title = input("请输入想要评论的文章标题：")
        content = input("请输入要评价的内容：")
        send_str = "comment {} {}".format(title, content)
        # 发送注册信息给服务端
        send_func.send_data(self.conn, send_str)
        # 接收服务端对注册的响应信息
        reply_dict = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
        if reply_dict['status']:
            print(reply_dict['data'])
            return
        else:
            print(reply_dict['error'])

    def attitude(self):
        title = input("请输入文章标题：")
        print("""点赞请输入：1     点踩请输入：0 """)
        choice = int(input("请输入您的态度：").strip())
        choice_list = [0, 1]
        if choice not in choice_list:
            print("输入有误，请重试！")
            return
        send_str = "attitude {} {}".format(title, choice)
        # 发送注册信息给服务端
        send_func.send_data(self.conn, send_str)
        # 接收服务端对注册的响应信息
        reply_dict = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
        if reply_dict['status']:
            print(reply_dict['data'])
            return
        else:
            print(reply_dict['error'])
