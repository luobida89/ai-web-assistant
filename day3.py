import requests
import json
import config

while True:
    user_input = input("\n请输入你的问题（输入'退出'结束程序）：")
    if user_input == "退出":
        print("对话结束，再见！")
        break
    else:
        # 第一步：设置你的API Key和请求地址（以智谱AI为例）
        api_key = config.API_KEY # 🔴 请务必替换成你自己的Key！
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

        # 第二步：告诉AI我们要做什么
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        # 第三步：我们发送给AI的消息内容
        data = {
            "model": "glm-4",  # 使用指定的模型
            "messages": [
                {"role": "user", "content": user_input}
            ]
        }

        # 第四步：发送请求并获取回复
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # 第五步：打印结果
        if response.status_code == 200:
            result = response.json()
            # 从返回的JSON中提取AI的回答
            ai_reply = result['choices'][0]['message']['content']
            print("AI回复：", ai_reply)
        else:
            print("请求失败，状态码：", response.status_code)
            print("失败原因：", response.text)




