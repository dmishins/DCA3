def ADC_to_uA(V, g_exp):
    res = -1000.0
    if (V >4.096):
        V = V-8.192

    if (abs(V) < 1):
        gain_adj = 1
    elif (abs(V) > 4):
        gain_adj = -1
    else:
        gain_adj = 0

    V = V * (2 ** g_exp)
    res = V / 0.004
    correct_V = V - res / 250
    return res , correct_V , gain_adj