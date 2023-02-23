from mongokit import Document, ObjectId
from db_connect import collection


class AppDeployment(Document):
    structure = {
        "id": int,
        "envName": str,
        "envId": int,
        "nodeName": str,
        "nodeId": int,
        "state": int,
        "comment": str,
        "installType": int,
        "installRequestType": int,
        "groupId": int,
        "groupName": str,
        "branchDeployment": {
            "id": int,
            "branchId": int,
            "branchName": str,
            "strategy": str,
            "manualReleaseId": int,
            "scheduledRelease": int,
            "installState": [
                {
                    "nodeName": str,
                    "nodeId": int,
                    "currentVersion": str,
                    "currentVersionId": int,
                    "state": str,
                    "lastVersion": str,
                    "lastVersionId": int,
                    "installDate": str,
                    "changeNo": str,
                    "prio": int,
                }
            ]
        },
        "puppetAppConfig": {
            "puppetClassId": int,
            "puppetClassName": str,
            "configData": {
                "cdi_url": str,
                "ingress": {
                    "name": str,
                    "tls": {
                        "name": str,
                    },
                },
                "ingress_docs": {
                    "name": str,
                    "tls": {
                        "name": str,
                    },
                },
                "man_repo_url": str,
            }
        }
    }

class Branch(Document):
    structure = {
        "id": int,
        "name": str,
        "state": str,
        "releases": [
            {
                "id": int,
                "version": str,
                "state": str,
                "created": str,
                "updated": str,
                "guid": str,
                "content": dict,
            }
        ]
    }

class App(Document):
    structure = {
        'legacy_id': int,
        'name': str,
        'app_deployments': [AppDeployment],
        'branches': [Branch]
    }

    use_dot_notation = True

    def to_dict(self):
        return {
            'id': str(self['_id']),
            'legacy_id': self['legacy_id'],
            'name': self['name'],
            'app_deployments': [a.to_dict() for a in self['app_deployments']],
            'branches': [b.to_dict() for b in self['branches']]
        }

class AppDocument:
    def __init__(self, connection, database, collection):
        # Register the App document with the connection
        connection.register([App])

    def get_by_id(self, id):
        # Find a document by its ID and return an App instance
        doc = collection.find_one({'_id': ObjectId(id)})
        return self._document_to_instance(doc)

    def create(self, data):
        # Create a new document from the given data and return its ID
        doc_id = collection.insert(data)
        return str(doc_id)

    def update(self, id, data):
        # Update an existing document with the given ID using the given data
        doc = collection.find_one({'_id': ObjectId(id)})
        doc.update(data)
        collection.save(doc)

    def delete(self, id):
        # Delete a document with the given ID
        collection.remove({'_id': ObjectId(id)})

    def find(self, query):
        # Find documents matching the given query and return them as an AppList object
        docs = collection.find(query)
        return AppList([self._document_to_instance(doc) for doc in docs])

    def _document_to_instance(self, doc):
        # Convert a MongoDB document to an App instance
        app = App()
        app.update(doc)
        return app

class AppList(list):
    def first_or_none(self):
        # Return the first element of the list, or None if the list is empty
        return self[0] if len(self) > 0 else None

    def last_or_none(self):
        # Return the last element of the list, or None if the list is empty
        return self[-1] if len(self) > 0 else None
