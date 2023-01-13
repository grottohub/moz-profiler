import os

from applications.application import Application
from applications.mozphab import MozPhabApplication
from utils.storage import storage


def generate_application(application: str, force_recreate: bool) -> Application:
    if application == "moz-phab":
        moz_phab_path = storage.get("moz-phab-path")
        path = os.getcwd() if moz_phab_path is None else moz_phab_path
        return MozPhabApplication(
            application_name=application,
            path=path,
            force_recreate=force_recreate,
        )
    else:
        raise NotImplementedError("Application not supported.")
