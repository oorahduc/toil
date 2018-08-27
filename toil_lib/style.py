# styles
def underline(string):
    return "\033[4m" + string + "\033[0m"


def bright(string):
    return "\033[1m" + string + "\033[0m"


def dim(string):
    return "\033[2m" + string + "\033[0m"


# colors
def dark(string):
    return "\033[30m" + string + "\033[0m"


def red(string):
    return "\033[31m" + string + "\033[0m"


def green(string):
    return "\033[32m" + string + "\033[0m"


def yellow(string):
    return "\033[33m" + string + "\033[0m"


def blue(string):
    return "\033[34m" + string + "\033[0m"


def cyan(string):
    return "\033[36m" + string + "\033[0m"


def white(string):
    return "\033[37m " + string + "\033[0m"


# brights
def brightgreen(string):
    return "\033[32;1m" + string + "\033[0m"


def brightyellow(string):
    return "\033[33;1m" + string + "\033[0m"


def brightred(string):
    return "\033[91" + string + "\033[0m"


def brightblue(string):
    return "\033[94" + string + "\033[0m"


# custom
def tagline(string):
    return "\033[36;4m" + string + "\033[0m"
