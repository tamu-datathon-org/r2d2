def format_top_n_items(data, n=5):
    total_count = sum([data[item] for item in data])
    item_count_list = [(item, data[item]) for item in data]
    item_count_list.sort(key=lambda x: x[1], reverse=True)
    top_n_items = [
        f"{item}: {count} ({int(count / total_count * 100)}%)" for item, count in item_count_list[:5]]
    return "\n\t\t|>| " + "\n\t\t|>| ".join(top_n_items)


def format_dict(data):
    total_count = sum([data[item] for item in data])
    items = [
        f"{item}: {data[item]} ({int(data[item] / total_count * 100)}%)" for item in data]
    return "\n\t\t|>| " + "\n\t\t|>| ".join(items)


def format_stats_for_message(stats):
    top_5_majors_str = format_top_n_items(stats["majors"])
    top_5_schools_str = format_top_n_items(stats["schools"])
    top_5_locations_str = format_top_n_items(stats["locations"])

    genders_str = format_dict(stats["genders"])
    classifications_str = format_dict(stats["classifications"])
    return f"""
    ```
  | ## General Stats:
  | Number of applicants: {stats["num_apps"]}
  | Top 5 Locations: {top_5_locations_str}
  | Gender Distribution: {genders_str}

  | ## Education Stats
  | First Generation Students: {stats["first_gen"]} ({int(stats["first_gen"]/stats["num_apps"]*100)}%)
  | Classification Distribution: {classifications_str}
  | Top 5 Majors: {top_5_majors_str}
  | Top 5 Schools: {top_5_schools_str}
    ```
    """
