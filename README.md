## DataBase Project 1 ReadMe
### Member
UenoRuuku
CappuccinoCup

### Overview
DataBase Project 1 is a database operation system, which mainly provides the requirements provided in the document. You can run it on a server easily if you have prepared the running environment.

### Running Environment
- Main language - Python3.8，HTML
- Backend - Django
```
# python 3.5 or higher
# Windows
Pip install Django
```
- Database Operation
```
python 3.5 or higher
> import pymysql
```

### Structure of Out Project
Front end - back end - MySQL Operation

- Frontend
	- mainly use origin HTML5, CSS3 and JavaScript
	- Use Animation.css and Jquery
	- Thanks to the powerful engine of Django, all htmls are rendered in one view, which makes the frontend more complete
- Backend
	- Backend divided its service into several small services or called tiny service. They concentrate only on their duty, which has been demonstrated as their name.
		- For example
```
/nurse
/doctor
```
	- Frontend uses ajax to make connect with backend, during which all constants that required for Mysql operation are delivered to corresponding tiny service.
	- Backend passes data to frontend using Json-format packets. Frontend gets it and the put it into html.

More, we add log in our project and all operations done to MySQL database will be logged and can be checked later. The person who connects himself to the database and what he done would be clear.
```
static/Logs/database.log
```

Online DEMO: http://150.158.192.230:8000/service

## 数据库设计Project1
### 成员
- UenoRuuku
- CappuccinoCup

### 运行环境
- 主要使用的编程语言 - Python3.8、HTML
- 前后端交互 - Django
```
Pip install Django
```
- 数据库操作
```
python 3.5 or higher
> import pymysql
```

### 项目结构
前端 - 后端 - 数据库操作
- 前端
	- 主要使用HTML5、CSS3和原生JAVASCript
	- 引用了Animation.css和JQuery库
	- 在Django的强大引擎的支持下，所有的页面可以在同一个视图中进行渲染，使得整个项目包装得更加完善
- 后端
	- 后端使用了微服务的思想，整个后端的服务被分割成了多个微服务，每个服务只关心自己的工作 - 正如他们的名字所展现的那样。
		- 举例来说
```
/nurse
/doctor 
```
- 前端使用ajax与后端交接，在这一过程中，所有的mysql操作所需要的变量都从前端转移到了后端对应的微服务中。
- 后端使用json格式的数据包向前端发送数据，前端接收到后，javaScript将之渲染在页面中。

另外我们的项目中还使用了Log对所有的数据库操作进行记录。任何人对数据库的访问都会被记录在数据库的log中，以供以后查阅。
```
static/Logs/database.log
```


项目的在线DEMO：http://150.158.192.230:8000/service
