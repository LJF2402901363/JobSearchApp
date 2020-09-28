from Util.JsonUtil import JsonUtil
import json
if __name__ == '__main__':
    json_obj = json.load(open("static/json/urlSettingPro.json", mode="r", encoding="utf8"))
    print(json_obj)