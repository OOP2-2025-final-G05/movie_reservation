from flask import Flask, render_template
from models import initialize_database, Order
from routes import blueprints
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    now_year = datetime.now().year
    monthly_sales = defaultdict(int)

    for order in Order.select():
        if order.order_date.year == now_year:
            month = order.order_date.strftime('%Y-%m')
            monthly_sales[month] += int(order.get_discounted_price())

    # 月順に並べる
    labels = sorted(monthly_sales.keys())
    values = [monthly_sales[m] for m in labels]

    return render_template(
        'index.html',
        labels=labels,
        values=values
    )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
