package Knapsack;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

// Item sınıfı, bir eşyanın ağırlığını ve değerini temsil eder.
class Item {
    int weight; // Eşyanın ağırlığı
    int value;  // Eşyanın değeri

    // Item sınıfının yapıcı (constructor) metodu
    Item(int weight, int value) {
        this.weight = weight;
        this.value = value;
    }
}

public class Knapsack {

    public static void main(String[] args) {
        // Girdi dosyasının adı ve yolu
        String filename = "src//Knapsack//14";
        knapsackBruteForce(filename); // Dosya adını kullanarak knapsackBruteForce metodunu çağır
    }

    // knapsackBruteForce metodu, dosyadan verileri okuyarak sırt çantası problemini brute force yöntemi ile çözer.
    public static void knapsackBruteForce(String filename) {
        List<Item> items = new ArrayList<>(); // Eşyaların listesini tutan bir ArrayList
        int totalCapacity = 0; // Sırt çantasının toplam kapasitesi

        // Girdi dosyasını oku
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            totalCapacity = Integer.parseInt(br.readLine().trim()); // İlk satırda çantanın kapasitesi var

            String line;
            while ((line = br.readLine()) != null) {
                // Her satırda bir eşyanın ağırlığı ve değeri var
                String[] parts = line.trim().split("\\s+");
                int weight = Integer.parseInt(parts[0]);
                int value = Integer.parseInt(parts[1]);
                items.add(new Item(weight, value)); // Eşyayı listeye ekle
            }
        } catch (IOException e) {
            e.printStackTrace(); // Hata olursa yığın izini (stack trace) yazdır
            return;
        }

        int n = items.size(); // Eşyaların sayısı
        int bestValue = 0; // En iyi değeri tutan değişken
        int[] bestVector = new int[n]; // En iyi çözümü tutan vektör (binary form)
        int bestWeight = 0; // En iyi çözümün ağırlığını tutan değişken

        long startTime = System.currentTimeMillis(); // Algoritmanın başlangıç zamanı

        // Tüm olası kombinasyonları (2^n) dolaş
        int totalCombinations = (1 << n);
        for (int i = 0; i < totalCombinations; i++) {
            int currentWeight = 0; // Şu anki kombinasyonun toplam ağırlığı
            int currentValue = 0; // Şu anki kombinasyonun toplam değeri
            int[] currentVector = new int[n]; // Şu anki kombinasyonun vektörü

            // Her bir eşya için
            for (int j = 0; j < n; j++) {
                // Eğer j. eşya bu kombinasyonda varsa
                if ((i & (1 << j)) != 0) {
                    currentWeight += items.get(j).weight; // Ağırlığı ekle
                    currentValue += items.get(j).value; // Değeri ekle
                    currentVector[j] = 1; // Vektörde bu eşyayı işaretle
                } else {
                    currentVector[j] = 0; // Vektörde bu eşyayı işaretleme
                }
            }

            // Eğer bu kombinasyon çantanın kapasitesini aşmıyorsa ve önceki en iyi değerden daha iyiyse
            if (currentWeight <= totalCapacity && currentValue > bestValue) {
                bestValue = currentValue; // En iyi değeri güncelle
                bestWeight = currentWeight; // En iyi ağırlığı güncelle
                System.arraycopy(currentVector, 0, bestVector, 0, n); // En iyi vektörü güncelle
            }

            // Her 1000 kombinasyonda bir veya son kombinasyonda ilerleme durumu yazdır
            if (i % 1000 == 0 || i == totalCombinations - 1) {
                System.out.println("Checked " + (i + 1) + " / " + totalCombinations + " combinations...");
            }
        }

        long endTime = System.currentTimeMillis(); // Algoritmanın bitiş zamanı

        // Sonucu yazdır
        System.out.print("The best items: ");
        for (int j = 0; j < n; j++) {
            if (bestVector[j] == 1) {
                System.out.print("Item " + (j + 1) + " ");
            }
        }
        System.out.println();
        System.out.println("Total weight: " + bestWeight);
        System.out.println("Total value: " + bestValue);
        System.out.println("Running time: " + (endTime - startTime) / 1000.0 + " saniye");
    }
}

//Java 165.615 seconds
//C++  1344.23 seconds
//Python 2093.223423719406 seconds