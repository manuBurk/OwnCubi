
# #idee, ich habe jetzt zwei ketten, die nciht verbundne werden wollen also remainchains und die haupt kette
# #ich suche in der kleineren kette (entweder remainingchain oder current final chain)das element was auch in der größeren kette vorhanden ist, hier wäre es jetzt die 24.
# #ich splite die kleinere Kette an der stelle also hier an der 24 und mache zwei ketten daraus. 
# #dann füge ich diese zwei kleineren ketten die aus der kleinen kette entstanden sind nacheinander in die größeere Kette ein mit den umgekehrten elementen.
# #dadurch erhalte ich dann eine große endkette.





# print("neu von klein nach gr0ß verbinden")

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

#     chains.sort(key=len)
#     print("Initial sorted chains:", chains)

#     while chains:
#         inserted = False
#         for i in range(len(chains)):
#             current_chain = chains[i]
#             for j in range(len(chains)):
#                 if i != j:
#                     insertion_index, modified_chain = try_insert_chain(current_chain, chains[j])
#                     if insertion_index is not None:
#                         print(f"Inserting chain {modified_chain} into chain {chains[j]} at index {insertion_index}")
#                         chains[j][insertion_index:insertion_index] = modified_chain
#                         reversed_modified_chain = [(y, x) for x, y in modified_chain[::-1]]
#                         chains[j][insertion_index + len(modified_chain):insertion_index + len(modified_chain)] = reversed_modified_chain
#                         chains.pop(i)
#                         inserted = True
#                         break
#             if inserted:
#                 break

#         if not inserted:
#             for i, chain in enumerate(chains):
#                 insertion_index, modified_chain = try_insert_chain(chain, final_chain)
#                 if insertion_index is not None:
#                     print(f"Inserting chain {modified_chain} at index {insertion_index}")
#                     reversed_chain = [(y, x) for x, y in modified_chain[::-1]]
#                     final_chain[insertion_index:insertion_index] = modified_chain + reversed_chain
#                     print(f"Updated final chain: {final_chain}")
#                     chains.pop(i)
#                     inserted = True
#                     break

#         if not inserted:
#             print("No more insertions possible, stopping.")
#             print(f"Remaining chains: {chains}")
#             print(f"Current final chain: {final_chain}")
#             break

#     return final_chain

# def find_common_elements(chain1, chain2):
#     elements1 = set(x for pair in chain1 for x in pair)
#     elements2 = set(x for pair in chain2 for x in pair)
#     common_elements = elements1 & elements2
#     return list(common_elements)

# def split_chain_at_element(chain, element):
#     index = next(i for i, pair in enumerate(chain) if element in pair)
#     first_part = chain[:index+1]
#     second_part = chain[index+1:]
#     return first_part, second_part

# def merge_chains(final_chain, remaining_chains):
#     if not remaining_chains:
#         return final_chain

#     while remaining_chains:
#         # Identify the smaller and larger chain
#         smaller_chain = min([final_chain] + remaining_chains, key=len)
#         larger_chain = max([final_chain] + remaining_chains, key=len)

#         # Find common elements
#         common_elements = find_common_elements(smaller_chain, larger_chain)

#         if not common_elements:
#             print("No common elements found, stopping.")
#             break

#         # Split the smaller chain at the first common element
#         common_element = common_elements[0]
#         part1, part2 = split_chain_at_element(smaller_chain, common_element)

#         # Insert the split parts into the larger chain
#         extended_chain = extend_chain(larger_chain, [part1, part2])
        
#         # Update final_chain and remaining_chains
#         if smaller_chain == final_chain:
#             final_chain = extended_chain
#         else:
#             remaining_chains.remove(smaller_chain)
#             final_chain = extended_chain

#     return final_chain

# def process_lines(lines):
#     print("Processing lines:", lines)
#     chains = find_chains(lines)
#     print("Found chains:", chains)

#     if not chains:
#         return []

#     main_chain = max(chains, key=len)
#     print("Main chain:", main_chain)
#     chains.remove(main_chain)

#     extended_chain = extend_chain(main_chain, chains)
#     print("Extended chain:", extended_chain)

#     return extended_chain

# def process_components(sorted_components):
#     processed_components = []
#     for component in sorted_components:
#         extended_component = process_lines(component)
#         processed_components.append(extended_component)
    
#     sorted_final = sorted(processed_components, key=len, reverse=True)

#     final_chain = sorted_final[0]
#     remaining_chains = sorted_final[1:]
    
#     final_chain = merge_chains(final_chain, remaining_chains)

#     return final_chain


# input= [[(19, 30), (30, 38), (38, 4), (4, 29), (29, 19), (19, 12), (12, 24), (24, 2), (2, 28), (28, 12), 
#           (25, 6), (6, 36), (36, 33), (33, 18), (18, 9), (9, 23),(23, 21), (21, 33),
#           (7, 11), (11, 13), (13, 18), 
#           (7, 39), (39, 17), (17, 25), (25, 11), 
#           (13, 41), (41, 36), 
#           (17, 22), (22, 30), 
#           (37, 22), 
#           (23, 24),
#           (29, 28), 
#           (39, 37), (37, 38)]
#         ]

# output = process_components(input)


# print(output)
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

#     chains.sort(key=len)
#     print("Initial sorted chains:", chains)

#     while chains:
#         inserted = False
#         for i in range(len(chains)):
#             current_chain = chains[i]
#             for j in range(len(chains)):
#                 if i != j:
#                     insertion_index, modified_chain = try_insert_chain(current_chain, chains[j])
#                     if insertion_index is not None:
#                         #print(f"Inserting chain {modified_chain} into chain {chains[j]} at index {insertion_index}")
#                         chains[j][insertion_index:insertion_index] = modified_chain
#                         reversed_modified_chain = [(y, x) for x, y in modified_chain[::-1]]
#                         chains[j][insertion_index + len(modified_chain):insertion_index + len(modified_chain)] = reversed_modified_chain
#                         chains.pop(i)
#                         inserted = True
#                         break
#             if inserted:
#                 break

#         if not inserted:
#             for i, chain in enumerate(chains):
#                 insertion_index, modified_chain = try_insert_chain(chain, final_chain)
#                 if insertion_index is not None:
#                     print(f"Inserting chain {modified_chain} at index {insertion_index}")
#                     reversed_chain = [(y, x) for x, y in modified_chain[::-1]]
#                     final_chain[insertion_index:insertion_index] = modified_chain + reversed_chain
#                     print(f"Updated final chain: {final_chain}")
#                     chains.pop(i)
#                     inserted = True
#                     break

#         if not inserted:
#             print("No more insertions possible, stopping.")
#             print(f"Remaining chains: {chains}")
#             print(f"Current final chain: {final_chain}")
#             break

#     return final_chain, chains, final_chain

# def find_common_elements(chain1, chain2):
#     elements1 = set(x for pair in chain1 for x in pair)
#     elements2 = set(x for pair in chain2 for x in pair)
#     common_elements = elements1 & elements2
#     return list(common_elements)

# def split_chain_at_element(chain, element):
#     index = next(i for i, pair in enumerate(chain) if element in pair)
#     first_part = chain[:index+1]
#     second_part = chain[index+1:]
#     return first_part, second_part

# def merge_chains(final_chain, remaining_chains):
#     if not remaining_chains:
#         return final_chain

#     while remaining_chains:
#         # Identify the smaller and larger chain
#         smaller_chain = min([final_chain] + remaining_chains, key=len)
#         larger_chain = max([final_chain] + remaining_chains, key=len)

#         # Find common elements
#         common_elements = find_common_elements(smaller_chain, larger_chain)

#         if not common_elements:
#             print("No common elements found, stopping.")
#             break

#         # Split the smaller chain at the first common element
#         common_element = common_elements[0]
#         part1, part2 = split_chain_at_element(smaller_chain, common_element)

#         # Insert the split parts into the larger chain
#         extended_chain, _, _ = extend_chain(larger_chain, [part1, part2])
        
#         # Update final_chain and remaining_chains
#         if smaller_chain == final_chain:
#             final_chain = extended_chain
#         else:
#             remaining_chains.remove(smaller_chain)
#             final_chain = extended_chain

#     return final_chain

# def process_lines(lines):
#     print("Processing lines:", lines)
#     chains = find_chains(lines)
#     print("Found chains:", chains)

#     if not chains:
#         return [], []

#     main_chain = max(chains, key=len)
#     print("Main chain:", main_chain)
#     chains.remove(main_chain)

#     extended_chain, remaining_chains, final_chain = extend_chain(main_chain, chains)
#     print("Extended chain:", extended_chain)
#     print("Remaining chains:", remaining_chains)

#     return extended_chain, chains, final_chain

# def process_components(sorted_components):
#     processed_components = []
#     all_chains = []
#     #final_chains = []
    
#     for component in sorted_components:
#         extended_component, chains, final_chain = process_lines(component)
#         processed_components.append(extended_component)
#         all_chains.extend(chains)
#        # final_chains.append(final_chain)
    
#     sorted_final = sorted(processed_components, key=len, reverse=True)
#     final_chain = sorted_final[0]
#     remaining_chains = sorted_final[1:]
    
#     final_chain = merge_chains(final_chain, remaining_chains)

#     return final_chain, all_chains

# input= [[(19, 30), (30, 38), (38, 4), (4, 29), (29, 19), (19, 12), (12, 24), (24, 2), (2, 28), (28, 12), 
#           (25, 6), (6, 36), (36, 33), (33, 18), (18, 9),(9, 23), (23, 21), (21, 33),
#           (7, 11), (11, 13), (13, 18), 
#           (7, 39), (39, 17), (17, 25), (25, 11), 
#           (13, 41), (41, 36), 
#           (17, 22), (22, 30), 
#           (37, 22), 
#           (23, 24),
#           (29, 28), 
#           (39, 37), (37, 38)]
#         ]

# input= [[(100,200),(30,200)]]




# final_chain, all_chains, final_chains = process_components(input)

# print("Final chain:", final_chain)
# print("Remaining chains:", all_chains)






# def split_chain(chain1, chain2):
#     if len(chain1) <= len(chain2):
#         smaller_chain = chain1
#         larger_chain = chain2
#     else:
#         smaller_chain = chain2
#         larger_chain = chain1

#     for (i, tuple1) in enumerate(smaller_chain):
#         current1 = (smaller_chain[i-1][1], smaller_chain[i][0])
#         for (j, tuple2) in enumerate(larger_chain):
#             current2 = (larger_chain[j-1][1], larger_chain[j][0])
#             if current1 == current2:
#                 return larger_chain, smaller_chain[:i],smaller_chain[i:]

# #geht nur in die if, wenn es zwei ketten am ende gibt die noch zusammengefügt werden müssen     
# if all_chains != []:
#     result = all_chains[0]
#     print(result)
#     larger_chain, split1 , split2 = split_chain(result, final_chain)
#     print("Übereinstimmende Teilkette gefunden:", split1, split2 ) 

#     chains2 = [split1,split2]

#     final = extend_chain(larger_chain, chains2)
#     # print("final",final)








#---------
#versino 12:57 -> prints kürzen

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

    chains.sort(key=len)
   # print("Initial sorted chains:", chains)

    while chains:
        inserted = False
        for i in range(len(chains)):
            current_chain = chains[i]
            for j in range(len(chains)):
                if i != j:
                    insertion_index, modified_chain = try_insert_chain(current_chain, chains[j])
                    if insertion_index is not None:
                        #print(f"Inserting chain {modified_chain} into chain {chains[j]} at index {insertion_index}")
                        chains[j][insertion_index:insertion_index] = modified_chain
                        reversed_modified_chain = [(y, x) for x, y in modified_chain[::-1]]
                        chains[j][insertion_index + len(modified_chain):insertion_index + len(modified_chain)] = reversed_modified_chain
                        chains.pop(i)
                        inserted = True
                        break
            if inserted:
                break

        if not inserted:
            for i, chain in enumerate(chains):
                insertion_index, modified_chain = try_insert_chain(chain, final_chain)
                if insertion_index is not None:
                   # print(f"Inserting chain {modified_chain} at index {insertion_index}")
                    reversed_chain = [(y, x) for x, y in modified_chain[::-1]]
                    final_chain[insertion_index:insertion_index] = modified_chain + reversed_chain
                    print(f"UPDATED final chain: {final_chain}")
                    chains.pop(i)
                    inserted = True
                    break

        if not inserted:
           # print("No more insertions possible, stopping.")
           # print(f"Remaining chains: {chains}")
           # print(f"Current final chain: {final_chain}")
            break

    return final_chain, chains, final_chain

def find_common_elements(chain1, chain2):
    elements1 = set(x for pair in chain1 for x in pair)
    elements2 = set(x for pair in chain2 for x in pair)
    common_elements = elements1 & elements2
    return list(common_elements)

def split_chain_at_element(chain, element):
    index = next(i for i, pair in enumerate(chain) if element in pair)
    first_part = chain[:index+1]
    second_part = chain[index+1:]
    return first_part, second_part

def merge_chains(final_chain, remaining_chains):
    if not remaining_chains:
        return final_chain

    while remaining_chains:
        # Identify the smaller and larger chain
        smaller_chain = min([final_chain] + remaining_chains, key=len)
        larger_chain = max([final_chain] + remaining_chains, key=len)

        # Find common elements
        common_elements = find_common_elements(smaller_chain, larger_chain)

        if not common_elements:
           # print("No common elements found, stopping.")
            break

        # Split the smaller chain at the first common element
        common_element = common_elements[0]
        part1, part2 = split_chain_at_element(smaller_chain, common_element)

        # Insert the split parts into the larger chain
        extended_chain, _, _ = extend_chain(larger_chain, [part1, part2])
        
        # Update final_chain and remaining_chains
        if smaller_chain == final_chain:
            final_chain = extended_chain
        else:
            remaining_chains.remove(smaller_chain)
            final_chain = extended_chain

    return final_chain

def process_lines(lines):
   # print("Processing lines:", lines)
    chains = find_chains(lines)
   # print("Found chains:", chains)

    if not chains:
        return [], []

    main_chain = max(chains, key=len)
   # print("Main chain:", main_chain)
    chains.remove(main_chain)

    extended_chain, remaining_chains, final_chain = extend_chain(main_chain, chains)
   # print("Extended chain:", extended_chain)
   # print("Remaining chains:", remaining_chains)

    return extended_chain, chains, final_chain

def process_components(sorted_components):
    processed_components = []
    all_chains = []
    #final_chains = []
    
    for component in sorted_components:
        extended_component, chains, final_chain = process_lines(component)
        processed_components.append(extended_component)
        all_chains.extend(chains)
       # final_chains.append(final_chain)
    
    sorted_final = sorted(processed_components, key=len, reverse=True)
    final_chain = sorted_final[0]
    remaining_chains = sorted_final[1:]
    
    final_chain = merge_chains(final_chain, remaining_chains)

    return final_chain, all_chains


def split_chain(chain1, chain2):
    if len(chain1) <= len(chain2):
        smaller_chain = chain1
        larger_chain = chain2
    else:
        smaller_chain = chain2
        larger_chain = chain1

    for (i, tuple1) in enumerate(smaller_chain):
        current1 = (smaller_chain[i-1][1], smaller_chain[i][0])
        for (j, tuple2) in enumerate(larger_chain):
            current2 = (larger_chain[j-1][1], larger_chain[j][0])
            if current1 == current2:
                return larger_chain, smaller_chain[:i],smaller_chain[i:]
