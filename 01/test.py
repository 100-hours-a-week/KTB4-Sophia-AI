import argparse

def train(args):
    print(f"Training with data={args.data}, epochs={args.epochs}")

# python test.py -h 입력했을 때 나오는 메시지. 이 프로그램 전체의 이름
parser = argparse.ArgumentParser(description="ML Workflow CLI")

# 프로그램에 하위 명령어 등록하는 로직을 subparsers에 저장
subparsers = parser.add_subparsers(dest="command")

# train: 사용자가 터미널에 실제로 입력할 하위 명령어 이름, help: train 명령어에 대한 설명
# 터미널의 {}안에 들어있는 단어들은 사용자가 터미널에 입력 가능한 명령어들
train_parser = subparsers.add_parser("train", help="모델 학습")

# train 뒤에 올 명령어는 --data, --epochs
# required=True는 train을 하기 위해 --data 경로 입력이 반드시 필요하다는 뜻
train_parser.add_argument("--data", required=True, help="학습 데이터 경로")
train_parser.add_argument("--epochs", type=int, default=10, help="훈련 횟수")

# 사용자가 터미널에 train이라고 치면 맨 위에 있는 def train(args) 함수를
# 실행하라고 컴퓨터에게 연결
train_parser.set_defaults(func=train)

# 사용자가 터미널에 친 글자를 읽어서 args에 저장
args = parser.parse_args()

# 사용자가 터미널에 명령어를 입력했다면
if args.command:
    # args에 저장된 함수를 실행
    args.func(args)