import json
import re

import requests

import Channel


class Instance:

    def __init__(self, public_key, private_key, custom_domain):
        self.slug = None
        self.version = None
        self.timeout = None
        self.request_url = "https://api.v2.blastream.com"
        self.app_url = "app.v2.blastream.com"
        self.APIToken = ""
        self.token = ""
        self.channel_url = ""
        self.embed = 1
        self.whitelabel_url = ""
        self.is_channel = False

        self.public_key = public_key
        self.private_key = private_key

        if custom_domain != "":
            self.whitelabel_url = custom_domain

    def getPublicKey(self):
        return self.public_key

    def setChannelModel(self, Channel):
        self.Channel = Channel

    def setRequestUrl(self, url):
        self.request_url = url

    def setChannelUrl(self,url):
        self.channel_url = url

    def setTimeout(self, timeout):
        self.timeout = timeout

    def setVersion(self, v):
        self.version = v

    def get(self, url, params):
        tmp = {
            "X-Api-Public": self.public_key,
            "X-Api-Private": self.private_key,
            "X-Auth-Token": self.APIToken
        }
        response = requests.get(self.request_url + url, headers=tmp, json=params)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()

    def post(self, url, params):
        tmp = {
            "X-Api-Public": self.public_key,
            "X-Api-Private": self.private_key,
            "X-Auth-Token": self.APIToken,
        }
        param = json.loads(params)
        response = requests.post(self.request_url + url, headers=tmp, json=param)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()

    def put(self, url, params):
        tmp = {
            "X-Api-Public": self.public_key,
            "X-Api-Private": self.private_key,
            "X-Auth-Token": self.APIToken,
        }
        param = json.loads(params)
        response = requests.put(self.request_url + url, headers=tmp, json=param)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()

    def delete(self, url):
        tmp = {
            "X-Api-Public": self.public_key,
            "X-Api-Private": self.private_key,
            "X-Auth-Token": self.APIToken
        }
        response = requests.delete(self.request_url + url, headers=tmp)
        return response.json()

    def getIframe(self, width, height, params):
        if 'url' in params:
            url = params["url"]
        else:
            url = self.getUrl()
        style = ""
        if 'style' in params:
            style = params["style"]

        htmlFrame = '<iframe allow="microphone; camera; display-capture" width="' + width + '" height="' + height + \
                    '" src="' + url + '" frameborder="0" scrolling="no" allowFullScreen="true" style="' + style + \
                    '" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>'
        return htmlFrame

    def getUrl(self):
        url = self.channel_url
        if self.whitelabel_url != "":
            url = url.replace(self.app_url, self.whitelabel_url)
        return url + '?token=' + self.token + '&api=' + self.public_key + '&embed=1'

    def initChannel(self, result):
        channel = Channel.Channel(self.public_key, self.private_key, self.whitelabel_url)
        channel.setRequestUrl(self.request_url)
        channel.setSlug(self.slug)
        channel.setChannelUrl(result["url"])
        channel.setResponseToken(result)
        channel.setId(result["id"])
        channel.setToken(result["token"])
        self.setToken(result["token"])
        self.channel_url = result["url"]
        if self.APIToken == "":
            self.APIToken = result["token"]
            channel.setAPIToken(result["token"])
        return channel

    def createOrGetChannel(self, slug, params):
        self.setSlug(slug)
        body = json.dumps({'body': params})
        result = self.post("/space/channel/" + self.slug, body)
        return self.initChannel(result)

    def createOrGetParticipant(self, slug, identifier, params):
        if 'nickname' not in params:
            params["nickname"] = identifier
        params["id"] = identifier
        self.setSlug(slug)
        body = json.dumps(params)
        result = self.post("/space/channel/" + self.slug + "/participant", body)
        return self.initChannel(result)

    def setResponseToken(self, res):
        self.token = res["token"]

    def getToken(self):
        return self.token

    def setToken(self, token):
        self.token = token

    def getAPIToken(self):
        return self.APIToken

    def setAPIToken(self, token):
        self.APIToken = token

    def revokeToken(self, token):
        params = json.dumps({})
        return self.post("/revoke-token/" + token, params)

    def revokeTokens(self, slug):
        params = json.dumps({})
        return self.post("/revoke-tokens/" + slug, params)

    def registerHook(self, url):
        body = json.dumps({"url": url})
        return self.post("/space/hook", body)

    def getPlans(self):
        body = json.dumps({})
        return self.get("/plans", body)

    def setSlug(self, slug):
        test = re.findall("[^A-Za-z0-9-]", slug)
        if test:
            raise Exception("This is not a valid slug. Only alphanumeric and " - " character are accepted")
        else:
            if len(slug) > 64 or len(slug) < 2:
                raise Exception("slug is too long or too short")
            else:
                self.slug = slug
