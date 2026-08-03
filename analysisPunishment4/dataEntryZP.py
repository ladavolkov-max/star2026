import pandas as pd
import os
if __name__ == "__main__":
    spreadsheetPath = 'STAR Data snalysisPunishment4ZP.xlsx'

    #checking if the spreadsheet file exists and if not creating it
    if not os.path.exists(spreadsheetPath):
        print(f"Creating a new Excel file because '{spreadsheetPath}' was not found.")
        pd.DataFrame().to_excel(spreadsheetPath)

    #dictionary with sheet name key and folder path value
    sheetToPath = {
        'vision0.05' : '/Users/ladavolkov/Desktop/analysisPunishment4/3x3MazeVision/visionInversePun0.05/data/zeroProportions',
        'vision0.1' : '/Users/ladavolkov/Desktop/analysisPunishment4/3x3MazeVision/visionInversePun0.1/data/zeroProportions',
        'spatial0.05' : '/Users/ladavolkov/Desktop/analysisPunishment4/3x3MazeSpatial/spatialInversePun0.05/data/zeroProportions',
        'spatial0.1' : '/Users/ladavolkov/Desktop/analysisPunishment4/3x3MazeSpatial/spatialInversePun0.1/data/zeroProportions'
    }
    finalSheetData = {}

    #getting the data for each sheet
    for sheet, folderPath in sheetToPath.items():
        print(f"Processing {folderPath} data into {sheet}")
        columnsList = []
        for i in range(1, 41):
            #getting the path to the data file
            fileName = f"zeroProportions{i}.txt"
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
                print(f"successfully saved sheet {sheet}")

