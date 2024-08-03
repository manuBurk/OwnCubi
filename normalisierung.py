import matplotlib.pyplot as plt
import numpy as np

# Daten einlesen
goldline_points = [
    1078, 1535, 1086, 1274, 845, 1274, 793, 1112, 1329, 1643, 305, 1643, 458, 207, 305, 590,
    994, 207, 1329, 590, 577, 1026, 793, 590, 1329, 1277, 577, 1426, 458, 590, 994, 590, 577,
    1643, 1078, 1643, 305, 1026, 577, 1112, 1240, 1277, 305, 1426
]

user_points = [
    389, 830, 289, 830, 291, 940, 134, 941, 133, 829, 291, 832, 89, 829, 89, 705, 168, 701, 
    168, 677, 231, 677, 231, 831, 88, 829, 88, 522, 168, 522, 169, 676, 168, 520, 385, 520, 
    247, 629, 317, 631, 248, 627
]

# Helferfunktion zum Umformen der Punkte
def reshape_points(points):
    return np.array(points).reshape(-1, 2)

goldline_points = reshape_points(goldline_points)
user_points = reshape_points(user_points)

# Normierung der Punkte (Beispiel: Skalierung auf [0, 1])
def normalize_points(points):
    min_vals = np.min(points, axis=0)
    max_vals = np.max(points, axis=0)
    return (points - min_vals) / (max_vals - min_vals)

goldline_points_normalized = normalize_points(goldline_points)
user_points_normalized = normalize_points(user_points)

# Plot der beiden Grundrisse
plt.figure(figsize=(10, 8))
plt.plot(goldline_points_normalized[:, 0], goldline_points_normalized[:, 1], label='Goldline', marker='o')
plt.plot(user_points_normalized[:, 0], user_points_normalized[:, 1], label='User', marker='x')
plt.legend()
plt.title('Vergleich der Grundrisse')
plt.xlabel('X-Koordinate (normalisiert)')
plt.ylabel('Y-Koordinate (normalisiert)')
plt.show()

# Berechnung der Abweichungen
def calculate_deviation(points1, points2):
    deviations = []
    for p1 in points1:
        distances = np.linalg.norm(points2 - p1, axis=1)
        min_distance = np.min(distances)
        deviations.append(min_distance)
    return deviations

deviations = calculate_deviation(goldline_points_normalized, user_points_normalized)
average_deviation = np.mean(deviations)
max_deviation = np.max(deviations)

print(f'Durchschnittliche Abweichung: {average_deviation}')
print(f'Maximale Abweichung: {max_deviation}')
