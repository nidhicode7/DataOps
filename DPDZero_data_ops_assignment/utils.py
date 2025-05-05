import pandas as pd

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded: {file_path} (Rows: {len(df)})")
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None
