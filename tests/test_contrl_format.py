import json
import unittest

from ediel_parser.lib.EDIParser import EDIParser
from ediel_parser.lib.UNSegment import UNSegment
from tests.utils import get_tag


class TestEdielParser(unittest.TestCase):
    edi = (
        "UNA:+.? 'UNB+UNOC:3+33333:ZZ+44444:ZZ+111008:1607+3314+ +23-DDQ-E66-S++1'UNH+1+UTILTS:D:02B:UN:E5SE1B'"
        "BGM+E66::260+205436160319+9+AB'DTM+137:201110081503:203'DTM+735:?+0100:406'MKS+23+E02::260'"
        "NAD+MS+33333:SVK:260'NAD+MR+44444:SVK:260'NAD+DDQ'IDE+24+MD200205832134'LOC+172+735999888777777778::9"
        "'LOC+239+TES:SVK:260'LIN+++8716867000030:::9'DTM+324:201109010000201110010000:719'"
        "DTM+597:201110010000:203'DTM+354:1:802'STS+7++E88::260'MEA+AAZ++KWH'RFF+TN:890123'"
        "CCI+++E12::260'CAV+E17::260'SEQ++1'RFF+AES:101'RFF+MG:M-3333'QTY+220:1234'DTM+597:201109010000:203'"
        "CCI+++E22::260'CAV+E27::260'SEQ++2'RFF+AES:101'QTY+220:2234'DTM+597:201110010000:203'CCI+++E22::260"
        "'CAV+E27::260'SEQ++3'QTY+136:1000'UNT+xxx+1'UNZ+1+3314'"
    )
    output_format = "edi"
    test_ediel = "99999"
    test_country = "Uzbekistan"

    def runTest(self):
        ediel_parser = EDIParser(self.edi,
                                 self.output_format,
                                 self.test_ediel,
                                 self.test_country)
        contrl = ediel_parser.create_contrl()

        unb = get_tag(contrl, "UNB")
        self.assertEqual(
            unb['interchange_sender']['sender_identification'].value,
            self.test_ediel
        )
        self.assertEqual(
            unb['interchange_recipient']['recipient_identification'].value,
            ediel_parser.segments['UNB']['interchange_sender']['sender_identification'].value
        )
        self.assertEqual(
            unb['application_reference'].value,
            ediel_parser.segments['UNB']['application_reference'].value
        )