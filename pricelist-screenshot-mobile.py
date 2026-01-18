"""
生成手机端截图（多种尺寸）
"""
from playwright.sync_api import sync_playwright
import os

def capture_mobile_screenshots():
    """捕获不同手机尺寸的截图"""
    html_file = "pricelist_报价单_iQ_Shoreditch.html"

    if not os.path.exists(html_file):
        print(f"❌ HTML文件不存在: {html_file}")
        return

    html_path = f"file://{os.path.abspath(html_file)}"

    # 常见手机尺寸
    devices = [
        {"name": "iPhone 13 Pro", "width": 390, "height": 844},
        {"name": "iPhone SE", "width": 375, "height": 667},
        {"name": "微信推荐", "width": 375, "height": 1500},  # 长图
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for device in devices:
            page = browser.new_page(viewport={'width': device['width'], 'height': device['height']})
            page.goto(html_path)
            page.wait_for_load_state('networkidle')

            # 全页截图
            output = f"pricelist_mobile_{device['name'].replace(' ', '_')}.png"
            page.screenshot(path=output, full_page=True)
            print(f"✅ {device['name']}: {output}")
            page.close()

        browser.close()

if __name__ == "__main__":
    print("="*70)
    print("  手机端截图工具")
    print("="*70)
    capture_mobile_screenshots()
    print("="*70)
