from flask import Flask
from flask_restful import Api

from resources.recipe_test import 아무거나_이름_넣기
from resources.recipe import 아무거나_이름, DB_1개_조회

app = Flask(__name__)

api = Api(app)

# 경로와 API 동작 코드(Resource)를 연결한다.
api.add_resource( 아무거나_이름_넣기 , '/recipes_test')
api.add_resource( 아무거나_이름 , '/recipes')

# 1개 조회 URL
    # <> 파라미터 값을 넘길때 사용
api.add_resource( DB_1개_조회 , '/recipes/<int:recipe_id>')

if __name__ == '__main__':
    app.run()