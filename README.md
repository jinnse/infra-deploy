# ☁️ 온프레미스 기반 인프라 자동화 프로젝트

이 프로젝트는 **클라우드 비용 절감**과 **개발자 생산성 향상**을 목표로, 온프레미스 환경에 자동으로 개발/서비스 인프라를 구성하는 자동화 시스템입니다.

> Jenkins + Ansible + Docker Compose를 활용해 App, DB, Web, Monitoring 환경을 자동으로 배포합니다.

---

## 📦 프로젝트 목적

- AWS 등 클라우드 비용 절감
- 내부 인프라 자원을 활용한 하이브리드 환경 구성
- DevOps 기반 자동화 환경 구축
- 개발자는 ‘코드’에만 집중하고, 인프라는 자동화

---

## 🖥️ 인프라 구성

### 🛜 네트워크 UML
![Project - Page 1](https://github.com/user-attachments/assets/f0425267-ac7b-4d77-be94-a6df4554520d)

### 🎛️ 인프라 UML
![Project - Page 1 (2)](https://github.com/user-attachments/assets/d4e9d6f8-c88b-4323-b1be-93cbd9579514)

```
[Control Server] ── Ansible + SSH
     │
     ├── [Web Server]         : Nginx Proxy + Web1 + Web2 컨테이너
     ├── [App Server]         : Flask App1 컨테이너 + 로그
     ├── [DB Server]          : PostgreSQL Patroni(HA) + etcd + HAProxy
     ├── [Storage Server]     : GlusterFS + 앱/모니터링 로그
     └── [Monitoring Server]  : Prometheus + Grafana + Alertmanager
```

---

## 📁 디렉토리 구조

```bash
infra-deploy/
├── ansible/
│   ├── inventory.yml             # 서버 목록
│   ├── playbooks/                # 배포 플레이북
│   ├── roles/                    # 공통 역할 (common, docker)
│   └── secrets/                  # 보안 설정 (vault 등)
├── infra-components/
│   ├── app/                      # Flask App 소스
│   ├── db/                       # Patroni + HA 구성
│   ├── web/                      # Web1, Web2, Proxy + HTML
│   ├── storage/                  # GlusterFS 설정
│   └── monitoring/              # Prometheus, Grafana 설정
├── jenkins/
│   └── Jenkinsfile               # CI/CD 자동화 정의
└── team1.drawio                 # 인프라 구조 다이어그램
```

---

## 🚀 자동화 방식

### 1. Jenkins Pipeline 구성
- Git Clone → Rsync → Ansible Playbook 실행
- 서버별 SSH 키 기반 인증

### 2. Ansible Playbooks
- `deploy_control.yml`: SSH 구성 및 key 배포
- `deploy_db.yml`: DB 서버에 Patroni+etcd+HAProxy 자동 구성
- `deploy_app.yml`: Flask App 자동 배포
- `deploy_web.yml`: Proxy + Web1/2 Nginx 컨테이너 자동 구성
- `deploy_storage.yml`: GlusterFS Mount 및 마운트 경로 생성
- `deploy_monitoring.yml`: Prometheus + Grafana 자동 배포

---

## 🌐 간단한 웹 페이지 프로세스
![Project - Page 1 (1)](https://github.com/user-attachments/assets/21760762-759f-44de-a747-06571e8e2a52)

1. 사용자가 `http://web-server-ip` 접속
2. `proxy` 컨테이너가 `web1` 또는 `web2`로 분산 처리
3. `index.html`은 `/api/weather` 호출
4. `proxy → app-server → PostgreSQL`로 연결
5. 날씨 정보 조회 및 응답 반환

---

## 🗃️ 스토리지, 백업 프로세스

![Image](https://github.com/user-attachments/assets/840fbb5a-07b8-4227-b0db-b9cae2c73b29)

1. 스토리지 서버 2대를 GlusterFS로 클러스터링하여 고가용성(HA) 스토리지 환경을 구성함.
2. 클러스터링된 스토리지 서버는 /shared 디렉토리를 공유하며, 웹, 앱, DB, 모니터링 서버의 로그 디렉토리와 마운트하여 사용함.
3. 각 서버에서 발생하는 로그 파일은 해당 공유 디렉토리에 저장됨.
4. 저장된 로그는 cron을 이용해 매일 자정에 tar로 압축한 후, S3 버킷으로 자동 백업.
---

## 📈 모니터링 프로세스
<img width="591" height="292" alt="제목 없는 다이어그램 drawio" src="https://github.com/user-attachments/assets/602b1890-a960-4050-b001-b7c6c20e1dc7" />

1. **메트릭 수집**: 각 서버(Web, App, DB, Storage)에 Node Exporter를 설치하여 시스템 메트릭(CPU, Memory, Disk, Network) 데이터를 수집함.

2. **데이터 저장**: Prometheus가 각 Node Exporter로부터 메트릭 데이터를 주기적으로 스크래핑하여 시계열 데이터베이스에 저장함.

3. **시각화**: Grafana가 Prometheus를 데이터소스로 연결하여 실시간 대시보드를 통해 인프라 상태를 모니터링함.
   - 시스템 리소스 사용률 그래프
   - 서버별 상태 패널
   - 네트워크 트래픽 현황

4. **알림 처리**: Alertmanager가 설정된 임계값 초과 시 자동으로 알림을 전송함.
   - CPU 사용률 80% 이상
   - Memory 사용률 85% 이상
   - Disk 사용률 90% 이상
   - 서비스 다운 상태

5. **알림 전송**: 임계값 초과 또는 장애 발생 시 이메일을 통해 관리자에게 즉시 알림을 전송하여 신속한 대응이 가능하도록 함.

---

## 🧪 주요 명령어

```bash
# 컨트롤 서버에서 ansible로 배포
ansible-playbook -i inventory.yml playbooks/deploy_app.yml --ask-become-pass

# 특정 서버에서 수동 확인
curl http://localhost
docker ps
docker logs flask-app1
```

---

## ✅ 기대 효과

- 개발자는 “코드”에만 집중할 수 있는 환경 제공
- 클라우드 대비 유지비용 최소화
- 서비스 초기 단계에서 안정적인 내부 인프라 확보
- 장애 대응력 향상 (HA 구성, 모니터링 포함)

---

## ✍️ 기술스택

- Python Flask
- PostgreSQL + Patroni + etcd
- Docker Compose
- Nginx Proxy
- GlusterFS (로그 저장용)
- Jenkins Pipeline
- Prometheus / Grafana

---

## 🤝 팀원

- 인프라 자동화 / DevOps: 모든 팀원
- 웹,앱,DB 설계 및 개발: 이재기
- 모니터링 설계 및 개발: 송태현
- 스토리지, 백업 설계 및 개발: 박세진

---
