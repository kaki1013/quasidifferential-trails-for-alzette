"""
{cases{
c _{6} +c _{15} +c _{25} +c _{28} +c _{29} =0#
c _{5} +c _{7} +c _{8} +c _{10} +c _{14} +c _{15} +c _{23} +c _{25} +c _{27} +c _{28} +c _{29} =0#
c _{4} +c _{5} +c _{6} +c _{15} +c _{25} +c _{28} +c _{29} =0#
c _{6} +c _{15} +c _{22} +c _{23} +c _{25} +c _{28} +c _{29} =0#
c _{6} +c _{9} +c _{13} +c _{22} +c _{24} +c _{26} +c _{27} =1#
c _{13} +c _{22} +c _{24} +c _{25} +c _{26} +c _{27} =1#
c _{6} +c _{9} +c _{13} +c _{22} +c _{24} +c _{26} +c _{27} =0#
c _{13} +c _{21} +c _{23} +c _{25} +c _{26} +c _{27} =0
}}
"""
import numpy as np

# 계수 행렬 (각 방정식의 c_i 계수)
# c1~c29 중 문제에서 등장하는 변수만 다룸
# 등장 변수: 4,5,6,7,8,9,10,13,14,15,21,22,23,24,25,26,27,28,29
# 총 20개 변수

vars_index = [4,5,6,7,8,9,10,13,14,15,21,22,23,24,25,26,27,28,29]
n_vars = len(vars_index)
var_to_idx = {v:i for i,v in enumerate(vars_index)}

# 식 구성 (각 줄은 계수 + 상수항)
equations = [
    # c6 + c15 + c25 + c28 + c29 = 0
    ([6,15,25,28,29], 0),
    # c5 + c7 + c8 + c10 + c14 + c15 + c23 + c25 + c27 + c28 + c29 = 0
    ([5,7,8,10,14,15,23,25,27,28,29], 0),
    # c4 + c5 + c6 + c15 + c25 + c28 + c29 = 0
    ([4,5,6,15,25,28,29], 0),
    # c6 + c15 + c22 + c23 + c25 + c28 + c29 = 0
    ([6,15,22,23,25,28,29], 0),
    # c6 + c9 + c13 + c22 + c24 + c26 + c27 = 1
    ([6,9,13,22,24,26,27], 1),
    # c13 + c22 + c24 + c25 + c26 + c27 = 1
    ([13,22,24,25,26,27], 1),
    # c6 + c9 + c13 + c22 + c24 + c26 + c27 = 0
    ([6,9,13,22,24,26,27], 0),
    # c13 + c21 + c23 + c25 + c26 + c27 = 0
    ([13,21,23,25,26,27], 0),
]

# 계수행렬(A)과 상수벡터(b) 구성
A = np.zeros((len(equations), n_vars), dtype=int)
b = np.zeros(len(equations), dtype=int)

for i, (vars_, val) in enumerate(equations):
    for v in vars_:
        A[i, var_to_idx[v]] = 1
    b[i] = val

# 가우스 소거법 mod 2
def gauss_mod2(A, b):
    A = A.copy()
    b = b.copy()
    n, m = A.shape
    row = 0
    for col in range(m):
        # 피벗 찾기
        pivot = None
        for r in range(row, n):
            if A[r, col] == 1:
                pivot = r
                break
        if pivot is None:
            continue
        # 행 교환
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]
            b[[row, pivot]] = b[[pivot, row]]
        # 다른 행 소거
        for r in range(n):
            if r != row and A[r, col] == 1:
                A[r] ^= A[row]
                b[r] ^= b[row]
        row += 1
        if row == n:
            break
    return A, b

A_r, b_r = gauss_mod2(A, b)

# 결과 출력
print("단순화된 식 (mod 2):")
for i in range(len(b_r)):
    if not A_r[i].any() and b_r[i]==0:
        continue
    eq_terms = [f"c{vars_index[j]}" for j in range(n_vars) if A_r[i,j]==1]
    eq_str = " + ".join(eq_terms) if eq_terms else "0"
    print(f"{eq_str} = {b_r[i]}")
