import json
from typing import List, Union, Dict, Set

Element = Union[str, int]
Cluster = List[Element]
Ranking = List[Union[Element, Cluster]]


def flatten_ranking(ranking: Ranking) -> List[Element]:

    flat = []
    for item in ranking:
        if isinstance(item, list):
            flat.extend(item)
        else:
            flat.append(item)
    return flat


def build_preference_matrix(ranking: Ranking) -> Dict[Element, Set[Element]]:

    flat = flatten_ranking(ranking)
    pref = {elem: set() for elem in flat}


    processed = set()

    for item in ranking:
        if isinstance(item, list):

            cluster_elements = set(item)

            for elem in cluster_elements:
                pref[elem].update(processed)

            processed.update(cluster_elements)
        else:

            pref[item].update(processed)
            processed.add(item)

    return pref


def find_contradictions(pref1: Dict[Element, Set[Element]],
                        pref2: Dict[Element, Set[Element]]) -> List[Cluster]:

    all_elements = set(pref1.keys()) | set(pref2.keys())
    contradictions = set()

    for a in all_elements:
        for b in all_elements:
            if a == b:
                continue


            a_before_b_in_1 = b in pref1.get(a, set())
            b_before_a_in_1 = a in pref1.get(b, set())
            a_before_b_in_2 = b in pref2.get(a, set())
            b_before_a_in_2 = a in pref2.get(b, set())


            if (a_before_b_in_1 and b_before_a_in_2) or (b_before_a_in_1 and a_before_b_in_2):
                contradictions.add(tuple(sorted([a, b])))

    result = []
    processed = set()


    for a, b in contradictions:
        if a in processed or b in processed:
            continue


        cluster = set([a, b])
        changed = True
        while changed:
            changed = False
            for x, y in contradictions:
                if (x in cluster or y in cluster) and not (x in cluster and y in cluster):
                    cluster.update([x, y])
                    changed = True

        result.append(sorted(list(cluster)))
        processed.update(cluster)

    return result


def merge_clusters(clusters: List[Cluster], ranking: Ranking) -> Ranking:

    elem_to_cluster = {}
    for cluster in clusters:
        for elem in cluster:
            elem_to_cluster[elem] = cluster

    result = []
    used = set()

    for item in ranking:
        if isinstance(item, list):

            new_cluster = []
            for elem in item:
                if elem in elem_to_cluster:

                    conflict_cluster = elem_to_cluster[elem]
                    if conflict_cluster[0] not in used:

                        result.append(conflict_cluster)
                        used.update(conflict_cluster)
                elif elem not in used:
                    new_cluster.append(elem)
                    used.add(elem)

            if new_cluster:
                if len(new_cluster) == 1:
                    result.append(new_cluster[0])
                else:
                    result.append(new_cluster)
        else:

            if item in elem_to_cluster:
                conflict_cluster = elem_to_cluster[item]
                if conflict_cluster[0] not in used:
                    result.append(conflict_cluster)
                    used.update(conflict_cluster)
            elif item not in used:
                result.append(item)
                used.add(item)

    return result


def main(json_str1: str, json_str2: str) -> str:

    ranking1: Ranking = json.loads(json_str1)
    ranking2: Ranking = json.loads(json_str2)


    pref1 = build_preference_matrix(ranking1)
    pref2 = build_preference_matrix(ranking2)


    core = find_contradictions(pref1, pref2)


    merged_from_1 = merge_clusters(core, ranking1)

    final_ranking = merge_clusters(core, ranking2)


    def convert_elements(ranking):
        result = []
        for item in ranking:
            if isinstance(item, list):
                result.append([str(elem) for elem in item])
            else:
                result.append(str(item))
        return result

    final_converted = convert_elements(final_ranking)


    return json.dumps(final_converted, ensure_ascii=False)



if __name__ == "__main__":

    ranking_a = '[1, [2, 3], 4, [5, 6, 7], 8, 9, 10]'
    ranking_b = '[[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]'

    result = main(ranking_a, ranking_b)
    print("Согласованная кластерная ранжировка:")
    print(result)


    ranking1 = json.loads(ranking_a)
    ranking2 = json.loads(ranking_b)
    pref1 = build_preference_matrix(ranking1)
    pref2 = build_preference_matrix(ranking2)
    core = find_contradictions(pref1, pref2)
    print("\nЯдро противоречий:")
    print(json.dumps(core, ensure_ascii=False))