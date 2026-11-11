from info import getLaps
#user input
def isValidScSequence(start, length, track):
    start = list(map(int, start.split()))
    length = list(map(int, length.split()))
    if len(start) != len(length):
        return False
    lim = getLaps(track)
    SClaps = []
    for i in range(len(start)):
        st = start[i]
        ln = length[i]
        for j in range(ln):
            SClaps.append(st)
            st += 1
    if min(SClaps) >= 1 and max(SClaps) <= lim and len(SClaps) == len(set(SClaps)):
        return True
    return False
#not a user input
def isValidPitSequence(laps, ncomp, track):
    lim = getLaps(track)
    if min(laps) > 1 and max(laps) <= lim and len(laps) <= ncomp-1 and len(laps) == len(set(laps)):
        return True
    return False