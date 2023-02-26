from flask import Flask

app = Flask(__name__)

product_list = [
    ["1", "ノートパソコンA", "Core i5", "￥68,500"],
    ["2", "ノートパソコンB", "AMD Ryzen 5", "￥81,300"],
    ["3", "ノートパソコンC", "CeleronN4020", "￥64,300"]
]

@app.route('/')
def index():
    return '<h1>Product Page</h1>'


@app.route('/product/<product_id>')
def product(product_id):
    res = ''
    if product_id == '1':
        res = "Product Name : {} <br>CPU : {} <br>Price : {}".format(product_list[0][1], product_list[0][2], product_list[0][3])
    elif product_id == '2':
        res = "Product Name : {} <br>CPU : {} <br>Price : {}".format(product_list[1][1], product_list[1][2], product_list[1][3])
    else:
        res = "Product Name : {} <br>CPU : {} <br>Price : {}".format(product_list[2][1], product_list[2][2], product_list[2][3])
      
    return "<h4>{}</h4>".format(res)


if __name__ == '__main__':
    app.run(debug=True)