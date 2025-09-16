#!/usr/bin/env python3
"""Check that alpha_roft = 0 reproduces LCDM."""
import numpy as np
import subprocess
import tempfile
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
CLASS = os.path.join(ROOT, "class")
DEFAULT = os.path.join(ROOT, "default.ini")

def run(extra, root):
    cfg = open(DEFAULT).read().replace("write_background = no", "write_background = yes")
    cfg += f"root = {root}\n"
    cfg += extra
    with tempfile.NamedTemporaryFile('w', suffix='.ini', delete=False) as f:
        f.write(cfg)
        name = f.name
    subprocess.run([CLASS, name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.remove(name)
    return f"{root}00_background.dat", f"{root}00_cl.dat"

def relmax(a, b):
    return np.max(np.abs(a - b) / np.where(a != 0, a, 1))

def main():
    lcdm_bg, lcdm_cl = run("", os.path.join(ROOT, "output/reg_lcdm_"))
    roft_bg, roft_cl = run("fluid_equation_of_state = ROFT\nalpha_roft = 0.\nroft_model = add\n", os.path.join(ROOT, "output/reg_roft0_"))
    bg1 = np.loadtxt(lcdm_bg)
    bg2 = np.loadtxt(roft_bg)
    cl1 = np.loadtxt(lcdm_cl)
    cl2 = np.loadtxt(roft_cl)
    if relmax(bg1[:,3], bg2[:,3]) > 1e-4:
        raise SystemExit("H(z) mismatch")
    if relmax(bg1[:,5], bg2[:,5]) > 1e-4:
        raise SystemExit("distance mismatch")
    if relmax(cl1[:,1], cl2[:,1]) > 1e-4:
        raise SystemExit("C_l mismatch")
    print("ROFT regression passed")

if __name__ == "__main__":
    main()
