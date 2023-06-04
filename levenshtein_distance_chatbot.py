
import csv

def levenshtein_distance(s1, s2):
    m = len(s1)
    n = len(s2)
    
     # dp는 레벤슈타인 거리를 저장하기 위한 DP(Dynamic Programming) 테이블
     # dp 테이블 초기화
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # 레벤슈타인 거리 계산
    # 이중 반복문을 통해 s1의 문자와 s2의 문자를 한 글자씩 비교
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # 문자가 같으면 대각선 위의 값으로 갱신
            else:
                dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]) + 1  # 삽입, 삭제, 치환 중 최소값 + 1로 갱신

    # 최종 레벤슈타인 거리 반환
    return dp[m][n]

def load_qa_from_csv(file_path):
    qa_pairs = [] # 질문과 대응하는 답변을 저장할 리스트
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:  # csv는 질문,답변,레이블로 있고 우리는 질문,답변만 사용
                question = row[0]
                answer = row[1]
                qa_pairs.append((question, answer))

    return qa_pairs

def get_most_similar_response(user_input, qa_pairs):
    min_distance = float('inf') # 최소 거리를 무한대로 초기화
    most_similar_response = None

    for question, answer in qa_pairs:
        distance = levenshtein_distance(user_input, question)
        if distance < min_distance:
            min_distance = distance # 최소 거리 갱신
            most_similar_response = answer # 가장 유사한 답변 갱신

    return most_similar_response

#  CSV 파일 경로를 지정
file_path = 'ChatbotData.csv'
qa_pairs = load_qa_from_csv(file_path)

# 사용자 입력과 가장 유사한 응답 찾기
# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복
while True:
    user_input = input('You: ')
    if user_input.lower() == '종료':
        break
    most_similar_response = get_most_similar_response(user_input, qa_pairs)
    print('Chatbot:', most_similar_response)