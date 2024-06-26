import pandas as pd

def seperator(file_name):
    df = pd.read_csv(file_name +'.csv')
    df2 = pd.DataFrame()
    df2['Output'] = df[df.columns[9]]
    df.drop(df.columns[9], axis=1, inplace=True)
    df.to_csv(file_name + "_sliced.csv", index=False)
    df2.to_csv("data/Output_" + file_name + ".csv", index=False)

# seperator("Training_data")

# seperator("cross_validation")

seperator("test_set")

#something might be wrong deleted starting row will check