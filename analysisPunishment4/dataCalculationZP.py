import numpy as np
import pandas as pd
import math
if __name__ == "__main__":
    #sheeyt information
    spreadsheetPath = 'STAR Data snalysisPunishment4ZP.xlsx'
    targetSheets = ['vision0.05', 'vision0.1', 'spatial0.05', 'spatial0.1']
    #dictionary to hold the values for each sheet
    # Format: { 'sheet_name': {'auc': df, 'slopes': df} }
    calculatedResults = {}

    #process the data in each sheet
    for sheet in targetSheets:
        print(f"calculating values for sheet {sheet}")
        #read the data from the sheet
        df = pd.read_excel(spreadsheetPath, sheet_name = sheet)
        #our x values are +1 to the automatic 0 indexing of the program
        x = df.index + 1
        sheetSlopeVals = {}
        sheetAucVals = {}
        N_CONST = 100
        #loop through all 40 columns of the sheet
        for col in df.columns:
            y = df[col]
            #calculating the slope and yint for the linarized equation 
            mNumerator = N_CONST * np.sum(x * y) - np.sum(x) * np.sum(y)
            mDenominator = N_CONST * np.sum(x ** 2) - (np.sum(x) ** 2)
            m = mNumerator / mDenominator
            bNumerator = np.sum(y) - m * np.sum(x)
            bDenominator = N_CONST
            b = bNumerator / bDenominator
            auc = 5000 * m + 100 * b
            sheetSlopeVals[col] = m
            sheetAucVals[col] = auc
        #convert the results into a horizontal row dataframe
        #a dataframe is associated with each original sheet
        calculatedResults[sheet] = {
            'auc': pd.DataFrame([sheetAucVals]),
            'slopes': pd.DataFrame([sheetSlopeVals])
        }

    print("writing to excel sheet")
    with pd.ExcelWriter(spreadsheetPath, mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:
        for sheet, data_dict in calculatedResults.items():
            #save AUC data frame
            aucSheetName = f"{sheet}auc"
            data_dict['auc'].to_excel(writer, sheet_name=aucSheetName, index=False)
            print(f"updated {aucSheetName}")
            #save slopes data frame
            slopesSheetName = f"{sheet}slopes"
            data_dict['slopes'].to_excel(writer, sheet_name=slopesSheetName, index=False)
            print(f"updated {slopesSheetName}")