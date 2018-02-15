class DataFile:
    def __init__(self, filename):
        self.filename = filename
        self.loaded_line = ''

    def __enter__(self):
        self.file = open(self.filename + '.txt', 'a+')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def write_line(self, string):
        self.file.write(string if '\n' in string else string + '\n')
        self.loaded_line = ''

    def write_values(self, *values):
        line = ''
        for value in values:
            line += value.strip() + '"'
        self.file.write(line + '\n')
        self.loaded_line = ''

    def load_values(self, *values):
        for value in values:
            self.loaded_line += value.strip() + '"'

    def load_value(self, value):
        self.load_values(value)

    def write_loaded(self):
        self.file.write(self.loaded_line + '\n')
        self.loaded_line = ''

