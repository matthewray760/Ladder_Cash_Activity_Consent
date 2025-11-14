import pandas as pd
import numpy as np
import openpyxl
import xlsxwriter



def def_excel(cashsheet_filename,bulk_entry,cash_transfers,concat_df):

    pathway = fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\outputs\{cashsheet_filename}_output.xlsx'

    writer = pd.ExcelWriter(pathway,engine= 'openpyxl', mode='w')

    concat_df.to_excel(writer, sheet_name= 'Bulk Entry', index=False)
    bulk_entry.to_excel(writer, sheet_name= 'OE_OI', index=False)
    cash_transfers.to_excel(writer, sheet_name= 'TRN', index=False)

    for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column_cells in worksheet.columns:
                max_length = 0
                column = column_cells[0].column_letter
                for cell in column_cells:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 6)
                worksheet.column_dimensions[column].width = adjusted_width
    print("Python: Executed successfully. Output file created")
    writer.save()

