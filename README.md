# 첫 번째 트렉 프로젝트

- [첫 번째 트렉 프로젝트](#첫-번째-트렉-프로젝트)
- [plan](#plan)
  - [github](#github)
  - [CI/CD](#cicd)
  - [INFRA](#infra)
  - [BACKEND](#backend)
  - [FRONTEND](#frontend)
- [TODO](#todo)
  - [DRF](#drf)
  - [docker](#docker)
  - [terraform](#terraform)
  - [kubernetes](#kubernetes)
  - [github actions](#github-actions)
  - [frontend](#frontend-1)
- [Quick Start](#quick-start)
  - [Local](#local)
  - [Prod](#prod)

# plan

## github

- 피어리뷰를 위해 main 브랜치는 제출 전 PR
- main 대신 develop 브랜치에 변경사항 적용
- main, develop 브랜치 pull 비활성화 (적용 불가능)
- 모든 기능은 issue로 생성하고 PR로 마무리
- github projects와 issues를 활용하여 프로젝트 관리

## CI/CD

- CI는 github actions 사용
- CD는 argocd 사용
- NCP CR, docker image로 배포
- repo에 TOKEN 권한이 없어 helm을 따로 관리
- github actions에서 helm chart를 수정해 argocd로 배포

## INFRA

- terraform으로 k8s 환경 구성
- terraform state는 s3 backend와 NCP Object Storage 사용
- actions에서 새로운 이미지를 업로드 하도록 구성

## BACKEND

- 테스트는 docker compose 활용
- 환경변수로 allowed hosts, secret key, db, env 정보 입력
- gunicorn 사용
- ERD
  ![ERD image](images/erd.png)
- API  
  ```yaml
  User:
    - path: /users
      method: GET
      description: 전체 유저 조회
      response: 유저 리스트
    
    - path: /user/post
      method: GET
      description: 유저가 작성한 전체 개시글 조회
      response: 개시글 리스트

  Post:
    - path: /post
      method: GET
      description: 전체 개시글 조회
      response: 개시글 리스트

    - path: /post
      method: POST
      description: 개시글 작성
      response: 생성된 개시글 정보

    - path: /post/<int:post_id>
      method: PUT
      description: 개시글 수정
      response: 수정된 개시글 정보
    
    - path: /post/<int:post_id>
      method: DELETE
      description: 개시글 삭제
      response: 삭제된 개시글 정보

  Follow:
    - path: /user/following
      method: GET
      description: 팔로우한 유저 조회
      response: 유저 리스트

    - path: /user/follower
      method: GET
      description: 나를 팔로우한 유저 조회
      response: 유저 리스트
    
    - path: /user/follow/
      method: POST
      description: 팔로우 토글
      response: 결과
  ```
- global DNS로 도메인 연결 (api.limeskin.kr)
- allowed hosts를 전체 허용으로 변경
- cros origin 허용
- CSRF 토큰 비활성화

## FRONTEND

- React 사용
- tailwindcss로 디자인
- Object Storage에 업로드 해 정적 웹으로 배포
- NCP global DNS로 도메인 연결

# TODO

대략적인 계획입니다.  
자세한 내용은 issue를 참고해주세요.

## DRF

- [x] 프로젝트 생성
- [x] 앱 생성
- [x] 환경 분리
- [x] 설정 변경
- [x] start script 작성
- [x] entrypoint script 작성
- [x] ERD 구성
- [x] 모델 작성
- [x] 테스트 작성
- [x] VIEWSET 생성
- [x] boto3 NCP 연결
- [x] docs 페이지 생성
- [x] API 개선
- [ ] post 비활성화 기능 추가

## docker

- [x] dockerfile 작성
- [x] docker compose 구성

## terraform

- [x] server 생성 전 LB url 생성 테스트
- [x] network 모듈 생성
- [x] server 모듈 생성
- [x] LB 모듈 생성
- [ ] github secret 모듈 생성 (실패)
- [x] prod 환경 생성

## kubernetes

- [x] helm chart 작성
- [x] k8s 작성
- [ ] 모니터링 시스템구축

## github actions

- [x] docker build
- [x] DRF test
- [x] docker push
- [x] server update
- [x] 실패시 discord 알림
- [ ] 새롭게 CI/CD 작성

## frontend

- [x] react 프로젝트 생성
- [x] tailwindcss 적용
- [x] Login 페이지
- [x] Signup 페이지
- [x] MyPost 페이지
- [x] Post 페이지
- [x] UserList 페이지
- [ ] post 비활성화 기능 추가

# Quick Start

## Local

.env 파일을 생성하고 다음 내용을 작성해 줍니다.
```env
# DB
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432

# DRF
DB_HOST=db
DJANGO_SECRET_KEY=enter_your_django_secret
RUN_MODE=local
DJANGO_ALLOWED_HOST=localhost

# NCP
NCP_ACCESS_KEY=enter_your_ncp_access_key
NCP_SECRET_KEY=enter_your_ncp_secret_key
```

compose를 싱행해주고 테스트를 실행합니다.

```bash
docker compose up -d --build
# for test
docker compose exec follow-app python manage.py test
```

추가로 더미데이터를 생성할 수 있습니다.

```bash
docker compose exec -it follow-app python manage.py make_dummy
```

더미 유저는 id, pw 모두 user0~user4로 생성됩니다.

테스트는 /api/docs/ 또는 VScode의 Thunder Client를 사용해 테스트할 수 있습니다.

## Prod

infra/prod 디렉토리에 terraform.tfvars 파일을 생성하고 다음 내용을 작성해 줍니다.

생성된 인스턴스의 기본 유저는 terry 입니다.

```bash
NCP_ACCESS_KEY    = "enter_your_ncp_access_key"
NCP_SECRET_KEY    = "enter_your_ncp_secret_key"
password          = "enter_your_server_password"
postgres_db       = "enter_your_db_name"
postgres_user     = "enter_your_db_user"
postgres_password = "enter_your_db_password"
ncr_registry      = "enter_your_ncr_registry_url"
django_secret_key = "enter_your_django_secret"
```

statefile 관리를 위해 infra/prod/ 디렉토리에 .credentials 파일도 생성하고 다음 내용을 작성해 줍니다.

```ini
[default]
aws_access_key_id = enter_your_ncp_access_key
aws_secret_access_key = enter_your_ncp_secret_key
```

terraform init후 인프라를 생성해 줍니다.

```bash
terraform init
terraform apply --auto-approve
```

출력으로 be 인스턴스 ip와 LB url을 얻을 수 있습니다.

```bash
be_public_ip = "223.130.163.73"
domian = "prod-lb-19480009-8e40422f6c1b.kr.lb.naverncp.com"
```

PS
테라폼이로 prod 환경을 구성할 때 LB주소를 변수로 넘겨줘서 ALLOWED_HOSTS에 추가하는 것은 의외로 잘 되었는데 NCP 크래딧이 조금 아슬아슬 하여 서버를 열어두진 않았습니다.