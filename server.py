import flask_citas_dojo.controllers.core
from flask_citas_dojo.controllers.citas import citas

from flask_citas_dojo import app

app.register_blueprint(citas, url_prefix='/citas')


if __name__ == "__main__":
    app.run(debug=True)