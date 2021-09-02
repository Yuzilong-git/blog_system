# Introduction

本项目是一个基于socket、select、pymysql模块的博客系统

可以实现注册、登录、发博客、浏览博客、点赞评论点踩等功能，且具有多并发的优点，旨在打造一个快速全面的博客系统。

# 一、开发环境

Python 3.9

# 二、数据库准备

数据库名为blog，内有user、article、comment、up_down四个数据表，结构分别如下：

### 1、blog数据库的建立

```mysql
drop database IF EXISTS blog;
create database blog default charset utf8 collate utf8_general_ci;
```

### 2、user表结构

```mysql
create table user(
id int not null auto_increment primary key,
username varchar(16) not null,
nickname varchar(16) not null,
mobile char(11) not null,
password varchar(64) not null,
email varchar(64) not null,
ctime datetime not null
)default charset=utf8;
```

### 3、article表结构

```mysql
create table article(
id int not null auto_increment primary key,
title varchar(255) not null,
text text not null,
read_count int default 0,
comment_count int default 0,
up_count int default 0,
down_count int default 0,
user_id int not null,
ctime datetime not null,
constraint fk_article_user foreign key (user_id) references user(id)
)default charset=utf8;
```

### 4、comment表结构

```mysql
create table comment(
id int not null auto_increment primary key,
content varchar(255) not null,
user_id int not null,
article_id int not null,
ctime datetime not null,
constraint fk_comment_user foreign key (user_id) references user(id),
constraint fk_comment_article foreign key (article_id) references article(id)
)default charset=utf8;
```

### 5、up_down表结构

```mysql
create table up_down(
id int not null auto_increment primary key,
choice tinyint not null,
user_id int not null,
article_id int not null,
ctime datetime not null,
constraint fk_up_down_user foreign key (user_id) references user(id),
constraint fk_up_down_article foreign key (article_id) references article(id)
)default charset=utf8;
```



# 三、启动项目

- 运行服务端

  启动blog_system项目目录下blog_server.py文件即可运行服务端

- 运行客户端

  启动blog_client项目下blog_client.py程序即可运行客户端

  运行效果如下

![image-20210618202922215](/Users/coco/Library/Application Support/typora-user-images/image-20210618202922215.png)

# 四、项目结构图

### 1、服务端项目结构图

![image-20210618210614835](/Users/coco/Library/Application Support/typora-user-images/image-20210618210614835.png)

### 2、客户端项目结构图

![image-20210618211047352](/Users/coco/Library/Application Support/typora-user-images/image-20210618211047352.png)

# 五、主要功能

### 1、用户注册功能

启动服务端及客户端后，用户输入register即可进行注册请求

注册请求前，用户表为空

![image-20210618212215377](/Users/coco/Library/Application Support/typora-user-images/image-20210618212215377.png)

发送注册请求，期间若格式不正确会提示重新输入：

![image-20210618212337923](/Users/coco/Library/Application Support/typora-user-images/image-20210618212337923.png)

重新查询用户表数据：

![image-20210618212411789](/Users/coco/Library/Application Support/typora-user-images/image-20210618212411789.png)

### 2、用户登录功能

启动服务端及客户端后，用户输入login即可进行登录请求

![image-20210618212625541](/Users/coco/Library/Application Support/typora-user-images/image-20210618212625541.png)

密码错误情况：

![image-20210618212745008](/Users/coco/Library/Application Support/typora-user-images/image-20210618212745008.png)

### 3、发布博客功能

启动服务端及客户端且登录后，用户输入post即可进行发送博客请求，发送请求前文章表为空

![image-20210618212831685](/Users/coco/Library/Application Support/typora-user-images/image-20210618212831685.png)

发送post请求：

![image-20210618212952316](/Users/coco/Library/Application Support/typora-user-images/image-20210618212952316.png)

查询文章表，可见该博客已保存至服务端数据库中

![image-20210618213043263](/Users/coco/Library/Application Support/typora-user-images/image-20210618213043263.png)

### 4、浏览博客功能

启动服务端及客户端且登录后，用户输入show即可选择浏览自己的博客还是所有博客

![image-20210618213150127](/Users/coco/Library/Application Support/typora-user-images/image-20210618213150127.png)

可查看各个博客的标题、用户名、发布时间、阅读量、评论量、点赞量和点踩量

### 5、查看博客详细内容功能

启动服务端及客户端且登录后，用户输入show_details，输入标题，即可查看该博客的具体内容

![image-20210618213433130](/Users/coco/Library/Application Support/typora-user-images/image-20210618213433130.png)

查看过后，该博客的浏览量＋1

![image-20210618213526161](/Users/coco/Library/Application Support/typora-user-images/image-20210618213526161.png)

### 6、评论博客功能

启动服务端及客户端且登录后，用户输入comment，输入标题，即可对该博客进行单层评论

![image-20210618220239263](/Users/coco/Library/Application Support/typora-user-images/image-20210618220239263.png)

评论表相应更新：

![image-20210618220300798](/Users/coco/Library/Application Support/typora-user-images/image-20210618220300798.png)

文章表相应更新：

![image-20210618220348317](/Users/coco/Library/Application Support/typora-user-images/image-20210618220348317.png)

### 7、点赞、点踩功能

启动服务端及客户端且登录后，用户输入attitude，输入标题，即可对该博客进行态度的发表

![image-20210618220439782](/Users/coco/Library/Application Support/typora-user-images/image-20210618220439782.png)

up_down表相应更新：

![image-20210618220516940](/Users/coco/Library/Application Support/typora-user-images/image-20210618220516940.png)

文章表相应更新：

![image-20210618220601540](/Users/coco/Library/Application Support/typora-user-images/image-20210618220601540.png)