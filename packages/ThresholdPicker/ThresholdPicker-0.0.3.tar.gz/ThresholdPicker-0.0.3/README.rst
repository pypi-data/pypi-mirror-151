The Purpose of this project is to provide a tool for Threshold optimization.
There are severalMachine learning models use by default a threshold of 0.5.
In many situations this threshold is not the optimal.
for example when the data set is unbalanced or the value of true predictions vs the
cost of false predictions are unequal.

This project provide several tools to help dealing with the threshold picking problems:
1. analyze percision and recall vs threshold
2. evaluate fscore vs threshold
3. pick best threshold for a given fscore
4. pick best threshold for a given case based on:
    -true vs false samples distribution
    -True Positives value
    -Cost of False Positives
