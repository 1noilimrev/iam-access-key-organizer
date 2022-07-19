# iam-acceess-key-organizer

## 오래된 AWS IAM Access Key 검출하는 HTTP API 입니다.

## 실행 방법

### AWS 환경 변수 설정

AWS CLI 가 설치되어 있다면 아래 명령어를 사용하여 환경 변수를 넣어줍니다.

```
aws configure
```

혹은 아래처럼 직접 export 합니다.

```
export AWS_ACCESS_KEY_ID=<your access key id>
export AWS_SECRET_ACCESS_KEY=<your secret access key>
export AWS_DEFAULT_REGION=<your aws region>
```
---
### FastAPI를 이용하여 Local에서 개발서버 실행하기

Python 3.10 이상의 버젼이 필요합니다.


```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
위의 명령어에서는 8000번 port를 사용합니다.

---
### 로컬 머신에서 k8s를 사용하여 서버 실행하기

1. iam-access-key-organizer/k8s/secret.yml 파일의 해당하는 환경변수를 설정합니다.

```
...
data:
  AWS_ACCESS_KEY_ID: <AWS_ACCESS_KEY_ID>
  AWS_SECRET_ACCESS_KEY: <AWS_SECRET_ACCESS_KEY>
  AWS_DEFAULT_REGION: <AWS_DEFAULT_REGION>
```

2. 환경변수 설정이 끝나면 shell에서 kubectl를 사용하여 아래와 같이 서버를 실행합니다.

```
# iam-access-key-organizer/k8s 디렉토리로 들어가기
cd k8s

kubectl apply -f .
```
---
### API 사용하기

k8s가 port forwading한 port를 사용하여 아래의 같은 endpoint(`/find`)와 parameter(`?age_hours`)를 사용하여 api에 정보를 요청합니다.

`age_hours` parameter에는 Access Key Pair가 생성 후 N시간을 초과하는지 확인하는데 사용되는 시간을 정수(integer)로 입력합니다.

예시:
`http://localhost::<PORT>/find?age_hours=<int>`

### IAM Access Key Organizer API Documentation

아래 주소를 접속하시면 Swagger로 작성된 API 문서를 볼 수 있습니다.

`http://localhost:<PORT>/docs/`

---
### 테스트 코드 실행하기

```
# iam-access-key-organizer/app 디렉토리로 들어가기
cd app

python -m unittest tests
```
