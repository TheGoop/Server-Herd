import datetime
from places import parse_loc
IAMAT = "IAMAT"
WHATSAT = "WHATSAT"

class MessageExtractor:
    def __init__(self, msg):
        self.original_msg = msg
        msg.strip()
        self.msg = msg
        self.type = None
        self.IAMAT_info = dict()
        self.WHATSAT_info = dict()
        self.bad_msg = "? " + self.original_msg
        self.is_loaded = False

    def _IAMAT_handler(self, split_msg):
        try:
            coords = parse_loc(split_msg[2])
        except ValueError:
            print (err.args[0])
            raise ValueError

        self.type = split_msg[0]
        self.IAMAT_info["lat"] = coords[0]
        self.IAMAT_info["long"] = coords[1]
        self.IAMAT_info["id"] = split_msg[1]
        self.IAMAT_info["timestamp"] = split_msg[3]

    def _WHATSAT_handler(self, split_msg):
        self.type = split_msg[0]
        self.WHATSAT_info["id"] = split_msg[1]
        self.WHATSAT_info["radius"] = split_msg[2]
        self.WHATSAT_info["num_results"] = split_msg[3]

    def load_info(self):
        #if we have a bad message in this, we return the bad message else we return None

        #if its already loaded, return None
        if self.is_loaded:
            return None

        s = self.msg.split()
        if (len(s) != 4):
            return self.bad_msg

        if s[0] == IAMAT:
            try:
                self._IAMAT_handler(s)
            except ValueError:
                return self.bad_msg

        elif s[0] == WHATSAT:
            try:
                self._WHATSAT_handler(s)
            except ValueError:
                return self.bad_msg

        else:
            print("Bad command - limited to IAMAT or WHATSAT")
            return self.bad_msg

        return None








