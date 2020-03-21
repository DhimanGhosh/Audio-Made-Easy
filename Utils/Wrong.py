class Wrong:
    __wrong_flag = False
    __wrong_count = []
    __made_right_choice_atleast_once = False

    def __init__(self):
        self.__wrong_flag = False
        self.__wrong_count = []

    def set_wrong_flag(self, wrong_flag):
        self.__wrong_flag = wrong_flag
        if wrong_flag: # Wrong Choice
            self.__wrong_count_inc()
        else: # Right Choice
            self.__wrong_count_reset()
            self.__made_right_choice_atleast_once = True

    def __wrong_count_inc(self):
        self.__wrong_count.append(self.__wrong_flag)
        if len(self.__get_wrong_count()) >= 3:
            if self.__wrong_count[-3:] == [True]*3:
                if self.__made_right_choice_atleast_once:
                    print('Session Closed!\nYou have made consecutive \'3\' wrong entries!\nThanks for consulting music theory guide!\nSee you soon!')
                else:
                    print('Session Closed!\nYou have made consecutive \'3\' wrong entries!\nSee you soon!')
                exit()

    def __wrong_count_reset(self):
        if len(self.__get_wrong_count()) > 0:
            #self.__wrong_count.pop() # For 3 wrong counts
            self.__wrong_count = [] # For consecutive 3 wrong counts
    
    def __get_wrong_count(self):
        return self.__wrong_count