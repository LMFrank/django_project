## Django_library

该项目尝试将自己写的一些django项目的组件结合起来构建一个图书管理系统。

项目中使用自定义的User Model，DRF构建后端api，通过Vue构建前端界面。全程使用远端Docker环境开发并测试。

### 依赖：

```text
Django==3.0.4
pymysql==0.9.3
mysqlclient==1.4.6
gunicorn==20.0.4
requests==2.23.0
Pillow==7.1.1
PyJWT==1.7.1
django-cors-headers==3.2.1
django-crispy-forms==1.9
djangorestframework==3.11.0
itsdangerous==1.1.0
flower==0.9.4
redis==3.4.1
celery==4.4.2
django-redis==4.11.0
djangorestframework-jwt==1.11.0
drf-extensions==0.3.1
```

### 使用方法：

1. 创建docker容器：

   ```shell
   $ docker-compose up -d --build
   ```

2. 迁移数据：

   ```shell
   $ docker-compose exec web python manage.py makemigrations
   $ docker-compose exec web python manage.py migrate
   ```

3. web：http://localhost:8000

   celery-dashboard：http://localhost:5555