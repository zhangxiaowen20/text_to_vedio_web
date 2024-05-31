import os
import urllib

from flask import Flask, render_template,request,send_from_directory

import webbrowser
import threading
import pandas as pd

from data_promt_words import load_data_text
from data_split import split_data_process
from data_to_image import load_image_data
from data_to_vedio import merge_vedio
from data_tts import load_source_data_text

app = Flask(__name__,static_folder="static",template_folder="templates")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/data/<path:filename>')
def send_vedio(filename):
    return send_from_directory('data', filename)

@app.route('/')
def index():
    data = pd.read_csv("data.csv")
    table = data.to_html(index=False, table_id="my-table")
    return render_template('cloud/index.html',table=table)


@app.route('/send', methods=['POST'])
def receive_text():
    pdata = pd.read_csv("data.csv")
    api_key = pdata.iloc[5, 1]
    data = request.get_json()
    text = data.get('text')
    text = text.replace(" ","").replace(" ","")
    data_path = split_data_process(text)
    print("数据预处理完成")
    data_prompt_path = load_data_text(data_path,api_key)
    print("图片描述生成完成")
    tts_key = pdata.iloc[1, 1]
    tts_url = pdata.iloc[3, 1]
    tts_region = pdata.iloc[2, 1]
    tts_data = load_source_data_text(data_path,tts_key,tts_url,tts_region)
    print("音频生成完成")
    iamge_source= load_image_data(data_prompt_path,api_key)
    print("图片生成完成")
    path_vedio = merge_vedio(iamge_source, tts_data,data_path)
    print("视频生成完成")
    print(path_vedio)


    return path_vedio


def load_data():
    data = pd.read_csv("data.csv")
    return data

def open_browser():
    # 在启动后延迟几秒钟打开浏览器，确保Flask应用已经开始运行
    print("打开浏览器")
    webbrowser.open('http://localhost:5000')




if __name__ == '__main__':
    # 创建一个新线程来打开浏览器
    thread = threading.Timer(1,open_browser)
    thread.start()
    app.run()
    # load_data()