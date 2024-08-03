from collections import defaultdict
import json
import uuid
import math

#bei linine welche nur aus zwei punkten bestehen, ohne weitere verbindung, werden diese zwei Punkte 
#durch eine Parallele Linie ergänzt. Dies geht nun bei allen Richtungenen der ersten linie
#da die zweite nach dem richtungsvektor der erste ausgerichtet wird.
#Auskommentierte Teile sind unwichtige ausgaben 

def generate_uuid():
    return str(uuid.uuid4()).replace("-", "")[:22]

def find_cycles(point_order):
    # Initialize a dictionary to store edges
    edges = defaultdict(list)
    
    # Populate the dictionary with edges from pointOrder
    for i in range(0, len(point_order), 2):
        start = point_order[i]
        end = point_order[i+1]
        edges[start].append(end)
        edges[end].append(start)
    
    # Function to perform DFS and find cycles
    def dfs(node, visited, parent, cycle_nodes):
        nonlocal cycle_count
        visited[node] = True
        cycle_nodes.append(node)
        
        for neighbor in edges[node]:
            if not visited[neighbor]:
                if dfs(neighbor, visited, node, cycle_nodes):
                    return True
            elif neighbor != parent and neighbor in cycle_nodes:
                # Found a cycle
                index = cycle_nodes.index(neighbor)
                cycle = cycle_nodes[index:] + [neighbor]
                if len(cycle) > 2:  # Only consider cycles with 3 or more points
                    cycles.append(cycle)
                    cycle_count += 1
                return True
        
        cycle_nodes.pop()
        return False
    
    # Initialize variables
    visited = {node: False for node in edges}
    cycles = []
    cycle_count = 0
    
    # Find all cycles using DFS
    for node in edges:
        if not visited[node]:
            dfs(node, visited, None, [])
    
    return cycles

def create_parallel_points(segment_points, point_order):
    # Create point pairs from segment_points
    point_pairs = []
    for i in range(0, len(segment_points), 2):
        point_pairs.append((segment_points[i], segment_points[i + 1]))

    # Find cycles in the current pointOrder
    cycles = find_cycles(point_order)

    # Create a set of cycle points
    cycle_points = set()
    for cycle in cycles:
        cycle_points.update(cycle)

    # Create parallel points for points not in cycles
    parallel_points = []
    visited_connections = set()
    new_cycles = []
    new_segment_points = list(segment_points)
    new_point_order = []
    point_index = len(segment_points) // 2

def create_parallel_points(segment_points, point_order, distance=1):
    # Create point pairs from segment_points
    point_pairs = []
    for i in range(0, len(segment_points), 2):
        point_pairs.append((segment_points[i], segment_points[i + 1]))

    # Find cycles in the current pointOrder
    cycles = find_cycles(point_order)

    # Create a set of cycle points
    cycle_points = set()
    for cycle in cycles:
        cycle_points.update(cycle)

    # Create parallel points for points not in cycles
    parallel_points = []
    visited_connections = set()
    new_cycles = []
    new_segment_points = list(segment_points)
    new_point_order = []
    point_index = len(segment_points) // 2

    # Iterate through original segment points
    for i in range(0, len(point_order), 2):
        start = point_order[i]
        end = point_order[i + 1]

        if start in cycle_points or end in cycle_points:
            new_point_order.extend([start, end])
            continue

        if (start, end) not in visited_connections and (end, start) not in visited_connections:
            x1, y1 = segment_points[start * 2], segment_points[start * 2 + 1]
            x2, y2 = segment_points[end * 2], segment_points[end * 2 + 1]

            # Calculate the direction vector of the line
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx**2 + dy**2)
            if length == 0:
                continue  # Skip if the points are the same

            # Normalize the direction vector and rotate it by 90 degrees to get the parallel direction
            nx = -dy / length
            ny = dx / length

            # Create the parallel points by shifting along the perpendicular direction
            px1, py1 = x1 + distance * nx, y1 + distance * ny
            px2, py2 = x2 + distance * nx, y2 + distance * ny

            # Add new parallel points to segment points
            new_segment_points.extend([px1, py1, px2, py2])

            # Update point order with new indices
            new_start_index = point_index
            new_end_index = point_index + 1
            new_point_order.extend([start, new_start_index, new_start_index, new_end_index, new_end_index, end, end, start])
            
            # Create parallel points and new cycles
            parallel_points.append((x1, y1, px1, py1))
            parallel_points.append((x2, y2, px2, py2))

            # Update point order to form a cycle
            new_cycle = []
            current_index = new_start_index
            for j in range(4):  # Create the new cycle [(x1, y1), (px1, py1), (px2, py2), (x2, y2), (x1, y1)]
                if current_index * 2 < len(segment_points):
                    new_cycle.append((segment_points[current_index * 2], segment_points[current_index * 2 + 1]))
                if j < 3:
                    current_index += 1
            new_cycles.append(new_cycle)

            visited_connections.add((start, end))

            # Increment point index
            point_index += 2

    return new_segment_points, new_point_order, parallel_points, new_cycles


# Given input segmentPoints and pointOrder
segmentPoints= [
        1049,
        63,
        1053,
        63,
        1049,
        62,
        1049,
        63,
        94,
        63,
        94,
        1021,
        87,
        63,
        94,
        63,
        1055,
        62,
        1055,
        1020,
        1049,
        62,
        1055,
        62,
        95,
        1020,
        1049,
        1020
    ]
pointOrder= [
        2,
        0,
        4,
        0,
        6,
        0,
        7,
        0,
        6,
        1,
        11,
        1,
        7,
        2,
        2,
        13,
        6,
        3,
        11,
        3,
        3,
        10,
        4,
        11,
        4,
        13,
        7,
        5,
        13,
        5,
        6,
        13,
        7,
        13,
        9,
        10
    ]

# Create parallel points and new cycles
new_segment_points, new_point_order, parallel_points, new_cycles = create_parallel_points(segmentPoints, pointOrder)

# Organize data into the desired format
domain_polygon = {
    "numberPoints": len(new_segment_points) // 2,
    "segmentPoints": new_segment_points,
    "numberSegments": len(new_point_order) // 2,
    "pointOrder": new_point_order,
}

grid = {}

polygon_corners = {
    "corners": [
        {"id": generate_uuid(), "x": segmentPoints[i], "y": segmentPoints[i + 1]}
        for i in range(0, 12, 2)
    ],
    "closed": True
}

# Output the original segment points
# print("Original Segment Points:")
# for i in range(0, len(segmentPoints), 2):
#     print(f"({segmentPoints[i]}, {segmentPoints[i + 1]})")

# Output the cycles found in pointOrder
# cycles = find_cycles(pointOrder)
# print("\nCycles found in Point Order:")
# for i, cycle in enumerate(cycles):
#     cycle_points = []
#     for node in cycle:
#         cycle_points.append((segmentPoints[node * 2], segmentPoints[node * 2 + 1]))
#     formatted_cycle = ' -> '.join(map(str, cycle_points))
#     print(f"Kreis {i + 1}: {formatted_cycle}")

# Output the parallel points for connections without cycle
# print("\nParallel Points for Connections without Cycle:")
# for (x1, y1, px1, py1), (x2, y2, px2, py2) in zip(parallel_points[::2], parallel_points[1::2]):
#     print(f"Original: ({x1}, {y1}) <-> ({x2}, {y2})  Parallel: ({px1}, {py1}) <-> ({px2}, {py2})")

# Output the new created cycles
# print("\nNewly Created Cycles:")
# for i, new_cycle in enumerate(new_cycles):
#     formatted_new_cycle = ' -> '.join(map(str, new_cycle))
#     print(f"New Cycle {i + 1}: {formatted_new_cycle}")

# Organize all data into the final format
output = {
    "Domainpolygon": domain_polygon,
    "PolygonCorners": polygon_corners,
    "ParallelPointsForConnectionsWithoutCycle": [
        {
            "Original": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            "Parallel": {"px1": px1, "py1": py1, "px2": px2, "py2": py2}
        }
        for (x1, y1, px1, py1), (x2, y2, px2, py2) in zip(parallel_points[::2], parallel_points[1::2])
    ],
    
}

# Print the final output in JSON format
#print("\nFinal Output in JSON format:")
print(json.dumps(output, indent=2))
