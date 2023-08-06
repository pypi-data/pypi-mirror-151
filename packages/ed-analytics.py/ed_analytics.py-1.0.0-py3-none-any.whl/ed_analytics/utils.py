import re


UTC_FORMAT = re.compile(r"^\d{4}\-[01][0-9]\-[0-3][0-9]T[012][0-9]\-[0-5][0-9]\-[0-5][0-9]Z$")


def verifyUTC(ts):
    return UTC_FORMAT.match(ts)
