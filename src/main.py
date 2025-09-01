import datetime
import math

# 주차 타워 초기화 (빈자리는 "[]", 주차된 자리는 "[X]")
parking_floors, parking_clols = 10, 10
parking_tower = [["[]" for _ in range(parking_clols)] for _ in range(parking_floors)]

# 정기권 차량 목록 (차량번호: 할인율)
seasonal_pass = {}

# 주차 기록 {차량번호: (입차시각, 위치(층, 자리번호), 정기권여부)}
parking_record = {}

def print_tower():
    print("\n--- 현재 주차장 상태 ---")
    for floor in range(parking_floors - 1, -1, -1): # 윗층부터 출력
        print(f"{floor + 1:2d}층: ", end='')
        for space in parking_tower[floor]:
            print(space, end=' ')
        print()
    print()


def find_first_empty():
    for floor in range(parking_floors):
        for space in range(parking_clols):
            if parking_tower[floor][space] == "[]":
                return floor, space
    return None  # 만차


def parking_fee(minutes, is_seasonal):
    fee = math.ceil(minutes / 10) * 500
    if is_seasonal:
        fee = int(fee * 0.5)
    return fee

while True:
    action = input("입차: in / 출차: out / 종료: exit > ").strip()
    if action == "exit":
        print("종료합니다.")
        break

    if action == "in":
        print_tower()
        plate = input("차량번호 입력: ").strip()
        if plate in parking_record:
            print("이미 입차하신 차량입니다.")
            continue

        entry_time = input("입차 시각 (YYYY-MM-DD HH:MM): ").strip()
        try:
            entry_time_dt = datetime.datetime.strptime(entry_time, "%Y-%m-%d %H:%M")
        except ValueError:
            print("시간 형식 오류. 예시: 2025-09-01 09:30")
            continue

        try:
            floor = int(input("원하는 층 번호(1~10): ")) - 1
            space = int(input("원하는 자리(1~10): ")) - 1
        except ValueError:
            print("숫자만 입력하세요.")
            continue

        # 원하는 자리가 이미 사용중이면 빈자리 우선 안내 및 이동 처리
        if parking_tower[floor][space] != "[]":
            print("선택하신 자리는 이미 사용중입니다.")
            empty_spot = find_first_empty()
            if empty_spot:
                floor, space = empty_spot
                print(f"가장 가까운 빈자리 {floor + 1}층 {space + 1}번으로 안내합니다.")
            else:
                print("주차장이 만차입니다.")
                continue

        # 정기권 차량 여부 확인 및 신규 등록 의사 확인
        is_seasonal = plate in seasonal_pass
        if not is_seasonal:
            seasonal_ask = input("정기권 사용자가 아닙니다. 신규 등록 하시겠습니까? (y/n): ").lower()
            if seasonal_ask == "y":
                # 신규 등록 (할인률 50%)
                seasonal_pass[plate] = 0.5
                is_seasonal = True

        # 입차 처리
        parking_tower[floor][space] = "[X]"
        parking_record[plate] = (entry_time_dt, (floor, space), is_seasonal)
        print(f"{plate} 차량 입차 완료! {floor + 1}층 {space + 1}번\n")
        print_tower()

    elif action == "out":
        plate = input("출차 차량번호 입력: ").strip()
        if plate not in parking_record:
            print("주차 기록이 없습니다.")
            continue

        out_time = input("출차 시각 (YYYY-MM-DD HH:MM): ").strip()
        try:
            out_time_dt = datetime.datetime.strptime(out_time, "%Y-%m-%d %H:%M")
        except ValueError:
            print("시간 형식 오류. 예시: 2025-09-01 17:50")
            continue

        entry_time_dt, (floor, space), is_seasonal = parking_record[plate]

        # 주차 시간(10분 이하 단위 올림)
        timediff = out_time_dt - entry_time_dt
        minutes = int(timediff.total_seconds() // 60)
        # 요금 계산
        fee = parking_fee(minutes, is_seasonal)

        print(f"총 주차시간: {minutes}분, 요금: {fee}원 (정기권 {'적용' if is_seasonal else '미적용'})")
        # 자리 비우기
        parking_tower[floor][space] = "[]"
        del parking_record[plate]
        print_tower()
    else:
        print("잘못된 명령입니다.")
