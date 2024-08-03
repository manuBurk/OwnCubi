import os
import json
import re

# Pfad zu den Ordnern
base_path = "/Users/manuburkart/Desktop/Bachlorarbeit Manuel (File responses)/"  # Passe diesen Pfad an
folders = ["01", "02", "03", "04", "05", "01_goldlabel", "02_goldlabel", "03_goldlabel"]

def extract_data_from_json(file_path):
    """Extrahiert segmentPoints und pointOrder aus der JSON-Datei, wenn vorhanden."""
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        
        # Prüfe, ob Domainpolygon vorhanden ist
        domain_polygon = data.get("Domainpolygon", {})
        
        segment_points = domain_polygon.get("segmentPoints", [])
        point_order = domain_polygon.get("pointOrder", [])
        
        return segment_points, point_order

def extract_user_number(filename):
    """Extrahiert die Benutzerzahl aus dem Dateinamen."""
    match = re.search(r'user(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

for folder in folders:
    folder_path = os.path.join(base_path, folder)
    output_file = os.path.join(base_path, f"{folder}.txt")
    
    with open(output_file, 'w') as txt_file:
        # Überprüfe, ob der Ordner existiert
        if not os.path.exists(folder_path):
            print(f"Ordner {folder_path} nicht gefunden.")
            continue
        
        # Hole und sortiere alle JSON-Dateien im Ordner nach Benutzerzahl
        json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
        json_files.sort(key=extract_user_number)
        
        # Durchlaufe die sortierten Dateien
        for file_name in json_files:
            file_path = os.path.join(folder_path, file_name)
            file_base_name = os.path.splitext(file_name)[0]  # Entferne die .json Endung
            
            try:
                segment_points, point_order = extract_data_from_json(file_path)
                
                # Schreibe die Daten in die Textdatei
                #txt_file.write(file_base_name + " = { \n ")  # Nutze den Basisnamen ohne Endung
                txt_file.write('{"segmentPoints": [\n')
                txt_file.write(", ".join(map(str, segment_points)) + "\n")
                txt_file.write("],\n")
                txt_file.write('"pointOrder": [\n')
                txt_file.write(", ".join(map(str, point_order)) + "\n")
                txt_file.write("]\n")
                txt_file.write("},\n")
                
            except Exception as e:
                print(f"Fehler beim Verarbeiten der Datei {file_name}: {e}")

print("Fertig!")
