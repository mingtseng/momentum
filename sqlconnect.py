import pymysql

# 1.连接到mysql数据库
conn = pymysql.connect(
                        host='local host',  # 连接本地数据库
                        user='root',        # 用户名
                        password='1234',    # 密码
                        db='repository',    # 数据库名称
                        charset='utf-8'     # 数据库编码格式
                       )
# 2.创建游标对象
cur = conn.cursor()     # cur当前的程序到数据之间连接的管道

# 3.组装sql语句 需要查询的MySQL语句
sql = 'select * from repository'

# 4.执行sql语句
cur.execute(sql)

# 5.处理结果集
# 获取一条数据
one = cur.fetchone()
print(one)

# 获取多条数据 传入需要获取的数据的条数
many = cur.fetchmany(3)
print(many)

# 获取所有数据
all = cur.fetchall()
# 输出获取到的数据的数据类型
print(type(all))

# 逐条输出获取到的数据类型及数据
for each in all:
    print(type(each), each)

# 获取数据库表中列的参数
fields = cur.description
head = []

# 获取数据库中表头
for field in fields:
    head.append(field[0])
print(head)

# 6.关闭所有的连接
# 关闭游标
cur.close()
# 关闭数据库
conn.close()


