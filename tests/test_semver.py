import pytest

from powerstrip.utils.semver import SemVer


class TestSemVer:
    """
    test SemVer class
    """
    def test_major(self):
        # without parameter
        sv = SemVer()

        # set major part to invalid types
        for value in (None, "foobar", -1):
            with pytest.raises(AssertionError):
                sv.major = value

        # set major part to valid number
        for value in (0, 1, 2, 3):
            sv.major = value
            assert str(sv) == f"{value}.0.0"

    def test_minor(self):
        # without parameter
        sv = SemVer()

        # set minor part to invalid types
        for value in (None, "foobar", -1):
            with pytest.raises(AssertionError):
                sv.minor = value

        # set minor part to valid number
        for value in (0, 1, 2, 3):
            sv.minor = value
            assert str(sv) == f"0.{value}.0"

    def test_patch(self):
        # without parameter
        sv = SemVer()

        # set patch part to invalid types
        for value in ("foobar", -1):
            with pytest.raises(AssertionError):
                sv.patch = value

        # set patch part to valid number
        for value in (0, 1, 2, 3):
            sv.patch = value
            assert str(sv) == f"0.0.{value}"

    def test_prerelease(self):
        # without parameter
        sv = SemVer()

        # set prerelease part to invalid types
        for value in (-1, ):
            with pytest.raises(AssertionError):
                sv.prerelease = value

        # set prerelease part to valid string
        for value in ("alpha", "beta", "rc"):
            sv.prerelease = value
            assert str(sv) == f"0.0.0-{value}"

    def test_buildmetadata(self):
        # without parameter
        sv = SemVer()

        # set buildmetadata part to invalid types
        for value in (-1, 0):
            with pytest.raises(AssertionError):
                sv.buildmetadata = value

        # set buildmetadata part to valid string
        for value in ("001", "20220208", "beef"):
            sv.buildmetadata = value
            assert str(sv) == f"0.0.0+{value}"

    def test_complete(self):
        # initialize with no parameter
        sv = SemVer()
        assert str(sv) == "0.0.0"

        # initialize with some correct data
        sv = SemVer(
            major=1, minor=2, patch=3, prerelease="rc1",
            buildmetadata="20220208"
        )
        assert str(sv) == "1.2.3-rc1+20220208"

    def test_parsing(self):
        # invalid types
        for value in (-1, 0, 1, None):
            with pytest.raises(AssertionError):
                SemVer.create_from_str(value)

        # invalid string values
        for value in ("", "x", "1.x", "1.2.3.4"):
            with pytest.raises(TypeError):
                sv = SemVer.create_from_str(value)

        # valid string values
        for value in (
            "0.1.0", "1.0.2", "1.2.3", "1.2.3-rc1", "1.2.3-rc1+001",
            "0.2.1+002", "3.2.0-beta", "4.5.92-rc2+20220208"
        ):
            SemVer.create_from_str(value)
