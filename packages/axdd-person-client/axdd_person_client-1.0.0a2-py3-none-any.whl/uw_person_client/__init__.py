# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from conf.settings import AppSettings as settings  # noqa
from commonconf.backends import use_configuration_backend

# setup app settings
use_configuration_backend('conf.settings.AppSettings')

# setup logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ])
