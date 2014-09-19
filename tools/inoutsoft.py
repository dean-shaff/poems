import os

class InOut(object):
    def __init__(self, directory):
        self.old_dir = os.getcwd()
        self.new_dir = directory
        os.chdir(self.new_dir)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.go_out()
        return isinstance(value, OSError)

    def go_in(self):
        os.chdir(self.new_dir)

    def go_out(self):
        os.chdir(self.old_dir)