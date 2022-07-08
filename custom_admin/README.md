## Django_custom_admin

该项目自定义了Django中的User Model，使用`email`替代`username`作为验证字段，数据库使用Postgresql。

### 依赖

```txt
Django==3.0.4
psycopg2==2.8.5
```

### 使用方法

1. 运行

   ```shell
   $ docker-compose up -d --build
   $ docker-compose exec web python manage.py makemigrations
   $ docker-compose exec web python manage.py migrate
   ```

   可以使用`docker-compose exec web python manage.py makemigrations --dry-run`查看迁移文件是否正确。

   进入http://localhost:8002/admin查看admin界面：

   ![admin]( https://github.com/LMFrank/django_custom_admin/blob/master/images/admin.bmp )

2. 测试

   ```shell
   $ docker-compose exec python manage.py test
   ```

   

   