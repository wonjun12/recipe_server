from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

# API 동작하는 코드를 만들기 위해서는, class를 만들어야 한다.

# class 란??
# 비슷한 데이터끼리 모아놓은 것 (테이블)
# 단, 테이블과 다르게 변수와 함수로 구성된 묶음을 말한다.

# API를 만들기 위해서는, 
# flask_restful 라이브러리의 Resource 클래스를 상속해서 만들어야한다.
# 파이썬에서 상속은 괄호

# 요청 데이터 확인 객체
from flask import request

# mysql 연결 import
from mysql_connection import get_connection
# mysql 라이브러리 Error 사용하기
from mysql.connector import Error

class 아무거나_이름(Resource) : 
    
        # jwt 를 받아오기에 필수다.
    @jwt_required()
    # Resource 클래스의 상속받은 post 함수를 사용하는 부분
    def post(self):
        # post 요청 데이터 처리 코드 작성하기
        
        # 보내는 JSON 데이터 관해서 복사해서 보면서 하자.
        # {
        #     "name": "김치찌게",
        #     "description": "맛있게 끓이는 방법.",
        #     "num_of_servings": 4,
        #     "cook_time": 30,
        #     "directions": "고기볶고 김치 넣고 물 넣고, 두부 넣으면 된다는데?",
        #     "is_publish": 1
        # }

        # POST 저장 순서 작성
        # 1. 클라이언트가 보낸 데이터를 받아온다.
        # 2. 받아온 데이터를 DB에 저장한다.
        # 3. 에러 발생시 에러 응답, 저장된다면 완료 응답 보낸다.

        # 1. 데이터 받기
        받은_데이터 = request.get_json()
        print(받은_데이터)

            # 로그인한 헤더의 정보 JWT를 받는다.
            # 헤더에서 JWT를 바로 가져와서 내가 넣은 값을 바로 얻는다.
        user_id = get_jwt_identity()

        # 2.DB 저장
        # 1) 데이터 베이스 연결
        try : 
            connection = get_connection()

            # 2) 쿼리문 만들기
            # 데이터를 저장시킬것이니, insert
            # Workbench에서 미리 테스트 할것
            query = """
                insert into recipe
                (name, description, num_of_servings, cook_time, directions, is_publish, user_id)
                values
                (%s, %s, %s, %s, %s , %s, %s);
            """ # 컬럼과 매칭되는 데이터 들을 %s 로 변경하자.

            # 3) 쿼리에 매칭되는 변수를 처리하자.
            # 튜플로 처리
            record = (
                받은_데이터['name'], 
                받은_데이터['description'], 
                받은_데이터['num_of_servings'],
                받은_데이터['cook_time'],
                받은_데이터['directions'],
                받은_데이터['is_publish'],
                user_id
                )
            
            # 4) 커서를 가져온다.
            cursor = connection.cursor()

            # 5) 쿼리문 실행
            cursor.execute(query, record)

            # 6) DB 반영 완료 commit
            connection.commit()

            # 7) 자원 해제 (메모리 삭제)
            cursor.close()
            connection.close()

        except Error as e:
            # 3. 에러 처리
            print(e)
            return {
                'result' : 'fail',
                'error' : str(e)
            }, 500
        
        
        # 3. 정상적으로 완료 시 성공 처리
        return {
            'result' : 'success'
        }, 200

    def get(self):
        # 1. 클라이언트에서 데이터를 받아온다.
            # = 현재 없음
        # 2. 저장된 레시피 리스트를 DB로 부터 가져온다.
        try : 
            # 1) DB 연결
            DB_연결 = get_connection()

            # 2) 쿼리문 만들기
            # 쿼리문 = """
            #     select * 
            #     from recipe
            #     order by created_at desc;
            # """
                # 2--) 유저이름과 퍼블리쉬관련 추가
            쿼리문 = '''
                select r.*, u.username
                from recipe r
                    join user u
                    on r.user_id = u.id
                where is_publish = 1;
            '''

            # 3) 변수처리할 부분은 변수처리 한다.
                # = 없음
            
            # 4) 커서 가져오기
            커서_띵 = DB_연결.cursor(dictionary=True)
                # 그냥 사용시, 튜플의 형태로 가져오게된다.
                # 해당 옵션으로 딕셔너리 형태로 가져오자.
                # 왜? JSON의 형태로 보내기 위해

            # 5) 쿼리문을 커서로 실행한다.
            커서_띵.execute(쿼리문)

            # 6) 실행 결과를 가져온다.
            DB_값들 = 커서_띵.fetchall()

            # 7) 메모리 종료
            커서_띵.close()
            DB_연결.close()
            print(DB_값들)
        except Error as e:
            return {
                'result' : 'fail',
                'error' : str(e)
            }, 500

        # 3. 데이터 가공이 필요하면, 가공한 후에 클라이언트에 응답한다.
            # 문자열과 숫자만 보낼수 있기때문에 그 외의 것들을 전부 바꿔준다.
        # datetime의 값들을 바꿔주자.
        for i in range(len(DB_값들)):
            DB_값들[i]['created_at'] = DB_값들[i]['created_at'].isoformat()
            DB_값들[i]['updated_at'] = DB_값들[i]['updated_at'].isoformat()

        return {
            'result' : 'success',
            'count' : len(DB_값들),
            'items' : DB_값들
        }, 200 # 상태코드 보낼 수 있음


class DB_1개_조회(Resource):

    # GET 메서드에서 파라미터로 받는 값을 
    # get함수의 매개변수로 받는다.
    def get(self, recipe_id):
        # 1. 클라이언트로 부터 데이터를 받는다.
            # 위 매개변수 recipe_id에 담겨있다.

        # 2. 데이터베이스에 특정 아이디로 쿼리한다.
        try:
            DB_연결 = get_connection()

            쿼리 = '''
                select r.*, u.username
                from recipe r
                    join user u
                    on r.user_id = u.id
                where r.id = %s;
            '''

            쿼리_값 = [recipe_id ]

            커서 = DB_연결.cursor(dictionary=True)

            커서.execute(쿼리, 쿼리_값)

            불러온_값 = 커서.fetchall()
            print(불러온_값)

            커서.close()
            DB_연결.close()
            
        except Error as e:
            print(e)
            return {
                'result' : 'error',
                'error' : str(e)
            }, 500

        # 3. 결과를 클라이언트에 응답한다.
        for i in range(len(불러온_값)):
            불러온_값[i]['created_at'] = 불러온_값[i]['created_at'].isoformat()
            불러온_값[i]['updated_at'] = 불러온_값[i]['updated_at'].isoformat()
        
        return {
            'result' : 'success',
            'item' : 불러온_값[0] if len(불러온_값) != 0 else 'No Data'
            # 값은 하나이니 하나만 보내자.
        }, 200 if len(불러온_값) != 0 else 404
    
    #jwt 받기 함수
    @jwt_required()
    # 수정 함수 PUT
    # 데이터를 수정할때 사용하는 함수이다.
    def put(self,recipe_id):
        data = request.get_json()
        
        user_id = get_jwt_identity()

        try:
            connection = get_connection()

            query = '''
                update recipe
                set name = %s, 
                    description = %s, 
                    num_of_servings = %s, 
                    cook_time = %s, 
                    directions = %s, 
                    is_publish = %s
                where id = %s and user_id = %s;
            '''

            record = (
                data['name'],
                data['description'],
                data['num_of_servings'],
                data['cook_time'],
                data['directions'],
                data['is_publish'],
                recipe_id,
                user_id
                )
            
            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()
            
            cursor.close()
            connection.close()
        except Error as e:
            return {
                'result' : 'fail',
                'error' : str(e)
            }, 500
        
        return {
            'result' : 'success'
        }
    

    # jwt 필수 함수
    @jwt_required()
    # 삭제 함수 DELETE
    # 데이터를 삭제할때 사용하는 함수이다.
    def delete(self, recipe_id):

        user_id = get_jwt_identity()
        try:
            connection = get_connection()

            query = '''
                delete from recipe
                where id = %s and user_id = %s;
            '''

            record = (recipe_id, user_id)

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            return {
                'result' : 'fail',
                'error' : str(e)
            }, 500



        return {
            'result' : 'success'
        }
    



class 실습_레시피_전체조회(Resource):
    # 자신의 레시피만 가져오는 API
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()


        try:
            connection = get_connection()

            query = '''
                select id, name, description, num_of_servings, cook_time, directions, is_publish, created_at, updated_at
                from recipe
                where user_id = %s
                order by created_at desc;
            '''
            record = (user_id, )

            cursor = connection.cursor(dictionary= True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {
                'result' : 'fail',
                'error' : str(e)
            }
        
        for i in range(len(result_list)):
            result_list[i]['created_at'] = result_list[i]['created_at'].isoformat()
            result_list[i]['updated_at'] = result_list[i]['updated_at'].isoformat()
        
        return {
            'result' : 'success',
            'data' : result_list
        }
        
    
    
class 실습_레시피_공개수정(Resource):
    # 자신이 만든 레시피 공개하는 API
    @jwt_required()
    def put(self, recipe_id):
        data = request.get_json()
        user_id = get_jwt_identity()

        try:
            connection = get_connection()

            query = '''
                update recipe
                set is_publish = %s
                where id = %s and user_id = %s;
            '''
            record = (data['is_publish'], recipe_id, user_id)

            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {
                'result' : 'fail',
                'error' : str(e)
            }
        
        return {
            'result' : 'success'
        }




