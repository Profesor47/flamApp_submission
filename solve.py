import csv
import math


T_MIN = 6.0
T_MAX = 60.0


def load_points(path):
    """Read the assignment CSV and return the measured (x, y) points."""
    with open(path, newline="") as handle:
        reader = csv.DictReader(handle)
        return [(float(row["x"]), float(row["y"])) for row in reader]


def mean(values):
    values = list(values)
    return sum(values) / len(values)


def estimate_x(points, theta):
    """Estimate the horizontal translation for a candidate theta."""
    c = math.cos(theta)
    s = math.sin(theta)
    projected = sorted(c * x + s * (y - 42.0) for x, y in points)
    n = len(projected)
    t_values = [T_MIN + (T_MAX - T_MIN) * i / (n - 1) for i in range(n)]
    return mean(p - t for p, t in zip(projected, t_values)) / c


def transformed_coordinates(points, theta, x_shift):
    """Undo the translation and rotation so the curve becomes (t, wave)."""
    c = math.cos(theta)
    s = math.sin(theta)
    transformed = []
    for x, y in points:
        dx = x - x_shift
        dy = y - 42.0
        t = c * dx + s * dy
        wave = -s * dx + c * dy
        transformed.append((t, wave))
    return transformed


def residual_for_m(transformed, m):
    """Mean L1 distance between observed wave values and model prediction."""
    total = 0.0
    for t, observed in transformed:
        predicted = math.exp(m * abs(t)) * math.sin(0.3 * t)
        total += abs(observed - predicted)
    return total / len(transformed)


def best_m(transformed):
    """Estimate M from log(v / sin(0.3t)) = M |t|."""
    numerator = 0.0
    denominator = 0.0
    for t, observed in transformed:
        base = math.sin(0.3 * t)
        if abs(base) < 1e-4:
            continue
        ratio = observed / base
        if ratio <= 0.0:
            continue
        weight = abs(t)
        numerator += weight * math.log(ratio)
        denominator += weight * weight

    m0 = numerator / denominator
    m0 = max(-0.05, min(0.05, m0))

    return m0, residual_for_m(transformed, m0)


def score_theta(points, theta):
    x_shift = estimate_x(points, theta)
    transformed = transformed_coordinates(points, theta, x_shift)
    m, score = best_m(transformed)
    return score, theta, m, x_shift


def score_params(points, theta, x_shift):
    transformed = transformed_coordinates(points, theta, x_shift)
    m, score = best_m(transformed)
    return score, theta, m, x_shift


def solve(points):
    best = None
    for i in range(1001):
        theta = math.radians(50.0 * i / 1000)
        candidate = score_theta(points, theta)
        if best is None or candidate[0] < best[0]:
            best = candidate

    
    _, theta, _, x_shift = best
    best = score_params(points, theta, x_shift)
    theta_step = math.radians(0.01)
    x_step = 0.01
    while theta_step > math.radians(1e-9) or x_step > 1e-8:
        improved = False
        candidates = []
        for dt in (-theta_step, 0.0, theta_step):
            for dx in (-x_step, 0.0, x_step):
                if dt == 0.0 and dx == 0.0:
                    continue
                theta_candidate = best[1] + dt
                x_candidate = best[3] + dx
                if 0.0 < theta_candidate < math.radians(50.0) and 0.0 < x_candidate < 100.0:
                    candidates.append(score_params(points, theta_candidate, x_candidate))

        candidate = min(candidates, key=lambda item: item[0])
        if candidate[0] < best[0]:
            best = candidate
            improved = True

        if not improved:
            theta_step *= 0.5
            x_step *= 0.5

    return best


def main():
    points = load_points("xy_data.csv")
    score, theta, m, x_shift = solve(points)
    print(f"theta_rad = {theta:.12f}")
    print(f"theta_deg = {math.degrees(theta):.12f}")
    print(f"M = {m:.12f}")
    print(f"X = {x_shift:.12f}")
    print(f"mean_L1_residual = {score:.12e}")
    print()
    print("Rounded submission values:")
    print(f"theta_rad = {math.radians(round(math.degrees(theta))):.12f}")
    print(f"theta_deg = {round(math.degrees(theta))}")
    print(f"M = {m:.2f}")
    print(f"X = {round(x_shift)}")


if __name__ == "__main__":
    main()
