from config import N_TARGET, P_TARGET, K_TARGET

def engineer_nutrient_features(n, p, k, temperature, humidity, ph):
    n_def = max(0, N_TARGET - n) / N_TARGET
    p_def = max(0, P_TARGET - p) / P_TARGET
    k_def = max(0, K_TARGET - k) / K_TARGET

    yellowing = max(0.0, min(100.0, n_def * 70))
    dry_edge = max(0.0, min(100.0, k_def * 65))
    green = max(0.0, min(100.0, 100 - (yellowing * 0.5 + dry_edge * 0.4) - (p_def * 15)))

    return [n, p, k, temperature, humidity, ph, yellowing, green, dry_edge]