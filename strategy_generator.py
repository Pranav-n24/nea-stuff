from info import getLaps
from itertools import product
#actual combination generator
def stCombinations(s, m, h, n):
    result = []
    def generate(sequence, s_left, m_left, h_left, start):
        if len(sequence) == n:
            result.append("".join(sequence))
            return
        if start <= 0 and s_left > 0:
            generate(sequence + ["S"], s_left - 1, m_left, h_left, 0)
        if start <= 1 and m_left > 0:
            generate(sequence + ["M"], s_left, m_left - 1, h_left, 1)
        if start <= 2 and h_left > 0:
            generate(sequence + ["H"], s_left, m_left, h_left - 1, 2)
    generate([], s, m, h, 0)
    return result
#the final thing
def generateLegalSequence(s, m, h, mps):
    min_stints = 3 if mps else 2
    sequences = []
    for stints in range(min_stints, 5):
        sequences.append(stCombinations(s, m, h, stints))
    return sequences
#making stint length combinations
def generateStintLengths(laps, stints):
    average_length = laps // stints
    possible_pit_laps = [range(average_length*i-5, average_length*i+6) for i in range(1, stints)]
    strategies = []
    for pit_laps in product(*possible_pit_laps): 
        stint_lengths = [] 
        previous_pit = 0
        for pit_lap in pit_laps: 
            stint_lengths.append(pit_lap-previous_pit) 
            previous_pit = pit_lap
        stint_lengths.append(laps-previous_pit)
        strategies.append(stint_lengths)
    return strategies
#merging both
def generateCompleteStrategySequence(s, m, h, mps, track): 
    laps = getLaps(track)
    min_stints = 3 if mps else 2
    stints = []
    for i in range(min_stints, 5, 1):
        tstints = generateStintLengths(laps, i)
        stints.append(tstints)
    sequence = generateLegalSequence(s, m, h, mps)
    #sequence -> nested list: [[2 stints], [3 stints], [4 stints]] (tyre combinations) 2, 3, 4 stints: ["", "", "" ......]
    stl = []
    for i in sequence:
        stl.append(len(i[0]))
    stintlengths = []
    for i in stl:
        x = generateStintLengths(laps, i)
        stintlengths.append(x)
    #stintlengths -> nested list: [[2 stints], [3 stints], [4 stints]] (stint lengths) 2, 3, 4 stints: [[], [], [].......]
    for subsequence in sequence:
        stint = stintlengths[sequence.index(subsequence)]
        