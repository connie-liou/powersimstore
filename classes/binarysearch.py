def binarySearch(data, val):
    lo, hi = 0, len(data) - 1
    best_ind = lo
    while lo <=hi:
        mid = int(lo + (hi - lo) / 2)
        if data[mid] < val:
            lo = mid + 1
        elif data[mid] > val:
            hi = mid - 1
        else:
            best_ind = mid
            break
        # check if data[mid] is closer to val than data[best_ind]
        if abs(data[mid] - val) < abs(data[best_ind] - val):
            best_ind = mid
    return best_ind

def binarySearchPointList(dataPoints, val): #takes a list of orbittimepoints and finds closest 
    lo, hi = 0, len(dataPoints) - 1
    best_ind = lo
    while lo <=hi:
        mid = int(lo + (hi - lo) / 2)
        if dataPoints[mid].totalTime < val:
            lo = mid + 1
        elif dataPoints[mid].totalTime > val:
            hi = mid - 1
        else:
            best_ind = mid
            break
        # check if data[mid] is closer to val than data[best_ind]
        if abs(dataPoints[mid].totalTime - val) < abs(dataPoints[best_ind].totalTime - val):
            best_ind = mid
    return best_ind