from sklearn.ensemble import RandomForestRegressor


def build_model(random_state: int = 42) -> RandomForestRegressor:
    return RandomForestRegressor(n_estimators=100, max_depth=8, random_state=random_state)
