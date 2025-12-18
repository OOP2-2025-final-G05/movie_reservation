from flask import Flask, render_template
from routes import blueprints
from models import Order
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# Blueprint登録
for bp in blueprints:
    app.register_blueprint(bp)

@app.route('/')
def index():
    # 今月の開始日
    today = datetime.today()
    start_of_month = datetime(today.year, today.month, 1)

    # 今月の映画別売上を Python 側で集計（割引後価格反映）
    sales_dict = defaultdict(int)
    orders = Order.select().where(Order.order_date >= start_of_month)
    for o in orders:
        sales_dict[o.product.name] += o.get_discounted_price()

    labels = list(sales_dict.keys())
    sales  = list(sales_dict.values())

    return render_template('index.html', labels=labels, sales=sales)


if __name__ == '__main__':
    app.run(debug=True)
