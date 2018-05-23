import unittest

from deprecated.ProcessingControllers import *
from TestingTools.DataAndFunctionsForTesting import *
from TestingTools.Factories import DummyQueueFactory, UserFactory

sys.path.append('%s/TextTools/TextProcessors' % BASE)  # the directory that contains my_pkg


class IProcessingControllerUnitTests(unittest.TestCase):
    def setUp(self):
        self.queue = DummyQueueFactory()
        self.object = UserProcessingController(self.queue)
        self.user = UserFactory()

    def test_make_and_enque_result_not_none(self):
        sentenceIndex = 3
        wordIndex = 2
        text = 'taco'
        UserId = 123456789
        self.object.make_and_enque_result(sentenceIndex, wordIndex, text, UserId)

        result = self.queue.queue[0]
        self.assertIsInstance(result, Result)
        self.assertEqual(result.sentence_index, sentenceIndex)
        self.assertEqual(result.word_index, wordIndex)
        self.assertEqual(result.text, text)
        self.assertEqual(result.id, UserId)

    def test_make_and_enque_result_is_none(self):
        sentenceIndex = 3
        wordIndex = 2
        text = None
        UserId = 123456789
        self.object.make_and_enque_result(sentenceIndex, wordIndex, text, UserId)

        self.assertEqual(len(self.queue.queue), 0, "Nothing has been added to the queue")


if __name__ == '__main__':
    unittest.main()
