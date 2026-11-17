---
title: SmartHub와 비슷한 오픈소스·솔루션 비교
category: 프로젝트
tags: [프로젝트, 포트폴리오, smarthub, 포지셔닝, 오픈소스, 비교]
sources: ["저장소 qtw9723/smarthub README.md (3층 구조·두 에디션)", "Claude 일반 지식(2026-11-17 대화)", "웹 확인 2026-11-17: Grafana 커뮤니티 공식 답변·Checkly 비교 자료·Windmill 셀프호스트 문서·Odoo 포럼(아래 확인 출처)"]
created: 2026-11-17
updated: 2026-11-17
---

> [!tip] 핵심 takeaway (포트폴리오 관점)
> 🧠 SmartHub는 **"Backstage식 플러그인 허브 + Windmill식 팀 스코프 자동화"를 가볍게 만든 것**으로 설명하면 한 줄로 통한다. 차별점은 (1) 허브×모듈 on/off 매트릭스, (2) 코드 하나로 외부·사내 두 에디션, (3) 상용 기능(Checkly·Grafana Enterprise Reporting)을 사내 맞춤으로 직접 구현한 것.
> 📄 2026-11-17 웹 확인: Grafana 리포트 Enterprise 전용 · Checkly Playwright 기반 SaaS · Windmill 셀프호스트·AGPL · Odoo 모듈은 DB 단위 — 면접에 써도 되는 항목은 ✅ 표시. Backstage·내부 툴 빌더 등 표시 없는 항목은 아직 일반 지식 수준이다.

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
| **Windmill** ✅ | 스크립트를 UI·스케줄·웹훅으로 바로 만들고 워크스페이스·폴더·그룹 단위로 나누고 권한을 건다. Docker Compose·Helm(k8s) 셀프호스팅 | 모듈을 코드 계약으로 만드는 대신 스크립트·플로우를 화면에서 조립한다. 무료 Community Edition은 AGPL, SSO·감사 로그는 유료 Enterprise |
| **Odoo** ✅ | 기능을 모듈(앱) 단위로 설치·제거하는 구조가 같다 | ⚠ 정정(2026-11-17): 모듈 설치는 **데이터베이스 단위**라, 한 DB 안의 회사(멀티 컴퍼니)별로 앱을 켜고 끄는 기능은 기본 제공되지 않는다(포럼에서 회사별 앱 제한 방법을 묻는 질문이 나오는 이유). → SmartHub의 허브별 모듈 토글과 오히려 **대비되는 점**. 쓰임새도 ERP라 다르다 |

## 일부 기능이 겹치는 것 🧠

| 영역 | 솔루션 | SmartHub에서 겹치는 부분 |
|---|---|---|
| 내부 툴 빌더 | Appsmith·ToolJet·Budibase(오픈소스), Retool(상용) | 팀별 사내 도구를 빨리 만드는 것 → 무상태 툴 모듈(doc-to-esd·doc-to-api) |
| 워크플로 자동화 | n8n·Activepieces | 메일 발송 잡·정시 작업 |
| 합성 모니터링 | Checkly ✅(Playwright 테스트 파일로 체크 작성, SaaS 전용·셀프호스팅 없음), Uptime Kuma(오픈소스, 단순 핑) | chatbot-monitoring 모듈([[Playwright]] 정기 점검) |
| 대시보드 리포트 | Grafana Enterprise Reporting ✅(PDF 내보내기·예약 리포트는 Enterprise·Cloud 전용, OSS는 JSON 내보내기만) | grafana-reports 모듈 → OSS에 없어서 직접 만든 근거. ⚠ 비슷한 커뮤니티 PDF 플러그인은 있다 → "왜 플러그인 대신 직접 만들었나"에 답을 준비할 것 |
| 메일 발송 | listmonk | [[mailer]] 모듈 |
| 링크 포털 | Homarr·Heimdall | 허브 링크 화면만 비슷(모듈·데이터 없음) |

## 포지셔닝 정리 🧠
1. **허브×모듈 매트릭스**: 팀마다 기능을 켜고 끄는 것이 데이터(`hub_features`)로 관리된다. 🧠 Backstage는 플러그인을 배포 단위로 붙여 팀별 토글이 기본 제공되지 않는 것으로 알고 있다(출처 미확인 — 면접에선 "기본 제공되지 않는다" 수준으로). 📄 Odoo도 모듈 설치가 DB 단위라 회사별 토글이 기본이 아니다.
2. **두 에디션**: 차이를 설정(`SMARTHUB_EDITION`)·저장소 계층·에디션 드라이버에 가둬 같은 API로 외부·사내를 함께 운영한다([[사내-k8s-배포-CI-CD-구축]]).
3. **상용 기능의 사내 맞춤 구현**: Checkly·Grafana Enterprise Reporting에 해당하는 기능을 실사용 팀 요구에 맞춰 모듈로 만들었다.
4. **모듈 보안 레벨**: 모듈의 위험도 × 허브의 공개 여부를 조합해 위험 모듈을 차단하는 정책([[SmartHub-모듈-보안-레벨-설계]]). ⚠ 정정(2026-11-17): "다른 솔루션에 없다"고 단정하지 않는다 — Windmill은 그룹·경로 단위 권한, Backstage는 권한 프레임워크가 있다. 차별점은 권한 기능 자체가 아니라 **"기능 위험도와 노출 범위를 조합한 차단 규칙"**이라는 범위로 말한다.

## 후속 후보
- ✅ 2026-11-17 Grafana·Checkly·Windmill·Odoo 웹 확인 반영. 남은 확인: Backstage 팀별 플러그인 토글 여부, 내부 툴 빌더·n8n 라이선스
- 면접용 한 장 요약(위 포지셔닝 4항목)으로 [[프로젝트-포트폴리오]]에 반영 검토

## 확인 출처 (2026-11-17)
- Grafana: [커뮤니티 공식 답변 — PDF·Reporting은 Enterprise/Cloud 전용](https://community.grafana.com/t/export-dashboard-as-pdf-or-excel-format/114327) · [비슷한 커뮤니티 플러그인](https://community.grafana.com/t/grafana-dashboard-reporter-plugin/117281)
- Checkly: [Playwright 기반·셀프호스팅 없음 비교](https://europeanpurpose.com/tool/checkly) · [OneUptime 비교](https://oneuptime.com/compare/checkly)
- Windmill: [셀프호스트(Docker·Helm), CE=AGPL](https://automationatlas.io/answers/how-to-self-host-windmill-2026/) · [워크스페이스·그룹 권한](https://www.everydev.ai/tools/windmill)
- Odoo: [모듈은 DB 단위로 설치](https://www.odoo.com/forum/help-1/how-to-load-a-specific-module-into-a-specific-database-194149) · [회사별 앱 제한 질문](https://www.odoo.com/hi_IN/forum/help-1/filter-apps-list-per-company-in-multi-company-odoo-196667)

## 면접 대비 메모
- 🧠 [[면접-대비]] 페이지를 만들 때 이 페이지의 포지셔닝 4항목과 예상 반박(왜 Backstage·Windmill을 안 썼나, 왜 Grafana 플러그인 대신 직접 만들었나, 보안 레벨이 RBAC과 뭐가 다른가)을 함께 뽑는다(2026-11-17 사용자 요청).

## 관련 문서
- [[delivery-smarthub]] — 비교 대상인 SmartHub 본 페이지
- [[SmartHub-모듈-보안-레벨-설계]] — 같은 방식(오픈소스 사례 비교)으로 보안 레벨을 설계한 기록
- [[에이전트-자동화-도구]] — n8n 등 자동화 도구 정리
- [[내-프로필]]
