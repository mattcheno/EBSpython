#! python3

# === BOILERPLATE =============================================================
#
#  Pandas Test
#  Matthew Chenoweth
#  20YY/MM/DD

# --- Declarations ------------------------------------------------------------
import pandas as pd
#inCSV = pd.read_csv('ebsCSVData.csv', nrows = 20)
inCSV = pd.read_csv('ebsCSVData.csv', iterator = True, chunksize = 1000)
df = pd.concat(inCSV, ignore_index=True)

# --- Logic -------------------------------------------------------------------
print(df.info())

# === FOOTNOTES ===============================================================
# === END OF CODE =============================================================
