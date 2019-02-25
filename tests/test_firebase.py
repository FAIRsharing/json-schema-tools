import os
import json
from firebase import firebase
from validate import miflowcyt_validate


if __name__ == '__main__':
    map_file = os.path.join(os.path.dirname(__file__),
                            "./data/MiFlowCyt/experiment_mapping.json")
    api_key = 'DBasdfas89798asoj892KOS'
    client = miflowcyt_validate.FlowRepoClient(map_file, api_key, 717)

    firebase = firebase.FirebaseApplication('https://miflowcyt-instances.firebaseio.com/', None)
    """result = firebase.get('/', None)
    print(result)"""

    """
    could_not_upload = []
    json_ld_instances = client.inject_context()

    print(json.dumps(json_ld_instances))

    firebase = firebase.FirebaseApplication('https://miflowcyt-instances.firebaseio.com/', None)

    for instance in json_ld_instances:
        new_instance = {
            instance: json_ld_instances[instance]
        }
        try:
            result = firebase.put('/',
                                  data=new_instance,
                                  name=instance,
                                  params={'print': 'pretty', 'X_FANCY_HEADER': 'VERY FANCY'})
            print(result)
        except Exception as e:
            print(e)
            could_not_upload.append(instance)
    print(json.dumps(could_not_upload, indent=4))
    """

    result = firebase.get('/', None)

    print(json.dumps(result))
