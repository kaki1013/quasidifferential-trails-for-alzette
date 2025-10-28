"""
[값은 안 맞음 : 위 문자열에서 아래 형태로 변경]

Best Trail for 4 rounds:
Trail:
  Path:
    Node 1: [0x00804001, 0x00800001, 0x00004000]
    Node 2: [0x00004000, 0x00004000, 0x00000000]
    Node 3: [0x00000000, 0x80000000, 0x80000000]
    Node 4: [0x80000000, 0x00000180, 0x80000180]
  Probabilities:
    [3, 1, 0, 2]
  Total Probability: 6

-> 

diffs = [
    (0x00804001, 0x80400000),
    (0x00004000, 0x80000000),
    (0x00000000, 0x80000000),
    (0x80000000, 0x80000001),
    (0x80000180, 0x81808001)
]

"""
######################## parameters ###########################
rot_r = [31, 17,  0, 24] * 2
rot_s = [24, 17, 31, 16] * 2

######################## helper ###########################
def ROR(x, r):
    """32-bit right rotate"""
    r &= 31  # 회전량을 0~31로 제한
    return ((x >> r) | (x << (32 - r))) & 0xFFFFFFFF

def ROL(x, r):
    """32-bit left rotate"""
    r &= 31
    return ((x << r) | (x >> (32 - r))) & 0xFFFFFFFF

def alpha_beta_gamma_to_abcd(alpha_beta_gamma, round):
    alpha, beta, gamma = alpha_beta_gamma
    r, s = rot_r[round], rot_s[round]
    a, b, c, d = alpha, ROL(beta, r), gamma, ROL(beta, r) ^ ROR(gamma, s)
    return a, b, c, d

def hex_format(a):
    h = hex(a)[2:]
    return '0x' + (8-len(h)) * '0' + h

######################## parsing trail ###########################
def trail_to_arr(s):
    arr = []
    for line in s.split('\n'):
        if 'Node' in line:
            l, r = line.index('[')+1, line.index(']')
            alpha_beta_gamma_str_arr = line[l:r].split(',')
            alpha_beta_gamma_arr = list(map(lambda x: int(x, 16), alpha_beta_gamma_str_arr))
            arr.append(alpha_beta_gamma_arr)
    return arr

s = """Best Trail for 4 rounds:
Trail:
  Path:
    Node 1: [0x00804001, 0x00800001, 0x00004000]
    Node 2: [0x00004000, 0x00004000, 0x00000000]
    Node 3: [0x00000000, 0x80000000, 0x80000000]
    Node 4: [0x80000000, 0x00000180, 0x80000180]
  Probabilities:
    [3, 1, 0, 2]
  Total Probability: 6"""
round = 4

arr = trail_to_arr(s)
######################## checking connectivity between differences ###########################
def verify(arr, round):
    for i in range(round-1):
        curr = i % 4
        nxt = (i+1) % 4

        a, b, c, d = alpha_beta_gamma_to_abcd(arr[curr], curr)
        a_, b_, c_, d_ = alpha_beta_gamma_to_abcd(arr[nxt], nxt)

        # inter
        assert (c == a_)
        assert (d == b_)

        # intra
        assert (b ^ d == ROR(c, rot_s[i]))
        assert (b_ ^ d_ == ROR(c_, rot_s[i+1]))

verify(arr, round)
######################## converting format ###########################
def convert_trail(arr, round=4):
    diffs = []
    for i in range(round):
        a, b, _, __ = alpha_beta_gamma_to_abcd(arr[i], i)
        diffs.append((a, b))
    _, __, c, d = alpha_beta_gamma_to_abcd(arr[round-1], round-1)
    diffs.append((c, d))
    return diffs

diffs = convert_trail(arr, round)
######################## printing converted trail ###########################
def print_trail(diffs):
    print("diffs = [")
    for a, b in diffs[:-1]:
        print(f"    ({hex_format(a)}, {hex_format(b)}),")
    print(f"    ({hex_format(diffs[-1][0])}, {hex_format(diffs[-1][1])})")
    print("]")

print_trail(diffs)

######################## multiple trails ###########################
s = """Best Trail for 4 rounds:
Trail:
  Path:
    Node 1: [0x80000100, 0x00000100, 0x80000000]
    Node 2: [0x80000000, 0x00000000, 0x80000000]
    Node 3: [0x80000000, 0x00004000, 0x80004000]
    Node 4: [0x80004000, 0x00c00100, 0x80404100]
  Probabilities:
    [1, 0, 1, 4]
  Total Probability: 6

Best Trail for 4 rounds:
Trail:
  Path:
    Node 1: [0x80000100, 0x00000100, 0x80000000]
    Node 2: [0x80000000, 0x00000000, 0x80000000]
    Node 3: [0x80000000, 0x00004000, 0x80004000]
    Node 4: [0x80004000, 0x00c00100, 0x80c04100]
  Probabilities:
    [1, 0, 1, 4]
  Total Probability: 6

Best Trail for 4 rounds:
Trail:
  Path:
    Node 1: [0x80020100, 0x00020100, 0x80000000]
    Node 2: [0x80000000, 0x80000000, 0x00000000]
    Node 3: [0x00000000, 0x00010000, 0x00010000]
    Node 4: [0x00010000, 0x03000000, 0x01010000]
  Probabilities:
    [2, 0, 1, 3]
  Total Probability: 6

Best Trail for 4 rounds:
Trail:
  Path:
    Node 1: [0x80020100, 0x00020100, 0x80000000]
    Node 2: [0x80000000, 0x80000000, 0x00000000]
    Node 3: [0x00000000, 0x00010000, 0x00010000]
    Node 4: [0x00010000, 0x03000000, 0x03010000]
  Probabilities:
    [2, 0, 1, 3]
  Total Probability: 6

Best Trail for 4 rounds:
Trail:
  Path:
    Node 1: [0xa0008140, 0x00008140, 0xa0000000]
    Node 2: [0xa0000000, 0x20000000, 0x80000000]
    Node 3: [0x80000000, 0x00000000, 0x80000000]
    Node 4: [0x80000000, 0x00000100, 0x80000100]
  Probabilities:
    [4, 1, 0, 1]
  Total Probability: 6

Best Trail for 4 rounds:
Trail:
  Path:
    Node 1: [0x00804001, 0x00800001, 0x00004000]
    Node 2: [0x00004000, 0x00004000, 0x00000000]
    Node 3: [0x00000000, 0x80000000, 0x80000000]
    Node 4: [0x80000000, 0x00000180, 0x80000080]
  Probabilities:
    [3, 1, 0, 2]
  Total Probability: 6

Best Trail for 4 rounds:
Trail:
  Path:
    Node 1: [0x00804001, 0x00800001, 0x00004000]
    Node 2: [0x00004000, 0x00004000, 0x00000000]
    Node 3: [0x00000000, 0x80000000, 0x80000000]
    Node 4: [0x80000000, 0x00000180, 0x80000180]
  Probabilities:
    [3, 1, 0, 2]
  Total Probability: 6"""
round = 4

lines = s.split('\n')
start_idx = [i for i in range(len(lines)) if 'Best' in lines[i]]
separated_trails = ['\n'.join(lines[start_idx[i] : start_idx[i+1]]) for i in range(len(start_idx)-1)]
separated_trails.append('\n'.join(lines[start_idx[-1] : ]))

print("######################## multiple trails ###########################")
for separated_trail in separated_trails:
    ######################## parsing trail ###########################
    arr = trail_to_arr(separated_trail)

    ######################## checking connectivity between differences ###########################
    # for i in range(4):
    #     curr = i % 4
    #     nxt = (i+1) % 4

    #     a, b, c, d = alpha_beta_gamma_to_abcd(arr[curr], curr)
    #     a_, b_, c_, d_ = alpha_beta_gamma_to_abcd(arr[nxt], nxt)

    #     print(i)
    #     assert (c == a_)
    #     assert (d == b_)

    #     assert (b ^ d == ROR(c, rot_s[curr]))
    #     assert (b_ ^ d_ == ROR(c_, rot_s[nxt]))

    ######################## converting format ###########################
    diffs = convert_trail(arr, round)

    ######################## printing converted trail ###########################
    print_trail(diffs)
    print()