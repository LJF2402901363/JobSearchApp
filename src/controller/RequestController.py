from flask import Flask, request
from flask_cors import *
from service.RequestService import RequestService

app = Flask(__name__)
# 解决跨域请求资源被拦截问题
CORS(app, supports_credentials=True, resources=r"/*")
requestService = RequestService()


@app.route('/search', methods=['POST'])
def search():
    # 获取搜索框的内容
    searchContent = request.values.get("searchContent")
    # 获取省文  本
    province = request.values.get("province")
    # 获市文本
    city = request.values.get("city")
    # 调用业务逻辑进行处理
    jsonStr = requestService.handleSearchByThread(searchContent, province, city)
    return jsonStr


if __name__ == '__main__':
    app.run(debug=True)
