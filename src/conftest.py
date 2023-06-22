import os

# Set on the earliest possible moment
os.environ["PYTEST_RUNNING"] = "true"

from src.apps.authentication.tests.fixtures import *  # noqa: F401, F403, E402
from src.apps.core.tests.fixtures import *  # noqa: F401, F403, E402
