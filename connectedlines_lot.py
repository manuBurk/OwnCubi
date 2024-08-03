# input= [(19, 30), (30, 38), (38, 4), (4, 29), (29, 19), (19, 12), (12, 24), (24, 2), (2, 28), (28, 12), 
#          (25, 6), (6, 36), (36, 33), (33, 18), (18, 9), (9, 23), (23, 21), (21, 33), 
#          (7, 11), (11, 13), (13, 18), 
#          (7, 39), (39, 17), (17, 25), (25, 11), 
#          (13, 41), (41, 36), 
#          (17, 22), (22, 30), 
#          (37, 22), 
#          (23, 24), 
#          (29, 28), 
#          (39, 37), (37, 38)]

input = [
              (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
              (5, 39), (39, 17), (17, 25), (25, 11), 
              (13, 41), (41, 39), 
              (17, 24), 
            ]


def create_and_sort_list(input_list):
    new_lists = []
    split_i = 0
    for i, element in enumerate(input_list):
        if i>1:
            if input_list[i-1][1] != input_list[i][0]:
                new_lists.append(input_list[split_i:i])
                split_i = i
    print("len1", len(new_lists))
    return sorted(new_lists, key=len)

sorted_lists = create_and_sort_list(input)

def check_same_value(current_list, bigger_lists):
    x1 = current_list[0][0]
    x2 = current_list[-1][1]
    for list in bigger_lists:
        for i, tuple in enumerate(list):
            if x1 == tuple[1]:
                split1 = list[:i+1]
                split2 = list[i+1:]
                reverse = [t[::-1] for t in current_list[::-1]]
                new = split1 + current_list + reverse + split2
                return new
            if x2 == tuple[0]:
                split1 = list[:i]
                split2 = list[i:]
                reverse = [t[::-1] for t in current_list[::-1]]
                new = split1 + reverse + current_list + split2
                return new
    return(current_list)

def insert_lists(sorted_input):
    temporary_lists = []
    counter = 0
    for list in sorted_input:
        longer_lists = [sublist for sublist in sorted_input if len(sublist) > len(list)]
        temporary_lists.append(check_same_value(list, longer_lists))
    counter += 1
    concatenated = sorted(temporary_lists, key=len)
    print(concatenated)
    print(len(concatenated))

print(insert_lists(sorted_lists))








