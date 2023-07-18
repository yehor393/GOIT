def is_valid_pin_codes(pin_codes):
    pin_is_valid = False
    for i in pin_codes:
        try:
            int(i)
            if len(i) == 4 and \
                    i != '' and \
                    len(pin_codes) == len(set(pin_codes)):
                pin_is_valid = True
                continue
            else:
                pin_is_valid = False
                break
        except ValueError:
            pin_is_valid = False
            break
        print(i)
    print(pin_is_valid)
    return pin_is_valid