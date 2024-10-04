"""Primary Rosetta CSV generator functions."""

# pylint: disable=R1702,R0912,R0915,C0301,R0902,C0103

import configparser as ConfigParser
import logging
import sys
from urllib.parse import urlparse

try:
    from droid_csv_handler import DroidCSVHandler
    from json_table_schema import json_table_schema
    from rosetta_csv_sections import RosettaCSVSections
except ModuleNotFoundError:
    try:
        from rosetta_csv.droid_csv_handler import DroidCSVHandler
        from rosetta_csv.json_table_schema import json_table_schema
        from rosetta_csv.rosetta_csv_sections import RosettaCSVSections
    except ModuleNotFoundError:
        from src.rosetta_csv.droid_csv_handler import DroidCSVHandler
        from src.rosetta_csv.json_table_schema import json_table_schema
        from src.rosetta_csv.rosetta_csv_sections import RosettaCSVSections

logger = logging.getLogger(__name__)


def ingest_path_from_droid_row(droid_row: dict, path_mask: str) -> str:
    """Return an ingest path from a droid row with pathmask removed."""
    file_name = droid_row["NAME"].strip()
    file_path = droid_row["FILE_PATH"].strip()
    ingest_path = file_path.replace(file_name, "").replace(path_mask, "", 1)
    ingest_path = ingest_path.replace("\\", "/")
    return ingest_path.strip()


def zip_ingest_path_from_droid_row(droid_row: dict, path_mask: str) -> str:
    """Return an ingest path from a droid row with pathmask removed for
    zip ingests."""
    logger.warning("include zips functionality requires further testing...")
    path = droid_row["URI"]
    return (
        "/".join(urlparse(path).path.split("/")[1:-1])
        .replace(path_mask, "")
        .replace("\\", "/")
        + "/"
    )


class RosettaCSVGenerator:
    """Rosetta CSV Generator Class."""

    # flags for singleIE config
    ieOutput = False
    representationOutput = False
    sectionstatusupdate = False
    lenIE = 0
    lenREP = 0

    # zip name we removed
    zipname = ""

    # Main init options...
    config = None
    singleIE = None
    droidcsv = None
    rosettaschema = None
    rosettasections = None
    includezips = None

    def __init__(self, droidcsv=False, rosettaschema=False, configfile=False):
        """Rosetta CSV Constructor."""

        self.droidlist = None

        self.config = ConfigParser.RawConfigParser()
        self.config.read(configfile)

        if self.config.has_option("application configuration", "includezips"):
            self.includezips = self._handle_text_boolean(
                self.config.get("application configuration", "includezips")
            )

        if self.config.has_option("application configuration", "singleIE"):
            self.singleIE = self._handle_text_boolean(
                self.config.get("application configuration", "singleIE")
            )

        self.droidcsv = droidcsv

        # NOTE: A bit of a hack, compare with import schema work and refactor
        self.rosettaschema = rosettaschema
        self.readRosettaSchema()

        # Grab Rosetta Sections
        rs = RosettaCSVSections(configfile)
        self.rosettasections = rs.sections

    def _handle_text_boolean(self, boolvalue):
        """Determine if a textual boolean is `True` or `False`."""
        if boolvalue.lower() == "true":
            return True
        return False

    def add_csv_value(self, value):
        """Provide a save way to add a CSV value to the document."""
        field = f'"{value}"'
        return field

    def readRosettaSchema(self):
        """Read a Rosetta Table Schema document."""
        importschema = None
        with open(self.rosettaschema, "r", encoding="utf-8") as rosetta_schema:
            importschemajson = rosetta_schema.read()
        importschema = json_table_schema.JSONTableSchema(importschemajson)

        importschemadict = importschema.as_dict()
        importschemaheader = importschema.as_csv_header()

        self.rosettacsvheader = importschemaheader + "\n"
        self.rosettacsvdict = importschemadict["fields"]

    def createcolumns(self, columno):
        """Create a new empty CSV column."""
        columns = ""
        for _ in range(columno):
            columns = f'{columns}"",'
        return columns

    def csvstringoutput(self, csvlist):
        """Output a CSV as a string."""

        # String output...
        csvrows = self.rosettacsvheader

        SIPROW = ['"",'] * len(self.rosettacsvdict)
        SIPROW[0] = '"SIP",'

        # SIP Title...
        SIPROW[1] = '"CSV Load",'
        if self.config.has_option("rosetta mapping", "SIP Title"):
            SIPROW[1] = f'"{self.config.get("rosetta mapping", "SIP Title")}",'

        csvrows = f'{csvrows}{"".join(SIPROW).rstrip(",")}\n'

        for sectionrows in csvlist:
            rowdata = ""
            for sectionrow in sectionrows:
                for fielddata in sectionrow:
                    rowdata = f"{rowdata}{fielddata},"
                rowdata = f'{rowdata.rstrip(",")}\n'
            csvrows = f"{csvrows}{rowdata}"

        # this is the best i can think of because ExLibris have named two fields with the same
        # title in CSV which doesn't help us when we're trying to use unique names for populating rows
        # replaces SIP Title with Title (DC)
        csvrows = csvrows.replace(
            '"Object Type","SIP Title"', '"Object Type","Title (DC)"'
        )

        # finally return the CSV.
        return csvrows

    def _update_section_status(self, section):
        """Update CSV sections.

        NB. we should do this as few times as possible but it is being
        called too often currently.
        """
        sect = self._get_section_key(section)

        if self.singleIE is True and sect == "IE":
            self.ieOutput = True
            self.lenIE = len(list(section.values())[0])
        if self.singleIE is True and sect == "REPRESENTATION":
            self.representationOutput = True
            self.lenREP = len(list(section.values())[0])

        # One method of only visiting this function only as many times as required...
        return self.ieOutput is True and self.representationOutput is True

    def _get_section_key(self, section):
        """Return the key for a section."""
        return list(section)[0]

    def createrosettacsv(self):
        """Create the Rosetta CSV document."""
        CSVINDEXSTARTPOS = 2
        csvindex = CSVINDEXSTARTPOS

        fields = []

        for item in self.droidlist:
            itemrow = []

            for sections in self.rosettasections:
                if not (
                    self.sectionstatusupdate is True
                    and (
                        self._get_section_key(sections) == "REPRESENTATION"
                        or self._get_section_key(sections) == "IE"
                    )
                ):
                    sectionrow = ['""'] * len(self.rosettacsvdict)

                    section_value = list(sections)[0]

                    sectionrow[0] = self.add_csv_value(section_value)

                    # ROW OUTPUT LOOP STARTS
                    for field in sections[section_value]:
                        if field == self.rosettacsvdict[csvindex]["name"]:
                            if self.config.has_option("rosetta mapping", field):
                                if field in ("Title", "Title(DC)"):
                                    if (
                                        self.includezips is True
                                        and self.singleIE is True
                                    ):
                                        if self.config.has_option(
                                            "application configuration", "ziptitle"
                                        ):
                                            addvalue = self.config.get(
                                                "application configuration", "ziptitle"
                                            )
                                        else:
                                            addvalue = self.zipname
                                    elif self.singleIE is True:
                                        addvalue = self.config.get(
                                            "rosetta mapping", field
                                        )
                                    else:
                                        rosettafield = self.config.get(
                                            "rosetta mapping", field
                                        )
                                        addvalue = item[rosettafield]
                                else:
                                    rosettafield = self.config.get(
                                        "rosetta mapping", field
                                    )
                                    addvalue = item[rosettafield]

                                sectionrow[csvindex] = self.add_csv_value(addvalue)

                            elif self.config.has_option("static values", field):
                                rosettafield = self.config.get("static values", field)
                                sectionrow[csvindex] = self.add_csv_value(rosettafield)

                            elif self.config.has_option("droid mapping", field):
                                rosettafield = self.config.get("droid mapping", field)
                                pathmask = ""
                                if self.config.has_option("path values", "pathmask"):
                                    pathmask = self.config.get(
                                        "path values", "pathmask"
                                    )

                                    addvalue = item[rosettafield]

                                    if field in ("File Location", "File Original Path"):
                                        if not self.includezips:
                                            addvalue = ingest_path_from_droid_row(
                                                droid_row=item,
                                                path_mask=pathmask,
                                            )

                                        else:
                                            addvalue = zip_ingest_path_from_droid_row(
                                                droid_row=item,
                                                path_mask=pathmask,
                                            )
                                sectionrow[csvindex] = self.add_csv_value(addvalue)
                            else:
                                # If we haven't a value, add a blank field...
                                sectionrow[csvindex] = self.add_csv_value("")

                            csvindex += 1

                    itemrow.append(sectionrow)
                    # ROW OUTPUT LOOP ENDS

                # Need to know to output sections if we have a single IE
                if not self.sectionstatusupdate and self.singleIE:
                    self.sectionstatusupdate = self._update_section_status(sections)

            # add row to sheet
            fields.append(itemrow)

            # reset field entry point, default two represents Object Type and SIP Title (see schema)
            csvindex = CSVINDEXSTARTPOS
            if self.singleIE:
                number_of_empty_fields = CSVINDEXSTARTPOS + self.lenIE + self.lenREP
                # len IE + Len REP?
                csvindex = number_of_empty_fields

        return self.csvstringoutput(fields)

    def read_droid_csv(self):
        """Read the DROID CSV."""
        if self.droidcsv is not False:
            droidcsvhandler = DroidCSVHandler()
            droidlist = droidcsvhandler.read_droid_csv(self.droidcsv)
            droidlist = droidcsvhandler.remove_folders(droidlist)
            if not self.includezips:
                droidlist = droidcsvhandler.remove_container_contents(droidlist)
            if self.includezips:
                newlist = []
                for d in droidlist:
                    if droidcsvhandler.get_uri_scheme(d["URI"]) != "file":
                        newlist.append(d)
                    else:
                        self.zipname = d["NAME"]
                droidlist = newlist
            if len(droidlist) == 0:
                logging.error(
                    "listing empty. Check ingest from ZIP settings, or contents of DROID report."
                )
                sys.exit(1)
            return droidlist
        return ""

    def export_to_rosetta_csv(self):
        """Export the CSV."""
        if not self.droidcsv:
            return ""
        self.droidlist = self.read_droid_csv()
        return self.createrosettacsv()
