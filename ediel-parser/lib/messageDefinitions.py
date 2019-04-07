from lib.Segment import Group
from lib.UNSegment import UNSegment

#Segment(seg.get('UNH'), mandatory=True, max=9)

#seg.get('UNH').props(mandatory=True, max=9)
#seg.get('UNH')
# test = Segment.create_from(seg.get('UNH'), mandatory=True, max=9)

definitions = {
    "APERAK": Group('APERAK').add(
        UNSegment('UNH', mandatory=True),
        UNSegment('BGM', mandatory=True),
        UNSegment('DTM', max=9),
        UNSegment('FTX', max=9),
        UNSegment('CNT', max=9),
        Group('GRP1', max=9).add(
            UNSegment('RFF', mandatory=True),
            UNSegment('DTM', max=9)
        ),
        Group('GRP2', max=9).add(
            UNSegment('NAD', mandatory=True),
            UNSegment('CTA', max=9),
            UNSegment('COM', max=9)
        ),
        Group('GRP3', max=999).add(
            UNSegment('ERC', mandatory=True),
            UNSegment('FTX', max=1),
            Group('GRP4', max=1).add(
                UNSegment('RFF', mandatory=True),
                UNSegment('FTX', max=9),
            )
        ),
        UNSegment('UNT', mandatory=True)
    )
}