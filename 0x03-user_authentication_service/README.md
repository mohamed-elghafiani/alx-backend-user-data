# 0x03. User authentication service
### `Back-end` `Authentification`

In the industry, you should `not` implement your own authentication system and use a module or framework that doing it for you (like in Python-Flask: [Flask-User](https://flask-user.readthedocs.io/en/latest/)). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

![](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2019/12/4cb3c8c607afc1d1582d.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20240426%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240426T134704Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=a6a6cb487e1a0460f89f3b8cbf2e4b8275a5faedcd207979680b04942e0adc96)

## Resources
* [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
* [Requests module](https://requests.kennethreitz.org/en/latest/user/quickstart/)
* [HTTP status codes](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)

## Setup
You will need to install bcrypt
```
pip3 install bcrypt
```
