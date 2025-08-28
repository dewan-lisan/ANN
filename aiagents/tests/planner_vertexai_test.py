from unittest import TestCase
from aiagents.src.planner_vertexai import to_json


class PlannerVertextAiTest(TestCase):

    def test_parses_valid_json_string(self):
        valid_json = '{"key": "value"}'
        result = to_json(valid_json)
        self.assertEqual(result, {"key": "value"})

    def test_handles_invalid_json_string(self):
        invalid_json = '{"key": "value"'
        result = to_json(invalid_json)
        self.assertIsNone(result)

    def test_handles_empty_string(self):
        empty_string = ""
        result = to_json(empty_string)
        self.assertIsNone(result)

    def test_handles_non_string_input(self):
        non_string_input = 12345
        result = to_json(non_string_input)
        self.assertIsNone(result)

    def test_handles_null_input(self):
        null_input = None
        result = to_json(null_input)
        self.assertIsNone(result)
