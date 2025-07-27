# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin",
        "email": "admin@example.com",
        "hashed_password": "$2a$08$EIAMHXV1PVEJ6PV3IcCsSuBDnAyerGlGSMQWm2iQNu4qNRuCouIru",
        "disabled": False,
    }
}
