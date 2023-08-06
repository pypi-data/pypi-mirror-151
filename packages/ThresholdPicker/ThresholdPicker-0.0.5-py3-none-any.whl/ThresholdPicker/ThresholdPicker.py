from ThresholdPicker.utils import get_recall_threshold_curve, get_precision_threshold_curve
import numpy as np


class ThresholdPicker():

    def __init__(self, num_bins=1000, betta=2):
        self.num_bins = num_bins
        self.betta = betta
        self.values = None


    def get_curves(self, probas, labels):
        recall_rate, _ = get_recall_threshold_curve(probas[labels > 0],
                                                    num_bins=self.num_bins)
        precision_rate, bins = get_precision_threshold_curve(probas, labels,
                                                             num_bins=self.num_bins)
        return recall_rate, precision_rate, bins

    def get_threshold(self, probas, labels, target, mode='recall', betta=1):
        """
        calculate the threshold that would return the closest valuse to
        the desired recall/percision.
        :param target: float, between 0 and 1  the desired recall/percision/fscore
        :param mode: str, defines wheather to return threhsold for recall, percision or
        :param betta: float, the betta value for fscore calculation default is 2.
        fscore
        :return: threshold float, between 0 and 1, score float between 0 and 1.
        """
        if mode == 'recall':
            recalls, thresholds = get_recall_threshold_curve(probas[labels > 0])
            diffs = np.abs(recalls - target)
            min_index = np.argmin(diffs)
            return thresholds[min_index], recalls[min_index]

        if mode == 'percision':
            percisions, thresholds = get_recall_threshold_curve(
                probas[labels > 0], num_bins=self.num_bins)
            diffs = np.abs(percisions - target)
            min_index = np.argmin(diffs)
            return thresholds[min_index], percisions[min_index]

        if mode == 'fscore':
            recalls, percisions, thresholds = self.get_curves(probas, labels)
            fscores = self.calc_fscore(percisions, recalls, betta)
            diffs = np.abs(fscores - target)
            min_index = np.argmin(diffs)
            return thresholds[min_index], fscores[min_index], fscores


    @staticmethod
    def calc_fscore(percisions, recalls, betta):
        return (1 + betta**2) * (percisions * recalls) / (betta ** 2 * percisions + recalls)

    @staticmethod
    def gen_true_pos_signal(recalls, positive_rate):
        return recalls*positive_rate

    @staticmethod
    def gen_false_pos_signal(recalls, percisions, true_rate):
        return (percisions**-1 - 1) * recalls * true_rate

    def gen_mean_return_signal(self, persicoins, recalls, true_rate,
                               true_pos_value, false_pos_cost):
        true_pos = self.gen_true_pos_signal(recalls, true_rate)
        false_pos = self.gen_false_pos_signal(recalls, persicoins, true_rate)
        return true_pos*true_pos_value - false_pos*false_pos_cost


    def gen_optimal_return_threshold(self, probas, labels,
                                 true_pos_value, false_pos_cost):
        true_rate = labels.mean()
        recalls, percisions, thresholds = self.get_curves(probas, labels)
        return_threhold_sig = self.gen_mean_return_signal(percisions, recalls,
                                                          true_rate,
                                                          true_pos_value,
                                                          false_pos_cost)
        best_threshold_index = np.argmax(return_threhold_sig)
        return thresholds[best_threshold_index], return_threhold_sig