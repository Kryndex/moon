import json
import api.utilities as utilities


def get_policies(client):
    req = client.get("/policies")
    policies = utilities.get_json(req.data)
    return req, policies


def add_policies(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "model_id": "modelId",
        "genre": "genre"
    }
    req = client.post("/policies", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    policies = utilities.get_json(req.data)
    return req, policies


def delete_policies(client, name):
    request, policies = get_policies(client)
    for key, value in policies['policies'].items():
        if value['name'] == name:
            req = client.delete("/policies/{}".format(key))
            break
    return req


def delete_policies_without_id(client):
    req = client.delete("/policies/{}".format(""))
    return req


def test_get_policies():
    client = utilities.register_client()
    req, policies = get_policies(client)
    assert req.status_code == 200
    assert isinstance(policies, dict)
    assert "policies" in policies


def test_add_policies():
    client = utilities.register_client()
    req, policies = add_policies(client, "testuser")
    assert req.status_code == 200
    assert isinstance(policies, dict)
    value = list(policies["policies"].values())[0]
    assert "policies" in policies
    assert value['name'] == "testuser"
    assert value["description"] == "description of {}".format("testuser")
    assert value["model_id"] == "modelId"
    assert value["genre"] == "genre"


def test_delete_policies():
    client = utilities.register_client()
    req = delete_policies(client, "testuser")
    assert req.status_code == 200


def test_delete_policies_without_id():
    client = utilities.register_client()
    req = delete_policies_without_id(client)
    assert req.status_code == 500

