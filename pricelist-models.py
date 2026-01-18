"""
核心数据模型
定义报价单系统中所有的数据结构
"""

from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal
from datetime import date, timedelta
from enum import Enum


class DiscountPayer(Enum):
    """结算方"""
    LANDLORD = "landlord"  # 房东结算
    UHOMES = "uhomes"      # 异乡好居结算


class GiftCategory(Enum):
    """礼品类别"""
    CASH = "cash"          # 现金
    SERVICE = "service"    # 服务
    VOUCHER = "voucher"    # 优惠券
    GIFT = "gift"          # 实物礼品


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
        """租期周数"""
        days = (self.lease_end - self.lease_start).days
        return max(1, days // 7)  # 至少1周

    @property
    def lease_period_text(self) -> str:
        """租期文本"""
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
        """类型转换"""
        if isinstance(self.amount, (int, float)):
            self.amount = Decimal(str(self.amount))
        if isinstance(self.payer, str):
            self.payer = DiscountPayer(self.payer)

    @property
    def payer_text(self) -> str:
        """结算方文本"""
        return "由房东结算" if self.payer == DiscountPayer.LANDLORD else "由异乡好居结算"

    @property
    def payer_badge_type(self) -> str:
        """结算方标签类型（用于CSS）"""
        return self.payer.value


@dataclass
class Gift:
    """礼品库礼品"""
    id: str
    name: str
    value: Decimal
    category: GiftCategory
    description: str = ""
    icon: str = "🎁"
    unit: str = "GBP"
    sort_order: int = 999
    is_free: bool = False  # 是否免费礼品（价值为0）

    def __post_init__(self):
        """类型转换"""
        if isinstance(self.value, (int, float)):
            self.value = Decimal(str(self.value))
        if isinstance(self.category, str):
            self.category = GiftCategory(self.category)

    @property
    def display_value(self) -> str:
        """显示价值"""
        if self.is_free:
            return "免费"
        return f"£{self.value}"

    @property
    def category_name(self) -> str:
        """类别名称"""
        category_names = {
            GiftCategory.CASH: "现金类",
            GiftCategory.SERVICE: "服务类",
            GiftCategory.VOUCHER: "优惠券",
            GiftCategory.GIFT: "实物礼品",
        }
        return category_names.get(self.category, "其他")


@dataclass
class CompetitorPrice:
    """竞对价格"""
    platform: str
    weekly_price: Decimal
    annual_price: Decimal
    url: Optional[str] = None

    def __post_init__(self):
        """类型转换"""
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
        """头像首字母"""
        return self.name[0] if self.name else "?"


@dataclass
class QuoteData:
    """完整报价单数据"""
    # 房源信息
    property: PropertyInfo

    # 价格信息
    original_weekly_price: Decimal
    original_annual_price: Decimal

    # 优惠信息
    landlord_discounts: List[Discount] = field(default_factory=list)
    uhomes_subsidies: List[Discount] = field(default_factory=list)

    # 礼品库（新增）
    selected_gifts: List[Gift] = field(default_factory=list)

    # 竞对信息
    competitor_prices: List[CompetitorPrice] = field(default_factory=list)

    # 元信息
    valid_until: Optional[date] = None
    advisor: Optional[AdvisorInfo] = None
    created_at: date = field(default_factory=date.today)

    def __post_init__(self):
        """初始化后处理"""
        # 类型转换
        if isinstance(self.original_weekly_price, (int, float)):
            self.original_weekly_price = Decimal(str(self.original_weekly_price))
        if isinstance(self.original_annual_price, (int, float)):
            self.original_annual_price = Decimal(str(self.original_annual_price))

        # 如果没有设置有效期，默认7天
        if self.valid_until is None:
            self.valid_until = date.today() + timedelta(days=7)

    # ========== 计算属性 ==========

    @property
    def total_landlord_discount(self) -> Decimal:
        """房东优惠总额"""
        return sum(d.amount for d in self.landlord_discounts)

    @property
    def total_uhomes_subsidy(self) -> Decimal:
        """异乡补贴总额"""
        return sum(s.amount for s in self.uhomes_subsidies)

    @property
    def total_gifts_value(self) -> Decimal:
        """礼品总价值"""
        return sum(g.value for g in self.selected_gifts)

    @property
    def final_annual_price(self) -> Decimal:
        """最终年租金（到手价）"""
        return (self.original_annual_price
                - self.total_landlord_discount
                - self.total_uhomes_subsidy)

    @property
    def final_weekly_price(self) -> Decimal:
        """最终周租金"""
        if self.property.weeks > 0:
            return self.final_annual_price / self.property.weeks
        return Decimal(0)

    @property
    def total_savings(self) -> Decimal:
        """总节省金额（优惠 + 礼品）"""
        return (self.total_landlord_discount
                + self.total_uhomes_subsidy
                + self.total_gifts_value)

    @property
    def savings_rate(self) -> float:
        """优惠比例"""
        if self.original_annual_price > 0:
            return float(self.total_savings / self.original_annual_price * 100)
        return 0.0

    @property
    def lowest_competitor_price(self) -> Optional[Decimal]:
        """竞对最低价"""
        if not self.competitor_prices:
            return None
        return min(cp.annual_price for cp in self.competitor_prices)

    @property
    def advantage_vs_competitor(self) -> Optional[Decimal]:
        """相比竞对的优势金额"""
        lowest = self.lowest_competitor_price
        if lowest is None:
            return None
        return lowest - self.final_annual_price

    @property
    def advantage_rate(self) -> Optional[float]:
        """相比竞对的优势比例"""
        lowest = self.lowest_competitor_price
        advantage = self.advantage_vs_competitor
        if lowest is None or advantage is None or lowest == 0:
            return None
        return float(advantage / lowest * 100)

    # ========== 分组方法 ==========

    def get_gifts_by_category(self, category: GiftCategory) -> List[Gift]:
        """按类别获取礼品"""
        return [g for g in self.selected_gifts if g.category == category]

    @property
    def cash_gifts(self) -> List[Gift]:
        """现金类礼品"""
        return self.get_gifts_by_category(GiftCategory.CASH)

    @property
    def service_gifts(self) -> List[Gift]:
        """服务类礼品"""
        return self.get_gifts_by_category(GiftCategory.SERVICE)

    @property
    def voucher_gifts(self) -> List[Gift]:
        """优惠券类礼品"""
        return self.get_gifts_by_category(GiftCategory.VOUCHER)

    @property
    def physical_gifts(self) -> List[Gift]:
        """实物礼品"""
        return self.get_gifts_by_category(GiftCategory.GIFT)

    # ========== 格式化方法 ==========

    def format_price(self, price: Decimal, with_symbol: bool = True) -> str:
        """格式化价格"""
        price_str = f"{price:,.0f}" if price % 1 == 0 else f"{price:,.2f}"
        return f"£{price_str}" if with_symbol else price_str

    def format_percentage(self, value: float, decimals: int = 1) -> str:
        """格式化百分比"""
        return f"{value:.{decimals}f}%"

    # ========== 验证方法 ==========

    def validate(self) -> List[str]:
        """验证数据完整性，返回错误列表"""
        errors = []

        if self.original_annual_price <= 0:
            errors.append("原价必须大于0")

        if self.final_annual_price < 0:
            errors.append("最终价格不能为负数（优惠过大）")

        if self.property.lease_start >= self.property.lease_end:
            errors.append("租期开始日期必须早于结束日期")

        if self.valid_until and self.valid_until < date.today():
            errors.append("报价单有效期不能早于今天")

        return errors

    def is_valid(self) -> bool:
        """是否有效"""
        return len(self.validate()) == 0

    # ========== 导出方法 ==========

    def to_dict(self) -> dict:
        """转换为字典（用于JSON序列化）"""
        return {
            "property": {
                "property_name": self.property.property_name,
                "room_type": self.property.room_type,
                "address": self.property.address,
                "lease_start": self.property.lease_start.isoformat(),
                "lease_end": self.property.lease_end.isoformat(),
                "weeks": self.property.weeks,
            },
            "prices": {
                "original_weekly": float(self.original_weekly_price),
                "original_annual": float(self.original_annual_price),
                "final_weekly": float(self.final_weekly_price),
                "final_annual": float(self.final_annual_price),
            },
            "discounts": {
                "landlord": [
                    {
                        "name": d.name,
                        "amount": float(d.amount),
                        "description": d.description,
                    }
                    for d in self.landlord_discounts
                ],
                "uhomes": [
                    {
                        "name": s.name,
                        "amount": float(s.amount),
                        "description": s.description,
                    }
                    for s in self.uhomes_subsidies
                ],
                "total": float(self.total_savings),
            },
            "gifts": [
                {
                    "id": g.id,
                    "name": g.name,
                    "value": float(g.value),
                    "category": g.category.value,
                    "icon": g.icon,
                }
                for g in self.selected_gifts
            ],
            "competitors": [
                {
                    "platform": cp.platform,
                    "weekly_price": float(cp.weekly_price),
                    "annual_price": float(cp.annual_price),
                }
                for cp in self.competitor_prices
            ],
            "summary": {
                "total_savings": float(self.total_savings),
                "savings_rate": round(self.savings_rate, 2),
                "advantage_vs_competitor": float(self.advantage_vs_competitor) if self.advantage_vs_competitor else None,
                "advantage_rate": round(self.advantage_rate, 2) if self.advantage_rate else None,
            },
            "meta": {
                "created_at": self.created_at.isoformat(),
                "valid_until": self.valid_until.isoformat() if self.valid_until else None,
                "advisor": {
                    "name": self.advisor.name,
                    "wechat_id": self.advisor.wechat_id,
                    "phone": self.advisor.phone,
                } if self.advisor else None,
            },
        }


# ========== 工厂方法 ==========

def create_quote_from_dict(data: dict) -> QuoteData:
    """从字典创建报价单（用于API请求）"""
    property_info = PropertyInfo(
        property_name=data["property"]["property_name"],
        room_type=data["property"]["room_type"],
        address=data["property"]["address"],
        lease_start=date.fromisoformat(data["property"]["lease_start"]),
        lease_end=date.fromisoformat(data["property"]["lease_end"]),
    )

    landlord_discounts = [
        Discount(
            name=d["name"],
            amount=Decimal(str(d["amount"])),
            payer=DiscountPayer.LANDLORD,
            description=d.get("description", ""),
        )
        for d in data.get("landlord_discounts", [])
    ]

    uhomes_subsidies = [
        Discount(
            name=s["name"],
            amount=Decimal(str(s["amount"])),
            payer=DiscountPayer.UHOMES,
            description=s.get("description", ""),
        )
        for s in data.get("uhomes_subsidies", [])
    ]

    # ... 其他字段省略，根据实际需求完善

    return QuoteData(
        property=property_info,
        original_weekly_price=Decimal(str(data["original_weekly_price"])),
        original_annual_price=Decimal(str(data["original_annual_price"])),
        landlord_discounts=landlord_discounts,
        uhomes_subsidies=uhomes_subsidies,
        # ... 其他字段
    )
