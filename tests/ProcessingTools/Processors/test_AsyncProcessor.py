"""
Created by adam on 5/16/18
"""
__author__ = 'adam'

import sys
import unittest

import environment

sys.path.append( '%s/TextTools/TextProcessors' % environment.BASE )  # the directory that contains my_pkg

from TestingTools.DataAndFunctionsForTesting import *
from TestingTools.Factories import *

from ProcessingTools.Processors.UserProcessing import Processor

# from Servers.ClientSide import ServerQueueDropin
from TextTools.Filtration.Filters import URLFilter, UsernameFilter, PunctuationFilter, NumeralFilter, StopwordFilter
from TextTools.Replacement.Modifiers import WierdBPrefixConverter, CaseConverter
from TextTools.Processors.SingleWordProcessors import SingleWordProcessor


class AsyncProcessorUnitTests( unittest.TestCase ):
    def setUp( self ):
        self.queue = DummyQueueFactory()
        self.object = Processor()
        self.user = UserFactory()

    def test_make_result( self ):
        """Still need to test instance because each subclass uses different make_result"""
        sentenceIndex = 3
        wordIndex = 2
        text = 'taco'
        id = 123456789
        result = self.object.make_result( sentenceIndex, wordIndex, text, id )

        self.assertIsInstance( result, Result )
        self.assertEqual( result.sentence_index, sentenceIndex )
        self.assertEqual( result.word_index, wordIndex )
        self.assertEqual( result.text, text )
        self.assertEqual( result.id, id )
        self.assertEqual( result.type, 'user', "Result is correct type" )

    def test_processSentence( self ):
        sentenceIndex = 2
        userId = 123456789
        text = "Tacoes are nom. They should be eaten!"

        # call
        result = self.object._processSentence( sentenceIndex, text, userId )

        expect = [
            Result( sentence_index=2, word_index=0, text='Tacoes', id=123456789, type='user' ),
            Result( sentence_index=2, word_index=1, text='are', id=123456789, type='user' ),
            Result( sentence_index=2, word_index=2, text='nom', id=123456789, type='user' ),
            Result( sentence_index=2, word_index=3, text='.', id=123456789, type='user' ),
            Result( sentence_index=2, word_index=4, text='They', id=123456789, type='user' ),
            Result( sentence_index=2, word_index=5, text='should', id=123456789, type='user' ),
            Result( sentence_index=2, word_index=6, text='be', id=123456789, type='user' ),
            Result( sentence_index=2, word_index=7, text='eaten', id=123456789, type='user' ),
            Result( sentence_index=2, word_index=8, text='!', id=123456789, type='user' )
        ]

        self.assertEqual( len( result ), len( expect ), "Output contains the right amount of objects" )
        self.assertEqual( expect, result, "Output is expected objects" )


class AsyncProcessorFunctionalTests( unittest.TestCase ):
    def setUp( self ):
        self.numUsers = 4
        self.object = Processor()
        self.Users = [ UserFactory() for i in range( 0, self.numUsers ) ]

    def test_process_User_obj_input( self ):
        for user in self.Users:
            result = self.object.process( user )
            self.assertTrue( len( result ) > 0 )


# actual cases where the user data has not been handled
# properly
problem_cases = [ (168391959, '**SKYHIGH**'),
                  (401742354, '✌'),
                  (452749712, ':)'),
                  (1170228427, '|1104|•|0717|'),
                  (1268582460, '☀♑ · ☾♑ · ☿♐ · ♀♒ · ♂♉ · ♃♌ · ♄♑ · ♅♑ · ♆♑ · ♇♏'),
                  (1732483676, '[ ???¿¿¿???¿¿¿??? ]'),
                  (1942653919,
                   'Medical team, chiropractic team, physical therapy team.We work on spinal and joint conditions primarily the knee.'),
                  (1943096588,
                   'Lizzie. 19. In Love. My thoughts scare me. Follow if you dare.'),
                  (1943901734, 'RADIOFREQUENCE - QST-CHEPS-TENS-RECOVERY RX'),
                  (1946121392,
                   'In the fight of Pre-diabetes to prevent diabetes, survivor of dv, Fibro, Lover of #weather & #meteorology Nature Photographer,  Daughter, #Endosister, 3 Fall'),
                  (1947484375,
                   'Richmond Pickering Ltd are publishers of the My Guide series of self-help, wellness and how-to books, helping people improve their lives in some way.'),
                  (1952156365,
                   'Getting adjusted to a brand new life with a less capable body.                         Hoping to find new ways to live life to the fullest.'),
                  (1956700424,
                   'Craft Art Vintage ETSY http://t.co/V9JErLBmfL ZIBBET http://t.co/48TdGeLaWf FB http://t.co/MxdHsCFCbf RMOUSE http://t.co/qmoS7OlKwq PINT http://t.co/ZKIxVmu7g4'),
                  (1958085936,
                   'Physiotherapy, Exercise Rehabilitation, Corporate Health, Pilates'),
                  (1961129809,
                   'Montvale Advanced Center for Special Surgery is an outpatient ambulatory surgery center.'),
                  (1965229962,
                   'We are a state-of-the art center of excellence offering the highest standard of quality care with the most technologically advanced treatments.'),
                  (1966904126,
                   'Freelance writer/editor specializing in medical communications, health literacy and plain English writing.'),
                  (1967229895,
                   "#Cannabis #Tweets! If you're against #Cannabis get the fuck off my profile!! #CannabisCure #FreeTheWeed #TheGiftFromGod #HailQueenMJ #LetsGetHigh"),
                  (1971054716,
                   'Laid back! Turn up when i fell like it! Cool ass momma and G-ma going places soon ! Free DJ and Rock a.k.a Rakeem'),
                  (1974223567,
                   'Motivational speaker.  Suicide survivor, with BPD, Fibromyalgia, Addiction, & PTSD. Helping others stay strong as they travel through hell. DM me anytime!'),
                  (1977458240,
                   'I have been diagnosed with fibromyalgia, ibs, hypothyroidism, and multiple food allergies. Working on getting a second opinion about the fibro diagnosis.'),
                  (1978158529,
                   "Irish Children's Arthritis Network. A parent-run network providing support & information and advocating for best care for those affected by Juvenile Arthritis"),
                  (2147790896,
                   'Mountain Mom Adventures~ Life, love, family, photography, hunting, motorcycles, and food, not necessarily in that order. http://t.co/CuCjY3Hr2q'),
                  (2148022776,
                   'livet er ingen dans på roser, men en kamp i en tornebusk. Skriver om livet som ung og syk'),
                  (2148304566,
                   'We Change Lives Here. We treat all of your pain conditions and explore any method to help you get your life back.'),
                  (2150423437,
                   'Age 23. Suffering in Seattle. A place to vent that isnt to your friends and family.'),
                  (2151409467, '#humble #justblaze #spoonielove #lucky13'),
                  (2153422184, 'no'),
                  (2153945834,
                   'FGXPress PowerStrips are the first of their kind product that can be sold anywhere in the world. PowerStrips™ are a patented, doctor formulated and FDA approved'),
                  (2157188568,
                   'On a mission to educate the medical profession on treating patients in pain. In my experience not many know how to treat people, let alone people in pain.'),
                  (2163358988, 'Clinical case studies by clinicians'),
                  (2163604778, 'Clinical case study by clinicians'),
                  (2167298995, 'More healthcare information from innovative clinicians!'),
                  (2168963268,
                   'We are a full service pain management practice with integrated physical therapy at our locations. Your PAIN is our PRIORITY!'),
                  (2177120316,
                   'Ehlers-Danlos Syndrome Canada.\nEDS Canada provides knowledge, advocacy and support to individuals and their families living with Ehlers-Danlos Syndrome.'),
                  (2187999841,
                   "Recently diagnosed with Chronic Fatigue Syndrome and Chronic Pain, I'm trying to find a lifestyle that reduces the symptoms and makes life fulfilling.") ]


class AsyncProcessorProblemCases( unittest.TestCase ):
    def setUp( self ):
        self.object = Processor()

        filters = [
            UsernameFilter(),
            PunctuationFilter(),
            URLFilter(),
            NumeralFilter(),
            StopwordFilter()
        ]

        modifiers = [
            WierdBPrefixConverter(),
            CaseConverter()
        ]

        # First set up the object which will handle applying
        # filters and modifiers to each word
        word_processor = SingleWordProcessor()
        word_processor.add_filters( filters )
        word_processor.add_modifiers( modifiers )
        self.object.load_word_processor( word_processor )

        # take the problem case tuples and create
        # user objects with those data
        self.problemCases = [ ]
        for c in problem_cases:
            u = UserFactory()
            u.userID = c[ 0 ]
            u.description = c[ 1 ]
            self.problemCases.append( u )

    def test_cases( self ):
        for c in self.problemCases:
            r = self.object.process( c )
            print( r )
            self.assertEqual( [ ], r )

    def test_c1( self ):
        case = (1942653919,
                'Medical team, chiropractic team, physical therapy team.We work on spinal and joint conditions primarily the knee.')
        u = UserFactory()
        u.userID = case[ 0 ]
        u.description = case[ 1 ]
        expect = [ Result( sentence_index=0, word_index=0, text='medical', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=1, text='team', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=3, text='chiropractic', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=4, text='team', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=6, text='physical', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=7, text='therapy', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=8, text='team.we', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=9, text='work', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=10, text='on', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=11, text='spinal', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=12, text='and', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=13, text='joint', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=14, text='conditions', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=15, text='primarily', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=16, text='the', id=1942653919, type='user' ),
                   Result( sentence_index=0, word_index=17, text='knee', id=1942653919, type='user' ) ]

        r = self.object.process( u )
        self.assertEqual( expect, r )

    def test_c2( self ):
        """In the fight of Pre-diabetes to prevent diabetes, survivor of dv, Fibro, Lover of #weather & #meteorology
        Nature Photographer,  Daughter, #Endosister, 3 Fall """
        case = (1946121392,
                'In the fight of Pre-diabetes to prevent diabetes, survivor of dv, Fibro, Lover of #weather & #meteorology Nature Photographer,  Daughter, #Endosister, 3 Fall')

        u = UserFactory()
        u.userID = case[ 0 ]
        u.description = case[ 1 ]
        expect = [ Result( sentence_index=0, word_index=0, text='in', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=1, text='the', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=2, text='fight', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=3, text='of', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=4, text='pre-diabetes', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=5, text='to', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=6, text='prevent', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=7, text='diabetes', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=9, text='survivor', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=10, text='of', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=11, text='dv', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=13, text='fibro', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=15, text='lover', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=16, text='of', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=18, text='weather', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=21, text='meteorology', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=22, text='nature', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=23, text='photographer', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=25, text='daughter', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=28, text='endosister', id=1946121392, type='user' ),
                   Result( sentence_index=0, word_index=31, text='fall', id=1946121392, type='user' ) ]

        r = self.object.process( u )
        self.assertEqual( expect, r )
