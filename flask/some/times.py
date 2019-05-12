import time
import datetime
from methods import DateEncoder,json
start_time = "2012-1-1 17:00"
times = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
json_time = json.dumps(times, cls=DateEncoder)
adict = {'start_time': json_time}
print(type(json.loads(json_time))) #字符串类型
json_loadtime = json.loads(json_time)
json_adict = json.dumps(adict)
print(json_adict)
print(json.loads(json_adict)['start_time'])

import json
import datetime
import dateutil.parser
import decimal

CONVERTERS = {
    'datetime': dateutil.parser.parse,
    'decimal': decimal.Decimal,
}


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime,)):
            return {"val": obj.isoformat(), "_spec_type": "datetime"}
        elif isinstance(obj, (decimal.Decimal,)):
            return {"val": str(obj), "_spec_type": "decimal"}
        else:
            return super().default(obj)


def object_hook(obj):
    _spec_type = obj.get('_spec_type')
    if not _spec_type:
        return obj

    if _spec_type in CONVERTERS:
        return CONVERTERS[_spec_type](obj['val'])
    else:
        raise Exception('Unknown {}'.format(_spec_type))


def main():
    data = {
        "hello": "world",
        "thing": datetime.datetime.now(),
        "other": decimal.Decimal(0)
    }
    thing = json.dumps(data, cls=MyJSONEncoder)

    print(json.loads(thing, object_hook=object_hook))

if __name__ == '__main__':
  main()    {{(item.end_time[3] < 10)?('0' + item.end_time[3]): (item.end_time[3]) + ':'}}
    {{(item.end_time[4] < 10)?('0' + item.end_time[4]): (item.end_time[4])