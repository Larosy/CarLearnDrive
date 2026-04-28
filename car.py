import pygame
import math
import numpy as np
from network import NeuralNetwork

class Car:
    def __init__(self, x, y):
        # Konum ve Fizik
        self.x = x
        self.y = y
        self.angle = 90  # 90 derece = yukarı bakar (Pygame koordinatlarına göre ayarlayacağız)
        self.speed = 0
        self.max_speed = 5.0
        self.min_speed = 0.5  # Geri gitmesini engellemek için
        
        # Durum ve Fitness
        self.alive = True
        self.distance = 0.0  # Fitness skoru olarak kullanılacak
        
        # Sensörler (Ray-casting)
        self.radars = []  # [(x, y, distance), ...] her bir sensörün değdiği nokta
        self.sensor_angles = [-60, -30, 0, 30, 60]  # Araca göre sensör açıları
        self.sensor_max_len = 150
        
        # Beyin (Sinir Ağı)
        self.brain = NeuralNetwork(input_size=5, hidden_size=6, output_size=2)
        
        # Araç boyutu
        self.width = 14
        self.length = 28

    def _check_collision(self, track_surface):
        """Arabanın 4 köşesinden herhangi birinin beyaz (duvar) olup olmadığını kontrol eder."""
        self.alive = True
        
        # Arabanın 4 köşesini hesapla
        left_top = [self.x + math.cos(math.radians(360 - (self.angle + 30))) * self.length/2, 
                    self.y + math.sin(math.radians(360 - (self.angle + 30))) * self.length/2]
        right_top = [self.x + math.cos(math.radians(360 - (self.angle + 150))) * self.length/2, 
                     self.y + math.sin(math.radians(360 - (self.angle + 150))) * self.length/2]
        left_bottom = [self.x + math.cos(math.radians(360 - (self.angle + 210))) * self.length/2, 
                       self.y + math.sin(math.radians(360 - (self.angle + 210))) * self.length/2]
        right_bottom = [self.x + math.cos(math.radians(360 - (self.angle + 330))) * self.length/2, 
                        self.y + math.sin(math.radians(360 - (self.angle + 330))) * self.length/2]
        
        corners = [left_top, right_top, left_bottom, right_bottom]
        
        for corner in corners:
            cx, cy = int(corner[0]), int(corner[1])
            # Ekran sınırlarını aşarsa veya beyaz piksele (duvara) değerse ölür
            if cx < 0 or cx >= track_surface.get_width() or cy < 0 or cy >= track_surface.get_height():
                self.alive = False
                break
            
            # Yüzeydeki piksel rengini al
            color = track_surface.get_at((cx, cy))
            # Eğer beyaz renk ise (duvar) -> Kaza yapmıştır
            if color[0] > 200 and color[1] > 200 and color[2] > 200:
                self.alive = False
                break
                
        if not self.alive:
            self.distance -= 50  # Çarpma cezası

    def _update_sensors(self, track_surface):
        """5 adet sensör için ışın (ray) atar ve duvarlara olan mesafeyi ölçer."""
        self.radars.clear()
        
        for angle_offset in self.sensor_angles:
            sensor_angle = (360 - (self.angle + angle_offset)) % 360
            distance = 0
            
            x = int(self.x)
            y = int(self.y)
            
            # Işını adım adım ilerlet
            while distance < self.sensor_max_len:
                nx = int(self.x + math.cos(math.radians(sensor_angle)) * distance)
                ny = int(self.y + math.sin(math.radians(sensor_angle)) * distance)
                
                # Ekran sınırları kontrolü
                if nx < 0 or nx >= track_surface.get_width() or ny < 0 or ny >= track_surface.get_height():
                    break
                    
                # Duvar (beyaz piksel) kontrolü
                color = track_surface.get_at((nx, ny))
                if color[0] > 200 and color[1] > 200 and color[2] > 200:
                    break
                    
                distance += 1
                x, y = nx, ny
                
            self.radars.append((x, y, distance))

    def get_data(self):
        """Sensör mesafelerini normalize ederek (0 ile 1 arası) ağa vermek için hazırlar."""
        normalized_distances = []
        for radar in self.radars:
            # radars -> (x, y, distance)
            dist = radar[2]
            normalized_distances.append(dist / self.sensor_max_len)
        return normalized_distances

    def update(self, track_surface):
        """Arabanın durumunu bir adım günceller."""
        if not self.alive:
            return

        # 1. Sensörleri güncelle (Etrafı algıla)
        self._update_sensors(track_surface)
        
        # 2. Beyne sensör verisini ver ve karar al
        inputs = self.get_data()
        acceleration, steering = self.brain.forward(inputs)
        
        # acceleration: 0 ile 1 arası, steering: -1 ile 1 arası
        # 3. Alınan kararı fizik kurallarına uygula
        # Hız kontrolü
        self.speed += (acceleration - 0.5) * 2.0  # -1 ile 1 arası ivmelenme
        self.speed = max(self.min_speed, min(self.speed, self.max_speed))
        
        # Direksiyon kontrolü (Sadece hareket ediyorsa dönebilir)
        if self.speed > 0:
            self.angle += steering * 5.0  # Maksimum dönüş hızı
            
        # 4. Konumu güncelle
        self.x += math.cos(math.radians(360 - self.angle)) * self.speed
        self.y += math.sin(math.radians(360 - self.angle)) * self.speed
        
        # 5. Kaza kontrolü yap
        self._check_collision(track_surface)
        
        # 6. Yaşıyorsa mesafe kazan (Fitness artışı)
        if self.alive:
            # Sadece kendi etrafında dönen arabaları cezalandırmak için,
            # direksiyonu ne kadar az kırarsa o kadar fazla puan almasını sağlıyoruz.
            self.distance += self.speed * (1.0 - abs(steering) * 0.6)

    def draw(self, screen):
        """Arabayı ve sensör ışınlarını ekrana çizer."""
        if not self.alive:
            # Ölü arabalar daha soluk çizilebilir
            return

        # Arabayı çizmek için Pygame Surface kullanımı (Döndürme işlemi)
        car_surface = pygame.Surface((self.length, self.width), pygame.SRCALPHA)
        car_surface.fill((0, 150, 255))  # Mavi araba
        
        # Yönü göstermek için ön tarafına küçük kırmızı bir işaret koy
        pygame.draw.rect(car_surface, (255, 0, 0), (self.length - 4, 0, 4, self.width))
        
        # Döndürme
        rotated_surface = pygame.transform.rotate(car_surface, self.angle)
        rect = rotated_surface.get_rect(center=(self.x, self.y))
        
        screen.blit(rotated_surface, rect.topleft)
        
        # Sensörleri çiz
        for radar in self.radars:
            radar_x, radar_y, _ = radar
            pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (radar_x, radar_y), 1)
            pygame.draw.circle(screen, (0, 255, 0), (radar_x, radar_y), 3)