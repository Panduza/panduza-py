import re
import logging
from colorama import Fore, Back, Style

# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL


# UGLY
PZA_LOG_LEVEL=level=logging.CRITICAL


def level_highlighter(message, patterns):
    h = message
    # for pat, style in patterns.items():
    #     h = h.replace(pat, style + pat + Style.RESET_ALL)
    return h

def re_highlighter(message, patterns, debug=""):
    h = message

    # for pat, style in patterns:
    #     matches=(re.findall(pat, h))
    #     if matches:
    #         # print(pat, ">>>>", matches)
    #         for m in matches:
    #             h = h.replace(m, debug + style + m + Style.RESET_ALL)
    return h

def highlighter(message, patterns, debug=""):
    h = message
    # for pat, style in patterns.items():
    #     h = h.replace(pat, debug + style + pat + Style.RESET_ALL)
    return h



level_patterns = {
    "DEBUG": Fore.WHITE + Style.DIM,
    "INFO": Fore.BLUE + Style.NORMAL,
    "WARN": Fore.YELLOW + Style.BRIGHT,
    "ERROR": Fore.RED + Style.BRIGHT,
    "CRITICAL": Back.RED + Style.BRIGHT,
}

re_patterns = [
    # [ re.compile(r'[\s,{+](-?[0-9.]+)'), Fore.CYAN], # numbers
    [ re.compile(r'[\s,]+(\d.+)[\s,]+'), Fore.CYAN], # numbers
    [ re.compile(r'[\s,{}]+(\'.*?\')'), Fore.YELLOW], # strings
    [ re.compile(r'[\s,{}]+(\".*?\")'), Fore.YELLOW], # strings
    [ re.compile(r'[\s=]+(%.*?%)'), Fore.BLUE], # topics
    [ re.compile(r'<.*?>+'), Fore.GREEN], # topics
]

patterns = {
    "started!": Fore.GREEN,
    "MSG_IN": Fore.MAGENTA,
    "MSG_OUT": Fore.CYAN,
}


BACKS = [Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE]





class MainFormatter(logging.Formatter):

    # NextBackId=0

    # def __init__(self):
    #     super().__init__()
    #     self.back_id = MainFormatter.NextBackId
    #     self.back = BACKS[self.back_id]
    #     MainFormatter.NextBackId = (MainFormatter.NextBackId+1)%len(BACKS)


    def formatMessage(self, record):

        # print(record.__dict__)
        # print(self.back_id)

        debug=""
        # if record.levelname == "DEBUG":
        #     debug=Style.DIM

        hmsg = record.message
        hmsg = re_highlighter(hmsg, re_patterns, debug)
        hmsg = highlighter(hmsg, patterns, debug)
        
        output = ""
        output += record.threadName.ljust(12, ' ')[:12] + "| "
        output += level_highlighter(record.levelname.ljust(8, ' '), level_patterns)
        output += "| "
        output += debug + hmsg

        return output



Initialized=False
def create_logger(name):

    __logger = logging.getLogger()

    global Initialized
    if not Initialized:
        Initialized=True
        ch = logging.StreamHandler()
        ch.setFormatter(MainFormatter())
        __logger.addHandler(ch)

    return __logger




