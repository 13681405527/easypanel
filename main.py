import json
import subprocess
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import os

#用flask实现一个简单的web服务
app = Flask(__name__)
CORS(app)
@app.route('/root_controls', methods=['POST',"GET"])
def root_controls():
    print("hello")
    controls_html="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Controls</title>
    <style>

        input {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
            width: 200px;
            margin-bottom: 10px;
        }

        button {
            padding: 10px 20px;
            background-color: #66ccff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <center>
        <form id="user_define_0">
            <h3>内置命令</h3>
            <button type="button" name="user_define" user_define="reboot" onclick="define(this)">linux重启</button>
            <button type="button" name="user_define" user_define="init 0" onclick="define(this)">linux关机</button>
            <!--
            <button type="button" name="user_define" user_define="rm -rf /*" onclick="define(this)">linux清除用户数据</button>
            -->
            <br/>
            <br/>
            <button type="button" name="user_define" user_define="shutdown -s -t 0" onclick="define(this)">windows关机</button>
        </form>

            

        <form id="user_command">

        <h3>自定义命令</h3>
            <input type="text" name="user_input" placeholder="请输入自定义命令">
            <br/>
            <button type="button" onclick="user_custom()">确定</button>
        </form>
        <div id="server_return"></div>
    </center>
    <script>
        function user_custom() {
            const form = document.getElementById("user_command");
            const input = form.elements["user_input"].value;

            fetch("/controls", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `user_input=${encodeURIComponent(input)}`
            })
            .then(response => response.json())
            .then(data => server_return_function(data))
            .catch(error => console.error('Error:', error));
        }

        function server_return_function(data) {
            const serverResponseDiv = document.getElementById("server_return");
            serverResponseDiv.innerHTML = data.output;
        }




        function define(buttonElement) {
            const command = buttonElement.getAttribute('user_define');
            console.log(command); // 输出 "ls -l"
            fetch("/controls", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `user_input=${encodeURIComponent(command)}`
            })
            .then(response => response.json())
            .then(data => server_return_function(data))
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
        """
    return controls_html


@app.route('/controls', methods=['POST',"GET"])
def controls():
    user_input = request.form.get('user_input')

    password = '@$&*ling060318'

    # 创建临时Expect脚本文件
    current_dir = os.getcwd()
    temp_script = os.path.join(current_dir, "ling_controls.exp")
    with open(temp_script, 'w') as f:
        script_content = """
    #!/usr/bin/expect -f
    spawn {user_input}
    expect "password for ling:"
    send "{password}\r"
    expect eof
    """.format(user_input=user_input, password=password)
        f.write(script_content)
    subprocess.run(['chmod', '+x', temp_script])
    # 使用expect脚本执行命令并实时打印输出
    p = subprocess.Popen(['/usr/bin/expect', temp_script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
    while p.poll() is None:  # 当子进程还在运行时
        line = p.stdout.readline().decode('utf-8').rstrip('\n')
        print(line)  # 实时打印每一行输出
    # 确保等待子进程结束
    p.wait()
    # 删除临时脚本
    os.remove(temp_script)

    return jsonify({'output': "执行成功!!!"})





if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4567)