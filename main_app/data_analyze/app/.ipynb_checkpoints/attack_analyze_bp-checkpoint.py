from flask import Blueprint, jsonify, render_template
import folium
import os

from main_app.data_analyze.analyze_service.query_analyze import deadliest_attacks_analyze, deadliest_orgs_analyze, active_orgs_by_country

attack_analyze_bp = Blueprint('attack_analyze', __name__)


@attack_analyze_bp.route('/attack_analyze/deadliest_attacks/<int:head>', methods=['GET'])
def get_deadliest_attacks(head):
    data_df = deadliest_attacks_analyze()
    if head == 1:
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

@attack_analyze_bp.route('/attack_analyze/orgs_by_countries', methods=['GET'])
def get_active_orgs_by_countries():
    try:
        data_df = active_orgs_by_country().head()
        data_json = data_df.to_json(orient='records')
        return jsonify({'result': data_json}), 200
    except Exception as ex:
        print(f'Exception occurred in deadliest_attacks_orgs analyze: {ex}')
        return jsonify({'Error': 'Internal server error occurred'}), 500


@attack_analyze_bp.route('/attack_analyze/maps/render_maps')
def render_map():
    return render_template('./map.html')


@attack_analyze_bp.route('/attack_analyze/maps', methods=['GET', 'POST'])
def index():
    start_coords = (30.0, 100.7)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    map_path = os.path.join("C:/Users/mkf/Desktop/IDF DATA Course/Tests/final_test_18_-_24_12_24/main_app/maps/templates", "map.html")
    folium_map.save(map_path)
    return render_template("index.html")