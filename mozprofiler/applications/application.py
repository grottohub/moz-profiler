class Application:
    def __init__(self, application_name: str, path: str, force_recreate: bool = False):
        self.name = application_name
        self.modules = []
        self.path = path
        self.requirements = None
        self.venv = None
        self.force_recreate = force_recreate

    def run(self, args: str):
        raise NotImplementedError()

    def attach(self):
        raise NotImplementedError()

    def detach(self):
        raise NotImplementedError()
