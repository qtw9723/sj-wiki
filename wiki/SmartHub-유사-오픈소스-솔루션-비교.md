---
title: SmartHub와 비슷한 오픈소스·솔루션 비교
category: 프로젝트
tags: [프로젝트, 포트폴리오, smarthub, 포지셔닝, 오픈소스, 비교]
sources: ["저장소 qtw9723/smarthub README.md (3층 구조·두 에디션)", "Claude 일반 지식(2026-11-17 대화, 웹 최신 확인 전)"]
created: 2026-11-17
updated: 2026-11-17
---

> [!tip] 핵심 takeaway (포트폴리오 관점)
> 🧠 SmartHub는 **"Backstage식 플러그인 허브 + Windmill식 팀 스코프 자동화"를 가볍게 만든 것**으로 설명하면 한 줄로 통한다. 차별점은 (1) 허브×모듈 on/off 매트릭스, (2) 코드 하나로 외부·사내 두 에디션, (3) 상용 기능(Checkly·Grafana Enterprise Reporting)을 사내 맞춤으로 직접 구현한 것.
> ⚠ 아래 비교는 일반 지식 기반이다. 스타 수·라이선스·최신 기능은 웹으로 다시 확인한 뒤 면접·문서에 쓸 것.

## 비교 기준 — SmartHub의 핵심 구조 📄
[[delivery-smarthub|SmartHub]] README 기준:
- **모듈(기능)**: 계약(API 라우터 + HubPanel + `hub_id` 테이블 + overview)을 구현해 레지스트리에 등록
- **허브(팀)**: `hub_features(hub_id, feature_key)` 매트릭스로 허브별 모듈 on/off
- **백오피스**: 레지스트리를 돌며 허브 × 모듈을 한눈에 관망
- 같은 코드가 외부(Vercel·Supabase)·사내(k8s·자체 Postgres) **두 에디션**으로 돈다

## 구조가 가장 비슷한 것 🧠

| 이름 | 비슷한 점 | 다른 점 |
|---|---|---|
| **Backstage** (Spotify, CNCF) | 플러그인 레지스트리, 팀 소유권, 통합 포털. "사내 업무 도구를 한 곳에 모은다"는 철학이 가장 가깝다 | 개발자 포털(소프트웨어 카탈로그) 중심이고 무겁다. 허브별 모듈 on/off 매트릭스는 기본으로 없다 |
| **Windmill** | 스크립트를 UI·스케줄·웹훅으로 바로 만들고 워크스페이스(=팀) 단위로 나눈다. k8s 셀프호스팅 | 모듈을 코드 계약으로 만드는 대신 스크립트·플로우를 화면에서 조립한다 |
| **Odoo** | 모듈(앱) 설치·비활성화 + 멀티 컴퍼니 스코프가 같은 패턴 | ERP 영역이라 쓰임새가 다르다 |

## 일부 기능이 겹치는 것 🧠

| 영역 | 솔루션 | SmartHub에서 겹치는 부분 |
|---|---|---|
| 내부 툴 빌더 | Appsmith·ToolJet·Budibase(오픈소스), Retool(상용) | 팀별 사내 도구를 빨리 만드는 것 → 무상태 툴 모듈(doc-to-esd·doc-to-api) |
| 워크플로 자동화 | n8n·Activepieces | 메일 발송 잡·정시 작업 |
| 합성 모니터링 | Checkly(Playwright 기반, 상용), Uptime Kuma(오픈소스, 단순 핑) | chatbot-monitoring 모듈([[Playwright]] 정기 점검) |
| 대시보드 리포트 | Grafana Enterprise Reporting(OSS판엔 없음) | grafana-reports 모듈 → OSS에 없어서 직접 만든 근거 |
| 메일 발송 | listmonk | [[mailer]] 모듈 |
| 링크 포털 | Homarr·Heimdall | 허브 링크 화면만 비슷(모듈·데이터 없음) |

## 포지셔닝 정리 🧠
1. **허브×모듈 매트릭스**: 팀마다 기능을 켜고 끄는 것이 데이터(`hub_features`)로 관리된다. Backstage는 플러그인을 배포 단위로 붙이지 팀별 토글을 기본 제공하지 않는다.
2. **두 에디션**: 차이를 설정(`SMARTHUB_EDITION`)·저장소 계층·에디션 드라이버에 가둬 같은 API로 외부·사내를 함께 운영한다([[사내-k8s-배포-CI-CD-구축]]).
3. **상용 기능의 사내 맞춤 구현**: Checkly·Grafana Enterprise Reporting에 해당하는 기능을 실사용 팀 요구에 맞춰 모듈로 만들었다.
4. **모듈 보안 레벨**: 모듈 레벨 × 허브 보호 수준 정책([[SmartHub-모듈-보안-레벨-설계]])은 위 솔루션들에 없는 운영 관점 장치다.

## 후속 후보
- 웹으로 최신 상태(스타 수·라이선스·셀프호스팅 조건) 확인 후 표 보강
- 면접용 한 장 요약(위 포지셔닝 4항목)으로 [[프로젝트-포트폴리오]]에 반영 검토

## 관련 문서
- [[delivery-smarthub]] — 비교 대상인 SmartHub 본 페이지
- [[SmartHub-모듈-보안-레벨-설계]] — 같은 방식(오픈소스 사례 비교)으로 보안 레벨을 설계한 기록
- [[에이전트-자동화-도구]] — n8n 등 자동화 도구 정리
- [[내-프로필]]
