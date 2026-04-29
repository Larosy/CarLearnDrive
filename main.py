import pygame
import sys
from evolution import GeneticAlgorithm

# --- Sabitler ---
WIDTH, HEIGHT = 1200, 800
FPS = 60

# Renkler
WHITE = (255, 255, 255) # Duvarlar
BLACK = (30, 30, 30)    # Yol (Pist)

def get_map_data(map_index):
    """Haritaya göre yol noktalarını, yol kalınlığını ve başlangıç noktasını döndürür."""
    if map_index == 0:
        # Harita 1: Basit Klasik Pist
        points = [(150, 450), (150, 150), (400, 150), (600, 350), (800, 150), (1050, 150), (1050, 650), (600, 650), (400, 500), (150, 650)]
        start_pos = (150, 450)
        road_width = 150
    elif map_index == 1:
        # Harita 2: Basit Oval
        points = [(200, 400), (200, 200), (1000, 200), (1000, 600), (200, 600)]
        start_pos = (200, 400)
        road_width = 150
    else:
        # Harita 3: Zorlu Zikzak (Kıvrımlı, Dar)
        points = [(100, 700), (100, 100), (400, 100), (400, 700), (700, 700), (700, 100), (1000, 100), (1000, 700)]
        start_pos = (100, 600)
        road_width = 150
        
    return points, start_pos, road_width

def draw_track(surface, map_index):
    """Seçilen harita indexine göre pisti çizer ve başlangıç noktasını döner."""
    surface.fill(WHITE)
    points, start_pos, road_width = get_map_data(map_index)
    
    # Harita 3 (Zikzak) açık uçlu bir yol, diğerleri kapalı bir çember (loop)
    is_closed = (map_index != 2)
    pygame.draw.lines(surface, BLACK, closed=is_closed, points=points, width=road_width)
    
    # Kırık çizgileri yumuşatmak için bağlantı noktalarına daire çiz
    for p in points:
        pygame.draw.circle(surface, BLACK, p, road_width // 2)

    # Başlangıç noktasını yeşil bir yuvarlakla işaretle (Görsel amaçlı)
    pygame.draw.circle(surface, (0, 200, 0), start_pos, 15)
    return start_pos

def main_menu(screen, clock):
    font_title = pygame.font.SysFont("Arial", 50, bold=True)
    font_sub = pygame.font.SysFont("Arial", 30)
    
    while True:
        screen.fill((240, 240, 240))
        title = font_title.render("Neuroevolution Car AI", True, (0, 0, 0))
        sub = font_sub.render("Press ENTER to Begin Configuration", True, (0, 150, 0))
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 20))
        
        pygame.display.flip()
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def parameter_menu(screen, clock):
    font_title = pygame.font.SysFont("Arial", 40, bold=True)
    font_item = pygame.font.SysFont("Arial", 30)
    font_hint = pygame.font.SysFont("Arial", 20)
    
    pop_options = [20, 50, 100, 200]
    mut_options = [0.01, 0.05, 0.1, 0.2]
    
    pop_idx = 1 # Default: 50
    mut_idx = 2 # Default: 0.1
    selected = 0 # 0: Population, 1: Mutation
    
    while True:
        screen.fill((240, 240, 240))
        title = font_title.render("Set Evolution Parameters", True, (0, 0, 0))
        hint = font_hint.render("Use UP/DOWN to select, LEFT/RIGHT to change, ENTER to confirm", True, (100, 100, 100))
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        
        # Seçili olanı yeşil göster
        color_pop = (0, 150, 0) if selected == 0 else (0, 0, 0)
        color_mut = (0, 150, 0) if selected == 1 else (0, 0, 0)
        
        pop_text = font_item.render(f"Population Size:  <  {pop_options[pop_idx]}  >", True, color_pop)
        mut_text = font_item.render(f"Mutation Rate:  <  {mut_options[mut_idx]}  >", True, color_mut)
        
        screen.blit(pop_text, (WIDTH//2 - pop_text.get_width()//2, 300))
        screen.blit(mut_text, (WIDTH//2 - mut_text.get_width()//2, 400))
        
        pygame.display.flip()
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected = 1 - selected
                elif event.key == pygame.K_LEFT:
                    if selected == 0: pop_idx = max(0, pop_idx - 1)
                    else: mut_idx = max(0, mut_idx - 1)
                elif event.key == pygame.K_RIGHT:
                    if selected == 0: pop_idx = min(len(pop_options)-1, pop_idx + 1)
                    else: mut_idx = min(len(mut_options)-1, mut_idx + 1)
                elif event.key == pygame.K_RETURN:
                    return pop_options[pop_idx], mut_options[mut_idx]

def map_selection_menu(screen, clock):
    font_title = pygame.font.SysFont("Arial", 40, bold=True)
    font_item = pygame.font.SysFont("Arial", 30)
    font_hint = pygame.font.SysFont("Arial", 20)
    
    maps = ["1. Classic Track", "2. Simple Oval", "3. Hard Zigzag"]
    selected = 0
    
    while True:
        screen.fill((240, 240, 240))
        title = font_title.render("Select Map", True, (0, 0, 0))
        hint = font_hint.render("Use UP/DOWN to select, ENTER to confirm", True, (100, 100, 100))
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 160))
        
        for i, m in enumerate(maps):
            color = (0, 150, 0) if i == selected else (0, 0, 0)
            text = font_item.render(f"> {m} <" if i == selected else f"  {m}  ", True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 280 + i * 80))
            
        pygame.display.flip()
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = max(0, selected - 1)
                elif event.key == pygame.K_DOWN:
                    selected = min(len(maps)-1, selected + 1)
                elif event.key == pygame.K_RETURN:
                    return selected

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neuroevolution Car Simulation")
    clock = pygame.time.Clock()

    # 1. Ana Giriş Ekranı
    main_menu(screen, clock)
    
    # 2. Parametre Ayarlama Menüsü
    pop_size, mut_rate = parameter_menu(screen, clock)
    
    # 3. Harita Seçim Menüsü
    map_index = map_selection_menu(screen, clock)

    # Seçilen Haritayı Çiz ve Başlangıç Noktasını Al
    track_surface = pygame.Surface((WIDTH, HEIGHT))
    start_pos = draw_track(track_surface, map_index)
    start_x, start_y = start_pos

    # Genetik Algoritmayı Kullanıcı Parametreleriyle Başlat
    ga = GeneticAlgorithm(population_size=pop_size, mutation_rate=mut_rate)
    cars = ga.create_initial_population(start_x, start_y)

    generation_font = pygame.font.SysFont("Arial", 30)
    info_font = pygame.font.SysFont("Arial", 20)

    # Ana Döngü
    running = True
    frame_count = 0
    max_frames = 20 * FPS # Her nesil için maksimum 20 saniye süre

    while running:
        frame_count += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Ekranı temizle ve pisti çiz
        screen.blit(track_surface, (0, 0))

        alive_count = 0
        
        # Tüm arabaları güncelle ve çiz
        for car in cars:
            if car.alive:
                alive_count += 1
            car.update(track_surface)
            car.draw(screen)

        # Süre dolduysa veya hiç araba kalmadıysa yeni nesle geç
        if alive_count == 0 or frame_count > max_frames:
            print(f"Generation {ga.generation} bitti. Yeni nesil üretiliyor...")
            cars = ga.next_generation(cars, start_x, start_y)
            frame_count = 0 # Sayacı sıfırla

        # Bilgileri ekrana yazdır
        gen_text = generation_font.render(f"Generation: {ga.generation}", True, (0, 0, 0))
        alive_text = info_font.render(f"Alive: {alive_count} / {pop_size}", True, (0, 0, 0))
        time_text = info_font.render(f"Time: {frame_count // FPS} / {max_frames // FPS}s", True, (0, 0, 0))
        
        # Yazıları beyaz zemin üzerine (sol üst) koyalım ki net okunsun
        screen.blit(gen_text, (20, 20))
        screen.blit(alive_text, (20, 60))
        screen.blit(time_text, (20, 90))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
