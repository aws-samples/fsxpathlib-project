# -*- coding: utf-8 -*-

import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, format="<level>{message}</level>")

TAB = "  "
TAB1 = TAB
TAB2 = TAB * 2
TAB3 = TAB * 3
TAB4 = TAB * 4
TAB5 = TAB * 5
