from lib.Segment import Group
from lib.UNSegment import UNSegment

definitions = {
    # https://www.truugo.com/edifact/d96a/aperak/
    "APERAK": Group('APERAK').structure(
        UNSegment('UNB', mandatory=True),
        UNSegment('UNH', mandatory=True),
        UNSegment('BGM', mandatory=True),
        UNSegment('DTM', max=9),
        UNSegment('FTX', max=9),
        UNSegment('CNT', max=9),
        Group('GRP1', max=9).structure(
            UNSegment('RFF', mandatory=True),
            UNSegment('DTM', max=9)
        ),
        Group('GRP2', max=9).structure(
            UNSegment('NAD', mandatory=True),
            UNSegment('CTA', max=9),
            UNSegment('COM', max=9)
        ),
        Group('GRP3', max=999).structure(
            UNSegment('ERC', mandatory=True),
            UNSegment('FTX', max=1),
            Group('GRP4', max=1).structure(
                UNSegment('RFF', mandatory=True),
                UNSegment('FTX', max=9),
            )
        ),
        UNSegment('UNT', mandatory=True),
        UNSegment('UNZ', mandatory=True)
    )
}