"""
生成微信分享用的PNG长图
适合直接在微信聊天中发送
"""
from playwright.sync_api import sync_playwright
import os
from datetime import datetime

def generate_wechat_image(html_file=None, output_file=None):
    """
    生成微信分享用的PNG长图

    Args:
        html_file: HTML文件路径，默认为最新的报价单
        output_file: 输出PNG文件名，默认自动生成

    Returns:
        output_file: 生成的PNG文件路径
    """
    # 默认使用最新生成的HTML
    if html_file is None:
        html_file = "pricelist_报价单_iQ_Shoreditch.html"

    if not os.path.exists(html_file):
        print(f"❌ HTML文件不存在: {html_file}")
        return None

    # 生成输出文件名
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"报价单_微信分享_{timestamp}.png"

    html_path = f"file://{os.path.abspath(html_file)}"

    print(f"📄 读取报价单: {html_file}")

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch()

        # 创建375px宽度的手机页面（微信标准宽度）
        page = browser.new_page(viewport={'width': 375, 'height': 1500})

        # 加载HTML
        page.goto(html_path)
        page.wait_for_load_state('networkidle')

        # 全页截图（长图）
        print(f"📸 生成PNG长图...")
        page.screenshot(path=output_file, full_page=True)

        browser.close()

    # 获取文件大小
    file_size = os.path.getsize(output_file) / 1024  # KB

    print(f"✅ PNG长图已生成!")
    print(f"   文件: {output_file}")
    print(f"   大小: {file_size:.1f} KB")
    print(f"   宽度: 375px (微信标准)")
    print(f"")
    print(f"💡 使用方法:")
    print(f"   1. 在微信聊天中点击 [+] 按钮")
    print(f"   2. 选择 [相册]")
    print(f"   3. 找到并发送 {output_file}")
    print(f"   4. 客户可以点击图片放大查看细节")

    return output_file

if __name__ == "__main__":
    print("="*70)
    print("  微信分享图片生成器")
    print("="*70)
    print("")

    result = generate_wechat_image()

    if result:
        print("")
        print("="*70)
        print("✅ 完成!")
        print("="*70)
