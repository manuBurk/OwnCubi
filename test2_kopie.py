import numpy as np
import json
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
import json
from datetime import datetime
from collections import defaultdict
from order import sort_and_rearrange_components, process_components
from wall_lines_points import print_corners_by_lines, print_segmentpoints_by_lines, wall_lines_order
from conectedLinesTest import process_components, split_chain, extend_chain


#Wall_lines und wall_points extrahiert aus den svg Datein mit test_val2.py

# #/high_quality_architectural/199
# wall_lines=[(10, 0, 2), (1, 10, 2), (12, 2, 2), (15, 2, 2), (9, 3, 2), (3, 12, 2), (16, 4, 2), (4, 14, 2), (5, 8, 2), (5, 16, 2), (7, 6, 2), (8, 9, 2), (8, 13, 2), (10, 15, 2), (13, 14, 2), (16, 13, 2), (14, 15, 2)]
# wall_points=[[348, 308, 0, 1, 1.0], [267, 308, 0, 3, 1.0], [529, 427, 1, 0, 1.0], [405, 243, 1, 1, 1.0], [42, 427, 1, 1, 1.0], [42, 53, 1, 2, 1.0], [538, 49, 1, 3, 1.0], [510, 49, 2, 0, 1.0], [189, 53, 2, 0, 1.0], [405, 53, 2, 0, 1.0], [308, 308, 2, 0, 1.0], [538, 49, 2, 1, 1.0], [529, 243, 2, 1, 1.0], [189, 294, 2, 1, 1.0], [189, 427, 2, 2, 1.0], [308, 427, 2, 2, 1.0], [42, 294, 2, 3, 1.0], [510, 49, 3, 0, 1.0]]

# #/high_quality_architectural/1191/
wall_lines=[(0, 13, 8), (1, 14, 8), (30, 2, 8), (22, 3, 8), (10, 4, 2), (24, 5, 8), (8, 13, 8), (9, 45, 8), (47, 11, 2), (42, 11, 2), (35, 12, 2), (43, 12, 2), (46, 14, 8), (31, 15, 2), (15, 42, 2), (49, 16, 2), (16, 38, 2), (38, 17, 2), (17, 32, 2), (52, 18, 2), (18, 44, 2), (19, 24, 8), (20, 27, 2), (20, 51, 2), (21, 35, 2), (21, 36, 2), (22, 41, 8), (23, 46, 2), (25, 50, 2), (49, 25, 2), (26, 40, 2), (53, 26, 2), (27, 28, 2), (27, 48, 2), (28, 33, 2), (28, 34, 2), (29, 30, 2), (29, 49, 2), (47, 29, 2), (30, 35, 2), (31, 34, 2), (48, 31, 2), (32, 43, 2), (32, 46, 2), (33, 47, 2), (34, 42, 2), (36, 43, 2), (50, 36, 2), (48, 37, 2), (37, 39, 2), (51, 37, 2), (50, 38, 2), (39, 53, 2), (52, 39, 2), (40, 45, 2), (44, 40, 2), (45, 41, 2), (53, 44, 2), (51, 52, 2)]
wall_points=[[834, 221, 0, 0, 1.0], [796, 426, 0, 0, 1.0], [836, 138, 0, 1, 1.0], [453, 368, 0, 1, 1.0], [506, 539, 0, 1, 1.0], [599, 88, 0, 2, 1.0], [424, 539, 0, 2, 1.0], [540, 539, 0, 2, 1.0], [794, 373, 0, 3, 1.0], [88, 505, 0, 3, 1.0], [456, 539, 0, 3, 1.0], [451, 290, 1, 0, 1.0], [793, 323, 1, 0, 1.0], [834, 373, 1, 0, 1.0], [796, 506, 1, 0, 1.0], [262, 290, 1, 1, 1.0], [594, 290, 1, 1, 1.0], [640, 323, 1, 1, 1.0], [49, 436, 1, 1, 1.0], [457, 60, 1, 2, 1.0], [49, 97, 1, 2, 1.0], [726, 219, 1, 2, 1.0], [424, 368, 1, 2, 1.0], [540, 506, 1, 2, 1.0], [599, 60, 1, 3, 1.0], [640, 219, 1, 3, 1.0], [259, 368, 1, 3, 1.0], [171, 97, 2, 0, 1.0], [337, 97, 2, 0, 1.0], [594, 138, 2, 0, 1.0], [793, 138, 2, 0, 1.0], [262, 213, 2, 0, 1.0], [688, 323, 2, 0, 1.0], [451, 97, 2, 1, 1.0], [337, 213, 2, 1, 1.0], [793, 219, 2, 1, 1.0], [726, 242, 2, 1, 1.0], [171, 255, 2, 1, 1.0], [640, 290, 2, 1, 1.0], [171, 326, 2, 1, 1.0], [259, 436, 2, 1, 1.0], [424, 505, 2, 1, 1.0], [337, 290, 2, 2, 1.0], [726, 323, 2, 2, 1.0], [171, 436, 2, 2, 1.0], [259, 505, 2, 2, 1.0], [688, 506, 2, 2, 1.0], [451, 138, 2, 3, 1.0], [171, 213, 2, 3, 1.0], [594, 219, 2, 3, 1.0], [640, 242, 2, 3, 1.0], [49, 255, 2, 3, 1.0], [49, 326, 2, 3, 1.0], [171, 368, 2, 3, 1.0]]


#high_quality_architecture 18
#output /nethome/lkiefer/pogo/CubiCasa5k/output_20240725_120636.json
#json  (35)
# wall_lines = [(0, 17, 2), (2, 1, 2), (11, 3, 2), (19, 3, 2), (12, 4, 2), (17, 4, 2), (21, 5, 2), (5, 16, 2), (6, 8, 8), (6, 14, 8), (7, 14, 2), (7, 18, 2), (8, 15, 8), (9, 12, 2), (15, 9, 2), (10, 19, 2), (18, 10, 2), (11, 15, 2), (14, 11, 2), (20, 12, 2), (19, 13, 2), (13, 16, 2), (21, 13, 2), (16, 17, 2), (18, 21, 2)]
# wall_points = [[1078, 1535, 0, 0, 1.0], [1086, 1274, 0, 1, 1.0], [845, 1274, 0, 3, 1.0], [793, 1112, 1, 0, 1.0], [1329, 1643, 1, 0, 1.0], [305, 1643, 1, 1, 1.0], [458, 207, 1, 2, 1.0], [305, 590, 1, 2, 1.0], [994, 207, 1, 3, 1.0], [1329, 590, 1, 3, 1.0], [577, 1026, 1, 3, 1.0], [793, 590, 2, 0, 1.0], [1329, 1277, 2, 1, 1.0], [577, 1426, 2, 1, 1.0], [458, 590, 2, 2, 1.0], [994, 590, 2, 2, 1.0], [577, 1643, 2, 2, 1.0], [1078, 1643, 2, 2, 1.0], [305, 1026, 2, 3, 1.0], [577, 1112, 2, 3, 1.0], [1240, 1277, 2, 3, 1.0], [305, 1426, 2, 3, 1.0]]

#high_quality_architecture 2536
#output /nethome/lkiefer/pogo/CubiCasa5k/output_20240725_122030.json
#json 36
# wall_lines=[(0, 9, 2), (15, 1, 2), (12, 1, 2), (14, 2, 2), (19, 2, 2), (13, 3, 2), (3, 16, 2), (22, 4, 2), (4, 18, 2), (5, 7, 8), (5, 20, 2), (6, 13, 2), (6, 15, 2), (7, 23, 2), (8, 14, 2), (11, 8, 2), (9, 19, 2), (10, 11, 2), (10, 16, 2), (23, 10, 2), (11, 17, 2), (12, 18, 2), (22, 12, 2), (23, 13, 2), (17, 14, 2), (21, 15, 2), (16, 17, 2), (18, 19, 2), (20, 23, 2), (20, 21, 2), (21, 22, 2)]
# wall_points=[[195, 350, 0, 3, 0.9797987], [138, 389, 1, 0, 0.9797987], [597, 469, 1, 0, 0.9797987], [193, 284, 1, 1, 0.9797987], [30, 469, 1, 1, 0.9797987], [30, 35, 1, 2, 0.9797987], [138, 202, 1, 2, 0.9797987], [193, 35, 1, 3, 0.9797987], [597, 95, 1, 3, 0.9797987], [284, 350, 1, 3, 0.9797987], [318, 95, 2, 0, 0.9797987], [440, 95, 2, 0, 0.9797987], [77, 389, 2, 0, 0.9797987], [193, 202, 2, 1, 0.9797987], [597, 284, 2, 1, 0.9797987], [138, 317, 2, 1, 0.9797987], [318, 284, 2, 2, 0.9797987], [440, 284, 2, 2, 0.9797987], [77, 469, 2, 2, 0.9797987], [284, 469, 2, 2, 0.9797987], [30, 95, 2, 3, 0.9797987], [30, 317, 2, 3, 0.9797987], [30, 389, 2, 3, 0.9797987], [193, 95, 3, 0, 0.9797987]]


#entfernen der nicht relevaten werte
first_two_wall_point_values = [[sublist[0], sublist[1]] for sublist in wall_points]
first_two_wall_lines = [(line[0], line[1]) for line in wall_lines]
print("first two wall points", first_two_wall_point_values)


#-1000 für die darstellung "segmentpoints" -> in flowculate ist die y achse verkehrt herum 
reversed_wall_points = [(line[0], 1000-line[1]) for line in first_two_wall_point_values]
print("wallPoints (nur x, y, y umgekehrter Wert):")
print(reversed_wall_points)

print("Aktualisierte wall_lines (nur Punkt1, Punkt2):")
print(first_two_wall_lines)
anzahl_wall_points = int(len(first_two_wall_lines)/2)
print(anzahl_wall_points)


#zusammenhängende Punkte  gruppieren
# Schritt 1: Graph erstellen
# Graph-Adjazenzliste
graph = defaultdict(list)

# Erstellen des Graphen
for line in first_two_wall_lines:
    if line[0] != line[1]:  # Selbstverbindungen ignorieren
        graph[line[0]].append(line[1])
        graph[line[1]].append(line[0])


# Funktion zur Tiefensuche, um verbundene Komponenten zu finden
def dfs(node, visited, component):
    stack = [node]
    while stack:
        current = stack.pop()
        if current not in visited:
            visited.add(current)
            component.append(current)
            for neighbor in graph[current]:
                if neighbor not in visited:
                    stack.append(neighbor)


# Schritt 2: Finden der verbundenen Komponenten
visited = set()
components = []

for node in graph:
    if node not in visited:
        component = []
        dfs(node, visited, component)
        components.append(component)

# Schritt 3: Linien in jeder Komponente sammeln und sortieren
connected_lines = []

for component in components:
    lines = []
    for line in first_two_wall_lines:
        if line[0] in component and line[1] in component:
            lines.append(line)
    connected_lines.append(lines)
# print("connected_lines (die verschiedenen Kreise)")
# print(connected_lines)


#aufruf der order
sorted_components_final = sort_and_rearrange_components(connected_lines)
# print("Endgültig sortierte und reorganisierte Linien:")
# for i, component in enumerate(sorted_components_final):
#     print(f"Komponente {i + 1}: {component}")
print("sorted_final -> weiter in connecteLinesTest nutzen")
print(sorted_components_final)


ergebnis_liste = []  

for inner_list in sorted_components_final:
    changed_inner_list = [inner_list]
    final_chain, all_chains = process_components(changed_inner_list)
    print("Final :", final_chain)

    
    endergebnis = []
    if all_chains == []:
        if final_chain[0][0] != final_chain[-1][1]:
    # Wenn position 0 und endpossiton nicht gelcih sind [(0, 17), (17, 4), (4, 12)] dann
    # [(0, 17), (17, 4), (4, 12), (12, 4), (4, 17), (17, 0)]
            final_chain += [(b, a) for a, b in reversed(final_chain)]

# Ergebnis ausgeben
        print("neu", final_chain)
        endergebnis = final_chain
    else:
        weitereKlammer = all_chains[0]
        larger_chain, split1, split2 = split_chain(weitereKlammer, final_chain)
        chains2 = [split1, split2]
        ende, ende1, ende2 = extend_chain(larger_chain, chains2)
        endergebnis = ende
    
    print("endeergebenis",endergebnis)



   # print("ENDE", endergebnis)
    ergebnis_liste.append(endergebnis)  # Ergebnis zur Liste hinzufügen

# Ausgabe der gesamten Ergebnisliste nach dem Durchlaufen der Schleife
print("Ergebnis Liste:", ergebnis_liste)


cornersTemplate = print_corners_by_lines(reversed_wall_points, ergebnis_liste)
print("segementpoinstTemp")
segemntpointsTemplate = print_segmentpoints_by_lines(reversed_wall_points)
point_order_Template = wall_lines_order(ergebnis_liste)

# Load existing JSON template
with open("json_Template.json", "r") as f:
    data = json.load(f)

# Populate the JSON template
data["Domainpolygon"]["numberPoints"] = len(reversed_wall_points)
data["Domainpolygon"]["segmentPoints"] = segemntpointsTemplate
data["Domainpolygon"]["numberSegments"] = len(ergebnis_liste)
data["Domainpolygon"]["pointOrder"] = point_order_Template

# Insert corners into the JSON template
polygon_corners = [{"corners": line, "closed": "True"} for line in cornersTemplate]
data["PolygonCorners"] = polygon_corners
# Timestemp erstellen und in json mitgeben 
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"output_{timestamp}.json"
with open(filename, "w") as json_file:
    json.dump(data, json_file, indent=4)