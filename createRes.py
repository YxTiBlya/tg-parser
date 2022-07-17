import pandas as pd

def create_Excel_Table2GIS(results, req):
    df = pd.DataFrame()
    writer = pd.ExcelWriter(f'2gis/{req}.xlsx')

    name = []
    adress = []
    number = []
    Wapp = []

    for result in results:
        name.append(result[0])
        adress.append(result[1])
        number.append(result[2])
        Wapp.append(result[3])

    df['Название'] = name
    df['Адресс'] = adress
    df['Номер'] = number
    df['WhatsApp'] = Wapp

    df.to_excel(writer, sheet_name='result', index=False, na_rep='NaN')

    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['result'].set_column(col_idx, col_idx, column_width)

    writer.save()

def create_Excel_TableAVITO(results, req):
    df = pd.DataFrame()
    writer = pd.ExcelWriter(f'avito/{req}.xlsx')

    name = []
    price = []
    link = []

    for vacancy in results:
        name.append(vacancy[0])
        price.append(vacancy[1])
        link.append(vacancy[2])

    df['Название'] = name
    df['Оплата'] = price
    df['Резюме'] = link

    df.to_excel(writer, sheet_name='result', index=False, na_rep='NaN')

    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['result'].set_column(col_idx, col_idx, column_width)

    writer.save()