
## 0 经验总结

1. 项目不规范会导致各种各样的问题
1). 代码风格不统一
2).



## 1 短查询和长查询

```python
result_dict = {}

for obj in classroom_qs:
    result_dict[obj.id] = {
        "course_name": obj.course.name
    }

```

```python
result_dict = {}
course_classroom_map = {}
course_id_list = []

for obj in classroom_qs:
    course_id_list.append(obj.course_id)
    course_classroom_map.setdefault(obj.course_id, [])
    course_classroom_map[obj.course_id].append(obj.id)
    result_dict[obj.id] = {
        "course_name": ""
    }

# 先完成课程信息
for obj in Course.objects.filter(id__in=course_id_list, deleted=False):
    for classroom_id in course_classroom_map[obj.id]:
        result_dict[classroom_id]["course_id"] = obj.id
```

第一种方法远比第二种方法慢

### 1.1 SQL改进

django的查询转化

```python
for classroom in Classroom.objects.filter(university_id=19)[:3]:
    print classroom.name

```

会转化成SQL
```sql
SELECT
	`course_meta_classroom`.`id`,
	...省略其他classroom的所有剩余字段...
	`course_meta_classroom`.`type_of_teaching` 
FROM
	`course_meta_classroom` 
WHERE
	`course_meta_classroom`.`university_id` = 19 
	LIMIT 3
```

### 1.2 连表查询

```python
for classroom in Classroom.objects.filter(university_id=19).select_related("course")[:3]:
    print classroom.name
```

```sql
SELECT
	`course_meta_classroom`.`id`,
	...省略其他classroom的所有剩余字段...
	`course_meta_classroom`.`type_of_teaching`,
	
	`course_meta_course`.`id`,
	...省略其他course的所有剩余字段...
	`course_meta_course`.`source_instance_id` 
	
FROM
	`course_meta_classroom`
	INNER JOIN `course_meta_course` ON ( `course_meta_classroom`.`course_id` = `course_meta_course`.`id` ) 
WHERE
	`course_meta_classroom`.`university_id` = 19 
	LIMIT 3

```

```python
for classroom in Classroom.objects.filter(university_id=19).select_related("course__name")[:3]:
    print classroom.name
```

就算`select_related`指定了字段同样是取得所有的字段!

### 1.3 指定字段

```python
for info in Classroom.objects.filter(university_id=19).select_related("course").only("id", "name", "course__id", "course__name")[:3]:
    print info
```

转化成sql为

```sql
SELECT
	`course_meta_classroom`.`id`,
	`course_meta_classroom`.`name`,
	`course_meta_classroom`.`course_id`,
	`course_meta_course`.`name` 
FROM
	`course_meta_classroom`
	INNER JOIN `course_meta_course` ON ( `course_meta_classroom`.`course_id` = `course_meta_course`.`id` ) 
WHERE
	`course_meta_classroom`.`university_id` = 19 
	LIMIT 3
```

当然除了使用`only()`还可以使用`values_list()`等

### 1.4 连表没有外键的

有两种方法
一种是通过`where`关联之后查询出来, 

```python
for classroom in Classroom.objects.filter(university_id=19).extra(
        select={'department_name': "professional_department.name"},
        where=['professional_department.id = course_meta_classroom.department_id'],
        tables=["professional_department"]):
    print classroom.department_name
```

另一种直接在`select`的途中取出来

```python
department_name_sql = 'SELECT name FROM professional_department WHERE professional_department.id = course_meta_classroom.department_id'
for classroom in Classroom.objects.filter(university_id=19).extra(select={'department_name': department_name_sql}):
    print classroom.department_name
```

通过ipython的测试发现, 第一种的方法有助于缓存数据, 所以在直接跑SQL的时候总是出现执行时间不一样的情况, 实际上第一种方法比第二种方法更快

具体生成的SQL语句如下:

```sql
SELECT
	( professional_department.NAME ) AS `department_name`,
	`course_meta_classroom`.`id`,
    ...省略其他classroom的所有剩余字段...
	`course_meta_classroom`.`type_of_teaching` 
FROM
	`course_meta_classroom`,
	`professional_department` 
WHERE
	(
		`course_meta_classroom`.`university_id` = 19 
		AND ( professional_department.id = course_meta_classroom.department_id ) 
	) 
	LIMIT 3
```

第二种方法的SQL

```sql
SELECT
	(
	SELECT NAME 
	FROM
		professional_department 
	WHERE
		professional_department.id = course_meta_classroom.department_id 
	) AS `department_name`,
	`course_meta_classroom`.`id`,
	...省略其他classroom的所有剩余字段...
	`course_meta_classroom`.`type_of_teaching` 
FROM
	`course_meta_classroom` 
WHERE
	`course_meta_classroom`.`university_id` = 19;
```


相关JOIN和WHERE的阅读: 

https://blog.csdn.net/xianrenyingzi/article/details/19083133
https://www.jianshu.com/p/e7e6ce1200a4
https://www.dofactory.com/sql/join

## 2 索引命中

参考文档: 
https://blog.csdn.net/lixingying567/article/details/73505943
https://blog.csdn.net/fansunion/article/details/80095867

```
3.1 type＝ALL　全表扫描，
3.2 type＝index 索引全扫描，遍历整个索引来查询匹配的行
3.3 type=range 索引范围扫描，常见于　<,<=,>,>=,between,in等操作符。
　　　　explain select * from adminlog where id>0 , 
　　　　explain select * from adminlog where id>0 and id<=100
　　　　explain select * from adminlog where id in (1,2) 
3.4 type=ref　使用非唯一索引或唯一索引的前缀扫描，返回匹配某个单独值的记录行。ref还经常出现在JOIN操作中
3.5 type=eq_ref 类似于ref，区别就在使用的索引是唯一索引，对于每个索引键值，表中有一条记录匹配；简单来说，说是多表连接中使用　主建或唯一健作为关联条件
3.6 type=const/system 单表中最多有一个匹配行。主要用于比较primary key [主键索引]或者unique[唯一]索引,因为数据都是唯一的，所以性能最优。条件使用=。 
3.7 type=NULL　不用访问表或者索引，直接就能够得到结果　
```


```sql
EXPLAIN SELECT `course_meta_classroomuserrelationship`.`id` FROM `course_meta_classroomuserrelationship` WHERE (`course_meta_classroomuserrelationship`.`user_id` = 12);
EXPLAIN SELECT `course_meta_classroomuserrelationship`.`id` FROM `course_meta_classroomuserrelationship` WHERE (`course_meta_classroomuserrelationship`.`classroom_id` = 39);
EXPLAIN SELECT `course_meta_classroomuserrelationship`.`id` FROM `course_meta_classroomuserrelationship` WHERE (`course_meta_classroomuserrelationship`.`user_id` = 12  AND `course_meta_classroomuserrelationship`.`classroom_id` = 39);
EXPLAIN SELECT `course_meta_classroomuserrelationship`.`id` FROM `course_meta_classroomuserrelationship` WHERE (`course_meta_classroomuserrelationship`.`classroom_id` = 12  AND `course_meta_classroomuserrelationship`.`user_id` = 39);
```

其中`user_id`和`classroom_id`都有索引, 所以条件以这俩其中一个开始都会命中, 如果两个都在条件内则两个索引都会命中


```sql
EXPLAIN SELECT `course_meta_classroomuserrelationship`.`id` FROM `course_meta_classroomuserrelationship` WHERE (`course_meta_classroomuserrelationship`.`classroom_id` = 12  AND `course_meta_classroomuserrelationship`.`user_id` = 39 AND `course_meta_classroomuserrelationship`.`role` = 1);
EXPLAIN SELECT `course_meta_classroomuserrelationship`.`id` FROM `course_meta_classroomuserrelationship` WHERE (`course_meta_classroomuserrelationship`.`user_id` = 12  AND `course_meta_classroomuserrelationship`.`classroom_id` = 39 AND `course_meta_classroomuserrelationship`.`role` = 1);
```

再新增`role`的时候就不会命中索引了


```sql
EXPLAIN SELECT `course_meta_classroomuserrelationship`.`id` FROM `course_meta_classroomuserrelationship` WHERE (`course_meta_classroomuserrelationship`.`role` = 1 AND `course_meta_classroomuserrelationship`.`classroom_id` = 12  AND `course_meta_classroomuserrelationship`.`user_id` = 39);
```

同时以`role`开始同样无法命中


## 3 异步任务

```python
celery==3.1.25
django-celery==3.1.17
```

### 3.0 基础知识

1. Celery Beat：任务调度器，Beat进程会读取配置文件的内容，周期性地将配置中到期需要执行的任务发送给任务队列。
2. Celery Worker：执行任务的消费者，通常会在多台服务器运行多个消费者来提高执行效率。
3. Broker：消息代理，或者叫作消息中间件，接受任务生产者发送过来的任务消息，存进队列再按序分发给任务消费方（通常是消息队列或者数据库）。
4. Producer：调用了Celery提供的API、函数或者装饰器而产生任务并交给任务队列处理的都是任务生产者。
5. Result Backend：任务处理完后保存状态信息和结果，以供查询。Celery默认已支持Redis、RabbitMQ、MongoDB、Django ORM、SQLAlchemy等方式。





### 3.1 定时任务的写法

settings
```python
CELERY_IMPORTS = (
    'quiz.period_task', 
    'lesson.period_task', 
    'student.tasks', 
    'course_meta.period_task', 
    'cards.period_tasks',
    'gkk_course.period_task', 
    'gkk_qa.period_tasks', 
    'pc.period_tasks'
)
```

```python
from celery.task import periodic_task

@periodic_task(run_every=crontab(minute='*/10'))
def task():
    pass
    
    
@periodic_task(run_every=crontab(hour='10, 15, 19', minute=0))
def task():
    pass


```



