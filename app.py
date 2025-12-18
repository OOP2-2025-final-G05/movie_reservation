from flask import Flask, render_template
from datetime import datetime
from collections import defaultdict
from peewee import fn

# モデルとルートのインポート
from models import initialize_database
from models.product import Product
from models.order import Order
from routes import blueprints

app = Flask(__name__)

# データベースの初期化
initialize_database()

# Blueprint登録
for bp in blueprints:
    app.register_blueprint(bp)

@app.route('/')
def index():
    # --- 1. 今月の映画別売上集計（割引後価格反映） ---
    today = datetime.today()
    start_of_month = datetime(today.year, today.month, 1)

    sales_dict = defaultdict(int)
    # 注文データから今月分を取得
    orders = Order.select().where(Order.order_date >= start_of_month)
    for o in orders:
        sales_dict[o.product.name] += o.get_discounted_price()

    sales_labels = list(sales_dict.keys())
    sales_values = list(sales_dict.values())

    # --- 2. 映画ごとの予約人数集計（全期間） ---
    count_query = (
        Product
        .select(Product.name, fn.COUNT(Order.id).alias('count'))
        .join(Order)
        .group_by(Product.name)
    )

    count_labels = []
    count_values = []
    for row in count_query:
        count_labels.append(row.name)
        count_values.append(row.count)

    return render_template(
        'index.html',
        sales_labels=sales_labels,
        sales_values=sales_values,
        count_labels=count_labels,
        count_values=count_values
    )

if __name__ == '__main__':
    # 両方の設定を考慮（ポート指定が必要な場合はこちらを使用）
    app.run(host='0.0.0.0', port=8080, debug=True)