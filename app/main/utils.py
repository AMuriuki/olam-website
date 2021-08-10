def search_dict(values, searchFor):
    for k in values:
        for v in values[k]:
            if searchFor in v:
                return v
    return None
