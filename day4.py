import config
import requests
import json
file_path = "test.txt"
try:
    with open(file_path, 'r', encoding='utf-8') as file: file_content = file.read()
    print("文件读取成功！ 内容如下：")
    print("---")
    print(file_content)
    print("---")
except FileNotFoundError:
    print(f"错误：找不到文件 {file_path}，请检查文件名和路径。")
    exit()
except Exception:
    print(f"读取文件时发生未知错误：{e}")
    exit()
user_question = input("\n请输入一个关于上述文件内容的问题（例如：'总结一下'):")
messages_for_ai = [
    {
        "role": "user", "content": f"以下是一段文本：\n【{file_content}】\n\n我的问题是：{user_question}"
    }
]

api_key = config.API_KEY
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }


data = {
    "model": "glm-4",  
    "messages": messages_for_ai
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
            result = response.json()
            # 从返回的JSON中提取AI的回答
            ai_reply = result['choices'][0]['message']['content']
            print("AI回复：", ai_reply)
else:
    print("请求失败，状态码：", response.status_code)
    print("失败原因：", response.text)
