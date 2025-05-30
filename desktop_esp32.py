import machine
import time
import random
import ssd1306
import network
import math
import ujson as json  
import ntptime
import urequests as requests


SCL_PIN = 22
SDA_PIN = 21
I2C_FREQ = 400000

OLED_WIDTH = 128
OLED_HEIGHT = 64
sch_00 = 0
TIME_FILE = "time.json"
NTP_HOST = "pool.ntp.org"


i2c = machine.I2C(0, scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN), freq=I2C_FREQ)
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
button_1 = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
button_2 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
button_3 = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(5, machine.Pin.OUT)
led_1 = machine.Pin(23, machine.Pin.OUT)
# --- Конфигурация ---
TIME_FILE = "time.json"
NTP_HOST = "pool.ntp.org" # Хост для получения времени
KRASNOYARSK_TIMEZONE = 7   # Красноярск: UTC+7
TIME_UPDATE_INTERVAL = 40 * 1000  # 10 секунд в миллисекундах
last_sync_time = 0  # Время последней синхронизации

# --- Функция для получения времени из сети ---
def get_network_time():
    """Получает время из сети и возвращает его в формате (год, месяц, день, час, минута, секунда, день недели, год. день)"""
    try:
        ntptime.settime()
        return time.localtime()
    except Exception as e:
        print("Error getting network time:", e)
        return None

# --- Функция для сохранения времени в JSON-файл ---
def save_time_to_json(hour, minute):
    """Сохраняет час и минуту в JSON-файл."""
    try:
        with open(TIME_FILE, 'w') as f:
            json.dump({'hour': hour, 'minute': minute}, f)
        print("Time saved to {}".format(TIME_FILE))
    except Exception as e:
        print("Error saving time: {}".format(e))

# --- Функция для загрузки времени из JSON-файла ---
def load_time_from_json():
    """Загружает час и минуту из JSON-файла.  Возвращает (час, минута) или None, если файл не найден."""
    try:
        with open(TIME_FILE, 'r') as f:
            data = json.load(f)
            return data['hour'], data['minute']
    except OSError:
        print("Time file not found, using default time")
        return None  # Файл не найден
    except Exception as e:
        print("Error loading time: {}".format(e))
        return None

# --- Функция для синхронизации времени ---
def sync_time(timer):
    """Синхронизирует время с сетью и сохраняет его в файл."""
    global last_sync_time
    if root_wifi_conn:  # Если есть подключение к Wi-Fi
        try:
            utc_time = get_network_time()
            if utc_time:
                hour = (utc_time[3] + KRASNOYARSK_TIMEZONE) % 24  # Применяем часовой пояс Красноярска
                minute = utc_time[4]
                save_time_to_json(hour, minute)  # Сохраняем полученное время
                print("Time synchronized from network (Krasnoyarsk)")
                last_sync_time = time.time() # Store the time
            else:
                print("Failed to get network time")
        except Exception as e:
            print("Error synchronizing time: {}".format(e))
    else:
        print("No Wi-Fi connection, skipping time synchronization")

# --- Функция time_clock (с использованием JSON и сети) ---
def time_clock(root_wifi_conn):
    """Возвращает текущее время в формате HH:MM.  Использует время из JSON-файла или дефолтное значение, если файл не найден."""
    hour = 0
    minute = 0
    saved_time = load_time_from_json()
    if saved_time:
        hour, minute = saved_time
    else:
        print("Using default time")

    time_str = "{:02d}:{:02d}".format(hour, minute)
    return time_str

# --- Инициализация таймера ---
timer = machine.Timer(-1)  # Используем Timer ID -1
timer.init(period=TIME_UPDATE_INTERVAL, mode=machine.Timer.PERIODIC, callback=sync_time) # Вызываем sync_time каждые 10 сек

icon_k = [20,40,60,80,100]

znak_1 = [30,43,56,69,82,94]
znak_2 = [50]
top = ["","","","","",""]
passtop = [1,0,0,3,2,1]
root_wifi_conn = False
utills = ["watch","calculator","editor","notepad","setup","other utill"]
watch = ["mus",0,"watch_p"]
calc = ["app",1,"calc_p"]
edition = ["app",2,"mus_p"]
setup = ["app",3,"setup_p"]
notepad = ["app",4,"notepad_p"]
wifil = ["app",5,"wifi_p"]
bluetooth = ["app",6,"bluet_p"]
display = ["app",7,"display_p"]
war = 1
app_hi = [14,45,76,107]
app_ht = [9,39,69,99]
app_wi = [23]
app_wt = [33]  
TEXT = "ESP32"
TEXT_WIDTH = len(TEXT) * 8  # Ширина текста (каждый символ 8 пикселей)
TEXT_HEIGHT = 8
x = 0  # Начальная позиция по X
y = 0  # Начальная позиция по Y
x_speed = 1  # Скорость по X (1 пиксель за кадр)
y_speed = 1  # Скорость по Y (1 пиксель за кадр)



def notepad_p():
    oled.fill(0)
    oled.text("start app...",0,0)
    oled.show()
    time.sleep(2)
    oled.fill(0)
    oled.text("The application",0,0)
    oled.text("is under",0,10)
    oled.text("development!",0,20)
    oled.show()
    time.sleep(3)
def wifi_p():
    oled.fill(0)
    oled.text("start app...",0,0)
    oled.show()
    time.sleep(2)
    oled.fill(0)
    oled.text("The application",0,0)
    oled.text("is under",0,10)
    oled.text("development!",0,20)
    oled.show()
    time.sleep(3)
def bluet_p():
    oled.fill(0)
    oled.text("start app...",0,0)
    oled.show()
    time.sleep(2)
    oled.fill(0)
    oled.text("The application",0,0)
    oled.text("is under",0,10)
    oled.text("development!",0,20)
    oled.show()
    time.sleep(3)
def display_p():
    oled.fill(0)
    oled.text("start app...",0,0)
    oled.show()
    time.sleep(2)
    oled.fill(0)
    oled.text("The application",0,0)
    oled.text("is under",0,10)
    oled.text("development!",0,20)
    oled.show()
    time.sleep(3)
# --- Функция рисования текста ---
def draw_logo(x, y):
    oled.text(TEXT, x, y, 1)

# --- Функция анимации ---

def animate_logo():
    global x1, y1, x_speed1, y_speed1, x2, y2, x_speed2, y_speed2, x3, y3, x_speed3, y_speed3

    # --- Параметры первого текста ("GNOME") ---
    TEXT1 = "GNOME"
    TEXT_WIDTH1 = len(TEXT1) * 8
    TEXT_HEIGHT1 = 8
    x1 = 0
    y1 = 0
    x_speed1 = 1
    y_speed1 = 1

    # --- Параметры второго текста ("V1.1") ---
    TEXT2 = "BETA"
    TEXT_WIDTH2 = len(TEXT2) * 8
    TEXT_HEIGHT2 = 8
    x2 = 50
    y2 = 20
    x_speed2 = -1
    y_speed2 = -1

    # --- Параметры третьего текста ("ESP32") ---
    TEXT3 = "ESP32"
    TEXT_WIDTH3 = len(TEXT3) * 8
    TEXT_HEIGHT3 = 8
    x3 = 25
    y3 = 40
    x_speed3 = 2
    y_speed3 = 0

    # --- Количество пузырей и их параметры ---
    NUM_BUBBLES = 10  # Можно увеличить или уменьшить
    bubbles = []
    for _ in range(NUM_BUBBLES):
        bubbles.append({
            'x': random.randint(0, OLED_WIDTH),
            'y': random.randint(0, OLED_HEIGHT),
            'radius': random.randint(1, 3),  # Случайный радиус
            'speed_x': random.uniform(-0.5, 0.5), # Горизонтальная скорость
            'speed_y': random.uniform(-0.5, 0.5)  # Вертикальная скорость
        })

    # --- Функция рисования текста ---
    def draw_text(text, x, y):
        oled.text(text, x, y, 1)

    # --- Функция рисования пузыря (рисование пикселями) ---
    def draw_bubble(oled, x0, y0, radius, color):
        for x in range(x0 - radius, x0 + radius + 1):
            for y in range(y0 - radius, y0 + radius + 1):
                if (x - x0)**2 + (y - y0)**2 <= radius**2:
                    if 0 <= x < OLED_WIDTH and 0 <= y < OLED_HEIGHT:  # Проверка выхода за границы
                        oled.pixel(x, y, color)

    # --- Функция рисования пузыря (алгоритм Брезенхэма) - ЗАКОММЕНТИРОВАНА ПО УМОЛЧАНИЮ ---
    # def draw_circle(oled, x0, y0, r, color):
    #     x = r
    #     y = 0
    #     decisionOver2 = 1 - x
    #
    #     while y <= x:
    #         oled.pixel(x + x0, y + y0, color)
    #         oled.pixel(y + x0, x + y0, color)
    #         oled.pixel(-x + x0, y + y0, color)
    #         oled.pixel(-y + x0, x + y0, color)
    #         oled.pixel(-x + x0, -y + y0, color)
    #         oled.pixel(-y + x0, -x + y0, color)
    #         oled.pixel(x + x0, -y + y0, color)
    #         oled.pixel(y + x0, -x + y0, color)
    #         y += 1
    #         if decisionOver2 <= 0:
    #             decisionOver2 += 2 * y + 1
    #         else:
    #             x -= 1
    #             decisionOver2 += 2 * (y - x) + 1

    while True:
        oled.fill(0)

        # Рисуем пузыри
        for bubble in bubbles:
            draw_bubble(oled, int(bubble['x']), int(bubble['y']), bubble['radius'], 1) # Рисуем пузырь

            # Обновляем позицию пузыря
            bubble['x'] += bubble['speed_x']
            bubble['y'] += bubble['speed_y']

            # Обработка столкновений со стенками для пузырей
            if bubble['x'] - bubble['radius'] < 0:
                bubble['x'] = bubble['radius']  # Отталкиваем от левой границы
                bubble['speed_x'] = -bubble['speed_x']
            elif bubble['x'] + bubble['radius'] > OLED_WIDTH:
                bubble['x'] = OLED_WIDTH - bubble['radius']  # Отталкиваем от правой границы
                bubble['speed_x'] = -bubble['speed_x']

            if bubble['y'] - bubble['radius'] < 0:
                bubble['y'] = bubble['radius']  # Отталкиваем от верхней границы
                bubble['speed_y'] = -bubble['speed_y']
            elif bubble['y'] + bubble['radius'] > OLED_HEIGHT:
                bubble['y'] = OLED_HEIGHT - bubble['radius']  # Отталкиваем от нижней границы
                bubble['speed_y'] = -bubble['speed_y']

        # Рисуем тексты
        draw_text(TEXT1, x1, y1)
        draw_text(TEXT2, x2, y2)
        draw_text(TEXT3, x3, y3)

        # Обновляем позиции текстов
        x1 += x_speed1
        y1 += y_speed1
        x2 += x_speed2
        y2 += y_speed2
        x3 += x_speed3
        y3 += y_speed3

        # Обработка столкновений со стенками для текстов
        if x1 + TEXT_WIDTH1 > OLED_WIDTH or x1 < 0:
            x_speed1 = -x_speed1
        if y1 + TEXT_HEIGHT1 > OLED_HEIGHT or y1 < 0:
            y_speed1 = -y_speed1

        if x2 + TEXT_WIDTH2 > OLED_WIDTH or x2 < 0:
            x_speed2 = -x_speed2
        if y2 + TEXT_HEIGHT2 > OLED_HEIGHT or y2 < 0:
            y_speed2 = -y_speed2

        if x3 + TEXT_WIDTH3 > OLED_WIDTH or x3 < 0:
            x_speed3 = -x_speed3
        if y3 + TEXT_HEIGHT3 > OLED_HEIGHT or y3 < 0:
            y_speed3 = -y_speed3

        # --- Проверка столкновений между текстами ---
        # Текст 1 и Текст 2
        if (
            x1 < x2 + TEXT_WIDTH2
            and x1 + TEXT_WIDTH1 > x2
            and y1 < y2 + TEXT_HEIGHT2
            and y1 + TEXT_HEIGHT1 > y2
        ):
            x_speed1, x_speed2 = -x_speed1, -x_speed2
            y_speed1, y_speed2 = -y_speed1, -y_speed2

        # Текст 1 и Текст 3
        if (
            x1 < x3 + TEXT_WIDTH3
            and x1 + TEXT_WIDTH1 > x3
            and y1 < y3 + TEXT_HEIGHT3
            and y1 + TEXT_HEIGHT1 > y3
        ):
            x_speed1, x_speed3 = -x_speed1, -x_speed3
            y_speed1, y_speed3 = -y_speed1, -y_speed3

        # Текст 2 и Текст 3
        if (
            x2 < x3 + TEXT_WIDTH3
            and x2 + TEXT_WIDTH2 > x3
            and y2 < y3 + TEXT_HEIGHT3
            and y2 + TEXT_HEIGHT2 > y3
        ):
            x_speed2, x_speed3 = -x_speed2, -x_speed3
            y_speed2, y_speed3 = -y_speed2, -y_speed3

        oled.show()
        time.sleep(0.02)


        if button.value() == 0:
            break
        elif button_1.value() == 0:
            break
        elif button_2.value() == 0:
            break
        elif button_3.value() == 0:
            break
def slide_1(root_wifi_conn):
    global sch_00
    ees = root_wifi_conn
    oled.fill(0)
    tre_ku()
    wifi(root_wifi_conn)
    oled.rect(3, 3, 122, 58, 1)
    time_str = time_clock(root_wifi_conn)
    oled.text(time_str,65,6)
    draw_half_tone_rectangle(30, 53, 70, 3)
    draw_arrow_pixels(27, 54, 'left_f')
    draw_arrow_pixels(102, 54, 'right_f')
    app_wh()
    cklick()
    sch_01 = sch_00
    sch_00 = sch_01 + 1
    if sch_00 == 300:
        sch_00 = 0
        animate_logo()
    if ees == True:
        draw_wifi_icon(107, 4)
        oled.show()
            
    elif ees == False:
        draw_wifi_off_icon(107, 4)
        oled.show()
            
            
    elif ees == None:
        draw_wifi_off_icon(107, 4)
        oled.show()
    time.sleep(0.1)

        
        
def slide_2(root_wifi_conn):
    global sch_00
    ees = wifi(root_wifi_conn)
    oled.fill(0)
    tre_ku()
    wifi(root_wifi_conn)
    oled.rect(3, 3, 122, 58, 1)
    time_str = time_clock(root_wifi_conn)
    oled.text(time_str,65,6)
    draw_half_tone_rectangle(30, 53, 70, 3)
    draw_arrow_pixels(27, 54, 'left_f')
    draw_arrow_pixels(102, 54, 'right_f')
    app_wh_1()
    cklick_1()
    sch_01 = sch_00
    sch_00 = sch_01 + 1
    if sch_00 == 300:
        sch_00 = 0
        animate_logo() 
                
    if ees == True:
        draw_wifi_icon(107, 4)
        oled.show()
            
    elif ees == False:
        draw_wifi_off_icon(107, 4)
        oled.show()
            
            
    elif ees == None:
        draw_wifi_off_icon(107, 4)
        oled.show()
    time.sleep(0.1)


def calc_p(): # нужно чтобы вызывалось из основного кода
    oled.fill(0)
    oled.text("start app...",0,0)
    oled.show()
    time.sleep(2)
    oled.fill(0)
    oled.text("The application",0,0)
    oled.text("is under",0,10)
    oled.text("development!",0,20)
    oled.show()
    time.sleep(3)







def short_n(apps_list):
    nm = apps_list
    name_1s = nm[0][:3]
    name_2s = nm[1][:3]
    name_3s = nm[2][:3]
    name_4s = nm[3][:3]
    name_all = [name_1s,name_2s,name_3s,name_4s]
    return name_all


def short_n_1(apps_list):
    nm = apps_list
    name_1ss = nm[4][:3]
    name_2ss = nm[5][:3]
    name_3ss = nm[6][:3]
    name_4ss = nm[7][:3]
    name_alls = [name_1ss,name_2ss,name_3ss,name_4ss]
    return name_alls
    

apps_list = ["calc","edition","setup","watch","notepad","wifil","display","bluetooth"]
def util_app(apps_list):
    ig = apps_list
    info_1 = ['','','','']
    info_1[0] = globals()[apps_list[0]] #Используем строку как ключ
    info_1[1] = globals()[apps_list[1]] #Используем строку как ключ
    info_1[2] = globals()[apps_list[2]] #Используем строку как ключ
    info_1[3] = globals()[apps_list[3]] #Используем строку как ключ
    return info_1


def util_app_1(apps_list):
    ie = apps_list
    info_2 = ['','','','']
    info_2[0] = globals()[apps_list[4]] #Используем строку как ключ
    info_2[1] = globals()[apps_list[5]] #Используем строку как ключ
    info_2[2] = globals()[apps_list[6]] #Используем строку как ключ
    info_2[3] = globals()[apps_list[7]] #Используем строку как ключ
    return info_2


def util_tipe(apps_list):
    on = apps_list
    onfo_1 = ['','','','']
    onfo_1[0] = globals()[on[0]] #Используем строку как ключ
    onfo_1[1] = globals()[on[1]] #Используем строку как ключ
    onfo_1[2] = globals()[on[2]] #Используем строку как ключ
    onfo_1[3] = globals()[on[3]] #Используем строку как ключ
    return onfo_1

def util_tipe_1(apps_list):
    on = apps_list
    onfo_2 = ['','','','']
    onfo_2[0] = globals()[on[4]] #Используем строку как ключ
    onfo_2[1] = globals()[on[5]] #Используем строку как ключ
    onfo_2[2] = globals()[on[6]] #Используем строку как ключ
    onfo_2[3] = globals()[on[7]] #Используем строку как ключ
    return onfo_2





arrow_position = 0  # Индекс текущей позиции стрелки (0-3)


def tre_ku():
    global arrow_position
    

    oled.fill(0)

    # Обработка кнопки "вперед"
    if button.value() == 0:
        arrow_position = (arrow_position + 1) % 4
        time.sleep(0.001)

    # Обработка кнопки "назад"
    if button_3.value() == 0:
        arrow_position = (arrow_position - 1) % 4
        time.sleep(0.001)

    # Рисуем стрелку в текущей позиции
    if arrow_position == 0:
        draw_arrow_pixels(19, 45, 'up')
    elif arrow_position == 1:
        draw_arrow_pixels(50, 45, 'up')
    elif arrow_position == 2:
        draw_arrow_pixels(81, 45, 'up')
    elif arrow_position == 3:
        draw_arrow_pixels(112, 45, 'up')
        
        
def cklick():
    global arrow_position
    turn = util_tipe(apps_list)

    if arrow_position == 0:
        if button_1.value() == 0:
            function_name = turn[0][2]
            if function_name in globals():  # Проверяем, существует ли функция
                globals()[function_name]()

    elif arrow_position == 1:
        if button_1.value() == 0:
            function_name = turn[1][2]
            if function_name in globals():
                globals()[function_name]()

    elif arrow_position == 2:
        if button_1.value() == 0:
            function_name = turn[2][2]
            if function_name in globals():
                globals()[function_name]()

    elif arrow_position == 3:
        if button_1.value() == 0:
            function_name = turn[3][2]
            if function_name in globals():
                globals()[function_name]()
                
                
def cklick_1():
    global arrow_position
    turn = util_tipe_1(apps_list)

    if arrow_position == 0:
        if button_1.value() == 0:
            function_name = turn[0][2]
            if function_name in globals():  # Проверяем, существует ли функция
                globals()[function_name]()

    elif arrow_position == 1:
        if button_1.value() == 0:
            function_name = turn[1][2]
            if function_name in globals():
                globals()[function_name]()

    elif arrow_position == 2:
        if button_1.value() == 0:
            function_name = turn[2][2]
            if function_name in globals():
                globals()[function_name]()

    elif arrow_position == 3:
        if button_1.value() == 0:
            function_name = turn[3][2]
            if function_name in globals():
                globals()[function_name]()
                
    
def mus_p():
    oled.fill(0)
    oled.text("start app...",0,0)
    oled.show()
    time.sleep(2)
    oled.fill(0)
    oled.text("The application",0,0)
    oled.text("is under",0,10)
    oled.text("development!",0,20)
    oled.show()
    time.sleep(3)
    
def setup_p():
    oled.fill(0)
    oled.text("start app...",0,0)
    oled.show()
    time.sleep(2)
    oled.fill(0)
    oled.text("The application",0,0)
    oled.text("is under",0,10)
    oled.text("development!",0,20)
    oled.show()
    time.sleep(3)
    
def watch_p():
    oled.fill(0)
    oled.text("start app...",0,0)
    oled.show()
    time.sleep(2)
    oled.fill(0)
    oled.text("The application",0,0)
    oled.text("is under",0,10)
    oled.text("development!",0,20)
    oled.show()
    time.sleep(3)





            
    
    
    
    

def app_wh():
    
    x_name = short_n(apps_list)
    x_type_1 = util_app(apps_list)
    if x_type_1[0][0] == "app":
        draw_app_icon(app_hi[0],app_wi[0])
        oled.text(x_name[0],app_ht[0],app_wt[0])
    if x_type_1[0][0] == "text":
        draw_text_icon(app_hi[0],app_wi[0])
        oled.text(x_name[0],app_ht[0],app_wt[0])
    if x_type_1[0][0] == "mus":
        draw_music_icon(app_hi[0],app_wi[0])
        oled.text(x_name[0],app_ht[0],app_wt[0])
    if x_type_1[0][0] == "oth":
        draw_other_icon(app_hi[0],app_wi[0])
        oled.text(x_name[0],app_ht[0],app_wt[0])
    if x_type_1[1][0] == "app":
        draw_app_icon(app_hi[1],app_wi[0])
        oled.text(x_name[1],app_ht[1],app_wt[0])
    if x_type_1[1][0] == "text":
        draw_text_icon(app_hi[1],app_wi[0])
        oled.text(x_name[1],app_ht[1],app_wt[0])
    if x_type_1[1][0] == "mus":
        draw_music_icon(app_hi[1],app_wi[0])
        oled.text(x_name[1],app_ht[1],app_wt[0])
    if x_type_1[1][0] == "oth":
        draw_other_icon(app_hi[1],app_wi[0])
        oled.text(x_name[1],app_ht[1],app_wt[0])
    if x_type_1[2][0] == "app":
        draw_app_icon(app_hi[2],app_wi[0])
        oled.text(x_name[2],app_ht[2],app_wt[0])
    if x_type_1[2][0] == "text":
        draw_text_icon(app_hi[2],app_wi[0])
        oled.text(x_name[2],app_ht[2],app_wt[0])
    if x_type_1[2][0] == "mus":
        draw_music_icon(app_hi[2],app_wi[0])
        oled.text(x_name[2],app_ht[2],app_wt[0])
    if x_type_1[2][0] == "oth":
        draw_other_icon(app_hi[2],app_wi[0])
        oled.text(x_name[2],app_ht[2],app_wt[0])
    if x_type_1[3][0] == "app":
        draw_app_icon(app_hi[3],app_wi[0])
        oled.text(x_name[3],app_ht[3],app_wt[0])
    if x_type_1[3][0] == "text":
        draw_text_icon(app_hi[3],app_wi[0])
        oled.text(x_name[3],app_ht[3],app_wt[0])
    if x_type_1[3][0] == "mus":
        draw_music_icon(app_hi[3],app_wi[0])
        oled.text(x_name[3],app_ht[3],app_wt[0])
    if x_type_1[3][0] == "oth":
        draw_other_icon(app_hi[3],app_wi[0])
        oled.text(x_name[3],app_ht[3],app_wt[0])
        
def app_wh_1():
    
    x_name = short_n_1(apps_list)
    x_type_1 = util_app_1(apps_list)
    if x_type_1[0][0] == "app":
        draw_app_icon(app_hi[0],app_wi[0])
        oled.text(x_name[0],app_ht[0],app_wt[0])
    if x_type_1[0][0] == "text":
        draw_text_icon(app_hi[0],app_wi[0])
        oled.text(x_name[0],app_ht[0],app_wt[0])
    if x_type_1[0][0] == "mus":
        draw_music_icon(app_hi[0],app_wi[0])
        oled.text(x_name[0],app_ht[0],app_wt[0])
    if x_type_1[0][0] == "oth":
        draw_other_icon(app_hi[0],app_wi[0])
        oled.text(x_name[0],app_ht[0],app_wt[0])
    if x_type_1[1][0] == "app":
        draw_app_icon(app_hi[1],app_wi[0])
        oled.text(x_name[1],app_ht[1],app_wt[0])
    if x_type_1[1][0] == "text":
        draw_text_icon(app_hi[1],app_wi[0])
        oled.text(x_name[1],app_ht[1],app_wt[0])
    if x_type_1[1][0] == "mus":
        draw_music_icon(app_hi[1],app_wi[0])
        oled.text(x_name[1],app_ht[1],app_wt[0])
    if x_type_1[1][0] == "oth":
        draw_other_icon(app_hi[1],app_wi[0])
        oled.text(x_name[1],app_ht[1],app_wt[0])
    if x_type_1[2][0] == "app":
        draw_app_icon(app_hi[2],app_wi[0])
        oled.text(x_name[2],app_ht[2],app_wt[0])
    if x_type_1[2][0] == "text":
        draw_text_icon(app_hi[2],app_wi[0])
        oled.text(x_name[2],app_ht[2],app_wt[0])
    if x_type_1[2][0] == "mus":
        draw_music_icon(app_hi[2],app_wi[0])
        oled.text(x_name[2],app_ht[2],app_wt[0])
    if x_type_1[2][0] == "oth":
        draw_other_icon(app_hi[2],app_wi[0])
        oled.text(x_name[2],app_ht[2],app_wt[0])
    if x_type_1[3][0] == "app":
        draw_app_icon(app_hi[3],app_wi[0])
        oled.text(x_name[3],app_ht[3],app_wt[0])
    if x_type_1[3][0] == "text":
        draw_text_icon(app_hi[3],app_wi[0])
        oled.text(x_name[3],app_ht[3],app_wt[0])
    if x_type_1[3][0] == "mus":
        draw_music_icon(app_hi[3],app_wi[0])
        oled.text(x_name[3],app_ht[3],app_wt[0])
    if x_type_1[3][0] == "oth":
        draw_other_icon(app_hi[3],app_wi[0])
        oled.text(x_name[3],app_ht[3],app_wt[0])
        
        
    


        
        
pos_2 = 0
last_button_time = 0 # Добавляем переменную для защиты от дребезга

def slide_all(root_wifi_conn):
    global pos_2, last_button_time  # Объявляем, что используем глобальные переменные
    current_time = time.ticks_ms() # Получаем текущее время

    if pos_2 == 0:
        slide_1(root_wifi_conn)

    elif pos_2 == 1:
        slide_2(root_wifi_conn)

    # Проверяем нажатие кнопки и защиту от дребезга
    if button_2.value() == 0 and time.ticks_diff(current_time, last_button_time) > 200:
        # Кнопка нажата и прошло достаточно времени с последнего нажатия
        pos_2 = 1 - pos_2  # Переключаем состояние (0 <-> 1)
        last_button_time = current_time  # Запоминаем время последнего нажатия
        time.sleep(0.1)  # Небольшая задержка для устранения дребезга





def draw_half_tone_rectangle(x, y, width, height):
    for i in range(x, x + width):
        for j in range(y, y + height):
            # Если сумма координат четная, рисуем пиксель, иначе - нет
            if (i + j) % 2 == 0:
                oled.pixel(i, j, 1)  # Белый пиксель
            else:
                oled.pixel(i, j, 0)  # Черный пиксель

def draw_pixel(x, y, color=1):
    oled.pixel(x, y, color)



def draw_wifi_off_icon(x_offset, y_offset):
    """Рисует перечеркнутый значок Wi-Fi по заданным координатам.
    x_offset: Смещение по оси X.
    y_offset: Смещение по оси Y.
    """
    # 1. Wi-Fi (округлый)
    draw_pixel(x_offset + 3, y_offset + 5)
    draw_pixel(x_offset + 4, y_offset + 4)
    draw_pixel(x_offset + 5, y_offset + 3)
    draw_pixel(x_offset + 6, y_offset + 2)
    draw_pixel(x_offset + 7, y_offset + 2)
    draw_pixel(x_offset + 8, y_offset + 1)
    draw_pixel(x_offset + 9, y_offset + 1)
    draw_pixel(x_offset + 10, y_offset + 2)
    draw_pixel(x_offset + 11, y_offset + 2)
    draw_pixel(x_offset + 12, y_offset + 3)
    draw_pixel(x_offset + 13, y_offset + 4)
    draw_pixel(x_offset + 14, y_offset + 5)

    # Второй уровень
    draw_pixel(x_offset + 5, y_offset + 7)
    draw_pixel(x_offset + 6, y_offset + 6)
    draw_pixel(x_offset + 7, y_offset + 5)
    draw_pixel(x_offset + 8, y_offset + 4)
    draw_pixel(x_offset + 9, y_offset + 4)
    draw_pixel(x_offset + 10, y_offset + 5)
    draw_pixel(x_offset + 11, y_offset + 6)
    draw_pixel(x_offset + 12, y_offset + 7)

    # Третий уровень
    draw_pixel(x_offset + 7, y_offset + 9)
    draw_pixel(x_offset + 8, y_offset + 8)
    draw_pixel(x_offset + 9, y_offset + 8)
    draw_pixel(x_offset + 10, y_offset + 9)
    draw_pixel(x_offset + 8, y_offset + 10)
    draw_pixel(x_offset + 9, y_offset + 10)

    # 2. Перечеркивающая линия
    oled.line(x_offset + 1, y_offset + 0, x_offset + 15, y_offset + 10, 1)




# --- Функция для рисования значка Wi-Fi ---
def draw_wifi_icon(x_offset, y_offset):
    """Рисует значок Wi-Fi по заданным координатам.
    x_offset: Смещение по оси X.
    y_offset: Смещение по оси Y.
    """
    draw_pixel(x_offset + 3, y_offset + 5)
    draw_pixel(x_offset + 4, y_offset + 4)
    draw_pixel(x_offset + 5, y_offset + 3)
    draw_pixel(x_offset + 6, y_offset + 2)
    draw_pixel(x_offset + 7, y_offset + 2)
    draw_pixel(x_offset + 8, y_offset + 1)
    draw_pixel(x_offset + 9, y_offset + 1)
    draw_pixel(x_offset + 10, y_offset + 2)
    draw_pixel(x_offset + 11, y_offset + 2)
    draw_pixel(x_offset + 12, y_offset + 3)
    draw_pixel(x_offset + 13, y_offset + 4)
    draw_pixel(x_offset + 14, y_offset + 5)

    # Второй уровень
    draw_pixel(x_offset + 5, y_offset + 7)
    draw_pixel(x_offset + 6, y_offset + 6)
    draw_pixel(x_offset + 7, y_offset + 5)
    draw_pixel(x_offset + 8, y_offset + 4)
    draw_pixel(x_offset + 9, y_offset + 4)
    draw_pixel(x_offset + 10, y_offset + 5)
    draw_pixel(x_offset + 11, y_offset + 6)
    draw_pixel(x_offset + 12, y_offset + 7)

    # Третий уровень
    draw_pixel(x_offset + 7, y_offset + 9)
    draw_pixel(x_offset + 8, y_offset + 8)
    draw_pixel(x_offset + 9, y_offset + 8)
    draw_pixel(x_offset + 10, y_offset + 9)
    draw_pixel(x_offset + 8, y_offset + 10)
    draw_pixel(x_offset + 9, y_offset + 10)

attop = True
def wifi(root_wifi_conn):
    global attop
    max_attempts = 5  # Максимальное количество попыток подключения
    attempt = 0
    while attempt < max_attempts:
        try:
            if attop == False:
                break
            else:
                
                wlan = network.WLAN(network.STA_IF)
                wlan.active(True)
                if not wlan.isconnected():
                    print("Connecting to WiFi...")
                    wlan.connect("DIR-615","B987654321")
                    start_time = time.time()
                    while not wlan.isconnected() and time.time() - start_time < 10:  # Ждем 10 секунд
                        time.sleep(1)
                        print(".")
                    if wlan.isconnected():
                        root_wifi_conn = True
                        print("WiFi connected")
                        return root_wifi_conn
                    else:
                        print("WiFi connection failed")
                else:
                    root_wifi_conn = True
                    return root_wifi_conn
        except Exception as e:
            oled.fill(0)
            e = str(e)
            oled.text(e,0,0)
            oled.show()
            print("Error:", e)
            attempt += 1
            time.sleep(2)  # Ждем перед следующей попыткой
    root_wifi_conn = False
    attop = False
    return root_wifi_conn
root_wifi_conn = wifi(root_wifi_conn)
  
def draw_app_icon(x, y, color=1):
    # Квадратная рамка
    for i in range(x, x + 10):
        oled.pixel(i, y, color)
        oled.pixel(i, y + 9, color)
    for j in range(y, y + 10):
        oled.pixel(x, j, color)
        oled.pixel(x + 9, j, color)
    
    # Иконка приложения (шестеренка)
    oled.pixel(x+2, y+1, color)
    oled.pixel(x+3, y+1, color)
    oled.pixel(x+6, y+1, color)
    oled.pixel(x+7, y+1, color)

    oled.pixel(x+1, y+2, color)
    oled.pixel(x+4, y+2, color)
    oled.pixel(x+5, y+2, color)
    oled.pixel(x+8, y+2, color)

    oled.pixel(x+1, y+3, color)
    oled.pixel(x+3, y+3, color)
    oled.pixel(x+6, y+3, color)
    oled.pixel(x+8, y+3, color)

    oled.pixel(x, y+4, color)
    oled.pixel(x+2, y+4, color)
    oled.pixel(x+7, y+4, color)
    oled.pixel(x+9, y+4, color)

    oled.pixel(x, y+5, color)
    oled.pixel(x+2, y+5, color)
    oled.pixel(x+7, y+5, color)
    oled.pixel(x+9, y+5, color)

    oled.pixel(x+1, y+6, color)
    oled.pixel(x+3, y+6, color)
    oled.pixel(x+6, y+6, color)
    oled.pixel(x+8, y+6, color)

    oled.pixel(x+1, y+7, color)
    oled.pixel(x+4, y+7, color)
    oled.pixel(x+5, y+7, color)
    oled.pixel(x+8, y+7, color)

    oled.pixel(x+2, y+8, color)
    oled.pixel(x+3, y+8, color)
    oled.pixel(x+6, y+8, color)
    oled.pixel(x+7, y+8, color)

def draw_text_icon(x, y, color=1):
    # Квадратная рамка
    for i in range(x, x + 10):
        oled.pixel(i, y, color)
        oled.pixel(i, y + 9, color)
    for j in range(y, y + 10):
        oled.pixel(x, j, color)
        oled.pixel(x + 9, j, color)

    # Иконка текста (лист с текстом)
    oled.pixel(x+1, y+1, color)
    oled.pixel(x+2, y+1, color)
    oled.pixel(x+3, y+1, color)
    oled.pixel(x+4, y+1, color)
    oled.pixel(x+5, y+1, color)
    oled.pixel(x+6, y+1, color)
    oled.pixel(x+7, y+1, color)

    oled.pixel(x+1, y+2, color)
    oled.pixel(x+1, y+3, color)
    oled.pixel(x+1, y+4, color)
    oled.pixel(x+1, y+5, color)
    oled.pixel(x+1, y+6, color)
    oled.pixel(x+1, y+7, color)

    oled.pixel(x+2, y+3, color)
    oled.pixel(x+2, y+5, color)
    oled.pixel(x+2, y+7, color)

    oled.pixel(x+3, y+3, color)
    oled.pixel(x+3, y+5, color)
    oled.pixel(x+3, y+7, color)

    oled.pixel(x+4, y+3, color)
    oled.pixel(x+4, y+5, color)
    oled.pixel(x+4, y+7, color)

    oled.pixel(x+5, y+3, color)
    oled.pixel(x+5, y+5, color)
    oled.pixel(x+5, y+7, color)

    oled.pixel(x+6, y+3, color)
    oled.pixel(x+6, y+5, color)
    oled.pixel(x+6, y+7, color)

    oled.pixel(x+7, y+2, color)
    oled.pixel(x+7, y+4, color)
    oled.pixel(x+7, y+6, color)
    oled.pixel(x+7, y+8, color)

def draw_music_icon(x, y, color=1):
    # Квадратная рамка
    for i in range(x, x + 10):
        oled.pixel(i, y, color)
        oled.pixel(i, y + 9, color)
    for j in range(y, y + 10):
        oled.pixel(x, j, color)
        oled.pixel(x + 9, j, color)

    # Иконка музыки (нотный стан с нотой)
    oled.pixel(x+1, y+2, color)
    oled.pixel(x+2, y+2, color)
    oled.pixel(x+3, y+2, color)
    oled.pixel(x+4, y+2, color)
    oled.pixel(x+5, y+2, color)
    oled.pixel(x+6, y+2, color)
    oled.pixel(x+7, y+2, color)
    oled.pixel(x+8, y+2, color)

    oled.pixel(x+1, y+4, color)
    oled.pixel(x+2, y+4, color)
    oled.pixel(x+3, y+4, color)
    oled.pixel(x+4, y+4, color)
    oled.pixel(x+5, y+4, color)
    oled.pixel(x+6, y+4, color)
    oled.pixel(x+7, y+4, color)
    oled.pixel(x+8, y+4, color)

    oled.pixel(x+3, y+5, color)
    oled.pixel(x+3, y+6, color)
    oled.pixel(x+4, y+6, color)
    oled.pixel(x+5, y+5, color)

def draw_other_icon(x, y, color=1):
    # Квадратная рамка
    for i in range(x, x + 10):
        oled.pixel(i, y, color)
        oled.pixel(i, y + 9, color)
    for j in range(y, y + 10):
        oled.pixel(x, j, color)
        oled.pixel(x + 9, j, color)

    # Иконка "прочее" (три точки в ряд)
    oled.pixel(x+2, y+4, color)
    oled.pixel(x+4, y+4, color)
    oled.pixel(x+6, y+4, color)

def draw_arrow_pixels(x, y, direction, color=1):
    """Рисует стрелку, используя пиксели.
    x, y: Координаты центра основания стрелки.
    direction: Направление стрелки ('up', 'down', 'left', 'right').
    color: Цвет (0 или 1).
    """

    if direction == 'up':
        oled.pixel(x, y - 2, color)
        oled.pixel(x - 1, y - 1, color)
        oled.pixel(x, y - 1, color)
        oled.pixel(x + 1, y - 1, color)
        oled.pixel(x - 2, y, color)
        oled.pixel(x - 1, y, color)
        oled.pixel(x, y, color)
        oled.pixel(x + 1, y, color)
        oled.pixel(x + 2, y, color)


    elif direction == 'down':
        oled.pixel(x, y + 2, color)
        oled.pixel(x - 1, y + 1, color)
        oled.pixel(x, y + 1, color)
        oled.pixel(x + 1, y + 1, color)
        oled.pixel(x - 2, y, color)
        oled.pixel(x - 1, y, color)
        oled.pixel(x, y, color)
        oled.pixel(x + 1, y, color)
        oled.pixel(x + 2, y, color)

    elif direction == 'left':
        oled.pixel(x - 2, y, color)
        oled.pixel(x - 1, y - 1, color)
        oled.pixel(x - 1, y, color)
        oled.pixel(x - 1, y + 1, color)
        oled.pixel(x, y - 2, color)
        oled.pixel(x, y - 1, color)
        oled.pixel(x, y, color)
        oled.pixel(x, y + 1, color)
        oled.pixel(x, y + 2, color)

    elif direction == 'right':
        oled.pixel(x + 2, y, color)
        oled.pixel(x + 1, y - 1, color)
        oled.pixel(x + 1, y, color)
        oled.pixel(x + 1, y + 1, color)
        oled.pixel(x, y - 2, color)
        oled.pixel(x, y - 1, color)
        oled.pixel(x, y, color)
        oled.pixel(x, y + 1, color)
        oled.pixel(x, y + 2, color)
        
    elif direction == 'left_f':
        oled.pixel(x - 2, y, color)
        oled.pixel(x - 1, y - 1, color)
        oled.pixel(x - 1, y, color)
        oled.pixel(x - 1, y + 1, color)
        oled.pixel(x, y - 1, color)
        oled.pixel(x, y, color)
        oled.pixel(x, y + 1, color)

    elif direction == 'right_f':
        oled.pixel(x + 2, y, color)
        oled.pixel(x + 1, y - 1, color)
        oled.pixel(x + 1, y, color)
        oled.pixel(x + 1, y + 1, color)
        oled.pixel(x, y - 1, color)
        oled.pixel(x, y, color)
        oled.pixel(x, y + 1, color)

def desktop(oled,button,button_1,button_2,button_3,led,led_1,top,root_wifi_conn,kop = False,kop_1 = False,kop_2 = False,kop_3 = False,kop_4 = False,kop_5 = False):
    global sch_00
    oled.fill(0)
    oled.rect(3, 3, 122, 58, 1)
    oled.rect(24,45,80,10,1)
    oled.text("welcome!",34,7)
    oled.text("enter you pass",8,22)
    oled.show()
    while True:
        if button.value() == 0:
            draw_arrow_pixels(znak_1[0], 50, 'right')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[0] = 0
            kop = True
        if button_1.value() == 0:
            draw_arrow_pixels(znak_1[0], 50, 'down')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[0] = 1
            kop = True
        if button_2.value() == 0:
            draw_arrow_pixels(znak_1[0], 50, 'up')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[0] = 2
            kop = True
        if button_3.value() == 0:
            draw_arrow_pixels(znak_1[0], 50, 'left')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[0] = 3
            kop = True
        if kop == True:
            break
    while True:
        if button.value() == 0:
            draw_arrow_pixels(znak_1[1], 50, 'right')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[1] = 0
            kop_1 = True
        if button_1.value() == 0:
            draw_arrow_pixels(znak_1[1], 50, 'down')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[1] = 1
            kop_1 = True
        if button_2.value() == 0:
            draw_arrow_pixels(znak_1[1], 50, 'up')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[1] = 2
            kop_1 = True
        if button_3.value() == 0:
            draw_arrow_pixels(znak_1[1], 50, 'left')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[1] = 3
            kop_1 = True
        if kop_1 == True:
            break
    while True:
        if button.value() == 0:
            draw_arrow_pixels(znak_1[2], 50, 'right')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[2] = 0
            kop_2 = True
        if button_1.value() == 0:
            draw_arrow_pixels(znak_1[2], 50, 'down')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[2] = 1
            kop_2 = True
        if button_2.value() == 0:
            draw_arrow_pixels(znak_1[2], 50, 'up')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[2] = 2
            kop_2 = True
        if button_3.value() == 0:
            draw_arrow_pixels(znak_1[2], 50, 'left')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[2] = 3
            kop_2 = True
        if kop_2 == True:
            break
    while True:
        if button.value() == 0:
            draw_arrow_pixels(znak_1[3], 50, 'right')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[3] = 0
            kop_3 = True
        if button_1.value() == 0:
            draw_arrow_pixels(znak_1[3], 50, 'down')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[3] = 1
            kop_3 = True
        if button_2.value() == 0:
            draw_arrow_pixels(znak_1[3], 50, 'up')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[3] = 2
            kop_3 = True
        if button_3.value() == 0:
            draw_arrow_pixels(znak_1[3], 50, 'left')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[3] = 3
            kop_3 = True
        if kop_3 == True:
            break
    while True:
        if button.value() == 0:
            draw_arrow_pixels(znak_1[4], 50, 'right')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[4] = 0
            kop_4 = True
        if button_1.value() == 0:
            draw_arrow_pixels(znak_1[4], 50, 'down')      # Стрелка вверх
            oled.show()
            top[4] = 1
            time.sleep(0.2)
            kop_4 = True
        if button_2.value() == 0:
            draw_arrow_pixels(znak_1[4], 50, 'up')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[4] = 2
            kop_4 = True
        if button_3.value() == 0:
            draw_arrow_pixels(znak_1[4], 50, 'left')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[4] = 3
            kop_4 = True
        if kop_4 == True:
            break
    while True:
        if button.value() == 0:
            draw_arrow_pixels(znak_1[5], 50, 'right')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[5] = 0
            kop_5 = True
        if button_1.value() == 0:
            draw_arrow_pixels(znak_1[5], 50, 'down')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[5] = 1
            kop_5 = True
        if button_2.value() == 0:
            draw_arrow_pixels(znak_1[5], 50, 'up')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[5] = 2
            kop_5 = True
        if button_3.value() == 0:
            draw_arrow_pixels(znak_1[5], 50, 'left')      # Стрелка вверх
            oled.show()
            time.sleep(0.2)
            top[5] = 3
            kop_5 = True
        if kop_5 == True:
            break
    if passtop == top:
        led.value(1)
        oled.fill(0)

        # Рамка вокруг логотипа
        oled.rect(5, 5, 118, 54, 1)

        # Верхняя линия
        oled.line(10, 15, 117, 15, 1)

        # Текст "GNOME ESP32"
        text = "GNOME ESP32"
        text_width = len(text) * 8
        x_position = (OLED_WIDTH - text_width) // 2
        oled.text(text, x_position, 25, 1)

        # Нижняя линия
        oled.line(10, 35, 117, 35, 1)

        # Текст "V1.1"
        version_text = "BETA"
        version_x = OLED_WIDTH - len(version_text) * 8 - 5 # Смещение вправо
        oled.text(version_text, version_x, 45, 1)

        # Отображаем на дисплее
        oled.show()
        time.sleep(7)
        led.value(0)
        ees = wifi(root_wifi_conn)
        oled.fill(0)
        oled.rect(3, 3, 122, 58, 1)
        oled.show()
        print(ees)
        while True:
            slide_all(root_wifi_conn)
           
           
              
                
                
             

            
       
    else:
        led_1.value(1)
        oled.fill(0)
        oled.rect(3, 3, 122, 58, 1)
        oled.text("invalid pass..",10,7)
        oled.text("restart the",20,22)
        oled.text("ESP32",40,36)
        oled.show()

        
        
         

                
        
    
    
    
  # Инициализация arrow_position
desktop(oled, button, button_1, button_2, button_3, led, led_1, top, root_wifi_conn)
    




