# ThresholdPicker
## A Tool for Optimizing Model Threshold.
Model Threshold is for most models set to a default of 0.5.
Inmany cases your model performance can be imporved by selecting another threshold.
The Purpose of this project is to provide a tool for optimal Threshold picking.<br>
*This tool is designed to work only with Binary Calssifiers*.<br>

The tool currently supports the following scenarios:<br><br>
**1. Balance True-Positive and False-Positive rates for Maximal Return.** <br>
For Example:<br> If the value of each TP is 10\$ and the 
cost of every FP is 2\$ and your data has 20% **True** vs 80% **False** labels.<br>
You can use this tool to optimize the threshold so that your model will
return the maximal average income.
<br>Usage Example:


    from ThresholdPicker.utils import *
    from ThresholdPicker.ThresholdPicker import ThresholdPicker as PRTC
    # simulate model probabilities and labels
    predicted_probas = np.arange(0, 1 ,.01)
    labels = np.random.choice([0,1], num_bins)
    prtc = PRTC()
    threshold, _ = prtc.gen_optimal_return_threshold(predicted_probas,
                                                     labels,
                                                     true_pos_value=10,
                                                     false_pos_cost=2
                                                     ) 
                                                     
<br>**2. Pick Threshold by Recall:**
   in case you need to configure the model to return a 
   specific recall score. <br>
   You can run the ThresholdPicker with a labeled Validation 
   set and receive the threshold that would give the recall 
   closest to the the one you specified. Usage Example:
   
    threshold, _ = get_threshold(predicted_probas,
                                 labels, target=target,
                                 mode='recall', betta=1) 
   
<br>**3. Pick Threshold by Percision:**<br>
   in case you need to configure the model to return a 
   specific recall score. <br>
   You can run the ThresholdPicker with a labeled Validation 
   set and receive the threshold that would give the recall 
   closest to the the one you specified. Usage Example:
   
    threshold, _ = get_threshold(predicted_probas,
                                 labels, target=target,
                                 mode='percision', betta=1) 
   
<br>**4. Pick Threshold by F-Score:**<br>
   in case you need to configure the model to return a 
   specific recall score. <br>
   You can run the ThresholdPicker with a labeled Validation 
   set and receive the threshold that would give the recall 
   closest to the the one you specified. Usage Example:
   
    betta=1 # can peak any betta 
    threshold, _ = get_threshold(predicted_probas,
                                 labels, target=target,
                                 mode='fscore', betta=betta)
   
<br>**5. Pick Threshold for maximal F-Score:**<br>
in progress