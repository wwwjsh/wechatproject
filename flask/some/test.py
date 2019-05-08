def decorator(func):
    def app(n1):
       return func(n1=2*n1)
    return app

@decorator
def decoratded(n1):
    return n1**2
a = "[{'date': [2019, 5, 5], 'objs': [{'start_time': [14, 0], 'obj': [{'obj_id': 179, 'obj_name': '三号场', 'minOrd_time': 60, 'residue': 30}, {'obj_id': 182, 'obj_name': '四号场', 'minOrd_time': 60, 'residue': 30}]}, {'start_time': [15, 0], 'obj': [{'obj_id': 180, 'obj_name': '三号场', 'minOrd_time': 60, 'residue': 30}, {'obj_id': 183, 'obj_name': '四号场', 'minOrd_time': 60, 'residue': 30}]}, {'start_time': [16, 0], 'obj': [{'obj_id': 181, 'obj_name': '三号场', 'minOrd_time': 60, 'residue': 30}, {'obj_id': 184, 'obj_name': '四号场', 'minOrd_time': 60, 'residue': 30}]}]}, {'date': [2019, 5, 6], 'objs': [{'start_time': [15, 0], 'obj': [{'obj_id': 185, 'obj_name': '三号场', 'minOrd_time': 60, 'residue': 30}, {'obj_id': 188, 'obj_name': '四号场', 'minOrd_time': 60, 'residue': 30}]}, {'start_time': [16, 0], 'obj': [{'obj_id': 186, 'obj_name': '三号场', 'minOrd_time': 60, 'residue': 30}, {'obj_id': 189, 'obj_name': '四号场', 'minOrd_time': 60, 'residue': 30}]}, {'start_time': [17, 0], 'obj': [{'obj_id': 187, 'obj_name': '三号场', 'minOrd_time': 60, 'residue': 30}, {'obj_id': 190, 'obj_name': '四号场', 'minOrd_time': 60, 'residue': 30}]}]}]"
print(len(a))