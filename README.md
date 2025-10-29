# Security Analysis of Alzette in the Fixed-Key Model

This repository contains the source code used in the paper **"고정키 환경에서의 Alzette 안전성 분석 (Security Analysis of Alzette in the Fixed-Key Model)"**.
It provides implementations and analysis scripts for evaluating the fixed-key differential probabilities of the 64-bit ARX-based S-box **Alzette**, based on the quasidifferential framework proposed by Beyne and Rijmen.

---

## Abstract

In this study, we apply Beyne and Rijmen’s fixed-key probabilistic analysis framework to the 64-bit ARX-based S-box **Alzette** to verify the exact differential probabilities of given trails.
The original Alzette paper presents seven differential trails with the highest expected probabilities in a random-key setting, experimentally confirming only eight candidates among 2^32 possible round constants.

Through theoretical modeling, this work computes the fixed-key probabilities of the same seven trails and confirms the consistency between experimental and analytical results. It further shows that the differential probabilities depend on the round constants.
Based on this finding, we derive necessary conditions for selecting secure round constants and propose new candidates such as `c = 0x0205000` and `c = 0xffdfdf7f`.

This research validates the applicability of fixed-key analysis for nonlinear ARX components and provides a foundation for assessing the security of lightweight ciphers such as CRAX, TRAX, and SPARKLE.

---

## Code Reference

The base implementation references the quasidifferential framework developed by Tim Beyne:
🔗 [https://github.com/TimBeyne/quasidifferential-trails](https://github.com/TimBeyne/quasidifferential-trails)

---

## Directory Structure

```
quasidifferential-trails-for-alzette/
├─ alzette/
│  ├─ result/
│  │  ├─ 30/
│  │  ├─ 35/
│  │  ├─ 37/
│  │  ├─ 38/
│  │  └─ 39/
│  └─ __pycache__/
└─ trail_search/
```

### Directory Descriptions

**alzette/**

* `alzette.py`, `common.py`: Contain SMT models for finding quasidifferential trails of Alzette.
* `result/`: Stores the trails corresponding to each weight.

  * `analysis.py`: Counts the number of quasidifferential trails by weight.
  * `gaussian_elimination_mod2.py`: Simplifies equations derived from trails.

**trail_search/**

* `best_trail_search.cpp`: Searches for optimal characteristics of Alzette (based on modular addition input/output).
* `trail_convert.py`: Converts characteristics from modular addition I/O representation to round I/O representation.

---

## Requirements

* **Python 3.10.12**
* **numpy 1.21.5**
* **PyBoolector 3.2.4.20240823.1**
* **GCC** (for C++ modules)

### Environment

This project was tested under **Windows Subsystem for Linux (WSL 2)** with the following configuration:

* **Distribution:** Ubuntu 22.04.5 LTS (Jammy Jellyfish)
* **Kernel version:** 5.15.167.4-microsoft-standard-WSL2
* **GCC:** 11.4.0
* **Python:** 3.10.12
* **numpy:** 1.21.5
* **PyBoolector:** 3.2.4.20240823.1

---

## How to Run

1. **Characteristic Search**

   ```bash
   cd trail_search
   g++ best_trail_search.cpp -o best_trail_search
   ./best_trail_search
   ```

2. **Convert Trail Format (trail_convert.py)**

   ```bash
   python3 trail_convert.py
   ```

3. **Search Quasidifferential Trails (alzette.py)**

   ```bash
   cd ../alzette
   python3 alzette.py
   ```

4. **Analyze Results (analysis.py)**

   ```bash
   python3 result/analysis.py
   ```

5. **Simplify Derived Equations (gaussian_elimination_mod2.py)**

   ```bash
   python3 result/gaussian_elimination_mod2.py
   ```


---

## Citation

If you use this code, please cite the following work:

> **고정키 환경에서의 Alzette 안전성 분석 (Security Analysis of Alzette in the Fixed-Key Model)**
> [Author names and publication details to be updated.]

---

## License

This project is intended for **academic and research use only**.
If no explicit license is provided, it is distributed under a **non-commercial research-only policy**.
