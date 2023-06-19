from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error
from flask import request

# 이메일 확인 라이브러리
#                           이메일 확인 ,       이메일 여부 오류 확인
from email_validator import validate_email, EmailNotValidError

from utils import hash_password, check_password

#jwt 사용 
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
import datetime

# UserRegisterResource
class 유저_회원가입_리소스(Resource):

    def post(self):
        # {
        #     "username" : "김홀길",
        #     "email": "악동뮤지션",
        #     "password" : "1234"
        # }

        # 1. 클라이언트가 보낸 데이터를 받아준다.
        data = request.get_json()

        # 2. 이메일 주소형식이 올바른지 확인.
        try:
            # 이메일 형식 확인 함수
            validate_email(data['email'])
        except EmailNotValidError as e:
            # 실패시 오류를 일으키니 리턴함
            return {
                'result' : 'fail',
                'error' : str(e)
            }, 400
        
        # 3. 비밀번호 길이가 유효한지 체크한다.
        # 비밀번호 4자리 이상, 12자리 이하로 한다.
        if len(data['password']) < 4 or len(data['password']) > 12:
            return {
                'result' : 'fail',
                'error' : '비번 길이 에러'
            }, 400
        

        # 4. 비밀번호를 암호화 한다.
        hashed_psasword = hash_password(data['password'])


        # 5. DB에 이미 회원정보가 있는지 확인한다.
        try:
            connection = get_connection()
            qery = '''
                select *
                from user
                where email = %s;
            '''
            record = (data['email'], )

            cursor = connection.cursor()
            cursor.execute(qery, record)

            result_list = cursor.fetchall()

            if len(result_list) == 1:
                return {
                    'result' : 'fail',
                    'error' : '이미 회원이 있음'
                }
            

            # 회원이 아니므로, 회원가입 코드를 작성한다.
            # db에 저장한다.
            qery ='''
                insert into user
                (username, email, password)
                values
                (%s, %s, %s);
            '''
            record = (data['username'], data['email'], hashed_psasword)
            cursor = connection.cursor()
            cursor.execute(qery, record)

            connection.commit()

                # 로그인 후에 만든 코드
                # DB에 넣고 유저id를 가져오는 코드를 작성
            user_id = cursor.lastrowid

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {
                'result':'fail',
                'error' : str(e)
            }, 500


        # jwt 암호화 
        #create_access_token(user_id, expires_delta=datetime.timedelta(days=10))
        access_token = create_access_token(user_id)

        return {
            'result' : 'success',
            'access_token' : access_token
        }
    
class UserLoginResource(Resource):
    def post(self):
        # {
        #     "email": "qwe1233asd@naber.com",
        #     "password" : "1234"
        # }

        # 클라이언트로부터 데이터를 받아온다.
        data = request.get_json()

        # 이메일 주소로, DB에 select한다.
        try:
            connection = get_connection()
            qery = '''
                select *
                from user
                where email = %s;
            '''
            record = (data['email'], )

            cursor = connection.cursor(dictionary=True)
            cursor.execute(qery, record)

            result_list = cursor.fetchall()

            if len(result_list) == 0:
                return {
                    'result' : 'fail',
                    'error' : '등록된 회원이 없음'
                }

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {
                'result':'fail',
                'error' : str(e)
            }, 500
        

        # 비밀번호가 일치하는지 확인한다.
            # 암호화된 비밀번호가 일치하는지 확인해야함
        if not check_password(data['password'], result_list[0]['password']):
            return{
                'result' : 'fail',
                'error' : '비밀번호 일치하지 않음'
            }, 400


        # 클리이언트에게 데이터를 보내준다.
            # 데이터를 암호화해서 클라이언트에게 보내야한다.
        access_token = create_access_token(result_list[0]['id'],)

        return {
            'result' : 'success',
            'access_token' : access_token
        }
    


## 로그아웃된 토큰을 저장할 set을 만든다.
jwt_blocklist = set()
# 로그아웃 API
class UserLogoutResource(Resource):

    @jwt_required()
    def delete(self):
        
        jti = get_jwt()['jti']
        print(jti)
        jwt_blocklist.add(jti)

        return{
            'result':'success'
        }