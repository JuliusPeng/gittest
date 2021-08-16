from flask import Flask


app = Flask(__name__)


def test_git():
    """test函数"""
    # Zhangsan operation
    num = 1

    # Manager operation
    num1 = 2


@app.route('/')
def index()
    """the First page"""
    return 'The Flask Framwork Learning'


if __name__ = "__main__":
    """Start flask framework"""
    app.run(debug=True)

