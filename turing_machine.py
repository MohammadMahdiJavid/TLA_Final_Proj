'''
MohammadMahdi Javid


blank --> 1
final --> 1 ^ number states
'''


def main():
    '''
    101101011011 1010110101
    sigma(q1, a) = sigma(q1, a, R)
    sigma(q1, blank) = sigma(q2, blank, L)
    3
    '''
    transitions = {}
    en_turing = input()
    for en_transistion in en_turing.split("00"):
        toks = en_transistion.split("0")
        src = len(toks[0])  # 1 : q1, 11 : q2
        trans_state = len(toks[1])  # 1 : blank, 11 : a, 111 : b
        dst = len(toks[2])  # 1 : q1, 11 : q2
        rep_state = len(toks[3])  # 1 : blank, 11 : a, 111 : b
        move = len(toks[4])  # 1 : L, 2 : R
        if not src in transitions:
            transitions[src] = {}
        if not dst in transitions:
            transitions[dst] = {}
        transitions[src][trans_state] = (dst, rep_state, move)
    queries = [input() for i in range(int(input()))]
    for query in queries:
        tape = [1] if query == "" else [
            len(tok) for tok in query.split("0")]
        tape = [1] * 100 + tape + [1] * 100
        print(decode_string(1, tape, 100, len(transitions), transitions))


def decode_string(curr, tape, curr_idx, last, transitions, blank=False):
    '''
    ' ' -> 1 -> blank
    11011011 --> 2, 2, 2 --> a, a, a
    110111011 --> 2, 3, 2 --> a, b, a
    state jadid , tabdile tape, rasto chap | 1 : L, 2 : R | 1 : q1, 11 : q2 | 1 : blank, 11 : a, 111 : b | 
    '''
    if curr == last:
        return "Accepted"
    # try:
    #     if blank:
    #         if 1 in transitions[curr]:
    #             dst, rep_state, move = transitions[curr][1]
    #             return "Accepted" if dst == last else "Rejected"
    #         else:
    #             return "Rejected"
    #     if curr_idx < 0 or curr_idx >= len(tape) and blank is False:
    #         return decode_string(curr, tape, curr_idx, last, transitions, blank=True)
    if not tape[curr_idx] in transitions[curr]:
        return "Rejected"
    curr, tape[curr_idx], move = transitions[curr][tape[curr_idx]]
    curr_idx = curr_idx - 1 if move == 1 else curr_idx + 1
    return decode_string(curr, tape, curr_idx, last, transitions)
    # except:
    #     return "Rejected"


if __name__ == '__main__':
    main()
