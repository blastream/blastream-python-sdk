All URIs are relative to *https://api.v2.blastream.com/api-docs*  
This is also where you can find all parameters related to params variable

### Examples

### createOrGetChannel

```python
instance = Instance("PUBLIC_KEY","PRIVATE_KEY", "")
params = {}
channel = instance.createOrGetChannel(name,params)
iframe = instance.getIframe()
```
### createCollaborator

```python
instance = Instance("PUBLIC_KEY","PRIVATE_KEY", "")
params = {}
channel = instance.createOrGetChannel(name,params)
paramsCollab = {"email": "user@example.com"}
colabname = channel.createOrGetCollaborator(name, status, paramsCollab)
channel.getIframe()
  ```
  ### create participant
  
  ```python
  instance = Instance("PUBLIC_KEY","PRIVATE_KEY", "")
  params = {}
  channel = instance.createOrGetChannel(name,params)
  iframe = instance.getIframe()
  paramsParticipant = {}
  instance.createOrGetParticipant(channelslug,participant id, paramsParticipant)
  iframe = instance.getIframe()
```

### getReplays

```python
instance = Instance("PUBLIC_KEY","PRIVATE_KEY", "")
params = {}
channel = instance.createOrGetChannel(name,params)
iframe = instance.getIframe()
channel.getReplays()
```

### setAccessRule

```python
instance = Instance("PUBLIC_KEY","PRIVATE_KEY", "")
params = {}
channel = instance.createOrGetChannel(name,params)
iframe = instance.getIframe()
AccessRule = {"password": "exemple_password"}
channel.setAccessRule("PRIVATE", AccessRule)
```

### updateSubscription

```python
instance = Instance("PUBLIC_KEY","PRIVATE_KEY", "")
params = {}
channel = instance.createOrGetChannel(name,params)
iframe = instance.getIframe()
channel.updateSubscription("pro2","hourly")
```

### updateSettings

```python
instance = Instance("PUBLIC_KEY","PRIVATE_KEY", "")
params = {}
channel = instance.createOrGetChannel(name,params)
iframe = instance.getIframe()
params = {"autojoin": 1}
channel.updateSettings(params)
```

### updateCollaborator

```python
instance = Instance("PUBLIC_KEY","PRIVATE_KEY", "")
params = {}
channel = instance.createOrGetChannel(name,params)
iframe = instance.getIframe()
Collaborator colab = channel.createOrGetCollaborator("username","moderator", {})
colab.update("new username","animator", {})
```
