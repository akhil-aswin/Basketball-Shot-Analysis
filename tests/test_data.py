from data import _height_to_inches


class TestHeightToInches:
    def test_valid_height(self):
        assert _height_to_inches('6-9') == 81

    def test_zero_inches(self):
        assert _height_to_inches('7-0') == 84

    def test_double_digit_inches(self):
        assert _height_to_inches('5-11') == 71

    def test_missing_separator_returns_none(self):
        assert _height_to_inches('69') is None

    def test_non_numeric_returns_none(self):
        assert _height_to_inches('six-nine') is None

    def test_empty_string_returns_none(self):
        assert _height_to_inches('') is None

    def test_none_input_returns_none(self):
        assert _height_to_inches(None) is None
