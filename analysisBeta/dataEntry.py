import pandas as pd
import os
if __name__ == "__main__":
    spreadsheetPath = 'STAR Data Beta.xlsx'

    #checking if the spreadsheet file exists and if not creating it
    if not os.path.exists(spreadsheetPath):
        print(f"Creating a new Excel file because '{spreadsheetPath}' was not found.")
        pd.DataFrame().to_excel(spreadsheetPath)

    #dictionary with sheet name key and folder path value
    sheetToPath = {
        '0.25Data' : 'analysis4x4Maze0.25',
        '0.5Data' : 'analysis4x4Maze0.5',
        '0.75Data' : 'analysis4x4Maze0.75'
    }
    finalSheetData = {}

    #getting the data for each sheet
    for sheet, folderPath in sheetToPath.items():
        print(f"Processing {folderPath} data into {sheet}")
        columnsList = []
        for i in range(0, 40):
            #getting the path to the data file
            fileName = f"batch{i}.txt"
            filePath = os.path.join(folderPath, fileName)
            #putting data from each file into a list
            if os.path.exists(filePath):
                print(f"getting data for batch {i}")
                colHeader = f"batch{i}"
                col = pd.read_csv(filePath, header=None, names=[colHeader])
                #each batch goes into its own column
                columnsList.append(col)
            else:
                print(f"!!! Missing file {fileName} in {folderPath}!")
            #combining all the columns
            finalSheetData[sheet] = pd.concat(columnsList, axis=1)

    #writing everything to the excel file
    with pd.ExcelWriter(spreadsheetPath, mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:
        for sheet in sheetToPath.keys():
            if sheet in finalSheetData:
                finalSheetData[sheet].to_excel(writer, sheet_name = sheet, index = False)
                #print(f"successfully saved sheet {sheet}")

