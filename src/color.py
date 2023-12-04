class Color:
    # Reset styles
    RESET = "\033[0m"
    RESET_FG = "\033[39m"
    RESET_BG = "\033[49m"

    # Text styles
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    CONCEAL = "\033[8m"
    STRIKETHROUGH = "\033[9m"

    # Foreground text color
    class Foreground:
        BLACK = "\033[30m"
        LIGHT_RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        LIGHT_GRAY = "\033[37m"
        WHITE = "\033[38m"
        GRAY = "\033[90m"
        RED = "\033[91m"
        LIME = "\033[92m"
        GOLD = "\033[93m"
        LIGHT_BLUE = "\033[94m"
        PINK = "\033[95m"
        TURQUOISE = "\033[96m"

    # Background text color
    class Background:
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        YELLOW = "\033[43m"
        BLUE = "\033[44m"
        MAGENTA = "\033[45m"
        CYAN = "\033[46m"
        LIGHT_GRAY = "\033[47m"
        GRAY = "\033[100m"
        LIGHT_RED = "\033[101m"
        LIME = "\033[102m"
        GOLD = "\033[103m"
        LIGHT_BLUE = "\033[104m"
        PINK = "\033[105m"
        TURQUOISE = "\033[106m"

    @staticmethod
    def attribute(attribute: str):
        items: list[tuple[str, "Any"]] = list(Color.__dict__.items())
        items.extend(Color.Foreground.__dict__.items())
        items.extend(Color.Background.__dict__.items())

        for key, value in items:
            if key.isupper() and attribute == value:
                return key

        return None

    @staticmethod
    def styletext(message: str, *attributes):
        """
        Styles the message with the given attributes.

        :param message: The message to style.
        :param attributes: The styles to use. Can provide a list of styles or can list the styles one at a time.
        :return: The styled message.
        """
        style = ""
        for attr in attributes:
            if not isinstance(attr, list) and Color.attribute(attr):
                style += attr
            style += ''.join(value for value in attr if Color.attribute(value))
        return style + message + Color.RESET

    @staticmethod
    def print(message: str, *attributes):
        """
        Prints a styled message.

        :param message: The message to style and print.
        :param attributes: The styles to use. Can provide a list of styles or can list the styles one at a time.
        """
        print(Color.styletext(message, attributes))


if __name__ == "__main__":
    # Foreground
    print(Color.Foreground.BLACK + "black")
    print(Color.Foreground.LIGHT_RED + "light red")
    print(Color.Foreground.GREEN + "green")
    print(Color.Foreground.YELLOW + "yellow")
    print(Color.Foreground.BLUE + "blue")
    print(Color.Foreground.MAGENTA + "magenta")
    print(Color.Foreground.CYAN + "cyan")
    print(Color.Foreground.LIGHT_GRAY + "light gray")
    print(Color.Foreground.WHITE + "white")
    print(Color.Foreground.GRAY + "gray")
    print(Color.Foreground.RED + "red")
    print(Color.Foreground.LIME + "lime")
    print(Color.Foreground.LIGHT_BLUE + "light blue")
    print(Color.Foreground.GOLD + "gold")
    print(Color.Foreground.PINK + "pink")
    print(Color.Foreground.TURQUOISE + "turquoise")

    # Background
    print(Color.Background.BLACK + Color.Foreground.WHITE + "black")
    print(Color.Background.LIGHT_RED + Color.Foreground.BLACK + "light red")
    print(Color.Background.GREEN + "green")
    print(Color.Background.YELLOW + "yellow")
    print(Color.Background.BLUE + "blue")
    print(Color.Background.MAGENTA + "magenta")
    print(Color.Background.CYAN + "cyan")
    print(Color.Background.LIGHT_GRAY + "light gray")
    print(Color.Background.GRAY + "gray")
    print(Color.Background.RED + "red")
    print(Color.Background.LIME + "lime")
    print(Color.Background.LIGHT_BLUE + "light blue")
    print(Color.Background.GOLD + "gold")
    print(Color.Background.PINK + "pink")
    print(Color.Background.TURQUOISE + "turquoise")
