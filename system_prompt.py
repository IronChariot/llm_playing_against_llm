class SystemPrompt:
    @staticmethod
    def load_from_file(gamename, filename):
        with open('system_prompts/' + gamename + '/' + filename, 'r') as file:
            return file.read().strip()