
def country_in_df(df, internal_param, external_param):
    # df[internal_param] = df[internal_param].str.lower()
    result = external_param in df[internal_param].values
    return result
