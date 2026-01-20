import config
import requests
import json

#调用AI API的通用函数，返回AI的回复文本或错误信息
def call_ai_api(messages):
    api_key = config.API_KEY
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

    data = {
        "model": "glm-4",  
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        return "【错误】 请求超时，请检查网络。"
    except requests.exceptions.RequestException as e:
        return f"【错误】 API请求失败：{e}"
    except (KeyError, json.JSONDecodeError):
        return "【错误】 解析API响应时出错。"

#自由对话
def chat_mod():

    print('\n' + "="*30)
    print("已进入自由对话模式")
    print('='*30)

    while True:
        user_input = input("\n你：")
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("结束对话，返回主菜单。")
            break
        messages = [{"role":"user", "content":user_input}]
        print("AI:",end="")
        reply = call_ai_api(messages)
        print(reply)

#文件分析对话
def file_mode():

    print('\n' + "="*30)
    print("已进入自由对话模式")
    print('='*30)

    #读取文件
    file_name = input("请输入要分析的文件名：").strip()
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            file_content = f.read()
        print(f"文件 '{file_name}'读取成功,共{len(file_content)} 个字符。")
    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_name}', 请检查路径和文件名。 ")
        return
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return
    
    #与AI交互分析文件
    print("/n现在你可以针对文件内容提问了（输入'返回'退出此模式)。")
    while True:
        user_question = input("\n你的问题：")
        if user_question == "返回":
            print("退出文件分析模式。")
            break

        prompt = f"请根据以下文本内容回答问题。如果问题与文本无关，请说明。\n\n【文本开始】 \n{file_content}\n【文本结束】\n\n问题：{user_question}"
        messages = [{"role":"user", "content":prompt}]

        print("\nAI分析：",end="")
        reply = call_ai_api(messages)
        print(reply)
    
def main():
    print("*欢迎使用你的初代AI个人助手！*")
    while True:
        print('\n'+"="*30)
        print("请选择模式：")
        print(" 1.自由对话模式")
        print(" 2.文件分析模式")
        print(" 3.退出程序")
        print("="*30)

        choice = input("请输入选项:").strip()

        if choice == "1":
            chat_mod()
        elif choice == "2":
            file_mode()
        elif choice == "3":
            print("感谢使用，再见！")
            break
        else:
            print("输入无效，请输入1，2或3.")

if __name__ == "__main__":
    main()