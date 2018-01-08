terminals = {
    'identifier': 'I',
    'constant': 'C',
    'int': 'i',
    'double': 'd',
    'cin': 'a',
    'cout': 'b',
    'if': 'e',
    'for': 'f',
    'else': 'g',
    '/': 'h',
    '*': 'j',
    '-': 'k',
    '+': 'l',
    '<': 'm',
    '>': 'n',
    '<=': 'o',
    '>=': 'p',
    '=': 'q',
    '==': 'r',
    '!=': 's',
    '{': 't',
    '}': 'u',
    ';': 'v',
    '.': 'w',
    '(': 'z',
    ')': 'x',
    '>>': 'y',
    '<<': 'A',
    'struct': 'B',
    'main': 'D',
    '<iostream>': 'E',
    'return': 'F',
    '#include': 'G',
    'using': 'H',
    'namespace': 'J',
    'std': 'K'
}

non_terminals = {
    'L': 'program',
    'M': 'directives',
    'N': 'global',
    'O': 'statement_list',
    'P': 'struct_definitions',
    'Q': 'struct',
    'R': 'fields',
    'S': 'type',
    'T': 'statement',
    'U': 'declaration',
    'V': 'assignment',
    'W': 'if_stmt',
    'Z': 'for_stmt',
    'X': 'output',
    'Y': 'input',
    '1': 'block_code',
    '2': 'simple_type',
    '3': 'expression',
    '4': 'term',
    '5': 'operator',
}

grammar = [
    'L->MNiDzxtOu',
    'M->GE',
    'N->HJKvP', 'N->HJKv',
    'O->TO', 'O->T',
    'P->QP', 'P->Q',
    'Q->BItRuv',
    'R->SIvR', 'R->SIv',
    'S->2', 'S->I',
    'T->Uv', 'T->Vv', 'T->W', 'T->Z', 'T->Xv', 'T->Yv', 'T->FCv',
    'U->SIq3', 'U->SIqC', 'U->SI',
    'V->IwIqC', 'V->IwIq3', 'V->Iq3', 'V->IqC',
    'W->ez3x1g1', 'W->ez3x1',
    'X->bA3',
    'Y->ayI',
    'Z->fzVv3vVx1',
    '1->tOu', '1->O',
    '2->i', '2->d',
    '3->453', '3->z3x', '3->4',
    '4->IwI', '4->C', '4->I',
    '5->h', '5->j', '5->k', '5->l', '5->m', '5->n', '5->o', '5->p', '5->s'
]