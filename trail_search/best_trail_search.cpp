/*
Best Trail for 4 rounds:
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
  Total Probability: 6

실행 시간: 38.4076 초
*/

#include <iostream>
#include <cstdint>
#include <vector>
#include <array>
#include <iomanip> // setw, setfill, hex, dec 사용을 위해 필요
#include <chrono>  // 시간 측정을 위한 헤더

#define ROR(x,r) (((x)>>(r)) | ((x)<<(32-(r))))
#define ROL(x,r) (((x)<<(r)) | ((x)>>(32-(r))))

using namespace std;

using diff = uint32_t; 
using node = array<diff, 3>;

// --------------------------- Trail 구조체 ---------------------------
struct trail {
    vector<node> path;
    vector<uint32_t> probability;
    uint32_t total_probability;     // -log2(pr) : 작은 trail 찾아야 함

    // 생성자
    trail(const vector<node>& p = {}, const vector<uint32_t>& probs = {}, uint32_t total_prob = 0)
        : path(p), probability(probs), total_probability(total_prob) {}
};

// --------------------------- 출력 오버로딩 ---------------------------
ostream& operator<<(ostream& os, const trail& t) {
    os << "Trail:\n";
    os << "  Path:\n";
    for (size_t i = 0; i < t.path.size(); ++i) {
        os << "    Node " << (i+1) << ": [";
        for (size_t j = 0; j < t.path[i].size(); ++j) {
            os << "0x" << hex << setw(8) << setfill('0') << t.path[i][j];
            if (j < t.path[i].size() - 1) os << ", ";
        }
        os << dec << "]\n"; // 10진수 포맷으로 되돌림
    }

    os << "  Probabilities:\n    [";
    for (size_t i = 0; i < t.probability.size(); ++i) {
        os << t.probability[i];
        if (i < t.probability.size() - 1) os << ", ";
    }
    os << "]\n";

    os << "  Total Probability: " << t.total_probability << '\n';

    return os;
}

// --------------------------- 헬퍼 함수들 ---------------------------
// 해밍 웨이트 계산: 비트 수 세기
inline int hamming_weight(uint32_t x) {
#if defined(__GNUG__)
    return __builtin_popcount(x);
#else
    int count = 0;
    while (x) { count += x & 1; x >>= 1; }
    return count;
#endif
}

// eq(x, y, z): 세 값이 모두 같은 비트 위치에 대해 1을 반환
uint32_t eq(uint32_t x, uint32_t y, uint32_t z) {
    // -x = ~x + 1, ~x = -x-1
    return ((~x ^ y) & (~x ^ z));
}

// xdp((α, β, γ)) 계산
uint32_t xdp(diff alpha, diff beta, diff gamma, int n) {
    uint32_t mask = (1ULL << n) - 1;
    uint32_t eq_mask = eq(alpha, beta, gamma);

    // Step 1: valid 확인
    uint32_t eq_cond = ((eq_mask << 1) & mask) | 1;     // shift 됐으므로 LSB 에 대한 eq_mask는 항상 1
    uint32_t xor_cond = alpha ^ beta ^ gamma ^ ((alpha << 1) & mask);

    if ((eq_cond & xor_cond) != 0)
        return UINT32_MAX - 10000;  // inf 대신.. + overflow 피하기 위해 UINT32_MAX 보다 조금 더 작게

    // Step 2: xdp 값 계산
    uint32_t hw = hamming_weight((~eq_mask) & (mask >> 1));  // x[n-1] 제외 (mask >> 1)
    return hw; // 1.0 / (1U << hw);
}


// --------------------------- 차분 경로 탐색 ---------------------------
// 전역 변수
int n, w; 
trail best_trail_global;
vector<uint32_t> B;             // 각 라운드별 best probability 저장
uint32_t Bn_bar;                // underestimate of best probability
trail T = trail();              // stack

// start index = 1 & 4라운드 이후는 반복됨
int rot_r[9] = {0, 31, 17,  0, 24, 31, 17,  0, 24};
int rot_s[9] = {0, 24, 17, 31, 16, 24, 17, 31, 16};

// 모듈러 덧셈 후 다음 round 입력 계산
void next_round_inputs(const node& alpha_beta_gamma, node& next_alpha_beta_gamma, int round) {
    diff alpha = alpha_beta_gamma[0];
    diff beta  = alpha_beta_gamma[1];
    diff gamma = alpha_beta_gamma[2];
    
    next_alpha_beta_gamma[0] = gamma;                           // αr+1 = γr >> r1
    diff tmp_diff = ROL(beta, rot_r[round]) ^ ROR(gamma, rot_s[round]);
    next_alpha_beta_gamma[1] = ROR(tmp_diff, rot_r[round+1]);   // βr+1 = γr ⊕ (βr << r2)
    next_alpha_beta_gamma[2] = 0;                               // γr+1 = 0
}

// 현재 라운드에서 비트 탐색
void BestDiffSearch(int r, int i, node alpha_beta_gamma) {
    if (r > n) return; // 종료 조건

    if (r == 1 && r != n) {
        // 첫 번째 라운드
        if (i == w) {
            uint32_t pr = xdp(alpha_beta_gamma[0], alpha_beta_gamma[1], alpha_beta_gamma[2], w);

            T.path.push_back(alpha_beta_gamma);
            T.probability.push_back(pr);
            T.total_probability += pr;

            node next_abg;
            next_round_inputs(alpha_beta_gamma, next_abg, r);
            BestDiffSearch(r + 1, 0, next_abg);
            
            T.path.pop_back();
            T.probability.pop_back();
            T.total_probability -= pr;
        } else {
            for (int ja = 0; ja <= 1; ++ja)
                for (int jb = 0; jb <= 1; ++jb)
                    for (int jg = 0; jg <= 1; ++jg) {
                        uint32_t mask = 1U << i;
                        node next = alpha_beta_gamma;
                        if (ja) next[0] |= mask; else next[0] &= ~mask;
                        if (jb) next[1] |= mask; else next[1] &= ~mask;
                        if (jg) next[2] |= mask; else next[2] &= ~mask;
                        
                        uint32_t pr_tilde = xdp(next[0] & ((1U << (i+1))-1),
                                                next[1] & ((1U << (i+1))-1),
                                                next[2] & ((1U << (i+1))-1),
                                                i+1);
                        if (pr_tilde + B[n-1] <= Bn_bar) {  // Note : xdp means minus log (ineq. direction)
                            BestDiffSearch(r, i + 1, next);
                        }
                    }
        }
    } else if (r > 1 && r != n) {
        // 중간 라운드
        if (i == w) {
            uint32_t pr = xdp(alpha_beta_gamma[0], alpha_beta_gamma[1], alpha_beta_gamma[2], w);

            T.path.push_back(alpha_beta_gamma);
            T.probability.push_back(pr);
            T.total_probability += pr;

            node next_abg;
            next_round_inputs(alpha_beta_gamma, next_abg, r);
            BestDiffSearch(r + 1, 0, next_abg);

            T.path.pop_back();
            T.probability.pop_back();
            T.total_probability -= pr;
        } else {
            for (int jg = 0; jg <= 1; ++jg) {
                uint32_t mask = 1U << i;
                node next = alpha_beta_gamma;
                if (jg) next[2] |= mask; else next[2] &= ~mask;

                uint32_t pr_tilde = xdp(next[0] & ((1U << (i+1))-1),
                                        next[1] & ((1U << (i+1))-1),
                                        next[2] & ((1U << (i+1))-1),
                                        i+1);

                if (T.total_probability + pr_tilde + B[n-r] <= Bn_bar) {
                    BestDiffSearch(r, i + 1, next);
                }
            }
        }
    } else if (r == n) {
        // 마지막 라운드
        if (i == w) {
            uint32_t pr = xdp(alpha_beta_gamma[0], alpha_beta_gamma[1], alpha_beta_gamma[2], w);

            T.path.push_back(alpha_beta_gamma);
            T.probability.push_back(pr);
            T.total_probability += pr;

            if ((T.total_probability <= Bn_bar) && (T.total_probability > 0)) {
                Bn_bar = T.total_probability;
                best_trail_global = T;

                // 결과 출력
                cout << "Best Trail for " << n << " rounds:\n";
                cout << best_trail_global << endl;

            }

            T.path.pop_back();
            T.probability.pop_back();
            T.total_probability -= pr;
        } else {
            for (int jg = 0; jg <= 1; ++jg) {
                uint32_t mask = 1U << i;
                node next = alpha_beta_gamma;
                if (jg) next[2] |= mask; else next[2] &= ~mask;

                uint32_t pr_tilde = xdp(next[0] & ((1U << (i+1))-1),
                                        next[1] & ((1U << (i+1))-1),
                                        next[2] & ((1U << (i+1))-1),
                                        i+1);

                if (T.total_probability + pr_tilde <= Bn_bar) {
                    BestDiffSearch(r, i + 1, next);
                }
            }
        }
    }
}

int main() {
    // 파라미터 설정
    n = 4;       // 라운드 수
    w = 32;      // 워드 사이즈

    // 라운드마다 rotation에 의해 구조가 달라져서 사용 X : 모든 범위 확인
    B = {0, 0, 1, 2, 6, 10, 16};  // B[1] ~ B[n-1] 사용 (최초엔 모두 1로 초기화)

    // 초기 α, β, γ 설정
    node init_abg = {0, 0, 0};

    // 전역 변수 초기화
    Bn_bar = 6;
    best_trail_global = trail();

    // 시작 시각 기록
    auto start = std::chrono::high_resolution_clock::now();

    // 탐색 시작
    BestDiffSearch(1, 0, init_abg);

    // 종료 시각 기록
    auto end = std::chrono::high_resolution_clock::now();

    // 경과 시간 계산 (초 단위)
    std::chrono::duration<double> elapsed = end - start;

    std::cout << "실행 시간: " << elapsed.count() << " 초\n";

    // 결과 출력

    return 0;
}
