# This file will make sense of data
# ex. History List -> Top Websites Visited

import json

def extractVisitCount(json):
    try:
        return int(json['visit_count'])
    except KeyError:
        return 0



def topWebsitesVisited(historyList):
    historyList.sort(key=extractVisitCount, reverse=True)
    return historyList