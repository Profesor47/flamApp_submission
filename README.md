# Flam AI R&D Assignment

This is my submission for the Research and Development / AI assignment. The task was to find the unknown values of `theta`, `M`, and `X` in the given parametric curve using the points from `xy_data.csv`.

## Final Answer

The values I got are:

```text
theta = 30 deg
theta = 0.523598775598 rad
M = 0.03
X = 55
```

The equation to paste in Desmos is:

```latex
\left( t\cos(0.523598775598)-e^{0.03\left|t\right|}\sin(0.3t)\sin(0.523598775598)+55,\ 42+t\sin(0.523598775598)+e^{0.03\left|t\right|}\sin(0.3t)\cos(0.523598775598) \right)
```

Use the range:

```text
6 < t < 60
```

## How I Approached It

The original equations were:

```text
x = t cos(theta) - exp(M |t|) sin(0.3t) sin(theta) + X
y = 42 + t sin(theta) + exp(M |t|) sin(0.3t) cos(theta)
```

At first, this looks like a general nonlinear fitting problem. The useful observation is that the curve is basically made from two parts:

- a straight movement along `t`
- a wave term `exp(M |t|) sin(0.3t)` that is rotated by `theta`

So I tried undoing the translation and rotation. If I subtract `(X, 42)` and rotate the points back by `theta`, the equations become much simpler:

```text
u = (x - X) cos(theta) + (y - 42) sin(theta)
v = -(x - X) sin(theta) + (y - 42) cos(theta)
```

For the correct values, these should behave like:

```text
u = t
v = exp(M |t|) sin(0.3t)
```

That means the problem can be reduced to checking which `theta` and `X` make the rotated points line up with the expected wave.

## Steps Followed

1. Loaded all points from `xy_data.csv`.
2. Swept `theta` in the allowed range `0 deg < theta < 50 deg`.
3. For each `theta`, estimated `X` by projecting the points along the main curve direction.
4. Rotated the points back into `(u, v)` coordinates.
5. Estimated `M` from the relation:

```text
log(v / sin(0.3u)) = M |u|
```

6. Refined `theta` and `X` locally to reduce the mean L1 residual.
7. Rounded the fitted values to the clean final values.

The fitted output from the script is:

```text
theta_rad = 0.523598295938
theta_deg = 29.999972517490
M = 0.029999990748
X = 54.999997739089
mean_L1_residual = 2.622198581421e-06
```

These values round naturally to:

```text
theta = 30 deg
M = 0.03
X = 55
```

## How To Run

```bash
python solve.py
```

The script uses only Python's standard library, so no extra packages are needed.

## References

- Flam. (2026). `Assignment for Research and Development / AI` [Assignment PDF].
- Desmos. (n.d.). Graphing calculator. https://www.desmos.com/calculator/rfj91yrxob
