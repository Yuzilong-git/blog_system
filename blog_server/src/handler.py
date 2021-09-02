import re
import json
from datetime import datetime
from utils import recv_func, verify, send_func, sql_func


class BlogServer(object):
    def __init__(self, conn):
        self.conn = conn
        self.user_name = None

    def send_json_data(self, **kwargs):
        send_func.send_data(self.conn, json.dumps(kwargs, cls=DateEncoder))

    def execute(self):
        """
        用于处理客户端发送来的请求
        :return: True：继续运行，处理客户端请求。False：断开此次与该客户端的连接
        """
        conn = self.conn
        command = recv_func.recv_data(conn).decode('utf-8')
        # print(command)
        if command.upper() == "Q":
            self.send_json_data(status=True, data="退出")
            print("用户 {} 退出".format(self.user_name))
            return False
        method_map = {
            "register": self.register,
            "login": self.log_in,
            "show_blog": self.show_blog,
            "show_blog_y": self.show_blog_y,
            "post_blog": self.post_blog,
            "show_details": self.show_details,
            "comment": self.comment,
            "attitude": self.attitude
        }
        command, *args = re.split(r'\s+', command)
        method = method_map[command]
        method(*args)

        return True

    def register(self, user_name, nickname, mobile, pass_word, email):
        verify_result = verify.verify_register(user_name)
        if not verify_result:
            verify.update_info(user_name, nickname, mobile, pass_word, email)
            print("用户 {} 注册成功！".format(user_name))
            self.send_json_data(status=True, data="注册成功")
            self.user_name = user_name
        else:
            # 发送注册失败，用户名已存在
            self.send_json_data(status=False, error="用户名已存在")

    def log_in(self, user_name, password):
        verify_result = verify.verify(user_name, password)
        if verify_result:
            # 发送登录成功
            self.user_name = user_name
            print("用户 {} 登录成功！".format(user_name))
            self.send_json_data(status=True, data="登录成功")
            # 把该次通信的用户名改为改用户的用户名
        else:
            # 发送用户名不存在或密码错误
            self.send_json_data(status=False, error="用户名不存在或密码错误")

    def post_blog(self, title, content):
        user_id = sql_func.username2id(self.user_name)
        post_result = sql_func.post_article(user_id, title, content)
        if post_result:
            blog_title = post_result[0]
            blog_content = post_result[1]
            blog_dict = {"标题：": blog_title, "内容：": blog_content}
            send_dict = {"text": "博客发布成功，详情为：", "blog_dick": blog_dict}
            self.send_json_data(status=True, data=send_dict)
            print("用户 {} 成功发布标题为 {} 的博客！".format(self.user_name, blog_title))
        else:
            # 发送用户名不存在或密码错误
            self.send_json_data(status=False, error="博客发布失败，该标题博客已发布过！")

    def show_blog_y(self):
        article_tuple = sql_func.select_article(self.user_name)
        self.send_json_data(status=True, data=article_tuple)

    def show_blog(self):
        article_tuple = sql_func.show_all_article()
        self.send_json_data(status=True, data=article_tuple)

    def show_details(self, title):
        text = sql_func.select_content(title)
        if text:
            self.send_json_data(status=True, data=text)
        else:
            self.send_json_data(status=False, error="该文章不存在！")

    def comment(self, title, comment_text):
        user_id, article_id = sql_func.title2userid(title)
        result = sql_func.make_comment(comment_text, user_id, article_id)
        if result:
            self.send_json_data(status=True, data="评论成功！")
            print("用户 {} 成功发表评论！".format(self.user_name))
        else:
            # 评论失败
            self.send_json_data(status=False, error="已评论过该文章！")

    def attitude(self, title, choice):
        user_id = sql_func.username2id(self.user_name)
        article_id = sql_func.title2userid(title)[1]
        result = sql_func.make_attitude(choice, user_id, article_id)
        if result:
            self.send_json_data(status=True, data="态度评价成功！")
            print("用户 {} 成功发表态度！".format(self.user_name))
        else:
            # 评论失败
            self.send_json_data(status=False, error="态度评价失败，您已有过评价或文章不存在！")


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)
