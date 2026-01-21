# config.py - 安全配置管理器
import os

# ==================== 核心配置 ====================
# 重要：真实API密钥只通过环境变量或Vercel后台设置，切勿直接写在这里！

def get_api_key():
    """
    安全获取API密钥的函数。
    优先级：1. 系统环境变量 -> 2. .env文件 -> 3. 本地开发占位符
    """
    # 1. 优先从系统环境变量读取（Vercel、Docker等云平台会在这里注入）
    api_key = os.getenv('API_KEY')
    if api_key:
        return api_key
    
    # 2. 尝试从本地的 .env 文件读取（用于更规范的本地开发）
    try:
        from dotenv import load_dotenv
        load_dotenv()  # 加载 .env 文件中的环境变量
        api_key = os.getenv('API_KEY')
        if api_key:
            return api_key
    except ImportError:
        pass  # 如果没安装python-dotenv库，则跳过
    
    # 3. 最终回退：本地开发占位符（仅在你明确知道时使用）
    # 警告：这仅用于临时本地测试，值可以是空字符串或测试密钥
    # 切勿提交包含真实密钥的代码到Git！
    LOCAL_DEV_KEY = ""  # 你可以暂时在这里填本地测试密钥，但提交前必须清空！
    if LOCAL_DEV_KEY:
        print("⚠️  警告：正在使用本地开发配置。生产环境请务必设置环境变量 API_KEY。")
        return LOCAL_DEV_KEY
    
    # 如果所有方式都未获取到密钥，抛出明确的错误
    raise ValueError(
        "❌ 未找到API密钥。请选择以下方式之一设置：\n"
        "1. (推荐) 设置系统环境变量 API_KEY\n"
        "2. 在项目根目录创建 .env 文件，写入：API_KEY=你的密钥\n"
        "3. 临时在 LOCAL_DEV_KEY 变量中填写（仅限本地测试，务必及时清除）"
    )

# 对外暴露的配置变量
API_KEY = get_api_key()  # 程序将通过这个变量使用密钥