"""
WSGI入口文件 - 生产环境使用
"""
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(__file__))

# 导入Flask应用
from pricelist_web_app import app as application

if __name__ == "__main__":
    application.run()
