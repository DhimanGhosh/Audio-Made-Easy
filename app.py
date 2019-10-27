def run():
    wrg = Wrong()
    ch = 0
    count = 0
    while ch != 10:
        menu = Menu()
        try:
            ch = int(input("Choice: "))
        except ValueError:
            wrg.set_wrong_flag(True)
            print('The choice must an integer!\nTry Again')
            continue
        except:
            ch = None
        if ch is None:
            continue

        if ch == 1:
            menu.major_scale(wrg)

        elif ch == 2:
            menu.major_chord(wrg)

        elif ch == 3:
            menu.notes_in_major_scale(wrg)

        elif ch == 4:
            menu.note_in_major_scales(wrg)

        elif ch == 5:
            menu.note_shift_with_capo_position(wrg)

        elif ch == 6:
            menu.scale_shift_with_capo_position(wrg)
            
        elif ch == 7:
            menu.minor_scale(wrg)

        elif ch == 8:
            menu.notes_in_minor_scale(wrg)

        elif ch == 9:
            menu.best_capo_position(wrg)
            count -= 1
            
        elif ch < 1 or ch > 10:
            menu.wrong_entry(wrg)
            count -= 1
            
        count += 1
    if count > 1:
        print('Thanks for consulting music theory guide!\nSee you soon!')
    else:
        print('See you soon!')

if __name__ == '__main__':
    from Utils.Wrong import Wrong
    from Utils.Menu import Menu
    run()
