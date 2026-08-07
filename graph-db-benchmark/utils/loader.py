def load_wiki_vote(file_path):
    edges = []

    with open(file_path, "r", encoding="utf-8") as file:

        for line in file:

            # Skip comments
            if line.startswith("#"):
                continue

            # Remove spaces/newlines
            line = line.strip()

            if not line:
                continue

            source, target = line.split()

            edges.append((int(source), int(target)))

    return edges