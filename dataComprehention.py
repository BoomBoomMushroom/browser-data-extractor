# This file will make sense of data
# ex. History List -> Top Websites Visited

import json

# Utility for this file
def extractVisitCount(json):
    try:
        return int(json['visit_count'])
    except KeyError:
        return 0

# All the actual functions
def topWebsitesVisited(historyList):
    historyList.sort(key=extractVisitCount, reverse=True)
    return historyList