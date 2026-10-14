# -*- coding: utf-8 -*-
"""
[어와나 불티단 3권 스카이스토머 성경퀴즈대회 대비 문제은행식 RPG 게임]
버전: v3.0 (문제 은행 랜덤 무한 생성 시스템)
특징:
 - 스카이스토머 전체 범위(승급과정, 성경 66권, 빨강보석 1~4, 초록보석 1~4, 성경실화, 단어 뜻, 맞춤법) 70문항 대규모 문제은행 탑재
 - 매 게임마다 10문제가 전체 범위에서 무작위로 추출되며, 객관식 보기 순서(1,2,3)도 실시간 셔플
 - 2학년 아이 눈높이 맞춤 타격감 연출, 콤보 시스템, 전신갑주 파츠 & 10대 말씀 보석 수집 RPG
"""

import sys
import time
import random
import re

# ==============================================================================
# 1. 스카이스토머 전 범위 대규모 문제 은행 (QUESTION BANK)
# ==============================================================================

# 🅰️ 객관식 문제 은행 (총 40문항)
MC_QUESTION_BANK = [
    # --- [승급과정: SPARKS & 주제성구] ---
    {
        "category": "승급과정 (SPARKS)",
        "question": "불티단 SPARKS 구원 성구 중 'R'은 'Rose again(부활)'을 뜻합니다. 이에 해당하는 말씀은?",
        "correct": "고린도전서 15장 4절 (장사 지낸 바 되셨다가 성경대로 사흘 만에 다시 살아나사)",
        "distractors": [
            "요한1서 4장 14절 (아버지가 아들을 세상의 구주로 보내신 것을...)",
            "야고보서 2장 10절 (누구든지 온 율법을 지키다가 그 하나를 범하면...)"
        ],
        "hint": "'다시 살아나셨다'는 부활(Rose again)은 고린도전서 15장 4절이에요!",
        "explanation": "R은 Rose again(부활) - 고린도전서 15장 4절입니다!"
    },
    {
        "category": "승급과정 (SPARKS)",
        "question": "불티단 SPARKS 구원 성구 중 'P'는 'Power(능력)'을 뜻합니다. 이에 해당하는 말씀은?",
        "correct": "시편 147편 5절 (우리 주는 위대하시며 능력이 많으시며...)",
        "distractors": [
            "사도행전 16장 31절 (주 예수를 믿으라 그리하면 너와 네 집이 구원을 받으리라)",
            "고린도전서 15장 3절 (...성경대로 그리스도께서 우리 죄를 위하여 죽으시고)"
        ],
        "hint": "하나님의 크신 능력을 찬양하는 시편 말씀이에요!",
        "explanation": "P는 Power(능력) - 시편 147편 5절입니다!"
    },
    {
        "category": "승급과정 (SPARKS)",
        "question": "불티단 SPARKS 구원 성구 중 'K'는 'Keep(지키다)'를 의미합니다. 이에 해당하는 말씀은?",
        "correct": "야고보서 2장 10절 (누구든지 온 율법을 지키다가 그 하나를 범하면 모두 범한 자가 되나니)",
        "distractors": [
            "고린도전서 15장 3절 (...성경대로 그리스도께서 우리 죄를 위하여 죽으시고)",
            "요한1서 4장 14절 (아버지가 아들을 세상의 구주로 보내신 것을...)"
        ],
        "hint": "율법을 지키는 것에 관한 야고보서 말씀이에요!",
        "explanation": "K는 Keep(지키다) - 야고보서 2장 10절입니다!"
    },
    {
        "category": "승급과정 (SPARKS)",
        "question": "불티단 SPARKS 구원 성구 중 'A'는 'According to the scriptures(성경대로)'를 뜻합니다. 이에 해당하는 말씀은?",
        "correct": "고린도전서 15장 3절 (...성경대로 그리스도께서 우리 죄를 위하여 죽으시고)",
        "distractors": [
            "시편 147편 5절 (우리 주는 위대하시며 능력이 많으시며...)",
            "사도행전 16장 31절 (주 예수를 믿으라 그리하면...)"
        ],
        "hint": "'성경대로 그리스도께서 죽으시고' 말씀이에요!",
        "explanation": "A는 According to the scriptures(성경대로) - 고린도전서 15장 3절입니다!"
    },
    {
        "category": "승급과정 (SPARKS)",
        "question": "다음 중 불티단 영어 이름 'SPARKS'의 약자를 설명하는 성경구절이 [아닌] 것은?",
        "correct": "디모데후서 3장 15절",
        "distractors": [
            "요한1서 4장 14절 (S: Savior)",
            "시편 147편 5절 (P: Power)"
        ],
        "hint": "디모데후서는 초록보석 3에서 배운 말씀이에요!",
        "explanation": "SPARKS 성구 6개는 요일 4:14, 시 147:5, 고전 15:3, 고전 15:4, 약 2:10, 행 16:31 입니다."
    },
    {
        "category": "승급과정 (주제성구)",
        "question": "‘신명기 31장 8절’ 말씀 “여호와 그가 네 앞에서 가시며…” 다음에 이어지는 바른 말씀은?",
        "correct": "너와 함께 하사 너를 떠나지 아니하시며 버리지 아니하시리니 너는 두려워하지 말라 놀라지 말라",
        "distractors": [
            "기도를 계속하고 기도에 감사함으로 깨어 있으라",
            "그에게 감사하며 그의 이름을 송축할지어다"
        ],
        "hint": "하나님이 항상 함께 계시니 두려워하지 말고 놀라지 말라는 약속이에요!",
        "explanation": "신명기 31:8 - '...너와 함께 하사 너를 떠나지 아니하시며 버리지 아니하시리니 너는 두려워하지 말라 놀라지 말라'"
    },
    {
        "category": "승급과정 (단어)",
        "question": "요한복음 3장 16절 주제성구에서 '멸망'의 의미로 올바른 것은?",
        "correct": "하나님으로부터 영원히 분리됨",
        "distractors": [
            "세상에서 돈을 다 잃어버림",
            "시험에서 점수를 못 받음"
        ],
        "hint": "하나님 곁을 떠나 영원히 나누어지는 것을 뜻해요!",
        "explanation": "멸망 = 하나님으로부터 영원히 분리됨"
    },
    {
        "category": "승급과정 (단어)",
        "question": "야고보서 2장 10절에서 '율법'의 뜻으로 올바른 것은?",
        "correct": "하나님의 계명에서 정한 규칙",
        "distractors": [
            "사람들이 만든 세상의 법률",
            "교회에서 부르는 찬송가"
        ],
        "hint": "하나님의 계명에서 정해진 규칙을 뜻해요!",
        "explanation": "율법은 '하나님의 계명에서 정한 규칙'을 의미합니다."
    },

    # --- [성경 목록: 66권, 구약 39권, 신약 27권, 순서] ---
    {
        "category": "성경목록",
        "question": "다음 중 구약성경 책 이름의 순서가 바르게 연결된 것은?",
        "correct": "에스겔 ➜ 다니엘 ➜ 호세아",
        "distractors": [
            "아모스 ➜ 요엘 ➜ 요나",
            "에스더 ➜ 느헤미야 ➜ 에스라"
        ],
        "hint": "성경 목록가: '...이사야 예레미야 애가 에스겔 다니엘 호세아 요엘...' 순서예요!",
        "explanation": "구약 순서: 에스겔(겔) - 다니엘(단) - 호세아(호) - 요엘(욜) 순서입니다."
    },
    {
        "category": "성경목록",
        "question": "다음 중 구약성경 책 이름의 순서가 바르게 연결된 것은?",
        "correct": "전도서 ➜ 아가 ➜ 이사야",
        "distractors": [
            "느헤미야 ➜ 에스라 ➜ 욥기",
            "레위기 ➜ 사사기 ➜ 룻기"
        ],
        "hint": "시편 - 잠언 - 전도서 - 아가 - 이사야 순서예요!",
        "explanation": "시편 다음 잠언, 전도서, 아가, 이사야로 이어집니다."
    },
    {
        "category": "성경목록",
        "question": "다음 중 구약성경 책 이름의 순서가 바르게 연결된 것은?",
        "correct": "요나 ➜ 미가 ➜ 나훔",
        "distractors": [
            "신명기 ➜ 민수기 ➜ 여호수아",
            "느헤미야 ➜ 에스라 ➜ 욥기"
        ],
        "hint": "오바댜 - 요나 - 미가 - 나훔 - 하박국 순서예요!",
        "explanation": "요나 다음은 미가, 그 다음은 나훔입니다."
    },
    {
        "category": "성경목록",
        "question": "다음 중 신약성경 책 이름의 순서가 바르게 연결된 것은?",
        "correct": "갈라디아서 ➜ 에베소서 ➜ 빌립보서",
        "distractors": [
            "골로새서 ➜ 빌립보서 ➜ 에베소서",
            "로마서 ➜ 갈라디아서 ➜ 고린도전서"
        ],
        "hint": "'갈-엡-빌-골' 순서로 외워요!",
        "explanation": "갈라디아서 - 에베소서 - 빌립보서 - 골로새서 순서입니다."
    },
    {
        "category": "성경목록",
        "question": "다음 중 구약성경의 책 이름과 약자 표기가 올바른 것은?",
        "correct": "예레미야애가 - (애)",
        "distractors": [
            "에스라 - (에)",
            "예레미야 - (예)"
        ],
        "hint": "에스라는 (스), 예레미야는 (렘), 예레미야애가는 (애)예요!",
        "explanation": "에스더가 (에)이고, 에스라는 (스), 예레미야애가는 (애)가 맞습니다."
    },

    # --- [빨강보석 1: 크리스마스의 진실 & 동방박사] ---
    {
        "category": "빨강보석 1",
        "question": "‘천사가 이르되 무서워하지 말라 보라 내가 (이것)에게 미칠 큰 기쁨의 (이것)을 너희에게 전하노라’ (이것) 2개는?",
        "correct": "온 백성, 좋은 소식",
        "distractors": [
            "모든 사람, 기쁜 소식",
            "온 나라, 복된 소식"
        ],
        "hint": "누가복음 2:10 말씀! '온 백성'에게 미칠 큰 기쁨의 '좋은 소식'!",
        "explanation": "눅 2:10-11: '...온 백성에게 미칠 큰 기쁨의 좋은 소식을 너희에게 전하노라'"
    },
    {
        "category": "빨강보석 1",
        "question": "스카이스토머 핸드북에서 배운 예수님의 어린 시절 내용 중 [틀린] 것은?",
        "correct": "예수님은 베들레헴에서 자랐어요.",
        "distractors": [
            "예수님이 태어난 지 1년쯤 되었을 때, 동방박사들이 베들레헴의 집으로 찾아왔어요.",
            "헤롯 왕이 죽은 후에 요셉의 가족은 나사렛으로 돌아왔어요."
        ],
        "hint": "예수님은 헤롯을 피해 애굽에 갔다가 '나사렛'에서 자라셨어요!",
        "explanation": "예수님은 베들레헴에서 태어나셨지만, 자라신 곳은 나사렛입니다."
    },
    {
        "category": "빨강보석 1",
        "question": "이사야 9장 6절에서 '놀라운 기적을 행하는 분'을 의미하는 예수님의 이름은?",
        "correct": "기묘자",
        "distractors": [
            "모사",
            "평강의 왕"
        ],
        "hint": "기이하고 묘한 놀라운 기적을 베푸시는 분!",
        "explanation": "기묘자 = 놀라운 기적을 행하는 분, 모사 = 올바르고 참된 말을 해 주는 분입니다."
    },
    {
        "category": "빨강보석 1",
        "question": "이사야 9장 6절 말씀에서 '그의 어깨에는 정사를 메었고'의 올바른 뜻은?",
        "correct": "예수님이 왕으로 세상을 다스리심",
        "distractors": [
            "예수님이 무거운 십자가를 짊어지심",
            "예수님이 겉옷을 어깨에 걸치심"
        ],
        "hint": "예수님이 온 세상의 왕으로서 다스리신다는 뜻이에요!",
        "explanation": "정사를 메었고는 '예수님이 왕으로 세상을 다스리심'을 의미합니다."
    },
    {
        "category": "빨강보석 1",
        "question": "‘태초에 말씀이 계시니라 이 말씀이 하나님과 함께 계셨으니...’ 이 말씀의 출처는?",
        "correct": "요한복음 1장 1-3절",
        "distractors": [
            "누가복음 2장 10-11절",
            "이사야 9장 6절"
        ],
        "hint": "태초의 '말씀(예수 그리스도)'을 증언하는 요한복음 첫 장이에요!",
        "explanation": "요한복음 1장 1-3절 말씀입니다."
    },

    # --- [초록보석 1: 예수님의 생애 - 나병환자, 어린아이, 삭개오] ---
    {
        "category": "초록보석 1",
        "question": "‘...그에게 감사하며 그의 이름을 송축할지어다’(시편 100:4)의 앞부분으로 알맞은 것은?",
        "correct": "감사함으로 그의 문에 들어가며 찬송함으로 그의 궁정에 들어가서",
        "distractors": [
            "찬송함으로 그의 성에 들어가며 기쁨으로 여호와를 섬기며",
            "즐거운 찬송을 부르며 노래하면서 그의 앞에 나아가며"
        ],
        "hint": "'감사함으로 그의 문에 들어가며 찬송함으로 그의 궁정에 들어가서'!",
        "explanation": "시편 100편 4절: '감사함으로 그의 문에 들어가며 찬송함으로 그의 궁정에 들어가서...'"
    },
    {
        "category": "초록보석 1",
        "question": "마태복음 19장 14절 ‘예수께서 이르시되 어린 아이들을 용납하고 ( 이것 )을 금하지 말라’에서 (이것)은?",
        "correct": "내게 오는 것",
        "distractors": [
            "가까이 오는 것",
            "시끄럽게 하는 것"
        ],
        "hint": "아이들이 예수님께 나아오는 것을 막지 말라고 하셨어요!",
        "explanation": "마 19:14: '어린 아이들을 용납하고 내게 오는 것을 금하지 말라 천국이 이런 사람의 것이니라'"
    },
    {
        "category": "초록보석 1",
        "question": "누가복음 19장 10절 ‘인자가 온 것은 잃어버린 자를 찾아 구원하려 함이니라’에서 '인자'가 뜻하는 분은?",
        "correct": "예수 그리스도",
        "distractors": [
            "세리장 삭개오",
            "사도 베드로"
        ],
        "hint": "사람의 아들로 오신 우리의 참 구주 예수님을 가리켜요!",
        "explanation": "인자는 '예수 그리스도'를 의미하며, 잃어버린 자는 '예수님을 믿어야 하는 죄인들'입니다."
    },
    {
        "category": "초록보석 1",
        "question": "핸드북 내용 중 [틀린] 것은 무엇인가요?",
        "correct": "예수님을 구주로 믿는다고 하나님의 자녀가 되는 것은 아니에요.",
        "distractors": [
            "예수님은 어린이를 사랑하고 돌보세요.",
            "하늘나라는 예수님을 어린이들처럼 믿는 사람들을 위한 것이에요."
        ],
        "hint": "예수님을 구주로 믿으면 누구든지 하나님의 자녀(왕의 자녀)가 됩니다!",
        "explanation": "예수님을 구주로 믿으면 하나님의 자녀가 됩니다."
    },

    # --- [빨강보석 2: 죽으시고 다시 사신 예수님 - 백부장, 마리아] ---
    {
        "category": "빨강보석 2",
        "question": "‘요한1서 5장 12절’ 말씀으로 알맞은 것은?",
        "correct": "아들이 있는 자에게는 생명이 있고 하나님의 아들이 없는 자에게는 생명이 없느니라",
        "distractors": [
            "아버지가 아들을 세상의 구주로 보내신 것을 우리가 보았고 또 증언하노니",
            "우리가 사랑함은 그가 먼저 우리를 사랑하셨음이라"
        ],
        "hint": "'아들이 있는 자에게는 생명이 있고...'!",
        "explanation": "요일 5:12: '아들이 있는 자에게는 생명이 있고 하나님의 아들이 없는 자에게는 생명이 없느니라'"
    },
    {
        "category": "빨강보석 2",
        "question": "로마서 5장 8절 ‘...하나님께서 우리에 대한 자기의 사랑을 확증하셨느니라’에서 '확증하다'의 뜻은?",
        "correct": "보여주다, 증명하다",
        "distractors": [
            "숨겨두다, 감추다",
            "마음속으로 생각하다"
        ],
        "hint": "사랑을 눈앞에 확실하게 보여주고 증명하셨다는 뜻이에요!",
        "explanation": "확증하다 = 보여주다, 증명하다"
    },
    {
        "category": "빨강보석 2",
        "question": "“그가 여기 계시지 않고 그가 말씀 하시던 대로 살아나셨느니라”로 시작하는 부활의 성경구절은?",
        "correct": "마태복음 28장 6절",
        "distractors": [
            "마태복음 18장 6절",
            "마태복음 28장 16절"
        ],
        "hint": "마태복음 마지막 28장에 나오는 빈 무덤 말씀이에요!",
        "explanation": "마태복음 28장 6절 말씀입니다."
    },
    {
        "category": "빨강보석 2",
        "question": "‘요한1서 4장 15절’ “누구든지 예수를 ( 이것 )이라 시인하면 하나님이 그의 안에 거하시고...”에서 (이것)은?",
        "correct": "하나님의 아들",
        "distractors": [
            "영원한 왕",
            "위대한 선지자"
        ],
        "hint": "예수님을 '하나님의 OO'이라고 고백해야 해요!",
        "explanation": "요일 4:15: '누구든지 예수를 하나님의 아들이라 시인하면...'"
    },
    {
        "category": "빨강보석 2",
        "question": "십자가에서 예수님이 숨을 거두실 때 땅이 흔들리는 것을 보고 “진실로 하나님의 아들이다!”라고 고백한 사람은?",
        "correct": "로마 백부장",
        "distractors": [
            "헤롯 왕",
            "본디오 빌라도 총독"
        ],
        "hint": "100명의 병사를 거느린 로마군의 지휘관이에요!",
        "explanation": "로마 백부장의 참된 신앙고백이었습니다."
    },

    # --- [초록보석 2: 선교활동 - 빌립, 행 1:8] ---
    {
        "category": "초록보석 2",
        "question": "“내가 복음을 부끄러워하지 아니하노니...”로 시작하는 복음의 능력 성경구절은?",
        "correct": "로마서 1장 16절",
        "distractors": [
            "사도행전 1장 8절",
            "로마서 5장 8절"
        ],
        "hint": "복음은 모든 믿는 자에게 구원을 주시는 하나님의 능력이 됨이라!",
        "explanation": "로마서 1장 16절 말씀입니다."
    },
    {
        "category": "초록보석 2",
        "question": "“오직 성령이 너희에게 임하시면 너희가 권능을 받고...”로 시작하는 성경구절은?",
        "correct": "사도행전 1장 8절",
        "distractors": [
            "사도행전 11장 8절",
            "사도행전 1장 18절"
        ],
        "hint": "예루살렘과 온 유대와 사마리아와 땅 끝까지 이르러 내 증인이 되리라!",
        "explanation": "사도행전 1장 8절 말씀입니다."
    },
    {
        "category": "초록보석 2",
        "question": "에디오피아 여왕의 관리(내시)에게 이사야서를 풀어서 복음을 전하고 세례를 준 사람은?",
        "correct": "빌립",
        "distractors": [
            "바울",
            "베드로"
        ],
        "hint": "천사의 말에 순종하여 광야 길로 달려간 전도자예요!",
        "explanation": "집사 빌립이 에디오피아 관리에게 예수님을 전하고 세례를 주었습니다."
    },
    {
        "category": "초록보석 2",
        "question": "사도행전 1장 8절에서 '증인'의 의미로 올바른 것은?",
        "correct": "예수님의 복음을 전하는 사람들",
        "distractors": [
            "법원에서 재판을 구경하는 사람",
            "글씨를 예쁘게 쓰는 사람"
        ],
        "hint": "땅 끝까지 이르러 예수님의 십자가와 부활을 전하는 성도들!",
        "explanation": "증인 = 예수님의 복음을 전하는 사람들"
    },

    # --- [빨강보석 3: 베드로와 처음교회 - 다비다, 기도] ---
    {
        "category": "빨강보석 3",
        "question": "‘골로새서 4장 2절’에서 ‘깨어 있으라’의 의미는 무엇인가요?",
        "correct": "기도할 때 하나님의 응답에 주의를 기울이라",
        "distractors": [
            "기도할 때 잠들거나 졸지 말아라",
            "기도할 때 중언부언하지 말아라"
        ],
        "hint": "기도하면서 하나님이 어떻게 응답하시는지 귀 기울여 살펴보라는 뜻!",
        "explanation": "깨어 있으라 = 기도할 때 하나님의 응답에 주의를 기울이라"
    },
    {
        "category": "빨강보석 3",
        "question": "욥바 마을에서 가난한 이웃을 위해 옷을 지어주다 숨졌으나 베드로의 기도로 살아난 여제자의 이름은?",
        "correct": "다비다 (도르가)",
        "distractors": [
            "살로메 (마르다)",
            "루디아 (뵈베)"
        ],
        "hint": "도르가라는 또 다른 이름을 가진 아름다운 제자예요!",
        "explanation": "가난한 이웃의 친구 다비다(도르가) 이야기입니다."
    },
    {
        "category": "빨강보석 3",
        "question": "‘자녀들아 우리가 말과 혀로만 사랑하지 말고 행함과 진실함으로 하자’ 이 말씀의 출처는?",
        "correct": "요한1서 3장 17-18절",
        "distractors": [
            "골로새서 4장 2절",
            "빌립보서 4장 4절"
        ],
        "hint": "세상의 재물을 가지고 궁핍한 형제를 돕는 참 사랑의 말씀!",
        "explanation": "요한1서 3장 17-18절 말씀입니다."
    },

    # --- [초록보석 3: 바울의 선교여행 - 감옥 찬송, 풍랑, 기뻐하라] ---
    {
        "category": "초록보석 3",
        "question": "‘빌립보서 4장 4절’ 말씀으로 알맞은 것은?",
        "correct": "주 안에서 항상 기뻐하라 내가 다시 말하노니 기뻐하라",
        "distractors": [
            "기도를 계속하고 기도에 감사함으로 깨어 있으라",
            "인자가 온 것은 잃어버린 자를 찾아 구원하려 함이니라"
        ],
        "hint": "'기뻐하라'가 두 번 들어가는 감옥에서의 찬송 말씀!",
        "explanation": "빌립보서 4:4 - '주 안에서 항상 기뻐하라 내가 다시 말하노니 기뻐하라'"
    },
    {
        "category": "초록보석 3",
        "question": "‘고린도후서 12장 9절’에서 ‘우리가 자격이 없는데도 도와주시고 돌보아주시는 하나님의 사랑’을 뜻하는 단어는?",
        "correct": "은혜",
        "distractors": [
            "긍휼",
            "화평"
        ],
        "hint": "\"내 은혜가 네게 족하도다!\"",
        "explanation": "은혜 = 우리가 자격이 없는데도 도와주시고 돌보아주시는 하나님의 사랑"
    },
    {
        "category": "초록보석 3",
        "question": "바울이 로마로 가던 배가 거센 유라굴로 광풍을 만났을 때, 무사히 구원받은 사람은 몇 명인가요?",
        "correct": "276명 전원",
        "distractors": [
            "120명",
            "70명"
        ],
        "hint": "하나님의 약속대로 단 한 사람도 잃지 않고 276명 모두 살았어요!",
        "explanation": "하나님의 천사가 바울에게 약속하신 대로 276명 전원이 해변에 안전하게 상륙했습니다."
    },
    {
        "category": "초록보석 3",
        "question": "‘어려서부터 성경을 알았나니... 구원에 이르는 지혜가 있게 하느니라’ 이 말씀의 출처는?",
        "correct": "디모데후서 3장 15절",
        "distractors": [
            "고린도후서 12장 9절",
            "빌립보서 4장 4절"
        ],
        "hint": "어머니 유니게와 외할머니 로이스에게 어려서부터 성경을 배운 디모데!",
        "explanation": "디모데후서 3장 15절 말씀입니다."
    },

    # --- [빨강보석 4: 다시 오실 예수님 - 재림, 천국, 거처] ---
    {
        "category": "빨강보석 4",
        "question": "‘공중에서 주를 영접하게 하시리니’ 이 말씀이 들어 있는 성경구절은?",
        "correct": "데살로니가전서 4장 17절",
        "distractors": [
            "데살로니가전서 4장 16절",
            "데살로니가전서 5장 17절"
        ],
        "hint": "16절은 호령과 천사장의 소리 강림, 17절은 구름 속으로 끌어올려 공중 영접!",
        "explanation": "살전 4:17 - '...구름 속으로 끌어 올려 공중에서 주를 영접하게 하시리니...'"
    },
    {
        "category": "빨강보석 4",
        "question": "‘요한복음 14장 1-2절’에서 ‘거처’의 의미는 무엇인가요?",
        "correct": "살 집 (천국의 처소)",
        "distractors": [
            "임시 천막",
            "기도하는 제단"
        ],
        "hint": "예수님이 우리를 위하여 하늘나라에 예비하러 가신 곳!",
        "explanation": "거처 = 살 집을 의미합니다."
    },
    {
        "category": "빨강보석 4",
        "question": "요한계시록 21장 3-4절에서 새 하늘과 새 땅에 대해 설명한 내용 중 [틀린] 것은?",
        "correct": "해와 달이 지금보다 10배 더 밝아진다.",
        "distractors": [
            "하나님이 모든 눈물을 닦아 주신다.",
            "다시는 사망이나 애통하는 것이나 아픈 것이 없다."
        ],
        "hint": "천국에는 하나님이 친히 빛이 되시므로 해와 달이 필요 없다고 했어요!",
        "explanation": "계 21:4 눈물을 닦아주시며 사망이나 슬픔, 눈물이 없고 하나님이 친히 빛이 되십니다."
    },

    # --- [초록보석 4 & 맞춤법] ---
    {
        "category": "초록보석 4",
        "question": "‘로마서 6장 23절’ 말씀으로 올바른 것은?",
        "correct": "죄의 삯은 사망이요 하나님의 은사는 그리스도 예수 우리 주 안에 있는 영생이니라",
        "distractors": [
            "모든 사람이 죄를 범하였으매 하나님의 영광에 이르지 못하더니",
            "내가 복음을 부끄러워하지 아니하노니 이 복음은 모든 믿는 자에게 구원을 주시는..."
        ],
        "hint": "죄의 '삯'은 사망, 하나님의 선물은 '영생'!",
        "explanation": "롬 6:23: '죄의 삯은 사망이요 하나님의 은사는 그리스도 예수 우리 주 안에 있는 영생이니라'"
    },
    {
        "category": "맞춤법",
        "question": "다음 중 성경 단어의 맞춤법이 [모두 올바른] 것은?",
        "correct": "레위기, 느헤미야, 하박국, 룻기",
        "distractors": [
            "래위기, 느혜미야, 하박국, 룻기",
            "레위기, 느헤미아, 하바국, 룯기"
        ],
        "hint": "레위기(O), 느'헤'미야(O), 하'박'국(O), '룻'기(O)!",
        "explanation": "맞춤법 단골 함정: 레위기, 느헤미야, 하박국, 룻기, 에스라, 에스겔 등입니다."
    },
    {
        "category": "맞춤법",
        "question": "다음 중 성경 표현의 맞춤법이 올바르게 짝지어진 것은?",
        "correct": "정사를 메었고 / 죄의 삯",
        "distractors": [
            "정사를 매었고 / 죄의 삵",
            "정사를 메었고 / 죄의 삵"
        ],
        "hint": "어깨에 메다(메었고), 일한 대가 삯(삯 - ㄳ받침)!",
        "explanation": "정사를 '메'었고, 죄의 '삯'이 올바른 맞춤법입니다."
    }
]


# 🅱️ 필기/주관식 문제 은행 (총 30문항)
WRITTEN_QUESTION_BANK = [
    # --- [O/X 판정형] ---
    {
        "category": "OX 진위판정",
        "type": "ox",
        "question": "성경책은 모두 66권이며, 구약 성경책은 39권, 신약 성경책은 26권이다. (O 또는 X)",
        "answers": ["X", "x"],
        "hint": "신약 성경책은 27권이에요! (구약 39권 + 신약 27권 = 총 66권)",
        "explanation": "구약 39권, 신약 27권으로 총 66권입니다!"
    },
    {
        "category": "OX 진위판정",
        "type": "ox",
        "question": "모세오경은 창세기, 출애굽기, 레위기, 민수기, 여호수아이다. (O 또는 X)",
        "answers": ["X", "x"],
        "hint": "모세오경의 마지막 책은 '신명기'예요! 여호수아는 역사서입니다.",
        "explanation": "모세오경은 창세기, 출애굽기, 레위기, 민수기, 신명기 5권입니다."
    },
    {
        "category": "OX 진위판정",
        "type": "ox",
        "question": "예수님의 탄생을 알고 동방박사와 헤롯왕은 아기 예수님께 함께 나아가 경배를 드렸습니다. (O 또는 X)",
        "answers": ["X", "x"],
        "hint": "헤롯왕은 아기 예수님을 죽이려 했어요! 동방박사들만 경배했습니다.",
        "explanation": "헤롯은 아기 예수님을 죽이려 했으므로 X입니다!"
    },
    {
        "category": "OX 진위판정",
        "type": "ox",
        "question": "예수님이 십자가에서 숨을 거두셨을 때 지진이 일어나며 로마 백부장은 '이 사람은 진실로 하나님의 아들이다!'라고 고백했다. (O 또는 X)",
        "answers": ["O", "o"],
        "hint": "100명의 군사를 거느린 로마 백부장의 참된 신앙고백이었어요!",
        "explanation": "백부장이 '진실로 하나님의 아들이다'라고 고백한 것이 맞습니다."
    },
    {
        "category": "OX 진위판정",
        "type": "ox",
        "question": "텅 빈 무덤을 보고 베드로와 요한은 집으로 돌아갔고, 마리아도 슬퍼서 곧바로 집으로 돌아갔다. (O 또는 X)",
        "answers": ["X", "x"],
        "hint": "막달라 마리아는 무덤 곁에 혼자 남아 울다가 부활하신 예수님을 만났어요!",
        "explanation": "마리아는 무덤에 남아 부활하신 예수님을 가장 먼저 만났습니다."
    },
    {
        "category": "OX 진위판정",
        "type": "ox",
        "question": "예수님은 사도 요한에게 앞으로 일어날 일을 보여주시고, 반드시 다시 오시겠다고 약속하셨다. (O 또는 X)",
        "answers": ["O", "o"],
        "hint": "요한계시록에서 예수님은 '내가 속히 오리라' 약속하셨어요!",
        "explanation": "예수님께서 반드시 다시 오시겠다고 약속하신 것이 맞습니다."
    },

    # --- [성경 단어의 의미형] ---
    {
        "category": "성경 단어 뜻",
        "type": "short",
        "question": "누가복음 19장 10절 '인자가 온 것은 잃어버린 자를 찾아 구원하려 함이니라'에서 '인자'가 가리키는 분은 누구인가요?",
        "answers": ["예수그리스도", "예수님", "그리스도"],
        "hint": "우리를 위해 십자가를 지신 하나님의 아들이신 분!",
        "explanation": "인자 = 예수 그리스도"
    },
    {
        "category": "성경 단어 뜻",
        "type": "short",
        "question": "누가복음 19장 10절에서 '예수님을 구주로 믿어야 하는 모든 죄인들'을 나타내는 네 글자 단어는?",
        "answers": ["잃어버린 자", "잃어버린자"],
        "hint": "인자가 온 것은 (       )를 찾아 구원하려 함이니라!",
        "explanation": "잃어버린 자 = 예수님을 구주로 믿어야 하는 모든 죄인들"
    },
    {
        "category": "성경 단어 뜻",
        "type": "short",
        "question": "고린도후서 12장 9절에서 '우리가 자격이 없는데도 도와주시고 돌보아주시는 하나님의 사랑'을 뜻하는 두 글자 단어는?",
        "answers": ["은혜"],
        "hint": "\"내 OO가 네게 족하도다!\"",
        "explanation": "은혜 = 우리가 자격이 없는데도 베풀어주시는 하나님의 사랑"
    },
    {
        "category": "성경 단어 뜻",
        "type": "short",
        "question": "이사야 9장 6절에서 '올바르고 참된 말을 해 주는 분'을 나타내는 두 글자 단어는?",
        "answers": ["모사"],
        "hint": "기묘자라, OO라, 전능하신 하나님이라...",
        "explanation": "모사 = 올바르고 참된 말을 해 주는 분"
    },
    {
        "category": "성경 단어 뜻",
        "type": "short",
        "question": "이사야 9장 6절에서 '놀라운 기적을 행하는 분'을 나타내는 세 글자 단어는?",
        "answers": ["기묘자"],
        "hint": "기이하고 묘한 일을 행하시는 분!",
        "explanation": "기묘자 = 놀라운 기적을 행하는 분"
    },
    {
        "category": "성경 단어 뜻",
        "type": "short",
        "question": "데살로니가전서 4장 16절에서 '천사들의 대장'을 나타내는 세 글자 단어는?",
        "answers": ["천사장"],
        "hint": "천사들의 우두머리 대장!",
        "explanation": "천사장 = 천사들의 대장"
    },
    {
        "category": "성경 단어 뜻",
        "type": "short",
        "question": "로마서 5장 8절에서 '보여주다, 증명하다'의 의미를 지닌 두 글자 단어는? (사랑을 OO하셨느니라)",
        "answers": ["확증"],
        "hint": "확실하게 증명하여 보여주셨다는 뜻이에요!",
        "explanation": "확증하다 = 보여주다, 증명하다"
    },
    {
        "category": "성경 단어 뜻",
        "type": "short",
        "question": "사도행전 16장 31절에서 '내가 지은 죄에 대한 벌을 받지 않고 용서받다'를 의미하는 세 글자 단어는?",
        "answers": ["구원받다", "구원"],
        "hint": "너와 네 집이 OO을 받으리라!",
        "explanation": "구원받다 = 지은 죄에 대한 벌을 받지 않고 용서받음"
    },
    {
        "category": "성경 단어 뜻",
        "type": "short",
        "question": "골로새서 4장 2절에서 '기도할 때 하나님의 응답에 주의를 기울이라'는 의미의 네 글자 성경 표현은?",
        "answers": ["깨어 있으라", "깨어있으라"],
        "hint": "기도에 감사함으로 OO OOO!",
        "explanation": "깨어 있으라 = 기도할 때 하나님의 응답에 주의를 기울이라"
    },

    # --- [성경 출처/책이름형] ---
    {
        "category": "성경 출처",
        "type": "short",
        "question": "“감사함으로 그의 문에 들어가며 찬송함으로 그의 궁정에 들어가서…” 이 말씀이 나오는 성경 책 이름은?",
        "answers": ["시편", "시편 100편", "시편100편"],
        "hint": "다윗과 여러 믿음의 사람들이 쓴 찬양의 노래 책이에요!",
        "explanation": "시편 100편 4절 말씀입니다."
    },
    {
        "category": "성경 출처",
        "type": "short",
        "question": "“그가 여기 계시지 않고 그가 말씀 하시던 대로 살아나셨느니라 와서 그가 누우셨던 곳을 보라” 이 말씀의 성경 책 이름은?",
        "answers": ["마태복음", "마태"],
        "hint": "신약성경 맨 첫 번째 복음서예요!",
        "explanation": "마태복음 28장 6절 말씀입니다."
    },
    {
        "category": "성경 출처",
        "type": "short",
        "question": "“주 안에서 항상 기뻐하라 내가 다시 말하노니 기뻐하라” 이 말씀의 성경 책 이름은?",
        "answers": ["빌립보서", "빌립보"],
        "hint": "사도 바울이 옥중에서 기쁨으로 쓴 편지예요!",
        "explanation": "빌립보서 4장 4절 말씀입니다."
    },
    {
        "category": "성경 출처",
        "type": "short",
        "question": "“어려서부터 성경을 알았나니 성경은 능히 너로 하여금... 구원에 이르는 지혜가 있게 하느니라” 이 말씀의 성경 책 이름은?",
        "answers": ["디모데후서", "디모데후서 3장", "디모데후서3장"],
        "hint": "바울이 믿음의 아들 디모데에게 보낸 두 번째 편지예요!",
        "explanation": "디모데후서 3장 15절 말씀입니다."
    },

    # --- [성경 목록 순서 빈칸형] ---
    {
        "category": "성경 목록 순서",
        "type": "short",
        "question": "구약성경 순서 빈칸 채우기: [ 호세아 ➜ (  ?  ) ➜ 아모스 ➜ 오바댜 ] 빈칸에 들어갈 성경 책 이름은?",
        "answers": ["요엘"],
        "hint": "호세아 다음, 아모스 앞! 두 글자 선지서예요.",
        "explanation": "호세아 - 요엘 - 아모스 - 오바댜 순서입니다."
    },
    {
        "category": "성경 목록 순서",
        "type": "short",
        "question": "신약성경 순서 빈칸 채우기: [ 디도서 ➜ (  ?  ) ➜ 히브리서 ➜ 야고보서 ] 빈칸에 들어갈 성경 책 이름은?",
        "answers": ["빌레몬서", "빌레몬"],
        "hint": "디모데전후서, 디도서 다음에 나오는 한 장짜리 편지예요!",
        "explanation": "디도서 - 빌레몬서 - 히브리서 - 야고보서 순서입니다."
    },
    {
        "category": "성경 목록 순서",
        "type": "short",
        "question": "구약성경 순서 빈칸 채우기: [ 에스라 ➜ (   ?   ) ➜ 에스더 ➜ 욥기 ] 빈칸에 들어갈 성경 책 이름은?",
        "answers": ["느헤미야"],
        "hint": "예루살렘 성벽을 무너진 데서 다시 지은 총독의 이름이에요!",
        "explanation": "에스라 - 느헤미야 - 에스더 - 욥기 순서입니다."
    },

    # --- [성경 실화 인물/지명형] ---
    {
        "category": "성경 실화",
        "type": "short",
        "question": "삭개오는 직업이 (  ?  )장이었고 키가 작았으나, 예수님을 만나 재산의 절반을 가난한 자에게 주기로 결단했습니다.",
        "answers": ["세리", "세리장"],
        "hint": "세금을 거두던 로마의 관리 우두머리였어요!",
        "explanation": "삭개오는 여리고의 부자 세리장이었습니다."
    },
    {
        "category": "성경 실화",
        "type": "short",
        "question": "교회 성도들이 밤새 간절히 기도했을 때, 천사가 나타나 쇠사슬을 풀고 감옥에서 구출해 준 사도는 누구인가요?",
        "answers": ["베드로", "베드로사도"],
        "hint": "예수님의 수제자이자 초대 예루살렘 교회의 지도자예요!",
        "explanation": "사도행전 12장에서 천사가 베드로를 구출했습니다."
    },
    {
        "category": "성경 실화",
        "type": "short",
        "question": "사도 요한이 복음을 전했다는 이유로 로마 감옥에 갇혀 요한계시록을 기록했던 외딴 섬의 이름은?",
        "answers": ["밧모섬", "밧모"],
        "hint": "두 글자 섬 이름이에요! 'ㅂㅁ'섬",
        "explanation": "요한은 밧모섬에 유배되어 계시록을 기록했습니다."
    },
    {
        "category": "성경 실화",
        "type": "short",
        "question": "욥바 마을에서 가난한 이웃에게 옷을 지어주던 여제자 다비다의 또 다른 헬라어 이름은 무엇인가요?",
        "answers": ["도르가"],
        "hint": "세 글자! 'ㄷㄹㄱ'",
        "explanation": "다비다의 또 다른 이름은 도르가입니다."
    },

    # --- [구절 빈칸 완성형] ---
    {
        "category": "구절 빈칸 완성",
        "type": "short",
        "question": "로마서 1장 16절 완성하기: \"내가 (  ?  )을 부끄러워하지 아니하노니 이 (  ?  )은 모든 믿는 자에게 구원을 주시는 하나님의 능력이 됨이라\"",
        "answers": ["복음"],
        "hint": "예수 그리스도의 기쁜 소식을 뜻하는 두 글자 단어예요!",
        "explanation": "로마서 1:16 - '내가 복음을 부끄러워하지 아니하노니 이 복음은...'"
    },
    {
        "category": "구절 빈칸 완성",
        "type": "short",
        "question": "사도행전 1장 8절 완성하기: \"오직 (  ?  )이 너희에게 임하시면 너희가 권능을 받고... 내 증인이 되리라\"",
        "answers": ["성령", "성령님"],
        "hint": "하나님의 거룩한 영을 뜻하는 두 글자 단어예요!",
        "explanation": "행 1:8 - '오직 성령이 너희에게 임하시면...'"
    },
    {
        "category": "구절 빈칸 완성",
        "type": "short",
        "question": "동방박사들이 아기 예수님께 경배하며 드린 가장 귀한 3가지 예물은 [ 황금, (  ?  ), 몰약 ]입니다. 빈칸에 들어갈 예물은?",
        "answers": ["유향"],
        "hint": "황금, OO, 몰약!",
        "explanation": "황금, 유향, 몰약을 드렸습니다."
    },

    # --- [맞춤법 주관식 받아쓰기] ---
    {
        "category": "맞춤법 교정",
        "type": "short",
        "question": "틀린 맞춤법 고치기: [ 래위기 ]의 올바른 성경 책 이름을 바르게 쓰세요.",
        "answers": ["레위기"],
        "hint": "'래'가 아니라 '레'예요!",
        "explanation": "레위기가 올바른 표기입니다."
    },
    {
        "category": "맞춤법 교정",
        "type": "short",
        "question": "틀린 맞춤법 고치기: [ 죄의 삵 ]에서 '일한 대가로 받는 몫'을 뜻하는 올바른 단어 받침으로 고쳐 쓰세요.",
        "answers": ["삯", "죄의 삯", "죄의삯"],
        "hint": "ㄹㄱ 받침이 아니라 ㄱㅅ(ㄳ) 받침이에요!",
        "explanation": "죄의 삯(ㄳ 받침)이 올바른 맞춤법입니다."
    },
    {
        "category": "맞춤법 교정",
        "type": "short",
        "question": "틀린 맞춤법 고치기: [ 느혜미야 ]의 올바른 성경 책 이름을 바르게 쓰세요.",
        "answers": ["느헤미야"],
        "hint": "'혜'가 아니라 '헤'예요!",
        "explanation": "느헤미야가 올바른 표기입니다."
    },
    {
        "category": "맞춤법 교정",
        "type": "short",
        "question": "틀린 맞춤법 고치기: 이사야 9장 6절 [ 그의 어깨에는 정사를 매었고 ]에서 틀린 글자 하나를 바르게 고쳐 쓰세요. (ㅁ 받침 모음)",
        "answers": ["메었고", "정사를 메었고", "정사를메었고"],
        "hint": "짐을 어깨에 메다할 때는 '매'가 아니라 '메'예요!",
        "explanation": "정사를 '메었고'가 올바른 성경 표기입니다."
    }
]

# 10단계 스테이지 테마 & 몬스터 템플릿
STAGE_THEMES = [
    {"level": 1, "zone": "불티단 비밀기지 (승급과정)", "monster": "깜빡이 도깨비", "armor": "진리의 허리띠", "gem": "구원의 루비"},
    {"level": 2, "zone": "말씀의 도서관 (성경 66권)", "monster": "책장 뒤죽박죽 골렘", "armor": "의의 흉배(가슴 갑옷)", "gem": "지혜의 사파이어"},
    {"level": 3, "zone": "베들레헴 별빛 사막 (빨강보석 1)", "monster": "사막의 그림자 전갈", "armor": "평안의 복음 신발", "gem": "성탄의 에메랄드"},
    {"level": 4, "zone": "사마리아 은혜의 호수 (초록보석 1)", "monster": "투덜이 늪지 괴물", "armor": "감사의 방패띠", "gem": "생명의 토파즈"},
    {"level": 5, "zone": "골고다 언덕 & 빈 무덤 (빨강보석 2)", "monster": "어둠의 골고다 기사", "armor": "믿음의 대방패", "gem": "부활의 오팔"},
    {"level": 6, "zone": "광야의 전도 마차 길 (초록보석 2)", "monster": "광야의 모래폭풍 마왕", "armor": "전도의 날개망토", "gem": "선교의 페리도트"},
    {"level": 7, "zone": "욥바 마을 & 예루살렘 감옥 (빨강보석 3)", "monster": "쇠사슬 감옥 간수장", "armor": "사랑과 기도의 건틀릿", "gem": "소망의 가넷"},
    {"level": 8, "zone": "빌립보 감옥 & 유라굴로 바다 (초록보석 3)", "monster": "성난 파도 유라굴로", "armor": "기쁨의 황금갑옷", "gem": "찬양의 아쿠아마린"},
    {"level": 9, "zone": "밧모섬 천국의 보좌 (빨강보석 4)", "monster": "영원한 밤의 드래곤", "armor": "구원의 투구", "gem": "영광의 자수정"},
    {"level": 10, "zone": "최후의 시험의 탑 (초록보석 4 & 총정리)", "monster": "오답의 군주 '틀림마왕' (최종보스)", "armor": "성령의 검 (말씀의 검)", "gem": "승리의 황금 면류관"}
]


# ==============================================================================
# 2. 플레이어 캐릭터 클래스
# ==============================================================================
class Hero:
    def __init__(self, name="스카이스토머"):
        self.name = name
        self.level = 1
        self.max_hp = 100
        self.hp = 100
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.armors = []
        self.gems = []

    def print_status(self):
        print("\n" + "="*60)
        hearts = "❤️ " * (self.hp // 20) + "🖤 " * max(0, (self.max_hp - self.hp) // 20)
        print(f" 🛡️  [빛의 용사] {self.name}  |  레벨: Lv.{self.level} (스카이스토머)")
        print(f" 💖  체력(HP): {self.hp}/{self.max_hp}  [{hearts.strip()}]   |  점수: {self.score}점")
        print(f" 🔥  현재 콤보: {self.combo}연속 정답! (최고: {self.max_combo}연속)")
        gem_str = ", ".join(self.gems) if self.gems else "아직 없음"
        print(f" 💎  모은 보석 ({len(self.gems)}/10): {gem_str}")
        print("="*60 + "\n")

    def hit(self, damage=20):
        self.hp = max(0, self.hp - damage)
        self.combo = 0
        print(f"💥 앗! 몬스터의 암흑 공격! HP -{damage}! (남은 HP: {self.hp})")
        if self.hp <= 0:
            print("\n🕊️ \"여호와 그가 네 앞에서 가시며 너와 함께 하사 너를 떠나지 아니하시리라!\" (신명기 31:8)")
            print("✨ 천사의 기도로 용사님이 다시 일어났습니다! HP가 60 회복됩니다!")
            self.hp = 60

    def add_correct(self, base_score=100):
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo
        bonus = (self.combo - 1) * 20
        total_gain = base_score + bonus
        self.score += total_gain
        combo_msg = f" 🔥 {self.combo}연속 콤보 보너스 +{bonus}점!" if self.combo > 1 else ""
        print(f"🎯 정답입니다! +{total_gain}점 획득!{combo_msg}")

    def level_up(self, armor_name, gem_name):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.armors.append(armor_name)
        self.gems.append(gem_name)
        print("\n" + "★"*60)
        print(f"🎉 빰빠카빰! 스테이지 클리어! 레벨 업! ➜ [Lv.{self.level}]")
        print(f"🎁 전신갑주 파츠 장착: 【 {armor_name} 】 !!")
        print(f"💎 말씀의 보석 획득: 【 {gem_name} 】 !!")
        print(f"💖 HP 완전 회복 & 최대 체력 {self.max_hp}로 증가!")
        print("★"*60 + "\n")


# ==============================================================================
# 3. 답변 유연성 판정 (2학년 눈높이 정규화 함수)
# ==============================================================================
def normalize_answer(text):
    text = str(text).strip().lower()
    text = re.sub(r'[\s\.,\-\?!~_\"\'\(\)]', '', text)
    return text

def check_written_answer(user_input, correct_answers):
    norm_user = normalize_answer(user_input)
    if not norm_user:
        return False
    for ans in correct_answers:
        norm_ans = normalize_answer(ans)
        if norm_user == norm_ans:
            return True
        if len(norm_ans) >= 2 and norm_ans in norm_user:
            return True
        if len(norm_user) >= 2 and norm_user in norm_ans:
            return True
    return False


# ==============================================================================
# 4. 랜덤 문제 추출 및 배틀 루틴
# ==============================================================================
def play_mc_question(q_data, hero, stage_num, theme):
    """객관식 문제를 보기 셔플하여 출제"""
    print("\n" + "-"*60)
    print(f"🚩 [STAGE {stage_num}/10] {theme['zone']}")
    print(f"👾 몬스터 등장: [{theme['monster']}]")
    print(f"💬 {theme['monster']}: \"말씀의 검을 받아칠 준비가 되었느냐!\"")
    print("-" * 60)
    print(f"📜 [객관식 성경 퀴즈] ({q_data['category']}):")
    print(f"👉 {q_data['question']}\n")

    # 보기 셔플 (정답 위치를 1, 2, 3 중 무작위 배치)
    choices = [q_data['correct']] + q_data['distractors']
    random.shuffle(choices)
    correct_idx = choices.index(q_data['correct']) + 1

    for i, choice in enumerate(choices, 1):
        print(f"  [{i}] {choice}")

    while True:
        try:
            user_input = input("\n👉 정답 번호를 골라주세요 (1, 2, 3): ").strip()
            if user_input not in ["1", "2", "3"]:
                print("⚠️ 숫자 1, 2, 3 중에서 하나를 입력해주세요!")
                continue

            chosen = int(user_input)
            if chosen == correct_idx:
                print("\n⚡ [크리티컬 히트!! 말씀의 일격 발동!] ⚡")
                print(f"💥 슈우우욱! {theme['monster']} 소멸!! 💥")
                print(f"📖 [말씀 지혜]: {q_data['explanation']}")
                hero.add_correct(100)
                break
            else:
                hero.hit(20)
                print(f"💡 [천사의 힌트]: {q_data['hint']}")
                print("💪 다시 힘을 내서 풀어보세요!")
        except (KeyboardInterrupt, EOFError):
            print("\n게임을 종료합니다.")
            sys.exit(0)


def play_written_question(q_data, hero, stage_num, theme):
    """주관식 필기시험 문제를 출제하고 유연 채점"""
    print("\n" + "-"*60)
    print(f"🚩 [STAGE {stage_num}/10] {theme['zone']}")
    print(f"👾 몬스터 등장: [{theme['monster']}]")
    print(f"💬 {theme['monster']}: \"키보드로 직접 바르게 쓸 수 있을까?!\"")
    print("-" * 60)
    print(f"📜 [주관식 필기 미션] ({q_data['category']}):")
    print(f"👉 {q_data['question']}\n")

    if q_data['type'] == 'ox':
        print("  ※ 정답을 O 또는 X 로 입력하세요.")
    else:
        print("  ※ 정답 단어나 구절을 직접 입력하세요.")

    while True:
        try:
            user_input = input("\n✍️ 용사의 답 입력: ").strip()
            if not user_input:
                print("⚠️ 답을 입력해주세요!")
                continue

            if check_written_answer(user_input, q_data['answers']):
                print("\n✨ ⚡ [말씀 완성의 검! 강력한 카운터 어택!] ⚡ ✨")
                print(f"💥 번쩍! {theme['monster']} 퇴치 완료!! 💥")
                print(f"📖 [정답 확인]: {q_data['answers'][0]}")
                print(f"📖 [말씀 지혜]: {q_data['explanation']}")
                hero.add_correct(120)
                break
            else:
                hero.hit(20)
                print(f"💡 [천사의 힌트]: {q_data['hint']}")
                print("💪 다시 한 번 생각하고 입력해보세요!")
        except (KeyboardInterrupt, EOFError):
            print("\n게임을 종료합니다.")
            sys.exit(0)


# ==============================================================================
# 5. 게임 모드별 메인 컨트롤러
# ==============================================================================
def start_game():
    print("\n" + "⚔️ "*25)
    print("      🌟 [스카이스토머 AWANA SPARKS 3] 전 범위 랜덤 RPG 🌟")
    print("               << 문제 은행 무한 던전 v3.0 >>")
    print("⚔️ "*25 + "\n")
    print("초등학교 2학년 용사님, 환영합니다!")
    print(f"대규모 문제 은행 (객관식 {len(MC_QUESTION_BANK)}문항 + 주관식 {len(WRITTEN_QUESTION_BANK)}문항 = 총 {len(MC_QUESTION_BANK)+len(WRITTEN_QUESTION_BANK)}문항)이 탑재되었습니다.")
    print("플레이할 때마다 전체 범위에서 새로운 문제가 무작위로 추출됩니다!\n")

    user_name = input("플레이할 용사님의 이름을 입력하세요 (엔터 시 '번개스토머'): ").strip()
    if not user_name:
        user_name = "번개스토머"

    hero = Hero(user_name)

    print("\n" + "═"*50)
    print("🎮 [원하는 도전 모드를 선택하세요]")
    print(f"  [1] 객관식 랜덤 챔피언십 (문제은행 {len(MC_QUESTION_BANK)}문항 중 10문제 무작위)")
    print(f"  [2] 필기시험 랜덤 마스터 (문제은행 {len(WRITTEN_QUESTION_BANK)}문항 중 10문제 무작위)")
    print(f"  [3] 종합 어드벤처 레이드 (객관식 5 + 주관식 5 무작위 믹스 10단계)")
    print("═"*50)

    mode = input("\n👉 모드 번호를 선택하세요 (1, 2, 3): ").strip()
    if mode not in ["1", "2", "3"]:
        mode = "1"

    # 문제 은행에서 랜덤 10문제 추출 (중복 없이 sample)
    if mode == "1":
        selected_questions = random.sample(MC_QUESTION_BANK, 10)
        q_types = ["mc"] * 10
        mode_title = "객관식 랜덤 챔피언십"
    elif mode == "2":
        selected_questions = random.sample(WRITTEN_QUESTION_BANK, 10)
        q_types = ["written"] * 10
        mode_title = "필기시험 주관식 마스터"
    else:
        # 모드 3: 객관식 5개 + 주관식 5개를 골라 골고루 섞음
        mc_sample = random.sample(MC_QUESTION_BANK, 5)
        wr_sample = random.sample(WRITTEN_QUESTION_BANK, 5)
        combined = []
        for m, w in zip(mc_sample, wr_sample):
            combined.append((m, "mc"))
            combined.append((w, "written"))
        random.shuffle(combined)
        selected_questions = [item[0] for item in combined]
        q_types = [item[1] for item in combined]
        mode_title = "종합 어드벤처 레이드 (하이브리드)"

    print(f"\n🚀 【{mode_title}】 모험을 시작합니다! 10단계 관문을 돌파하세요!\n")
    time.sleep(1)

    # 10단계 진행
    for step in range(10):
        theme = STAGE_THEMES[step]
        hero.print_status()
        q_data = selected_questions[step]
        q_type = q_types[step]

        if q_type == "mc":
            play_mc_question(q_data, hero, step + 1, theme)
        else:
            play_written_question(q_data, hero, step + 1, theme)

        # 레벨업 및 보상 지급
        hero.level_up(theme['armor'], theme['gem'])
        time.sleep(0.5)

    # 최종 결과 발표
    print("\n" + "🎉 "*25)
    print(f"       🏆 축하합니다!! {hero.name} 용사님 10단계 완벽 제패!! 🏆")
    print("🎉 "*25)
    hero.print_status()
    print(f"""
    🌟 [빛의 전신갑주 6종 풀세트 & 10대 보석 완성!]
       • 머리: 구원의 투구
       • 가슴: 의의 흉배
       • 허리: 진리의 허리띠
       • 손: 사랑과 기도의 건틀릿
       • 발: 평안의 복음 신발
       • 무기: 성령의 검 (하나님의 말씀)
       • 방어: 믿음의 대방패

    🏆 최종 획득 점수: {hero.score}점
    🔥 최고 연속 정답: {hero.max_combo}연속 콤보!

    📖 "어려서부터 성경을 알았나니 성경은 능히 너로 하여금
        그리스도 예수 안에 있는 믿음으로 말미암아
        구원에 이르는 지혜가 있게 하느니라" (디모데후서 3장 15절)

    성경퀴즈대회 금메달은 바로 용사님의 것입니다! 🥇
    게임을 다시 실행할 때마다 문제 은행에서 또 새로운 문제가 나옵니다! 🚀
    """)

if __name__ == "__main__":
    start_game()
