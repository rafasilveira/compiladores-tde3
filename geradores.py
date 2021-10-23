label_num = 0
temp_num = 0


def gera_label():
    global label_num
    out = f"LB00{label_num}"
    label_num += 1
    return out


def gera_temp():
    global temp_num
    out = f"T00{temp_num}"
    temp_num += 1
    return out
