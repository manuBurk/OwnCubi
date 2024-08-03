# from xml.etree import ElementTree as ET
# from xml.dom import minidom #für die formtierung der neuen svg

# # Parse the original SVG file
# tree = ET.parse('data/cubicasa5k/colorful/619/model.svg')
# root = tree.getroot()

# # Create a new SVG root element
# new_root = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="1.1")

# # Copy relevant attributes from the original SVG
# new_root.attrib.update({
#     'height': root.attrib.get('height', '100%'),
#     'width': root.attrib.get('width', '10%'),
# })

# # Find all Wall elements and append them to the new SVG root
# for wall in root.findall(".//*[@class='Wall']"):
#     new_root.append(wall)

# for wall in root.findall(".//*[@class='Wall External']"):
#     new_root.append(wall)

# # Convert the new tree to a string
# rough_string = ET.tostring(new_root, 'utf-8')
# reparsed = minidom.parseString(rough_string)
# pretty_string = reparsed.toprettyxml(indent="  ")

# # Save the formatted SVG string to a file
# with open('walls_only.svg', 'w') as f:
#     f.write(pretty_string)

# print("Die Wände wurden erfolgreich in 'walls_only.svg' gespeichert.")

from xml.etree import ElementTree as ET
from xml.dom import minidom  # für die Formatierung der neuen SVG

# Parse the original SVG file
tree = ET.parse('data/cubicasa5k/high_quality_architectural/2536/model.svg')
root = tree.getroot()

# Create a new SVG root element
new_root = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="1.1")

# Copy relevant attributes from the original SVG
new_root.attrib.update({
    'height': root.attrib.get('height', '100%'),
    'width': root.attrib.get('width', '100%'),
})

# Helper function to update stroke-width and remove fill
def update_stroke_and_fill(element, new_width):
    style = element.attrib.get('style', '')
    if 'stroke-width' in style:
        style = ';'.join([f'stroke-width: {new_width}' if 'stroke-width' in s else s for s in style.split(';')])
    else:
        style += f';stroke-width: {new_width}'
    
    if 'fill' in style:
        style = ';'.join(['fill: none' if 'fill' in s else s for s in style.split(';')])
    else:
        style += ';fill: none'
    
    element.attrib['style'] = style
    element.set('fill', 'none')
    element.set('stroke', '#000000')  # Set stroke to black for visibility

# Find all Wall elements and append them to the new SVG root with updated stroke-width
for wall in root.findall(".//*[@class='Wall']"):
    update_stroke_and_fill(wall, '5')
    new_root.append(wall)

for wall in root.findall(".//*[@class='Wall External']"):
    update_stroke_and_fill(wall, '5')
    new_root.append(wall)

# Convert the new tree to a string
rough_string = ET.tostring(new_root, 'utf-8')
reparsed = minidom.parseString(rough_string)
pretty_string = reparsed.toprettyxml(indent="  ")

# Save the formatted SVG string to a file
with open('walls_only.svg', 'w') as f:
    f.write(pretty_string)

print("Die Wände wurden erfolgreich in 'walls_only.svg' gespeichert.")
