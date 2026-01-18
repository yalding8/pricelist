"""
生成1024×768分辨率的报价单截图
"""
from playwright.sync_api import sync_playwright
import os

def capture_screenshot():
    """捕获1024×768分辨率下的截图"""
    html_file = "pricelist_报价单_iQ_Shoreditch.html"
    output_file = "pricelist_screenshot_1024x768.png"

    if not os.path.exists(html_file):
        print(f"❌ HTML文件不存在: {html_file}")
        return

    # 获取绝对路径
    html_path = f"file://{os.path.abspath(html_file)}"

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch()

        # 创建1024×768的页面
        page = browser.new_page(viewport={'width': 1024, 'height': 768})

        # 加载HTML
        print(f"📄 加载HTML: {html_file}")
        page.goto(html_path)

        # 等待加载完成
        page.wait_for_load_state('networkidle')

        # 截图
        print(f"📸 捕获1024×768截图...")
        page.screenshot(path=output_file, full_page=False)

        browser.close()

    print(f"✅ 截图已保存: {output_file}")
    print(f"   分辨率: 1024×768px")
    return output_file

if __name__ == "__main__":
    print("="*70)
    print("  1024×768 分辨率截图工具")
    print("="*70)
    output = capture_screenshot()
    print("="*70)
