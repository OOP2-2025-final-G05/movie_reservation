from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from models.product import Product
from models.order import Order
from peewee import fn

app = Flask(__name__)

initialize_database()

for blueprint in blueprints:
    app.register_blueprint(blueprint)

@app.route('/')
def index():
    # 映画ごとの注文数（＝見た人数）を集計
    query = (
        Product
        .select(Product.name, fn.COUNT(Order.id).alias('count'))
        .join(Order)
        .group_by(Product.name)
    )

    labels = []
    data = []

    for row in query:
        labels.append(row.name)
        data.append(row.count)

    return render_template(
        'index.html',
        labels=labels,
        data=data
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)