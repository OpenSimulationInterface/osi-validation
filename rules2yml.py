import sys
import argparse
import re
from glob import *
import os
from ruamel.yaml import YAML


def command_line_arguments():
    """Define and handle command line interface"""

    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    parser = argparse.ArgumentParser(
        description="Export the rules of *.proto files into the *.yml format so it can be used by the validator.",
        prog="python3 rules2yml.py",
    )
    parser.add_argument(
        "--dir",
        "-d",
        help="Name of the directory where the yml rules will be stored.",
        default="rules",
        required=False,
        type=str,
    )
    parser.add_argument(
        "--full-osi",
        "-f",
        help="Add is_set rule to all fields that do not contain it already.",
        action="store_true",
        required=False,
    )

    return parser.parse_args()


def gen_yml_rules(dir_name="rules", full_osi=False):
    with open(r"open-simulation-interface/rules.yml") as file:
        yaml = YAML(typ="safe")
        rules_dict = yaml.load(file)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if not os.path.exists(dir_name + "/schema"):
        os.makedirs(dir_name + "/schema")

    for file in glob("open-simulation-interface/*.proto"):
        filename = file.split("open-simulation-interface/")[1].split(".proto")[0]

        if os.path.exists(f"{dir_name}/{filename}.yml"):
            continue

        with open(f"{dir_name}/schema/{filename}_schema.yml", "a") as schema_file:
            with open(file, "rt") as fin:
                isEnum = False
                numMessage = 0
                saveStatement = ""
                prevMainField = False  # boolean, that the previous field has children

                for line in fin:
                    if file.find(".proto") != -1:
                        # Search for comment ("//").
                        matchComment = re.search("//", line)
                        if matchComment is not None:
                            statement = line[: matchComment.start()]
                        else:
                            statement = line

                        # Add part of the statement from last line.
                        statement = saveStatement + " " + statement

                        # New line is not necessary. Remove for a better output.
                        statement = statement.replace("\n", "")

                        # Is statement complete
                        matchSep = re.search(r"[{};]", statement)
                        if matchSep is None:
                            saveStatement = statement
                            statement = ""
                        else:
                            saveStatement = statement[matchSep.end() :]
                            statement = statement[: matchSep.end()]

                        # Search for "enum".
                        matchEnum = re.search(r"\benum\b", statement)
                        if matchEnum is not None:
                            isEnum = True

                        # Search for a closing brace.
                        matchClosingBrace = re.search("}", statement)
                        if isEnum is True and matchClosingBrace is not None:
                            isEnum = False
                            continue

                        # Check if not inside an enum.
                        if isEnum is False:
                            # Search for "message".
                            matchMessage = re.search(r"\bmessage\b", statement)
                            if matchMessage is not None:
                                # a new message or a new nested message
                                numMessage += 1
                                endOfLine = statement[matchMessage.end() :]
                                matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                                if matchName is not None and prevMainField is False:
                                    # Check previous main field to exclude empty fields from sensor specific file
                                    matchNameConv = re.search(
                                        r"\b[A-Z][a-zA-Z0-9]*\b",
                                        endOfLine[matchName.start() : matchName.end()],
                                    )
                                    schema_file.write(
                                        2 * (numMessage - 1) * " "
                                        + f"{matchNameConv.group(0)}:\n"
                                    )
                                    prevMainField = True

                            elif re.search(r"\bextend\b", statement) is not None:
                                # treat extend as message
                                numMessage += 1

                            # Search for a closing brace.
                            matchClosingBrace = re.search("}", statement)
                            if numMessage > 0 and matchClosingBrace is not None:
                                numMessage -= 1

                            if matchComment is None and len(saveStatement) == 0:
                                if numMessage > 0 or isEnum == True:
                                    if statement.find(";") != -1:
                                        field = statement.strip().split()[2]
                                        schema_file.write(
                                            (2 * numMessage) * " "
                                            + f"{field}: any(list(include('rules', required=False)), null(), required=False)\n"
                                        )
                                        prevMainField = False
                schema_file.write(
                    "---\n"
                    "rules:\n"
                    "  is_greater_than: num(required=False)\n"
                    "  is_greater_than_or_equal_to: num(required=False)\n"
                    "  is_less_than_or_equal_to: num(required=False)\n"
                    "  is_less_than: num(required=False)\n"
                    "  is_equal_to: any(num(), bool(), required=False)\n"
                    "  is_different_to: num(required=False)\n"
                    "  is_globally_unique: str(required=False)\n"
                    "  refers_to: str(required=False)\n"
                    "  is_iso_country_code: str(required=False)\n"
                    "  is_set: str(required=False)\n"
                    "  check_if: list(include('rules', required=False),required=False)\n"
                    "  do_check: any(required=False)\n"
                    "  target: any(required=False)\n"
                    "  first_element: any(required=False)\n"
                    "  last_element: any(required=False)"
                )

    for file in glob("open-simulation-interface/*.proto*"):
        filename = file.split("open-simulation-interface/")[1].split(".proto")[0]

        if os.path.exists(f"{dir_name}/{filename}.yml"):
            continue

        with open(f"{dir_name}/{filename}.yml", "a") as yml_file:
            with open(file, "rt") as fin:
                isEnum = False
                numMessage = 0
                shiftCounter = False
                saveStatement = ""
                prevMainField = False  # boolean, that the previous field has children
                rules = []

                for line in fin:
                    if file.find(".proto") != -1:
                        # Search for comment ("//").
                        matchComment = re.search("//", line)
                        if matchComment is not None:
                            statement = line[: matchComment.start()]
                            comment = line[matchComment.end() :]
                        else:
                            statement = line
                            comment = ""

                        # Add part of the statement from last line.
                        statement = saveStatement + " " + statement
                        saveStatement = ""

                        # New line is not necessary. Remove for a better output.
                        statement = statement.replace("\n", "")
                        comment = comment.replace("\n", "")

                        # Is statement complete
                        matchSep = re.search(r"[{};]", statement)
                        if matchSep is None:
                            saveStatement = statement
                            statement = ""
                        else:
                            saveStatement = statement[matchSep.end() :]
                            statement = statement[: matchSep.end()]

                        if isEnum is True:
                            matchName = re.search(r"\b\w[\S:]+\b", statement)
                            if matchName is not None:
                                checkName = statement[
                                    matchName.start() : matchName.end()
                                ]

                        # Search for "enum".
                        matchEnum = re.search(r"\benum\b", statement)
                        if matchEnum is not None:
                            isEnum = True
                            # print(f"Matched enum {isEnum}")
                            endOfLine = statement[matchEnum.end() :]
                            matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                            if matchName is not None:
                                # Test case 8: Check name - no special char
                                matchNameConv = re.search(
                                    r"\b[A-Z][a-zA-Z0-9]*\b",
                                    endOfLine[matchName.start() : matchName.end()],
                                )

                        # Search for a closing brace.
                        matchClosingBrace = re.search("}", statement)
                        if isEnum is True and matchClosingBrace is not None:
                            isEnum = False
                            continue

                        # Check if not inside an enum.
                        if isEnum is False:
                            # Search for "message".
                            matchMessage = re.search(r"\bmessage\b", statement)
                            if matchMessage is not None:
                                # a new message or a new nested message
                                numMessage += 1
                                endOfLine = statement[matchMessage.end() :]
                                matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                                if matchName is not None and prevMainField is False:
                                    # Test case 10: Check name - no special char -
                                    # start with a capital letter
                                    matchNameConv = re.search(
                                        r"\b[A-Z][a-zA-Z0-9]*\b",
                                        endOfLine[matchName.start() : matchName.end()],
                                    )
                                    # print(matchNameConv.group(0))
                                    yml_file.write(
                                        2 * (numMessage - 1) * " "
                                        + f"{matchNameConv.group(0)}:\n"
                                    )
                                    prevMainField = True

                            elif re.search(r"\bextend\b", statement) is not None:
                                # treat extend as message
                                numMessage += 1

                            else:
                                # Check field names
                                if numMessage > 0:
                                    matchName = re.search(r"\b\w[\S]*\b\s*=", statement)
                                    if matchName is not None:
                                        checkName = statement[
                                            matchName.start() : matchName.end() - 1
                                        ]
                                        # Check field message type (remove field name)
                                        type = statement.replace(checkName, "")
                                        matchName = re.search(r"\b\w[\S\.]*\s*=", type)

                            # Search for a closing brace.
                            matchClosingBrace = re.search("}", statement)
                            if numMessage > 0 and matchClosingBrace is not None:
                                numMessage -= 1

                            if matchComment is not None:
                                if comment != "":
                                    for rulename, ruleregex in rules_dict.items():
                                        if re.search(ruleregex, comment):
                                            rules.append(comment)
                                            shiftCounter = True

                            elif len(saveStatement) == 0:
                                if numMessage > 0 or isEnum == True:
                                    if statement.find(";") != -1:
                                        field = statement.strip().split()[2]
                                        yml_file.write(
                                            (2 * numMessage) * " " + f"{field}:\n"
                                        )
                                        prevMainField = False

                                        # If option --full-osi is enabled:
                                        # Check if is_set is already a rule for the current field, if not, add it.
                                        if full_osi and not any(
                                            "is_set" in rule for rule in rules
                                        ):
                                            yml_file.write(
                                                (2 * numMessage + 2) * " "
                                                + f"- is_set:\n"
                                            )

                                        if shiftCounter:
                                            for rule in rules:
                                                rule_list = rule.split()
                                                # Check if syntax
                                                if "check_if" in rule_list:
                                                    yml_file.write(
                                                        (2 * numMessage + 2) * " "
                                                        + f"- {rule_list[0]}:\n"
                                                    )
                                                    yml_file.write(
                                                        (2 * numMessage + 4) * " "
                                                        + f"- {rule_list[2]}: {rule_list[3]}\n"
                                                    )
                                                    yml_file.write(
                                                        (2 * numMessage + 6) * " "
                                                        + f"target: {rule_list[1]}\n"
                                                    )
                                                    yml_file.write(
                                                        (2 * numMessage + 4) * " "
                                                        + f"{rule_list[5]}:\n"
                                                    )
                                                    yml_file.write(
                                                        (2 * numMessage + 4) * " "
                                                        + f"- {rule_list[6]}:\n"
                                                    )

                                                # First element syntax
                                                elif "first_element" in rule_list:
                                                    yml_file.write(
                                                        (2 * numMessage + 2) * " "
                                                        + f"- {rule_list[0]}:\n"
                                                    )
                                                    yml_file.write(
                                                        (2 * numMessage + 6) * " "
                                                        + f"{rule_list[1]}:\n"
                                                    )
                                                    yml_file.write(
                                                        (2 * numMessage + 8) * " "
                                                        + f"- {rule_list[2]}: {rule_list[3]}\n"
                                                    )

                                                # Last element syntax
                                                elif "last_element" in rule_list:
                                                    yml_file.write(
                                                        (2 * numMessage + 2) * " "
                                                        + f"- {rule_list[0]}:\n"
                                                    )
                                                    yml_file.write(
                                                        (2 * numMessage + 6) * " "
                                                        + f"{rule_list[1]}:\n"
                                                    )
                                                    yml_file.write(
                                                        (2 * numMessage + 8) * " "
                                                        + f"- {rule_list[2]}: {rule_list[3]}\n"
                                                    )

                                                # Standalone rules
                                                elif any(
                                                    list_item
                                                    in [
                                                        "is_globally_unique",
                                                        "is_set",
                                                        "is_iso_country_code",
                                                    ]
                                                    for list_item in rule_list
                                                ):
                                                    yml_file.write(
                                                        (2 * numMessage + 2) * " "
                                                        + f"-{rule}:\n"
                                                    )
                                                # Values or parameters of rules
                                                else:
                                                    yml_file.write(
                                                        (2 * numMessage + 2) * " "
                                                        + f"-{rule}\n"
                                                    )

                                            shiftCounter = False
                                            rules = []


def main():
    # Handling of command line arguments
    args = command_line_arguments()
    gen_yml_rules(args.dir, args.full_osi)


if __name__ == "__main__":
    main()
