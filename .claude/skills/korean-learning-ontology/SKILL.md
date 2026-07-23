---
name: korean-learning-ontology
description: "국어 학습 플랫폼에 작품·단원·개념·창작자 관계를 추가하거나 수정하고, Graphify로 온톨로지 그래프를 다시 만들거나 시각화할 때 반드시 사용한다. 새 문학 작품, 학습 지도, 단원, 갈래, 읽기 개념을 입력받아 공개 가능한 메타정보만 Graphify graph.json·graph.html로 갱신하고, 중복 작품 병합과 정적 사이트 검증을 수행한다. 온톨로지 그래프의 재생성·업데이트·보완에도 사용한다."
---

# 국어 학습 온톨로지

1. 공개 가능한 식별 정보만 입력으로 삼는다. 작품명, 창작자·전승, 갈래, 학습 관점, 지도 경로는 허용한다. 교재 본문·문항·선택지·해설·정답·페이지 위치는 제외한다.
2. 학습 지도 Markdown을 먼저 갱신한 뒤 `uv run --with graphifyy python .claude/skills/korean-learning-ontology/scripts/build_ontology_graph.py`를 실행한다. 이 스크립트는 두 문학 읽기 지도의 작품·읽기 관점·창작자 관계를 Graphify 형식으로 생성한다.
3. Graphify 출력은 `source/ontology/graphify/graph.json`과 `graph.html`을 함께 유지한다. HTML은 Graphify의 클릭·검색·관계 필터 기능을 제공하며, JSON은 미래 입력의 원본 그래프이다.
4. 같은 작품은 지도마다 중복 노드를 만들지 않는다. 지도별 분류는 `contains_work` 엣지로 보존한다.
5. 생성 후 `npm run build`, `npm test`를 실행하고, 그래프 화면에서 작품·읽기 관점·창작자를 검색해 관계가 보이는지 확인한다.

## 테스트 시나리오

- 정상: 새 작품을 문학 읽기 지도에 추가하면 그래프가 작품 노드 하나와 지도·관점·창작자 엣지를 생성한다.
- 오류: 교재 문제나 해설을 그래프에 넣으려 하면 해당 항목을 제외하고 공개 메타정보만 유지한다.
