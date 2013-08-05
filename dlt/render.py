def field_to_text(field):
    txt = "{name}:{value}"
    if not field.name:
        txt = "{value}"
    value = ""
    for v in field:
        value += "{value}".format(value=v)
    return txt.format(name=field.name.strip(), value=value)


def paragraph_to_text(paragraph):
    txt = ""
    for field in paragraph:
        txt += '{0}'.format(field_to_text(field))
    return txt


def paragraphs_to_text(data):
    txt = ""
    for paragraph in data:
        txt += '{0}\n\n'.format(paragraph_to_text(paragraph))
    return txt[:-1]
