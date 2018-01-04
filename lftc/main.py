from entity.tree import Tree


def test():
    grammar_lines = [
        'S->aSbS',
        'S->aS',
        'S->c'
    ]
    tree = Tree(grammar_lines)
    results = [tree.validate('ac'), tree.validate('acbc'), tree.validate('aacbc'), tree.validate('d')]
    for r in results:
        print (r)

def main():
    test()

if __name__ == '__main__':
    main()