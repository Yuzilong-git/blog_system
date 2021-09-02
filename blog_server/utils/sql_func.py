import pymysql
from datetime import datetime
from config import settings


# 查找用户名对应的ID
def username2id(user_name):
    # 连接MySQL（socket）
    conn = pymysql.connect(host=settings.SQL_HOST, port=settings.SQL_PORT, user=settings.USER, passwd=settings.PASSWORD,
                           charset=settings.CHARSET, database=settings.DATABASE)
    cursor = conn.cursor()
    sql = "select id from user where username='{}'".format(user_name)
    cursor.execute(sql)
    result = cursor.fetchone()[0]  # 去向mysql获取结果
    try:
        return result
    finally:
        cursor.close()
        conn.close()


def post_article(user_id, title, content):
    # 连接MySQL（socket）
    conn = pymysql.connect(host=settings.SQL_HOST, port=settings.SQL_PORT, user=settings.USER, passwd=settings.PASSWORD,
                           charset=settings.CHARSET, database=settings.DATABASE)
    cursor = conn.cursor()
    sql = 'select * from article where title="{}"'.format(title)
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        return
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = 'insert into article(title,text,user_id,ctime) values("{}","{}","{}","{}")'.format(title, content, user_id,
                                                                                             now_time)
    cursor.execute(sql)
    conn.commit()
    sql = 'select title,text from article where title="{}" and text="{}" and ctime="{}"'.format(title, content,
                                                                                                now_time)
    cursor.execute(sql)
    result = cursor.fetchall()
    try:
        return result[0]
    finally:
        cursor.close()
        conn.close()


def select_article(user_name):
    conn = pymysql.connect(host=settings.SQL_HOST, port=settings.SQL_PORT, user=settings.USER, passwd=settings.PASSWORD,
                           charset=settings.CHARSET, database=settings.DATABASE)
    cursor = conn.cursor()
    sql = "select nickname from user where username='{}'".format(user_name)
    cursor.execute(sql)
    result = cursor.fetchone()[0]  # 去向mysql获取结果
    sql = "select title,nickname,article.ctime,read_count,comment_count,up_count,down_count from user left outer join article on user.id=article.user_id where nickname='{}'".format(
        result)
    cursor.execute(sql)
    result = cursor.fetchall()
    try:
        return result
    finally:
        cursor.close()
        conn.close()


def show_all_article():
    conn = pymysql.connect(host=settings.SQL_HOST, port=settings.SQL_PORT, user=settings.USER, passwd=settings.PASSWORD,
                           charset=settings.CHARSET, database=settings.DATABASE)
    cursor = conn.cursor()
    sql = "select title,nickname,article.ctime,read_count,comment_count,up_count,down_count from user left outer join article on user.id=article.user_id"
    cursor.execute(sql)
    result = cursor.fetchall()
    blog_list = []
    for blog in result:
        if blog[0] is not None:
            blog_list.append(blog)
    try:
        return blog_list
    finally:
        cursor.close()
        conn.close()


def select_content(title):
    conn = pymysql.connect(host=settings.SQL_HOST, port=settings.SQL_PORT, user=settings.USER, passwd=settings.PASSWORD,
                           charset=settings.CHARSET, database=settings.DATABASE)
    cursor = conn.cursor()
    sql = "select text from article where title='{}'".format(title)
    cursor.execute(sql)
    result = cursor.fetchall()
    try:
        sql = "update article set read_count=read_count+1 where title='{}'".format(title)
        cursor.execute(sql)
        conn.commit()
        return result
    finally:
        cursor.close()
        conn.close()


def title2userid(title):
    # 连接MySQL（socket）
    conn = pymysql.connect(host=settings.SQL_HOST, port=settings.SQL_PORT, user=settings.USER, passwd=settings.PASSWORD,
                           charset=settings.CHARSET, database=settings.DATABASE)
    cursor = conn.cursor()
    sql = "select user_id, id from article where title='{}'".format(title)
    cursor.execute(sql)
    result = cursor.fetchone()  # 去向mysql获取结果
    try:
        return result
    finally:
        cursor.close()
        conn.close()


def make_comment(content, user_id, article_id):
    # 连接MySQL（socket）
    conn = pymysql.connect(host=settings.SQL_HOST, port=settings.SQL_PORT, user=settings.USER,
                           passwd=settings.PASSWORD,
                           charset=settings.CHARSET, database=settings.DATABASE)
    cursor = conn.cursor()
    sql = 'select * from comment where user_id="{}"'.format(user_id)
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    if result:
        return
    print("可以写")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = 'insert into comment(content,user_id,article_id,ctime) values("{}","{}","{}","{}")'.format(content, user_id, article_id, now_time)
    cursor.execute(sql)
    conn.commit()
    sql = 'select * from comment where ctime="{}"'.format(now_time)
    cursor.execute(sql)
    result = cursor.fetchone()
    print("评论好了", result)
    try:
        if result[0]:
            sql = 'update article set comment_count=comment_count+1 where id="{}"'.format(article_id)
            cursor.execute(sql)
            conn.commit()
            return True
        else:
            return False
    finally:
        cursor.close()
        conn.close()


def make_attitude(choice, user_id, article_id):
    # 连接MySQL（socket）
    print(user_id, article_id)
    conn = pymysql.connect(host=settings.SQL_HOST, port=settings.SQL_PORT, user=settings.USER,
                           passwd=settings.PASSWORD,
                           charset=settings.CHARSET, database=settings.DATABASE)
    cursor = conn.cursor()
    sql = 'select choice from up_down where article_id="{}" and user_id="{}"'.format(article_id, user_id)
    cursor.execute(sql)
    is_att_result = cursor.fetchone()
    # 之前没有评价过该文章
    if not is_att_result:
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = 'insert into up_down(choice,user_id,article_id,ctime) values("{}","{}","{}","{}")'.format(choice, user_id, article_id, now_time)
        cursor.execute(sql)
        conn.commit()
        sql = 'select * from up_down where ctime="{}"'.format(now_time)
        cursor.execute(sql)
        result = cursor.fetchone()
    else:
        return
    try:
        if result[0]:
            if result[1] == 1:
                sql = 'update article set up_count=up_count+1 where id="{}"'.format(article_id)
            else:
                sql = 'update article set down_count=down_count+1 where id="{}"'.format(article_id)
            cursor.execute(sql)
            conn.commit()
            return True
        else:
            return False
    finally:
        cursor.close()
        conn.close()
