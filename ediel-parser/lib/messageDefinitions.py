from lib.segmentDefinitions import definitions as seg
from lib.Message import Message
from lib.Segment import Segment, Group

definitions = {
    "APERAK": Message().structure([
        Message(seg.get('UNH'), mandatory=True),
        Message(seg.get('BGM'), mandatory=True),
        Message(seg.get('DTM'), max=9),
        Message(seg.get('FTX'), max=9),
        Message(seg.get('CNT'), max=9),
        Message(Group('GRP1'), max=9).structure([
            Message(seg.get('RFF'), mandatory=True),
            Message(seg.get('DTM'), max=9)
        ]),
        Message(Group('GRP2'), max=9).structure([
            Message(seg.get('NAD'), mandatory=True),
            Message(seg.get('CTA'), max=9),
            Message(seg.get('COM'), max=9)
        ]),
        Message(Group('GRP3'), max=999).structure([
            Message(seg.get('ERC'), mandatory=True),
            Message(seg.get('FTX'), max=1),
            Message(Group('GRP4'), max=1).structure([
                Message(seg.get('RFF'), mandatory=True),
                Message(seg.get('FTX'), max=9),
            ])
        ]),
        Message(seg.get('UNT'), mandatory=True)
    ])
}