from flask import Flask

from main_app.data_analyze.app.attack_analyze_bp import attack_analyze_bp


app = Flask(__name__)


app.register_blueprint(attack_analyze_bp)


if __name__ == '__main__':
    app.run(debug=True)


