import unittest
import reeds_shepp as rs


class TestLetter(unittest.TestCase):
    def setUp(self) -> None:
        self.letter = rs.Letter(1.5, rs.Steering.LEFT, rs.Gear.FORWARD)

    def test_repr(self):
        self.assertEqual(
            repr(self.letter), 
            '{ Steering: left' + '\tGear: forward' + '\tLength: 1.5 }'
        )

    def test_reverse_steering(self):
        self.letter.reverse_steering()
        self.assertEqual(
            self.letter.steering,
            rs.Steering.RIGHT
        )

    def test_reverse_gear(self):
        self.letter.reverse_gear()
        self.assertEqual(
            self.letter.gear,
            rs.Gear.BACKWARD
        )

    # def test_with_negative_parameter(self):
    #     letter = rs.Letter(-1.5, rs.Steering.LEFT, rs.Gear.FORWARD)
    #     self.assertEqual(
    #         letter,
    #         rs.Letter(1.5, rs.Steering.LEFT, rs.Gear.BACKWARD)
    #     )


class TestWordLength(unittest.TestCase):
    def test_with_positive_path_elements(self):
        word = [rs.Letter(1.5, rs.Steering.LEFT, rs.Gear.FORWARD) for _ in range(2)]
        self.assertEqual(
            rs.word_length(word),
            3
        )


class TestTimeflip(unittest.TestCase):
    def setUp(self) -> None:
        self.word = [rs.Letter(1.5, rs.Steering.LEFT, g) for g in (rs.Gear.FORWARD, rs.Gear.BACKWARD)]
        self.timeflipped = rs.timeflip(self.word)

    def test_it_flips_forward_backward(self):
        self.assertEqual(
            self.timeflipped[0].gear,
            rs.Gear.BACKWARD
        )
        self.assertEqual(
            self.timeflipped[1].gear,
            rs.Gear.FORWARD
        )

    def test_it_does_not_mutate_original_word(self):
        self.assertEqual(
            self.word[0].gear,
            rs.Gear.FORWARD,
        )


class TestReflect(unittest.TestCase):
    def setUp(self) -> None:
        self.word = [rs.Letter(1.5, s, rs.Gear.FORWARD) for s in (rs.Steering.LEFT, rs.Steering.STRAIGHT, rs.Steering.RIGHT)]
        self.reflected = rs.reflect(self.word)

    def test_it_reflects_steering(self):
        self.assertEqual(
            self.reflected[0].steering,
            rs.Steering.RIGHT
        )
        self.assertEqual(
            self.reflected[1].steering,
            rs.Steering.STRAIGHT
        )
        self.assertEqual(
            self.reflected[2].steering,
            rs.Steering.LEFT
        )

    def test_it_does_not_mutate_original_path(self):
        self.assertEqual(
            self.word[0].steering,
            rs.Steering.LEFT,
        )


class TestGetOptimalWord(unittest.TestCase):
    def test_optimal_word(self):
        word = rs.get_optimal_word((0, 0, 0), (1, 0, 0))
        self.assertEqual(
            repr(word),
            repr([rs.Letter(1.0, rs.Steering.STRAIGHT, rs.Gear.FORWARD)])
        )


if __name__ == '__main__':
    unittest.main()
