import datetime

IAMAT = "IAMAT"
WHATSAT = "WHATSAT"

class MessageExtractor:
    def __init__(self, msg):
        msg.strip()
        self.original_msg = msg
        self.type = None
        self.is_loaded = False


    def _IAMAT_handler(self, split_msg):

        pass

    def _WHATSAT_handler(self, split_msg):
        pass

    def load_extractor(self):
        if is_loaded:
            return

        s = self.original_msg.split()
        if (len(s) != 4):
            raise ValueError("Bad message format - incorrect number of args")

        if (s[0] == IAMAT or s[0] == WHATSAT):
            self.type = s[0]
        else:
            raise ValueError("Bad command - limited to IAMAT or WHATSAT")

        if self.type == IAMAT:
            self._IAMAT_handler(s)
        elif self.type == WHATSAT:
            self._WHATSAT_handler(s)

        self.is_loaded = True
        return








