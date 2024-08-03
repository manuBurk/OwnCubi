# funktioniert, jedoch nur für eine kette ohne zusammenhang
# def find_longest_chain(lines):
#     max_chain = []
#     current_chain = []

#     for i in range(len(lines)):
#         if not current_chain:
#             current_chain.append(lines[i])
#         else:
#             last = current_chain[-1]
#             if last[1] == lines[i][0]:
#                 current_chain.append(lines[i])
#             else:
#                 if len(current_chain) > len(max_chain):
#                     max_chain = current_chain
#                 current_chain = [lines[i]]
    
#     if len(current_chain) > len(max_chain):
#         max_chain = current_chain
    
#     return max_chain

# def extend_chain(lines):
#     chain = find_longest_chain(lines)
    
#     for i in range(len(chain)-1, len(lines)):
#         if chain[-1][1] == lines[i][0]:
#             chain.append(lines[i])
    
#     break_point = chain[-1][1]
    
#     new_chain = []
#     for line in lines:
#         if line not in chain:
#             new_chain.append(line)
#             if line[0] == break_point or line[1] == break_point:
#                 break
    
#     final_chain = chain[:1] + new_chain + chain[1:]
#     reversed_new_chain = [(y, x) for x, y in new_chain[::-1]]
#     final_chain = final_chain[:len(new_chain)+1] + reversed_new_chain + final_chain[len(new_chain)+1:]
    
#     return final_chain

# # Beispielinput
# lines = [(19, 30), (30, 38), (38, 4), (4, 29), (29, 19), (30, 21), (21, 12), (4,8), (8,100)]

# extended_chain = extend_chain(lines)
# print(extended_chain)
# def find_chains(lines):
#     chains = []
#     visited = set()

# funktioniert mit mehreren ketten, aber immer start mit der längsten, dies kann zu problemen führen, wenn zu erste die kleinen ketten verbundne wrden müsstn 

# def find_chains(lines):
#     chains = []
#     visited = set()

#     def find_chain(start):
#         chain = [start]
#         current = start
#         while True:
#             found = False
#             for line in lines:
#                 if line not in visited:
#                     if current[1] == line[0]:
#                         chain.append(line)
#                         current = line
#                         visited.add(line)
#                         found = True
#                         break
#             if not found:
#                 break
#         return chain

#     for line in lines:
#         if line not in visited:
#             visited.add(line)
#             chain = find_chain(line)
#             chains.append(chain)

#     return chains


# def extend_chain(main_chain, chains):
#     final_chain = main_chain.copy()

#     for chain in chains:
#         insertion_index = None
  
#         if insertion_index is not None:
#             final_chain[insertion_index:insertion_index] = chain

#     # Extend and reverse each additional chain before inserting into final_chain
#     extended_chains = []
#     for chain in chains:
#         extended_chain = chain.copy()
#         reversed_chain = [(y, x) for x, y in chain[::-1]]
#         extended_chain.extend(reversed_chain)
#         extended_chains.append(extended_chain)

#     # Insert each extended chain into final_chain
#     for i, chain in enumerate(extended_chains):
#         insertion_index = None
#         for j in range(len(final_chain)):
#             if final_chain[j][1] == chain[0][0]:
#                 insertion_index = j + 1
#                 break
        
#         if insertion_index is not None:
#             final_chain[insertion_index:insertion_index] = chain

#     return final_chain

# def process_lines(lines):
#     chains = find_chains(lines)
    
#     if not chains:
#         return []

#     main_chain = max(chains, key=len)
#     chains.remove(main_chain)
    
#     extended_chain = extend_chain(main_chain, chains)
    
#     return extended_chain

# # Beispielinput
# lines = [(32, 34), (34, 14), (14, 15), (15, 10), (10, 26), (26, 3), (3, 32), (32, 40), (40, 15), 
#          (8, 5), (5, 31), (31, 42), (42, 20), (20, 8),
#            (16, 14), (16, 27), (27, 35), (35, 31),
#              (20, 16), 
#              (40, 26), 
#              (42, 27), 
#              (35, 34)]

# extended_lines = process_lines(lines)
# print(extended_lines)


# #alle werte werden eingefügt, aber die reihenfolge stimmt nciht mehr 
# def find_chains(lines):
#     chains = []
#     visited = set()

#     def find_chain(start):
#         chain = [start]
#         current = start
#         while True:
#             found = False
#             for line in lines:
#                 if line not in visited:
#                     if current[1] == line[0]:
#                         chain.append(line)
#                         current = line
#                         visited.add(line)
#                         found = True
#                         break
#             if not found:
#                 break
#         return chain

#     for line in lines:
#         if line not in visited:
#             visited.add(line)
#             chain = find_chain(line)
#             chains.append(chain)

#     return chains


# def extend_chain(main_chain, chains):
#     final_chain = main_chain.copy()

#     # Sort chains by length, shortest first
#     chains.sort(key=len)

#     # Process each single-glied chain
#     for single_chain in chains:
#         x1, y1 = single_chain[0]

#         # Try to insert single_chain into final_chain or its reversed version
#         inserted = False
#         for i in range(len(final_chain)):
#             if final_chain[i][1] == x1:
#                 final_chain[i:i+1] = single_chain
#                 final_chain.extend([(y, x) for x, y in single_chain[::-1]])
#                 inserted = True
#                 break
#             elif final_chain[i][1] == y1:
#                 final_chain[i:i+1] = [(y1, x1)] + single_chain
#                 final_chain.extend([(y, x) for x, y in [(y1, x1)] + single_chain[::-1]])
#                 inserted = True
#                 break

#         if not inserted:
#             final_chain.extend(single_chain)
#             final_chain.extend([(y, x) for x, y in single_chain[::-1]])

#     return final_chain


# def process_lines(lines):
#     chains = find_chains(lines)

#     if not chains:
#         return []

#     main_chain = max(chains, key=len)
#     chains.remove(main_chain)

#     extended_chain = extend_chain(main_chain, chains)

#     return extended_chain


# # Beispielinput
# lines = [(32, 34), (34, 14), (14, 15), (15, 10), (10, 26), (26, 3), (3, 32), (32, 40), (40, 15), 
#          (8, 5), (5, 31), (31, 42), (42, 20), (20, 8),
#          (14, 16), (16, 27), (27, 35), (35, 31),
#          (20, 16), 
#          (40, 26), 
#          (42, 27), 
#          (35, 34)]

# lines = [(34, 35), (35, 34), (14, 16), (16, 27), (27, 35), (35, 31), (14, 15), (15, 10), (26, 40), 
#          (40, 26), (26, 3), (3, 32), (32, 40), (40, 15),
#         (20, 16), (16, 20), (40, 26), (26, 40),
#          (42, 27), 
#          (27, 42), (35, 34), (34, 35), (31, 35), (35, 27), (27, 16), (16, 14), (8, 5), (5, 31), (31, 42), (42, 20), (20, 8), (8, 20), (20, 42), (42, 31), (31, 5), (5, 8)]
# extended_lines = process_lines(lines)
# print(extended_lines)

# #funtioniert -> problem noch, es kommt falscher input an
# def find_chains(lines):
#     chains = []
#     visited = set()

#     def find_chain(start):
#         chain = [start]
#         current = start
#         while True:
#             found = False
#             for line in lines:
#                 if line not in visited:
#                     if current[1] == line[0]:
#                         chain.append(line)
#                         current = line
#                         visited.add(line)
#                         found = True
#                         break
#             if not found:
#                 break
#         return chain

#     for line in lines:
#         if line not in visited:
#             visited.add(line)
#             chain = find_chain(line)
#             chains.append(chain)

#     return chains

# def extend_chain(main_chain, chains):
#     final_chain = main_chain.copy()

#     def try_insert_chain(chain, target_chain):
#         for i in range(len(target_chain)):
#             if target_chain[i][1] == chain[0][0]:
#                 return i + 1, chain
#             if target_chain[i][1] == chain[-1][1]:
#                 reversed_chain = [(y, x) for x, y in chain[::-1]]
#                 return i + 1, reversed_chain
#         return None, None

#     # Sort chains by length, shortest first
#     chains.sort(key=len)

#     while chains:
#         for i, chain in enumerate(chains):
#             insertion_index, modified_chain = try_insert_chain(chain, final_chain)
#             if insertion_index is not None:
#                 reversed_chain = [(y, x) for x, y in modified_chain[::-1]]
#                 final_chain[insertion_index:insertion_index] = modified_chain + reversed_chain
#                 chains.pop(i)
#                 break
#         else:
#             break  # No more insertions possible, avoid infinite loop

#     return final_chain

# def process_lines(lines):
#     chains = find_chains(lines)

#     if not chains:
#         return []

#     main_chain = max(chains, key=len)
#     chains.remove(main_chain)

#     extended_chain = extend_chain(main_chain, chains)

#     return extended_chain

# # Beispielinput
# lines = [(32, 34), (34, 14), (14, 15), (15, 10), (10, 26), (26, 3), (3, 32), (32, 40), (40, 15), 
#          (8, 5), (5, 31), (31, 42), (42, 20), (20, 8),
#          (14, 16), (16, 27), (27, 35), (35, 31),
#          (20, 16), 
#          (40, 26), 
#          (42, 27), 
#          (35, 34)]
# lines = [(32, 34), (34, 35), (35, 34), (34, 14), (14, 16), (16, 20), (20, 16), (16, 27), (27, 42),
#           (42, 27), (27, 35), (35, 31), (31, 35), (35, 27),
#             (27, 16), (16, 14), (14, 15), (15, 10),
#               (10, 26), 
#               (26, 40), 
#               (40, 26), (26, 3), (3, 32), (32, 40), (40, 15)]
# extended_lines = process_lines(lines)
# print(extended_lines)

def find_chains(lines):
    chains = []
    visited = set()

    def find_chain(start):
        chain = [start]
        current = start
        while True:
            found = False
            for line in lines:
                if line not in visited:
                    if current[1] == line[0]:
                        chain.append(line)
                        current = line
                        visited.add(line)
                        found = True
                        break
            if not found:
                break
        return chain

    for line in lines:
        if line not in visited:
            visited.add(line)
            chain = find_chain(line)
            chains.append(chain)

    return chains

def extend_chain(main_chain, chains):
    final_chain = main_chain.copy()

    def try_insert_chain(chain, target_chain):
        for i in range(len(target_chain)):
            if target_chain[i][1] == chain[0][0]:
                return i + 1, chain
            if target_chain[i][1] == chain[-1][1]:
                reversed_chain = [(y, x) for x, y in chain[::-1]]
                return i + 1, reversed_chain
        return None, None

    # Sort chains by length, shortest first
    chains.sort(key=len)

    while chains:
        for i, chain in enumerate(chains):
            insertion_index, modified_chain = try_insert_chain(chain, final_chain)
            if insertion_index is not None:
                reversed_chain = [(y, x) for x, y in modified_chain[::-1]]
                final_chain[insertion_index:insertion_index] = modified_chain + reversed_chain
                chains.pop(i)
                break
        else:
            break  # No more insertions possible, avoid infinite loop

    return final_chain

def process_lines(lines):
    chains = find_chains(lines)

    if not chains:
        return []

    main_chain = max(chains, key=len)
    chains.remove(main_chain)

    extended_chain = extend_chain(main_chain, chains)

    return extended_chain

def process_components(components):
    processed_components = []
    for component in components:
        extended_component = process_lines(component)
        processed_components.append(extended_component)
    
    # Sort processed components by length
    sorted_final = sorted(processed_components, key=len, reverse=True)
    
    return sorted_final

# Beispielinput
components = [
    [(0, 1)],
    [(19, 30), (30, 38), (38, 4), (4, 29), (29, 19), (19, 12), (12, 24), (24, 2), (2, 28), (28, 12), (30, 5), (5,100)],
    [(32, 34), (34, 14), (14, 15), (15, 10), (10, 26), (26, 3), (3, 32), (32, 40), (40, 15), 
     (8, 5), (5, 31), (31, 42), (42, 20)]
]

sorted_final = process_components(components)
print(sorted_final)
