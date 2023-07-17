pin_codes = ['1101', '9034', '0011', '0012']
def is_valid_pin_codes(pin_codes):
    pin_is_valid = []
    for i in pin_codes:
        try:
            int(i)
            if len(i) == 4 and \
                    i != '' and \
                    len(pin_codes) == len(set(pin_codes)):
                pin_is_valid.append(True)
            else:
                pin_is_valid.append(False)
        except ValueError:
            pin_is_valid.append(False)
        print(i)
    if all(pin_is_valid):
        pin_is_valid = True
    else:
        pin_is_valid = False
    return pin_is_valid
print(is_valid_pin_codes(pin_codes))