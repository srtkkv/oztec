import sys
import win32evtlogutil
import win32evtlog
import time


DUMMY_EVT_APP_NAME = "Dummy Application"
DUMMY_EVT_ID = 7040  # Got this from another event
DUMMY_EVT_CATEG = 9876
DUMMY_EVT_STRS = ["Dummy event string {0:d}".format(item) for item in range(5)]
DUMMY_EVT_DATA = b"Dummy event data"
win32evtlogutil.ReportEvent(DUMMY_EVT_APP_NAME, DUMMY_EVT_ID, eventCategory=DUMMY_EVT_CATEG,
                            eventType=win32evtlog.EVENTLOG_WARNING_TYPE, strings=DUMMY_EVT_STRS,
                            data=DUMMY_EVT_DATA)