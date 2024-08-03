# def try_insert_chain(chain, target_chain):
#     for i in range(len(target_chain)):
#         if target_chain[i][1] == chain[0][0]:
#             return i + 1, chain
#         if target_chain[i][1] == chain[-1][1]:
#             reversed_chain = [(y, x) for x, y in chain[::-1]]
#             return i + 1, reversed_chain
#     return None, None

# def merge_chains(remaining_chain, current_final_chain):
#     # Determine which chain is smaller
#     if len(remaining_chain) <= len(current_final_chain):
#         smaller_chain = remaining_chain
#         larger_chain = current_final_chain
#     else:
#         smaller_chain = current_final_chain
#         larger_chain = remaining_chain

#     # Find common numbers
#     common_numbers = []
#     for pair1 in smaller_chain:
#         for pair2 in larger_chain:
#             if pair1[1] == pair2[0] and pair1 not in common_numbers:
#                 common_numbers.append(pair1)
#             elif pair1[1] == pair2[1] and pair1 not in common_numbers:
#                 common_numbers.append(pair1)

#     if not common_numbers:
#         print("No common number found between chains.")
#         return None

#     # Split the smaller chain at each common number and merge into the larger chain
#     for common_number in common_numbers:
#         chain1 = []
#         chain2 = []
#         split1_found = False
#         split2_found = False

#         for pair in smaller_chain:
#             if not split1_found and pair[1] == common_number[1]:
#                 chain1.append(pair)
#                 split1_found = True
#             elif split1_found:
#                 chain2.append(pair)
        
#         for pair in smaller_chain:
#             if not split2_found and pair[1] == common_number[1]:
#                 chain2.append(pair)
#                 split2_found = True
#             elif split2_found:
#                 chain1.append(pair)

#         print(f"Splitting smaller chain {smaller_chain} at common number {common_number[1]} into:")
#         print(f"Chain 1: {chain1}")
#         print(f"Chain 2: {chain2}")

#         # Insert chain1 and chain2 into the larger chain
#         chains_to_insert = [chain1, chain2]
#         for chain_to_insert in chains_to_insert:
#             inserted = False
#             for i in range(len(larger_chain)):
#                 insertion_index, modified_chain = try_insert_chain(chain_to_insert, larger_chain[i])
#                 if insertion_index is not None:
#                     print(f"Inserting chain {modified_chain} into chain {larger_chain[i]} at index {insertion_index}")
#                     larger_chain[i][insertion_index:insertion_index] = modified_chain
#                     reversed_modified_chain = [(y, x) for x, y in modified_chain[::-1]]
#                     larger_chain[i][insertion_index + len(modified_chain):insertion_index + len(modified_chain)] = reversed_modified_chain
#                     inserted = True
#                     break
#             if not inserted:
#                 print(f"Appending chain {chain_to_insert} to the end of the larger chain.")
#                 larger_chain.extend(chain_to_insert)

#     print("Merged chain:", larger_chain)
#     return larger_chain


# remaining_chains = [
#     [(17, 25), (25, 11), (11, 7), (7, 11), (11, 13), (13, 41), (41, 36), (36, 41), (41, 13), (13, 18),
#      (18, 9), (9, 23), (23, 24), (24, 23), (23, 21), (21, 33)]
# ]

# current_final_chain = [
#     [(19, 12), (12, 24), (24, 2), (2, 28), (28, 12)]
# ]

# merged_chain = merge_chains(remaining_chains, current_final_chain)
# print("Merged Chain:", merged_chain)



# remaining_chains = [
#     [(17, 25), (25, 11), (11, 7), (7, 11), (11, 13), (13, 41), (41, 36), (36, 41), (41, 13), (13, 18),
#      (18, 9), (9, 23), (12, 24),(24, 2),(23, 24),(24, 23), (23, 21), (21, 33)]
# ]

# current_final_chain = [
#     [(19, 12), (12, 24),(24, 2), (2, 28), (28, 12)]
# ]
# def find_matching_subchain(remaining_chains, current_final_chain):
#     smaller_chain = remaining_chains[0]
#     larger_chain = current_final_chain[0]

#     for i in range(len(smaller_chain)):
#         match_found = True
#         for j in range(len(smaller_chain) - i):
#             if i + j >= len(smaller_chain) or j >= len(larger_chain):
#                 match_found = False
#                 break
#             if smaller_chain[i + j][1] != larger_chain[j][0]:
#                 match_found = False
#                 break
        
#         if match_found:
#             return smaller_chain[i:i + len(larger_chain)]
    
#     return None

# Beispielaufruf mit deinen gegebenen Daten
remaining_chains = [(17, 25), (25, 11), (11, 7), (7, 11), (11, 13), (13, 41), (41, 36), (36, 41), (41, 13), (13, 18),
     (18, 9), (9, 23), (23, 24), (24, 23), (23, 21), (21, 33)]

current_final_chain = [(19, 12), (12, 24), (24, 2), (2, 28), (28, 12)]





# result = find_matching_subchain(remaining_chains, current_final_chain)
# print("Übereinstimmende Teilkette gefunden:", result)


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
                return smaller_chain[:i],smaller_chain[i:]

            
split1, split2 = split_chain(remaining_chains, current_final_chain)
print("Übereinstimmende Teilkette gefunden:", split1, split2 ) 
#split_chain(remaining_chains, current_final_chain)