# 57blocks
57blocks_flask_demo

库
Flask==2.0.2
PyJWT==2.3.0
requests==2.26.0
SQLAlchemy==1.4.27

启动
flask run

单元测试
python test_app.py

接口说明：

注册接口
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
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
    "state": "success"
}

#### 接口URL
> http://127.0.0.1:5000/login

#### 请求方式
> POST

#### Content-Type
> form-data


登录接口
#### 请求Body参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
email | abcd@163.com | Text | 是 | 邮箱
password | abcd1234 | Text | 是 | 密码
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
    "state": "success",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjIsInRpbWUiOjE2Mzg5NzI1ODUsImV4cCI6MTYzODk3Mjg4NX0.BZcE79CnOWbKP9-9eIEqUPn6Jgw49_v0CvUUCzNK49I"
}
```


编辑接口
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
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
    "state": "success"
}
```
