from sklearn.ensemble import RandomForestClassifier


def build_model(random_state: int = 42) -> RandomForestClassifier:
    return RandomForestClassifier(n_estimators=100, max_depth=8, random_state=random_state, class_weight="balanced")
