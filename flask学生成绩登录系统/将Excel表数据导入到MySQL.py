import xlrd
import pymysql
import random

book = xlrd.open_workbook("高三13班三统成绩册.xlsx")#打开需要导入数据库的excel表
sheet=book.sheet_by_name("Sheet1")
#建立一个MySQL连接
conn = pymysql.connect(host="localhost",user="root",password="123456",db="score")
# 获得游标
cur = conn.cursor()
# 创建插入SQL语句
SQL_1 = 'insert into studentscore (姓名,总分赋,语文,数学,英语,日语,历史,生物赋,地理赋,名次,id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)'
# 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题行
for r in range(2, sheet.nrows):
      姓名 = sheet.cell(r, 0).value
      总分赋 = sheet.cell(r, 1).value
      语文 = sheet.cell(r, 2).value
      数学 = sheet.cell(r, 3).value
      英语 = sheet.cell(r, 4).value
      日语 = sheet.cell(r, 5).value
      历史 = sheet.cell(r, 6).value
      生物赋 = sheet.cell(r, 7).value
      地理赋 = sheet.cell(r, 8).value
      名次 = sheet.cell(r, 9).value
      id = random.randint(1,100000000)
      values = (姓名, 总分赋, 语文, 数学, 英语, 日语, 历史, 生物赋, 地理赋, 名次, id)
      print(values)
      # 执行sql语句
      cur.execute(SQL_1,values)
cur.close()
conn.commit()
conn.close()
columns = str(sheet.ncols)
rows = str(sheet.nrows)
print ("导入 " +columns + " 列 " + rows + " 行数据到MySQL数据库!")
