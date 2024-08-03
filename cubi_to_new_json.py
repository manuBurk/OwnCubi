import numpy as np
import json
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from floortrans.models import get_model
from floortrans.loaders import FloorplanSVGnew, DictToTensor, Compose, RotateNTurns
from floortrans.plotting import segmentation_plot, polygons_to_image, draw_junction_from_dict, discrete_cmap
from floortrans.post_prosessing import split_prediction, get_polygons
from mpl_toolkits.axes_grid1 import AxesGrid
import json
from datetime import datetime
from collections import defaultdict
from order import sort_and_rearrange_components

# Initialize colormap and rotation transformation
discrete_cmap()
rot = RotateNTurns()

# Load dataset
data_folder = 'data/cubicasa5k/'
data_file = 'cubitest.txt'
normal_set = FloorplanSVGnew(data_folder, data_file, format='txt', original_size=True)
data_loader = DataLoader(normal_set, batch_size=1, num_workers=0)
data_iter = iter(data_loader)

# Setup model
model = get_model('hg_furukawa_original', 51)
n_classes = 44
split = [21, 12, 11]
model.conv4_ = torch.nn.Conv2d(256, n_classes, bias=True, kernel_size=1)
model.upsample = torch.nn.ConvTranspose2d(n_classes, n_classes, kernel_size=4, stride=4)
checkpoint = torch.load('model_best_val_loss_var.pkl')
model.load_state_dict(checkpoint['model_state'])
model.eval()
model.cuda()
print("Model loaded.")

# Load the next batch of data
val = next(data_iter)
folder = val['folder'][0]
image = val['image'].cuda()
np_img = np.moveaxis(image[0].cpu().data.numpy(), 0, -1) / 2 + 0.5
# print("image")
# print(image)
print("folder")
print(folder)
# Perform prediction with rotations
with torch.no_grad():
    rotations = [(0, 0), (1, -1), (2, 2), (-1, 1)]
    pred_count = len(rotations)
    height, width = image.shape[2:]
    prediction = torch.zeros([pred_count, n_classes, height, width])
    for i, r in enumerate(rotations):
        forward, back = r
        # Rotate the image
        rot_image = rot(image, 'tensor', forward)
        pred = model(rot_image)
        # Rotate prediction back
        pred = rot(pred, 'tensor', back)
        # Ensure the size is correct
        pred = F.interpolate(pred, size=(height, width), mode='bilinear', align_corners=True)
        # Add the prediction to output
        prediction[i] = pred[0]

prediction = torch.mean(prediction, 0, True)
# print("prediction")
# print(prediction)

rooms_pred = F.softmax(prediction[0, 21:21+12], 0).cpu().data.numpy()
rooms_pred = np.argmax(rooms_pred, axis=0)
# print("rooms_pred")
# print(rooms_pred)

icons_pred = F.softmax(prediction[0, 21+12:], 0).cpu().data.numpy()
icons_pred = np.argmax(icons_pred, axis=0)
# print("icon_pred")
# print(icons_pred)

heatmaps, rooms, icons = split_prediction(prediction, (height, width), split)
polygons, types, room_polygons, room_types, wall_lines, wall_points = get_polygons((heatmaps, rooms, icons), 0.2, [1, 2])




print("wall_lines")
print(wall_lines)
# #wall_points gibt alle Punkte zurück, auch die welche in wall_lines nicht benötigt werden
print("wall points")
print(wall_points)

# Liste ersten mit den ersten beiden Punkte, anderen Werte Fallen weg
first_two_points = [[sublist[0], sublist[1]] for sublist in wall_points]
# print("ersten zwei Punkte:")
# print(first_two_points)

# Set der Indizes, die in wall_lines verwendet werden, punkte die nicht in Wall_lines vorkommen werden mit &&& markiert
line_indices = {index for line in wall_lines for index in line[:2]}
selected_wall_points = []
for i, point in enumerate(first_two_points):
    if i in line_indices:
        selected_wall_points.append([point[0], point[1], i])
    else:
        selected_wall_points.append([point[0], point[1], "&&&&"])

# Vergleich der Punkte und Aktualisierung
#wenn punkte +-5 sind werden sie angepasst. (der zuvergeleichende Punkt wird auf den ersten wert geändert)
#ursprungs index sowie index das ersten werts werden mit gespeichert
#damit die punkte auf einander liegen
for i in range(len(selected_wall_points)):
    x1, y1, idx1 = selected_wall_points[i][:3]
    if idx1 == '&&&&':
        continue
    for j in range(i + 1, len(selected_wall_points)):
        x2, y2, idx2 = selected_wall_points[j][:3]
        if idx2 == '&&&&':
            continue
        if abs(x1 - x2) <= 5 and abs(y1 - y2) <= 4:
            selected_wall_points[j][0] = x1
            selected_wall_points[j][1] = y1
            selected_wall_points[j].append(idx1)

print("alle wall_points nach Vergleich und Aktualisierung:")
print(selected_wall_points)


# Mapping von alten Indizes zu neuen Indizes
index_mapping = {}
for point in selected_wall_points:
    x, y, idx = point[:3]
    if idx != '&&&&':
        new_indices = point[3:] if len(point) > 3 else []
        for new_idx in new_indices:
            index_mapping[new_idx] = idx

# Aktualisieren der wall_lines-Liste, punkte in lines, welche mit sich selebr verbundne sind (40,40,2) fallen raus, 
updated_wall_lines = []
for line in wall_lines:
    old_idx1, old_idx2, category = line
    new_idx1 = index_mapping.get(old_idx1, old_idx1)
    new_idx2 = index_mapping.get(old_idx2, old_idx2)
    updated_line = (new_idx1, new_idx2, category)
    updated_wall_lines.append(updated_line)

#        updated_wall_lines.append(updated_line)
    
print("alte wall_lines")
print(wall_lines)
print("aktualisierte wall_lines:")
print(updated_wall_lines)

#wall lines ohne den 3. wert (kategorie)
# Extrahiere die ersten beiden Punkte aus wall_lines
extracted_wall_lines = [(line[0], line[1]) for line in updated_wall_lines]

# Erstelle die aktualisierte Liste updated_wall_lines ohne den dritten Wert
updated_wall_lines = extracted_wall_lines

print("Aktualisierte wall_lines (nur Punkt1, Punkt2):")
print(updated_wall_lines)


#numberPoints -> für Segementpoints
anzahl_wall_points = int(len(selected_wall_points)/2)

print(anzahl_wall_points)


#zusammenhängende Punkte  gruppieren
# Schritt 1: Graph erstellen
# Graph-Adjazenzliste
graph = defaultdict(list)

# Erstellen des Graphen
for line in updated_wall_lines:
    if line[0] != line[1]:  # Selbstverbindungen ignorieren
        graph[line[0]].append(line[1])
        graph[line[1]].append(line[0])

print("graph")
print(graph)

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

print("components")
print(components)
# Schritt 3: Linien in jeder Komponente sammeln und sortieren
connected_lines = []

for component in components:
    lines = []
    for line in updated_wall_lines:
        if line[0] in component and line[1] in component:
            lines.append(line)
    connected_lines.append(lines)
print("connected_lines")
print(connected_lines)


#aufruf der order
sorted_components_final = sort_and_rearrange_components(connected_lines)
print("Endgültig sortierte und reorganisierte Linien:")
for i, component in enumerate(sorted_components_final):
    print(f"Komponente {i + 1}: {component}")



# #json tamplet befüllen 
# with open("json_Template.json", "r") as f:
#     data = json.load(f)
# data["Domainpolygon"]["numberPoints"] = anzahl_wall_points
# data["Domainpolygon"]["segmentPoints"] = selected_wall_points

# # Timestemp erstellen und in json mitgeben 
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# filename = f"output_{timestamp}.json"
# with open(filename, "w") as json_file:
#     json.dump(data, json_file, indent=4)

# #uniqu_id für corners
# def generate_unique_id(counter):
#     alphabet = 'abcdefghijklmnopqrstuvwxyz'
#     letters = alphabet[counter // (10*10)]
#     first_digit = counter // 10 % 10
#     second_digit = counter % 10
#     return f'{letters}{letters}{first_digit}{second_digit}{second_digit}'