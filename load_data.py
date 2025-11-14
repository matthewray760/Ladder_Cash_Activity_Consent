import pandas as pd


filename = 'GL_Mappings'

def load_mappings(mapping_filename):
    df = pd.read_excel(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\inputs\Mappings\{mapping_filename}.xlsx')
    return df




def load_cash_activity(cashsheet_filename):
    dataframes = []

    xls = pd.ExcelFile(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\inputs\Cash_Activity\{cashsheet_filename}.xlsx')


    for sheet in xls.sheet_names:
        if 'Cash Activity' in sheet:
            df = pd.read_excel(xls, sheet_name=sheet, skiprows=3)
            df['Source_Sheet'] = sheet

            dataframes.append(df)


    combined_df = pd.concat(dataframes, ignore_index=True)

    combined_df.dropna(subset=['Short Description'], inplace=True)
    combined_df = combined_df[combined_df['Source_Sheet'] != 'Cash Activity MM-DD']

    return combined_df



def load_tran_detail(tran_detail_filename):
    df = pd.read_csv(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\inputs\CW_Tran_Detail\{tran_detail_filename}.csv')
    return df
