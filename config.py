
class Config:
    #DB 관련
    HOST = 'mysqlinstance.cr2sp2mx5gjz.ap-northeast-2.rds.amazonaws.com'
    DATABASE = 'recipe_db'
    DB_USER = 'recipe_db_user'
    DB_PASSWORD = '1234'

    # 비번 암호화
    SALT = '1q2w3e4r'

    # jwt 변수 셋팅
    JWT_SECRET_KEY = 'jwt_secret_key'
    JWT_ACCESS_TOKKEN_EXPIRES = False
    PROPAGATE_EXCEPTIONS = True

