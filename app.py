from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v3 as fsqla

# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager
# from flask_migrate import Migrate
# from flask_script._compat import text_type


from config import Configuration
# from posts.blueprint import posts


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)


### ADMIN ###
from models import *


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)



admin = Admin(app)
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))


### Flask-sequrity

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)


