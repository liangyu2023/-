# -使用流程
1、新建虚拟环境，之后的依赖项安装在这个环境中

命令：python3.10 -m venv chatbot

2、激活虚拟环境

命令：chatbot\Scripts\activate

3、安装依赖项

用北大源快一点：pip config set global.index-url https://mirrors.pku.edu.cn/pypi/web/simple

安装命令：pip install -r requirements.txt -U

4、运行脚本命令

4.1启动模型

在第一个终端运行：python tools/chatglm3_server.py

4.2挂载同步端口

在第二个终端运行：streamlit run webdemo.py --server.port 6006
