import cloudinary

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

cloudinary.config(
    cloud_name="dqhskfiob",
    api_key="414385218289625",
    api_secret="5KyUedXz6D2NdNsYnua3buTG2nE"
)