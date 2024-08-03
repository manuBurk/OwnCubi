#für segementpoints ->PLACEHOLDER_SEGMENT_POINTS

def print_segmentpoints_by_lines(segmentpoints):
    points_to_print = []
    for point in segmentpoints:
        x, y = point[:2]
        points_to_print.extend([x, y])  # Add x and y to the flat list
    return points_to_print

# für order:
print("wall_lines_order")
def wall_lines_order(wall_lines):
    indices = []
    for line in wall_lines:
        for segment in line:
            indices.extend(segment)
    return indices


# print("\nWall lines order:")
# print_wall_lines_order(wall_lines)

#für polygon corners
def generate_unique_id(counter):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    letters = alphabet[counter // (10*10) % 26]  # Corrected to ensure index is within range
    first_digit = counter // 10 % 10
    second_digit = counter % 10
    return f'{letters}{letters}{first_digit}{second_digit}{second_digit}'

def process_line(line, points_corners, counter):
    sub_results = []  # List for storing corners of a single line
    for pair in line:
        for index in pair:
            if 0 <= index < len(points_corners):
                point = points_corners[index]
                x, y = point[:2]
                uniqid = generate_unique_id(counter)
                sub_results.append({
                    "id": uniqid,
                    "x": x,
                    "y": y
                })
                counter += 1  # Increment counter
    return sub_results, counter

def print_corners_by_lines(points_corners, wall_lines):
    counter = 0  # Initialize counter
    results = []  # List to collect the results
    
    for line in wall_lines:
        sub_results, counter = process_line(line, points_corners, counter)
        results.append(sub_results)
    
    return results