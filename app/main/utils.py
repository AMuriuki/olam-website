from configparser import SafeConfigParser

parser = SafeConfigParser()


def updating(file, variables):
    parser.read(file)
    for k, v in variables.items():
        parser.set('tenant', k, v)
        with open(file, 'w') as configfile:
            parser.write(configfile)


def search_dict(values, searchFor):
    for k in values:
        for v in values[k]:
            if searchFor in v:
                return v
    return None
