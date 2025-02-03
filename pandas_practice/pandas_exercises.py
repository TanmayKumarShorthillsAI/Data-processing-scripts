import pandas as pd
import os

df = pd.read_csv("./input_files/chipotle.tsv", sep="\t", header=0)

# print(df.head(), "\n", df.dtypes)

def get_data_type(df, col):
    return df[f"{col}"].dtypes


print(get_data_type(df, "item_name"))

# dfn = df.convert_dtypes()
dfn = df.astype({"item_name": "string"})
dfn = dfn.astype({"choice_description": "string"})
dfn = dfn.fillna("")


def remove_currency_symbol(dfn, item_price):
    dfn[f'{item_price}'] = dfn[f'{item_price}'].str.replace('$', '').astype(float)

    return dfn


dfn = remove_currency_symbol(dfn, 'item_price')

df1 = dfn.groupby(by=["order_id", "item_name"]).sum("item_price")

def create_output_dir():
    cwd = os.getcwd()
    dir_path = os.path.join(cwd, "output_files")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Output directory made at: {dir_path}")

    return dir_path


def save_to_excel(df, file_name, index=False):
    if file_name != '':
        try:
            dir_path = create_output_dir()
            df.to_excel(f'{dir_path}/{file_name}.xlsx', index=index)
            print(f'File: {file_name}.xlsx saved')
        except Exception as e:
            print("Can't save file to excel", e)


def total_item_cost(df):
    df['total_item_cost'] = 0
    for index,row in df.iterrows():
        quantity = row['quantity']
        item_price = row['item_price']

        df.at[index,'total_item_cost'] = item_price*quantity
    
    return df


# save_to_excel(df=df1, file_name='receipt', index=True)
# df2 = total_item_cost(dfn)
# df2 = df2.groupby(by="order_id").sum("total_item_cost")
# df2 = df2.filter(items=['order_id', 'quantity', 'total_item_cost'])
# save_to_excel(df=df2, file_name="final_order_prices", index=True)
# print(df2.head(10))

def remove_ducplicates(df):
    df_unique = df.drop_duplicates(['item_name', 'choice_description', 'quantity'])

    return df_unique

df_unique = remove_ducplicates(dfn)

def filter_products(df):
    df_filtered = df_unique[df_unique.quantity == 1]
    df_filtered = df_filtered[df_filtered.item_price > 10.00].filter(['item_name', 'choice_description', 'item_price'])

    print(df_filtered)

    return df_filtered

df_filtered = filter_products(df_unique)
save_to_excel(df=df_filtered, file_name='cost_more_than_$10')

print(dfn.sort_values(['item_name']))

def most_expensive_order_quantity(df):
    print(df.agg(['item_price','max']))
    # print(df)
most_expensive_order_quantity(df_unique)

# print(dfn.dtypes, dfn.head())
