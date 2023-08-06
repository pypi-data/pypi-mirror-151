"""
Protocol definitions for bonsai3 library
"""
__copyright__ = "Copyright 2020, Microsoft Corp."

# pyright: strict

from argparse import ArgumentParser, SUPPRESS
import json
import os
import sys
from typing import List, Optional
import uuid


# CLI help strings
_ACCESS_KEY_HELP = """
    The access key to use when connecting to the BRAIN server. If
    specified, it will be used instead of any access key
    information stored in a bonsai config file.
    """

_WORKSPACE_HELP = """
    This is the value of the workspace.
    """

_SIM_CONTEXT_HELP = """
    This is an opaque string.
    """


class BonsaiClientConfig:
    """Configuration information needed to connect to the service."""

    server = ""  # type: str
    workspace = ""  # type: str
    access_key = ""  # type: str
    simulator_context = ""  # type: str

    def __init__(
        self,
        workspace: str = "",
        access_key: str = "",
        enable_logging: bool = False,
        argv: Optional[List[str]] = sys.argv,
    ):
        """
        Initialize a config object.

        Command line argument switches will take priority over environment variables.
        Environment variables will take priority over initializer parameters.
        """

        # defaults
        self.server = os.getenv("SIM_API_HOST", "https://api.bons.ai")
        self.workspace = os.getenv("SIM_WORKSPACE", workspace)
        self.access_key = os.getenv("SIM_ACCESS_KEY", access_key)
        self.simulator_context = os.getenv("SIM_CONTEXT", "")
        self.enable_logging = enable_logging

        # parse the args last
        if argv:
            self.argparse(argv)

        # Finally, if this is an unmanaged simulator, then give it a clientId.
        # Here's why: If this simulator is given a Purpose via the BonsaiCLI,
        # then, if/when it re-registers, SimulatorGateway will restore this
        # simulator's Purpose.
        if not self.simulator_context:
            client_id = uuid.uuid4().hex
            self.simulator_context = json.dumps({"simulatorClientId": client_id})

    def argparse(self, argv: List[str]):
        """parser command line arguments"""
        parser = ArgumentParser(allow_abbrev=False)

        parser.add_argument("--accesskey", "--access-key", help=_ACCESS_KEY_HELP)
        parser.add_argument("--workspace", help=_WORKSPACE_HELP)
        parser.add_argument("--sim-context", help=_SIM_CONTEXT_HELP)
        parser.add_argument("--api-host", help=SUPPRESS)

        args, _ = parser.parse_known_args(argv[1:])

        # unpack arguments
        if args.accesskey:
            self.access_key = args.accesskey

        if args.workspace:
            self.workspace = args.workspace

        if args.sim_context:
            self.simulator_context = args.sim_context

        if args.api_host:
            self.server = args.api_host


def validate_config(config: BonsaiClientConfig):
    if not config.workspace:
        raise RuntimeError(
            "Workspace has not been set. Please set env variable SIM_WORKSPACE, "
            "pass in workspace in config constructor, or set the workspace property "
            "on the config object."
        )
    if not config.access_key:
        raise RuntimeError(
            "Access Key has not been set. Please set env variable SIM_ACCESS_KEY, "
            "pass in access_key in config constructor, or set the access_key property "
            "on the config object."
        )
