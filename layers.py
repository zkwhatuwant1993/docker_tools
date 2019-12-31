import sys
import json
from io import StringIO
import hashlib


def to_layer_ids(layers):
    layer_ids = []
    for index in range(len(layers)):
        if index == 0:
            layer_ids.append(layers[0])
        else:
            layer_ids.append(sha256(layer_ids[index-1] + " " + layers[index]))
    return layer_ids


def sha256(value):
    m = hashlib.sha256()
    m.update(value.encode("utf-8"))
    return "sha256:" + m.hexdigest()


def parse_image_diff_ids():
    in_put = StringIO()
    for line in sys.stdin:
        in_put.write(line)
        # print(line)
    try:
        json_info = json.loads(in_put.getvalue())
        if isinstance(json_info, list):
            json_info = json_info[0]
        layers = json_info['RootFS']['Layers']
        return to_layer_ids(layers)
    finally:
        in_put.close()


if __name__ == "__main__":
    print(parse_image_diff_ids())
