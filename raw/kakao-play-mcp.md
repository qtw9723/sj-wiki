# 카카오 Play MCP 도구 정리

- **MCP 서버**: 카카오에서 공식 제공하는 MCP 서버
- **서버 ID**: `8b9464aa-7091-4f2f-b3ad-f7055a1e8c3a`
- **정리일**: 2026-06-09

---

## 1. KakaoMap (카카오맵)

| 도구 | 설명 |
|------|------|
| `SearchPlaceByKeywordOpen` | 키워드로 장소 검색 |
| `GetWalkDirections` | 도보 길찾기 |
| `GetBikeDirections` | 자전거 길찾기 |
| `GetPublicTransitDirections` | 대중교통 길찾기 |

---

## 2. KakaotalkCal (카카오톡 캘린더)

| 도구 | 설명 |
|------|------|
| `GetCurrentTime` | 현재 시간 조회 |
| `GetEvent` | 캘린더 이벤트 조회 |
| `CreateEvent` | 캘린더 이벤트 생성 |
| `GetTask` | 할 일 조회 |
| `CreateTask` | 할 일 생성 |
| `GetFriendsBirthdays` | 카카오톡 친구 생일 조회 |

---

## 3. KakaotalkChat (카카오톡 채팅)

| 도구 | 설명 |
|------|------|
| `MemoChat` | 나에게 메모 메시지 전송 (나와의 채팅) |

---

## 4. TodoMate (투두메이트)

| 도구 | 설명 |
|------|------|
| `loadTodoItems` | 특정 날짜 할 일 목록 조회 |
| `loadTodoItemsByDateRange` | 날짜 범위로 할 일 목록 조회 |
| `loadGoals` | 목표 조회 |
| `addTodoItem` | 할 일 추가 |
| `updateTodoItem` | 할 일 수정 (완료 처리 포함) |
| `updateTodoItemRemindAt` | 할 일 알림 시간 설정/수정 |

---

## 5. NaverSearch (네이버 검색)

### 검색 도구
| 도구 | 설명 |
|------|------|
| `search_news` | 뉴스 검색 |
| `search_blog` | 블로그 검색 |
| `search_cafearticle` | 카페 글 검색 |
| `search_kin` | 지식iN 검색 |
| `search_image` | 이미지 검색 |
| `search_webkr` | 웹 문서 검색 |
| `search_book` | 책 검색 |
| `search_encyc` | 백과사전 검색 |
| `search_local` | 지역 검색 |
| `search_shop` | 쇼핑 검색 |
| `search_academic` | 학술 자료 검색 |

### 데이터랩 도구
| 도구 | 설명 |
|------|------|
| `datalab_search` | 검색어 트렌드 분석 |
| `datalab_shopping_category` | 쇼핑 카테고리 트렌드 |
| `datalab_shopping_keywords` | 쇼핑 키워드 트렌드 |
| `datalab_shopping_by_device` | 기기별 쇼핑 트렌드 |
| `datalab_shopping_by_gender` | 성별 쇼핑 트렌드 |
| `datalab_shopping_by_age` | 연령별 쇼핑 트렌드 |
| `datalab_shopping_keyword_by_device` | 키워드별 기기 트렌드 |
| `datalab_shopping_keyword_by_gender` | 키워드별 성별 트렌드 |
| `datalab_shopping_keyword_by_age` | 키워드별 연령 트렌드 |

### 기타
| 도구 | 설명 |
|------|------|
| `get_current_korean_time` | 현재 한국 시간 조회 |
| `find_category` | 카테고리 검색 |

---

## 6. AptInfo (아파트 정보)

| 도구 | 설명 |
|------|------|
| `get_region_code` | 지역 코드 조회 |
| `get_apt_list` | 지역 내 아파트 목록 조회 |
| `get_apt_info` | 아파트 상세 정보 조회 |
| `get_apt_info_bulk` | 아파트 정보 일괄 조회 |
| `get_apt_price` | 아파트 실거래가 조회 |

---

## 7. UsStockInfo (미국 주식 정보)

| 도구 | 설명 |
|------|------|
| `get_stock_info` | 주식 기본 정보 조회 |
| `get_historical_stock_prices` | 주가 이력 조회 |
| `get_financial_statement` | 재무제표 조회 |
| `get_finance_news` | 금융 뉴스 조회 |
| `get_holder_info` | 주주 정보 조회 |
| `get_recommendations` | 애널리스트 투자의견 조회 |
| `get_stock_actions` | 배당·주식분할 등 액션 조회 |
| `get_option_expiration_dates` | 옵션 만료일 조회 |
| `get_option_chain` | 옵션 체인 조회 |

---

## 8. YouTubeData (유튜브 데이터)

| 도구 | 설명 |
|------|------|
| `search_videos` | 영상 검색 |
| `get_video_details` | 영상 상세 정보 |
| `get_video_comments` | 영상 댓글 조회 |
| `get_transcripts` | 자막/스크립트 추출 |
| `list_available_captions` | 사용 가능한 자막 목록 |
| `get_related_videos` | 관련 영상 조회 |
| `get_trending_videos` | 트렌딩 영상 조회 |
| `get_video_categories` | 영상 카테고리 목록 |
| `search_live_videos` | 라이브 영상 검색 |
| `get_channel_details` | 채널 상세 정보 |
| `get_channel_statistics` | 채널 통계 |
| `get_channel_top_videos` | 채널 인기 영상 |
| `search_playlists` | 재생목록 검색 |
| `get_playlist_details` | 재생목록 상세 |
| `get_playlist_items` | 재생목록 영상 목록 |
