import pymysql
from datetime import datetime
from config import settings


def verify_register(user_name):
    # 连接MySQL（socket）
    conn = pymysql.connect(host=settings.SQL_HOST, port=settings.SQL_PORT, user=settings.USER, passwd=settings.PASSWORD,
                           charset=settings.CHARSET, database=settings.DATABASE)
    cursor = conn.cursor()
    sql = "select * from user where username='{}'".format(user_name)
    cursor.execute(sql)
    result = cursor.fetchone()  # 去向mysql获取结果
    try:
        if result:
            return True
        else:
            return False
    finally:
        cursor.close()
        conn.close()


def verify(user, password):
    # 连接MySQL（socket）
    conn = pymysql.connect(host=settings.SQL_HOST, port=settings.SQL_PORT, user=settings.USER, passwd=settings.PASSWORD,
                           charset=settings.CHARSET, database=settings.DATABASE)
    cursor = conn.cursor()
    sql = "select * from user where username='{}' and password='{}'".format(user, password)
    cursor.execute(sql)
    result = cursor.fetchone()  # 去向mysql获取结果
    try:
        if result:
            return True
        else:
            return False
    finally:
        cursor.close()
        conn.close()


def update_info(user_name, nickname, mobile, pass_word, email):
    conn = pymysql.connect(host=settings.SQL_HOST, port=settings.SQL_PORT, user=settings.USER, passwd=settings.PASSWORD,
                           charset=settings.CHARSET, database=settings.DATABASE)
    cursor = conn.cursor()
    sql = 'insert into user(username,nickname,mobile,password,email,ctime) values("{}","{}","{}","{}","{}","{}")'.format(
        user_name, nickname, mobile, pass_word, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cursor.execute(sql)
    conn.commit()
    # 关闭数据库连接
    cursor.close()
    conn.close()


if __name__ == '__main__':
    update_info('coco', 'coco', '18857057972', '123456', '601656371@qq.com')
    verify_result = verify('coco', 123456)
    print(verify_result)
