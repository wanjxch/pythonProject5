import pymysql

class DB:
    def __init__(self):
        self.conn = pymysql.connect(host="localhost",user="root",password="123456",db='score')
        self.cursor = self.conn.cursor()

    def search_by_id(self,id):
        try:
            self.cursor.execute("select * from studentscore where id =  " + id + ";")
            data = self.cursor.fetchall()
            data_dict = {
                "姓名": data[0][0],
                "总分赋": data[0][1],
                "语文": data[0][2],
                "数学": data[0][3],
                "英语": data[0][4],
                "日语": data[0][5],
                "历史": data[0][6],
                "生物赋": data[0][7],
                "地理赋": data[0][8],
                "名次": data[0][9],
                "id": data[0][10],
            }
            return data_dict
        except:
            return False
if __name__ == '__main__':
    db= DB()
    print(db.search_by_id(id))