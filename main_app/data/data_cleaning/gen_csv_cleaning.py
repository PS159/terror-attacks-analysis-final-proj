import pandas as pd

from main_app.app_variables.variables import MAIN_CSV_DS_PATH

from main_app.data.data_cleaning.clean_main_csv import clean_df


def remove_columns(df, columns_to_save):
    column_names = list(df.columns)
    column_to_remove = [column for column in column_names if column not in columns_to_save]
    df = df.drop(column_to_remove, axis=1)
    print(f'Removed columns successfully, remaining columns: {df.columns}\n')
    return df


def rename_all_columns(df, new_columns_names):
    df.columns = new_columns_names
    print(f'Renamed all columns successfully, columns names: {df.columns}\n')
    return df


def load_clean_csv(csv_path):
    """
    for testing purposes
    creates a clean csv file
    """
    df = pd.read_csv(csv_path, encoding='latin-1', low_memory=False)
    columns_to_save = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt',
                       'latitude', 'longitude', 'success', 'summary',
                       'attacktype1_txt', 'targtype1_txt', 'gname', 'nkill', 'nwound']
    new_columns_names = ['country', 'region', 'lat', 'lon', 'description',
                         'successful', 'attack_type', 'target_type',
                         'terror_organization', 'killed', 'injured', 'date']
    cleaned_df = clean_df(df, columns_to_save, new_columns_names)
    with open('C:/Users/mkf/Desktop/IDF DATA Course/Tests/final_test_18_-_24_12_24/main_app/data/csv/clean_datasets/clean_main_csv.csv', encoding='latin-1', mode='w') as file:
        cleaned_df.to_csv(file)
    print('Successfully loaded clean_df to csv')


# Test
if __name__ == '__main__':
    load_clean_csv(MAIN_CSV_DS_PATH)
