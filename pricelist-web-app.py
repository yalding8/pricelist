"""
Pricelist Web应用 - 顾问表单界面
Flask后端服务
"""
from flask import Flask, render_template, request, jsonify, send_file
from datetime import date, timedelta, datetime
from decimal import Decimal
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from enum import Enum
from jinja2 import Template
import yaml
import os
import json
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# ========== 数据模型 ==========

class DiscountPayer(Enum):
    """结算方"""
    LANDLORD = "landlord"
    UHOMES = "uhomes"

class GiftCategory(Enum):
    """礼品类别"""
    CASH = "cash"
    SERVICE = "service"
    VOUCHER = "voucher"
    GIFT = "gift"

@dataclass
class PropertyInfo:
    """房源信息"""
    property_name: str
    room_type: str
    address: str
    lease_start: date
    lease_end: date

    @property
    def weeks(self) -> int:
        days = (self.lease_end - self.lease_start).days
        return max(1, days // 7)

    @property
    def lease_period_text(self) -> str:
        start = self.lease_start.strftime('%Y-%m-%d')
        end = self.lease_end.strftime('%Y-%m-%d')
        return f"{start} - {end} ({self.weeks}周)"

@dataclass
class Discount:
    """优惠"""
    name: str
    amount: Decimal
    payer: DiscountPayer

@dataclass
class Gift:
    """礼品"""
    id: str
    name: str
    value: Decimal
    category: GiftCategory
    icon: str
    description: str = ""

@dataclass
class AdvisorInfo:
    """顾问信息"""
    name: str
    phone: str
    wechat_id: str

    @property
    def avatar_initial(self) -> str:
        return self.name[0] if self.name else "?"

@dataclass
class QuoteData:
    """报价单完整数据"""
    property: PropertyInfo
    original_weekly_price: Decimal
    landlord_discounts: List[Discount] = field(default_factory=list)
    uhomes_subsidies: List[Discount] = field(default_factory=list)
    selected_gifts: List[Gift] = field(default_factory=list)
    advisor: Optional[AdvisorInfo] = None
    valid_days: int = 7

    @property
    def original_annual_price(self) -> Decimal:
        return self.original_weekly_price * self.property.weeks

    @property
    def total_landlord_discount(self) -> Decimal:
        return sum(d.amount for d in self.landlord_discounts)

    @property
    def total_uhomes_subsidy(self) -> Decimal:
        return sum(d.amount for d in self.uhomes_subsidies)

    @property
    def total_gifts_value(self) -> Decimal:
        return sum(g.value for g in self.selected_gifts)

    @property
    def final_annual_price(self) -> Decimal:
        return (self.original_annual_price -
                self.total_landlord_discount -
                self.total_uhomes_subsidy)

    @property
    def final_weekly_price(self) -> Decimal:
        return self.final_annual_price / self.property.weeks

    @property
    def total_savings(self) -> Decimal:
        return (self.total_landlord_discount +
                self.total_uhomes_subsidy +
                self.total_gifts_value)

    @property
    def savings_rate(self) -> float:
        if self.original_annual_price == 0:
            return 0
        return float(self.total_savings / self.original_annual_price * 100)

    @property
    def valid_until(self) -> str:
        valid_date = date.today() + timedelta(days=self.valid_days)
        return valid_date.strftime('%Y-%m-%d')

# ========== 工具函数 ==========

def load_gift_library():
    """加载礼品库"""
    try:
        with open('pricelist-gift_library.yaml', 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            gifts = []
            for item in data.get('gift_library', []):
                gift = Gift(
                    id=item['id'],
                    name=item['name'],
                    value=Decimal(str(item['value'])),
                    category=GiftCategory(item['category']),
                    icon=item['icon'],
                    description=item.get('description', '')
                )
                gifts.append(gift)
            return gifts
    except Exception as e:
        print(f"❌ 加载礼品库失败: {e}")
        return []

def generate_html(quote: QuoteData) -> str:
    """生成HTML报价单"""
    template_file = "pricelist-quote-wechat.html"

    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        return None

    from jinja2 import Environment
    env = Environment()
    template = env.from_string(template_content)

    # 转换数据为模板可用格式
    data = {
        "property": {
            "property_name": quote.property.property_name,
            "room_type": quote.property.room_type,
            "address": quote.property.address,
            "lease_period_text": quote.property.lease_period_text,
        },
        "original_weekly_price": float(quote.original_weekly_price),
        "original_annual_price": float(quote.original_annual_price),
        "landlord_discounts": [
            {"name": d.name, "amount": float(d.amount)}
            for d in quote.landlord_discounts
        ],
        "uhomes_subsidies": [
            {"name": d.name, "amount": float(d.amount)}
            for d in quote.uhomes_subsidies
        ],
        "selected_gifts": [
            {"name": g.name, "value": float(g.value), "icon": g.icon}
            for g in quote.selected_gifts
        ],
        "total_landlord_discount": float(quote.total_landlord_discount),
        "total_uhomes_subsidy": float(quote.total_uhomes_subsidy),
        "total_gifts_value": float(quote.total_gifts_value),
        "final_annual_price": float(quote.final_annual_price),
        "final_weekly_price": float(quote.final_weekly_price),
        "total_savings": float(quote.total_savings),
        "savings_rate": quote.savings_rate,
        "valid_until": quote.valid_until,
    }

    if quote.advisor:
        data["advisor"] = {
            "name": quote.advisor.name,
            "phone": quote.advisor.phone,
            "wechat_id": quote.advisor.wechat_id,
            "avatar_initial": quote.advisor.avatar_initial,
        }

    html = template.render(**data)
    return html

def generate_png(html_file, output_file):
    """生成PNG图片"""
    html_path = f"file://{os.path.abspath(html_file)}"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 375, 'height': 1500})
        page.goto(html_path)
        page.wait_for_load_state('networkidle')
        page.screenshot(path=output_file, full_page=True)
        browser.close()

# ========== 路由 ==========

@app.route('/')
def index():
    """主页 - 顾问表单"""
    return render_template('form.html')

@app.route('/api/gift-library')
def get_gift_library():
    """获取礼品库"""
    gifts = load_gift_library()
    return jsonify([
        {
            'id': g.id,
            'name': g.name,
            'value': float(g.value),
            'category': g.category.value,
            'icon': g.icon,
            'description': g.description
        }
        for g in gifts
    ])

@app.route('/api/generate', methods=['POST'])
def generate_quote():
    """生成报价单"""
    try:
        data = request.json

        # 解析房源信息
        property_info = PropertyInfo(
            property_name=data['property_name'],
            room_type=data['room_type'],
            address=data['address'],
            lease_start=datetime.strptime(data['lease_start'], '%Y-%m-%d').date(),
            lease_end=datetime.strptime(data['lease_end'], '%Y-%m-%d').date(),
        )

        # 解析优惠
        landlord_discounts = [
            Discount(
                name=d['name'],
                amount=Decimal(str(d['amount'])),
                payer=DiscountPayer.LANDLORD
            )
            for d in data.get('landlord_discounts', [])
        ]

        uhomes_subsidies = [
            Discount(
                name=d['name'],
                amount=Decimal(str(d['amount'])),
                payer=DiscountPayer.UHOMES
            )
            for d in data.get('uhomes_subsidies', [])
        ]

        # 解析礼品
        gift_library = {g.id: g for g in load_gift_library()}
        selected_gifts = [
            gift_library[gift_id]
            for gift_id in data.get('selected_gifts', [])
            if gift_id in gift_library
        ]

        # 解析顾问信息
        advisor = None
        if data.get('advisor_name'):
            advisor = AdvisorInfo(
                name=data['advisor_name'],
                phone=data.get('advisor_phone', ''),
                wechat_id=data.get('advisor_wechat', '')
            )

        # 创建报价单
        quote = QuoteData(
            property=property_info,
            original_weekly_price=Decimal(str(data['weekly_price'])),
            landlord_discounts=landlord_discounts,
            uhomes_subsidies=uhomes_subsidies,
            selected_gifts=selected_gifts,
            advisor=advisor
        )

        # 生成HTML
        html = generate_html(quote)
        if not html:
            return jsonify({'error': '生成HTML失败'}), 500

        # 保存HTML
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_filename = f"quote_{timestamp}.html"
        png_filename = f"quote_{timestamp}.png"

        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html)

        # 生成PNG
        generate_png(html_filename, png_filename)

        return jsonify({
            'success': True,
            'html_file': html_filename,
            'png_file': png_filename,
            'summary': {
                'property_name': quote.property.property_name,
                'original_price': float(quote.original_annual_price),
                'final_price': float(quote.final_annual_price),
                'total_savings': float(quote.total_savings),
                'savings_rate': round(quote.savings_rate, 1)
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """下载文件"""
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    print("="*70)
    print("  Pricelist 顾问表单系统")
    print("="*70)
    print("")
    print("🚀 启动Web服务...")
    print("📱 请在浏览器中打开: http://localhost:5001")
    print("")
    print("💡 功能:")
    print("  - 填写房源信息和价格")
    print("  - 选择优惠和礼品")
    print("  - 一键生成HTML和PNG报价单")
    print("")
    print("按 Ctrl+C 停止服务")
    print("="*70)
    app.run(debug=True, port=5001)
