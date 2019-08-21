import sys
import unicodedata
import re
from glob import *

state = 0

# Define grammar rules for rule definitions
rules_dict = {'in_range': r'\b(in_range)\b: \[\d+(\.\d+)?, \d+(\.\d+)?\]',
              'is_greater_than': r'\b(is_greater_than)\b: \d+(\.\d+)?',
              'is_greater_than_or_equal_to': r'\b(is_greater_than_or_equal_to)\b: \d+(\.\d+)?',
              'is_less_than_or_equal_to': r'\b(is_less_than_or_equal_to)\b: \d+(\.\d+)?',
              'is_less_than': r'\b(is_less_than)\b: \d+(\.\d+)?',
              'is_equal': r'\b(is_equal)\b: \d+(\.\d+)?',
              'is_different': r'\b(is_different)\b: \d+(\.\d+)?',
              'is_global_unique': r'\b(is_global_unique)\b',
              'refers': r'\b(refers)\b',
              'is_iso_country_code': r'\b(is_iso_country_code)\b',
              'first_element': r'\b(first_element)\b: \{.*: \d+\.\d+\}',
              'last_element': r'\b(last_element)\b: \{.*: \d+\.\d+\}',
              'is_optional': r'\b(is_optional)\b',
              'check_if': r'\b(check_if)\b: \{.*: \{.*: \[.*\]\}\}',
              'is_set': r'\b(is_set)\b'}


for file in glob("open-simulation-interface/*.proto"):
    with open(file, "rt") as fin:
        i = 0
        isEnum = False
        enumName = ""
        noMessage = 0
        noComment = 0
        hasBrief = False
        hasNewLine = True
        htmlblock = False
        saveStatement = ""

        for line in fin:
            i = i + 1
            hasNewLine = line.endswith("\n")

            # --------------------------------------------------------------
            # Test case 1 is checking if there are illegal tabulators in the code
            if line.find("\t") != -1:
                print(file + " in line " + str(i) + ": not permitted tab found")
                state = 1

            # --------------------------------------------------------------
            # Test case 2 is checking if there is an "Umlaut" etc.
            if (sys.version_info >= (3, 0)):
                if line != unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').decode():
                    print(file + " in line " + str(i) + ": a none ASCII char is present")
                    state = 1
            else:
                if line != unicodedata.normalize('NFKD', unicode(line, 'ISO-8859-1')).encode('ASCII', 'ignore'):
                    print(file + " in line " + str(i) + ": a none ASCII char is present")
                    state = 1

            if file.find(".proto") != -1:
                # --------------------------------------------------------------
                # Test case 3 is checking if there are more than the two allowed '/'
                if line.find("///") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '///' ")
                    state = 1

                # --------------------------------------------------------------
                # Test case 4 is checking if there is an other type of comment
                if line.find("/*") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '/*' ")
                    state = 1

                # --------------------------------------------------------------
                # Test case 5 is checking if there is an other type of comment
                if line.find("*/") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '*/' ")
                    state = 1

                # --------------------------------------------------------------
                # Test case 9 is checking if there is '__'
                if line.find("__") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '__' ")
                    state = 1

                # --------------------------------------------------------------
                # Divide statement and comment. Concatenate multi line statements.

                # Search for comment ("//").
                matchComment = re.search("//", line)
                if matchComment is not None:
                    statement = line[:matchComment.start()]
                    comment = line[matchComment.end():]
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
                    saveStatement = statement[matchSep.end():]
                    statement = statement[:matchSep.end()]
                    
                # --------------------------------------------------------------
                # Test case 6-8 camelcase for enums and check enum name?

                # .
                if isEnum is True:
                    matchName = re.search(r"\b\w[\S:]+\b", statement)
                    if matchName is not None:
                        checkName = statement[matchName.start():matchName.end()]
                        # Test case 6: Check correct name
                        if checkName.find(enumName) != 0:
                            print(file + " in line " + str(i) + ": enum type wrong. '"+checkName+"' should start with '"+enumName+"'")
                            state = 1
                        # Test case 7: Check upper case
                        elif checkName != checkName.upper():
                            print(file + " in line " + str(i) + ": enum type wrong. '"+checkName+"' should use upper case")
                            state = 1

                # Search for "enum".
                matchEnum = re.search(r"\benum\b", statement)
                if matchEnum is not None:
                    isEnum = True
                    endOfLine = statement[matchEnum.end():]
                    matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                    if matchName is not None:
                        # Test case 8: Check name - no special char
                        matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b",endOfLine[matchName.start():matchName.end()])
                        if matchNameConv is None:
                            print(file + " in line " + str(i) + ": enum name wrong. '"+endOfLine[matchName.start():matchName.end()]+"'")
                            state = 1
                        enumName = convert(endOfLine[matchName.start():matchName.end()])+"_"

                # Search for a closing brace.
                matchClosingBrace = re.search("}", statement)
                if isEnum is True and matchClosingBrace is not None:
                    isEnum = False
                    enumName = ""

                def convert(name):
                    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
                    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).upper()

                # --------------------------------------------------------------
                # Test case 10-12,18 check message name, field type and field name
                #
                # Check (nested) messages

                if isEnum is False:
                    # Check if not inside an enum.

                    # Search for "message".
                    matchMessage = re.search(r"\bmessage\b", statement)
                    if matchMessage is not None:
                        # a new message or a new nested message
                        noMessage += 1
                        endOfLine = statement[matchMessage.end():]
                        matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                        if matchName is not None:
                            # Test case 10: Check name - no special char -
                            # start with a capital letter
                            matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b",endOfLine[matchName.start():matchName.end()])
                            if matchNameConv is None:
                                print(file + " in line " + str(i) + ": message name wrong. '"+endOfLine[matchName.start():matchName.end()]+"'")
                                state = 1
                    elif re.search(r"\bextend\b", statement) is not None:
                        # treat extend as message
                        noMessage += 1
                    else:
                        # Check field names
                        if noMessage > 0:
                            matchName = re.search(r"\b\w[\S]*\b\s*=", statement)
                            if matchName is not None:
                                checkName = statement[matchName.start():matchName.end()-1]
                                # Test case 11: Check lowercase letters for field names
                                if checkName != checkName.lower():
                                    print(file + " in line " + str(i) + ": field name wrong. '"+checkName+"' should use lower case")
                                    state = 1
                                # Check field message type (remove field name)
                                type = statement.replace(checkName, "")
                                matchName = re.search(r"\b\w[\S\.]*\s*=", type)
                                if matchName is not None:
                                    checkType = " "+type[matchName.start():matchName.end()-1]+" "
                                    # Test case 12: Check nested message type
                                    matchNameConv = re.search(r"[ ][a-zA-Z][a-zA-Z0-9]*([\.][A-Z][a-zA-Z0-9]*)*[ ]",checkType)
                                    if matchNameConv is None:
                                        print(file + " in line " + str(i) + ": field message type wrong. Check: '"+checkType+"'")
                                        state = 1
                                        
                                if re.search(r"\boptional\b",type) is None and re.search(r"\brepeated\b",type) is None:
                                    # Test 18 has every field the multiplicity "repeated" or "optional"
                                    print(file + " in line " + str(i) + ": field multiplicity (\"optional\" or \"repeated\") is missing. Check: '"+statement+"'")
                                    state = 1

                    # Search for a closing brace.
                    matchClosingBrace = re.search("}", statement)
                    if noMessage > 0 and matchClosingBrace is not None:
                        noMessage -= 1

                # --------------------------------------------------------------
                # Test case 13-17 is checking comment
                if matchComment is not None:
                    noComment += 1
                    if comment.find("\\brief") != -1:
                        hasBrief = True
                elif len(saveStatement) == 0:
                    # Test case 13 is checking if comment is min. 2 lines
                    if noComment == 1:
                        print(file + " in line " + str(i-1) + ": short comment - min. 2 lines.")
                        state = 1
                    if re.search(r"\bmessage\b", statement) is not None or re.search(r"\bextend\b", statement) is not None:
                        if hasBrief == False:
                            # Test case 14 each message and extend has a \brief comment
                            print(file + " in line " + str(i-1) + ": \\brief section in comment is missing for: '"+statement+"'")
                            state = 1
                    elif hasBrief == True:
                        # Test case 15 only message and extend has a \brief comment
                        print(file + " in line " + str(i-1) + ": \\brief section in comment is not necessary for: '"+statement+"'")
                        state = 1
                            
                    if re.search(r"\bmessage\b", statement) is not None or re.search(r"\bextend\b", statement) is not None or re.search(r"\benum\b", statement) is not None:
                        if noComment == 0:
                            # Test case 16 every message, extend or enum has a comment
                            print(file + " in line " + str(i) + ": comment is missing for: '"+statement+"'")
                            state = 1

                    if noMessage > 0 or isEnum == True:
                        if statement.find(";") != -1:
                            if noComment == 0:
                                # Test case 17 every statement has a comment
                                print(file + " in line " + str(i) + ": comment is missing for: '"+statement+"'")
                                state = 1

                
                    noComment = 0
                    hasBrief = False

     
                # --------------------------------------------------------------
                # Test case 20 is checking comment and html tags
                if matchComment is not None:
                    htmlComment = ""
                    htmlFreeComment = comment
                    if htmlblock is False:
                        matchHTMLOnly = re.search(r"\\htmlonly", comment)
                        if matchHTMLOnly is not None:

                            htmlComment = comment[matchHTMLOnly.end():]
                            htmlFreeComment = comment[:matchHTMLOnly.start()]
                            htmlblock = True
                    else:
                        htmlComment = comment
                        htmlFreeComment = ""
                        
                    if htmlblock is True:
                        matchEndHTMLOnly = re.search(r"\\endhtmlonly", htmlComment)
                        if matchEndHTMLOnly is not None:
                            htmlFreeComment = htmlFreeComment+htmlComment[matchEndHTMLOnly.end():]
                            htmlComment = htmlComment[:matchEndHTMLOnly.start()]
                            htmlblock = False
                                           
                    #if htmlFreeComment.find("<") != -1:
                        # Test case 20 html tags only in htmlonly sections --> no error
                        #print(file + " in line " + str(i) + ": doxygen comment html tag found (use htmlonly if possible): '"+htmlFreeComment+"'")
                        ##state = 1
                    if htmlComment.find("\\") != -1:
                        # Test case 23 html tags only in htmlonly sections
                        print(file + " in line " + str(i) + ": doxygen comment \\.. reference found: '"+htmlComment+"'")
                        #state = 1
                    if htmlComment.find("#") != -1:
                        # Test case 24 html tags only in htmlonly sections
                        print(file + " in line " + str(i) + ": doxygen comment #.. reference found: '"+htmlComment+"'")
                        #state = 1
                        
                elif htmlblock is True:
                    # Test case 22 html tags only in htmlonly sections without end html only
                    print(file + " in line " + str(i-1) + ": doxygen comment html section without endhtmlonly")
                    htmlblock = False
                    #state = 1
                 

                # --------------------------------------------------------------
                # Test case 21 is checking comment and html tags
                if matchComment is not None:
                    if comment.find("@") != -1:
                        # Test case 21 html tags only in htmlonly sections
                        print(file + " in line " + str(i) + ": @ tag found (please replace with \\): '"+htmlFreeComment+"'")
                        state = 1
                        
                # --------------------------------------------------------------
                # Test case 25 is checking if each field has a rule and must be set
                if isEnum is False:
                    if matchComment is not None:
                        if comment.find("\\endrules") != -1:
                            endRule = True

                        if comment.find("\\rules") != -1:
                            hasRule = True
                            lineruleCount = -1
                            foundruleCount = -1

                        if re.search(r'\b(is_set)\b', comment):
                            isSet = True
                            # foundruleCount += 1

                        # TODO Stehen geblieben
                        
                        if not endRule and comment != '':
                            foundRule = False
                            for rulename, ruleregex in rules_dict.items():
                                if re.search(ruleregex, comment):
                                    foundRule = True
                                    foundruleCount += 1


                    elif len(saveStatement) == 0:
                        if noMessage > 0 or isEnum == True:
                            if statement.find(";") != -1:
                                statement = statement.strip()
                                if not hasRule and not endRule:
                                    # Test case 17 every statement has a comment
                                    print(file + " in line " + str(i) + ": rule is missing for: '"+statement+"'")
                                    state = 1

                                if hasRule and not isSet and endRule:
                                    print(file + " in line " + str(i) + ": rule is_set is missing for: '"+statement+"'")
                                    state = 1

                                if hasRule and lineruleCount != foundruleCount and endRule:
                                    print(file + " in line " + str(i) + ": "+str(lineruleCount-foundruleCount-1)+" defined rule(s) does not exists for: '"+statement+"'")
                                    state = 1

                                if hasRule and lineruleCount > foundruleCount and not endRule:
                                    print(file + " in line " + str(i) + ": endrules statement does not exists for: '"+statement+"'")
                                    state = 1
                    
                        foundRule = False
                        hasRule = False
                        endRule = False
                        isSet = False
                        

                    if hasRule and not endRule:
                        lineruleCount += 1
                # --------------------------------------------------------------
                # Next Test 26
                
                
        # Test case 19 last line must end with a new line.
        if hasNewLine == False:
            print(file + " has no new line at the end of the file.")
            state = 1

sys.exit(state)
