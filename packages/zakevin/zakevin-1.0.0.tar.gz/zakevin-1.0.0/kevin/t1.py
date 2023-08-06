import json


def generate_tree(source, parent):
    tree = []
    for item in source:

        if item["parent"] == parent:
            item["child"] = generate_tree(source, item["id"])
            tree.append(item)
    return tree


if __name__ == '__main__':
    with open("./area_base1.json", 'r', encoding='utf8') as f:
        load_dict = json.load(f)['RECORDS']
    permission_tree = generate_tree(load_dict, "0")
    print(json.dumps(permission_tree, ensure_ascii=False))
