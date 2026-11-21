"""N이 커질 때 MAC 시간이 N²에 비례하는지 확인하는 보조 측정 스크립트.

실행: E1-3 폴더에서  python3 samples/perf_sweep.py
main.py의 패턴 생성기(make_x, make_cross)와 측정 함수(average_ms)를 그대로 쓴다.
"""
import os
import sys

sys.dont_write_bytecode = True  # 폴더에 __pycache__를 만들지 않는다
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import main  # noqa: E402

print("N      N²      2D 평균(ms)  1D 평균(ms)")
for n in (25, 50, 100, 200, 400):
    p, f = main.make_x(n), main.make_cross(n)
    a = main.average_ms(main.mac, p, f)
    b = main.average_ms(main.mac_flat, p.flatten(), f.flatten())
    print("{:<6} {:<7} {:>11.4f} {:>12.4f}".format(n, n * n, a, b))
