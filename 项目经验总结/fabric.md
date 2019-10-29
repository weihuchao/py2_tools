
## 1 版本

需要使用版本2.0.0以下的版本配合官方文档, 推荐1.14.0

## 2 文档

https://fabric-chs.readthedocs.io/zh_CN/chs/tutorial.html

## 3 使用方法

```python
def hello():
    print("Hello world!")
``` 

```bash    
$ fab hello
Hello world!

Done.
```

---

```python
def hello(name="world"):
    print("Hello %s!" % name)
``` 

```bash    
$ fab hello:name=Jeff
$ fab hello:Jeff
Hello Jeff!

Done.
```

---

```python
from fabric.api import local

def prepare_deploy():
    local("./manage.py test my_app")
    local("git add -p && git commit")
    local("git push")
``` 

```bash
$ fab prepare_deploy
[localhost] run: ./manage.py test my_app
Creating test database...
Creating tables
Creating indexes
..........................................
----------------------------------------------------------------------
Ran 42 tests in 9.138s

OK
Destroying test database...

[localhost] run: git add -p && git commit

<interactive Git add / git commit edit message session>

[localhost] run: git push

<git push session, possibly merging conflicts interactively>

Done.
```

---

```python
from fabric.api import local

def test():
    local("./manage.py test my_app")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()
```

这样有个好处, 先`test`如果执行失败了不会继续往下执行

```bash
$ fab prepare_deploy
[localhost] run: ./manage.py test my_app
Creating test database...
Creating tables
Creating indexes
.............E............................
======================================================================
ERROR: testSomething (my_project.my_app.tests.MainTests)
----------------------------------------------------------------------
Traceback (most recent call last):
[...]

----------------------------------------------------------------------
Ran 42 tests in 9.138s

FAILED (errors=1)
Destroying test database...

Fatal error: local() encountered an error (return code 2) while executing './manage.py test my_app'

Aborting.
```

---


引入如果失败之后确认是否继续

```python
from fabric.api import local, settings, abort
from fabric.contrib.console import confirm

def test():
    with settings(warn_only=True):
        result = local('./manage.py test my_app', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")
```

---

连接远程的服务器

```python

```