# version 8.7 10:39
# import numpy as np
# import json
# import matplotlib.pyplot as plt
# import torch
# import torch.nn.functional as F
# from torch.utils.data import DataLoader
# from floortrans.models import get_model
# from floortrans.loaders import FloorplanSVGLotta, DictToTensor, Compose, RotateNTurns
# from floortrans.plotting import segmentation_plot, polygons_to_image, draw_junction_from_dict, discrete_cmap
# from floortrans.post_prosessing import split_prediction, get_polygons
# from mpl_toolkits.axes_grid1 import AxesGrid
# import json
# from datetime import datetime
# from collections import defaultdict
# from order import sort_and_rearrange_components, process_components
# from wall_lines_points import print_corners_by_lines, print_segmentpoints_by_lines, wall_lines_order

# rot = RotateNTurns()
# room_classes = ["Background", "Outdoor", "Wall", "Kitchen", "Living Room" ,"Bed Room", "Bath", "Entry", "Railing", "Storage", "Garage", "Undefined"]
# icon_classes = ["No Icon", "Window", "Door", "Closet", "Electrical Applience" ,"Toilet", "Sink", "Sauna Bench", "Fire Place", "Bathtub", "Chimney"]

# data_folder = 'data/cubicasa5k/'
# data_file = 'cubitest.txt'
# normal_set = FloorplanSVGLotta(data_folder, data_file, format='txt', original_size=True)
# data_loader = DataLoader(normal_set, batch_size=1, num_workers=0)
# data_iter = iter(data_loader)
# # Setup Model
# model = get_model('hg_furukawa_original', 51)

# n_classes = 44
# split = [21, 12, 11]
# model.conv4_ = torch.nn.Conv2d(256, n_classes, bias=True, kernel_size=1)

# model.upsample = torch.nn.ConvTranspose2d(n_classes, n_classes, kernel_size=4, stride=4)
# checkpoint = torch.load('model_best_val_loss_var.pkl')

# model.load_state_dict(checkpoint['model_state'])
# model.eval()
# model.cuda()
# print("Model loaded.")

# val = next(data_iter)
# image = val['image'].cuda()

# with torch.no_grad():
#     height, width = image.shape[2:]
#     img_size = (height, width)
    
#     rotations = [(0, 0), (1, -1), (2, 2), (-1, 1)]
#     pred_count = len(rotations)
#     prediction = torch.zeros([pred_count, n_classes, height, width])

#     for i, r in enumerate(rotations):
#         forward, back = r
#         # We rotate first the image
#         rot_image = rot(image, 'tensor', forward)
#         pred = model(rot_image)
#         # We rotate prediction back
#         pred = rot(pred, 'tensor', back)
#         # We fix heatmaps
#         pred = rot(pred, 'points', back)
#         # We make sure the size is correct
#         pred = F.interpolate(pred, size=(height, width), mode='bilinear', align_corners=True)
#         # We add the prediction to output
#         prediction[i] = pred[0]

# prediction = torch.mean(prediction, 0, True)

# rooms_pred = F.softmax(prediction[0, 21:21+12], 0).cpu().data.numpy()
# rooms_pred = np.argmax(rooms_pred, axis=0)

# icons_pred = F.softmax(prediction[0, 21+12:], 0).cpu().data.numpy()
# icons_pred = np.argmax(icons_pred, axis=0)

# heatmaps, rooms, icons = split_prediction(prediction, img_size, split)
# polygons, types, room_polygons, room_types, wall_lines, wall_points = get_polygons((heatmaps, rooms, icons), 0.2, [1, 2])

# # print("wall Lines")
# # print(wall_lines)
# # print("wall_points")
# # print(wall_points)


# first_two_wall_points = [[sublist[0], sublist[1]] for sublist in wall_points]
# first_two_wall_lines = [(line[0], line[1]) for line in wall_lines]



# #für PolygonCorners
# extracted_wall_points = [(line[0], line[1]) for line in first_two_wall_points]
# points_corners = extracted_wall_points
# print("wallPoints (nur x, y):")
# print(points_corners)

# #-1000 für die darstellung "segmentpoints"
# extracted_wall_points = [(line[0], 1000-line[1]) for line in first_two_wall_points]
# segmentpoints = extracted_wall_points

# print("wallPoints (nur x, y, y umgekehrter Wert):")
# print(segmentpoints)






# #wall lines ohne den 3. wert (kategorie)
# # Extrahiere die ersten beiden Punkte aus wall_lines


# print("Aktualisierte wall_lines (nur Punkt1, Punkt2):")
# print(first_two_wall_lines)


# #numberPoints -> für Segementpoints
# anzahl_wall_points = int(len(first_two_wall_lines)/2)

# print(anzahl_wall_points)


# #zusammenhängende Punkte  gruppieren
# # Schritt 1: Graph erstellen
# # Graph-Adjazenzliste
# graph = defaultdict(list)

# # Erstellen des Graphen
# for line in first_two_wall_lines:
#     if line[0] != line[1]:  # Selbstverbindungen ignorieren
#         graph[line[0]].append(line[1])
#         graph[line[1]].append(line[0])


# # Funktion zur Tiefensuche, um verbundene Komponenten zu finden
# def dfs(node, visited, component):
#     stack = [node]
#     while stack:
#         current = stack.pop()
#         if current not in visited:
#             visited.add(current)
#             component.append(current)
#             for neighbor in graph[current]:
#                 if neighbor not in visited:
#                     stack.append(neighbor)


# # Schritt 2: Finden der verbundenen Komponenten
# visited = set()
# components = []

# for node in graph:
#     if node not in visited:
#         component = []
#         dfs(node, visited, component)
#         components.append(component)

# # Schritt 3: Linien in jeder Komponente sammeln und sortieren
# connected_lines = []

# for component in components:
#     lines = []
#     for line in first_two_wall_lines:
#         if line[0] in component and line[1] in component:
#             lines.append(line)
#     connected_lines.append(lines)
# print("connected_lines (die verschiedenen Kreise)")
# print(connected_lines)


# #aufruf der order
# sorted_components_final = sort_and_rearrange_components(connected_lines)
# print("Endgültig sortierte und reorganisierte Linien:")
# for i, component in enumerate(sorted_components_final):
#     print(f"Komponente {i + 1}: {component}")
# print("sorted_final")
# print(sorted_components_final)
# print("weiter sortiert und ergänzt mit conectedLines")

# sorted_final = process_components(sorted_components_final)
# print(sorted_final)



# #corners = print_corners_by_lines(points_corners, sorted_components_final) #hier fehler
# cornersTemplate = print_corners_by_lines(points_corners, sorted_final)
# print("segementpoinstTemp")
# segemntpointsTemplate = print_segmentpoints_by_lines(points_corners)
# point_order_Template = wall_lines_order(sorted_final)

# # Load existing JSON template
# with open("json_Template.json", "r") as f:
#     data = json.load(f)

# # Populate the JSON template
# data["Domainpolygon"]["numberPoints"] = len(segmentpoints)
# data["Domainpolygon"]["segmentPoints"] = segemntpointsTemplate
# data["Domainpolygon"]["numberSegments"] = len(sorted_final)
# data["Domainpolygon"]["pointOrder"] = point_order_Template

# # Insert corners into the JSON template
# polygon_corners = [{"corners": line, "closed": "True"} for line in cornersTemplate]
# data["PolygonCorners"] = polygon_corners
# # Timestemp erstellen und in json mitgeben 
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# filename = f"output_{timestamp}.json"
# with open(filename, "w") as json_file:
#     json.dump(data, json_file, indent=4)





import numpy as np
import json
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from floortrans.models import get_model
from floortrans.loaders import FloorplanSVGLotta, DictToTensor, Compose, RotateNTurns
from floortrans.plotting import segmentation_plot, polygons_to_image, draw_junction_from_dict, discrete_cmap
from floortrans.post_prosessing import split_prediction, get_polygons
from mpl_toolkits.axes_grid1 import AxesGrid
import json
from datetime import datetime
from collections import defaultdict
from order import sort_and_rearrange_components, process_components
from wall_lines_points import print_corners_by_lines, print_segmentpoints_by_lines, wall_lines_order
from conectedLinesTest import process_components, split_chain, extend_chain

rot = RotateNTurns()
room_classes = ["Background", "Outdoor", "Wall", "Kitchen", "Living Room" ,"Bed Room", "Bath", "Entry", "Railing", "Storage", "Garage", "Undefined"]
icon_classes = ["No Icon", "Window", "Door", "Closet", "Electrical Applience" ,"Toilet", "Sink", "Sauna Bench", "Fire Place", "Bathtub", "Chimney"]

data_folder = 'data/cubicasa5k/'
data_file = 'cubitest.txt'
normal_set = FloorplanSVGLotta(data_folder, data_file, format='txt', original_size=True)
data_loader = DataLoader(normal_set, batch_size=1, num_workers=0)
data_iter = iter(data_loader)
# Setup Model
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

val = next(data_iter)
image = val['image'].cuda()

with torch.no_grad():
    height, width = image.shape[2:]
    img_size = (height, width)
    
    rotations = [(0, 0), (1, -1), (2, 2), (-1, 1)]
    pred_count = len(rotations)
    prediction = torch.zeros([pred_count, n_classes, height, width])

    for i, r in enumerate(rotations):
        forward, back = r
        # We rotate first the image
        rot_image = rot(image, 'tensor', forward)
        pred = model(rot_image)
        # We rotate prediction back
        pred = rot(pred, 'tensor', back)
        # We fix heatmaps
        pred = rot(pred, 'points', back)
        # We make sure the size is correct
        pred = F.interpolate(pred, size=(height, width), mode='bilinear', align_corners=True)
        # We add the prediction to output
        prediction[i] = pred[0]

prediction = torch.mean(prediction, 0, True)

rooms_pred = F.softmax(prediction[0, 21:21+12], 0).cpu().data.numpy()
rooms_pred = np.argmax(rooms_pred, axis=0)

icons_pred = F.softmax(prediction[0, 21+12:], 0).cpu().data.numpy()
icons_pred = np.argmax(icons_pred, axis=0)

heatmaps, rooms, icons = split_prediction(prediction, img_size, split)
polygons, types, room_polygons, room_types, wall_lines, wall_points = get_polygons((heatmaps, rooms, icons), 0.2, [1, 2])

# print("wall Lines")
# print(wall_lines)
# print("wall_points")
# print(wall_points)


first_two_wall_points = [[sublist[0], sublist[1]] for sublist in wall_points]
first_two_wall_lines = [(line[0], line[1]) for line in wall_lines]



#für PolygonCorners
extracted_wall_points = [(line[0], line[1]) for line in first_two_wall_points]
points_corners = extracted_wall_points
print("wallPoints (nur x, y):")
print(points_corners)
#-1000 für die darstellung "segmentpoints"
extracted_wall_points = [(line[0], 1000-line[1]) for line in first_two_wall_points]
segmentpoints = extracted_wall_points
print("wallPoints (nur x, y, y umgekehrter Wert):")
print(segmentpoints)

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



# #aufruf vonn conectedLinesTest.py für doppelte linien
# for inner_list in sorted_components_final:
#     changed_inner_list = [inner_list]
#     final_chain, all_chains = process_components(changed_inner_list)
#     print("Final :", final_chain)
#     #print("Remaining chains:", all_chains)

#     #geht nur in die if, wenn es zwei ketten am ende gibt die noch zusammengefügt werden müssen  
#     endergebnis = []
#     if all_chains == []:
#         endergebnis = final_chain
#     if all_chains != []:
#         result = all_chains[0]
#         print("ergebnis",result)
#         larger_chain, split1 , split2 = split_chain(result, final_chain)
#        # print("Übereinstimmende Teilkette gefunden:", split1, split2 ) 
#         chains2 = [split1,split2]
#         extend_chain(larger_chain, chains2)

ergebnis_liste = []  # Liste zum Speichern der Ergebnisse

for inner_list in sorted_components_final:
    changed_inner_list = [inner_list]
    final_chain, all_chains = process_components(changed_inner_list)
    print("Final :", final_chain)

    endergebnis = []
    if all_chains == []:
        endergebnis = final_chain
    else:
        weitereKlammer = all_chains[0]
        larger_chain, split1, split2 = split_chain(weitereKlammer, final_chain)
        chains2 = [split1, split2]
        ende, ende1, ende2 = extend_chain(larger_chain, chains2)
        endergebnis = ende
    
   # print("ENDE", endergebnis)
    ergebnis_liste.append(endergebnis)  # Ergebnis zur Liste hinzufügen

# Ausgabe der gesamten Ergebnisliste nach dem Durchlaufen der Schleife
print("Ergebnis Liste:", ergebnis_liste)


# #corners = print_corners_by_lines(points_corners, sorted_components_final) #hier fehler
cornersTemplate = print_corners_by_lines(points_corners, ergebnis_liste)
print("segementpoinstTemp")
segemntpointsTemplate = print_segmentpoints_by_lines(points_corners)
point_order_Template = wall_lines_order(ergebnis_liste)

# Load existing JSON template
with open("json_Template.json", "r") as f:
    data = json.load(f)

# Populate the JSON template
data["Domainpolygon"]["numberPoints"] = len(segmentpoints)
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






# print("weiter sortiert und ergänzt mit conectedLines")

# sorted_final = process_components(sorted_components_final)
# print("sortedfinal",sorted_final)



# #corners = print_corners_by_lines(points_corners, sorted_components_final) #hier fehler
# cornersTemplate = print_corners_by_lines(points_corners, sorted_final)
# print("segementpoinstTemp")
# segemntpointsTemplate = print_segmentpoints_by_lines(points_corners)
# point_order_Template = wall_lines_order(sorted_final)

# # Load existing JSON template
# with open("json_Template.json", "r") as f:
#     data = json.load(f)

# # Populate the JSON template
# data["Domainpolygon"]["numberPoints"] = len(segmentpoints)
# data["Domainpolygon"]["segmentPoints"] = segemntpointsTemplate
# data["Domainpolygon"]["numberSegments"] = len(sorted_final)
# data["Domainpolygon"]["pointOrder"] = point_order_Template

# # Insert corners into the JSON template
# polygon_corners = [{"corners": line, "closed": "True"} for line in cornersTemplate]
# data["PolygonCorners"] = polygon_corners
# # Timestemp erstellen und in json mitgeben 
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# filename = f"output_{timestamp}.json"
# with open(filename, "w") as json_file:
#     json.dump(data, json_file, indent=4)
