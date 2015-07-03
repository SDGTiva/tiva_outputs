from argparse import ArgumentParser
import json
import os

def main():
    arguments_parser = ArgumentParser(description="Register outputs.")
    arguments_parser.add_argument("command", help="command")
    arguments_parser.add_argument("args", nargs="*", help="command arguments")
    arguments_parser.add_argument("--tiva-path", default="/usr/share/tiva", help="path to tiva directory")
    arguments = arguments_parser.parse_args()
    command = vars(arguments)["command"]
    args = vars(arguments)["args"]
    tiva_path = vars(arguments)["tiva_path"]
    outputs_path = os.path.join(tiva_path, "outputs")
    if not os.path.isdir(outputs_path):
        os.mkdir(outputs_path)
    if command == "add":
        output_type = args[0]
        name = args[1]
        output_id = max(map(lambda filename: int(filename.split(".")[0]), os.listdir(outputs_path)) + [-1]) + 1
        output = open(os.path.join(outputs_path, "%s.json" % output_id), "w")
        json.dump({
            "name": name,
            "type": output_type,
        }, output)
        output.close()
    if command == "getid":
        name = args[0]
        for filename in os.listdir(outputs_path):
            output = json.load(open(os.path.join(outputs_path, filename)))
            if output["name"] == name:
                output_id = filename.split(".")[0]
                print output_id
                return
    if command == "rm":
        output_id = args[0]
        output_path = os.path.join(outputs_path, "%s.json" % output_id)
        os.remove(output_path)
    if command == "get":
        output_id = args[0]
        key = args[1]
        output_path = os.path.join(outputs_path, "%s.json" % output_id)
        output = json.load(open(output_path))
        print output[key]
    if command == "set":
        output_id = args[0]
        key = args[1]
        value = args[2]
        output_path = os.path.join(outputs_path, "%s.json" % output_id)
        output = json.load(open(output_path))
        output[key] = value
        json.dump(output, open(output_path, "w"))
