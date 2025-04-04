import pandas as pd

file_path = 'Data.xlsx'  

expected_cols = [
    'ID', 'Nganh', 'Gioi tinh', 'Doi tuong', 'Khu vuc', 
    'Khoi TS', 'Diem TS', 'Hoc Ky', 'DKHK', 'TBHK', 
    'TCTL', 'TBTL', 'XLHV', 'Diem TN', 'KET QUA'
]

xls = pd.ExcelFile(file_path)
sheet_names = ['Data1', 'Data2', 'Data3', 'Data4']

df_list = []
for sheet in sheet_names:
    df_sheet = pd.read_excel(xls, sheet_name=sheet, header=0)
    df_sheet.columns = expected_cols
    df_list.append(df_sheet)

df_all = pd.concat(df_list, ignore_index=True)

df_sorted = df_all.sort_values(by=['ID', 'Hoc Ky'], ascending=[True, True])

output_file = 'raw_data.csv'
df_sorted.to_csv(output_file, index=False, encoding='utf-8-sig')

print("Đã lưu file CSV:", output_file)
