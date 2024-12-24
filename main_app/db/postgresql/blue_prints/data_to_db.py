from flask import Blueprint, jsonify

from main_app.data_analyze.map_service.map_service import json_country_coords
from main_app.db.postgresql.init_db.init_db import init_database
from ..insert_csv_data.insert_main_csv import insert_main_csv
from main_app.app_variables.variables import MAIN_CSV_DS_PATH
from ..session.session_maker import db_session
from ..models.db_models import TerrorAttack
from main_app.data.data_cleaning.gen_csv_cleaning import load_clean_csv


insert_data_bp = Blueprint('insert_data', __name__)


@insert_data_bp.route('/insert_data/main_csv', methods=['GET'])
def insert_main_csv_data():
    init_database()
    insert_main_csv(MAIN_CSV_DS_PATH)
    """
    Possibly run 'load_clean_csv(MAIN_CSV_DS_PATH)' -
    creates a clean csv for testing
    """
    print('Inserted csv data into the db')
    db_test = db_session.query(TerrorAttack).filter(TerrorAttack.killed == 0.0).all()
    return jsonify({'Success': f'successfully inserted main csv into db, query example: {db_test}'}), 200


@insert_data_bp.route('/insert_data/country_coords_to_json', methods=['GET'])
def save_coords_by_country_name():
    try:
        json_country_coords()
        return jsonify({'Success': 'Successfully saved countries coordinates to json'})
    except Exception as e:
        print(f'Exception occurred while getting country coordinates: {e}')
        return jsonify({'Error': 'Internal server error'}), 500

