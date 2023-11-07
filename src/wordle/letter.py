from wordle.letter_state import LetterState

# blank square emoji
blank_square = "<:blank:1170476171251687494>"

# dict containing all letters and four differnt color emojis for each
squares = {
"a": ["<:a_gray_dark:1168951510663696394>", "<:a_gray:1162435739192148038>", "<:a_yellow:1162452541783691456>", "<:a_green:1162498445790171176>"],
"b": ["<:b_gray_dark:1168951512488214588>", "<:b_gray:1162437701723750574>", "<:b_yellow:1162452544702914580>", "<:b_green:1162498447715352586>"],
"c": ["<:c_gray_dark:1168951513754902538>", "<:c_gray:1162437702990446744>", "<:c_yellow:1162452547391459538>", "<:c_green:1162498448600334376>"],
"d": ["<:d_gray_dark:1168951515558445096>", "<:d_gray:1162437706807267390>", "<:d_yellow:1162452550558167152>", "<:d_green:1162498449581817916>"],
"e": ["<:e_gray_dark:1168951516472815757>", "<:e_gray:1162437709172846615>", "<:e_yellow:1162452553385123870>", "<:e_green:1162498450559086652>"],
"f": ["<:f_gray_dark:1168951517794021447>", "<:f_gray:1162437711685226626>", "<:f_yellow:1162452554727297044>", "<:f_green:1162498451850936412>"],
"g": ["<:g_gray_dark:1168951518607720448>", "<:g_gray:1162437714201808896>", "<:g_yellow:1162452555968815278>", "<:g_green:1162498452824019127>"],
"h": ["<:h_gray_dark:1168951519429791876>", "<:h_gray:1162437716240240660>", "<:h_yellow:1162452593780465705>", "<:h_green:1162498487515107339>"],
"i": ["<:i_gray_dark:1168951650560512051>", "<:i_gray:1162437718345777244>", "<:i_yellow:1162452595428827238>", "<:i_green:1162498489025036360>"],
"j": ["<:j_gray_dark:1168951652401827900>", "<:j_gray:1162437719461482687>", "<:j_yellow:1162452597349826851>", "<:j_green:1162498490216235038>"],
"k": ["<:k_gray_dark:1168951522617471137>", "<:k_gray:1162437720539402240>", "<:k_yellow:1162452598410973284>", "<:k_green:1162498490853765221>"],
"l": ["<:l_gray_dark:1168951653194535014>", "<:l_gray:1162437721499910376>", "<:l_yellow:1162452600965308537>", "<:l_green:1162498492984459294>"],
"m": ["<:m_gray_dark:1168951731493810337>", "<:m_gray:1162437723223773286>", "<:m_yellow:1162452605071544340>", "<:m_green:1162498493991092244>"],
"n": ["<:n_gray_dark:1168951733532250212>", "<:n_gray:1162437726533058570>", "<:n_yellow:1162452649648590939>", "<:n_green:1162498538463314073>"],
"o": ["<:o_gray_dark:1168951734794735737>", "<:o_gray:1162437867491053689>", "<:o_yellow:1162452651787690065>", "<:o_green:1162498539499290824>"],
"p": ["<:p_gray_dark:1168951735914598511>", "<:p_gray:1162437901334876250>", "<:p_yellow:1162452653645758564>", "<:p_green:1162498540711456871>"],
"q": ["<:q_gray_dark:1168951736904454205>", "<:q_gray:1162437730114998312>", "<:q_yellow:1162452655440920626>", "<:q_green:1162498542246559824>"],
"r": ["<:r_gray_dark:1168951743061692416>", "<:r_gray:1162437939083624548>", "<:r_yellow:1162452657638740090>", "<:r_green:1162498543496474654>"],
"s": ["<:s_gray_dark:1168951800448172112>", "<:s_gray:1162437734636470464>", "<:s_yellow:1162452660562182204>", "<:s_green:1162498545094512713>"],
"t": ["<:t_gray_dark:1168951802545319946>", "<:t_gray:1162438000190427277>", "<:t_yellow:1162452755315703891>", "<:t_green:1162498568460972082>"],
"u": ["<:u_gray_dark:1168951804101406760>", "<:u_gray:1162437737371144322>", "<:u_yellow:1162452756813066280>", "<:u_green:1162498569308213268>"],
"v": ["<:v_gray_dark:1168951805321945241>", "<:v_gray:1162438118142644294>", "<:v_yellow:1162452758549499927>", "<:v_green:1162498570759454730>"],
"w": ["<:w_gray_dark:1168954446076723220>", "<:w_gray:1162438154549219328>", "<:w_yellow:1162452761166761994>", "<:w_green:1162498571908677682>"],
"x": ["<:x_gray_dark:1168954450002583563>", "<:x_gray:1162437740596580482>", "<:x_yellow:1162452764144701520>", "<:x_green:1162498573561237594>"],
"y": ["<:y_gray_dark:1168954452221382656>", "<:y_gray:1162438311814631492>", "<:y_yellow:1162497511307608076>", "<:y_green:1162498575016677510>"],
"z": ["<:z_gray_dark:1168954453492236288>", "<:z_gray:1162438313370730546>", "<:z_yellow:1162497513140527124>", "<:z_green:1162498576283357184>"]
}

class Letter:
    """
    A class used to represent a Wordle letter.
    """

    def __init__(self, letter:str, state:LetterState = LetterState.BLACK):
        """
        Constructs a Wordle letter.
        
        Args:
            letter (str): The letter represented by a string
            state (LetterState, optional): The state of the letter (e.g. black, gray, yellow, green). Defaults to LetterState.BLACK.
        """

        self.letter = letter
        'The letter represented by a string.'
        self.state = state
        'The state of the letter (e.g. black, gray, yellow, green).'
    
    def emoji(self) -> str:
        """
        Converts a letter into an emoji usable by Discord.

        Returns:
            str: A string representation of the letter emoji.
        """
        match self.state:
            case LetterState.BLACK:
                return squares[self.letter][0]
            case LetterState.GRAY:
                return squares[self.letter][1]
            case LetterState.YELLOW:
                return squares[self.letter][2]
            case LetterState.GREEN:
                return squares[self.letter][3]

    def __eq__(self, other):
        """
        The equality method for letters.

        Returns:
            bool: True if the letters and states are the same; otherwise false.
        """
        return isinstance(other, Letter) and self.letter == other.letter and self.state == other.state
    
    def __hash__(self) -> int:
        """
        The hash code method for letters.

        Returns:
            int: A hash code.
        """
        hash = 13
        hash = (hash * 7) + self.letter.__hash__
        hash = (hash * 7) + self.state.__hash__
        return hash
    
    def __str__(self) -> str:
        """
        A string representation of a letter.
        
        * An uppercase letter represents the green state.
        * A lowercase letter represents the yellow state.
        * A '-' represents the gray state.
        * A '?' represents the black state.

        Returns:
            str: Returns a string representation of a letter.
        """
        if self.state == LetterState.GREEN:
            return self.letter.upper()
        
        if self.state == LetterState.YELLOW:
            return self.letter.lower()
        
        if self.state == LetterState.GRAY:
            return "-"
        
        return "?"