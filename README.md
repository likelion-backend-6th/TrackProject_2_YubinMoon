# 첫 번째 트렉 프로젝트

- [첫 번째 트렉 프로젝트](#첫-번째-트렉-프로젝트)
- [plan](#plan)
  - [github](#github)
  - [CI/CD](#cicd)
  - [INFRA](#infra)
  - [BACKEND](#backend)
- [TODO](#todo)
  - [DRF](#drf)
  - [docker](#docker)
  - [terraform](#terraform)
  - [github actions](#github-actions)
- [Quick Start](#quick-start)
  - [Local](#local)
  - [staged](#staged)
  - [Prod](#prod)

# plan

## github

- 피어리뷰를 위해 main 브랜치는 제출 전 PR
- main 대신 develop 브랜치에 변경사항 적용
- main, develop 브랜치 pull 비활성화 (적용 불가능)
- 모든 기능은 issue로 생성하고 PR로 마무리
- github projects와 issues를 활용하여 프로젝트 관리

## CI/CD

- CI/CD는 github actions 사용
- NCP CR, docker로 배포
- main, develop 브랜치를 prod로 나머지를 staged로 배포
- 배포 인스턴스에 ssh로 접속하여 배포
- allowed hosts만 환경변수로 입력

## INFRA

- terraform으로 staged, prod 환경 따로 구성
- terraform state는 s3 backend와 NCP Object Storage 사용
- 생성된 인스턴스 ip, LB url등은 github actions secret에 업데이트
- actions에서 새로운 이미지로 업데이트 가능하도록 구성

## BACKEND

- 테스트는 docker compose 활용
- 환경변수로 allowed hosts, secret key, db, env 정보 입력
- gunicorn 사용

# TODO

대략적인 계획입니다.  
자세한 내용은 issue를 참고해주세요.

## DRF

- [ ] 프로젝트 생성
- [ ] 환경 분리
- [ ] 설정 변경
- [ ] start script 작성

## docker

- [ ] dockerfile 작성
- [ ] docker compose 구성

## terraform

- [ ] server 생성 전 LB url 생성 테스트
- [ ] network 모듈 생성
- [ ] server 모듈 생성
- [ ] LB 모듈 생성
- [ ] github secret 모듈 생성
- [ ] staged 환경 생성
- [ ] prod 환경 생성

## github actions

- [ ] staged, prod 분리
- [ ] docker build
- [ ] DRF test
- [ ] docker push
- [ ] server update
- [ ] 실패시 discord 알림

# Quick Start

## Local

## staged

## Prod