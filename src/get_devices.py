import requests
import json
import datetime
import os
import math

viewId = 1510


# Provide an easy interface to interact with the Eniris API, in the style of the requests library (https://docs.python-requests.org/en/master/)
# The documentation of the API is available via https://github.com/eniris-international/middleware/blob/master/openapi.yaml: copy the contents of this file in the swagger editor (https://editor.swagger.io/)
class InsightsApiConnector:
    def __init__(self, username, password, refreshTokenFilePath=None):
        self.username = username
        self.password = password
        self.refreshTokenFilePath = refreshTokenFilePath
        self.authenticationBaseUrl = 'https://authentication.eniris.be'
        self.middlewareBaseUrl = 'https://middleware-new.eniris.be'
        self.refreshDtAndToken = None
        self.accessDtAndToken = None

    def _authenticate(self):
        dt = datetime.datetime.now()
        if self.refreshDtAndToken is None and self.refreshTokenFilePath is not None and os.path.isfile(
                self.refreshTokenFilePath):
            with open(self.refreshTokenFilePath) as refreshTokenFile:
                refreshTokenFileContent = json.loads(refreshTokenFile.read())
            self.refreshDtAndToken = (
            datetime.datetime.fromtimestamp(refreshTokenFileContent["timestamp"]), refreshTokenFileContent["token"])
        if self.refreshDtAndToken is None or (
                dt - self.refreshDtAndToken[0]).total_seconds() > 13 * 24 * 60 * 60:  # 13 days
            data = {"username": self.username, "password": self.password}
            resp = requests.post(self.authenticationBaseUrl + '/auth/login', json=data)
            if resp.status_code != 200:
                raise Exception("login failed: " + resp.text)
            self.refreshDtAndToken = (dt, resp.text)
            if self.refreshTokenFilePath is not None:
                with open(self.refreshTokenFilePath, "w") as refreshTokenFile:
                    refreshTokenFile.write(json.dumps(
                        {"timestamp": self.refreshDtAndToken[0].timestamp(), "token": self.refreshDtAndToken[1]}))
        elif (dt - self.refreshDtAndToken[0]).total_seconds() > 7 * 24 * 60 * 60:  # 7 days
            resp = requests.get(self.authenticationBaseUrl + '/auth/refreshtoken',
                                headers={'Authorization': 'Bearer ' + self.refreshDtAndToken[1]})
            if resp.status_code != 200:
                raise Exception("refreshtoken failed: " + resp.text)
            self.refreshDtAndToken = (dt, resp.text)
            if self.refreshTokenFilePath is not None:
                with open(self.refreshTokenFilePath, "w") as refreshTokenFile:
                    refreshTokenFile.write(json.dumps(
                        {"timestamp": self.refreshDtAndToken[0].timestamp(), "token": self.refreshDtAndToken[1]}))
        if self.accessDtAndToken is None or (dt - self.accessDtAndToken[0]).total_seconds() > 2 * 60:  # 2 minutes
            resp = requests.get(self.authenticationBaseUrl + '/auth/accesstoken',
                                headers={'Authorization': 'Bearer ' + self.refreshDtAndToken[1]})
            if resp.status_code != 200:
                raise Exception("accesstoken failed: " + resp.text)
            self.accessDtAndToken = (dt, resp.text)

    def get(self, relPath, params=None):
        self._authenticate()
        return requests.get(self.middlewareBaseUrl + relPath, params=params,
                            headers={'Authorization': 'Bearer ' + self.accessDtAndToken[1]})

    def post(self, relPath, data={}, params=None):
        self._authenticate()
        return requests.post(self.middlewareBaseUrl + relPath, json=data, params=params,
                             headers={'Authorization': 'Bearer ' + self.accessDtAndToken[1]})

    def put(self, relPath, data={}, params=None):
        self._authenticate()
        return requests.put(self.middlewareBaseUrl + relPath, json=data, params=params,
                            headers={'Authorization': 'Bearer ' + self.accessDtAndToken[1]})

    def delete(self, relPath, params=None):
        self._authenticate()
        return requests.delete(self.middlewareBaseUrl + relPath, params=params,
                               headers={'Authorization': 'Bearer ' + self.accessDtAndToken[1]})


def findViewIdByRoleName(roleName, connector, ancestorRoleId=None):
    if ancestorRoleId is None:
        resp = connector.get("/v1/role")
    else:
        resp = connector.get("/v1/role", {"ancestorRoleId": ancestorRoleId})
    if resp.status_code != 200:
        raise Exception("device post failed: " + resp.text)
    roles = resp.json()["role"]
    roleId = None
    for role in roles:
        if role["name"] == roleName:
            roleId = role["id"]
            break
    if roleId is not None:
        resp = connector.get("/v1/role/" + str(roleId) + "/views")
        if resp.status_code != 200:
            raise Exception("device post failed: " + resp.text)
        else:
            return resp.json()["views"][0]["viewId"]
    raise Exception("Failed to find a role with name: " + roleName)


def run(vieuw,klant=None,deviceId=None):
    # import argparse
    # parser = argparse.ArgumentParser(description='Add one or more devices to a given customer')
    # parser.add_argument('-username', type=str, nargs="?",
    #                     help="Username to authenticate with the Eniris Insights API")
    # parser.add_argument('-password', type=str, nargs="?",
    #                     help="Password to authenticate with the Eniris Insights API")
    # parser.add_argument('-refreshTokenPath', type=str, nargs="?", default="../refreshTokenAndTimestamp.txt",
    #                     help="Path of the file in which the refresh token should be stored")
    # # parser.add_argument('filepath', type=str, nargs=1,
    # #                     help="file path for the data.json file")
    # # parser.add_argument('roleName', type=str, nargs=1,
    # #                     help="Name of the role to which the view is coupled where the devices will be fetched from")
    # # args = parser.parse_args()
    # if args.username is None or args.password is None:
    #     print(
    #         "Warning: If the there is no refresh token stored, or the stored refresh token is expired, you will not be able to authenticate. Pass the username and password to deal with this case")

    connector = InsightsApiConnector("nick@insoldev.be", "Insoldev050287!")
    roleName = vieuw
    filepath = "data.json"

    viewId = findViewIdByRoleName(roleName, connector)
    # print(viewId)

    if klant:
        r = connector.get(relPath='/v1/device', params={"viewId": viewId,"name":klant})
    if  deviceId:
         r= connector.get(relPath='/v1/device', params={"viewId": viewId,"id": deviceId})




    if (r.status_code == 200):
        deviceData = r.json()

        with open(filepath, 'w') as file_object:  # open the file in write mode
            tempDevices = []

            for device in deviceData["device"]:
                # print(device)
                klantId=device['id']
                print(klantId)

                tempDevices.append(device["properties"])
            json.dump(tempDevices, file_object)  # json.dump() function to stores the data in data.json file
    else:
        print("Error while getting devices status code: " + str(r.status_code))

    # Read in the file
    with open(filepath, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('\\\\"', '"')
    filedata = filedata.replace('\\"', '"')
    filedata = filedata.replace(']"', ']')
    filedata = filedata.replace('}"', '}')
    filedata = filedata.replace('"[', '[')
    filedata = filedata.replace('"{', '{')
    filedata = filedata.replace('\\t', '')
    filedata = filedata.replace('\\n','')


    # Write the file out again
    with open(filepath, 'w') as file:
        file.write(filedata)




