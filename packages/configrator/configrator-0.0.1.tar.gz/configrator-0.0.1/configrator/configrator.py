import json
import os

config_L = {
    "name": "",
    "id": ""
}
class manager:
    def CreateConfig(file, name, id,):
        global config_L
        config_L["name"] = name
        config_L["id"] = id
        with open(file + ".json", "w") as config_file:
            json.dump(config_L, config_file)
    def CheckConfig(file, name, id):
        global config_L
        if os.path.isfile(file + ".json"):
            return True
        else:
            manager.CreateConfig(file, name, id)
            return False
        

    
    def GetConfig(file):
        global config_L
        with open(file + ".json", "r") as config_file:
            config_L = json.load(config_file)
        return config_L
    def GetName(file):
        global config_L
        config_L = manager.GetConfig(file)
        return config_L["name"]
    def GetID(file):
        global config_L
        config_L = manager.GetConfig(file)
        return config_L["id"]
    def SetName(file, name):
        global config_L
        config_L = manager.GetConfig(file)
        config_L["name"] = name
        with open(file + ".json", "w") as config_file:
            json.dump(config_L, config_file)
    def SetID(file, id):
        global config_L
        config_L = manager.GetConfig(file)
        config_L["id"] = id
        with open(file + ".json", "w") as config_file:
            json.dump(config_L, config_file)
    # add option to config file with a value in function
    def SetOption(file, option, value):
        global config_L
        config_L = manager.GetConfig(file)
        config_L[option] = value
        with open(file + ".json", "w") as config_file:
            json.dump(config_L, config_file)
    def GetOption(file, option):
        global config_L
        config_L = manager.GetConfig(file)
        return config_L[option]
    def CheckOption(file, option):
        global config_L
        config_L = manager.GetConfig(file)
        if option in config_L:
            return True
        else:
            return False
    def DeleteConfig(file):
        global config_L
        os.remove(file + ".json")
    # create multiple configs
    