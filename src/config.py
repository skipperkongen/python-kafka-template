class Config:
    JWT_SECRET_KEY = 'dinmor'#os.environ['JWT_SECRET_KEY']
    SECRET_KEY = 'dinmor'#os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'#os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = Config
