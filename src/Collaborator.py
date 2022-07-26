import json


class Collaborator:

    def __init__(self, data, instance):
        self._data = data
        self._instance = instance

    def getDisplayname(self):
        return self._data["displayname"]

    def getStatus(self):
        return self._data["status"]

    def getData(self):
        return self._data

    def getInstance(self):
        return self._instance

    def update(self, displayname, status, params):
        params["displayname"] = displayname
        params["email"] = self._data["email"]
        params["status"] = status
        body = json.dumps(params)
        res = self._instance.post("/channel/collaborator/" + self._data["token"], body)
        self._data = res
        return res

    def remove(self):
        self._instance.delete("/channel/collaborator/" + self._data["token"])

    def getIframe(self, width, height, params):
        data = self.getData()
        if 'url' in params:
            url = params["url"]
        else:
            url = data["invite_link"] + '?token=' + data["token"] + '&api=' + self._instance.getPublicKey() + '&embed=1'
        style = ""
        if 'style' in params:
            style = params["style"]

        htmlFrame = '<iframe allow="microphone; camera; display-capture" width="' + width + '" height="' + height + \
                    '" src="' + url + '" frameborder="0" scrolling="no" allowFullScreen="true" style="' + style + \
                    '" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>'
        return htmlFrame
