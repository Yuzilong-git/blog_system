""" 博客项目入口程序 """
from src.handler import BlogServer
from src.server import SelectServer

if __name__ == '__main__':
    server = SelectServer()
    server.run(BlogServer)
