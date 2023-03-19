
from nasdaqdatalink import nasdaq
nasdaq.read_key(filename = "/data/.HP2mLCTfC38KJsseJSos")
sp_data = nasdaq.get("FRED/NROUST").reset_index()
print(sp_data.head())
zillow = nasdaq.get_table("ZILLOW/INDICATORS", paginate = True)
print(zillow.head())