from flask import Blueprint, jsonify, render_template, request
import folium
import os

from main_app.app_variables.variables import MAP_PATH
from main_app.data_analyze.analyze_service.query_analyze import deadliest_attacks_analyze, deadliest_orgs_analyze, active_orgs_by_country
from main_app.data_analyze.map_service.map_service import view_top_orgs_by_country, view_top_orgs_by_country_backup

attack_analyze_bp = Blueprint('attack_analyze', __name__)


@attack_analyze_bp.route('/attack_analyze/deadliest_attacks/<int:top_5>', methods=['GET'])
def get_deadliest_attacks(top_5):
    data_df = deadliest_attacks_analyze()
    if top_5 == 1:
        data_json = data_df.head().to_json(orient='records')
        return jsonify({'result': data_json}), 200
    else:
        data_json = data_df.to_json(orient='records')
        return jsonify({'result': data_json}), 200


@attack_analyze_bp.route('/attack_analyze/deadliest_orgs', methods=['GET'])
def get_deadliest_attacks_orgs():
    try:
        data_df = deadliest_orgs_analyze().head(6)
        data_json = data_df.to_json(orient='records')
        return jsonify({'result': data_json}), 200
    except Exception as ex:
        print(f'Exception occurred in deadliest_attacks_orgs analyze: {ex}')
        return jsonify({'Error': 'Internal server error occurred'}), 500


@attack_analyze_bp.route('/attack_analyze/maps/orgs_by_countries', methods=['GET'])
def get_active_orgs_by_countries():
    # country = request.form['region']
    country = request.args.get('country')
    data_df = active_orgs_by_country(country)
    if data_df is None:
        return jsonify({'Bad request': 'Country does not exist in the data base'}), 400
    folium_map = view_top_orgs_by_country(data_df)
    if folium_map:
        map_path = os.path.join(MAP_PATH, "map.html")
        folium_map.save(map_path)
        return render_template("index.html")
    else:
        return jsonify({'Bad request': f'Could not find country name - {country}'}), 400

# Backup
@attack_analyze_bp.route('/attack_analyze/orgs_by_countries/backup', methods=['GET'])
def get_active_orgs_by_countries_backup():
    country = request.args.get('country')
    data_df = active_orgs_by_country(country)
    if data_df is None:
        return jsonify({'Bad request': 'Country does not exist in the data base'}), 400
    folium_map = view_top_orgs_by_country_backup(data_df)
    map_path = os.path.join(MAP_PATH, "map.html")
    folium_map.save(map_path)
    return render_template("index.html")


@attack_analyze_bp.route('/attack_analyze/maps/render_maps')
def render_map():
    print('Render the map')
    return render_template('./map.html')

