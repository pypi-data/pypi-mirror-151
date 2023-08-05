# coding: utf-8
import pyCGM2; LOGGER = pyCGM2.LOGGER
from pyCGM2.Anomaly import anomalyFilters
from pyCGM2.Anomaly import anomalyDetectionProcedures

def gaitEventsAnomaly(DATA_PATH,trialname):
    """
    Verify if gait events are identified correctly

    Args:
        DATA_PATH (str): folder path
        trialname (str): trial filename

    Examples:

    ```python
    analysis.gaitEventsAnomaly(DATA_PATH, "file1.c3d")
    ```

    """
    acq = btkTools.smartReader(DATA_PATH+trialname)

    madp = anomalyDetectionProcedures.GaitEventAnomalyProcedure()
    adf = anomalyFilters.AnomalyDetectionFilter(acq,trialname,madp)
    anomaly_event = adf.run()
    if anomaly_event["ErrorState"]:
        raise Exception("[pyCGM2-flow] - gait events not correctly detected in fitting trial  [%s]"%(trialname))
