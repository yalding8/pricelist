"""
品牌配置模块
包含异乡好居的品牌规范、颜色、Logo等
"""

# 品牌主色
BRAND_PRIMARY_COLOR = "#FF5A5F"  # 珊瑚红
BRAND_PRIMARY_RGB = (255, 90, 95)
BRAND_PRIMARY_CMYK = (0, 78, 51, 0)

# 辅助色
BRAND_SECONDARY_COLORS = {
    "light_red": "#FFE5E5",     # 浅红色背景
    "dark_red": "#E54850",       # 深红色
    "gray": "#666666",           # 文字灰色
    "light_gray": "#F8F9FA",     # 浅灰色背景
    "border_gray": "#F0F0F0",    # 边框灰色
    "success_green": "#4CAF50",  # 成功绿色（优惠金额）
    "warning_yellow": "#FFF3CD", # 警告黄色（最终价格背景）
}

# 品牌文本
BRAND_NAME_CN = "异乡好居"
BRAND_NAME_EN = "Uhomes"
BRAND_SLOGAN_CN = "留学生海外的家"
BRAND_SLOGAN_EN = "Your Home Away From Home"

# Logo配置
LOGO_TEXT = "异乡好居"  # 纯文字Logo（如无图片资源）
LOGO_URL = ""  # Logo图片URL（如有）
LOGO_HEIGHT = 36  # Logo高度（px）

# 字体配置
FONTS = {
    "primary_cn": "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
    "primary_en": "'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif",
    "mono": "'SF Mono', 'Consolas', 'Monaco', monospace",
}

# 报价单设计规范
QUOTE_CARD_DESIGN = {
    # 尺寸
    "width": 750,               # 宽度（px）适配微信查看
    "max_width": 750,
    "padding": 24,
    "border_radius": 16,

    # 头部
    "header_padding": 32,
    "header_bg": f"linear-gradient(135deg, {BRAND_PRIMARY_COLOR} 0%, #764ba2 100%)",

    # 字体大小
    "font_size_h1": 24,
    "font_size_h2": 18,
    "font_size_h3": 16,
    "font_size_body": 15,
    "font_size_small": 14,
    "font_size_tiny": 13,

    # 间距
    "section_padding": 24,
    "item_spacing": 12,

    # 圆角
    "card_radius": 16,
    "group_radius": 12,
    "badge_radius": 4,

    # 阴影
    "card_shadow": "0 4px 20px rgba(0,0,0,0.1)",
}

# 结算方标签配置
PAYER_BADGES = {
    "landlord": {
        "text": "由房东结算",
        "bg_color": "#E3F2FD",
        "text_color": "#1976D2",
        "icon": "💳",
    },
    "uhomes": {
        "text": "由异乡好居结算",
        "bg_color": "#FFE5E5",
        "text_color": BRAND_PRIMARY_COLOR,
        "icon": "🎁",
    },
}

# 礼品类别配置
GIFT_CATEGORIES = {
    "cash": {
        "name": "现金类",
        "color": "#4CAF50",
        "icon": "💵",
    },
    "service": {
        "name": "服务类",
        "color": "#2196F3",
        "icon": "✈️",
    },
    "voucher": {
        "name": "优惠券",
        "color": "#FF9800",
        "icon": "💳",
    },
    "gift": {
        "name": "实物礼品",
        "color": "#E91E63",
        "icon": "🎁",
    },
}

# 微信分享配置
WECHAT_SHARE = {
    "image_width": 750,
    "image_quality": 90,        # PNG质量
    "max_file_size_mb": 2,      # 最大文件大小（微信限制）
}

# 报价单有效期配置
QUOTE_VALIDITY = {
    "default_days": 7,          # 默认有效期7天
    "max_days": 30,             # 最长有效期30天
}

# CSS变量（用于HTML模板）
def get_css_variables() -> str:
    """生成CSS变量声明"""
    return f"""
:root {{
    /* 品牌色 */
    --brand-primary: {BRAND_PRIMARY_COLOR};
    --brand-light-red: {BRAND_SECONDARY_COLORS['light_red']};
    --brand-dark-red: {BRAND_SECONDARY_COLORS['dark_red']};

    /* 功能色 */
    --color-gray: {BRAND_SECONDARY_COLORS['gray']};
    --color-light-gray: {BRAND_SECONDARY_COLORS['light_gray']};
    --color-border: {BRAND_SECONDARY_COLORS['border_gray']};
    --color-success: {BRAND_SECONDARY_COLORS['success_green']};
    --color-warning: {BRAND_SECONDARY_COLORS['warning_yellow']};

    /* 字体 */
    --font-primary: {FONTS['primary_cn']};

    /* 尺寸 */
    --card-width: {QUOTE_CARD_DESIGN['width']}px;
    --card-padding: {QUOTE_CARD_DESIGN['padding']}px;
    --border-radius: {QUOTE_CARD_DESIGN['border_radius']}px;

    /* 字号 */
    --font-h1: {QUOTE_CARD_DESIGN['font_size_h1']}px;
    --font-h2: {QUOTE_CARD_DESIGN['font_size_h2']}px;
    --font-h3: {QUOTE_CARD_DESIGN['font_size_h3']}px;
    --font-body: {QUOTE_CARD_DESIGN['font_size_body']}px;
    --font-small: {QUOTE_CARD_DESIGN['font_size_small']}px;

    /* 阴影 */
    --card-shadow: {QUOTE_CARD_DESIGN['card_shadow']};
}}
"""

# 导出配置字典
BRAND_CONFIG = {
    "colors": {
        "primary": BRAND_PRIMARY_COLOR,
        **BRAND_SECONDARY_COLORS,
    },
    "names": {
        "cn": BRAND_NAME_CN,
        "en": BRAND_NAME_EN,
        "slogan_cn": BRAND_SLOGAN_CN,
        "slogan_en": BRAND_SLOGAN_EN,
    },
    "logo": {
        "text": LOGO_TEXT,
        "url": LOGO_URL,
        "height": LOGO_HEIGHT,
    },
    "design": QUOTE_CARD_DESIGN,
    "payer_badges": PAYER_BADGES,
    "gift_categories": GIFT_CATEGORIES,
    "wechat": WECHAT_SHARE,
    "validity": QUOTE_VALIDITY,
}
