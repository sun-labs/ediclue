from lib.Message import Message
from lib.Segment import Segment
from lib.UNMessage import UNMessage

import json

class Generator():
    
    @staticmethod
    def getAperakFor(message: Segment) -> Segment:
        aperak = UNMessage('APERAK')
        aperak['UNH']['message_reference_number'] = 'test'
        print(json.dumps(aperak.toList()))