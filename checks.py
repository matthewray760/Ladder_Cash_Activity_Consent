import pandas as pd



### to ensure identical cash transfer is posted

def cash_tran_check(bulk_entry, cash_transactions):
    print(bulk_entry.dtypes)
    print(cash_transactions.dtypes)

    bulk_entry['Amount'] = bulk_entry['Amount'].astype(float)
    cash_transactions['Amount'] = cash_transactions['Amount'].astype(float)

    bulk_entry['Post Date'] = pd.to_datetime(bulk_entry['Post Date'])
    bulk_entry['Post Date'] = bulk_entry['Post Date'].dt.strftime('%m/%d/%Y')


    
    merged_df = bulk_entry.merge(
        cash_transactions,
        how = 'left',
        left_on = ['Post Date', 'Amount'],
        right_on=[ 'Post Date', 'Amount'],
        indicator = True
        )
    merged_df['Match'] = merged_df['_merge'].apply(lambda x: 'Y' if x == 'both' else 'N')

    merged_df.to_excel(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\outputs\check_output.xlsx')
