from flask import Flask
from flask_cors import CORS
from routes.prompts import prompts_bp
from routes.transcription import transcription_bp
from routes.complete import complete_bp
from routes.videos import videos_bp
from prisma import Prisma, register

db = Prisma()
db.connect()
register(db)

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(prompts_bp)
app.register_blueprint(transcription_bp)
app.register_blueprint(complete_bp)
app.register_blueprint(videos_bp)


if __name__ == "__main__":
    app.run(debug=True)