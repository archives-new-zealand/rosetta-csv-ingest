"""DROID CSV Handling class."""

# pylint: disable=R0903

import csv
import os.path
from urllib.parse import urlparse


class GenericCSVHandler:
    """Generic CSV handling class."""

    def __get_csv_headers(self, csvcolumnheaders):
        header_list = []
        for header in csvcolumnheaders:
            header_list.append(header)
        return header_list

    def csv_as_list(self, csvfname):
        """Enable the return of a CSV as a list.

        returns list of rows, each row is a dictionary: header: value, pair
        """
        columncount = 0
        csvlist = None
        if os.path.isfile(csvfname):
            csvlist = []
            with open(csvfname, "r", encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
                for row in csv_reader:
                    if csv_reader.line_num == 1:  # not zero-based index
                        header_list = self.__get_csv_headers(row)
                        columncount = len(header_list)
                    else:
                        csv_dict = {}
                        # for each column in header
                        # note: don't need ID data. Ignoring multiple ID.
                        for i in range(columncount):
                            csv_dict[header_list[i]] = row[i]
                        csvlist.append(csv_dict)
        return csvlist


class DroidCSVHandler:
    """DROID specific CSV handler."""

    def __init__(self):
        """Function Init."""
        self.csv = None

    def read_droid_csv(self, droidcsvfname):
        """Read a DROID CSV into self."""
        csvhandler = GenericCSVHandler()
        self.csv = csvhandler.csv_as_list(droidcsvfname)
        return self.csv

    def remove_container_contents(self, droidlist):
        """Remove container contents if they serve no purpose in an
        analysis or other output.
        """
        newlist = []  # naive remove causes loop to skip items
        for row in droidlist:
            self.get_uri_scheme(row["URI"])
            if self.get_uri_scheme(row["URI"]) == "file":
                newlist.append(row)
        return newlist

    def remove_folders(self, droidlist):
        """Remove folders if they serve no purpose in an analysis or
        other output.
        """
        newlist = []  # naive remove causes loop to skip items
        for _, row in enumerate(droidlist):
            if row["TYPE"] != "Folder":
                newlist.append(row)
        return newlist

    def retrieve_folder_list(self, droidlist):
        """Return a list of folder paths in a DROID report."""
        newlist = []
        for row in droidlist:
            if row["TYPE"] == "Folder":
                newlist.append(row["FILE_PATH"])
        return newlist

    def retrieve_folder_names(self, droidlist):
        """Return a list of folder names in a DROID report."""
        newlist = []
        for row in droidlist:
            if row["TYPE"] == "Folder":
                newlist.append(row["NAME"])
        return newlist

    def get_uri_scheme(self, url):
        """Get the URL scheme for a URI in a DROID report."""
        return urlparse(url).scheme
