import os
import pytest

from awsimple import use_moto_mock_env_var

is_mocked_flag = True  # set to True to tell awsimple to use moto mock

print(f"{is_mocked_flag=}")


@pytest.fixture(scope="session", autouse=True)
def options():
    print(f"{is_mocked_flag=}")


@pytest.fixture(autouse=True)
def is_mocked():

    def clear_mock_env_var():
        try:
            del os.environ[use_moto_mock_env_var]
        except KeyError:
            pass

    if is_mocked_flag:
        os.environ[use_moto_mock_env_var] = "1"
    yield is_mocked_flag
    clear_mock_env_var()
