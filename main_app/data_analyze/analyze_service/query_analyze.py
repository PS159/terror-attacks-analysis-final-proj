import pandas as pd

from main_app.db.db_config.db_config import engine
from main_app.data_analyze.analyze_service.gen_analyze_service import country_in_df


def deadliest_attacks_analyze():
    query = """
    SELECT terror_attacks.killed, terror_attacks.injured, attack_types.attack_type
    FROM terror_attacks
    JOIN attack_types ON terror_attacks.attack_type_id=attack_types.id
    """
    df = pd.read_sql_query(sql=query, con=engine)

    df['killed'] = df['killed'] * 2
    df['killed_injured'] = df.iloc[:, :2].sum(axis=1)
    result = df.groupby('attack_type', as_index=False)['killed_injured'].sum().sort_values('killed_injured', ascending=False)
    print(result.columns)

    return result['attack_type']

def deadliest_orgs_analyze():
    query = """
    SELECT terror_attacks.killed, terror_attacks.injured, terror_organizations.name
    FROM terror_attacks
    JOIN terror_organizations ON terror_attacks.terror_organization_id=terror_organizations.id
    """
    df = pd.read_sql_query(sql=query, con=engine)

    df['injured'] = df['injured'] * 2
    df['killed_injured'] = df.iloc[:, :2].sum(axis=1)
    result = df.groupby('name', as_index=False)['killed_injured'].sum().sort_values('killed_injured', ascending=False)

    return result['name']

def active_orgs_by_country(country):
    query = """
    SELECT terror_organizations.name org, countries.name country
    FROM terror_attacks
    JOIN terror_organizations ON terror_attacks.terror_organization_id=terror_organizations.id
    JOIN countries on terror_attacks.country_id=countries.id
    WHERE terror_organizations.name != 'Unknown'
    """
    df = pd.read_sql_query(sql=query, con=engine)

    count_orgs = df.groupby(['country', 'org']).agg(count=('org', 'count')).reset_index()
    top_orgs = count_orgs.sort_values(['country', 'count'], ascending=False).groupby('country').head(5).reset_index(drop=True)

    if not country:
        return top_orgs
    elif country_in_df(top_orgs, 'country', country):
        result = top_orgs.loc[top_orgs['country'] == country]
        print(result)
        return result
    else:
        print('Country does not exist in the data base')
        return None




if __name__ == '__main__':
    active_orgs_by_country(None)



