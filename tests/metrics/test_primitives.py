import unittest

from torch.autograd import Variable

from bink.metrics import Loss, Epoch, CategoricalAccuracy

import torch


class TestLoss(unittest.TestCase):
    def setUp(self):
        self._state = {
            'loss': torch.FloatTensor([2.35])
        }
        self._metric = Loss()

    def test_train_process(self):
        self._metric.train()
        result = self._metric.process(self._state)
        self.assertAlmostEqual(2.35, result[0], 3, 0.002)

    def test_validate_process(self):
        self._metric.eval()
        result = self._metric.process(self._state)
        self.assertAlmostEqual(2.35, result[0], 3, 0.002)


class TestEpoch(unittest.TestCase):
    def setUp(self):
        self._state = {
            'epoch': 101
        }
        self._metric = Epoch()

    def test_train_process(self):
        self._metric.train()
        result = self._metric.process(self._state)
        self.assertEqual(101, result)

    def test_validate_process(self):
        self._metric.eval()
        result = self._metric.process(self._state)
        self.assertEqual(101, result)


class TestCategoricalAccuracy(unittest.TestCase):
    def setUp(self):
        self._state = {
            'y_true':Variable(torch.LongTensor([0, 1, 2, 2, 1])),
            'y_pred':Variable(torch.FloatTensor([
                [0.9, 0.1, 0.1], # Correct
                [0.1, 0.9, 0.1], # Correct
                [0.1, 0.1, 0.9], # Correct
                [0.9, 0.1, 0.1], # Incorrect
                [0.9, 0.1, 0.1], # Incorrect
            ]))
        }
        self._targets = [1, 1, 1, 0, 0]
        self._metric = CategoricalAccuracy()

    def test_train_process(self):
        self._metric.train()
        result = self._metric.process(self._state)
        for i in range(0, len(self._targets)):
            self.assertEqual(result[i], self._targets[i],
                             msg='returned: ' + str(result[i]) + ' expected: ' + str(self._targets[i])
                                 + ' in: ' + str(result))

    def test_validate_process(self):
        self._metric.eval()
        result = self._metric.process(self._state)
        for i in range(0, len(self._targets)):
            self.assertEqual(result[i], self._targets[i],
                             msg='returned: ' + str(result[i]) + ' expected: ' + str(self._targets[i])
                                 + ' in: ' + str(result))