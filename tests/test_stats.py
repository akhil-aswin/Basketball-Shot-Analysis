import pandas as pd
import pytest

from stats import bar_widths, compute_stats, get_initials


def _shot(made, shot_type, team_name='Lakers'):
    return {'SHOT_MADE_FLAG': made, 'SHOT_TYPE': shot_type, 'TEAM_NAME': team_name}


class TestComputeStats:
    def test_empty_dataframe_returns_zeroed_stats(self):
        df = pd.DataFrame(columns=['SHOT_MADE_FLAG', 'SHOT_TYPE', 'TEAM_NAME'])
        assert compute_stats(df) == {'fg': 0.0, '3p': 0.0, 'ppp': 0.0, 'fga': 0, 'team': ''}

    def test_mixed_makes_and_misses(self):
        df = pd.DataFrame([
            _shot(1, '2PT Field Goal'),
            _shot(0, '2PT Field Goal'),
            _shot(1, '3PT Field Goal'),
            _shot(0, '3PT Field Goal'),
        ])
        result = compute_stats(df)
        assert result['fga'] == 4
        assert result['fg'] == 50.0
        assert result['3p'] == 50.0
        assert result['ppp'] == round((1 * 2 + 1 * 3) / 4, 2)
        assert result['team'] == 'Lakers'

    def test_no_three_point_attempts_does_not_divide_by_zero(self):
        df = pd.DataFrame([
            _shot(1, '2PT Field Goal'),
            _shot(0, '2PT Field Goal'),
        ])
        result = compute_stats(df)
        assert result['3p'] == 0.0
        assert result['fg'] == 50.0

    def test_all_makes(self):
        df = pd.DataFrame([
            _shot(1, '2PT Field Goal'),
            _shot(1, '3PT Field Goal'),
        ])
        result = compute_stats(df)
        assert result['fg'] == 100.0
        assert result['3p'] == 100.0
        assert result['ppp'] == 2.5

    def test_team_taken_from_first_row(self):
        df = pd.DataFrame([
            _shot(1, '2PT Field Goal', team_name='Celtics'),
            _shot(0, '2PT Field Goal', team_name='Celtics'),
        ])
        assert compute_stats(df)['team'] == 'Celtics'

    def test_missing_team_name_column(self):
        df = pd.DataFrame([
            {'SHOT_MADE_FLAG': 1, 'SHOT_TYPE': '2PT Field Goal'},
        ])
        assert compute_stats(df)['team'] == ''


class TestBarWidths:
    def test_scales_proportionally(self):
        a, b = bar_widths(50, 100, max_px=56)
        assert a == 28
        assert b == 56

    def test_equal_values_produce_equal_max_width(self):
        a, b = bar_widths(10, 10, max_px=56)
        assert a == b == 56

    def test_both_zero_avoids_division_by_zero(self):
        a, b = bar_widths(0, 0)
        assert a == 0
        assert b == 0

    def test_custom_max_px(self):
        a, b = bar_widths(1, 2, max_px=10)
        assert a == 5
        assert b == 10


class TestGetInitials:
    def test_two_part_name(self):
        assert get_initials('LeBron James') == 'LJ'

    def test_three_part_name_uses_first_and_last(self):
        assert get_initials('Karl Anthony Towns') == 'KT'

    def test_single_word_name_uses_first_two_letters(self):
        assert get_initials('Giannis') == 'GI'

    def test_lowercase_input_is_uppercased(self):
        assert get_initials('stephen curry') == 'SC'
