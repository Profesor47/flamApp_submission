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
assignment.pdf         Original assignment file
xy_data.csv            Data points provided for the curve
solve.py               Code used to estimate the unknown parameters
README.md              Final result, method, and references
```

Original assignment PDF: [assignment.pdf](assignment.pdf)

## Solving Steps

1. I started from the given parametric equations:

```text
x = t cos(theta) - e^(M|t|) sin(0.3t) sin(theta) + X
y = 42 + t sin(theta) + e^(M|t|) sin(0.3t) cos(theta)
```

2. I observed that the curve is a translated and rotated form of a simpler curve. The main movement is along `t`, and the oscillation is given by:

   ```text
   e^(M|t|) sin(0.3t)
   ```

3. To simplify the problem, I reversed the translation and rotation. For each point `(x, y)`, I transformed it into:

   ```text
   u = (x - X) cos(theta) + (y - 42) sin(theta)
   v = -(x - X) sin(theta) + (y - 42) cos(theta)
   ```

4. For the correct values of `theta`, `M`, and `X`, the transformed points should satisfy:

   ```text
   u = t
   v = e^(M|t|) sin(0.3t)
   ```

5. I searched over the allowed range of `theta`, estimated `X` from the projected points, and then fitted `M` using:

   ```text
   log(v / sin(0.3u)) = M |u|
   ```

6. Finally, I refined the values by minimizing the mean L1 distance between the transformed points and the expected curve.

The fitted values were:

```text
theta = 29.999972517490 degrees
M = 0.029999990748
X = 54.999997739089
```

So the final rounded answer is:

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

## References

- Desmos. (n.d.). `Graphing Calculator`. Used to understand and implement the parametric curve visualization. https://www.desmos.com/calculator
