"""Rosetta Sections Handler."""

import configparser as ConfigParser
import logging
import sys

logger = logging.getLogger(__name__)


class RosettaCSVSections:
    """Rosetta CSV sections object."""

    sections = None
    config = None

    def __init__(self, configfile):
        """Constructor."""
        self.config = ConfigParser.RawConfigParser()
        self.config.read(configfile, encoding="utf-8")
        if self.config.has_option("rosetta csv fields", "CSVSECTIONS"):
            sections = self.config.get("rosetta csv fields", "CSVSECTIONS").split(",")

        self.sections = []
        for section in sections:
            if self.config.has_option("rosetta csv fields", section):
                sectiondict = {}
                fieldlist = self.config.get("rosetta csv fields", section)
                sectiondict[section] = fieldlist.split(",")

                self.sections.append(sectiondict)
            else:
                logger.error("error reading fields from config file, exiting...")
                sys.exit(1)
