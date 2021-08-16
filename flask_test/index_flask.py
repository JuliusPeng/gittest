from flask import Flask


app = Flask(__name__)


@app.route('/')
def index()
    """the First page"""
    return 'The Flask Framwork Learning'


if __name__ = "__main__":
    """Start flask framework"""
    app.run(debug=True)

