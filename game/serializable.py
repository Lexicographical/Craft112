import json

class Serializable:
    def getSerializables(self):
        return self.__dict__

    @staticmethod
    def serialize(object):
        if isinstance(object, Serializable):
            return json.dumps(object.getSerializables())
        else:
            return json.dumps(object)