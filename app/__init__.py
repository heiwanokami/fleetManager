from sqlalchemy import MetaData
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import babel
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
app.config.from_object(Config)

db = SQLAlchemy(app)

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
migrate = Migrate(app, db, render_as_batch=True)

login = LoginManager(app)
login.login_view = 'login'


# sqlalchemy = SQLAlchemy()
# sqlalchemy.init_app(app)

# db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
# migrate = Migrate(app, db, render_as_batch=True)

@app.template_filter()
def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="dd.MM.yyyy"
    return babel.dates.format_datetime(value, format)


from app import routes, models