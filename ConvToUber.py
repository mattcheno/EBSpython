#! python3

# === BOILERPLATE =============================================================
#
#  Converter from Josh's file to Uber Key File
#  Matthew Chenoweth
#  2017/01/16

# --- Declarations ------------------------------------------------------------
import pandas as pd
joshXl = pd.ExcelFile("MakeModelKey_Year_v3.xlsx")     # Josh's YearFile
joshXl.sheet_names[u'Sheet 1', u'Input']          #Make sure this is correct!
uberFile = 'UberKey.csv'                   #Target UberKey File

# --- Logic -------------------------------------------------------------------

#import josh's file
pdfJosh = joshXl.parse("Input")

print(pdfJosh)

# === FOOTNOTES ===============================================================
# === END OF CODE =============================================================
