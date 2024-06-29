import numpy as np
import random
import math
import pandas as pd

# TSP verilerini dosyadan yüklemek için fonksiyon
# Girdi: Dosya yolu
# Çıktı: İki boyutlu numpy matrisi (komşuluk matrisi)
def load_tsp_data(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        # Satırları oku ve matrise çevir
        matrix = [list(map(int, line.strip().split())) for line in lines]
    return np.array(matrix)

# Başlangıç çözümü oluşturma fonksiyonu
# Girdi: Şehir sayısı
# Çıktı: Rastgele bir şehir sıralaması (başlangıç çözümü)
def initial_solution(num_cities):
    return list(np.random.permutation(num_cities))

# Toplam mesafeyi hesaplama fonksiyonu
# Girdi: Komşuluk matrisi ve çözüm
# Çıktı: Verilen çözümün toplam mesafesi
def calculate_total_distance(matrix, solution):
    distance = 0
    num_cities = len(solution)
    for i in range(num_cities):
        # Her şehirden bir sonrakine olan mesafeyi ekle
        distance += matrix[solution[i]][solution[(i + 1) % num_cities]]
    return distance

# Komşu şehirleri yer değiştirme fonksiyonu
# Girdi: Mevcut çözüm
# Çıktı: İki komşu şehrin yer değiştirilmesiyle oluşan yeni çözüm
def swap_neighboring_cities(solution):
    new_solution = solution.copy()
    # Rastgele bir pozisyon seç
    i = random.randint(0, len(solution) - 2)
    # Seçilen pozisyon ve bir sonrasındaki şehirlerin yerini değiştir
    new_solution[i], new_solution[i + 1] = new_solution[i + 1], new_solution[i]
    return new_solution

# Simulated Annealing algoritması
# Girdi: Komşuluk matrisi, başlangıç sıcaklığı, soğutma oranı, iterasyon sayısı
# Çıktı: En iyi çözüm, en iyi çözümün maliyeti ve tüm çözümler
def simulated_annealing(matrix, initial_temp, cooling_rate, num_iterations):
    num_cities = len(matrix)
    current_solution = initial_solution(num_cities)  # Başlangıç çözümü oluştur
    current_cost = calculate_total_distance(matrix, current_solution)  # Başlangıç çözümünün maliyetini hesapla

    best_solution = current_solution  # En iyi çözüm olarak başlangıç çözümünü belirle
    best_cost = current_cost  # En iyi çözüm maliyeti

    temperature = initial_temp  # Başlangıç sıcaklığı

    all_solutions = [current_solution]  # Tüm çözümleri sakla

    for iteration in range(num_iterations):
        new_solution = swap_neighboring_cities(current_solution)  # Yeni çözüm üret
        new_cost = calculate_total_distance(matrix, new_solution)  # Yeni çözümün maliyetini hesapla

        # Yeni çözümü kabul etme kriteri
        if new_cost < current_cost or math.exp((current_cost - new_cost) / temperature) > random.random():
            current_solution = new_solution
            current_cost = new_cost

        # En iyi çözümü güncelle
        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost

        all_solutions.append(current_solution)  # Mevcut çözümü sakla

        temperature *= cooling_rate  # Sıcaklığı soğutma oranına göre azalt

    return best_solution, best_cost, all_solutions

# Parametreler
initial_temp = 10000  # Başlangıç sıcaklığı
cooling_rate = 0.995  # Soğutma oranı
num_iterations = 10000  # Iterasyon sayısı

# Verileri yükle
matrix = load_tsp_data(r'AiToolsPython\LocalSearch\tsp_data.txt')

# Simulated Annealing algoritmasını çalıştır
best_solution, best_cost, all_solutions = simulated_annealing(matrix, initial_temp, cooling_rate, num_iterations)

# Tüm çözümleri daha iyi görüntülemek için bir DataFrame'e dönüştür
df_all_solutions = pd.DataFrame(all_solutions)

# Çözümleri CSV dosyasına kaydet (isteğe bağlı)
df_all_solutions.to_csv('all_solutions.csv', index=False)

# Sonuçları yazdır
print("Tüm aranan çözümler:")
print(df_all_solutions)

print("\nBulunan en iyi çözüm:")
print(best_solution)
print("En iyi çözümün toplam mesafesi:")
print(best_cost)
