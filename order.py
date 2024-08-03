def sort_and_rearrange_components(components):
    sorted_components = []

    for component in components:
        sorted_component = []
        if not sorted_component:
            sorted_component.append(component[0])
            component = component[1:]

        while component:
            if not sorted_component:
                sorted_component.append(component.pop(0))
                continue

            last_point = sorted_component[-1][1]
            first_point = sorted_component[0][0]
            found = False

        
            for i, line in enumerate(component):
                if last_point == line[0]: 
                    sorted_component.append(line)
                    component.pop(i)
                    found = True
                    break
                elif last_point == line[1]:
                    sorted_component.append((line[1], line[0]))
                    component.pop(i)
                    found = True
                    break
            for i, line in enumerate(component):
                if first_point == line[0]:
                    sorted_component.insert(0, (line[1], line[0]))
                    component.pop(i)
                    found = True
                    break
                elif first_point == line[1]:
                    sorted_component.insert(0, line)
                    component.pop(i)
                    found = True
                    break

            if not found:
                sorted_component.append(component.pop(0))

        sorted_components.append(sorted_component)

    return sorted_components



#für die endgültige sortierung sowie einfügen von doppelten werten um rein ragende Linien zu zeichnen (nachzuzeichnen)
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
        return [], []

    main_chain = max(chains, key=len)
    chains.remove(main_chain)

    extended_chain = extend_chain(main_chain, chains)

    # Füge die verbleibenden Ketten hinzu, die nicht verbunden wurden
    remaining_chains = [chain for chain in chains if chain]

    return extended_chain, remaining_chains

def process_components(sorted_components):
    final_connected_chains = []
    final_unconnected_chains = []
    
    for component in sorted_components:
        extended_chain, remaining_chains = process_lines(component)
        final_connected_chains.extend(extended_chain)  
        for chain in remaining_chains:
            final_unconnected_chains.extend(chain) 
    
    # Sort processed components by length
    final_connected_chains = sorted(final_connected_chains, key=lambda x: len(x), reverse=True)
    final_unconnected_chains = sorted(final_unconnected_chains, key=lambda x: len(x), reverse=True)
    
    return final_connected_chains, final_unconnected_chains

