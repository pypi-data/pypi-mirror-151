# built-in
import ast
import os
import subprocess
import json
import shutil
import pwd

from epibox import config_debug


def send_default(client, username):

    ######## Default MAC addresses ########

    try:
        with open(
            "/home/{}/Documents/epibox/args.json".format(username), "r"
        ) as json_file:
            defaults = json_file.read()
            defaults = ast.literal_eval(defaults)
            if defaults["devices_mac"] == {}:
                defaults["devices_mac"] = {"MAC1": "12:34:56:78:91:10", "MAC2": ""}
            listMAC = defaults["devices_mac"]
    except Exception as e:
        listMAC = {"MAC1": "12:34:56:78:91:10", "MAC2": ""}

    listMAC2 = json.dumps(
        [
            "DEFAULT MAC",
            "{}".format(list(listMAC.values())[0]),
            "{}".format(list(listMAC.values())[1]),
        ]
    )

    client.publish(topic="rpi", qos=2, payload=listMAC2)

    config = json.dumps(["DEFAULT CONFIG", defaults])
    client.publish(topic="rpi", qos=2, payload=config)

    ######## Available drives ########

    listDrives = ["DRIVES"]
    drives = os.listdir("/media/{}/".format(username))

    for drive in drives:
        total, _, free = shutil.disk_usage("/media/{}/{}".format(username, drive))
        listDrives += ["{} ({:.1f}% livre)".format(drive, (free / total) * 100)]

    client.publish(topic="rpi", qos=2, payload="{}".format(listDrives))

    ######## Default configurations ########


def on_message(client, userdata, message):

    username = pwd.getpwuid(os.getuid())[0]

    message = str(message.payload.decode("utf-8"))
    message = ast.literal_eval(message)

    if message[0] == "RESTART":
        # client.loop_stop()
        # client.keepAlive = False
        config_debug.log("Not sure what to do here yet")

    elif message[0] == "INTERRUPT":
        client.keepAlive = False

    elif message[0] == "PAUSE ACQ":
        config_debug.log("PAUSING ACQUISITION")
        client.pauseAcq = True

    elif message[0] == "RESUME ACQ":
        config_debug.log("RESUMING ACQUISITION")
        client.pauseAcq = False

    elif message[0] == "ANNOTATION":
        config_debug.log("RECEIVED ANNOT {} ----------------------".format(message[1]))
        client.newAnnot = message[1]

    elif message[0] == "TURN OFF":
        config_debug.log("TURNING OFF RPI")
        client.publish(topic="rpi", payload=str(["TURNED OFF"]))

    elif message[0] == "TURNED OFF":
        subprocess.run(["sudo", "shutdown", "-h", "now"])

    elif message == ["Send default"]:
        send_default(client, username)

    ######## New default configuration ########

    elif message[0] == "NEW CONFIG DEFAULT":

        try:
            with open(
                "/home/{}/Documents/epibox/args.json".format(username), "r"
            ) as json_file:
                defaults = json_file.read()
                defaults = ast.literal_eval(defaults)
        except Exception as e:
            defaults = {
                "initial_dir": "EpiBOX Core",
                "fs": 1000,
                "channels": [],
                "devices_mac": {"MAC1": "12:34:56:78:91:10", "MAC2": ""},
                "save_raw": "true",
                "patient_id": "default",
                "service": "Bitalino",
            }

        for key in message[1].keys():
            defaults[key] = message[1][key]

        with open(
            "/home/{}/Documents/epibox/args.json".format(username), "w+"
        ) as json_file:
            json.dump(defaults, json_file)

        msg = json.dumps(["RECEIVED DEFAULT"])
        client.publish(topic="rpi", qos=2, payload=msg)
