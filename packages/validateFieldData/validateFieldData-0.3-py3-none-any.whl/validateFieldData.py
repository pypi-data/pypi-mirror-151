import re
def validateField(field, capitalize = None, spaces = False, email = False, length = 0, document = False, integer = False, string =  False):
    validateField = "{field}".format(field = field)
    validatestrip = validateField.strip()

    if capitalize == 'lowercase' and spaces is True :
        space = re.sub(r"\s+", "", field)
        data = space.lower()
        return data

    if capitalize == 'uppercase' and spaces is True :
        space = re.sub(r"\s+", "", field)
        data = space.upper()
        return data

    if capitalize == 'lowercase' and string is True :
        r1 = (r'^[a-zA-Z-ñÑ]')
        if re.match(r1, field):
            validate = "{username}".format(username = field)
            validatedata = validate.replace(" ","")
            data = validatedata.lower()
            return data
        else:
            return ("El username no es válido, solo debe contener letras")

    if capitalize == 'lowercase':        
        data = validatestrip.lower()
        return data
    
    if capitalize == 'uppercase':
        data = validatestrip.upper()
        return data
    
    if spaces is True :
        data = re.sub(r"\s+", "", field)
        return data
    
    if email is True:
        r1 = r'^[\w._%+-]+@[\w.-]+\.[a-zA-Z-ñÑ]{2,4}'
        if re.match(r1, field):
            validate = "{email}".format(email = field)
            validatedata = validate.strip()
            data = validatedata.lower()
            return data
        else:
            return ("El email no es válido")
    if length == 300:
        if len(field) >300:
            return ("El texto tiene mas de 300 caracteres")
        else:
            return validatestrip

    if document is True:
        r1 = (r'^[1-9][0-9]')
        if re.match(r1, field):
            validate = "{document}".format(document = field)
            data = validate.replace(" ","")
            return data
        else:
            return ("El documento no es válido, solo debe contener numeros")

    return validatestrip

