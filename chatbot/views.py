from django.shortcuts import render
import json, os
from transformers import pipeline
import random
from django.shortcuts import redirect
from sentence_transformers import SentenceTransformer, util
import torch

# 모델 경로
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "./sbert_model/sbert_bible_emotion_model")  # 압축 해제한 위치로 맞추기

# 모델 로드
model = SentenceTransformer(model_path)

# 키워드 목록 (예: 200개 리스트)
candidate_labels = [
        "감사", "거룩함", "건강 문제", "결단", "결혼", "고난", "고독감", "고통", "고통스러움", "공포",
        "과로", "관계 갈등", "구원", "군중 속 외로움", "기다림", "기다림의 훈련", "기도", "기도 응답",
        "기쁨", "기름부음", "기술 발전에 대한 두려움", "기후 위기", "기회", "긍휼", "긴장", "낙담",
        "낙심", "노후 걱정", "다툼", "따돌림", "도움 필요", "도박", "돌봄", "두려움", "마음의 상처",
        "말씀", "말씀 목마름", "무기력", "무력감", "믿음", "믿음 약화", "미래 불확실성", "미래 사회 걱정",
        "부당함", "부부 갈등", "분노", "불공정함", "불만", "불안", "불신", "불의", "불쾌감", "비전 상실",
        "사회적 불안", "사랑", "사명", "사역", "사역자 피로", "상실", "상처", "성경 읽기 어려움", "성공",
        "성령", "성실", "성숙", "성화", "소그룹 스트레스", "소망", "소외감", "소원", "소명", "수용",
        "수치심", "순종", "시기", "시험", "신뢰", "신앙 회의", "신앙적 침체", "심리적 외상", "싸움",
        "악의", "안정감", "억울함", "엄청난 변화", "업무 과중", "어둠", "영광", "영적 무기력",
        "영적 침체", "영적 전쟁", "예배", "예배 회복", "예언", "예수님과의 관계", "우울", "우정",
        "운명", "웃음", "위로", "위축감", "응답", "의심", "의지", "이직 고민", "이혼", "인공지능 불안",
        "인도하심", "인내", "자녀 걱정", "자녀 양육", "자살 충동", "자신감", "자존감", "자책감", "자해 충동",
        "자비", "재난", "절망", "정치적 갈등", "정죄감", "죄", "죄책감", "조바심", "존중", "좌절",
        "주저함", "중독", "중보", "지구 환경 걱정", "지침", "직장 내 스트레스", "직장 문제", "질병",
        "질투", "진로 고민", "자아 혼란", "창피함", "찬란함", "찬양", "참회", "취업 고민", "치유",
        "침묵", "쾌락", "타락", "탄식", "탕자", "폭력", "피곤", "피해", "필요", "하나님의 뜻",
        "하나님의 음성", "한숨", "학업 스트레스", "한계", "한숨", "허무함", "헌신", "혜택", "혐오",
        "혼란", "혼자", "회개", "회복", "회복력", "회의감", "훈련", "희망"
    ]  # 기존 JSON 등에서 로딩하거나 직접 작성

# 키워드 임베딩
keyword_embeddings = model.encode(candidate_labels, convert_to_tensor=True)


def detect_topic(text, top_k=3):
    query_embedding = model.encode(text, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, keyword_embeddings)[0]
    top_results = torch.topk(cosine_scores, k=top_k)
    return [candidate_labels[i] for i in top_results.indices]


with open(os.path.join(os.path.dirname(__file__), "../tagged_bible_keywords_200_flat.json"), encoding="utf-8") as f:
    data = json.load(f)

def chatbot_view(request):
    result = []
    user_input = ""
    topics = []

    if request.method == "POST":
        if request.POST.get("clear"):
            request.session["chat_history"] = []
            return redirect(request.path)

        user_input = request.POST.get("message")
        topics = detect_topic(user_input, top_k=3)

        # 첫 번째 주제로 말씀 검색
        topic = topics[0] if topics else ""
        if topic:
            matched = [v for v in data if topic in v["topics"]]
            result = random.sample(matched, k=min(5, len(matched)))

        # 세션에 대화 기록 저장
        request.session.setdefault("chat_history", [])
        request.session["chat_history"].append({
            "user_input": user_input,
            "topics": topics,
            "result": result
        })
        request.session.modified = True

    chat_history = request.session.get("chat_history", [])

    return render(request, "chatbot/chat.html", {
        "result": result,
        "user_input": user_input,
        "topics": topics,
        "chat_history": chat_history
    })