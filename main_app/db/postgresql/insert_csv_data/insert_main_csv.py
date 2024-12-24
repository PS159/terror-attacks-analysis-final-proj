from main_app.data.data_cleaning.clean_main_csv import split_df
from main_app.data.data_cleaning.clean_main_csv import df_to_dict
from main_app.db.postgresql.session.session_maker import db_session
from main_app.db.postgresql.models.db_models import AttackType, Region, Country, TargetType, TerrorOrg, TerrorAttack


def insert_main_csv(csv_path):
    dfs = split_df(csv_path)
    data_dfs = df_to_dict(dfs)
    attack_types = data_dfs['attack_types']
    for attack_type in attack_types:
        attack_type = AttackType(
            id=attack_type['attack_type_id'],
            attack_type=attack_type['attack_type'],
            count=attack_type['count']
        )
        db_session.add(attack_type)
        print('Added all attack_types to table attack_types')
    db_session.commit()
    print('Successfully committed attack_types to table attack_types')

    regions = data_dfs['regions']
    for reg in regions:
        region = Region(
            id=reg['region_id'],
            region=reg['region'],
            count=reg['count'],
        )
        db_session.add(region)
    print('Added all regions to regions table successfully')
    db_session.commit()
    print('Successfully committed regions to table regions')

    countries = data_dfs['countries']
    for c in countries:
        country = Country(
            id=c['country_id'],
            name=c['country'],
            region_id=c['region_id'],
            count=c['count']
        )
        db_session.add(country)
    print('Successfully added all countries to countries table')
    db_session.commit()
    print('Successfully committed countries to table countries')

    target_types = data_dfs['target_types']
    for target in target_types:
        target_type = TargetType(
            id=target['target_type_id'],
            target_type=target['target_type'],
            count=target['count']
        )
        db_session.add(target_type)
    print('Successfully added all targets to target_types table')
    db_session.commit()
    print('Successfully committed targets to table target_types')

    terror_orgs = data_dfs['terror_orgs']
    for org in terror_orgs:
        terror_org = TerrorOrg(
            id=org['terror_organization_id'],
            name=org['terror_organization'],
            count=org['count']
        )
        db_session.add(terror_org)
    print('Successfully added all terror_orgs to terror_organizations table')
    db_session.commit()
    print('Successfully committed terror_orgs to table terror_organizations')


    terror_attacks = data_dfs['terror_attacks']
    for attack in terror_attacks:
        terror_attack = TerrorAttack(
            id=attack['id'],
            date=attack['date'],
            lat=attack['lat'],
            lon=attack['lon'],
            killed=attack['killed'],
            injured=attack['injured'],
            successful=attack['successful'],
            description=attack['description'],
            attack_type_id=attack['attack_type_id'],
            country_id=attack['country_id'],
            terror_organization_id=attack['terror_organization_id'],
            target_type_id=attack['target_type_id']
        )
        db_session.add(terror_attack)
    print('Added "terror_attack" successfully')
    db_session.commit()
    print('Finished adding all "terror_attacks" successfully')

