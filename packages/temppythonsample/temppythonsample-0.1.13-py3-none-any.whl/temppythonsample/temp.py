import json
import uuid
import string
import random
pipelineShapes = []
pipelineShapeConnections = []
pipelineShapesId = []
dataStores = []
# pipad = []
# pip = ["abc", "afa", "afa"]
# # print(type(pip))
# for a in pip:
#     pipad.append(a)
# print(pipad)
# print(pip)

pipelineShapeId = str(uuid.uuid4())
     
dataStore = {
    "id": pipelineShapeId,
    "pipelineId": 0,
    "pipelineShapeAttributes": [
        {
            "AttributeValue": "def_blob_store",
            "shapeAttributeId": 17
        },
        {
            "AttributeValue": "/textSearch",
            "shapeAttributeId": 18
        },
        {
            
        }
    ],
    "shapeDisplayName": "Data Tranfer",
    "shapeId": 3,
    "sortOrder": 4,
    "statusImageUrl": "assets/images/diagram/icon-none.svg",
    "stepOrder": 0,
    "x": 0,
    "y": 0
}
dataStores.append(dataStore)

pipelineShapeId = str(uuid.uuid4())
pipelineShapesId.append(pipelineShapeId)

pipelineShape = {
    "id": pipelineShapeId,
    "pipelineId": 0,
    "pipelineShapeAttributes": [
        {
            "AttributeValue": "def_blob_store",
            "shapeAttributeId": 1
        },
        {
            "AttributeValue": "path_on_datastore",
            "shapeAttributeId": 2
        }
    ],
    "shapeDisplayName": "data_reference_name",
    "shapeId": 1,
    "sortOrder": 0,
    "statusImageUrl": "assets/images/diagram/icon-none.svg",
    "stepOrder": 0,
    "x": 0,
    "y": 0
}
pipelineShapes.append(pipelineShape)

pipelineShapeId = str(uuid.uuid4())
pipelineShapesId.append(pipelineShapeId)

pipelineShape = {
    "id": pipelineShapeId,
    "pipelineId": 0,
    "pipelineShapeAttributes": [
        {
            "AttributeValue": "script_name",
            "shapeAttributeId": 6
        },
        {
            "AttributeValue": str(["gensim==3.8.0","scikit-learn"]),
            "shapeAttributeId": 7
        },
        {
            "AttributeValue": str(["pandas"]),
            "shapeAttributeId": 8
        },
        {
            "AttributeValue": str(["--read-from-file", "blob_input_data", "--save-to-file-path", "clean_text_data"]),
            "shapeAttributeId": 9
        }
    ],
    "shapeDisplayName": "name",
    "shapeId": 2,
    "sortOrder": 0,
    "statusImageUrl": "assets/images/diagram/icon-none.svg",
    "stepOrder": 0,
    "x": 0,
    "y": 0
}

pipelineShapes.append(pipelineShape)

pipelineShapeId = str(uuid.uuid4())
pipelineShapesId.append(pipelineShapeId)

pipelineShape = {
    "id": pipelineShapeId,
    "pipelineId": 0,
    "pipelineShapeAttributes": [
        {
            "AttributeValue": "script_name",
            "shapeAttributeId": 6
        },
        {
            "AttributeValue": "str(condaPackageList)",
            "shapeAttributeId": 7
        },
        {
            "AttributeValue": "str(pipPackagesList)",
            "shapeAttributeId": 8
        },
        {
            "AttributeValue": "str(arguments)",
            "shapeAttributeId": 9
        }
    ],
    "shapeDisplayName": "name",
    "shapeId": 2,
    "sortOrder": 0,
    "statusImageUrl": "assets/images/diagram/icon-none.svg",
    "stepOrder": 0,
    "x": 0,
    "y": 0
}

pipelineShapes.append(pipelineShape)
pipelineShapesId.append(dataStores[0]['id'])

pipelineShapes.append(dataStores[0])

print(len(pipelineShapesId))

res = ''.join(random.choices(string.ascii_lowercase +
                             string.ascii_uppercase + 
                             string.digits, k = 10))
print(res)

for id in range(0,len(pipelineShapesId)-1):
    print(id)
    pipelineShapeConnection = json.dumps({
        "from": pipelineShapesId[id],
        "fromConnector": "bottom",
        "id": res,
        "to": pipelineShapesId[id+1],
        "toConnector": "top"
    })
        
    pipelineShapeConnections.append(pipelineShapeConnection)

print(pipelineShapeConnections)

x = 450
y = 80
sortOrder = 1
for pipe in pipelineShapes:
    pipe['sortOrder'] = sortOrder
    pipe['x'] = x
    pipe['y'] = y
    sortOrder+=1
    y+=100


print(pipelineShapes)
 
# pipelineShapeConnections.append(pipelineShapeConnection)
# pipelineShapeConnections.append(pipelineShapeConnection)
# # pipelineShapeConnections[0].id.assign('abc')
# pipelineShapeConnections[0]['id'] = "acv"
# print(type(pipelineShapes))
# print(pipelineShapeConnections[0]['id'])