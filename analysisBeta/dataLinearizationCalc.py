import numpy as np
import pandas as pd
if __name__ == "__main__":
    a = 200
    spreadsheetPath = 'STAR Data Beta.xlsx'
    targetSheets = ['0.25Data', '0.5Data', '0.75Data']
    #dictionary to hold the b values for each sheet
    calculatedResults = {}

    #process the data in each sheet
    for sheet in targetSheets:
        print(f"calculating b values for sheet {sheet}")
        #read the data from the sheet
        df = pd.read_excel(spreadsheetPath, sheet_name = sheet)
        #our t values are +1 to the automatic 0 indexing of the program
        t = df.index + 1
        sheetBVals = {}
        #loop through all 40 columns of the sheet
        for col in df.columns:
            y = df[col]
            #mask to avoid math errors with ln(<=0)
            #filtering our all the rows in the col where y<=0 or y/a is invalid
            #but for us all ys are positive
            #valid_mask = (y > 0) & ((y / a) > 0)
            numerator = np.sum(t * np.log(y / a))
            denominator = np.sum(t ** 2)
            bVal = - (numerator / denominator)
            sheetBVals[col] = bVal
        #convert the results into a horizontal row dataframe
        #a dataframe is associated with each original sheet
        calculatedResults[sheet] = pd.DataFrame([sheetBVals])

    print("writing to excel sheet")
    with pd.ExcelWriter(spreadsheetPath, mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:
        for sheet, b_df in calculatedResults.items():
            sheetToStoreIn = f"{sheet}BVals"
            b_df.to_excel(writer, sheet_name = sheetToStoreIn, index = False)
            print(f"updated {sheetToStoreIn}")