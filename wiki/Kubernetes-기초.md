---
title: Kubernetes 기초 — 실전에서 배운 개념 사전
category: 개념/지식
tags: [kubernetes, k8s, docker, ci-cd, 인프라, 학습노트]
source: 2026-11-03~04 사내 클러스터 조회·배포 실습 세션(직접 실행 결과 해석), [[사내-k8s-배포-CI-CD-구축]]
created: 2026-11-04
updated: 2026-11-04
---

> [!tip] 핵심 takeaway
> 🧠 쿠버네티스는 **"이 상태로 유지해줘"라고 선언하면 알아서 맞춰 주는 관리자**다. pm2·systemd 가 프로세스를 지키듯, k8s 는 컨테이너 묶음(Pod)을 지킨다.
> 🧠 처음엔 **Namespace · Deployment · Service · Ingress · Secret** 다섯 개만 알면 서비스 하나를 올릴 수 있다. 나머지는 필요할 때 붙는다.
> 📄 모든 항목은 [[사내-k8s-배포-CI-CD-구축]] 실습에서 직접 쓰고 결과를 확인한 것.

---

## 1. 요청이 Pod 에 닿는 길

```
브라우저 → (가상 IP) → Ingress 컨트롤러(nginx) → Ingress 규칙(Host·경로) → Service → Pod(컨테이너)
```
- **가상 IP(VIP)** — 여러 서버가 하나의 IP 를 번갈아 맡는 것(keepalived). 서버 한 대가 죽어도 IP 는 살아 있게.
- **Ingress** — "어느 도메인/경로를 어느 Service 로" 보내는 규칙. **Host 헤더로 구분**하므로 같은 IP 에 여러 서비스를 올릴 수 있다.
  - ⚠ Host 를 비운 규칙(`*`)은 "나머지 전부"를 받는다. 남이 그런 규칙을 쓰고 있으면, 내가 같은 도메인을 쓰는 순간 그 트래픽을 가로챈다 → **도메인을 분리**.
- **Service** — Pod 들 앞의 고정 주소. Pod 는 재시작마다 IP 가 바뀌어서 직접 부르지 않는다.
- 사내 전용 도메인은 공인 DNS 에 없으니 각자 PC 의 **hosts 파일**에 `IP 도메인` 한 줄을 추가.

## 2. 리소스 사전

| 리소스 | 한 줄 | 실습에서 |
|---|---|---|
| **Namespace** | 리소스를 담는 칸. 칸째 지우면 안의 것 전부 삭제 | 내 칸 하나 → 정리는 `kubectl delete namespace <칸>` |
| **Deployment** | "이 이미지로 Pod N개 유지". 죽으면 새로 띄움, 교체는 롤링 업데이트 | replicas 1, 자원 상한, 헬스체크 |
| **StatefulSet** | 이름·저장소가 고정된 Pod(DB 류) | DB·캐시·검색엔진이 이 방식 |
| **Service** | Pod 앞 고정 주소 | ClusterIP 8080 |
| **Ingress** | 도메인/경로 → Service | 별도 도메인 1개 |
| **Secret** | 비밀값. ⚠ **암호화가 아니라 base64 인코딩**일 뿐 → 권한으로 보호 | 앱 키, 레지스트리 pull 인증 |
| **ConfigMap** | 비밀 아닌 설정 | — |
| **CronJob** | 정해진 주기로 Job(일회성 Pod) 실행 | 2분마다 새 이미지 확인 |
| **ServiceAccount + Role + RoleBinding** | 자동화용 계정과 그 권한. Role 은 **네임스페이스 한정**, ClusterRole 은 클러스터 전체 | Deployment 하나만 get/patch |

## 3. 꼭 알아야 할 동작

- **선언형(`apply`) vs 명령형(`create`)** — `apply` 는 파일과 현재 상태를 비교해 **다른 부분만** 바꾼다(결과에 `unchanged`/`configured`). `create` 로 만든 것에 `apply` 하면 "last-applied 없음" 경고가 한 번 나온다(정상).
- **환경변수는 Pod 시작 때만 읽힌다** — Secret 을 바꿔도 반영 안 됨 → `kubectl rollout restart`.
- **헬스체크(probe)** — readiness 실패 = 트래픽에서 뺌, liveness 실패 = 재시작.
- **종료 코드 137** = SIGKILL(강제 종료: 메모리 초과·liveness 실패 등). 원인은 로그로 따로 확인해야 한다.
- **이미지 태그 vs 지문(digest)** — 태그(`:deploy`)는 움직이는 이름표, digest(`sha256:…`)는 내용 그 자체. "새 이미지인가?"는 digest 로 비교.
- **`imagePullPolicy: Always`** — 재시작할 때마다 레지스트리에서 다시 받아 옴(이동 태그와 짝).
- **롤백** — `kubectl rollout undo` 는 직전 Deployment 설정으로. ⚠ 이동 태그 하나만 쓰면 설정이 같아 의미 없음 → Git 으로 되돌림.

## 4. 자주 쓴 명령

```bash
kubectl get pods,svc,ingress -n <칸>            # 상태
kubectl get pods -n <칸> -w                      # 계속 지켜보기 (-w 는 한 종류만)
kubectl logs -n <칸> deploy/<이름> -f            # 실시간 로그
kubectl logs -n <칸> job/<이름>                  # job 로그 (job.batch/ 접두 붙이면 오류)
kubectl describe pod -n <칸> -l app=<이름>       # 이벤트·재시작 이유
kubectl top node / pod                           # CPU·메모리 (metrics-server 필요)
kubectl rollout restart|status|undo deploy/<이름> -n <칸>
kubectl auth can-i <동사> <리소스> -n <칸> --as=system:serviceaccount:<칸>:<계정>   # 권한 미리 확인
kubectl create secret generic <이름> -n <칸> --from-env-file=/dev/stdin           # 붙여넣기 → Ctrl+D (파일·히스토리 미잔존)
kubectl create secret ... --dry-run=client -o yaml | kubectl apply -f -          # Secret 갱신
```

## 5. 컨테이너 이미지와 CI/CD

- **레지스트리 경로 = Git 프로젝트 경로** (GitLab). 짐작하면 `insufficient_scope` 로 거부된다.
- **토큰 권한은 용도별 최소로** — 올리기 `write_registry`, 클러스터가 받기 `read_registry`.
- **아키텍처** — 맥(M 시리즈)·클라우드 ARM 은 arm64, 운영 서버는 보통 amd64.
  - 간단: `docker buildx build --platform linux/amd64`
  - 에뮬레이션 없는 서버에서: **두 단계 Dockerfile** — `FROM --platform=$BUILDPLATFORM ... RUN npm ci` → 최종 `FROM node` 엔 `COPY --from` 만. (순수 JS 의존성일 때)
- **CI = 빌드·테스트 자동화, CD = 배포 자동화.**
  - push 방식: CI 가 클러스터에 직접 배포(kubectl) — CI 가 클러스터에 닿아야 함.
  - pull 방식: 클러스터 안의 무언가가 레지스트리/Git 을 보고 가져감 — GitOps(ArgoCD·Flux), 이미지 업데이터, 또는 직접 만든 CronJob.
- **GitLab CI 팁** — `.gitlab-ci.yml` 셸 명령에 `: ` `#` `{` 가 있으면 `- |` 블록으로. `rules: changes:` 로 특정 폴더 변경 때만 실행. `CI_REGISTRY_PASSWORD` 는 작업이 끝나면 만료되는 토큰.

## 6. pm2 와의 대응

| pm2 | k8s |
|---|---|
| `pm2 ls` | `kubectl get pods` |
| `pm2 logs` | `kubectl logs -f` |
| `pm2 monit` | `kubectl top pod` |
| `pm2 describe` | `kubectl describe pod` |
| 프로세스 자동 재시작 | Deployment 가 Pod 재생성 |

- ⚠ `pm2 ls` 는 데몬이 없으면 **새로 띄운다** — 공용 서버에서 "조회"로 치면 안 된다. 먼저 `ps aux | grep [p]m2`.

## 관련 문서
- [[사내-k8s-배포-CI-CD-구축]] · [[websdk-test]] · [[공통-기술스택]] · [[내-프로필]]
