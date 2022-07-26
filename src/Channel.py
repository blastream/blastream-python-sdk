import json

import requests

from Collaborator import Collaborator
import Instance
from Scene import Scene


class Channel(Instance.Instance):

    def __init__(self, public_key, private_key, custom_domain):
        super().__init__(public_key, private_key, custom_domain)
        self.identifier = None
        self.slug = None
        self._is_channel = True

    def setSlug(self, slug):
        self.slug = slug

    def setId(self, identifier):
        self.identifier = identifier

    def getId(self):
        return self.identifier

    def setAccessRule(self, privacy, params):
        tmp = {}
        if privacy == "PRIVATE":
            privacy = 2
        if privacy == "PUBLIC":
            privacy = 0
        tmp["privacy"] = privacy
        tmp["data"] = params
        body = json.dumps(tmp)
        return self.put("/channel/rule", body)

    def createOrRefreshSpeakersToken(self):
        body = json.dumps({})
        return self.post("/channel/speakers-token", body)

    def removeSpeakersToken(self):
        return self.delete("/channel/speakers-token")

    def getSpeakersToken(self):
        body = json.dumps({})
        return self.get("/channel/speakers-token", body)

    def getReplays(self):
        body = json.dumps({})
        return self.get("/channel/videos", body)

    def getSettings(self):
        body = json.dumps({})
        return self.get("/channel/settings", body)

    def updateAdvancedSettings(self, params):
        param = {"advanced": params}
        return self.updateSettings(param)

    def updateSettings(self, params):
        body = json.dumps({"data": params})
        return self.post("/channel/settings", body)

    def updateChatSettings(self, params):
        body = json.dumps({"data": params})
        return self.post("/chat/settings", body)

    def updateSubscription(self, plan, billing):
        body = json.dumps({"plan": plan, "billing": billing})
        return self.post("/channel/subscription", body)

    def setCustom(self, params):
        body = json.dumps({"data": params})
        return self.post("/channel/custom", body)

    def removeCustom(self):
        return self.delete("/channel/custom")

    def disconnectAll(self):
        params = json.dumps({})
        return self.post("/channel/disconnectAll", params)

    def sendMessage(self, params):
        self._is_channel = False
        body = json.dumps({"msg": params["msg"], "username": params["username"], "slug": self.slug})
        result = self.post("/api/msg", body)
        self._is_channel = True
        return result

    def remove(self):
        self._is_channel = False
        result = self.delete("/space/" + self.slug)
        self._is_channel = True
        return result

    def startLivestreaming(self):
        body = json.dumps({})
        return self.post("/channel/livestreaming/start", body)

    def stopLivestreaming(self):
        body = json.dumps({})
        return self.post("/channel/livestreaming/stop", body)

    def startRecord(self):
        body = json.dumps({})
        return self.post("/channel/startrecord", body)

    def stopRecord(self):
        body = json.dumps({})
        return self.post("/channel/stoprecord", body)

    def createOrGetCollaborator(self, displayname, status, params):
        if params is None:
            params = json.dumps({})
        collabs = self.getCollaborators(status),
        collabL = collabs[0]
        for i in range(len(collabL)):
            collab = collabL[i]
            if collab.getDisplayname() == displayname and collab.getStatus() == status:
                return collab
        return self.createCollaborator(displayname, status, params)

    def createCollaborator(self, displayname, status, params):
        if params is None:
            params = {}
        params = json.dumps(params)
        tmp = json.loads(params)
        tmp['displayname'] = displayname
        tmp["status"] = status
        body = json.dumps(tmp)
        collab = self.put("/channel/collaborator", body)
        return Collaborator(collab, self)

    def getCollaborators(self, status):
        if status == "":
            lists = self.get("/channel/collaborators", json.dumps({}))
        else:
            lists = self.get("/channel/collaborators/" + status, json.dumps({}))
        collabs = []
        for i in range(len(lists)):
            collab = lists[i]
            collabs.append(Collaborator(collab, self))
        return collabs

    def uploadPic(self, name, filePath, type='pic'):
        tmp = {
           "X-Api-Public": self.public_key,
           "X-Api-Private": self.private_key,
           "X-Auth-Token": self.APIToken,
        }
        file = {"file": open(filePath, 'rb'), "filename": name}
        response = requests.post(self.request_url + "/broadcaster/upload/" + type, headers=tmp, files=file)
        return response.json()

    def uploadScenePic(self, type, filePath):
        res = self.uploadPic(filePath, filePath, type)
        res["file"] = "./docs" + res["file"]
        return res

    def createScene(self, name, data):
        data["name"] = name
        body = json.dumps({"data": data})
        response = self.put("/channel/scene", body)
        listscene = response["list"]
        for i in range(len(listscene)):
            if listscene[i]["name"] == name:
                return Scene(listscene[i], self)

    def getScenes(self):
        scenes = []
        data = self.get("/channel/scenes", {})
        listScene = data["list"]
        for i in range(len(listScene)):
            scene = json.dumps(listScene[i])
            scenes.append(Scene(scene, self))
        return scenes
