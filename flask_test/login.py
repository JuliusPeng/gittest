def login():
    """模拟登陆函数"""
    b = 1
    a = b + 2
    num = a / b
    num2 = 1
    # 其他人定义的变量num1
    num1 = 1

    # dev 增加变量
    num4 = 4444

    username = "admin"
    password = "******"
    
    if username == "admin" and password == "******":
        return "登录成功!"
    else:
        return "登录失败!"
    code = 200
    return code
