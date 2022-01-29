import re
import collections


# named tuple for sem version
SemVer = collections.namedtuple(
    "SemVer", "major minor patch prerelease buildmetadata"
)


def semver(s):
    """
    splits input string into different components of the SemVer

    => see https://semver.org
    """
    res = re.compile(
        r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|"
        r"[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-]"
        r"[0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*)"
        r")?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    ).match(s)
    if not res:
        # not a valid SemVer
        raise TypeError(f"The string '{s}' is not a valid SemVer.")

    return SemVer(**res.groupdict())
