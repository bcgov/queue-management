import ast
import unittest
from pathlib import Path


APPOINTMENT_EVENTS = {
    'appointment_create',
    'appointment_update',
    'appointment_delete',
}


class AppointmentSocketRoomTest(unittest.TestCase):

    def test_appointment_events_are_never_broadcast_globally(self):
        app_root = Path(__file__).resolve().parents[1]
        global_emissions = []

        for path in app_root.rglob('*.py'):
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                    continue
                if node.func.attr != 'emit' or not node.args:
                    continue

                event = node.args[0]
                if not isinstance(event, ast.Constant) or event.value not in APPOINTMENT_EVENTS:
                    continue

                keyword_names = {keyword.arg for keyword in node.keywords}
                if not {'room', 'to'} & keyword_names:
                    global_emissions.append(f'{path.relative_to(app_root)}:{node.lineno}')

        self.assertEqual([], global_emissions)


if __name__ == '__main__':
    unittest.main()
