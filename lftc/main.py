from entity.tree import Tree
from lexical_analyser.lexical_analyser import LexicalAnalyser
from syntax_analyser.syntax_analyser import SyntaxAnalyser


def test():
    grammar_lines = [
        'S->aSbS',
        'S->aS',
        'S->c'
    ]
    tree = Tree(grammar_lines)
    results = [tree.validate('ac'), tree.validate('acbc'), tree.validate('aacbc'), tree.validate('d')]
    for r in results:
        print(r)


def main():
    #test()
    lexical_analyser = LexicalAnalyser()
    lexical_analyser.run()
    syntax_analyser = SyntaxAnalyser(lexical_analyser.tokenized_pif)
    syntax_analyser.analyse()

if __name__ == '__main__':
    main()
