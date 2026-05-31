import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///payments.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Midtrans (payment gateway Indonesia)
    MIDTRANS_SERVER_KEY = os.getenv('MIDTRANS_SERVER_KEY')
    MIDTRANS_CLIENT_KEY = os.getenv('MIDTRANS_CLIENT_KEY')
    MIDTRANS_IS_PRODUCTION = os.getenv('MIDTRANS_IS_PRODUCTION', 'False') == 'True'