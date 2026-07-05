# Flam AI R&D Assignment

This repository solves the curve-fitting assignment from `AI_R&D Assignment.pdf`.

## Result

Unknown parameter values:

```text
theta = 0.523598775598 rad = 30 deg
M = 0.03
X = 55
```

Desmos / LaTeX submission equation:

```latex
\left( t\cos(0.523598775598)-e^{0.03\left|t\right|}\sin(0.3t)\sin(0.523598775598)+55,\ 42+t\sin(0.523598775598)+e^{0.03\left|t\right|}\sin(0.3t)\cos(0.523598775598) \right)
```

with:

```text
6 < t < 60
```

## Method

The given curve is:

```text
x = t cos(theta) - exp(M |t|) sin(0.3t) sin(theta) + X
y = 42 + t sin(theta) + exp(M |t|) sin(0.3t) cos(theta)
```

After subtracting the translation `(X, 42)` and rotating by `-theta`, the coordinates become:

```text
u = (x - X) cos(theta) + (y - 42) sin(theta) = t
v = -(x - X) sin(theta) + (y - 42) cos(theta) = exp(M |t|) sin(0.3t)
```

So for a candidate `theta`, the projected coordinate `u` should match uniformly sampled values of `t` from `6` to `60`, shifted by `X cos(theta)`. The solver:

1. Sweeps `theta` in the allowed range `0 deg < theta < 50 deg`.
2. Estimates `X` by matching sorted projected points to uniformly spaced `t` values.
3. Rotates points into `(u, v)`.
4. Fits `M` by minimizing the mean L1 residual between `v` and `exp(M |u|) sin(0.3u)`.
5. Refines the best `theta` and `M` by ternary search.

## Reproduce

Run:

```bash
python solve.py
```

Expected output:

```text
theta_rad = 0.523598295938
theta_deg = 29.999972517490
M = 0.029999990748
X = 54.999997739089
mean_L1_residual = 2.622198581421e-06

Rounded submission values:
theta_rad = 0.523598775598
theta_deg = 30
M = 0.03
X = 55
```
