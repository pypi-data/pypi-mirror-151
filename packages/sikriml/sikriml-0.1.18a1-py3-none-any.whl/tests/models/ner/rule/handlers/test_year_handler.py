import unittest

from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.rule.handlers import NumberHandler, YearHandler

handler = YearHandler()


class YearHandlerTest(unittest.TestCase):
    def test_year_handler_correct_result(self):
        # Arrange
        year = "1990"
        # Act
        result = handler.process(f"Was born in {year}")
        # Assert
        expected_result = set([ScoreEntity(year, 12, 16, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_with_apostrophe(self):
        # Arrange
        year = "1990's"
        # Act
        result = handler.process(f"Was born in {year}")
        # Assert
        expected_result = set([ScoreEntity("1990", 12, 16, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_with_extra_chars(self):
        # Arrange
        year = "1990th"
        # Act
        result = handler.process(f"Was born in {year}")
        # Assert
        expected_result = set([ScoreEntity("1990", 12, 16, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_time_period(self):
        # Arrange
        year = "1990-årene"
        # Act
        result = handler.process(f"Det skjedde i {year}")
        # Assert
        expected_result = set([ScoreEntity(year, 14, 24, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_invalid_year(self):
        # Arrange
        year = "2990"
        # Act
        result = handler.process(f"Some random number {year}")
        # Assert
        self.assertSetEqual(result, set())

    def test_year_handler_extra_digit_behind(self):
        # Arrange
        year = "19784"
        # Act
        result = handler.process(f"Some random number {year}")
        # Assert
        self.assertSetEqual(result, set())

    def test_year_handler_extra_digit_front(self):
        # Arrange
        year = "11978"
        # Act
        result = handler.process(f"Some random number {year}")
        # Assert
        self.assertSetEqual(result, set())

    def test_year_handler_returns_empty_set(self):
        # Act
        result = handler.process("Date of birth is unknown")
        # Assert
        self.assertSetEqual(result, set())

    def test_year_handler_as_decorator(self):
        # Arrange
        number_handler = NumberHandler()
        year_decorator = YearHandler(number_handler)
        year = "2000's"
        number = "22"
        # Act
        result = year_decorator.process(f"Was born in {year}. He is {number}")
        # Assert
        expected_result = set(
            [
                ScoreEntity("2000", 12, 16, ScoreLabel.YEAR),
                ScoreEntity(number, 26, 28, ScoreLabel.NUMB),
            ]
        )
        self.assertSetEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
