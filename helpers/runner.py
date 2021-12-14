import pandas as pd

def run_simulation(df, system):
    results = []
    for i, data in df.iterrows():
        result = system.run(data, i)
        results.append(result)

    df = pd.DataFrame(results)
    df.reset_index(level=0, inplace=True)

    return df