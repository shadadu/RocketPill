import pandas as pd


def read_target_pressure_series(csv_path):
    # Expect columns: time_ms, pressure_Pa
    df = pd.read_csv(csv_path)
    if df.shape[1] < 2:
        raise ValueError("CSV must have at least two columns: time_ms, pressure_Pa")
    # standardize column names
    cols = df.columns.tolist()
    df = df.rename(columns={cols[0]: "time_ms", cols[1]: "pressure_Pa"})
    return df
