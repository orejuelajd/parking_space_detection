import requests
data = {"totalPermitidos":[10,11,12]}
response = requests.put('https://cv-mongoserver.herokuapp.com/api/rois/60706f423d7d85482c32fc88', data=data)
print(response.content)