"""Rosetta CSV generation tests.

Largely integration tests for the utility. Others as required.

Example primary runner from the CLI:

```bash
   python ingest-generator.py \\
      --csv sheets/droid.csv \\
      --ros sheets/validation.json \\
      --cfg sheets/config.cfg
```

"""

# pylint: disable=C0103

from typing import Final

from src.rosetta_csv.rosetta_csv_generator import RosettaCSVGenerator

schema: Final[
    str
] = """
{
    "title": "Rosetta CSV Validation Schem",
    "description": "Draft schema for validating CSV files for ingest in Rosetta",
	"validator": "http://csvlint.io/",
	"standard" : "http://dataprotocols.org/json-table-schema/",
    "fields": [
        {
            "name": "Object Type",
            "description": "The type of object we're describing in the row.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": true,
                "pattern": "^(SIP|IE|REPRESENTATION|FILE)$"
            }
        },
        {
            "name": "SIP Title",
            "description": "Title of the SIP to ingest.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "Title(DC)",
            "description": "Title of the digital object being uploaded.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "Revision Number",
            "description": "Version of the file to be uploaded.",
            "type": "http://www.w3.org/2001/XMLSchema#int",
            "constraints": {
                "required": false,
                "pattern": "(^\\\\d{1,2}$|^$)"
            }
        },
        {
            "name": "Usage Type",
            "description": "What we can do with file instance in Rosetta, e.g. VIEW.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "(^(VIEW)$|^$)"
            }
        },
        {
            "name": "Preservation Type",
            "description": "Preservation purpose of file instance in Rosetta, e.g. Preservation Master.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "(^(PRESERVATION_MASTER)$|^$)"
            }
        },
        {
            "name": "File Original Path",
            "description": "Directory path to location of file to be uploaded. Path begins at root of ZIP and does not begin with an opening slash. Does not contain filename",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "File Original Name",
            "description": "File name, including extension, of file to be uploaded.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false
            }
        },
        {
            "name": "MD5",
            "description": "Hash generated for the file to be uploaded.",
            "type": "http://www.w3.org/2001/XMLSchema#string",
            "constraints": {
                "required": false,
                "pattern": "♙♘♗♖♕♔♚♛♜♝♞♟ā, ē, ī, ō, ū, Ā, Ē, Ī, Ō Ū ♭ ♮ ♯"
            }
        }
    ]
}
"""

config: Final[
    str
] = """
[application configuration]
includezips = False
singleIE = {REPLACE THIS VALUE IN TESTS}

[rosetta mapping]

#rosetta field on the left
#export field on the right

SIP title = Getty CSV Ingest
Title(DC)=NAME

MD5=MD5_HASH

[static values]

Revision Number=1
Preservation Type=PRESERVATION_MASTER

Usage Type=VIEW

[droid mapping]

File Original Name=NAME
File Original Path=FILE_PATH

[path values]

pathmask=Z:\\distilled\\Mahara Okeroa - E1\\

[rosetta csv fields]

CSVSECTIONS=IE,REPRESENTATION,FILE

IE = Title(DC)
REPRESENTATION = Revision Number,Usage Type,Preservation Type
FILE = File Original Path,File Original Name,MD5
"""

droid_csv: Final[
    str
] = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"1","","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/","Z:\\distilled\\Mahara Okeroa - E1\\E1","E1",,"Done","","Folder",,"2014-11-03T14:34:22","false",,"",,"","",""
"2","1","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements","Press statements",,"Done","","Folder",,"2014-08-26T14:49:01","false",,"",,"","",""
"3","2","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage","Arts, Culture and Hertiage",,"Done","","Folder",,"2009-01-15T15:02:39","false",,"",,"","",""
"4","3","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs","advertsing blurbs",,"Done","","Folder",,"2011-04-05T13:05:18","false",,"",,"","",""
"5","4","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/Backup%20of%20Matariki.wbk","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs\\Backup of Matariki.wbk","Backup of Matariki.wbk","Container","Done","20992","File","wbk","2006-06-06T11:39:50","false","bbba63d962f53165177296d6cd570afd","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"6","4","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/Backup%20of%20OKEROA%20Hon%20Mahara%20Gover%20directory%20.wbk","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs\\Backup of OKEROA Hon Mahara Gover directory .wbk","Backup of OKEROA Hon Mahara Gover directory .wbk","Container","Done","826880","File","wbk","2006-10-09T14:20:14","false","6a1b841cc2ac30bd9f144208786ae297","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"7","4","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/Backup%20of%20Race%20relations%20day.wbk","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs\\Backup of Race relations day.wbk","Backup of Race relations day.wbk","Container","Done","20992","File","wbk","2006-03-10T13:31:49","false","85f3f1bcf29bc324782611a157fb8b47","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"8","4","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/Mahara%20Okeroa.doc","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs\\Mahara Okeroa.doc","Mahara Okeroa.doc","Container","Done","20992","File","doc","2006-01-27T09:31:39","false","0a62be84225ed47e353dd0a54b888e3b","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"9","4","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/Matariki.doc","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs\\Matariki.doc","Matariki.doc","Container","Done","20480","File","doc","2006-06-06T11:50:14","false","f865f031768e0449faf02842a53e7bed","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"10","4","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/OKEROA%20Hon%20Mahara%20Gover%20directory%20.doc","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs\\OKEROA Hon Mahara Gover directory .doc","OKEROA Hon Mahara Gover directory .doc","Container","Done","827392","File","doc","2006-10-09T15:15:53","false","cc1276e7b2ef8e74dd156ec56ba6d395","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"11","4","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/Race%20relations%20day.doc","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs\\Race relations day.doc","Race relations day.doc","Container","Done","20992","File","doc","2006-03-10T13:41:13","false","cf586acbd05b77a8b59e8712ff423a78","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"12","4","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/Te%20reo%20week.doc","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs\\Te reo week.doc","Te reo week.doc","Container","Done","21504","File","doc","2006-07-14T15:57:24","false","459efd825c127569fca8ec04f7f9ab9e","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"13","4","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/Trevs%20tribune.doc","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs\\Trevs tribune.doc","Trevs tribune.doc","Container","Done","20992","File","doc","2006-05-04T11:12:54","false","b0d0e663cd908f9c00df995af694e217","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"14","3","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/06-01-23%20Mauriexhibt.doc","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\06-01-23 Mauriexhibt.doc","06-01-23 Mauriexhibt.doc","Container","Done","30720","File","doc","2007-02-23T13:37:02","false","66d9ec86cbffc47b7d12e6a7962d0aaa","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"15","3","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/080415%20-%20Ministers%20acknowledge%20the%20life%20and%20work%20of%20Mahinarangi%20Tocker.doc","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\080415 - Ministers acknowledge the life and work of Mahinarangi Tocker.doc","080415 - Ministers acknowledge the life and work of Mahinarangi Tocker.doc","Container","Done","42496","File","doc","2008-04-15T16:54:12","false","076a8e23e7963e54a240e11f7ac46b96","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"16","3","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/Backup%20of%2006-01-23%20Mauriexhibt.wbk","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\Backup of 06-01-23 Mauriexhibt.wbk","Backup of 06-01-23 Mauriexhibt.wbk","Container","Done","31232","File","wbk","2007-01-23T15:59:06","false","54cb6992f830f68a5ca8ad607d78ca22","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"17","3","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/Backup%20of%20Japan%20Press%20statement%20.wbk","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\Backup of Japan Press statement .wbk","Backup of Japan Press statement .wbk","Container","Done","31744","File","wbk","2007-01-23T11:46:45","false","bc95b5990d358f07ae6a47ba5e732733","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"18","3","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/Backup%20of%20Maori%20heads%20to%20return%20.wbk","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\Backup of Maori heads to return .wbk","Backup of Maori heads to return .wbk","Container","Done","28160","File","wbk","2007-03-23T12:11:10","false","bcbf18f8073f8dcb072edc74e7f3d297","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"19","3","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/Backup%20of%20MaoriHeritageCouncilAppmts.wbk","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\Backup of MaoriHeritageCouncilAppmts.wbk","Backup of MaoriHeritageCouncilAppmts.wbk","Container","Done","36352","File","wbk","2006-07-28T10:49:28","false","0f9535a8373650d4d1777e18b3059fac","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"20","3","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/Backup%20of%20Mauri%20Ora%20reveals%20Maori%20taonga%20to%20the%20international%20stage.wbk","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\Backup of Mauri Ora reveals Maori taonga to the international stage.wbk","Backup of Mauri Ora reveals Maori taonga to the international stage.wbk","Container","Done","22528","File","wbk","2007-02-13T09:51:59","false","2554c32ffd7d61ec0e6a747fad5047b6","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"""

result_one: Final[
    str
] = """
"Object Type","Title (DC)","Title(DC)","Revision Number","Usage Type","Preservation Type","File Original Path","File Original Name","MD5"
"SIP","Getty CSV Ingest","","","","","","",""
"IE","","Backup of Matariki.wbk","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Backup of Matariki.wbk","bbba63d962f53165177296d6cd570afd"
"IE","","Backup of OKEROA Hon Mahara Gover directory .wbk","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Backup of OKEROA Hon Mahara Gover directory .wbk","6a1b841cc2ac30bd9f144208786ae297"
"IE","","Backup of Race relations day.wbk","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Backup of Race relations day.wbk","85f3f1bcf29bc324782611a157fb8b47"
"IE","","Mahara Okeroa.doc","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Mahara Okeroa.doc","0a62be84225ed47e353dd0a54b888e3b"
"IE","","Matariki.doc","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Matariki.doc","f865f031768e0449faf02842a53e7bed"
"IE","","OKEROA Hon Mahara Gover directory .doc","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","OKEROA Hon Mahara Gover directory .doc","cc1276e7b2ef8e74dd156ec56ba6d395"
"IE","","Race relations day.doc","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Race relations day.doc","cf586acbd05b77a8b59e8712ff423a78"
"IE","","Te reo week.doc","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Te reo week.doc","459efd825c127569fca8ec04f7f9ab9e"
"IE","","Trevs tribune.doc","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Trevs tribune.doc","b0d0e663cd908f9c00df995af694e217"
"IE","","06-01-23 Mauriexhibt.doc","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","06-01-23 Mauriexhibt.doc","66d9ec86cbffc47b7d12e6a7962d0aaa"
"IE","","080415 - Ministers acknowledge the life and work of Mahinarangi Tocker.doc","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","080415 - Ministers acknowledge the life and work of Mahinarangi Tocker.doc","076a8e23e7963e54a240e11f7ac46b96"
"IE","","Backup of 06-01-23 Mauriexhibt.wbk","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","Backup of 06-01-23 Mauriexhibt.wbk","54cb6992f830f68a5ca8ad607d78ca22"
"IE","","Backup of Japan Press statement .wbk","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","Backup of Japan Press statement .wbk","bc95b5990d358f07ae6a47ba5e732733"
"IE","","Backup of Maori heads to return .wbk","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","Backup of Maori heads to return .wbk","bcbf18f8073f8dcb072edc74e7f3d297"
"IE","","Backup of MaoriHeritageCouncilAppmts.wbk","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","Backup of MaoriHeritageCouncilAppmts.wbk","0f9535a8373650d4d1777e18b3059fac"
"IE","","Backup of Mauri Ora reveals Maori taonga to the international stage.wbk","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","Backup of Mauri Ora reveals Maori taonga to the international stage.wbk","2554c32ffd7d61ec0e6a747fad5047b6"
"""

result_two: Final[
    str
] = """
"Object Type","Title (DC)","Title(DC)","Revision Number","Usage Type","Preservation Type","File Original Path","File Original Name","MD5"
"SIP","Getty CSV Ingest","","","","","","",""
"IE","","NAME","","","","","",""
"REPRESENTATION","","","1","VIEW","PRESERVATION_MASTER","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Backup of Matariki.wbk","bbba63d962f53165177296d6cd570afd"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Backup of OKEROA Hon Mahara Gover directory .wbk","6a1b841cc2ac30bd9f144208786ae297"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Backup of Race relations day.wbk","85f3f1bcf29bc324782611a157fb8b47"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Mahara Okeroa.doc","0a62be84225ed47e353dd0a54b888e3b"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Matariki.doc","f865f031768e0449faf02842a53e7bed"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","OKEROA Hon Mahara Gover directory .doc","cc1276e7b2ef8e74dd156ec56ba6d395"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Race relations day.doc","cf586acbd05b77a8b59e8712ff423a78"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Te reo week.doc","459efd825c127569fca8ec04f7f9ab9e"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Trevs tribune.doc","b0d0e663cd908f9c00df995af694e217"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","06-01-23 Mauriexhibt.doc","66d9ec86cbffc47b7d12e6a7962d0aaa"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","080415 - Ministers acknowledge the life and work of Mahinarangi Tocker.doc","076a8e23e7963e54a240e11f7ac46b96"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","Backup of 06-01-23 Mauriexhibt.wbk","54cb6992f830f68a5ca8ad607d78ca22"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","Backup of Japan Press statement .wbk","bc95b5990d358f07ae6a47ba5e732733"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","Backup of Maori heads to return .wbk","bcbf18f8073f8dcb072edc74e7f3d297"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","Backup of MaoriHeritageCouncilAppmts.wbk","0f9535a8373650d4d1777e18b3059fac"
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/","Backup of Mauri Ora reveals Maori taonga to the international stage.wbk","2554c32ffd7d61ec0e6a747fad5047b6"
"""


def test_integration_multiple_ie(tmp_path):
    """Integration test for multiple IE."""

    tmp_dir = tmp_path / "multiple_ie"
    tmp_dir.mkdir()
    config_file = tmp_dir / "config.cfg"
    schema_file = tmp_dir / "schema.json"
    droid_report = tmp_dir / "droid.csv"

    config_file.write_text(
        config.replace("singleIE = {REPLACE THIS VALUE IN TESTS}", "singleIE = False")
        .strip()
        .lstrip()
    )
    schema_file.write_text(schema.strip().lstrip(), encoding="utf-8")
    droid_report.write_text(droid_csv.strip().lstrip(), encoding="utf-8")

    csv_generator = RosettaCSVGenerator(
        droidcsv=droid_report, rosettaschema=schema_file, configfile=config_file
    )
    csv_result = csv_generator.export_to_rosetta_csv()
    assert csv_result == result_one.lstrip()


def test_integration_one_ie(tmp_path):
    """Integration test for one IE."""

    tmp_dir = tmp_path / "single_ie"
    tmp_dir.mkdir()
    config_file = tmp_dir / "config.cfg"
    schema_file = tmp_dir / "schema.json"
    droid_report = tmp_dir / "droid.csv"

    config_file.write_text(
        config.replace("singleIE = {REPLACE THIS VALUE IN TESTS}", "singleIE = True")
        .strip()
        .lstrip()
    )
    schema_file.write_text(schema.strip().lstrip(), encoding="utf-8")
    droid_report.write_text(droid_csv.strip().lstrip(), encoding="utf-8")

    csv_generator2 = RosettaCSVGenerator(
        droidcsv=droid_report, rosettaschema=schema_file, configfile=config_file
    )
    csv_result = csv_generator2.export_to_rosetta_csv()
    assert csv_result == result_two.lstrip()


config_one: Final[
    str
] = """
[application configuration]
includezips = False
singleIE = {REPLACE THIS VALUE IN TESTS}

[rosetta mapping]

#rosetta field on the left
#export field on the right

SIP title = Getty CSV Ingest
Title(DC)=NAME

MD5=MD5_HASH

[static values]

Revision Number=1
Preservation Type=♙♘♗♖♕♔♚♛♜♝♞♟ā, ē, ī, ō, ū, Ā, Ē, Ī, Ō Ū ♭ ♮ ♯

Usage Type=VIEW

[droid mapping]

File Original Name=NAME
File Original Path=FILE_PATH

[path values]

pathmask=Z:\\distilled\\Mahara Okeroa - E1\\

[rosetta csv fields]

CSVSECTIONS=IE,REPRESENTATION,FILE

IE = Title(DC)
REPRESENTATION = Revision Number,Usage Type,Preservation Type
FILE = File Original Path,File Original Name,MD5
"""


droid_csv_one: Final[
    str
] = """
"ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"
"1","","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/","Z:\\distilled\\Mahara Okeroa - E1\\E1","E1",,"Done","","Folder",,"2014-11-03T14:34:22","false",,"",,"","",""
"2","1","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements","Press statements",,"Done","","Folder",,"2014-08-26T14:49:01","false",,"",,"","",""
"3","2","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage","Arts, Culture and Hertiage",,"Done","","Folder",,"2009-01-15T15:02:39","false",,"",,"","",""
"4","3","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs","advertsing blurbs",,"Done","","Folder",,"2011-04-05T13:05:18","false",,"",,"","",""
"5","4","file:/Z:/distilled/Mahara%20Okeroa%20-%20E1/E1/Press%20statements/Arts,%20Culture%20and%20Hertiage/advertsing%20blurbs/Backup%20of%20Matariki.wbk","Z:\\distilled\\Mahara Okeroa - E1\\E1\\Press statements\\Arts, Culture and Hertiage\\advertsing blurbs\\Backup of Matariki.wbk","Backup of Matariki.wbk","Container","Done","20992","File","wbk","2006-06-06T11:39:50","false","bbba63d962f53165177296d6cd570afd","1","fmt/40","application/msword","Microsoft Word Document","97-2003"
"""

res_one: Final[
    str
] = """
"Object Type","Title (DC)","Title(DC)","Revision Number","Usage Type","Preservation Type","File Original Path","File Original Name","MD5"
"SIP","Getty CSV Ingest","","","","","","",""
"IE","","NAME","","","","","",""
"REPRESENTATION","","","1","VIEW","♙♘♗♖♕♔♚♛♜♝♞♟ā, ē, ī, ō, ū, Ā, Ē, Ī, Ō Ū ♭ ♮ ♯","","",""
"FILE","","","","","","E1/Press statements/Arts, Culture and Hertiage/advertsing blurbs/","Backup of Matariki.wbk","bbba63d962f53165177296d6cd570afd"
"""


def test_unicode_one(tmp_path):
    """Integration test for one IE."""

    tmp_dir = tmp_path / "one_file"
    tmp_dir.mkdir()
    config_file = tmp_dir / "config.cfg"
    schema_file = tmp_dir / "schema.json"
    droid_report = tmp_dir / "droid.csv"

    config_file.write_text(
        config_one.replace(
            "singleIE = {REPLACE THIS VALUE IN TESTS}", "singleIE = True"
        )
        .strip()
        .lstrip()
    )
    schema_file.write_text(schema.strip().lstrip(), encoding="utf-8")
    droid_report.write_text(droid_csv_one.strip().lstrip(), encoding="utf-8")

    csv_generator2 = RosettaCSVGenerator(
        droidcsv=droid_report, rosettaschema=schema_file, configfile=config_file
    )
    csv_result = csv_generator2.export_to_rosetta_csv()
    print(csv_result)
    assert csv_result.strip() == res_one.strip()
