from flask_restful import Resource

# API 동작하는 코드를 만들기 위해서는, class를 만들어야 한다.

# class 란??
# 비슷한 데이터끼리 모아놓은 것 (테이블)
# 단, 테이블과 다르게 변수와 함수로 구성된 묶음을 말한다.

# API를 만들기 위해서는, 
# flask_restful 라이브러리의 Resource 클래스를 상속해서 만들어야한다.
# 파이썬에서 상속은 괄호

class 아무거나_이름_넣기(Resource) : 

    # Resource 클래스의 상속받은 post 함수를 사용하는 부분
    def post(self):
        # post 요청 데이터 처리 코드 작성하기
        print('API 동작맨')
        
        # client에게 값 보내기
        return {
            'result' : 'success'
        }, 200 # 상태 코드 보내기

    def get(self):
        print('레시피 조회 API 동작맨')

        return {
            'result' : 'success',
            'count' : 3,
            'items' : [
                {
                    'id' : 1,
                    'name' : '김치찌게',
                    'description' : '우와앜'
                }
            ]
        }, 300 # 상태코드 보낼 수 있음
    
    # POST 저장 순서 작성
    # 1. 클라이언트가 보낸 데이터를 받아온다.
    # 2. 받아온 데이터를 DB에 저장한다.
    # 3. 에러 발생시 에러 응답, 저장된다면 완료 응답 보낸다.