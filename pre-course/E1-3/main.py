"""Mini NPU Simulator.

MAC(Multiply-Accumulate) 연산으로 입력 패턴이 어떤 필터(Cross / X)와
더 비슷한지 판정하는 콘솔 프로그램이다.

- Python 3.8 이상, 표준 라이브러리(json, re, sys, time, os)만 사용한다.
- 실행: python main.py            (같은 폴더의 data.json 사용)
        python main.py 경로.json  (다른 JSON 파일로 모드 2 실행)
"""

import json
import os
import re
import sys
import time
import unicodedata

# ---------------------------------------------------------------------------
# 상수 / 정책
# ---------------------------------------------------------------------------
EPSILON = 1e-9           # 점수 비교 허용오차: |a - b| < EPSILON 이면 동점
REPEAT = 10              # 성능 측정 반복 횟수 (요구사항 최소 10회)
PERF_SIZES = (3, 5, 13, 25)

LABEL_CROSS = "Cross"    # 프로그램 내부 표준 라벨
LABEL_X = "X"
UNDECIDED = "UNDECIDED"

# 외부 표기(expected 값, filter 키) -> 표준 라벨. 소문자로 비교한다.
LABEL_ALIASES = {
    "+": LABEL_CROSS,
    "cross": LABEL_CROSS,
    "x": LABEL_X,
}

PATTERN_KEY_RE = re.compile(r"^size_(\d+)_(\d+)$")
FILTER_KEY_RE = re.compile(r"^size_(\d+)$")

# 실패 원인 분류 (README의 원인 분석과 같은 이름을 쓴다)
CAUSE_SCHEMA = "데이터/스키마"
CAUSE_NUMERIC = "수치 비교"
CAUSE_LOGIC = "로직/판정 불일치"

LINE = "#" + "-" * 39


# ---------------------------------------------------------------------------
# 1. 데이터 구조: N x N 격자
# ---------------------------------------------------------------------------
class Grid:
    """N x N 2차원 숫자 배열. 위치(행, 열)로 값을 저장하고 읽는다."""

    def __init__(self, size, fill=0.0):
        if size < 1:
            raise ValueError("크기는 1 이상이어야 합니다.")
        self.size = size
        self.cells = [[float(fill)] * size for _ in range(size)]

    @classmethod
    def from_rows(cls, rows, name="배열"):
        """2차원 리스트를 검증해 Grid로 만든다. 문제가 있으면 ValueError."""
        if not isinstance(rows, list) or not rows:
            raise ValueError("{}: 2차원 배열(리스트의 리스트)이 아닙니다.".format(name))
        size = len(rows)
        grid = cls(size)
        for r, row in enumerate(rows):
            if not isinstance(row, list):
                raise ValueError("{}: {}행이 리스트가 아닙니다.".format(name, r + 1))
            if len(row) != size:
                raise ValueError(
                    "{}: 정사각형이 아닙니다 ({}행, {}행의 열 수 {}).".format(
                        name, size, r + 1, len(row)))
            for c, value in enumerate(row):
                # bool은 int의 하위 타입이라 따로 막는다.
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ValueError("{}: ({}, {}) 값 {!r}이 숫자가 아닙니다.".format(
                        name, r + 1, c + 1, value))
                grid.set(r, c, value)
        return grid

    def get(self, row, col):
        return self.cells[row][col]

    def set(self, row, col, value):
        self.cells[row][col] = float(value)

    def flatten(self):
        """보너스: 행 우선(row-major) 순서의 길이 N*N 1차원 리스트."""
        flat = []
        for row in self.cells:
            flat.extend(row)
        return flat

    def lines(self):
        return [" ".join(_fmt_cell(v) for v in row) for row in self.cells]


def _fmt_cell(value):
    return str(int(value)) if value == int(value) else repr(value)


# ---------------------------------------------------------------------------
# 2. 라벨 정규화
# ---------------------------------------------------------------------------
def normalize_label(raw):
    """'+', 'x', 'cross', 'X' 등 외부 표기를 표준 라벨(Cross / X)로 바꾼다.

    알 수 없는 라벨이면 ValueError를 던져, 호출한 쪽이 케이스 단위로
    '데이터/스키마' 실패로 처리하게 한다.
    """
    if not isinstance(raw, str):
        raise ValueError("라벨 {!r}이 문자열이 아닙니다.".format(raw))
    key = raw.strip().lower()
    if key not in LABEL_ALIASES:
        raise ValueError("알 수 없는 라벨 {!r} (허용: +, x, cross)".format(raw))
    return LABEL_ALIASES[key]


# ---------------------------------------------------------------------------
# 3. MAC 연산 (반복문 직접 구현)
# ---------------------------------------------------------------------------
def mac(pattern, filt):
    """같은 위치의 값끼리 곱하고(Multiply) 모두 더해(Accumulate) 점수를 반환."""
    if pattern.size != filt.size:
        raise ValueError("크기 불일치: 패턴 {0}x{0}, 필터 {1}x{1}".format(
            pattern.size, filt.size))
    n = pattern.size
    a = pattern.cells
    b = filt.cells
    total = 0.0
    for r in range(n):
        for c in range(n):
            total += a[r][c] * b[r][c]
    return total


def mac_flat(pattern_flat, filter_flat):
    """보너스: 1차원(길이 N*N) 배열 버전. 인덱스 계산이 한 단계로 줄어든다."""
    if len(pattern_flat) != len(filter_flat):
        raise ValueError("크기 불일치: 길이 {} vs {}".format(
            len(pattern_flat), len(filter_flat)))
    total = 0.0
    for i in range(len(pattern_flat)):
        total += pattern_flat[i] * filter_flat[i]
    return total


# ---------------------------------------------------------------------------
# 4. 점수 비교 정책 (epsilon)
# ---------------------------------------------------------------------------
def compare_scores(score_a, score_b, epsilon=EPSILON):
    """'A', 'B' 또는 None(허용오차 내 동점)을 반환한다."""
    if abs(score_a - score_b) < epsilon:
        return None
    return "A" if score_a > score_b else "B"


def judge_labels(score_cross, score_x):
    """모드 2용: Cross / X / UNDECIDED."""
    winner = compare_scores(score_cross, score_x)
    if winner is None:
        return UNDECIDED
    return LABEL_CROSS if winner == "A" else LABEL_X


# ---------------------------------------------------------------------------
# 5. 성능 측정 (연산 구간만)
# ---------------------------------------------------------------------------
def average_ms(func, *args, repeat=REPEAT):
    """func(*args)를 repeat번 호출하고 평균 시간(ms)을 반환한다.

    측정 경계: perf_counter()를 함수 호출 바로 앞뒤에서만 읽는다.
    입력, 파일 읽기, 출력은 이 구간 밖에서 끝낸 뒤 호출한다.
    """
    func(*args)  # 워밍업 1회(측정 제외): 첫 호출의 캐시/할당 비용을 뺀다.
    total = 0.0
    for _ in range(repeat):
        start = time.perf_counter()
        func(*args)
        total += time.perf_counter() - start
    return total / repeat * 1000.0


# ---------------------------------------------------------------------------
# 6. 보너스: 패턴 생성기
# ---------------------------------------------------------------------------
def make_cross(n):
    """가운데 행과 가운데 열이 1인 N x N 십자가 (N은 홀수 권장)."""
    g = Grid(n)
    mid = n // 2
    for i in range(n):
        g.set(mid, i, 1)
        g.set(i, mid, 1)
    return g


def make_x(n):
    """두 대각선이 1인 N x N X 패턴."""
    g = Grid(n)
    for i in range(n):
        g.set(i, i, 1)
        g.set(i, n - 1 - i, 1)
    return g


# ---------------------------------------------------------------------------
# 출력 도우미
# ---------------------------------------------------------------------------
def section(title):
    print()
    print(LINE)
    print("# " + title)
    print(LINE)


def display_width(text):
    """한글처럼 화면에서 두 칸을 차지하는 글자를 2로 센다(표 정렬용)."""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
               for ch in text)


def pad(text, width, right=False):
    space = " " * max(0, width - display_width(text))
    return space + text if right else text + space


def print_perf_table(rows, title="성능 분석 (평균/{}회)".format(REPEAT)):
    """rows: (n, 2D 평균 ms, 1D 평균 ms 또는 None)."""
    section(title)
    show_flat = any(r[2] is not None for r in rows)
    cols = [("크기", 8, False), ("평균 시간(ms)", 16, True), ("연산 횟수(N²)", 16, True)]
    if show_flat:
        cols.append(("1D 평균(ms)", 14, True))
    print("".join(pad(name, w, right) for name, w, right in cols))
    print("-" * sum(w for _, w, _ in cols))
    for n, ms_2d, ms_1d in rows:
        cells = ["{0}x{0}".format(n), "{:.4f}".format(ms_2d), str(n * n)]
        if show_flat:
            cells.append("{:.4f}".format(ms_1d))
        print("".join(pad(cell, w, right) for cell, (_, w, right) in zip(cells, cols)))
    print("※ 연산 횟수 = N² (위치별 곱셈 N²번, 누적 덧셈 N²번)")


# ---------------------------------------------------------------------------
# 모드 1: 사용자 입력 (3x3)
# ---------------------------------------------------------------------------
def read_line(prompt=""):
    """EOF(Ctrl+D)면 프로그램을 정상 종료한다."""
    try:
        return input(prompt)
    except EOFError:
        print("\n입력이 끝나 프로그램을 종료합니다.")
        sys.exit(0)


def parse_row(text, n):
    """공백 구분 숫자 n개를 float 리스트로. 형식 오류면 ValueError."""
    parts = text.split()
    if len(parts) != n:
        raise ValueError("열 개수 불일치: {}개 입력됨".format(len(parts)))
    values = []
    for p in parts:
        try:
            values.append(float(p))
        except ValueError:
            raise ValueError("숫자 파싱 실패: {!r}".format(p))
    return values


def input_grid(title, n=3):
    """n줄을 입력받는다. 줄 단위 오류 시 안내 후 그 줄부터 다시 입력."""
    print("{} ({}줄 입력, 공백 구분)".format(title, n))
    rows = []
    while len(rows) < n:
        text = read_line()
        try:
            rows.append(parse_row(text, n))
        except ValueError as e:
            print("입력 형식 오류: 각 줄에 {}개의 숫자를 공백으로 구분해 입력하세요. ({})"
                  .format(n, e))
            print("  → {}번째 줄을 다시 입력하세요.".format(len(rows) + 1))
    return Grid.from_rows(rows, title)


def run_mode1():
    n = 3
    section("[1] 필터 입력")
    filter_a = input_grid("필터 A", n)
    print()
    filter_b = input_grid("필터 B", n)

    print()
    print("저장 확인 (필터 A / 필터 B)")
    for la, lb in zip(filter_a.lines(), filter_b.lines()):
        print("  {:<14}|  {}".format(la, lb))

    section("[2] 패턴 입력")
    pattern = input_grid("패턴", n)

    # 연산 (I/O 끝난 뒤)
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    ms_a = average_ms(mac, pattern, filter_a)
    ms_b = average_ms(mac, pattern, filter_b)
    winner = compare_scores(score_a, score_b)

    section("[3] MAC 결과")
    print("A 점수: {!r}".format(score_a))
    print("B 점수: {!r}".format(score_b))
    print("연산 시간(평균/{}회): A {:.4f} ms, B {:.4f} ms".format(REPEAT, ms_a, ms_b))
    if winner is None:
        print("판정: 판정 불가 (|A-B| < {:g})".format(EPSILON))
    else:
        print("판정: {}".format(winner))

    # 3x3 성능 분석: 사용자가 입력한 패턴/필터 그대로 측정
    ms_2d = average_ms(mac, pattern, filter_a)
    flat_p, flat_f = pattern.flatten(), filter_a.flatten()
    ms_1d = average_ms(mac_flat, flat_p, flat_f)
    print_perf_table([(n, ms_2d, ms_1d)], "[4] 성능 분석 (3x3, 평균/{}회)".format(REPEAT))


# ---------------------------------------------------------------------------
# 모드 2: data.json 분석
# ---------------------------------------------------------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_filters(data):
    """filters 섹션을 {N: {'Cross': Grid, 'X': Grid}}로 만든다.

    잘못된 항목은 건너뛰고 경고만 남긴다(해당 크기의 패턴은 나중에 FAIL).
    """
    filters = {}
    raw = data.get("filters") if isinstance(data, dict) else None
    if not isinstance(raw, dict):
        print("✗ 'filters' 섹션이 없거나 객체가 아닙니다.")
        return filters

    for key in sorted(raw, key=_size_sort_key):
        m = FILTER_KEY_RE.match(str(key))
        if not m:
            print("✗ {}: 필터 키 형식이 size_N이 아닙니다. 건너뜀".format(key))
            continue
        n = int(m.group(1))
        entry = raw[key]
        if not isinstance(entry, dict):
            print("✗ {}: 필터 묶음이 객체가 아닙니다. 건너뜀".format(key))
            continue
        loaded = {}
        for label_key, rows in entry.items():
            try:
                label = normalize_label(label_key)
                grid = Grid.from_rows(rows, "{}.{}".format(key, label_key))
                if grid.size != n:
                    raise ValueError("{}.{}: 키는 {}인데 실제 크기는 {}x{}".format(
                        key, label_key, n, grid.size, grid.size))
                loaded[label] = grid
            except ValueError as e:
                print("✗ {}".format(e))
        if loaded:
            filters[n] = loaded
            missing = [l for l in (LABEL_CROSS, LABEL_X) if l not in loaded]
            note = "" if not missing else " (누락: {})".format(", ".join(missing))
            print("✓ {:<8}필터 로드 완료 ({}){}".format(
                key, ", ".join(sorted(loaded)), note))
    return filters


def _size_sort_key(key):
    nums = [int(x) for x in re.findall(r"\d+", str(key))]
    return (nums, str(key))


def analyze_case(key, item, filters):
    """패턴 1개를 분석해 결과 dict를 반환한다. 예외를 밖으로 던지지 않는다."""
    result = {"key": key, "cross": None, "x": None, "decision": None,
              "expected": None, "passed": False, "cause": None, "reason": None}
    try:
        m = PATTERN_KEY_RE.match(str(key))
        if not m:
            raise ValueError("패턴 키 형식이 size_N_idx가 아닙니다.")
        n = int(m.group(1))
        if not isinstance(item, dict):
            raise ValueError("패턴 항목이 객체가 아닙니다.")
        if "expected" not in item:
            raise ValueError("expected 값이 없습니다.")
        result["expected"] = normalize_label(item["expected"])
        if "input" not in item:
            raise ValueError("input 값이 없습니다.")
        pattern = Grid.from_rows(item["input"], "{}.input".format(key))
        if n not in filters:
            raise ValueError("size_{} 필터가 없습니다.".format(n))
        pair = filters[n]
        for label in (LABEL_CROSS, LABEL_X):
            if label not in pair:
                raise ValueError("size_{} 필터에 {} 라벨이 없습니다.".format(n, label))
        if pattern.size != n:
            raise ValueError("크기 불일치: 키는 {0}x{0}, input은 {1}x{1}".format(
                n, pattern.size))
    except ValueError as e:
        result["cause"] = CAUSE_SCHEMA
        result["reason"] = str(e)
        return result

    result["cross"] = mac(pattern, pair[LABEL_CROSS])
    result["x"] = mac(pattern, pair[LABEL_X])
    result["decision"] = judge_labels(result["cross"], result["x"])

    if result["decision"] == UNDECIDED:
        result["cause"] = CAUSE_NUMERIC
        result["reason"] = "동점(UNDECIDED): |Cross-X| = {:.3g} < {:g}".format(
            abs(result["cross"] - result["x"]), EPSILON)
    elif result["decision"] != result["expected"]:
        result["cause"] = CAUSE_LOGIC
        result["reason"] = "판정 {} ≠ expected {}".format(
            result["decision"], result["expected"])
    else:
        result["passed"] = True
    return result


def print_case(res):
    print("--- {} ---".format(res["key"]))
    if res["cross"] is None:
        exp = res["expected"] or "?"
        print("판정: - | expected: {} | FAIL ({})".format(exp, res["reason"]))
        return
    print("Cross 점수: {!r}".format(res["cross"]))
    print("X 점수: {!r}".format(res["x"]))
    status = "PASS" if res["passed"] else "FAIL"
    if res["decision"] == UNDECIDED:
        status += " (동점 규칙)"
    print("판정: {} | expected: {} | {}".format(
        res["decision"], res["expected"], status))


def measure_sizes(filters, data_patterns):
    """크기별 2D/1D 평균 시간. 3x3은 생성기 패턴, 나머지는 data.json 값 우선."""
    rows = []
    for n in PERF_SIZES:
        if n in filters and LABEL_CROSS in filters[n]:
            filt = filters[n][LABEL_CROSS]
        else:
            filt = make_cross(n)
        pattern = data_patterns.get(n) or make_x(n)
        ms_2d = average_ms(mac, pattern, filt)
        ms_1d = average_ms(mac_flat, pattern.flatten(), filt.flatten())
        rows.append((n, ms_2d, ms_1d))
    return rows


def run_mode2(path):
    section("[1] 필터 로드")
    try:
        data = load_json(path)
    except OSError as e:
        print("✗ 파일을 열 수 없습니다: {} ({})".format(path, e))
        return
    except json.JSONDecodeError as e:
        print("✗ JSON 형식 오류: {}".format(e))
        return
    filters = load_filters(data)

    section("[2] 패턴 분석 (라벨 정규화 적용)")
    raw_patterns = data.get("patterns") if isinstance(data, dict) else None
    if not isinstance(raw_patterns, dict):
        print("✗ 'patterns' 섹션이 없거나 객체가 아닙니다.")
        raw_patterns = {}

    results = []
    perf_patterns = {}
    for key in sorted(raw_patterns, key=_size_sort_key):
        res = analyze_case(key, raw_patterns[key], filters)
        print_case(res)
        results.append(res)
        # 성능 측정에 쓸 크기별 대표 패턴(검증 통과한 것)
        m = PATTERN_KEY_RE.match(str(key))
        if res["cross"] is not None and m:
            n = int(m.group(1))
            if n not in perf_patterns:
                perf_patterns[n] = Grid.from_rows(raw_patterns[key]["input"])

    rows = measure_sizes(filters, perf_patterns)
    print_perf_table(rows, "[3] 성능 분석 (평균/{}회, 1D는 보너스 최적화)".format(REPEAT))

    section("[4] 결과 요약")
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    print("총 테스트: {}개".format(total))
    print("통과: {}개".format(passed))
    print("실패: {}개".format(failed))
    if failed:
        print()
        print("실패 케이스:")
        for r in results:
            if not r["passed"]:
                print("- {}: [{}] {}".format(r["key"], r["cause"], r["reason"]))


# ---------------------------------------------------------------------------
# 모드 3 (보너스): 패턴 생성기
# ---------------------------------------------------------------------------
def run_mode3():
    section("[1] 패턴 생성기")
    while True:
        text = read_line("크기 N (3 이상의 홀수): ").strip()
        try:
            n = int(text)
            if n < 3 or n % 2 == 0:
                raise ValueError
            break
        except ValueError:
            print("입력 형식 오류: 3 이상의 홀수 정수를 입력하세요.")
    cross, x = make_cross(n), make_x(n)
    if n <= 13:
        print("\nCross {0}x{0}".format(n))
        print("\n".join(cross.lines()))
        print("\nX {0}x{0}".format(n))
        print("\n".join(x.lines()))

    section("[2] 생성 패턴 자기 판정")
    for name, pat in ((LABEL_CROSS, cross), (LABEL_X, x)):
        sc, sx = mac(pat, cross), mac(pat, x)
        print("{} 패턴 → Cross 점수 {:g}, X 점수 {:g}, 판정 {}".format(
            name, sc, sx, judge_labels(sc, sx)))

    rows = []
    for size in sorted(set(PERF_SIZES + (n,))):
        p, f = make_x(size), make_cross(size)
        rows.append((size, average_ms(mac, p, f),
                     average_ms(mac_flat, p.flatten(), f.flatten())))
    print_perf_table(rows, "[3] 생성 패턴 성능 분석 (평균/{}회)".format(REPEAT))


# ---------------------------------------------------------------------------
# 진입점
# ---------------------------------------------------------------------------
def default_data_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else default_data_path()
    print("=== Mini NPU Simulator ===")
    print()
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    print("3. 패턴 생성기 (보너스)")
    while True:
        choice = read_line("선택: ").strip()
        if choice in ("1", "2", "3"):
            break
        print("1, 2, 3 중 하나를 입력하세요.")
    if choice == "1":
        run_mode1()
    elif choice == "2":
        run_mode2(path)
    else:
        run_mode3()


if __name__ == "__main__":
    main()
