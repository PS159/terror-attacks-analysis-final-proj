import pandas as pd

from main_app.app_variables.variables import MAIN_CSV_DS_PATH
from gen_csv_cleaning import remove_columns, rename_all_columns



def fill_date_details(df):
    df.loc[df["iday"] == 0, "iday"] = 1
    df.loc[df["imonth"] == 0, "imonth"] = 1
    print(f'Sum fields that contain 0 in the month column: {len(df.loc[df["imonth"] == 0])}')
    print(f'Sum fields that contain 0 in the day column: {len(df.loc[df["iday"] == 0])}\n')
    return df

def change_to_date_column(df):
    """
    add the 'Date' column, combining the 'iyear', 'imonth' and 'iday' columns
    and drop those three columns:
    """
    df['Date'] = pd.to_datetime(df.iyear * 10000 + df.imonth * 100 + df.iday, format='%Y%m%d')
    df = df.drop(['iyear', 'imonth', 'iday'], axis=1)
    print(f"Removed the 'iyear', 'imonth' and 'iday' columns successfully, df columns: {df.columns}\n")
    return df

def _0_and_1_to_boolean(df):
    """
    Change the 'successful' column values to true and false
    (instead of '0' and '1'):
    """
    df.iloc[:, 5:6] = df.iloc[:, 5:6].astype(bool)
    print(f'Changed "successful" column to boolean, column top 10:\n {df["successful"][:10]}\n')
    return df

def create_id_columns(df):
    """
    creates an 'id' column for the different tables
    """
    df['id'] = df.index + 1
    df['terror_organization_id'] = df.groupby('terror_organization', sort=False).ngroup() + 1
    df['attack_type_id'] = df.groupby('attack_type', sort=False).ngroup() + 1
    df['target_type_id'] = df.groupby('target_type', sort=False).ngroup() + 1
    df['region_id'] = df.groupby('region', sort=False).ngroup() + 1
    df['country_id'] = df.groupby('country', sort=False).ngroup() + 1
    return df

def unknown_to_none(df):
    df = df.replace('Unknown', None)
    return df

def clean_df(df, columns_to_save, new_columns_names):
    clean_columns = remove_columns(df, columns_to_save)
    full_dates = fill_date_details(clean_columns)
    containing_date = change_to_date_column(full_dates)

    renamed_columns = rename_all_columns(containing_date, new_columns_names)
    success_to_boolean = _0_and_1_to_boolean(renamed_columns)
    containing_ids = create_id_columns(success_to_boolean)

    print('Finished cleaning csv successfully')
    return containing_ids

def split_df(csv_path):
    """
    get csv, covert to df (use 'clean_df'),
     clean and reorder the columns,
    split the df according to the db tables,
    return a dict of the dfs
    """
    df = pd.read_csv(csv_path, encoding='latin-1', low_memory=False)
    columns_to_save = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt',
                       'latitude', 'longitude', 'success', 'summary',
                       'attacktype1_txt', 'targtype1_txt', 'gname', 'nkill', 'nwound']
    new_columns_names = ['country', 'region', 'lat', 'lon', 'description',
                         'successful', 'attack_type', 'target_type',
                         'terror_organization', 'killed', 'injured', 'date']
    new_columns_order = ['id', 'date', 'lat', 'lon', 'description',
                             'successful', 'killed', 'injured',
                             'terror_organization_id', 'attack_type_id',
                             'target_type_id', 'region_id', 'country_id',
                             'country', 'region', 'attack_type',
                             'target_type', 'terror_organization']
    try:
        cleaned_df = clean_df(df, columns_to_save, new_columns_names)
        df_reordered = cleaned_df[new_columns_order]

        all_data_frames = {}
        terror_attack_df = df_reordered.loc[:, : 'country']
        all_data_frames['terror_attacks'] = terror_attack_df
        country_df = df_reordered[['country_id', 'country', 'region_id']].groupby(['country_id', 'country', 'region_id']).size().reset_index(name='count')
        all_data_frames['countries'] = country_df
        region_df = df_reordered[['region_id', 'region']].groupby(['region_id', 'region']).size().reset_index(name='count')
        all_data_frames['regions'] = region_df
        attack_type_df = df_reordered[['attack_type_id', 'attack_type']].groupby(['attack_type_id', 'attack_type']).size().reset_index(name='count')
        all_data_frames['attack_types'] = attack_type_df
        target_type_df = df_reordered[['target_type_id', 'target_type']].groupby(['target_type', 'target_type_id']).size().reset_index(name='count')
        all_data_frames['target_types'] = target_type_df
        terror_org_df = df_reordered[['terror_organization_id', 'terror_organization']].groupby(['terror_organization_id', 'terror_organization']).size().reset_index(name='count')
        all_data_frames['terror_orgs'] = terror_org_df
        print('Split data frames successfully')
        return all_data_frames

    except Exception as ex:
        print(f'Exception occurred during splitting of data frames: {ex}')
        return None

def df_to_dict(dfs: dict):
    try:
        df_dicts = {}
        for key, value in dfs.items():
            df_dicts[key] = value.to_dict('records')
        print('Successfully converted all data frames to dictionaries')
        return df_dicts
    except Exception as ex:
        print(f'Exception occurred during converting data frames to dictionaries: {ex}')


# Test
if __name__ == '__main__':
    clean_df(pd.read_csv(MAIN_CSV_DS_PATH, encoding='latin-1', low_memory=False))

