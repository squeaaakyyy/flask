class Configuration(object):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root@localhost/music_news'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///news_base.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'abcabc'

    ### Flask-sequrity
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
