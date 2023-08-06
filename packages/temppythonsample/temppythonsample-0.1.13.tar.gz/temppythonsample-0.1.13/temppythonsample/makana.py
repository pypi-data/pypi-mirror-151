from glob import glob
import os
from authService import Authentication
from azureml.core import Workspace, Experiment, Datastore, RunConfiguration, Environment
import requests
import json
import uuid
import string
import random
pipelineShapes = []
pipelineShapeConnections = []
pipelineShapesId = []
pythonScriptShape = []

class Makana():
    global pipelineId
    def getProjects():
        authentication = Authentication
        access_token_header = authentication.getToken()
        url = "https://localhost:44350/api/makana/projects"
        headers = {
            'Authorization': access_token_header,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, verify=False)
        result = response.json()
        if response.ok:
            print(json.dumps(result, indent=2))
            return result
        else:
            print(result)

    def getBaseImages():
        authentication = Authentication
        access_token_header = authentication.getToken()
        url = "https://localhost:44350/api/makana/baseimages"
        headers = {
            'Authorization': access_token_header,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, verify=False)
        result = response.json()
        if response.ok:
            print(json.dumps(result, indent=2))
            return result
        else:
            print(result)
    
    def createPipeline(name: str, projectId: int, baseImageId: int):
        authentication = Authentication
        access_token_header = authentication.getToken()
        url = "https://makana-app-staging-wa.azurewebsites.net/api/makana/pipelines"
        headers = {
            'Authorization': access_token_header,
            'Content-Type': 'application/json'
        }
        pipeline = json.dumps({
            "name": name,
            "projectId": projectId,
            "baseImageId": baseImageId
        })
        
        response = requests.post(url, headers=headers, data=pipeline, verify=False)
        result = response.json()
        if response.ok:
            global pipelineId
            pipelineId = result['id']
            print(json.dumps(result, indent=2))
        else:
            print("Error" + response.text())
    
    def getDataStores():
        authentication = Authentication
        access_token_header = authentication.getToken()
        url = "https://makana-app-staging-wa.azurewebsites.net/api/makana/workspace/datastores"
        headers = {
            'Authorization': access_token_header,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, verify=False)
        results = response.json()
        if response.ok:
            for result in results:
                print(result['name'])
        else:
            print(result)
    
    
    def createSourceDataStep(name: str, blobStoreName: str, path: str):
        pipelineShapeId = str(uuid.uuid4())
        pipelineShapesId.append(pipelineShapeId)
        internalName = name.lower().replace(" ", "_")
        # global pipelineId
        # pipelineId = 2
        global sourceDataShape
        sourceDataShape = {
            "id": pipelineShapeId,
            "pipelineId": pipelineId,
            "pipelineShapeAttributes": [
                {
                    "attributeValue": blobStoreName,
                    "shapeAttributeId": 1
                },
                {
                    "attributeValue": path,
                    "shapeAttributeId": 2
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 3
                }
            ],
            "shapeDisplayName": name,
            "shapeInternalName": internalName,
            "shapeId": 1,
            "sortOrder": 0,
            "statusImageUrl": "assets/images/diagram/icon-none.svg",
            "stepOrder": 0,
            "x": 0,
            "y": 0
        }
    
    def CreatePythonScriptStep(name: str, scriptFileDirectory: str, condaDependencies: str, pipPackages: str, arguments: list):
        
        scriptFileName = os.path.basename(scriptFileDirectory)
        internalName = name.lower().replace(" ", "_")
        
        pipelineShapeId = str(uuid.uuid4())
        pipelineShapesId.append(pipelineShapeId)
        
        authentication = Authentication
        access_token_header = authentication.getToken()
        url = "https://makana-app-staging-wa.azurewebsites.net/api/makana/pipelines/uploadscript"
        headers = {
            'Authorization': access_token_header,
        }
        
        data = {
            'pipelineId': pipelineId
        }
        
        files=[
            ('files',(scriptFileName,open(scriptFileDirectory,'rb'),'application/octet-stream'))
        ]
         
        response = requests.post(url, headers=headers, data=data, files=files, verify=False)
        result = response.json()
        if response.ok:
            print(json.dumps(result, indent=2))
        else:
            print("Error" + response.text())
                   
        step = {
            "id": pipelineShapeId,
            "pipelineId": pipelineId,
            "pipelineShapeAttributes": [
                {
                    "attributeValue": "",
                    "shapeAttributeId": 5
                },
                {
                    "attributeValue": scriptFileName,
                    "shapeAttributeId": 6
                },
                {
                    "attributeValue": condaDependencies,
                    "shapeAttributeId": 7
                },
                {
                    "attributeValue": pipPackages,
                    "shapeAttributeId": 8
                },
                {
                    "attributeValue": arguments,
                    "shapeAttributeId": 9
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 10
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 11
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 12
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 13
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 14
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 15
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 16
                }
            ],
            "shapeDisplayName": name,
            "shapeInternalName": internalName,
            "shapeId": 2,
            "sortOrder": 0,
            "statusImageUrl": "assets/images/diagram/icon-none.svg",
            "stepOrder": 0,
            "x": 0,
            "y": 0
        }
        
        pythonScriptShape.append(step)
         
    
    def createDataTransferStep(name: str, blobStoreName: str, path_on_datastore: str):
        
        internalName = name.lower().replace(" ", "_")
        
        pipelineShapeId = str(uuid.uuid4())
        pipelineShapesId.append(pipelineShapeId)
        
        global dataTransferShape
        dataTransferShape = {
            "id": pipelineShapeId,
            "pipelineId": pipelineId,
            "pipelineShapeAttributes": [
                {
                    "attributeValue": blobStoreName,
                    "shapeAttributeId": 17
                },
                {
                    "attributeValue": path_on_datastore,
                    "shapeAttributeId": 18
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 19
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 20
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 21
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 22
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 23
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 24
                },
                {
                    "attributeValue": "",
                    "shapeAttributeId": 25
                }
            ],
            "shapeDisplayName": name,
            "shapeInternalName": internalName,
            "shapeId": 3,
            "sortOrder": 0,
            "statusImageUrl": "assets/images/diagram/icon-none.svg",
            "stepOrder": 0,
            "x": 0,
            "y": 0
        }
       
    def savePipeline():
        
        pipelineShapes.append(sourceDataShape)
        for shape in pythonScriptShape:
            pipelineShapes.append(shape)
        pipelineShapes.append(dataTransferShape)    

        
        x = 450
        y = 80
        sortOrder = 1
        for pipelineShape in pipelineShapes:
            pipelineShape['sortOrder'] = sortOrder
            pipelineShape['x'] = x
            pipelineShape['y'] = y
            sortOrder+=1
            y+=100
        
        
        for id in range(0,len(pipelineShapesId)-1):
            randomId = ''.join(random.choices(string.ascii_lowercase +
                             string.ascii_uppercase + 
                             string.digits, k = 10))
            pipelineShapeConnection = {
                "pipelineId": pipelineId,
                "from": pipelineShapesId[id],
                "fromConnector": "bottom",
                "id": randomId,
                "to": pipelineShapesId[id+1],
                "toConnector": "top"
            }
                
            pipelineShapeConnections.append(pipelineShapeConnection)

        
        pipeline = json.dumps({
            "id": pipelineId,
            "pipelineShapeConnections": pipelineShapeConnections,
            "pipelineShapes": pipelineShapes,
        })
        
        authentication = Authentication
        access_token_header = authentication.getToken()
        url = "https://makana-app-staging-wa.azurewebsites.net/api/makana/pipelines/pipelineShapes"
        headers = {
            'Authorization': access_token_header,
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, data=pipeline, verify=False)
        if response.ok:
            # global pipelineResult
            result = response.json()
            print(json.dumps(result, indent=2))
            # return response.json()
        else:
            print("Error" + response.text())
        
        
    def getPipeline(pipelineId: int):
        authentication = Authentication
        access_token_header = authentication.getToken()
        url = "https://makana-app-staging-wa.azurewebsites.net/api/makana/pipelines/" + str(pipelineId)
        headers = {
            'Authorization': access_token_header,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, verify=False)
        if response.ok:
            result = response.json()
            print(result)
            return result
        else:
            print("Error" + response)
            
    def runPipeline(pipelineId: int):
        
        pipelineResult = Makana.getPipeline(pipelineId)
        authentication = Authentication
        access_token_header = authentication.getToken()
        url = "https://makana-app-staging-wa.azurewebsites.net/api/makana/makanafunction/runrequest"
        headers = {
            'Authorization': access_token_header,
            'Content-Type': 'application/json'
        }
        
        pipeline = json.dumps(pipelineResult)
        
        # pipeline = pipelineResult
        
        response = requests.post(url, headers=headers, data=pipeline, verify=False)
        if response.ok:
            result = response.json()
            # print(result['id'])
            return response.json()
        else:
            print("Error" + response)