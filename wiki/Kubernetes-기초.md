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
> 🧠 **`imagePullPolicy: Always` 는 "매번 다운로드"가 아니라 "매번 확인"** — 실제로 받는 건 노드 캐시에 없는 레이어뿐(§3-2).
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

## 3-1. Pod 는 어느 노드에 뜨나 (스케줄링)

- **Pod 가 만들어질 때마다** 스케줄러가 노드를 고르고, 한 번 정해지면 **그 Pod 가 사라질 때까지 옮겨 가지 않는다.** 노드를 바꾸는 건 "이동"이 아니라 "새 Pod 생성".
- 고르는 법 2단계
  1. **거르기** — `nodeSelector`(예: `run=app` 라벨 노드만), 요청 자원(`requests`)이 들어갈 자리 없는 노드 제외.
  2. **점수** — 덜 찬·균형 맞는 노드 우선.
  - ⚠ "비어 있다"의 기준은 **실제 사용량이 아니라 예약량(requests)** 🧠.
- 실습 예 📄: 앱 Pod 는 배포·재시작 때만 자리를 정하고, CronJob Pod 는 **회차마다 새로** 정한다 → 같은 노드일 수도, 다를 수도 있다(붙이거나 떼는 설정 없음).
- 롤링 업데이트 순간엔 새 Pod 가 먼저 뜨고 옛 Pod 가 나중에 빠지므로 **잠깐 개수가 늘어난다**(앱 2 + CronJob 1 = 3).
- 확인: `kubectl get nodes -L run`(라벨), `kubectl get pods -o wide`(NODE 열), 대시보드 Pod 상세의 Node.

## 3-2. 이미지 pull 과 레이어 캐시 — "Always 면 매번 다 받나?" → 아니다

- 이미지 = **목차(manifest) + 레이어 여러 장**. 레이어마다 지문(digest)이 있고, 노드는 받아 둔 레이어를 지문으로 기억(캐시).
- pull 순서: ① 레지스트리에 태그의 목차 요청(수 KB) → ② 목차의 레이어 지문을 노드 캐시와 비교 → ③ **없는 레이어만** 다운로드.
- `imagePullPolicy: Always` = **항상 "확인"**(①을 매번), `IfNotPresent` = 같은 태그가 노드에 있으면 확인도 안 함. 다운로드 양은 둘 다 ③에서 캐시가 결정.
- 실측 예 📄 (websdk-test 이미지, 압축 전): alpine 9.1MB + Node 런타임 130MB + 기타 5.5MB(베이스) / `node_modules` 5.4MB / 코드·문서 **약 0.4MB**.

| 상황 | 실제로 받는 양 |
|---|---|
| 같은 노드, 이미지 그대로 | 목차만 — 0MB |
| 같은 노드, 코드·문서만 변경 | 바뀐 레이어만 — 약 0.4MB |
| 처음 가는 노드(캐시 없음) | 베이스까지 전부 — 약 150MB(압축 시 더 작음), 그 뒤엔 그 노드도 캐시 |

- 🧠 그래서 **Dockerfile 은 "잘 안 바뀌는 것(베이스·의존성) → 자주 바뀌는 것(코드·문서)" 순서**로 쓴다. 반대로 쓰면 코드 한 줄 수정에도 아래 레이어가 전부 새 지문이 되어 다시 받아야 한다(빌드 캐시도 같이 깨짐).
- 🧠 노드가 적을수록(워커 2대) "첫 방문 비용"은 금방 사라진다.

### 노드별 캐시, 문제는 없나 — 세 가지 확인
| 걱정 | 답 |
|---|---|
| **디스크가 계속 쌓이나** | kubelet 이 **이미지 GC** — 디스크 사용률 **85%**(기본 `imageGCHighThresholdPercent`) 넘으면 *어떤 Pod 도 안 쓰는* 이미지를 오래된 순으로 지워 **80%**(Low)까지 내림. 실행 중 이미지는 안 지움. 더 차서 남은 공간이 **10% 미만**(기본 `nodefs.available` 하드 축출)이면 그때는 **Pod 를 쫓아낸다(eviction)** — 이게 진짜 위험선 |
| **옛 이미지가 최신인 척 뜨나** | 아니다. 캐시는 태그가 아니라 **digest(내용 지문)** 로 저장·검증. `Always` 면 매번 태그→digest 를 확인하므로 stale 실행 없음. 깨진 조각은 지문 불일치로 다시 받음 |
| **노드에 남은 비공개 이미지를 남이 쓰나** | 이론상 가능 — 같은 노드의 다른 Pod 가 `IfNotPresent` 로 **인증 없이 캐시 사용** 가능(막는 설정: `AlwaysPullImages` 어드미션, 1.33 알파 `KubeletEnsureSecretPulledImages`). → 🧠 **이미지에 비밀을 넣지 않는 원칙**이면 노출돼도 코드뿐 |

- 디스크 확인(조회만): `df -h /var/lib/containerd` — 이미지가 사는 곳. 무엇이 큰지는 `du -sh /var/lib/containerd /var/log ...`.
- ⚠ **어느 노드에서 쳤는지가 중요** — 내 Pod 가 안 뜨는 노드(예: 컨트롤 플레인)의 숫자는 내 이미지와 무관하다. 실습에서 컨트롤 플레인 1대가 75% 였는데(2026-11-04 📄), 내 Pod 는 `nodeSelector` 로 워커에만 뜨므로 내 캐시는 거기 없다. 🧠 다만 그 노드는 DB·Ingress 가 있어 85%(이미지 GC)·90%(Pod 축출)선까지의 추세는 볼 가치가 있다.

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
