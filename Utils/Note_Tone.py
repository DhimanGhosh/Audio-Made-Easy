def notes(octave = 0):
    # Notes Frequency, Octave 0
    C0  = 262
    Cs0 = 277
    D0  = 294
    Ds0 = 311
    E0  = 330
    F0  = 349
    Fs0 = 370
    G0  = 392
    Gs0 = 415
    A0  = 440
    As0 = 466
    B0  = 494
    
    Octave0 = [C0, Cs0, D0, Ds0, E0, F0, Fs0, G0, Gs0, A0, As0, B0]

    # Notes Frequency, Octave 1
    C1  = 523
    Cs1 = 554
    D1  = 587
    Ds1 = 622
    E1  = 659
    F1  = 699
    Fs1 = 740
    G1  = 784
    Gs1 = 831
    A1  = 880
    As1 = 932
    B1  = 988
    
    Octave1 = [C1, Cs1, D1, Ds1, E1, F1, Fs1, G1, Gs1, A1, As1, B1]

    if octave == 0:
        return Octave0
    elif octave == 1:
        return Octave1
