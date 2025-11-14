import pandas as pd
from load_data import load_mappings, load_cash_activity, load_tran_detail
from to_excel import def_excel
from checks import cash_tran_check


to_excel = False

use_excel_for_mapping = True

cashsheet_filename = '10.2025_final'
mapping_filename = 'GL_Mappings'
tran_detail_filename = '10.2025_test' ## make sure Amount datatypes is Number

### Load data from cash activity file and mappings file
cashsheet = load_cash_activity(cashsheet_filename)
mappings = load_mappings(mapping_filename)
cash_tran_detail = load_tran_detail(tran_detail_filename)



### create list of mappings to short description
modifications = mappings['Short Description'].tolist()
modifications_man = ['Excess Funds']
print(modifications)

if use_excel_for_mapping == True:
    filtered_cashsheet = cashsheet[cashsheet['Short Description'].str.contains('|'.join(modifications))]

else:
    filtered_cashsheet = cashsheet[cashsheet['Short Description'].str.contains('|'.join(modifications_man))]



merged_df = pd.merge(filtered_cashsheet,mappings, on='Short Description')

merged_df['Date'] = merged_df['Date'].dt.date



### Create bulk cash entry
bulk_cash_entry = merged_df[['Account ID','Date','Amount']].copy()

bulk_cash_entry.loc[bulk_cash_entry['Amount'] > 0, 'Transaction Type'] = 'INC'
bulk_cash_entry.loc[bulk_cash_entry['Amount'] < 0, 'Transaction Type'] = 'EXP'

bulk_cash_entry.loc[:,'Entry Date'] = bulk_cash_entry['Date']
bulk_cash_entry.loc[:,'Settle Date'] = bulk_cash_entry['Date']
bulk_cash_entry.loc[:,'Post Date'] = bulk_cash_entry['Date']
bulk_cash_entry.loc[:,'Currency'] = 'USD'
bulk_cash_entry.loc[:,'Asset ID'] = 'CCYUSD'

bulk_cash_entry = bulk_cash_entry[['Account ID','Transaction Type', 'Entry Date', 'Settle Date', 'Post Date', 'Asset ID', 'Currency', 'Amount']]



#### creating offsetting cash transfers

cash_transfers = bulk_cash_entry.copy()
cash_transfers['Amount_1'] = cash_transfers['Amount'] * -1
cash_transfers.drop(columns='Amount', inplace= True)
cash_transfers.rename(columns={'Amount_1':'Amount'}, inplace=True)
cash_transfers['Transaction Type'] = 'TRN'




concat_df = pd.concat([bulk_cash_entry,cash_transfers])



### do Checks

tran_check = cash_tran_check(bulk_entry=bulk_cash_entry, cash_transactions=cash_tran_detail)

if to_excel == True:
    def_excel(cashsheet_filename=cashsheet_filename,bulk_entry=bulk_cash_entry,cash_transfers=cash_transfers,concat_df=concat_df)

#bulk_cash_entry.to_excel(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\outputs\{cashsheet_filename}_output.xlsx')
