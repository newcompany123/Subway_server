import random


# Recipe Name Pattern a
from recipes.models import Recipe

recipe_name_a_1 = [

    # Rule
    # - 주어 위치 X

    # 시간
    '퇴근하고',
    '퇴근길에',
    '출근길에',
    '새벽녘에',
    '노을 질 때',
    '동이 틀 때',
    '아침 일찍',
    '점심시간에',
    '쉬는 시간에',

    # 장소
    '학교에서',
    '회사에서',
    '옥상에서',
    '지하실에서',
    '벤치에서',
    '공원에서',
    '야구장에서',
    '피시방에서',
    '당구장에서',
    '서울역에서',
    '부산역에서',
    '해운대에서',
    '공항에서',
    '63빌딩에서',
    '백두산에서',
    '한라산에서',
    '지리산에서',
    '개마고원에서',
    '남산에서',
    '평양에서',
    '개성에서',
    '뉴욕에서',
    '워싱턴에서',
    '도쿄에서',
    '차이나타운에서',
    '홋카이도에서',
    '모스크바에서',
    '시드니에서',
    '맥도날드에서',

    # 감정
    '우울할 때',
    '우울한 날',
    '사랑하고 싶은 날',
    '괴로울 때',
    '괴로운 날',
    '힘들 때',
    '힘든 날',
    '그리움에 사무치는 날',
    '감정이 복받칠 때',
    '화나는 날',

    # 건강
    '피곤할 때',
    '피곤한 날',
    '머리 아플 때',
    '머리 아픈 날',
    '체력이 방전된 날',
    '미치도록 배가 고픈 날',

    # 연애
    '고백하는 날',
    '고백한 날',
    '고백받은 날',
    '헤어진 날',
    '헤어지는 날',
    '싸운 날',
    '다툰 날',
    '삐진 날',

    # 날씨
    '비 오는 날',
    '비 내리는 날',
    '바람 부는 날',
    '바람이 불 때',
    '벼락 치는 날',
    '벼락이 치면',
    '태풍이 상륙한 날',
    '태풍이 상륙하면',
    '폭설이 내린 날',
    '폭설이 내리면',
    '첫눈이 내린 날',
    '첫눈이 내리면',
    '안개 낀 날',
    '안개 낄 때',
    '황사 낀 날',
    '미세먼지가 심한 날',

    # 사건
    '운수 좋은 날',
    '퇴사하는 날',
    '퇴사한 날',
    '입사하는 날',
    '입사한 날',
    '입대하는 날',
    '행군하는 날',
    '수능 보는 날',
    '수능 본 날',
    '졸업하는 날',
    '졸업 날',
    '면접 보는 날',
    '보너스 받은 날',
    '팀플하는 날',
    '시험 끝난 날',
    '시험 망친 날',
    '수업 빠진 날',
    '밤새고 출근한 날',
    '밤샌 다음 날',
    '채용 비리로 입사 떨어진 날',

    # 업무
    '코딩하는 날',
    '출시하는 날',
    '발표하는 날',
    '외근하는 날',
    '반차 쓰는 날',
    '휴가내는 날',

    # 행동
    '티비 보면서',
    '게임하면서',
    '다이어트할 때',
    '운동할 때',
]

recipe_name_a_2 = [

    # 건강
    '먹기 좋은',
    '몸에 좋은',
    '맛나는',
    '다이어트 때려치고 싶게하는',

    # 사람
    '첫사랑과 먹고 싶은',
    '옛 연인과 먹고 싶은',
    '부모님과 먹고 싶은',
    '엄마랑 먹고 싶은',

    # 기억
    '고향 생각나게 하는',

    # 행동
    '먹고 싶은',
    '몰래 먹고 싶은',
    '혼자 먹고 싶은',

    # 재미
    '잃어버린',
    '땅에 떨궈버린',
    '5분 안에 먹어야하는',
    '5분 안에 먹을 수 있는',
    '5분 만에 사라져버린',

    # 속담
    '둘이 먹다 하나가 죽어도 모르는',
    '둘이 먹다 하나가 배탈 나도 모르는',
    '둘이 먹다 하나가 체해도 모르는',

    # 데코
    '김치랑 먹고 싶은',
    '케찹 발라먹고 싶은',
]


# Recipe Name Pattern b

recipe_name_b_1 = [

    # 영화
    '타노스가',
    '아이언맨이',
    '닥터스트레인지가',
    '헐크가',
    '스파이더맨이',
    '블랙팬서가',
    '앤트맨이',
    '톰 크루즈가',
    '슈퍼맨이',
    '배트맨이',
    '조커가',
    '원더우먼이',
    '아쿠아맨이',

    # 배우
    '수지가',
    '아이유가',
    '박보영이',

    # 가수
    '블랙핑크가',
    '블랙핑크 지수가',
    'BTS가',

    # 방송인
    '유시민이',
    '김제동이',
    '김구라가',

    # 정치인
    '문재인이',
    '김정은이',
    '트럼프가',
    '시진핑이',
    '푸틴이',
    '아베가',
    '보건복지부장관이',
]

recipe_name_b_2 = [

    # 홍보
    '강추하는',
    '선전하는',
    '홍보하는',
    '협찬하는',

    # 맛
    '세계 최고의 맛이라 극찬한',
    '세계 최고의 맛이라 평한',
    '감탄사를 연발했던',

    # 바람
    '먹어봤으면 하는',
    '먹었다고 소문난',

    # 재미
    '먹다가 남긴',
    '못 먹겠다고 한',
    '몰래 먹는',
    '먹다가 들킨',
    '두 개나 먹은',
    '절대 포기할 수 없다는',
    '너무 많이 먹어 질려버린',

    # 행동
    '집에 싸 들고 간',
    '소리내며 먹은',
    '한입에 삼켜버린',
]


def create_random_num(list):
    random_num = random.randint(0, len(list)-1)

    # print(list)
    # print(len(list))
    # print(random_num)

    return random_num


def create_random_sentence():
    dice = ['a', 'b']
    roll = random.choice(dice)
    return roll


def create_recipe_name_choice():

    recipe_name_choices_list = []
    while len(recipe_name_choices_list) < 5:
        sentence_pattern = create_random_sentence()
        first_half_list = 'recipe_name_' + sentence_pattern + '_1'
        first_half_sentence = eval(first_half_list)[create_random_num(eval(first_half_list))]

        second_half_list = 'recipe_name_' + sentence_pattern + '_2'
        second_half_sentence = eval(second_half_list)[create_random_num(eval(second_half_list))]

        # print(f'{first_half_sentence} {second_half_sentence}')
        complete_sentence = first_half_sentence + ' ' + second_half_sentence

        # 2018.11.11
        # recipe_name validation added
        if not Recipe.objects.filter(name=complete_sentence) and complete_sentence not in recipe_name_choices_list:
            # print(complete_sentence)
            recipe_name_choices_list.append(complete_sentence)

    return recipe_name_choices_list
