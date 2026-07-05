# Flam AI R&D Assignment

This repository contains my submission for the Flam Research and Development / AI assignment. The task was to find the unknown parameters `theta`, `M`, and `X` in the given parametric curve using the point data from `xy_data.csv`.

The final answer is supported by both a mathematical explanation and a reproducible Python script.

## Final Result

The estimated parameters are:

```text
theta = 30 degrees
theta = 0.523598775598 radians
M = 0.03
X = 55
```

My Desmos implementation is available here:

https://www.desmos.com/notebook/8aau0yt7tv/view

## Desmos Equation

The curve used for the final Desmos plot is:

```latex
\left( t\cos(0.523598775598)-e^{0.03\left|t\right|}\sin(0.3t)\sin(0.523598775598)+55,\ 42+t\sin(0.523598775598)+e^{0.03\left|t\right|}\sin(0.3t)\cos(0.523598775598) \right)
```

with the parameter range:

```text
6 < t < 60
```

## Files Included

```text
AI_R&D Assignment.pdf  Original assignment file
xy_data.csv            Data points provided for the curve
solve.py               Code used to estimate the unknown parameters
README.md              Final result, method, and references
```

## Method Used

The assignment gives the curve:

```text
x = t cos(theta) - exp(M |t|) sin(0.3t) sin(theta) + X
y = 42 + t sin(theta) + exp(M |t|) sin(0.3t) cos(theta)
```

I treated this as a rotated and translated parametric curve. The term involving `t` gives the main direction of the curve, while the term `exp(M |t|) sin(0.3t)` gives the oscillation around that direction.

To simplify the fitting, I reversed the translation and rotation. For a candidate value of `theta` and `X`, I transformed each point as:

```text
u = (x - X) cos(theta) + (y - 42) sin(theta)
v = -(x - X) sin(theta) + (y - 42) cos(theta)
```

For the correct parameters, the transformed coordinates should satisfy:

```text
u = t
v = exp(M |t|) sin(0.3t)
```

This reduced the problem from fitting the full two-dimensional curve directly to checking how well the transformed points match the expected one-dimensional wave.

## Estimation Steps

1. Read all `(x, y)` values from `xy_data.csv`.
2. Search through the allowed range of `theta`.
3. Estimate `X` from the projection of the points along the main curve direction.
4. Rotate the points back into `(u, v)` coordinates.
5. Estimate `M` using the logarithmic form:

```text
log(v / sin(0.3u)) = M |u|
```

6. Refine `theta` and `X` locally by minimizing the mean L1 residual.
7. Round the fitted values to the clean final constants.

The script gives:

```text
theta_rad = 0.523598295938
theta_deg = 29.999972517490
M = 0.029999990748
X = 54.999997739089
mean_L1_residual = 2.622198581421e-06
```

These values round to:

```text
theta = 30 degrees
M = 0.03
X = 55
```

## How To Run

```bash
python solve.py
```

The code uses only Python's standard library.

## Originality And Citation Note

The implementation in `solve.py` was written specifically for this assignment. I used standard ideas from coordinate geometry, rotation matrices, logarithmic transformation, and basic numerical search. The references below are included for the mathematical ideas used in the approach, not for copied code.

## References

- Flam. (2026). `Assignment for Research and Development / AI` [Assignment PDF].
- Strang, G. (2016). `Introduction to Linear Algebra` (5th ed.). Wellesley-Cambridge Press. Used for the rotation matrix and coordinate transformation idea.
- Nocedal, J., & Wright, S. J. (2006). `Numerical Optimization` (2nd ed.). Springer. Used as a reference for numerical parameter search and residual minimization.
- Weisstein, E. W. (n.d.). `Rotation Matrix`. MathWorld--A Wolfram Web Resource. https://mathworld.wolfram.com/RotationMatrix.html
- Desmos. (2026). `Submitted curve implementation`. https://www.desmos.com/notebook/8aau0yt7tv/view
