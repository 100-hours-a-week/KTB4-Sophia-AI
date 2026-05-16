import argparse
import json
import os
from datetime import datetime

# python care.py -h 입력했을 때 나오는 메시지. 이 프로그램 전체의 이름
parser = argparse.ArgumentParser(description="TIA (Today I Ate) CLI")

# 가장 먼저 이름 입력 필수
parser.add_argument("name", help="사용자 이름 입력")

# 프로그램에 하위 명령어 등록하는 로직을 subparsers에 저장
subparsers = parser.add_subparsers(dest="command")

eat_parser = subparsers.add_parser("eat", help="식사 메뉴 적기")
water_parser = subparsers.add_parser("water", help="물 몇 잔 마셨는지 적기")
coffee_parser = subparsers.add_parser("coffee", help="커피 몇 잔 마셨는지 적기")

# --가 없이 명령어만 적으면 필수 입력 항목
eat_parser.add_argument("food", help="먹은 음식 이름")
# --가 붙으면 옵션 입력. 시간을 입력해도 되고 안 해도 됨.
eat_parser.add_argument("--time", default=None, help="먹은 시간")

water_parser.add_argument("cups", type=int, help="물 몇 잔 마셨는지 적기(숫자만 입력)")

coffee_parser.add_argument("cups", type=int, help="커피 몇 잔 마셨는지 적기(숫자만 입력)")

# 명령 입력 후 안내 메시지 함수
def handle_eat(username, food_name, food_time, data) :
    # 사용자가 먹은 시간 입력 안 하면 현재 시간으로 기록
    if food_time == None :
        # 현재 시간을 시:분 형태로 저장
        food_time = datetime.now().strftime("%H시 %M분")
    print(f"{username}님이 {food_time}에 {food_name}을(를) 먹었습니다.")
    # 먹은 음식, 시간을 하나의 딕셔너리로 만들기
    new_meal = {
        "food" : food_name,
        "time" : food_time
    }
    # data 안에 meals 리스트에 음식 이름과 시간 저장
    data["meals"].append(new_meal)
    # json에 저장하기
    save_data(username, data)

def handle_water(username, water_cups, data) :    
    print(f"{username}님이 물을 {water_cups}잔 마셨습니다.")
    # data 안에 water 값에 더하기
    data["water"] += water_cups
    # 저장하기
    save_data(username, data)

def handle_coffee(username, coffee_cups, data) :    
    print(f"{username}님이 커피를 {coffee_cups}잔 마셨습니다.")
    # data 안에 coffee 값에 더하기
    data["coffee"] += coffee_cups
    # 저장하기
    save_data(username, data)
    # 커피 1잔당 물 2잔 마셔야 함
    if data["water"] < data["coffee"] * 2 :
        print(f"커피를 많이 마셨어요. {data['coffee']*2 - data['water']}잔의 물을 더 마셔주세요.")

def save_data(username, data) :
    filename = f"{username}_tia.json"
    with open(filename, "w", encoding="utf-8") as f:
        # 떠돌아다니는 데이터를 json에 넣음
        # data 안의 정보를 f라는 파일에 저장, 한글 깨지지 않게하고, 4번 들여써라
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data(username) :
    # json 파일명은 {username}_tia.json
    filename = f"{username}_tia.json"

    # 현재 디렉토리에 json 파일이 있다면 열기
    if os.path.exists(filename) : 
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    else : # json 파일이 없다면 새로 만들기
        data = { # 음식은 dict, 물과 커피는 int로 저장
            "username" : username,
            "meals" : [],
            "water" : 0,
            "coffee" : 0
        }
    return data

# 사용자가 터미널에 친 글자를 읽어서 args에 저장
args = parser.parse_args()

# 사용자가 터미널에 명령어를 입력했다면
if args.command :
    data = load_data(args.name)

if args.command == "eat" :
    handle_eat(args.name, args.food, args.time, data)
elif args.command == "water" :
    handle_water(args.name, args.cups, data)
elif args.command == "coffee" :
    handle_coffee(args.name, args.cups, data)