from flask import Flask, request ,render_template, redirect, url_for
from modeis import DB

app = Flask(__name__)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        id = request.form['id']
        print(username)
        print(id)
        global data
        data = DB().search_by_id(id)
        if not data:
            text="学号或姓名错误"
            return render_template("login.html",message=text)
        elif username == data["姓名"] and id == data["学号"]:
            return redirect("https://www.baidu.com")
        elif id == data["学号"] and username != data["姓名"]:
            text="姓名错误"
            return render_template("login.html",message=text)
    return render_template("login.html")



# @app.route('/result',methods=['GET','POST'])
# def result():
#     return render_template("result.html",studentscore=data)

if __name__ == '__main__':
    app.run(debug=True)