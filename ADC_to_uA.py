def ADC_to_uA(A0, gain_exp):
    res = -1000.0
    if (A0 >4.096):
        A0 = A0-8.192

    if (abs(A0) < 1):
        gain_adj = 1
    elif (abs(A0) > 4):
        gain_adj = -1
    else:
        gain_adj = 0

    A0 = A0 * (2 ** gain_exp)
    res = A0 / 0.004
    correct_A0 = A0 - res / 250
    return res , correct_A0 , gain_adj