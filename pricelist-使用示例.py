"""
pricelist 使用示例
演示如何使用核心模块生成报价单
"""

from datetime import date, timedelta
from decimal import Decimal
from jinja2 import Template

# 导入数据模型（实际使用时从 core.models 导入）
# from core.models import PropertyInfo, Discount, Gift, CompetitorPrice, AdvisorInfo, QuoteData, DiscountPayer, GiftCategory


# ========== 示例1: 创建基础报价单 ==========

def example_basic_quote():
    """基础报价单示例（手动输入所有数据）"""

    # 1. 创建房源信息
    property_info = PropertyInfo(
        property_name="iQ Shoreditch",
        room_type="Bronze Studio",
        address="2 Silicon Way, London N1 6AT",
        lease_start=date(2026, 9, 1),
        lease_end=date(2027, 8, 31),
    )

    # 2. 创建房东优惠
    landlord_discounts = [
        Discount(
            name="公寓直接返现",
            amount=Decimal("400"),
            payer=DiscountPayer.LANDLORD,
            description="由公寓运营方直接提供"
        ),
        Discount(
            name="推荐好友返现",
            amount=Decimal("200"),
            payer=DiscountPayer.LANDLORD,
            description="通过推荐好友获得"
        ),
    ]

    # 3. 创建异乡补贴
    uhomes_subsidies = [
        Discount(
            name="平台补贴价格 (£24/周)",
            amount=Decimal("1224"),  # £24 * 51周
            payer=DiscountPayer.UHOMES,
            description="异乡好居平台提供的价格优惠"
        ),
        Discount(
            name="老客户返现",
            amount=Decimal("830"),
            payer=DiscountPayer.UHOMES,
            description="老客户专享返现，签约后7-10个工作日到账"
        ),
    ]

    # 4. 选择礼品（从礼品库）
    selected_gifts = [
        Gift(
            id="cash_back_300",
            name="现金返现",
            value=Decimal("300"),
            category=GiftCategory.CASH,
            description="签约后7-10个工作日到账",
            icon="💵"
        ),
        Gift(
            id="airport_pickup",
            name="异乡接机服务",
            value=Decimal("80"),
            category=GiftCategory.SERVICE,
            description="专车接机，直达公寓",
            icon="✈️"
        ),
        Gift(
            id="welcome_pack",
            name="生活礼包",
            value=Decimal("50"),
            category=GiftCategory.GIFT,
            description="包含日用品、零食等",
            icon="🎁"
        ),
    ]

    # 5. 添加竞对价格
    competitor_prices = [
        CompetitorPrice(
            platform="Awehome",
            weekly_price=Decimal("428"),
            annual_price=Decimal("21828"),  # £428 * 51周
            url="https://www.awehome.com/uk/london/detail-apartment-4612"
        ),
        CompetitorPrice(
            platform="Amber Student",
            weekly_price=Decimal("414"),
            annual_price=Decimal("21114"),
            url="https://amberstudent.com/places/iq-shoreditch-london"
        ),
    ]

    # 6. 顾问信息
    advisor = AdvisorInfo(
        name="张顾问",
        wechat_id="uhomes_zhang",
        phone="+44 7700 900123"
    )

    # 7. 创建完整报价单
    quote = QuoteData(
        property=property_info,
        original_weekly_price=Decimal("438"),
        original_annual_price=Decimal("22338"),  # £438 * 51周
        landlord_discounts=landlord_discounts,
        uhomes_subsidies=uhomes_subsidies,
        selected_gifts=selected_gifts,
        competitor_prices=competitor_prices,
        valid_until=date.today() + timedelta(days=7),
        advisor=advisor,
    )

    # 8. 验证数据
    errors = quote.validate()
    if errors:
        print("❌ 数据验证失败:")
        for error in errors:
            print(f"  - {error}")
        return None

    # 9. 输出关键信息
    print("✅ 报价单生成成功!")
    print(f"  房源: {quote.property.property_name}")
    print(f"  原价: £{quote.original_annual_price:,.0f}/年")
    print(f"  到手价: £{quote.final_annual_price:,.0f}/年")
    print(f"  总节省: £{quote.total_savings:,.0f} ({quote.savings_rate:.1f}%)")
    print(f"  礼品价值: £{quote.total_gifts_value:,.0f}")
    if quote.advantage_vs_competitor:
        print(f"  比竞对低: £{quote.advantage_vs_competitor:,.0f} ({quote.advantage_rate:.1f}%)")

    return quote


# ========== 示例2: 生成HTML报价单 ==========

def generate_html_quote(quote: QuoteData, template_path: str) -> str:
    """生成HTML报价单"""

    # 读取模板
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # 创建Jinja2模板
    template = Template(template_content)

    # 准备模板数据
    template_data = {
        # 房源信息
        "property": quote.property,

        # 价格信息
        "original_weekly_price": quote.original_weekly_price,
        "original_annual_price": quote.original_annual_price,
        "final_weekly_price": quote.final_weekly_price,
        "final_annual_price": quote.final_annual_price,

        # 优惠信息
        "landlord_discounts": quote.landlord_discounts,
        "uhomes_subsidies": quote.uhomes_subsidies,
        "total_landlord_discount": quote.total_landlord_discount,
        "total_uhomes_subsidy": quote.total_uhomes_subsidy,

        # 礼品信息
        "selected_gifts": quote.selected_gifts,
        "total_gifts_value": quote.total_gifts_value,

        # 竞对信息
        "competitor_prices": quote.competitor_prices,
        "advantage_vs_competitor": quote.advantage_vs_competitor,
        "advantage_rate": quote.advantage_rate,

        # 汇总信息
        "total_savings": quote.total_savings,
        "savings_rate": quote.savings_rate,

        # 元信息
        "valid_until": quote.valid_until.strftime('%Y-%m-%d'),
        "advisor": quote.advisor,
    }

    # 渲染HTML
    html_content = template.render(**template_data)

    return html_content


# ========== 示例3: 生成PNG图片（需要Playwright）==========

async def generate_png_quote(html_content: str, output_path: str):
    """将HTML转换为PNG图片"""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 750, "height": 1800})

        # 加载HTML内容
        await page.set_content(html_content)

        # 等待渲染完成
        await page.wait_for_load_state('networkidle')

        # 截图
        await page.screenshot(
            path=output_path,
            full_page=True,
            type='png'
        )

        await browser.close()

    print(f"✅ PNG图片已生成: {output_path}")


# ========== 示例4: 从配置文件加载礼品库 ==========

def load_gift_library(yaml_path: str) -> list:
    """从YAML配置加载礼品库"""
    import yaml

    with open(yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    gifts = []
    for gift_data in config.get('gift_library', []):
        gift = Gift(
            id=gift_data['id'],
            name=gift_data['name'],
            value=Decimal(str(gift_data['value'])),
            category=GiftCategory(gift_data['category']),
            description=gift_data.get('description', ''),
            icon=gift_data.get('icon', '🎁'),
            unit=gift_data.get('unit', 'GBP'),
            sort_order=gift_data.get('sort_order', 999),
            is_free=gift_data.get('is_free', False),
        )
        gifts.append(gift)

    # 按排序字段排序
    gifts.sort(key=lambda g: g.sort_order)

    return gifts


# ========== 示例5: API请求处理 ==========

def api_create_quote(request_data: dict) -> dict:
    """处理API请求，创建报价单"""

    # 1. 解析请求数据
    property_info = PropertyInfo(
        property_name=request_data['property']['property_name'],
        room_type=request_data['property']['room_type'],
        address=request_data['property']['address'],
        lease_start=date.fromisoformat(request_data['property']['lease_start']),
        lease_end=date.fromisoformat(request_data['property']['lease_end']),
    )

    # 2. 从礼品库中筛选已选礼品
    gift_library = load_gift_library('config/gift_library.yaml')
    selected_gift_ids = request_data.get('selected_gift_ids', [])
    selected_gifts = [g for g in gift_library if g.id in selected_gift_ids]

    # 3. 创建报价单
    quote = QuoteData(
        property=property_info,
        original_weekly_price=Decimal(str(request_data['original_weekly_price'])),
        original_annual_price=Decimal(str(request_data['original_annual_price'])),
        # ... 其他字段
        selected_gifts=selected_gifts,
    )

    # 4. 生成HTML和PNG
    html_content = generate_html_quote(quote, 'templates/quote_card.html')
    png_path = f"output/{quote.property.property_name}_{date.today()}.png"
    # await generate_png_quote(html_content, png_path)  # 异步调用

    # 5. 返回结果
    return {
        "success": True,
        "quote_id": f"Q{date.today().strftime('%Y%m%d')}001",
        "html_url": f"/quotes/{quote.property.property_name}.html",
        "image_url": f"/quotes/{quote.property.property_name}.png",
        "summary": quote.to_dict()['summary'],
    }


# ========== 主程序 ==========

if __name__ == "__main__":
    print("=" * 60)
    print("pricelist - 异乡好居销售报价单系统")
    print("使用示例")
    print("=" * 60)
    print()

    # 示例1: 创建基础报价单
    print("【示例1】创建基础报价单")
    print("-" * 60)
    quote = example_basic_quote()
    print()

    if quote:
        # 示例2: 生成HTML
        print("【示例2】生成HTML报价单")
        print("-" * 60)
        html = generate_html_quote(quote, 'pricelist-quote_template.html')

        # 保存HTML文件
        output_html_path = 'output_quote_example.html'
        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ HTML已保存: {output_html_path}")
        print()

        # 示例3: 生成PNG（需要安装Playwright）
        print("【示例3】生成PNG图片")
        print("-" * 60)
        print("💡 提示: 需要先安装Playwright浏览器")
        print("   pip install playwright")
        print("   playwright install chromium")
        print()

        # 取消注释以下代码来生成PNG
        # import asyncio
        # asyncio.run(generate_png_quote(html, 'output_quote_example.png'))

    print("=" * 60)
    print("✅ 示例运行完成!")
    print("=" * 60)
    print()
    print("下一步操作:")
    print("1. 查看生成的HTML文件: output_quote_example.html")
    print("2. 在浏览器中打开查看效果")
    print("3. 根据需要调整模板样式")
    print("4. 安装Playwright生成PNG图片")
