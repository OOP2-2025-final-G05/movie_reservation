from flask import Flask, render_template
from datetime import datetime
from collections import defaultdict
from peewee import fn

# モデルとルートのインポート
from models import initialize_database, Order
from models.product import Product
from routes import blueprints

app = Flask(__name__)

# データベースの初期化
initialize_database()

for bp in blueprints:
    app.register_blueprint(bp)

@app.route('/')
def index():
    now = datetime.now()
    
    # 1. 月別の売上推移 (折れ線)
    monthly_trend = defaultdict(int)
    for order in Order.select():
        if order.order_date.year == now.year:
            month_key = order.order_date.strftime('%Y-%m')
            monthly_trend[month_key] += int(order.get_discounted_price())
    trend_labels = sorted(monthly_trend.keys())
    trend_values = [monthly_trend[m] for m in trend_labels]

    # 2. 今月の映画別売上 (横棒)
    start_of_month = datetime(now.year, now.month, 1)
    sales_dict = defaultdict(int)
    current_month_orders = Order.select().where(Order.order_date >= start_of_month)
    for o in current_month_orders:
        sales_dict[o.product.name] += o.get_discounted_price()
    movie_sales_labels = list(sales_dict.keys())
    movie_sales_values = list(sales_dict.values())

    # 3. 映画ごとの予約人数 (円)
    count_query = (
        Product.select(Product.name, fn.COUNT(Order.id).alias('count'))
        .join(Order).group_by(Product.name)
    )
    count_labels = [row.name for row in count_query]
    count_values = [row.count for row in count_query]

    return render_template(
        'index.html',
        trend_labels=trend_labels,
        trend_values=trend_values,
        movie_sales_labels=movie_sales_labels,
        movie_sales_values=movie_sales_values,
        count_labels=count_labels,
        count_values=count_values
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)