
import pandas as pd


path_spot = f'../data/price_energy_elec.csv'
path_cluster = f'../data/Time_series_18_clusters.csv'

prices = pd.read_csv(path_spot)


prices = prices[["MTU (CET/CEST)", "Day-ahead Price (EUR/MWh)"]]


prices["Time"] = (
    prices["MTU (CET/CEST)"]
    .str.split(" - ", expand=True)[0]
    .str.strip()
)


prices["Time"] = (
    prices["Time"]
    .str.replace(" (CET)", "", regex=False)
    .str.replace(" (CEST)", "", regex=False)
)


prices["Time"] = pd.to_datetime(
    prices["Time"],
    format="%d/%m/%Y %H:%M:%S",
    errors="raise"
)

prices = prices.drop(columns = "MTU (CET/CEST)")
prices = prices.rename(columns = {"Day-ahead Price (EUR/MWh)" : "Spot_Price"})

cluster = pd.read_csv(
    path_cluster,
    sep=";",
    decimal=",",
    engine="python"
)

cluster["Time"] = pd.to_datetime(cluster["Time"], format="%Y-%m-%d %H:%M:%S")


data = pd.merge(
    prices,
    cluster,
    on="Time",
    how="inner"
)

cols = ["Time", "Spot_Price"] + [str(i) for i in range(1, 19)]
data = data[cols]
print(data.columns)

