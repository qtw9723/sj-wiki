-- =====================================================================
--  팀숲(Bible Forest) 완료 보고서 — 데이터 추출 쿼리
--  작성: 상준 / 2026-08-31 / PostgreSQL(Supabase)
--
--  ▸ 이 파일 하나로 CSV 3장이 나옵니다. 나머지 지표는 제가 엑셀에서 계산할게요.
--    [쿼리 1] 개인별 집계 (1행 = 1명)
--    [쿼리 2] 일자별 활동  (1행 = 1일)
--    [쿼리 3] 검산용 퍼널 4숫자 (1·2가 맞는지 대조용)
--    [쿼리 4] 권별 읽힌 정도 (신약 27권, 27행)
--
--  ▸ 저장소를 직접 못 봐서 아래 4개는 추측으로 썼어요. 확인해서 고쳐주면 됩니다 🙏
-- =====================================================================
--
--  [확인 1] ⚠️ 가장 중요 — bible_progress가 권 단위 bulk replace 방식이라
--           row의 created_at이 "그 장을 실제로 읽은 시점"인지,
--           아니면 그 권을 마지막에 저장한 시점으로 갱신되는지?
--           → 후자면 [쿼리 2]의 날짜별 추이는 못 씁니다.
--             그 경우 new_users(가입 추이)만 살리고 활동 추이는 빼주세요.
--
--  [확인 2] created_at 컬럼 타입이 timestamptz인지 timestamp인지?
--           - timestamptz  → 아래처럼 AT TIME ZONE 'Asia/Seoul' 한 번 (현재 상태)
--           - timestamp(UTC 저장) → AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Seoul' 두 번
--             ⚠️ naive 컬럼에 한 번만 쓰면 변환이 거꾸로 돌아서 18시간 어긋납니다
--
--  [확인 3] (user_id, book, chapter) 유니크 키가 있는지?
--           없으면 아래 prog CTE의 중복 제거를 꼭 살려주세요.
--           (테스트해보니 중복 row 1건이 읽은 장수뿐 아니라
--            "인증한 날 수"까지 같이 부풀립니다)
--
--  [확인 4] book 컬럼 표기가 '마태'인지 'Matthew'인지 'MAT'인지?
--           → 아래 gospel 목록만 그 표기로 바꿔주면 됩니다.
--
--  [확인 5] 컬럼명 자체가 다르면 편한 대로 고쳐주세요
--           (bible_progress.book / .chapter / .created_at, users.created_at,
--            teams.theme, trees.user_id / .is_planted 가정)
-- =====================================================================


-- =====================================================================
--  [쿼리 1] 개인별 집계  → CSV 1
-- =====================================================================
WITH params AS (
  SELECT DATE '2026-07-01' AS d_start,      -- 배포일 (dev→main 머지 7/1 기준)
         DATE '2026-08-__' AS d_end         -- ⚠️ 수련회 종료 "다음날"로 채워주세요
),
excluded AS (   -- ⚠️ 테스트·개발팀 계정 제외 (닉네임 채워주세요)
  SELECT id FROM users
  WHERE nickname IN ('시연', '테스트' /* , '유성진', '백은률', '유혁상', '이다혜' ... */)
),
prog AS (
  -- 장 단위 중복 제거: (user, book, chapter)당 1건, 시각은 가장 이른 것
  -- ⚠️ DISTINCT에 created_at을 같이 넣으면 안 됩니다 —
  --    재저장된 중복은 시각이 달라서 DISTINCT를 그냥 통과해버려요
  SELECT bp.user_id, bp.book, bp.chapter, MIN(bp.created_at) AS created_at
  FROM bible_progress bp, params
  WHERE bp.user_id NOT IN (SELECT id FROM excluded)
    AND bp.created_at >= params.d_start
    AND bp.created_at <  params.d_end
  GROUP BY bp.user_id, bp.book, bp.chapter
),
tr AS (
  -- ⚠️ 요소(나무) 집계는 반드시 유저별 1행으로 먼저 접어야 합니다.
  --    trees를 그냥 LEFT JOIN하면 읽은 장 수가 나무 개수만큼 곱해져요.
  --    (테스트해보니 260장이 6,734장으로 부풀었습니다)
  SELECT t2.user_id,
         COUNT(*)                                AS items_total,
         COUNT(*) FILTER (WHERE t2.is_planted)   AS items_planted
  FROM trees t2
  WHERE t2.user_id NOT IN (SELECT id FROM excluded)
  GROUP BY t2.user_id
)
SELECT
  ROW_NUMBER() OVER (ORDER BY u.id)                AS user_no,      -- 실명/닉네임 대신 번호
  t.name                                           AS team,
  t.theme                                          AS team_theme,   -- 숲/바다/밤하늘
  (u.created_at AT TIME ZONE 'Asia/Seoul')         AS joined_at,
  COUNT(p.*)                                       AS total_ch,     -- 총 읽은 장 수
  COUNT(*) FILTER (WHERE p.book = '마태')          AS mt_ch,
  COUNT(*) FILTER (WHERE p.book = '마가')          AS mk_ch,
  COUNT(*) FILTER (WHERE p.book = '누가')          AS lk_ch,
  COUNT(*) FILTER (WHERE p.book = '요한')          AS jn_ch,
  COUNT(*) FILTER (WHERE p.book IN ('마태','마가','누가','요한'))
                                                   AS gospel_ch,    -- 사복음서 합 (89장 만점)
  MIN(p.created_at AT TIME ZONE 'Asia/Seoul')      AS first_read_at,
  MAX(p.created_at AT TIME ZONE 'Asia/Seoul')      AS last_read_at,
  COUNT(DISTINCT (p.created_at AT TIME ZONE 'Asia/Seoul')::date)
                                                   AS active_days,  -- 인증한 날 수
  COALESCE(tr.items_total, 0)                      AS items_total,  -- 보유 요소(나무/바다생물/별)
  COALESCE(tr.items_planted, 0)                    AS items_planted -- 그중 실제로 배치한 것
FROM users u
JOIN teams t ON t.id = u.team_id       -- ⚠️ team_id가 NULL인 유저가 있으면 LEFT JOIN으로
LEFT JOIN prog p ON p.user_id = u.id   -- ⚠️ LEFT: 0장 유저도 행을 남겨야 참여인원이 다 잡힘
LEFT JOIN tr    ON tr.user_id = u.id   --    tr은 이미 유저당 1행이라 뻥튀기 없음
WHERE u.id NOT IN (SELECT id FROM excluded)
GROUP BY u.id, t.name, t.theme, u.created_at, tr.items_total, tr.items_planted
ORDER BY total_ch DESC;


-- =====================================================================
--  [쿼리 2] 일자별 활동  → CSV 2
--  ⚠️ [확인 1]의 답에 따라 active_users / chapters는 못 쓸 수 있습니다.
--     new_users(가입 추이)는 bulk replace와 무관해서 항상 신뢰 가능해요.
-- =====================================================================
WITH params AS (
  SELECT DATE '2026-07-01' AS d_start, DATE '2026-08-__' AS d_end
),
excluded AS (
  SELECT id FROM users WHERE nickname IN ('시연', '테스트' /* + 개발팀 */)
),
prog AS (
  SELECT bp.user_id, bp.book, bp.chapter, MIN(bp.created_at) AS created_at
  FROM bible_progress bp, params
  WHERE bp.user_id NOT IN (SELECT id FROM excluded)
    AND bp.created_at >= params.d_start AND bp.created_at < params.d_end
  GROUP BY bp.user_id, bp.book, bp.chapter
),
d AS (   -- 활동 없는 날도 0으로 채우기 (빠지면 추이 그래프가 왜곡됨)
  SELECT generate_series(params.d_start, params.d_end - 1, INTERVAL '1 day')::date AS date_kst
  FROM params
),
act AS (
  SELECT (created_at AT TIME ZONE 'Asia/Seoul')::date AS d,
         COUNT(DISTINCT user_id) AS au,
         COUNT(*)                AS ch
  FROM prog GROUP BY 1
),
reg AS (
  SELECT (u.created_at AT TIME ZONE 'Asia/Seoul')::date AS d, COUNT(*) AS nu
  FROM users u, params
  WHERE u.id NOT IN (SELECT id FROM excluded)
    AND u.created_at >= params.d_start AND u.created_at < params.d_end
  GROUP BY 1
)
SELECT d.date_kst,
       COALESCE(act.au, 0) AS active_users,   -- 그날 1장 이상 인증한 인원
       COALESCE(act.ch, 0) AS chapters,       -- 그날 인증된 장 수
       COALESCE(reg.nu, 0) AS new_users       -- 그날 신규 가입자
FROM d
LEFT JOIN act ON act.d = d.date_kst
LEFT JOIN reg ON reg.d = d.date_kst
ORDER BY d.date_kst;


-- =====================================================================
--  [쿼리 3] 검산용 — 퍼널 4숫자
--  (쿼리 1을 엑셀에서 집계한 값과 이 결과가 같아야 정상)
--  사복음서 = 마태28 + 마가16 + 누가24 + 요한21 = 89장
--  신약 1독 = 260장
-- =====================================================================
WITH params AS (
  SELECT DATE '2026-07-01' AS d_start, DATE '2026-08-__' AS d_end
),
excluded AS (
  SELECT id FROM users WHERE nickname IN ('시연', '테스트' /* + 개발팀 */)
),
prog AS (
  SELECT bp.user_id, bp.book, bp.chapter, MIN(bp.created_at) AS created_at
  FROM bible_progress bp, params
  WHERE bp.user_id NOT IN (SELECT id FROM excluded)
    AND bp.created_at >= params.d_start AND bp.created_at < params.d_end
  GROUP BY bp.user_id, bp.book, bp.chapter
),
pu AS (
  SELECT u.id,
         COUNT(p.*) AS total_ch,
         COUNT(*) FILTER (WHERE p.book IN ('마태','마가','누가','요한')) AS gospel_ch
  FROM users u
  LEFT JOIN prog p ON p.user_id = u.id
  WHERE u.id NOT IN (SELECT id FROM excluded)
  GROUP BY u.id
)
SELECT COUNT(*)                                AS "가입",
       COUNT(*) FILTER (WHERE total_ch > 0)    AS "1장이상",
       COUNT(*) FILTER (WHERE gospel_ch >= 89) AS "사복음서완독",
       COUNT(*) FILTER (WHERE total_ch >= 260) AS "신약1독"
FROM pu;


-- =====================================================================
--  [쿼리 4] 권별 읽힌 정도  → CSV 3  (신약 27권, 27행)
--
--  ▸ "사람들이 신약 어디쯤에서 멈췄는지"를 보려고 합니다.
--    사복음서(89장)는 신약의 34%밖에 안 돼서, 나머지 66% 구간이
--    쿼리 1만으로는 전혀 안 보이거든요.
--
--  ▸ ⚠️ [확인 4] 관련: book 표기가 '마태'가 아니면 아래 VALUES 목록의
--    27개 이름만 실제 표기로 바꿔주면 됩니다. (장 수는 그대로 두세요)
--    쿼리 1의 사복음서 필터도 같은 표기로 맞춰주시고요.
-- =====================================================================
WITH params AS (
  SELECT DATE '2026-07-01' AS d_start, DATE '2026-08-__' AS d_end
),
excluded AS (
  SELECT id FROM users WHERE nickname IN ('시연', '테스트' /* + 개발팀 */)
),
prog AS (
  SELECT bp.user_id, bp.book, bp.chapter
  FROM bible_progress bp, params
  WHERE bp.user_id NOT IN (SELECT id FROM excluded)
    AND bp.created_at >= params.d_start AND bp.created_at < params.d_end
  GROUP BY bp.user_id, bp.book, bp.chapter      -- 장 단위 중복 제거
),
nt(ord, book, total_ch) AS (VALUES   -- 신약 27권 · 성경 순서 · 권별 장 수 (합 260)
  (1,'마태',28),(2,'마가',16),(3,'누가',24),(4,'요한',21),(5,'사도행전',28),
  (6,'로마서',16),(7,'고린도전서',16),(8,'고린도후서',13),(9,'갈라디아서',6),
  (10,'에베소서',6),(11,'빌립보서',4),(12,'골로새서',4),(13,'데살로니가전서',5),
  (14,'데살로니가후서',3),(15,'디모데전서',6),(16,'디모데후서',4),(17,'디도서',3),
  (18,'빌레몬서',1),(19,'히브리서',13),(20,'야고보서',5),(21,'베드로전서',5),
  (22,'베드로후서',3),(23,'요한1서',5),(24,'요한2서',1),(25,'요한3서',1),
  (26,'유다서',1),(27,'요한계시록',22)
),
per AS (   -- 권 × 사람 단위로 먼저 펼침
  SELECT nt.ord, nt.book, nt.total_ch, p.user_id, COUNT(p.*) AS ch
  FROM nt
  LEFT JOIN prog p ON p.book = nt.book   -- ⚠️ LEFT: 아무도 안 읽은 권도 0행으로 남겨야
  GROUP BY nt.ord, nt.book, nt.total_ch, p.user_id  --    "여기서 멈췄다"가 그래프에 보임
)
SELECT ord                                      AS book_order,
       book,
       total_ch,                                -- 그 권의 전체 장 수
       COUNT(user_id)                           AS readers,       -- 1장이라도 읽은 사람
       COUNT(*) FILTER (WHERE ch >= total_ch)   AS finishers,     -- 그 권을 완독한 사람
       COALESCE(SUM(ch), 0)                     AS chapters_read  -- 읽힌 장 수 합계
FROM per
GROUP BY ord, book, total_ch
ORDER BY ord;


-- =====================================================================
--  [쿼리 5] 완독 판정 — 권 단위 (2026-09-02 추가)
--
--  ▸ 왜 필요한가:
--    [쿼리 3]의 사복음서 완독은 "마태+마가+누가+요한 장수 합 = 89"로 셌습니다.
--    이건 합계 기준이라, "정말 네 권을 각각 끝까지 읽었는가"를 직접 확인하지 않습니다.
--    아래는 권마다 완독 여부를 판정한 뒤 그 개수를 세는 정공법입니다.
--
--  ▸ 2026-09-02 실측: 두 방식 모두 30명으로 같았습니다.
--    (장수 합 89 = 각 권 상한(28·16·24·21)의 합이라, 중복 제거가 제대로 되고
--     그 권에 없는 장 번호가 없으면 수학적으로 같은 집합이 됩니다.)
--    다만 ⚠️ 중복 row가 남거나 잘못된 장 번호(예: 마태 30장)가 섞이면
--    합계 기준은 89를 넘겨 "완독"으로 오판할 수 있고, 아래 권 단위 기준은
--    LEAST()로 상한을 걸어 그 오판을 막습니다. 보고서 기준은 이쪽을 씁니다.
-- =====================================================================
WITH params AS (
  SELECT DATE '2026-07-01' AS d_start, DATE '2026-08-__' AS d_end   -- ⚠️ 종료일 채우기
),
excluded AS (
  SELECT id FROM users WHERE nickname IN ('시연', '테스트' /* + 개발팀 */)
),
nt(ord, book, total_ch) AS (VALUES
  (1,'마태',28),(2,'마가',16),(3,'누가',24),(4,'요한',21),
  (5,'사도행전',28),(6,'로마서',16),(7,'고린도전서',16),(8,'고린도후서',13),
  (9,'갈라디아서',6),(10,'에베소서',6),(11,'빌립보서',4),(12,'골로새서',4),
  (13,'데살로니가전서',5),(14,'데살로니가후서',3),(15,'디모데전서',6),(16,'디모데후서',4),
  (17,'디도서',3),(18,'빌레몬서',1),(19,'히브리서',13),(20,'야고보서',5),
  (21,'베드로전서',5),(22,'베드로후서',3),(23,'요한1서',5),(24,'요한2서',1),
  (25,'요한3서',1),(26,'유다서',1),(27,'요한계시록',22)
),
prog AS (   -- 장 단위 중복 제거 (쿼리 1과 동일 규칙)
  SELECT DISTINCT bp.user_id, bp.book, bp.chapter
  FROM bible_progress bp, params
  WHERE bp.user_id NOT IN (SELECT id FROM excluded)
    AND bp.created_at >= params.d_start
    AND bp.created_at <  params.d_end
),
per_book AS (   -- 사람 × 권 : 그 권에서 읽은 장 수 (⚠️ 상한을 넘지 못하게 LEAST)
  SELECT p.user_id,
         nt.ord,
         nt.book,
         nt.total_ch,
         LEAST(COUNT(*), nt.total_ch)                  AS ch_read,
         (COUNT(*) >= nt.total_ch)                     AS is_done,
         (COUNT(*) >  nt.total_ch)                     AS is_overflow  -- ⚠️ 있으면 데이터 오류
  FROM prog p
  JOIN nt ON nt.book = p.book
  GROUP BY p.user_id, nt.ord, nt.book, nt.total_ch
),
per_user AS (
  SELECT user_id,
         COUNT(*) FILTER (WHERE is_done AND ord <= 4)  AS gospels_done,   -- 완독한 복음서 권수 0~4
         COUNT(*) FILTER (WHERE is_done)               AS books_done,     -- 완독한 신약 권수 0~27
         SUM(ch_read)                                  AS total_ch,
         SUM(ch_read) FILTER (WHERE ord <= 4)          AS gospel_ch,
         BOOL_OR(is_overflow)                          AS has_overflow
  FROM per_book
  GROUP BY user_id
)
SELECT
  COUNT(*) FILTER (WHERE gospels_done = 4)   AS 사복음서_완독_4권,      -- ★ 보고서 기준
  COUNT(*) FILTER (WHERE gospels_done >= 1)  AS 사복음서_1권이상_완독,
  COUNT(*) FILTER (WHERE gospel_ch   >  0)   AS 사복음서_1장이상,
  COUNT(*) FILTER (WHERE books_done  = 27)   AS 신약_1독_27권,          -- ★ 보고서 기준
  COUNT(*) FILTER (WHERE total_ch    = 260)  AS 신약_1독_260장_대조용,  -- 위와 같아야 정상
  COUNT(*) FILTER (WHERE has_overflow)       AS 데이터오류_상한초과      -- ⚠️ 0이어야 정상
FROM per_user;

-- 사람별로 보고 싶으면 마지막 SELECT를 아래로 바꾸세요 (완독 권수 분포 확인용)
-- SELECT gospels_done, COUNT(*) FROM per_user GROUP BY 1 ORDER BY 1;
--   → 2026-09-02 실측 결과: 0권 145 / 1권 12 / 2권 5 / 3권 4 / 4권 30
