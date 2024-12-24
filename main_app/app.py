from flask import Flask

from main_app.db.postgresql.blue_prints.data_to_db import insert_data_bp

app = Flask(__name__)


app.register_blueprint(insert_data_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5001)