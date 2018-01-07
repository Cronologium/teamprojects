from entity.tree import Tree
from syntax_analyser.syntax_rules import terminals, grammar


class SyntaxAnalyser:
    def __init__(self, PIF):
        self.tokens = terminals
        self.PIF = PIF
        self.grammar = grammar

    def analyse(self):
        sequence = ''
        for x in self.PIF:
            sequence += self.tokens[x]
        tree = Tree(grammar)
        result, program_code = tree.validate(sequence)
        print(sequence)
        print(result)
        print(program_code)
