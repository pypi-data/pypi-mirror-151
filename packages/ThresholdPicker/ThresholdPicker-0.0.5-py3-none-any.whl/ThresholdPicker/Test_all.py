import unittest
from ThresholdPicker.utils import *
np.random.seed(0)
from ThresholdPicker.ThresholdPicker import ThresholdPicker as PRTC


class TestMethods(unittest.TestCase):

    def test_recall_curve(self):
        positive_probas = [.5, .6, .9, 1, 0.1]
        recall, thresholds = get_recall_threshold_curve(positive_probas, num_bins=4)
        self.assertListEqual(list(recall), [.8, .6, .4])

    def test_precission_curve(self):
        num_bins = 100
        predicted_probas = np.arange(0, 1 ,.01)
        labels = np.random.choice([0,1], num_bins)
        percission, thresholds = get_precision_threshold_curve(predicted_probas, labels, num_bins=100)
        self.assertAlmostEqual(percission.mean(), .5, delta=.1)
        self.assertEqual(num_bins, thresholds.shape[0])

    def test_recall_threshold(self):
        num_bins = 100
        predicted_probas = np.arange(0, 1 ,.01)
        labels = np.random.choice([0,1], num_bins)
        target = .4
        prtc = PRTC()
        threshold, result_recall = prtc.get_threshold(predicted_probas, labels,
                                                      target=target,
                                                      mode='recall')
        self.assertAlmostEqual(result_recall, target, delta=.01)

    def test_percision_threshold(self):
        num_bins = 100
        predicted_probas = np.arange(0, 1 ,.01)
        labels = np.random.choice([0,1], num_bins)
        target=.6
        prtc = PRTC()
        threshold, result_percision = prtc.get_threshold(predicted_probas,
                                                         labels, target=target,
                                                         mode='percision')
        self.assertAlmostEqual(result_percision, target, delta=.01)


    def test_fscore_threshold(self):
        num_bins = 100
        predicted_probas = np.arange(0, 1 ,.01)
        labels = np.random.choice([0,1], num_bins)
        target =.7
        prtc = PRTC()
        threshold, result_fscore, _ = prtc.get_threshold(predicted_probas,
                                                         labels, target=target,
                                                         mode='fscore', betta=1)
        self.assertAlmostEqual(result_fscore, target, delta=.01)


    def test_gen_optimal_return_threshold(self):
        num_bins = 100
        predicted_probas = np.arange(0, 1 ,.01)
        labels = np.random.choice([0,1], num_bins)
        prtc = PRTC()
        threshold, return_signal = prtc.gen_optimal_return_threshold(predicted_probas,
                                                                     labels,
                                                                     true_pos_value=1,
                                                                     false_pos_cost=0
                                                                     )
        self.assertAlmostEqual(threshold, 0, delta=.05)
        threshold, return_signal = prtc.gen_optimal_return_threshold(predicted_probas,
                                                                     labels,
                                                                     true_pos_value=0,
                                                                     false_pos_cost=1
                                                                     )
        self.assertAlmostEqual(threshold, 1, delta=.05)


if __name__ == '__main__':
    unittest.main()