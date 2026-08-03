import numpy as np
import pandas as pd
import math
if __name__ == "__main__":
    #sheeyt information
    spreadsheetPath = 'STAR Data snalysisPunishment4NPP.xlsx'
    targetSheets = ['vision0.05', 'vision0.1', 'spatial0.05', 'spatial0.1']
    #dictionary to hold the b values for each sheet
    calculatedResults = {}

    #process the data in each sheet
    for sheet in targetSheets:
        print(f"calculating b values for sheet {sheet}")
        #read the data from the sheet
        df = pd.read_excel(spreadsheetPath, sheet_name = sheet)
        #our x values are +1 to the automatic 0 indexing of the program
        x = df.index + 1
        sheetAucVals = {}
        N_CONST = 100
        #loop through all 40 columns of the sheet
        for col in df.columns:
            y = df[col]
            #calculating the slope and yint for the linarized equation 
            #note: the clip is to avoid log(0) errors if y reaches 1.0, we just replace it
            safeLogY = np.log(np.clip(1 - y, 1e-9, None))
            mNumerator = N_CONST * np.sum(x * safeLogY) - np.sum(x) * np.sum(safeLogY)
            mDenominator = N_CONST * np.sum(x ** 2) - (np.sum(x) ** 2)
            m = mNumerator / mDenominator
            bNumerator = np.sum(safeLogY) - m * np.sum(x)
            bDenominator = N_CONST
            b = bNumerator / bDenominator
            #calculating exponential equation properties based on the linearized equation
            aVal = math.exp(b)
            kVal = -m
            auc = N_CONST + (aVal / kVal) * (math.exp(-kVal * N_CONST) - 1)
            sheetAucVals[col] = auc
        #convert the results into a horizontal row dataframe
        #a dataframe is associated with each original sheet
        calculatedResults[sheet] = pd.DataFrame([sheetAucVals])

    print("writing to excel sheet")
    with pd.ExcelWriter(spreadsheetPath, mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:
        for sheet, auc_df in calculatedResults.items():
            sheetToStoreIn = f"{sheet}auc"
            auc_df.to_excel(writer, sheet_name = sheetToStoreIn, index = False)
            print(f"updated {sheetToStoreIn}")