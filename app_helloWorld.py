from flask import Flask
from flask import request, jsonify
from string_convert import msg2msg
from config import config 
from app import create_app

cfg = config['test']

# app = Flask(__name__)
app = create_app(cfg)

@app.route('/', methods=['GET','POST'])
def hello():
    return 'Hello, Flask!'


if __name__ == '__main__':
    # 允许服务器被公开访问
    # app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    app.run(debug=cfg.APP_DEBUG, host=cfg.APP_HOST, port=cfg.APP_PORT, threaded=cfg.APP_THREADED)