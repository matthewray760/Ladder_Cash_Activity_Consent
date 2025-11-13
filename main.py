import pandas as pd


filename = '10.2025_final'




dataframes = []

xls = pd.ExcelFile(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\Cash Entry File\inputs\{filename}.xlsx')


for sheet in xls.sheet_names:
    if 'Cash Activity' in sheet:
        df = pd.read_excel(xls, sheet_name=sheet, skiprows=3)
        df['Source_Sheet'] = sheet

        dataframes.append(df)


combined_df = pd.concat(dataframes, ignore_index=True)

combined_df.dropna(subset=['Short Description'], inplace=True)


consent_fees = ['Float Payment','Consent','Defeasance']

combined_df = combined_df[combined_df['Short Description'].str.contains('|'.join(consent_fees))]

combined_df.to_excel(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\Cash Entry File\outputs\{filename}_output.xlsx')

print(combined_df)
