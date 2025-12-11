from peewee import Model, ForeignKeyField, DateTimeField
from decimal import Decimal
from .db import db
from .user import User
from .product import Product

class Order(Model):
    user = ForeignKeyField(User, backref='orders')
    product = ForeignKeyField(Product, backref='orders')
    order_date = DateTimeField()

    # ▼ ここから追加する ▼
    def get_discounted_price(self):
        age = self.user.age
        price = self.product.price   # Decimal

        # 12歳以下 → 半額（Decimalで計算）
        if age <= 12:
            discounted = price * Decimal('0.5')
            return discounted.quantize(Decimal('1'))  # 整数に丸める

        # 65歳以上 → 500円引き（Decimal 同士で計算）
        if age >= 65:
            discounted = price - Decimal('500')
            if discounted < 0:
                discounted = Decimal('0')
            return discounted

        # 通常
        return price
    # ▲ 追加ここまで ▲

    class Meta:
        database = db
