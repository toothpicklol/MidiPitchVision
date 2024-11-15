import mido
import pygame
import sys

# 音樂檔案路徑 (轉換為 Pygame 支援的格式)
audio_file_path = 'Astronomia.mid'
midi_file_path = 'Astronomia.mid'
mid = mido.MidiFile(midi_file_path)

# Pygame 設定
pygame.init()
pygame.mixer.init()  # 初始化 Pygame 音樂播放
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('MIDI 音高視覺化')

# 色彩和其他參數
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
note_positions = []

# 解析 MIDI 並生成音符資料
current_time = 0
for msg in mid:
    current_time += msg.time  # 使用累計時間來得到絕對時間戳
    if msg.type == 'note_on' and msg.velocity > 0:
        note_positions.append((msg.note, current_time))

# 播放音樂
pygame.mixer.music.load(audio_file_path)
pygame.mixer.music.play()

# 視覺化更新
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()  # 取得開始時間
scroll_speed = 200  # 控制捲動速度（像素/秒）
x_offset = 0  # 記錄捲動的位移

while True:  # 持續執行，直到使用者退出
    screen.fill(WHITE)
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 取得經過的秒數

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 繪製音符
    for note, timestamp in note_positions:
        if timestamp <= elapsed_time:  # 當前音符的時間點已到
            # 計算音符的 x 座標（根據捲動時間和音符時間）
            x_pos = (timestamp - elapsed_time + (start_time / 1000)) * scroll_speed + x_offset
            y_pos = height - (note * 5)  # 根據音高調整 y 軸
            rect_width =30
            pygame.draw.rect(screen, BLACK, (x_pos, y_pos, rect_width, 5))

    pygame.display.flip()
    clock.tick(60)  # 每秒更新60次畫面
