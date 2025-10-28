import pyboolector
from pyboolector import Boolector
from common import *

# rotation constant
rot_r = [31, 17,  0, 24] * 2
rot_s = [24, 17, 31, 16] * 2

def alzette_quasidifferential_trails(diffs, nb_bits):
    btor = Boolector()
    btor.Set_opt(pyboolector.BTOR_OPT_MODEL_GEN, 1)
    btor.Set_opt(pyboolector.BTOR_OPT_INCREMENTAL, 1)

    nb_rounds = len(diffs) - 1

    u = [btor.Var(btor.BitVecSort(nb_bits), "u%d" % i) for i in range(nb_rounds + 1)]
    v = [btor.Var(btor.BitVecSort(nb_bits), "v%d" % i) for i in range(nb_rounds + 1)]

    weight = btor.Const(0, nb_bits)
    for i in range(nb_rounds):
        a = btor.Const(diffs[i][0], nb_bits)
        b = btor.Const(diffs[i][1], nb_bits)
        c = btor.Const(diffs[i + 1][0], nb_bits)

        b  = btor.Ror(b, rot_r[i])

        u_ = u[i]
        v_ = btor.Ror(v[i + 1] ^ v[i], rot_r[i]) 

        w_ = u[i + 1] ^ btor.Rol(v[i + 1], rot_s[i])

        weight += modular_addition(
            btor, a, b, c, u_, v_, w_, nb_bits, i
        )
    
    btor.Assert(u[0] == 0)
    btor.Assert(v[0] == 0)
    btor.Assert(u[nb_rounds] == 0)
    btor.Assert(v[nb_rounds] == 0)

    return btor, weight


def compute_sign_alzette(differences, masks, word_size):
    """ Compute the sign of a quasidifferential trail for Alzette. """

    def pseudoinverseM(t):
        t = t ^ ((t << 1) % 2 ** word_size)
        return t >> 1

    def complement(t):
        return (2 ** word_size - 1) ^ t

    s = 1
    for i in range(len(masks) - 1):
        u = masks[i][0]
        v = rotl(masks[i + 1][1] ^ masks[i][1], word_size - rot_r[i], word_size)

        w = rotl(masks[i + 1][1], rot_s[i], word_size) ^ masks[i + 1][0]
        (u_, v_, _) = (u ^ w, v ^ w, u ^ v ^ w)

        (a , r) = differences[i]
        c       = differences[i + 1][0]

        b = rotl(r, word_size - rot_r[i], word_size) 

        (a_, b_, c_) = (b ^ c, a ^ c, pseudoinverseM(a ^ b ^ c))
        p1 = parity(((complement(a_) & u_) ^ (c_ & v_)) & ((complement(b_) & v_) ^ (c_ & u_)))
        p2 = parity((u_ & v_) & (c_ ^ (a_ & b_ & complement(c_))))
        s *= (-1) ** (p1 ^ p2)

    return s


# 4 rounds (weight 6)
diffs_array = []
diffs_array.append([
    (0x80000100, 0x00000080),
    (0x80000000, 0x00000000),
    (0x80000000, 0x00004000),
    (0x80004000, 0x0000c001),
    (0x80404100, 0x41004041)
])

diffs_array.append([
    (0x80000100, 0x00000080),
    (0x80000000, 0x00000000),
    (0x80000000, 0x00004000),
    (0x80004000, 0x0000c001),
    (0x80c04100, 0x410040c1)
])

diffs_array.append([
    (0x80020100, 0x00010080),
    (0x80000000, 0x00010000),
    (0x00000000, 0x00010000),
    (0x00010000, 0x00030000),
    (0x01010000, 0x00030101)
])

diffs_array.append([
    (0x80020100, 0x00010080),
    (0x80000000, 0x00010000),
    (0x00000000, 0x00010000),
    (0x00010000, 0x00030000),
    (0x03010000, 0x00030301)
])

diffs_array.append([
    (0xa0008140, 0x000040a0),
    (0xa0000000, 0x00004000),
    (0x80000000, 0x00000000),
    (0x80000000, 0x00000001),
    (0x80000100, 0x01008001)
])

diffs_array.append([
    (0x00804001, 0x80400000),
    (0x00004000, 0x80000000),
    (0x00000000, 0x80000000),
    (0x80000000, 0x80000001),
    (0x80000080, 0x80808001)
])

diffs_array.append([
    (0x00804001, 0x80400000),
    (0x00004000, 0x80000000),
    (0x00000000, 0x80000000),
    (0x80000000, 0x80000001),
    (0x80000180, 0x81808001)
])

############################# 결과 저장 ####################################
def save_results(filename, diffs, sols, word_size):
    """결과를 파일로 저장하는 함수"""
    with open(filename, "w") as f:
        f.write("Characteristic:\n")
        for (a, b) in diffs:
            f.write("    {:08x} {:08x}\n".format(a, b))

        for (weight, solution) in sols:
            s = compute_sign_alzette(diffs, solution, word_size)
            f.write("Weight: {} [{:+}]\n".format(weight, s))
            for (u, v) in solution:
                f.write("    {:08x} {:08x}\n".format(u, v))


word_size = 32
max_weight_loss = 35
for diff_idx in range(7):
    diffs = diffs_array[diff_idx]

    sols = []
    btor, weight = alzette_quasidifferential_trails(diffs, word_size)
    for w in range(max_weight_loss):
        for solution in solve_all(btor, weight, w, len(diffs) - 1, word_size):
            sols.append((w, solution))

    dir_name = "result/"
    filename = dir_name + f"diff_{diff_idx}_weight_{max_weight_loss}.txt"
    save_results(filename, diffs, sols, word_size)
