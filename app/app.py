from modules import *
from modules import db_functions as db

db_path = 'app/instance/game.db'

load_dotenv()

def create_app():
    app = Flask(__name__)

    from routes import main
    app.register_blueprint(main)

    db.create(db_path)

    return app

employees = [ { 'id': 1, 'name': 'Ashley' }, { 'id': 2, 'name': 'Kate' }, { 'id': 3, 'name': 'Joe' }]


# --- MAIN ---

PORT = os.getenv("PORT")

if __name__ == "__main__":
    app = create_app()
    app.run(port=PORT)