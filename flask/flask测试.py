from flask import Flask, json, request
app = Flask(__name__)


@app.route('/launchActivity',methods=['POST'])
def lau_item():
    lau_usId = str(json.loads(request.values.get("lau_usId")))
    item_name = str(json.loads(request.values.get("item_name")))
    item_type = str(json.loads(request.values.get("item_type")))
    contacts = str(json.loads(request.values.get("contacts")))
    start_time = str(json.loads(request.values.get("start_time")))
    end_time = str(json.loads(request.values.get("end_time")))
    item_address = str(json.loads(request.values.get("item_address")))
    text_info = str(json.loads(request.values.get("text_info")))
    ord_objects = str(json.loads(request.values.get("ord_objects")))
    return "ok"
if __name__ == "__main__":
    app.run()

