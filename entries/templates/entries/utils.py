def count_entries_with_keyword(entries, keyword):
    if not isinstance(keyword, str):
        raise ValueError("Keyword must be a string.")
    return sum(1 for entry in entries if keyword.lower() in entry.lower())
