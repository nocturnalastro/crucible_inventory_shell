class GuidedInput:
    def __init__(self, session, command, values=None):
        self.values = values or {}
        self.session = session
        self.command = command

    def get_values(self, skip_default_values=False):
        print(f"Fill in the following values for {self.command.name}")
        for expected_input in self.command.target.inputs:
            if expected_input in self.values:
                if skip_default_values:
                    continue
                default_text = f"[{self.values[expected_input]}]"
            else:
                default_text = ""
            value = self.session.prompt(f"{expected_input}{default_text}: ")
            if not value.strip():
                self.values[expected_input] = value
