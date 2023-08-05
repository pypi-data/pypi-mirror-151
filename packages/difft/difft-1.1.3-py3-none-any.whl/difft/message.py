from difft.utils import current_milli_time

class MessageRequestBuilder:
    def __init__(self) -> None:
        self.message_request = dict(version=1, type='TEXT', timestamp=current_milli_time())

    def sender(self, sender):
        self.message_request.update(dict(src=sender))
        return self
    
    def to_user(self, wuid:list):
        if not isinstance(wuid, list):
            raise Exception("user must be type list")
        dest = {
            "wuid": wuid,
            "type": "USER"
            }
        self.message_request['dest'] = dest
        return self
    
    def message(self, msg):
        if 'msg' in self.message_request:
            self.message_request['msg']['body'] = msg
        else:
            self.message_request['msg'] = {'body': msg}
        return self
    
    def to_group(self, group_id):
        dest = {
            "groupID": group_id,
            "type": "GROUP"
            }
        self.message_request['dest'] = dest
        return self
    
    def at_user(self, wuid: list):
        if not isinstance(wuid, list):
            raise Exception("at user must be type list")
        if 'msg' in self.message_request:
            self.message_request['msg']['atPersons'] = wuid
        else:
            self.message_request['msg'] = {'atPersons': wuid}
        return self
    
    def timestamp_now(self):
        self.message_request['timestamp'] = current_milli_time()
        return self

    def attachment(self, attachment):
        if 'msg' in self.message_request:
            self.message_request['msg']['attachment'] = attachment
        else:
            self.message_request['msg'] = {'attachment': attachment}
        return self
    
    def quote(self, refID, text):
        if 'msg' in self.message_request:
            self.message_request['msg']['quote'] = {'refID': refID, 'text': text}
        else:
            self.message_request['msg'] = {'quote': {'refID': refID, 'text': text}}
        return self
    
    def type(self, msg_type):
        self.message_request['type'] = msg_type
        return self

    def card(self, appid, id, content, creator=None, timestamp=None):
        self.message_request['type'] = 'CARD'
        self.message_request['card'] = dict(appID=appid, id=id, content=content)
        if creator:
            self.message_request['card']['creator'] = creator
        if timestamp:
            self.message_request['card']['timestamp'] = timestamp
        return self

    def build(self):
        return self.message_request


