from enum import Enum

unused_letters_dict = {
    "a": "<:a_gray_dark:1168951510663696394>",
    "b": "<:b_gray_dark:1168951512488214588>",
    "c": "<:c_gray_dark:1168951513754902538>",
    "d": "<:d_gray_dark:1168951515558445096>",
    "e": "<:e_gray_dark:1168951516472815757>",
    "f": "<:f_gray_dark:1168951517794021447>",
    "g": "<:g_gray_dark:1168951518607720448>",
    "h": "<:h_gray_dark:1168951519429791876>",
    "i": "<:i_gray_dark:1168951650560512051>",
    "j": "<:j_gray_dark:1168951652401827900>",
    "k": "<:k_gray_dark:1168951522617471137>",
    "l": "<:l_gray_dark:1168951653194535014>",
    "m": "<:m_gray_dark:1168951731493810337>",
    "n": "<:n_gray_dark:1168951733532250212>",
    "o": "<:o_gray_dark:1168951734794735737>",
    "p": "<:p_gray_dark:1168951735914598511>",
    "q": "<:q_gray_dark:1168951736904454205>",
    "r": "<:r_gray_dark:1168951743061692416>",
    "s": "<:s_gray_dark:1168951800448172112>",
    "t": "<:t_gray_dark:1168951802545319946>",
    "u": "<:u_gray_dark:1168951804101406760>",
    "v": "<:v_gray_dark:1168951805321945241>",
    "w": "<:w_gray_dark:1168954446076723220>",
    "x": "<:x_gray_dark:1168954450002583563>",
    "y": "<:y_gray_dark:1168954452221382656>",
    "z": "<:z_gray_dark:1168954453492236288>"
}

gray_letters_dict = {
    "a": "<:a_gray:1162435739192148038>",
    "b": "<:b_gray:1162437701723750574>",
    "c": "<:c_gray:1162437702990446744>",
    "d": "<:d_gray:1162437706807267390>",
    "e": "<:e_gray:1162437709172846615>",
    "f": "<:f_gray:1162437711685226626>",
    "g": "<:g_gray:1162437714201808896>",
    "h": "<:h_gray:1162437716240240660>",
    "i": "<:i_gray:1162437718345777244>",
    "j": "<:j_gray:1162437719461482687>",
    "k": "<:k_gray:1162437720539402240>",
    "l": "<:l_gray:1162437721499910376>",
    "m": "<:m_gray:1162437723223773286>",
    "n": "<:n_gray:1162437726533058570>",
    "o": "<:o_gray:1162437867491053689>",
    "p": "<:p_gray:1162437901334876250>",
    "q": "<:q_gray:1162437730114998312>",
    "r": "<:r_gray:1162437939083624548>",
    "s": "<:s_gray:1162437734636470464>",
    "t": "<:t_gray:1162438000190427277>",
    "u": "<:u_gray:1162437737371144322>",
    "v": "<:v_gray:1162438118142644294>",
    "w": "<:w_gray:1162438154549219328>",
    "x": "<:x_gray:1162437740596580482>",
    "y": "<:y_gray:1162438311814631492>",
    "z": "<:z_gray:1162438313370730546>"
}

yellow_letters_dict = {
    "a": "<:a_yellow:1162452541783691456>",
    "b": "<:b_yellow:1162452544702914580>",
    "c": "<:c_yellow:1162452547391459538>",
    "d": "<:d_yellow:1162452550558167152>",
    "e": "<:e_yellow:1162452553385123870>",
    "f": "<:f_yellow:1162452554727297044>",
    "g": "<:g_yellow:1162452555968815278>",
    "h": "<:h_yellow:1162452593780465705>",
    "i": "<:i_yellow:1162452595428827238>",
    "j": "<:j_yellow:1162452597349826851>",
    "k": "<:k_yellow:1162452598410973284>",
    "l": "<:l_yellow:1162452600965308537>",
    "m": "<:m_yellow:1162452605071544340>",
    "n": "<:n_yellow:1162452649648590939>",
    "o": "<:o_yellow:1162452651787690065>",
    "p": "<:p_yellow:1162452653645758564>",
    "q": "<:q_yellow:1162452655440920626>",
    "r": "<:r_yellow:1162452657638740090>",
    "s": "<:s_yellow:1162452660562182204>",
    "t": "<:t_yellow:1162452755315703891>",
    "u": "<:u_yellow:1162452756813066280>",
    "v": "<:v_yellow:1162452758549499927>",
    "w": "<:w_yellow:1162452761166761994>",
    "x": "<:x_yellow:1162452764144701520>",
    "y": "<:y_yellow:1162497511307608076>",
    "z": "<:z_yellow:1162497513140527124>"
}

green_letters_dict = {
    "a": "<:a_green:1162498445790171176>",
    "b": "<:b_green:1162498447715352586>",
    "c": "<:c_green:1162498448600334376>",
    "d": "<:d_green:1162498449581817916>",
    "e": "<:e_green:1162498450559086652>",
    "f": "<:f_green:1162498451850936412>",
    "g": "<:g_green:1162498452824019127>",
    "h": "<:h_green:1162498487515107339>",
    "i": "<:i_green:1162498489025036360>",
    "j": "<:j_green:1162498490216235038>",
    "k": "<:k_green:1162498490853765221>",
    "l": "<:l_green:1162498492984459294>",
    "m": "<:m_green:1162498493991092244>",
    "n": "<:n_green:1162498538463314073>",
    "o": "<:o_green:1162498539499290824>",
    "p": "<:p_green:1162498540711456871>",
    "q": "<:q_green:1162498542246559824>",
    "r": "<:r_green:1162498543496474654>",
    "s": "<:s_green:1162498545094512713>",
    "t": "<:t_green:1162498568460972082>",
    "u": "<:u_green:1162498569308213268>",
    "v": "<:v_green:1162498570759454730>",
    "w": "<:w_green:1162498571908677682>",
    "x": "<:x_green:1162498573561237594>",
    "y": "<:y_green:1162498575016677510>",
    "z": "<:z_green:1162498576283357184>"
}

class LetterState(Enum):
    """
    An enum class used to represent the state of a Wordle letter.
    """
    
    NONE = 0
    "Letters that have not been used in a guess yet."
    
    GRAY = 1
    "Letters that are not in the answer."
    
    YELLOW = 2
    "Letters that are in the answer, but in the wrong place."
    
    GREEN = 3
    "Letters that are in the answer and in the right place."

class Letter:
    """
    A class used to represent a single Wordle letter.
    """
    def __init__(self, letter:str, state:LetterState = LetterState.NONE):
        """
        DESC: Constructs a Letter object with a color state

        PARAMS:
            letter (boolean) - whether or not to use a randomly generated word
            state (letterState) - the color state of the letter
        """

        self.letter = letter
        "The letter represented by the class"
        self.states = {
            0:unused_letters_dict[letter],
            1:gray_letters_dict[letter],
            2:yellow_letters_dict[letter],
            3:green_letters_dict[letter]
        }
        "The possible states of the letter"
        self.state_id = state.value
        "The numerical value representing the state of the letter"
        self.state = self.states[self.state_id]
        "The Discord emoji identifier representing the state of the letter"
        
    
    def get_letter(self:str) -> str:
        """
        DESC: Returns the class's letter in plain text

        RETURNS: (str) the class's letter
        """
        return self.letter

    def get_state_id(self:int) -> int:
        """
        DESC: Returns the state (color) of the letter as a Discord emoji identifier

        RETURNS: (str) a Discord emoji identifer representing the class's letter's state
        """
        return self.state_id

    def get_state(self:str) -> str:
        """
        DESC: Returns the state (color) of the letter as a Discord emoji identifier

        RETURNS: (str) a Discord emoji identifer representing the class's letter's state
        """
        return self.state
    
    def set_state(self, state:LetterState, force:bool):
        """
        DESC: Changes the state (color) of a letter. If force is True, the letter's state will be
              changed regardless of its current state. If force is False, the letter's state will
              be updated ONLY IF the new state is greater than the letter's current state.

        MODIFIES: self.state_id
                  self.state

        PARAMS: state (LetterState) - a new state for the class's letter
                force (bool) - forces letter to change state regardless of current state
        """
        if force:
            self.state_id = state.value
            self.state = self.states[self.state_id]
        else:
            if state.value > self.state_id:
                self.state_id = state.value
                self.state = self.states[self.state_id]
    
    def __str__(self) -> str:
        """
        DESC: Converts letter object to the following printable format:

        RETURNS: (str) [<letter> (<color>), <letter> (<color>), <letter> (<color>), <letter> (<color>), <letter> (<color>)]
        """
        color = ""
        if self.state_id == 0:
            color = "NONE"
        elif self.state_id == 1:
            color = "GRAY"
        elif self.state_id == 2:
            color = "YELLOW"
        elif self.state_id == 3:
            color = "GREEN"
        
        return self.letter + " (" + color + ")"
    
    def __repr__(self) -> str:
        """
        DESC: Converts letter object to the following printable format:

        RETURNS: (str) [<letter> (<color>), <letter> (<color>), <letter> (<color>), <letter> (<color>), <letter> (<color>)]
        """
        color = ""
        if self.state_id == 0:
            color = "NONE"
        elif self.state_id == 1:
            color = "GRAY"
        elif self.state_id == 2:
            color = "YELLOW"
        elif self.state_id == 3:
            color = "GREEN"

        return self.letter + " (" + color + ")"