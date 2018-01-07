from enum import Enum


# Class used to generate unique identifiers for Constants
from lexical_analyser.automaton.json_parser import FiniteJsonAutomatonParser


class ConstantSerial:
    id = -1

    @staticmethod
    def get_id():
        ConstantSerial.id += 1
        return ConstantSerial.id


# Class used to generate unique identifiers for Variables
class IdentifierSerial:
    id = -1

    @staticmethod
    def get_id():
        IdentifierSerial.id += 1
        return IdentifierSerial.id


# Types of symbol table
class SymbolTableType(Enum):
    CONSTANT = 0,
    IDENTIFIER = 1,


# Nodes used in the Symbol Table (represented as a binary tree)
class Node:
    def __init__(self, info, serial):  # constructor of class
        self.id = serial
        self.info = info  # information for node
        self.left = None  # left leaf
        self.right = None  # right leaf
        self.level = None  # level none defined

    def __str__(self):
        return str(self.info)  # return as string


class SymbolTable:
    def __init__(self, sttype):  # constructor of class
        self.root = None    # Root node
        self.type = sttype  # Symbol Table type (constant or identifier)

    def insert(self, val):  # create binary search tree nodes
        serial = ConstantSerial.get_id() if self.type == SymbolTableType.CONSTANT else IdentifierSerial.get_id()
        if self.root is None:  # no root, we can just save it
            self.root = Node(val, serial)
        else:
            current = self.root
            while 1:  # find the new node's place in the tree
                if val < current.info:
                    if current.left:
                        current = current.left
                    else:
                        current.left = Node(val, serial)
                        break
                elif val > current.info:
                    if current.right:
                        current = current.right
                    else:
                        current.right = Node(val, serial)
                        break
                else:
                    break
        return serial

    # Returns a list representation of the Symbol Table (in order)
    def as_list(self, node, out):
        if node is not None:
            self.as_list(node.left, out)
            out.append(node)
            self.as_list(node.right, out)

    # Returns a specific element from a given index
    def at_index(self, node, index):
        if node is not None:
            list_repr = []
            self.as_list(node, list_repr)
            for n in list_repr:
                if n.id == index:
                    return n.info
            return -1
        return -1

    # Checks if an element exists in the Symbol Table
    def contains(self, node, value):
        if node is not None:
            list_repr = []
            self.as_list(node, list_repr)
            for n in list_repr:
                if n.info == value:
                    return n.id
            return -1
        return -1

    # In-order traversal
    def inorder(self, node):
        if node is not None:
            self.inorder(node.left)
            print(str(node.info) + " : " + str(node.id))
            self.inorder(node.right)

    # Pre-order traversal
    def preorder(self, node):
        if node is not None:
            print(node.info)
            self.preorder(node.left)
            self.preorder(node.right)

    # Post-order traversal
    def postorder(self, node):
        if node is not None:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.info)


class LexicalAnalyser:
    def __init__(self):
        parser = FiniteJsonAutomatonParser()
        self.constant_automaton = parser.parse("lexical_analyser/json_definitions/constants.json")
        self.identifier_automaton = parser.parse('lexical_analyser/json_definitions/identifiers.json')

        self.tokens = ['identifier', 'constant', 'int', 'double', 'cin', 'cout', 'if', 'for', 'else', '/', '*', '+', '-',
                  '<', '>',
                  '<=', '>=', '=', '==', '!=', '{', '}', ';', '.', '(', ')', '>>', '<<', 'struct', 'main', '<iostream>',
                  'return', '#include', 'using', 'namespace', 'std']
        self.sorted_tokens = sorted(self.tokens, key=lambda x: len(x), reverse=True)
        self.PIF = []
        self.constants = SymbolTable(SymbolTableType.CONSTANT)
        self.identifiers = SymbolTable(SymbolTableType.IDENTIFIER)
        self.tokenized_pif = []

    def is_whitespace(self, char):
        return char == ' ' or char == '\n' or char == '\t' or char == '\r'

    def is_separator(self, char):
        return char in [';', ',', ')', '(', '{', '}']

    def is_operator(self, char):
        return char in ['<', '>', '<=', '>=', '==', '=', '!=', '+', '-', '*', '/', '.']

    def is_allowed_for_next_character(self, char):
        return self.is_whitespace(char) or self.is_separator(char) or self.is_operator(char)

    # Function used to extract and save variables and constants
    def parse_variable_constant(self, raw_data, index):
        current_text = raw_data[index:]
        if current_text[0].isdigit() or current_text[0] == '-' or current_text == '+':
            constant, position = self.constant_automaton.process(current_text, 0)
            if not self.is_allowed_for_next_character(current_text[position]):
                return False, index + position, False, -1
            serial = self.constants.contains(self.constants.root, constant)
            if serial == -1:
                serial = self.constants.insert(constant)
            return True, index + position, False, serial
        else:
            identifier, position = self.identifier_automaton.process(current_text, 0)
            if len(identifier) > 8:
                return False, index, False, -1
            if not self.is_allowed_for_next_character(current_text[position]):
                return False, index + position, False, -1
            serial = self.identifiers.contains(self.identifiers.root, identifier)
            if serial == -1:
                serial = self.identifiers.insert(identifier)
            return True, index + position, True, serial

    def run(self):
        f = open("input.txt", "r")
        raw_data = f.read()
        f.close()
        index = 0
        current_line = 1
        last_new_line_index = 1
        while index < len(raw_data):
            # Last token was a constant, we can't use '.' after it
            if len(self.PIF) > 0 and self.PIF[-1][0] == 1 and raw_data[index] == '.':
                print("Lexical error: cannot have two decimal points. Line: " + str(current_line) + " Char: " + str(
                    index - last_new_line_index))
                return
            # check reserved words first
            reserved = False
            for token in self.sorted_tokens:
                if raw_data[index:index + len(token)] == token:
                    # try and see if we have a negative number:
                    check_for_constant = False
                    if raw_data[index] == '-' or raw_data[index] == '+':
                        if len(self.PIF) > 0 and self.PIF[-1][0] not in [0, 1]:
                            check_for_constant = True
                    if check_for_constant:
                        found, save_index, is_identifier, serial = self.parse_variable_constant(raw_data, index)
                        if found and not is_identifier:
                            index = save_index
                            self.PIF.append((1, serial))
                            reserved = True  # make it skip the next check
                            break
                    # found reserved word, add it as -1 to PIF
                    if len(self.PIF) > 0 and self.PIF[-1][0] == self.tokens.index(token):
                        print(
                            "Lexical error: can't repeat reserved words. Line: " + str(current_line) + " Char: " + str(
                                index - last_new_line_index))
                        return
                    self.PIF.append((self.tokens.index(token), -1))
                    index += len(token)
                    reserved = True
                    break
            # not a reserved word, try looking for variable/constant
            if not reserved:
                found, index, is_identifier, serial = self.parse_variable_constant(raw_data, index)
                # Lexical error
                if not found:
                    print("Lexical error. Line: " + str(current_line) + " Char: " + str(index - last_new_line_index))
                    return
                # add it to PIF with a reference to the identifier's/constant's ID from their respective ST
                self.PIF.append((0 if is_identifier else 1, serial))
            # Last token was a constant, we can't have directly after it variable
            if len(self.PIF) > 0 and self.PIF[-1][0] == 1 and raw_data[index].isalpha():
                print("Lexical error: digit followed by an alpha. Line: " + str(current_line) + " Char: " + str(
                    index - last_new_line_index))
                return
            # skip all useless characters such as space, newline, tabs, line feed
            while index < len(raw_data) and raw_data[index] in ['\n', '\r', '\t', ' ']:
                if raw_data[index] == '\n':
                    last_new_line_index = index
                    current_line += 1
                index += 1

        raw = False
        for entry in self.PIF:
            if raw:
                print(entry)
            else:
                string = "\"" + self.tokens[entry[0]] + "\""
                self.tokenized_pif.append(self.tokens[entry[0]])
                if entry[0] == 0:
                    string += " -> " + self.identifiers.at_index(self.identifiers.root, entry[1])
                elif entry[0] == 1:
                    string += " -> " + self.constants.at_index(self.constants.root, entry[1])
                print(string)
        #print("\nIdentifiers:")
        #self.identifiers.inorder(self.identifiers.root)
        #print("Constants:")
        #self.constants.inorder(self.constants.root)
        print(self.tokenized_pif)
