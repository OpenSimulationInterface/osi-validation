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

    return parser.parse_args()


def gen_yml_rules(dir_name="rules"):
    with open(r"open-simulation-interface/rules.yml") as file:
        yaml = YAML(typ="safe")
        rules_dict = yaml.load(file)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

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
                                if matchName is not None:
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
                                                elif "is_globally_unique" in rule_list:
                                                    yml_file.write(
                                                        (2 * numMessage + 2) * " "
                                                        + f"-{rule}:\n"
                                                    )
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
    gen_yml_rules(args.dir)


if __name__ == "__main__":
    main()
