def underline(string):
    return "\033[4m" + string + "\033[0m"


def bright(string):
    return "\033[1m" + string + "\033[0m"


def white(string):
    return "\033[37m " + string + "\033[0m"


def green(string):
    return "\033[32m" + string + "\033[0m"


def gold(string):
    return "\033[1m\033[36m" + string + "\033[0m"


def supergreen(string):
    return "\033[37m\033[32m" + string + "\033[0m"