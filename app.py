# app.py - 集成文件上传功能 (引号已修正)
from flask import Flask, render_template, request, session, redirect, url_for
import os
import config
import requests
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-123'  # 用于加密session，请在生产环境中更改
app.config['UPLOAD_FOLDER'] = 'uploads'  # 上传文件保存的目录
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 限制上传文件大小为2MB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'md'}  # 允许的文件类型

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """检查文件扩展名是否合法"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def call_ai_api(prompt):
    """调用AI API"""
    api_key = config.API_KEY
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
    data = {"model": "glm-4", "messages": [{"role": "user", "content": prompt}]}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"【API错误】{type(e).__name__}: {e}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    user_input = ""
    ai_reply = None
    uploaded_filename = None
    file_content = None

    # 检查session中是否已有上传的文件内容
    if 'file_content' in session:
        file_content = session['file_content']
        uploaded_filename = session.get('uploaded_filename', '某个文件')

    if request.method == 'POST':
        # 情况1：处理文件上传
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # 读取文本文件内容
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    # 将文件内容存入session
                    session['file_content'] = file_content
                    session['uploaded_filename'] = filename
                    uploaded_filename = filename
                except UnicodeDecodeError:
                    ai_reply = "错误：文件编码不支持，请上传UTF-8编码的文本文件。"
                except Exception as e:
                    ai_reply = f"读取文件时出错：{e}"
            else:
                ai_reply = "请上传一个有效的文本文件（支持.txt, .md, .pdf）。"

        # 情况2：处理文本提问
        elif 'question' in request.form:
            user_input = request.form.get('question', '').strip()
            if user_input:
                # 如果有文件内容，将其作为上下文
                prompt = user_input
                if file_content:
                    prompt = f"请根据以下文件内容回答问题。如果问题与文件无关，请根据你的知识回答。\n\n【文件内容开始】\n{file_content}\n【文件内容结束】\n\n问题：{user_input}"
                
                ai_reply = call_ai_api(prompt)

    # 渲染页面
    return render_template(
        'chat.html',
        user_input=user_input,
        ai_reply=ai_reply,
        uploaded_filename=uploaded_filename,
        has_file=file_content is not None
    )

@app.route('/clear_file')
def clear_file():
    """清除已上传的文件内容和session"""
    session.pop('file_content', None)
    session.pop('uploaded_filename', None)
    return redirect(url_for('chat'))

@app.route('/about')
def about():
    return render_template('about.html')

# ... (app.py前面的所有代码保持不变) ...

if __name__ == '__main__':
    # 本地开发时使用
    app.run(debug=True)
else:
    # 当被Vercel等服务器运行时，使用这个配置
    # 这行代码确保了应用在服务器上能被正确加载
    pass