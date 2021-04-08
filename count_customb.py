import json
import pymongo
from os import listdir
from os.path import isfile, join
import sys
import os

mypath = "./projects_sb3/"
new_path = "./sb3/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print("TEST FILES", onlyfiles[0])

db = pymongo.MongoClient(host="f-l2108-pc01.aulas.etsit.urjc.es", port=21000)
db = db["ct"]
col_custom = db["customblocks"]

#filename = "490319019.json"
for filename in onlyfiles:
    try:
        json_project = json.loads(open(mypath + filename, encoding="utf-8").read())
        list_customblocks_sprite = []
        list_calls = []
        data = {}
        count_definitions = 0
        count_calls = 0
        for e in json_project["targets"]:
            for k in e:
                if k == "blocks":
                    name = e["name"]
                    data = {}
                    data[name] = []
                    list_calls = []
                    is_stage = e["isStage"]
                    for key in e[k]:
                        try:
                            if e[k][key]["opcode"] == "procedures_prototype":
                                data[name].append({"type": "procedures_prototype", "name": e[k][key]["mutation"]["proccode"],
                                        "argument_names":e[k][key]["mutation"]["argumentnames"],
                                        "argument_ids": e[k][key]["mutation"]["argumentids"],
                                        "n_calls": 0})
                                count_definitions += 1
                            elif e[k][key]["opcode"] == "procedures_call":
                                list_calls.append({"type": "procedures_call", "name": e[k][key]["mutation"]["proccode"],
                                                   "argument_ids":e[k][key]["mutation"]["argumentids"]})
                                count_calls += 1
                                print(name)


                        except Exception as e:
                            pass
                    for call in list_calls:
                        for procedure in data[name]:
                            print("Comprueba")
                            print(procedure["name"], procedure["type"], " ||| ", call)
                            if procedure["name"] == call["name"] and procedure["type"] == "procedures_prototype":
                                print("encuentra llamada")
                                procedure["n_calls"] = procedure["n_calls"] + 1
                    data[name] += list_calls
                    list_customblocks_sprite.append(data)
        data = {"name": filename.split(".")[0], "custom_blocks": list_customblocks_sprite, "n_custom_blocks": count_definitions,
                "n_custom_blocks_calls": count_calls}
        col_custom.insert_one(data)

        print(filename, ": Number of custom blocks", count_definitions, count_calls)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(filename, "could not be analyzed")