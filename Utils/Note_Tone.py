def notes(octave = 4):
    # Notes Frequency, Octave 0
    C0  = 0
    Cs0 = 0
    D0  = 0
    Ds0 = 0
    E0  = 0
    F0  = 0
    Fs0 = 0
    G0  = 0
    Gs0 = 0
    A0  = 0
    As0 = 0
    B0  = 0
    
    Octave0 = [C0, Cs0, D0, Ds0, E0, F0, Fs0, G0, Gs0, A0, As0, B0]

    # Notes Frequency, Octave 1
    C1  = 0
    Cs1 = 0
    D1  = 37
    Ds1 = 39
    E1  = 41
    F1  = 44
    Fs1 = 46
    G1  = 49
    Gs1 = 52
    A1  = 55
    As1 = 58
    B1  = 62
    
    Octave1 = [C1, Cs1, D1, Ds1, E1, F1, Fs1, G1, Gs1, A1, As1, B1]

    # Notes Frequency, Octave 2
    C2  = 65
    Cs2 = 69
    D2  = 73
    Ds2 = 78
    E2  = 82
    F2  = 87
    Fs2 = 93
    G2  = 98
    Gs2 = 104
    A2  = 110
    As2 = 117
    B2  = 123
    
    Octave2 = [C2, Cs2, D2, Ds2, E2, F2, Fs2, G2, Gs2, A2, As2, B2]

    # Notes Frequency, Octave 3
    C3  = 131
    Cs3 = 139
    D3  = 147
    Ds3 = 156
    E3  = 165
    F3  = 175
    Fs3 = 185
    G3  = 196
    Gs3 = 208
    A3  = 220
    As3 = 233
    B3  = 247
    
    Octave3 = [C3, Cs3, D3, Ds3, E3, F3, Fs3, G3, Gs3, A3, As3, B3]

    # Notes Frequency, Octave 4
    C4  = 262
    Cs4 = 277
    D4  = 294
    Ds4 = 311
    E4  = 330
    F4  = 349
    Fs4 = 370
    G4  = 392
    Gs4 = 415
    A4  = 440
    As4 = 466
    B4  = 494
    
    Octave4 = [C4, Cs4, D4, Ds4, E4, F4, Fs4, G4, Gs4, A4, As4, B4]

    # Notes Frequency, Octave 5
    C5  = 523
    Cs5 = 554
    D5  = 587
    Ds5 = 622
    E5  = 659
    F5  = 699
    Fs5 = 740
    G5  = 784
    Gs5 = 831
    A5  = 880
    As5 = 932
    B5  = 988
    
    Octave5 = [C5, Cs5, D5, Ds5, E5, F5, Fs5, G5, Gs5, A5, As5, B5]

    # Notes Frequency, Octave 6
    C6  = 1047
    Cs6 = 1109
    D6  = 1175
    Ds6 = 1245
    E6  = 1319
    F6  = 1397
    Fs6 = 1480
    G6  = 1568
    Gs6 = 1661
    A6  = 1760
    As6 = 1865
    B6  = 1976
    
    Octave6 = [C6, Cs6, D6, Ds6, E6, F6, Fs6, G6, Gs6, A6, As6, B6]

    # Notes Frequency, Octave 7
    C7  = 2093
    Cs7 = 2217
    D7  = 2349
    Ds7 = 2489
    E7  = 2637
    F7  = 2794
    Fs7 = 2960
    G7  = 3136
    Gs7 = 3322
    A7  = 3520
    As7 = 3729
    B7  = 3950
    
    Octave7 = [C7, Cs7, D7, Ds7, E7, F7, Fs7, G7, Gs7, A7, As7, B7]

    # Notes Frequency, Octave 8
    C8  = 4186
    Cs8 = 4435
    D8  = 4699
    Ds8 = 4978
    E8  = 5274
    F8  = 5588
    Fs8 = 5920
    G8  = 6272
    Gs8 = 6645
    A8  = 7040
    As8 = 7459
    B8  = 7902
    
    Octave8 = [C8, Cs8, D8, Ds8, E8, F8, Fs8, G8, Gs8, A8, As8, B8]

    if octave == 0:
        return Octave0
    elif octave == 1:
        return Octave1
    elif octave == 2:
        return Octave2
    elif octave == 3:
        return Octave3
    elif octave == 4:
        return Octave4
    elif octave == 5:
        return Octave5
    elif octave == 6:
        return Octave6
    elif octave == 7:
        return Octave7
    elif octave == 8:
        return Octave8
