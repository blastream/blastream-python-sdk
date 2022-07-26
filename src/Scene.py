import json


class Scene:
    def __init__(self, data, instance):
        self.data = data
        self.instance = instance

    def update(self, data):
        body = json.dumps({"data": data})
        res = self.instance.post("/channel/scene/" + str(self.data["id"]), body)
        listscene = res["list"]
        for i in range(len(listscene)):
            if listscene[i]["id"] == self.data["id"]:
                self.data = listscene[i]
                return listscene[i]

    def getData(self):
        return self.data

    def isDefault(self):
        return self.data["default_scene"]

    def remove(self,):
        return self.instance.delete("/channel/scene/" + str(self.data["id"]))

    def getScene(self, identifier):
        scene = self.instance.get("/channel/scene/" + identifier, {})
        return Scene(scene, self)
