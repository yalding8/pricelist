"""
pricelist 完整演示脚本
可以直接运行，无需安装项目
"""

from datetime import date, timedelta
from decimal import Decimal
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from jinja2 import Template


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
    """优惠项"""
    name: str
    amount: Decimal
    payer: DiscountPayer
    description: str = ""

    def __post_init__(self):
        if isinstance(self.amount, (int, float)):
            self.amount = Decimal(str(self.amount))
        if isinstance(self.payer, str):
            self.payer = DiscountPayer(self.payer)


@dataclass
class Gift:
    """礼品"""
    id: str
    name: str
    value: Decimal
    category: GiftCategory
    description: str = ""
    icon: str = "🎁"
    is_free: bool = False

    def __post_init__(self):
        if isinstance(self.value, (int, float)):
            self.value = Decimal(str(self.value))
        if isinstance(self.category, str):
            self.category = GiftCategory(self.category)

    @property
    def category_name(self) -> str:
        names = {
            GiftCategory.CASH: "现金类",
            GiftCategory.SERVICE: "服务类",
            GiftCategory.VOUCHER: "优惠券",
            GiftCategory.GIFT: "实物礼品",
        }
        return names.get(self.category, "其他")


@dataclass
class CompetitorPrice:
    """竞对价格"""
    platform: str
    weekly_price: Decimal
    annual_price: Decimal
    url: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.weekly_price, (int, float)):
            self.weekly_price = Decimal(str(self.weekly_price))
        if isinstance(self.annual_price, (int, float)):
            self.annual_price = Decimal(str(self.annual_price))


@dataclass
class AdvisorInfo:
    """顾问信息"""
    name: str
    wechat_id: str
    phone: str
    qr_code_url: Optional[str] = None

    @property
    def avatar_initial(self) -> str:
        return self.name[0] if self.name else "?"


@dataclass
class QuoteData:
    """完整报价单数据"""
    property: PropertyInfo
    original_weekly_price: Decimal
    original_annual_price: Decimal
    landlord_discounts: List[Discount] = field(default_factory=list)
    uhomes_subsidies: List[Discount] = field(default_factory=list)
    selected_gifts: List[Gift] = field(default_factory=list)
    competitor_prices: List[CompetitorPrice] = field(default_factory=list)
    valid_until: Optional[date] = None
    advisor: Optional[AdvisorInfo] = None
    created_at: date = field(default_factory=date.today)

    def __post_init__(self):
        if isinstance(self.original_weekly_price, (int, float)):
            self.original_weekly_price = Decimal(str(self.original_weekly_price))
        if isinstance(self.original_annual_price, (int, float)):
            self.original_annual_price = Decimal(str(self.original_annual_price))
        if self.valid_until is None:
            self.valid_until = date.today() + timedelta(days=7)

    @property
    def total_landlord_discount(self) -> Decimal:
        return sum(d.amount for d in self.landlord_discounts)

    @property
    def total_uhomes_subsidy(self) -> Decimal:
        return sum(s.amount for s in self.uhomes_subsidies)

    @property
    def total_gifts_value(self) -> Decimal:
        return sum(g.value for g in self.selected_gifts)

    @property
    def final_annual_price(self) -> Decimal:
        return (self.original_annual_price
                - self.total_landlord_discount
                - self.total_uhomes_subsidy)

    @property
    def final_weekly_price(self) -> Decimal:
        if self.property.weeks > 0:
            return self.final_annual_price / self.property.weeks
        return Decimal(0)

    @property
    def total_savings(self) -> Decimal:
        return (self.total_landlord_discount
                + self.total_uhomes_subsidy
                + self.total_gifts_value)

    @property
    def savings_rate(self) -> float:
        if self.original_annual_price > 0:
            return float(self.total_savings / self.original_annual_price * 100)
        return 0.0

    @property
    def lowest_competitor_price(self) -> Optional[Decimal]:
        if not self.competitor_prices:
            return None
        return min(cp.annual_price for cp in self.competitor_prices)

    @property
    def advantage_vs_competitor(self) -> Optional[Decimal]:
        lowest = self.lowest_competitor_price
        if lowest is None:
            return None
        return lowest - self.final_annual_price

    @property
    def advantage_rate(self) -> Optional[float]:
        lowest = self.lowest_competitor_price
        advantage = self.advantage_vs_competitor
        if lowest is None or advantage is None or lowest == 0:
            return None
        return float(advantage / lowest * 100)


# ========== 创建示例数据 ==========

def create_sample_quote():
    """创建示例报价单数据"""

    # 房源信息
    property_info = PropertyInfo(
        property_name="iQ Shoreditch",
        room_type="Bronze Studio",
        address="2 Silicon Way, London N1 6AT",
        lease_start=date(2026, 9, 1),
        lease_end=date(2027, 8, 31),
    )

    # 房东优惠
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

    # 异乡补贴
    uhomes_subsidies = [
        Discount(
            name="平台补贴价格 (£24/周)",
            amount=Decimal("1224"),
            payer=DiscountPayer.UHOMES,
            description="异乡好居平台价格优惠"
        ),
        Discount(
            name="老客户返现",
            amount=Decimal("830"),
            payer=DiscountPayer.UHOMES,
            description="签约后7-10个工作日到账"
        ),
    ]

    # 礼品
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

    # 竞对价格
    competitor_prices = [
        CompetitorPrice(
            platform="Awehome",
            weekly_price=Decimal("428"),
            annual_price=Decimal("21828"),
        ),
        CompetitorPrice(
            platform="Amber Student",
            weekly_price=Decimal("414"),
            annual_price=Decimal("21114"),
        ),
    ]

    # 顾问信息
    advisor = AdvisorInfo(
        name="张顾问",
        wechat_id="uhomes_zhang",
        phone="+44 7700 900123"
    )

    # 创建报价单
    quote = QuoteData(
        property=property_info,
        original_weekly_price=Decimal("438"),
        original_annual_price=Decimal("22338"),
        landlord_discounts=landlord_discounts,
        uhomes_subsidies=uhomes_subsidies,
        selected_gifts=selected_gifts,
        competitor_prices=competitor_prices,
        valid_until=date.today() + timedelta(days=7),
        advisor=advisor,
    )

    return quote


# ========== 生成HTML ==========

def generate_html(quote: QuoteData) -> str:
    """生成HTML报价单"""

    # 读取模板（使用微信版）
    template_file = "pricelist-quote-wechat.html"
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"❌ 模板文件未找到: {template_file}")
        # 回退到1024×768版
        template_file = "pricelist-quote-1024x768.html"
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                template_content = f.read()
        except FileNotFoundError:
            # 再回退到紧凑版
            template_file = "pricelist-quote-compact.html"
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_content = f.read()
            except FileNotFoundError:
                return None

    # 创建Jinja2环境并添加自定义过滤器
    from jinja2 import Environment
    env = Environment()

    # 添加格式化过滤器
    def format_number(value, with_comma=True):
        """格式化数字"""
        if value is None:
            return "0"
        try:
            num = float(value)
            if with_comma:
                return f"{num:,.0f}"
            else:
                return f"{num:.0f}"
        except:
            return str(value)

    env.filters['format_num'] = format_number

    template = env.from_string(template_content)

    # 准备数据（将Decimal转为float，方便模板格式化）
    data = {
        "property": quote.property,
        "original_weekly_price": float(quote.original_weekly_price),
        "original_annual_price": float(quote.original_annual_price),
        "final_weekly_price": float(quote.final_weekly_price),
        "final_annual_price": float(quote.final_annual_price),
        "landlord_discounts": quote.landlord_discounts,
        "uhomes_subsidies": quote.uhomes_subsidies,
        "total_landlord_discount": float(quote.total_landlord_discount),
        "total_uhomes_subsidy": float(quote.total_uhomes_subsidy),
        "selected_gifts": quote.selected_gifts,
        "total_gifts_value": float(quote.total_gifts_value),
        "competitor_prices": quote.competitor_prices,
        "advantage_vs_competitor": float(quote.advantage_vs_competitor) if quote.advantage_vs_competitor else None,
        "advantage_rate": quote.advantage_rate,
        "total_savings": float(quote.total_savings),
        "savings_rate": quote.savings_rate,
        "valid_until": quote.valid_until.strftime('%Y-%m-%d'),
        "advisor": quote.advisor,
    }

    return template.render(**data)


# ========== 主程序 ==========

if __name__ == "__main__":
    print("=" * 70)
    print("  pricelist - 异乡好居销售报价单系统 - 演示程序")
    print("=" * 70)
    print()

    # 创建示例报价单
    print("📋 创建示例报价单...")
    quote = create_sample_quote()

    # 输出关键信息
    print()
    print("✅ 报价单数据:")
    print(f"  房源: {quote.property.property_name}")
    print(f"  户型: {quote.property.room_type}")
    print(f"  租期: {quote.property.lease_period_text}")
    print()
    print(f"  原价: £{quote.original_annual_price:,.0f}/年 (£{quote.original_weekly_price}/周)")
    print()
    print(f"  房东优惠: £{quote.total_landlord_discount:,.0f}")
    for d in quote.landlord_discounts:
        print(f"    - {d.name}: £{d.amount}")
    print()
    print(f"  异乡补贴: £{quote.total_uhomes_subsidy:,.0f}")
    for s in quote.uhomes_subsidies:
        print(f"    - {s.name}: £{s.amount}")
    print()
    print(f"  礼品价值: £{quote.total_gifts_value:,.0f}")
    for g in quote.selected_gifts:
        print(f"    - {g.icon} {g.name}: £{g.value}")
    print()
    print(f"  📊 到手价: £{quote.final_annual_price:,.0f}/年 (£{quote.final_weekly_price:.0f}/周)")
    print(f"  💰 总节省: £{quote.total_savings:,.0f} ({quote.savings_rate:.1f}%)")
    print()
    if quote.advantage_vs_competitor:
        print(f"  🏆 比竞对低: £{quote.advantage_vs_competitor:,.0f} ({quote.advantage_rate:.1f}%)")
    print()

    # 生成HTML
    print("=" * 70)
    print("📝 生成HTML报价单...")
    html_content = generate_html(quote)

    if html_content:
        # 保存文件
        output_file = "pricelist_报价单_iQ_Shoreditch.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ HTML已生成: {output_file}")
        print()
        print("🌐 请在浏览器中打开查看:")
        print(f"  open {output_file}")
        print()
        print("或者直接双击文件在浏览器中打开")
    else:
        print("❌ HTML生成失败")

    print()
    print("=" * 70)
    print("✅ 演示完成！")
    print("=" * 70)
    print()
    print("💡 提示:")
    print("  - 生成的HTML文件适合微信分享（750px宽度）")
    print("  - 可以截图或打印为PDF发送给客户")
    print("  - 修改模板文件可以调整样式")
    print()
