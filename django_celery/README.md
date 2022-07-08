## Django_celery

本项目将Celery集成到Django app中，并且加入了[Flower]( https://flower.readthedocs.io/en/latest/ )作为管理工具，最终通过Docker容器化进行部署。

### 依赖包

```text
celery==4.4.2
Django==3.0.4
flower==0.9.4
redis==3.4.1

pytest==5.4.1
pytest-django==3.9.0
```

### 项目结构

```text
django_celery
├── celery_tasks
│   ├── apps.py
│   ├── __init__.py
│   ├── sample_tasks.py
│   ├── urls.py
│   └── views.py
├── django_celery
│   ├── asgi.py
│   ├── celery.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Dockerfile
├── entrypoint.sh
├── logs
│   └── celery.log
├── manage.py
├── pytest.ini
├── requirements.txt
├── static
│   ├── css
│   │   ├── bulma.min.css
│   │   └── main.css
│   └── js
│       ├── jquery-3.4.1.min.js
│       └── main.js
├── templates
│   └── index.html
├── tests
    ├── __init__.py
    └── test_tasks.py
```

### 使用方法

1. 修改`entrypoint.sh`的属性及权限：

   进入vim编辑器，`: set ff=unix`，保存

   ```shell
   $ chmod +x ./entrypoint.sh
   ```

2. 构建Docker容器

   ```shell
   $ docker-compose up -d --build
   ```

   ![docker_ps]( https://github.com/LMFrank/django_celery/blob/master/images/docker_ps.bmp )

3. 访问`http://localhost:8002/`查看主页：

   ![index]( https://github.com/LMFrank/django_celery/blob/master/images/index.bmp )

   访问`http://localhost:5555`查看Flower界面：

   ![flower]( https://github.com/LMFrank/django_celery/blob/master/images/dashboard.bmp )

4. 测试

   集成测试

   ```shell
   $ docker-compose exec web python -m pytest -k "test_task_status"
   ```

   

