import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import requests
import json
import os

# 사용자 정보 저장                                      
users = {}
current_user = None

# 사용자 정보를 저장할 파일 경로
USER_DATA_FILE = 'users.json'

# OpenWeatherMap API 키
API_KEY = 'bd96f0be95b079f4e0f446632ebc6710'
CITY_NAME = 'Seoul'  # 원하는 도시 이름으로 변경 가능

# 사용자 정보를 파일에서 로드하는 함수
def load_users():
    global users
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            users = json.load(file)

# 사용자 정보를 파일에 저장하는 함수
def save_users():
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file)

# 날씨 정보를 가져오는 함수
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['main']['temp'], data['weather'][0]['description']
    else:
        messagebox.showerror("날씨 정보 오류", "날씨 정보를 가져오는 데 실패했습니다.")
        return None, None

# 성별과 체형, 날씨에 맞춰 코디를 추천하는 함수
def suggest_outfit_by_body_type_and_weather():
    temp, weather_desc = get_weather()
    if temp is None:
        return

    if len(users[current_user]['clothes_list']) < 3:
        messagebox.showinfo("오늘의 코디 제안", "옷을 충분히 추가해주세요.")
        return

    top_list = [cloth for cloth in users[current_user]['clothes_list'] if cloth[0] == "상의"]
    bottom_list = [cloth for cloth in users[current_user]['clothes_list'] if cloth[0] == "하의"]
    outerwear_list = [cloth for cloth in users[current_user]['clothes_list'] if cloth[0] == "겉옷"]

    if not top_list or not bottom_list:
        messagebox.showinfo("오늘의 코디 제안", "상의와 하의를 최소 하나씩 추가해주세요.")
        return

    user_gender = users[current_user]['gender']
    user_body_shape = users[current_user]['body_shape']

    # 체형에 따른 코디 규칙 및 이유
    reason = ""
    if user_body_shape == "삼각형":
        top = random.choice([cloth for cloth in top_list if cloth[1] in ["흰색", "빨간색", "파란색", "주황색", "초록색", "노란색", "분홍색", "베이지색"]])
        bottom = random.choice([cloth for cloth in bottom_list if cloth[1] in ["검은색", "갈색", "남색"]])
        reason = "삼각형 체형은 어깨가 좁고 엉덩이가 넓으므로, 밝은 색 상의와 어두운 색 하의를 입으면 상체를 강조하고 하체를 축소시킬 수 있습니다."
    elif user_body_shape == "역삼각형":
        top = random.choice([cloth for cloth in top_list if cloth[1] in ["검은색", "갈색", "보라색", "남색", "청록색"]])
        bottom = random.choice([cloth for cloth in bottom_list if cloth[1] in ["흰색", "파란색", "베이지색"]])
        reason = "역삼각형 체형은 어깨가 넓고 허리가 좁으므로, 어두운 색 상의와 밝은 색 하의를 입으면 상체를 축소하고 하체를 강조할 수 있습니다."
    elif user_body_shape == "직사각형":
        top = random.choice([cloth for cloth in top_list if cloth[1] in ["흰색", "빨간색", "파란색", "주황색", "초록색", "노란색", "분홍색", "베이지색"]])
        bottom = random.choice([cloth for cloth in bottom_list if cloth[1] in ["검은색", "갈색", "남색"]])
        reason = "직사각형 체형은 어깨와 허리, 엉덩이가 비슷하므로, 패턴이 있는 옷을 입으면 체형에 변화를 줄 수 있습니다."
    elif user_body_shape == "원형":
        top = random.choice([cloth for cloth in top_list if cloth[1] in ["검은색", "갈색", "보라색", "남색", "청록색"]])
        bottom = random.choice([cloth for cloth in bottom_list if cloth[1] in ["흰색"]])
        reason = "원형 체형은 복부가 두드러지므로, 어두운 색 상의와 밝은 색 하의를 입으면 상체를 축소하고 하체를 강조할 수 있습니다."
    elif user_body_shape == "모래시계형":
        top = random.choice([cloth for cloth in top_list if cloth[1] in ["흰색", "빨간색", "파란색", "주황색", "초록색", "노란색", "분홍색", "베이지색"]])
        bottom = random.choice([cloth for cloth in bottom_list if cloth[1] in ["검은색", "갈색", "남색"]])
        reason = "모래시계형 체형은 허리가 잘록하므로, 허리라인을 강조하는 옷을 입어 체형을 돋보이게 합니다."

    if temp > 20:
        # 더운 날씨: 상의와 하의만 추천
        outfit = f"상의: {top[1]} {top[2]}\n하의: {bottom[1]} {bottom[2]}"
        weather_reason = "더운 날씨에는 가벼운 옷차림을 추천합니다."
    elif 10 <= temp <= 20:
        # 쌀쌀한 날씨: 상의, 하의, 간단한 겉옷 추천
        outerwear = random.choice([cloth for cloth in outerwear_list if cloth[2] not in ["코트", "파카"]])
        outfit = f"상의: {top[1]} {top[2]}\n하의: {bottom[1]} {bottom[2]}\n겉옷: {outerwear[1]} {outerwear[2]}"
        weather_reason = "쌀쌀한 날씨에는 간단한 아우터를 추천합니다."
    else:
        # 추운 날씨: 상의, 하의, 두꺼운 겉옷 추천
        outerwear = random.choice([cloth for cloth in outerwear_list if cloth[2] in ["코트", "파카", "자켓"]])
        outfit = f"상의: {top[1]} {top[2]}\n하의: {bottom[1]} {bottom[2]}\n겉옷: {outerwear[1]} {outerwear[2]}"
        weather_reason = "추운 날씨에는 두꺼운 겉옷을 추천합니다."

    # 날씨 상태에 따른 추가 코디 설명
    if 'rain' in weather_desc.lower():
        weather_reason += " 비가 오므로, 우산을 챙겨가는건 어떨까요?"
    elif 'clear' in weather_desc.lower() or 'sun' in weather_desc.lower():
        weather_reason += " 날씨가 맑으므로, 기분 좋은 외출이 될 수 있을 것 같습니다."

    messagebox.showinfo("오늘의 코디 제안", f"{outfit}\n\n추천 이유: {reason}\n\n날씨: {weather_reason}\n현재 날씨: {temp}°C, {weather_desc}")

# 사용자가 옷을 추가하는 함수
def add_clothes(top_bottom_outerwear, color, category):
    users[current_user].setdefault('clothes_list', []).append((top_bottom_outerwear, color, category))
    save_users()  # 사용자 정보 저장
    messagebox.showinfo("옷 추가", f"{top_bottom_outerwear} {color} {category}를 추가했습니다.")

# 옷 리스트 보기
def view_clothes_list():
    if 'clothes_list' not in users[current_user] or not users[current_user]['clothes_list']:
        messagebox.showinfo("옷 리스트", "추가된 옷이 없습니다.")
        return
    
    tops = [f"{cloth[1]} {cloth[2]}" for cloth in users[current_user]['clothes_list'] if cloth[0] == "상의"]
    bottoms = [f"{cloth[1]} {cloth[2]}" for cloth in users[current_user]['clothes_list'] if cloth[0] == "하의"]
    outerwears = [f"{cloth[1]} {cloth[2]}" for cloth in users[current_user]['clothes_list'] if cloth[0] == "겉옷"]

    clothes_str = "상의:\n" + "\n".join(tops) + "\n\n하의:\n" + "\n".join(bottoms) + "\n\n겉옷:\n" + "\n".join(outerwears)
    messagebox.showinfo("옷 리스트", clothes_str)

# 옷 삭제 함수
def delete_clothes():
    if 'clothes_list' not in users[current_user] or not users[current_user]['clothes_list']:
        messagebox.showinfo("옷 삭제", "삭제할 옷이 없습니다.")
        return
    
    delete_window = tk.Toplevel(root)
    delete_window.title("옷 삭제")

    lbl_info = tk.Label(delete_window, text="삭제할 옷을 클릭하세요:")
    lbl_info.pack(pady=10)

    listbox = tk.Listbox(delete_window, width=50, height=20)
    for cloth in users[current_user]['clothes_list']:
        listbox.insert(tk.END, f"{cloth[0]}: {cloth[1]} {cloth[2]}")
    listbox.pack(pady=10)

    def on_cloth_select(event):
        selected_index = listbox.curselection()[0]
        deleted_cloth = users[current_user]['clothes_list'].pop(selected_index)
        save_users()  # 사용자 정보 저장
        messagebox.showinfo("옷 삭제", f"{deleted_cloth[0]} {deleted_cloth[1]} {deleted_cloth[2]}를 삭제했습니다.")
        delete_window.destroy()

    listbox.bind('<<ListboxSelect>>', on_cloth_select)

# 옷 추가 창을 띄우는 함수
def add_clothes_window(clothes_type):
    add_window = tk.Toplevel(root)
    add_window.title("옷 추가")

    lbl_color = tk.Label(add_window, text="색상: ")
    lbl_color.grid(row=0, column=0, padx=10, pady=5)

    # 미리 정의된 색상 리스트
    colors = ["검은색", "흰색", "빨간색", "파란색", "주황색", "초록색", "노란색", "보라색", "분홍색", "갈색", "베이지색", "주황색", "남색", "청록색"]

    color_var = tk.StringVar(add_window)
    color_var.set(colors[0])  # 기본값 설정

    # 색상을 선택할 드롭다운 목록 생성
    color_dropdown = tk.OptionMenu(add_window, color_var, *colors)
    color_dropdown.grid(row=0, column=1, padx=10, pady=5)

    lbl_category = tk.Label(add_window, text="옷 종류: ")
    lbl_category.grid(row=1, column=0, padx=10, pady=5)

    if clothes_type == "상의":
        categories = ["티셔츠", "와이셔츠", "니트", "맨투맨", "후드티"]
    elif clothes_type == "하의":
        categories = ["슬랙스", "데님팬츠", "면바지"]
    elif clothes_type == "겉옷":
        categories = ["코트", "자켓", "가디건", "블레이저", "파카"]

    category_var = tk.StringVar(add_window)
    category_var.set(categories[0])  # 기본값 설정

    category_dropdown = tk.OptionMenu(add_window, category_var, *categories)
    category_dropdown.grid(row=1, column=1, padx=10, pady=5)

    def save_clothes():
        add_clothes(clothes_type, color_var.get(), category_var.get())
        add_window.destroy()

    btn_save = tk.Button(add_window, text="저장", command=save_clothes)
    btn_save.grid(row=2, columnspan=2, padx=10, pady=10)

# 상의, 하의, 겉옷을 선택하는 함수
def select_clothes_type():
    select_window = tk.Toplevel(root)
    select_window.title("옷 추가 선택")

    btn_top = tk.Button(select_window, text="상의 추가", command=lambda: add_clothes_window("상의"))
    btn_top.pack(pady=5)

    btn_bottom = tk.Button(select_window, text="하의 추가", command=lambda: add_clothes_window("하의"))
    btn_bottom.pack(pady=5)

    btn_outerwear = tk.Button(select_window, text="겉옷 추가", command=lambda: add_clothes_window("겉옷"))
    btn_outerwear.pack(pady=5)

# 회원가입 함수
def signup():
    signup_window = tk.Toplevel(root)
    signup_window.title("회원가입")

    lbl_id = tk.Label(signup_window, text="아이디: ")
    lbl_id.grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(signup_window)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    lbl_pw = tk.Label(signup_window, text="비밀번호: ")
    lbl_pw.grid(row=1, column=0, padx=10, pady=5)
    pw_entry = tk.Entry(signup_window, show='*')
    pw_entry.grid(row=1, column=1, padx=10, pady=5)

    lbl_gender = tk.Label(signup_window, text="성별: ")
    lbl_gender.grid(row=2, column=0, padx=10, pady=5)
    gender_var = tk.StringVar(signup_window)
    gender_var.set("남성")
    gender_dropdown = tk.OptionMenu(signup_window, gender_var, "남성", "여성")
    gender_dropdown.grid(row=2, column=1, padx=10, pady=5)

    lbl_body_shape = tk.Label(signup_window, text="체형: ")
    lbl_body_shape.grid(row=3, column=0, padx=10, pady=5)
    body_shape_var = tk.StringVar(signup_window)
    body_shape_var.set("삼각형")
    body_shape_dropdown = tk.OptionMenu(signup_window, body_shape_var, "삼각형", "역삼각형", "직사각형", "원형", "모래시계형")
    body_shape_dropdown.grid(row=3, column=1, padx=10, pady=5)

    def save_user():
        user_id = id_entry.get()
        user_pw = pw_entry.get()
        if user_id in users:
            messagebox.showerror("회원가입 오류", "이미 존재하는 아이디입니다.")
        else:
            users[user_id] = {
                "password": user_pw,
                "gender": gender_var.get(),
                "body_shape": body_shape_var.get(),
                "clothes_list": []
            }
            save_users()  # 사용자 정보를 저장
            messagebox.showinfo("회원가입 완료", f"회원가입이 완료되었습니다.\n아이디: {user_id}\n성별: {users[user_id]['gender']}\n체형: {users[user_id]['body_shape']}")
            signup_window.destroy()

    btn_save = tk.Button(signup_window, text="가입하기", command=save_user)
    btn_save.grid(row=4, columnspan=2, padx=10, pady=10)

# 로그인 함수
def login():
    login_window = tk.Toplevel(root)
    login_window.title("로그인")

    lbl_id = tk.Label(login_window, text="아이디: ")
    lbl_id.grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(login_window)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    lbl_pw = tk.Label(login_window, text="비밀번호: ")
    lbl_pw.grid(row=1, column=0, padx=10, pady=5)
    pw_entry = tk.Entry(login_window, show='*')
    pw_entry.grid(row=1, column=1, padx=10, pady=5)

    def authenticate():
        global current_user
        user_id = id_entry.get()
        user_pw = pw_entry.get()
        if user_id in users and users[user_id]["password"] == user_pw:
            current_user = user_id
            # 만약 사용자의 clothes_list가 없으면 초기화
            if 'clothes_list' not in users[current_user]:
                users[current_user]['clothes_list'] = []
            messagebox.showinfo("로그인 성공", f"환영합니다, {user_id}님!")
            login_window.destroy()
            main_app()  # 메인 애플리케이션 실행
        else:
            messagebox.showerror("로그인 오류", "아이디 또는 비밀번호가 잘못되었습니다.")

    btn_login = tk.Button(login_window, text="로그인", command=authenticate)
    btn_login.grid(row=2, columnspan=2, padx=10, pady=10)

# 메인 애플리케이션 함수
def main_app():
    btn_signup.pack_forget()  # 회원가입 버튼 숨기기
    btn_login.pack_forget()  # 로그인 버튼 숨기기
    btn_add_clothes.pack(pady=5)
    btn_view_clothes.pack(pady=5)
    btn_delete_clothes.pack(pady=5)
    btn_outfit.pack(pady=10)

# GUI 생성
def main():
    global root, btn_signup, btn_login, btn_add_clothes, btn_view_clothes, btn_delete_clothes, btn_outfit
    root = tk.Tk()
    root.title("오늘의 코디")

    load_users()  # 프로그램 시작 시 사용자 정보 로드

    btn_signup = tk.Button(root, text="회원가입", command=signup)
    btn_signup.pack(pady=5)

    btn_login = tk.Button(root, text="로그인", command=login)
    btn_login.pack(pady=5)

    btn_add_clothes = tk.Button(root, text="내 옷장", command=select_clothes_type)
    btn_view_clothes = tk.Button(root, text="내 옷장 보기", command=view_clothes_list)
    btn_delete_clothes = tk.Button(root, text="옷 삭제", command=delete_clothes)
    btn_outfit = tk.Button(root, text="오늘의 코디 제안", command=suggest_outfit_by_body_type_and_weather)

    root.mainloop()

if __name__ == "__main__":
    main()
