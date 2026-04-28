import numpy as np
import random
from car import Car

class GeneticAlgorithm:
    def __init__(self, population_size=50, mutation_rate=0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generation = 1

    def create_initial_population(self, start_x, start_y):
        """İlk nesli tamamen rastgele ağırlıklarla (NeuralNetwork default) başlatır."""
        population = []
        for _ in range(self.population_size):
            car = Car(start_x, start_y)
            population.append(car)
        return population

    def crossover(self, parent1_weights, parent2_weights):
        """
        İki ebeveynin ağırlıklarını tek noktadan (veya uniform) çaprazlar.
        Burada rastgele bir noktadan bölme (Single-point crossover) veya maske (Uniform crossover) kullanılabilir.
        Uniform crossover uyguluyoruz: Her bir ağırlık %50 ihtimalle anne veya babadan gelir.
        """
        mask = np.random.rand(len(parent1_weights)) > 0.5
        child_weights = np.where(mask, parent1_weights, parent2_weights)
        return child_weights

    def mutate(self, weights):
        """
        Belirli bir olasılıkla (mutation_rate) genleri (ağırlıkları) rastgele değiştirir.
        Gaussian Noise (Normal dağılımlı gürültü) ekliyoruz.
        """
        for i in range(len(weights)):
            if random.random() < self.mutation_rate:
                # -0.5 ile 0.5 arasında rastgele bir gürültü ekle
                weights[i] += np.random.normal(0, 0.5)
                # Ağırlıkların çok fazla büyümemesi için sınırlayabiliriz
                weights[i] = np.clip(weights[i], -5.0, 5.0)
        return weights

    def next_generation(self, current_population, start_x, start_y):
        """
        Geçerli popülasyonun fitness değerlerine göre yeni bir nesil üretir.
        En iyi %10 doğrudan yeni nesle geçer (Elitizm).
        Geri kalan %90 elitlerden seçilip çaprazlanıp mutasyona uğratılır.
        """
        # Arabaları fitness (gidilen mesafe) değerlerine göre büyükten küçüğe sırala
        current_population.sort(key=lambda x: x.distance, reverse=True)
        
        new_population = []
        
        # 1. Elitizm: En iyi %10'u doğrudan koru
        elite_count = int(self.population_size * 0.1)
        if elite_count < 2:
            elite_count = 2 # Çaprazlama için en az 2 elit lazım
            
        elites = current_population[:elite_count]
        
        # Elitleri klonlayıp yeni nesle ekle (Aynı ağırlıklar, yeni pozisyon, sıfırlanmış mesafe)
        for elite in elites:
            car = Car(start_x, start_y)
            car.brain.set_weights(elite.brain.get_weights())
            new_population.append(car)
            
        # 2. Crossover & Mutation: Kalan %90'ı üret
        while len(new_population) < self.population_size:
            # Elitler arasından rastgele iki ebeveyn seç (veya rulet tekerleği kullanılabilir, basitlik için rastgele)
            parent1 = random.choice(elites)
            parent2 = random.choice(elites)
            
            p1_weights = parent1.brain.get_weights()
            p2_weights = parent2.brain.get_weights()
            
            # Çaprazlama yap
            child_weights = self.crossover(p1_weights, p2_weights)
            
            # Mutasyon uygula
            child_weights = self.mutate(child_weights)
            
            # Yeni arabayı oluştur ve ağını ayarla
            child = Car(start_x, start_y)
            child.brain.set_weights(child_weights)
            new_population.append(child)
            
        self.generation += 1
        return new_population
