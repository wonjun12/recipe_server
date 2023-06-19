from flask import Flask
from flask_restful import Api
from config import Config

from resources.recipe_test import 아무거나_이름_넣기
from resources.recipe import 실습_레시피_전체조회, 실습_레시피_공개수정, 아무거나_이름, DB_1개_조회

from resources.user import UserLogoutResource, 유저_회원가입_리소스, UserLoginResource, jwt_blocklist

from flask_jwt_extended import JWTManager

app = Flask(__name__)

# 환경 변수 셋팅
app.config.from_object(Config)
# JWT 매니저 초기화
jwt = JWTManager(app)
# 로그아웃된 토큰에 대한 요청을 비정상적으로 보고 접근못하게 해야한다.
# jwt가 알아서 처리하도록 코드 작성
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blocklist

api = Api(app)

# 경로와 API 동작 코드(Resource)를 연결한다.
api.add_resource( 아무거나_이름_넣기 , '/recipes_test')
api.add_resource( 아무거나_이름 , '/recipes')

# 1개 조회 URL
    # <> 파라미터 값을 넘길때 사용
api.add_resource( DB_1개_조회 , '/recipes/<int:recipe_id>')

# 유저 회원가입
api.add_resource( 유저_회원가입_리소스 , '/user/register')
# 유저 로그인
api.add_resource( UserLoginResource , '/user/login')
# 유저 로그아웃
api.add_resource( UserLogoutResource , '/user/logout')


# 실습
# 1. 자신이 만든 레시피를 공개하는 API
api.add_resource( 실습_레시피_공개수정, '/recipes/<int:recipe_id>/publish')
# 2. 자신이 만든 레시피를 임시저장하는 API

# 3. 자신의 레시피만 가져오는 API
api.add_resource( 실습_레시피_전체조회 , '/myrecipes')


if __name__ == '__main__':
    app.run()