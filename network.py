import numpy as np

class NeuralNetwork:
    """
    Basit bir İleri Beslemeli Sinir Ağı (Feedforward Neural Network).
    Sensör verilerini alıp Hız (Speed/Acceleration) ve Direksiyon (Steering) çıktılarını üretir.
    Backpropagation (Geri yayılım) içermez, çünkü ağırlıklar genetik algoritma ile güncellenir.
    """
    def __init__(self, input_size=5, hidden_size=6, output_size=2):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Ağırlık matrisleri ve bias vektörlerini rastgele değerlerle (-1 ile 1 arası) başlatıyoruz.
        self.W1 = np.random.uniform(-1, 1, (self.input_size, self.hidden_size))
        self.b1 = np.random.uniform(-1, 1, (1, self.hidden_size))
        
        self.W2 = np.random.uniform(-1, 1, (self.hidden_size, self.output_size))
        
        # İlk jenerasyonların daha mantıklı hareket etmesi (ileri gitmeye daha meyilli olmaları) için 
        # Hız (index 0) bias'ını pozitif, Direksiyon (index 1) bias'ını sıfıra yakın başlatıyoruz.
        self.b2 = np.zeros((1, self.output_size))
        self.b2[0, 0] = 1.0  # Hızlanmayı teşvik et
        self.b2[0, 1] = 0.0  # Başlangıçta düz gitmeye teşvik et

    def _relu(self, x):
        """Gizli katman için ReLU aktivasyon fonksiyonu."""
        return np.maximum(0, x)

    def _tanh(self, x):
        """Çıkış katmanı için Tanh aktivasyon fonksiyonu (-1 ile 1 arası değer üretir)."""
        return np.tanh(x)

    def _sigmoid(self, x):
        """(Alternatif) 0 ile 1 arası değerler için Sigmoid."""
        return 1 / (1 + np.exp(-x))

    def forward(self, inputs):
        """
        Sensör verilerini alarak (5 boyutlu vektör) ağda ileri besleme yapar.
        Çıktı olarak Hız (ivmelenme 0 ile 1 arası) ve Direksiyon (-1 ile 1 arası) döner.
        """
        # Girişleri doğru boyutta (1, input_size) matrise çevir
        inputs = np.array(inputs).reshape(1, self.input_size)
        
        # Gizli katman hesaplaması
        z1 = np.dot(inputs, self.W1) + self.b1
        a1 = self._relu(z1)
        
        # Çıkış katmanı hesaplaması
        z2 = np.dot(a1, self.W2) + self.b2
        
        # 1. Çıkış: Hız/İvmelenme (Sigmoid kullanarak 0 ile 1 arası değer)
        # 2. Çıkış: Direksiyon (Tanh kullanarak -1 ile 1 arası değer, sağ/sol dönüş)
        acceleration = self._sigmoid(z2[0, 0])
        steering = self._tanh(z2[0, 1])
        
        return acceleration, steering

    def get_weights(self):
        """
        Genetik algoritma için tüm ağırlıkları (W1, b1, W2, b2) tek bir düz (1D) NumPy dizisi olarak döner.
        """
        return np.concatenate((
            self.W1.flatten(),
            self.b1.flatten(),
            self.W2.flatten(),
            self.b2.flatten()
        ))

    def set_weights(self, weights):
        """
        Genetik algoritmadan gelen 1D ağırlık dizisini matrislere bölerek sinir ağının ağırlıklarını günceller.
        """
        # Ağırlıkları bölmek için indeksleri hesapla
        idx1 = self.input_size * self.hidden_size
        idx2 = idx1 + self.hidden_size
        idx3 = idx2 + self.hidden_size * self.output_size
        
        # Böl ve matrislere yeniden şekillendir (reshape)
        self.W1 = weights[:idx1].reshape((self.input_size, self.hidden_size))
        self.b1 = weights[idx1:idx2].reshape((1, self.hidden_size))
        self.W2 = weights[idx2:idx3].reshape((self.hidden_size, self.output_size))
        self.b2 = weights[idx3:].reshape((1, self.output_size))
