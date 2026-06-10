---
title: 카카오 Play MCP (도구 목록)
category: 도구/스킬
tags: [mcp, 카카오, kakao, 도구, 검색, 일정, 자동화]
source: raw/kakao-play-mcp.md
created: 2026-06-09
updated: 2026-06-09
---

> [!tip] 핵심 takeaway
> 카카오 공식 MCP 서버([[내-MCP-커넥터-환경]]에 연결됨)가 제공하는 8개 서비스의 도구 사전.
> 네([[내-프로필]]) 입장에서 당장 쓸모: **KakaotalkChat(나에게 메모)·KakaotalkCal(일정/할일)**로 자동화 결과를 카카오로 푸시 — [[schedule-reporter-kakao]]가 손으로 구현한 그 흐름을 MCP로 즉시. **NaverSearch(뉴스·데이터랩)·YouTubeData(자막)**는 [[Claude-Code-업데이트-동향]]식 AI 업계 동향 추적을 자동화하는 입력원.
> 의외의 포인트: 같은 카카오 생태계를 개인 자동화(알림·일정·검색)에 묶어 쓰면, 본업의 알림/발송 업무 감각과도 통한다.

## 서버
- 카카오 공식 MCP. 서버 ID `8b9464aa-7091-4f2f-b3ad-f7055a1e8c3a`. 정리일 2026-06-09.

## 서비스별 도구

**1. KakaoMap** — `SearchPlaceByKeywordOpen`(장소검색), `GetWalkDirections`/`GetBikeDirections`/`GetPublicTransitDirections`(도보·자전거·대중교통 길찾기).

**2. KakaotalkCal** — `GetCurrentTime`, `GetEvent`/`CreateEvent`(이벤트), `GetTask`/`CreateTask`(할일), `GetFriendsBirthdays`.

**3. KakaotalkChat** — `MemoChat`(나와의 채팅으로 메모 전송).

**4. TodoMate** — `loadTodoItems`/`loadTodoItemsByDateRange`(할일 조회), `loadGoals`(목표), `addTodoItem`/`updateTodoItem`(추가·완료), `updateTodoItemRemindAt`(알림 시간).

**5. NaverSearch**
- 검색: `search_news`·`search_blog`·`search_cafearticle`·`search_kin`·`search_image`·`search_webkr`·`search_book`·`search_encyc`·`search_local`·`search_shop`·`search_academic`.
- 데이터랩: `datalab_search`(검색어 트렌드), `datalab_shopping_*`(카테고리/키워드/기기/성별/연령별 쇼핑 트렌드).
- 기타: `get_current_korean_time`, `find_category`.

**6. AptInfo** — `get_region_code`, `get_apt_list`, `get_apt_info`(+`_bulk`), `get_apt_price`(실거래가).

**7. UsStockInfo** — `get_stock_info`, `get_historical_stock_prices`, `get_financial_statement`, `get_finance_news`, `get_holder_info`, `get_recommendations`, `get_stock_actions`, `get_option_expiration_dates`/`get_option_chain`.

**8. YouTubeData** — `search_videos`/`search_live_videos`/`search_playlists`, `get_video_details`/`get_video_comments`, `get_transcripts`/`list_available_captions`(자막), `get_related_videos`/`get_trending_videos`, `get_channel_details`/`_statistics`/`_top_videos`, `get_playlist_details`/`_items`, `get_video_categories`.

## 활용 아이디어 ([[내-프로필]] 관점)
- **일정·알림 자동화**: KakaotalkCal `CreateEvent` + KakaotalkChat `MemoChat`로 "정리 결과·리마인드"를 카카오로 푸시 → [[schedule-reporter-kakao]] 패턴을 코드 없이.
- **동향 추적**: NaverSearch `search_news`/`datalab_search` + YouTubeData `get_transcripts`로 AI 업계 뉴스·영상 요약 파이프라인 → [[Claude-Code-업데이트-동향]] 갱신 자동화.
- **TodoMate**로 위키 작성 후보·action item 관리.

## 의외의 연결점
- **카카오 푸시 = 알림 전략**: 개인 KakaotalkChat/Cal로 "결과를 사람에게 푸시" → [[에이전트-자동화-도구]]의 "자동화의 마지막 단계 = 알림".
- **NaverSearch 연령·성별 데이터랩**: 타게팅·트렌드 분석에 활용할 수 있는 데이터 소스.

## 관련 문서
- [[내-MCP-커넥터-환경]] · [[schedule-reporter-kakao]] · [[에이전트-자동화-도구]] · [[Claude-Code-업데이트-동향]] · [[내-프로필]]
