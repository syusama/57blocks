# 57blocks
57blocks_flask_demo

#### 库
> Flask==2.0.2
> PyJWT==2.3.0
> requests==2.26.0
> SQLAlchemy==1.4.27

#### 项目启动
> flask run

#### 单元测试
> python test_app.py

##### 测试报告
```javascript
test_edit_failed_by_token_exp (__main__.TestAdd) ... ok
test_edit_success (__main__.TestAdd) ... ok
test_index (__main__.TestAdd)
test Hello world ... ok
test_login_failed (__main__.TestAdd)
登录失败 ... ok
test_login_success (__main__.TestAdd)
登录成功 ... ok
test_register_failed_by_email (__main__.TestAdd)
因邮箱格式错误导致注册失败 ... ok
test_register_failed_by_lack (__main__.TestAdd)
因缺少参数注册失败 ... ok
test_register_failed_by_repeat (__main__.TestAdd)
因已经存在导致注册失败 ... ok
test_register_success (__main__.TestAdd)
注册成功 ... ok

----------------------------------------------------------------------
Ran 9 tests in 3.351s

OK
```

### 接口说明：

### 注册接口
#### 接口URL
> http://127.0.0.1:5000/register

#### 请求方式
> POST

#### 请求Header参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
Content-type | application/json | Text | 是 | -
#### 请求Body参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
username | abcd | Text | 是 | 用户名(姓名)
email | abcd@163.com | Text | 是 | 邮箱
password | abcd1234 | Text | 是 | 密码

#### 成功响应示例
```javascript
{
    "state": "success"
}
```


### 登录接口
#### 接口URL
> http://127.0.0.1:5000/login

#### 请求方式
> POST

#### Content-Type
> form-data

#### 请求Body参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
email | abcd@163.com | Text | 是 | 邮箱
password | abcd1234 | Text | 是 | 密码

#### 成功响应示例
```javascript
{
    "state": "success",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjIsInRpbWUiOjE2Mzg5NzI1ODUsImV4cCI6MTYzODk3Mjg4NX0.BZcE79CnOWbKP9-9eIEqUPn6Jgw49_v0CvUUCzNK49I"
}
```


### 编辑接口
#### 接口URL
> http://127.0.0.1:5000/edit

#### 请求方式
> POST

#### Content-Type
> form-data

#### 请求Header参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
Authorization | Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjIsInRpbWUiOjE2Mzg5NzI1ODUsImV4cCI6MTYzODk3Mjg4NX0.BZcE79CnOWbKP9-9eIEqUPn6Jgw49_v0CvUUCzNK49I | Text | 是 | -
#### 请求Body参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
username | abc8 | Text | 否 | 姓名
age | 25 | Text | 否 | 年龄
birth | 1999-09-29 | Text | 否 | 生日

#### 成功响应示例
```javascript
{
    "state": "success"
}
```
