'''
MohammadMahdi Javid
'''


import string


class Grammar:
    '''
    A non-terminal generating a terminal (e.g.; X->x)
    A non-terminal generating two non-terminals (e.g.; X->YZ)
    Start symbol generating ε. (e.g.; S-> ε)
    '''

    @classmethod
    def create_cell(cls, cell1, cell2):
        cell = set()
        if not cell1 and not cell2:
            return cell
        for f in cell1:
            for s in cell2:
                cell.add(f+s)
        return cell

    @classmethod
    def Check(cls, transisions: dict, inp: str, char2var: dict, transision_term, transision_var, var0, var1):
        length = len(inp)
        table = [[set() for _ in range(length-idx)] for idx in range(length)]
        for idx, char in enumerate(inp):
            if char in char2var:
                table[0][idx] = char2var[char].copy()
        for i in range(1, length):
            for j in range(length - i):
                for k in range(i):
                    cell = cls.create_cell(table[k][j], table[i-k-1][j+k+1])
                    for item in cell:
                        if item in char2var:
                            table[i][j] |= char2var[item]
        return 'Accepted' if '<S0>' in table[-1][0] else 'Rejected'

    @classmethod
    def extract_prods(cls, transition):
        idx = 0
        prod = []
        while idx < len(transition):
            if transition[idx] is '<':
                prod.append(transition[idx: idx+3: 1])
                idx += 2
            else:
                prod.append(transition[idx: idx + 1: 1])
            idx += 1
        return tuple(prod)

    @classmethod
    def extract_alphabet(cls, line, terms):
        toks = line.split('->')[1].split('|')
        for tok in toks:
            tok = tok.strip()
            idx = 0
            while idx < len(tok):
                if tok[idx] == '<':
                    idx += 2
                elif tok[idx] == '#':
                    pass
                else:
                    terms.add(tok[idx])
                idx += 1

    @classmethod
    def parse_input(cls, lines,  terms, variables, prods):
        for line in lines:
            var, transitions = line.split(
                "->")[0].strip(), [transition.strip() for transition in line.split('->')[1].split('|')]
            variables.add(var)
            for transition in transitions:
                prods.add((var, cls.extract_prods(transition)))
                if transition is "#":
                    continue
                cls.extract_alphabet(line, terms)

    @classmethod
    def add_new_root(cls, terms: set, variables: set, prods: set, new_label: str, root):
        variables.add(new_label)
        prods.add((new_label, (root,)))

    @classmethod
    def rem_TERMS(cls, terms: set, variables: set, prods: set, remained_chars: set):
        char2var = {}
        for variable, transision in prods:
            if not len(transision) is 1:
                continue
            if not variable in variables:
                continue
            if not next(iter(transision)) in terms:
                continue
            char2var[next(iter(transision))] = variable
        for variable, transision in prods.copy():
            if len(transision) is 1 and next(iter(transision)) in terms:
                continue
            for index, char in enumerate(transision):
                if char in char2var:
                    prods.remove((variable, transision))
                    transision = list(transision)
                    transision[index] = char2var[char]
                    transision = tuple(transision)
                    prods.add((variable, tuple(transision)))
                elif char in terms:
                    new_char = remained_chars.pop()
                    variables.add(new_char)
                    char2var[char] = new_char
                    prods.add((new_char, (char,)))
                    prods.remove((variable, transision))
                    transision = list(transision)
                    transision[index] = new_char
                    transision = tuple(transision)
                    prods.add((variable, transision))

    @classmethod
    def CNF(cls, terms, variables: set, prods: set, remained_chars: set):
        char2var = {}
        for variable, transision in prods.copy():
            size = len(transision)
            if size < 3:
                continue
            transision = list(transision)
            while size != 2:
                new_transision = tuple(transision[size-2:size+1:])
                prods.remove((variable, tuple(transision)))
                if not new_transision in char2var:
                    new_var = remained_chars.pop()
                    char2var[new_transision] = new_var
                    transision = tuple(transision[:size-2:1] + [new_var])
                    new_transision = tuple(new_transision)
                    prods.add((new_var, new_transision))
                    prods.add((variable, transision))
                    variables.add(new_var)
                else:
                    new_var = char2var[variable]
                    transision = tuple(transision[:size-1:1] + [new_var])
                    prods.add((variable, transision))
                size -= 1

    @classmethod
    def findvars(cls, terms: set, variables: set, prods: set, remained_chars: set):
        removed = set()
        for variable, transision in prods.copy():
            if not len(transision) is 1:
                continue
            if not next(iter(transision)) == '#':
                continue
            prods.remove((variable, transision))
            removed.add(variable)
        return removed

    @classmethod
    def NULL(cls, terms, variables, prods, remained_chars):
        vars = cls.findvars(terms, variables, prods, remained_chars)
        for var in vars:
            for variable, transision in prods.copy():
                if not var in transision:
                    continue
                new_transision = list(transision)
                new_transision.remove(var)
                prods.add((variable, tuple(new_transision)))

    @classmethod
    def find_UNARY(cls, terms, variables, prods, remained_chars):
        UNARIES = set()
        for variable, transision in prods.copy():
            if not len(transision) is 1:
                continue
            if not next(iter(transision)) in variables:
                continue
            UNARIES.add((variable, next(iter(transision))))  # parent - child
        return UNARIES

    @classmethod
    def var_trans(cls, prods, src, dst):
        for variable, transision in prods.copy():
            if not variable == dst:
                continue
            prods.add((src, transision))

    @classmethod
    def UNIT(cls, terms, variables, prods, remained_chars):
        UNARIES = cls.find_UNARY(terms, variables, prods, remained_chars)
        for variable, transision in prods.copy():
            if not len(transision) is 1:
                continue
            if not next(iter(transision)) in variables:
                continue
            if not (variable, next(iter(transision))) in UNARIES:
                continue
            prods.remove((variable, transision))
            cls.var_trans(prods, variable, next(iter(transision)))

    @classmethod
    def useless_prod(cls, terms, variables, prods, remained_chars):
        cls.rem_TERMS(terms, variables, prods, remained_chars)
        cls.CNF(terms, variables, prods, remained_chars)
        cls.NULL(terms, variables, prods, remained_chars)
        size_before = len(prods)
        cls.UNIT(terms, variables, prods, remained_chars)
        size_after = len(prods)
        while size_before != size_after:
            size_before = len(prods)
            cls.UNIT(terms, variables, prods, remained_chars)
            size_after = len(prods)

    @classmethod
    def simplify(cls, terms: set, variables: set, prods: set, remained_chars: set, root):
        '''
        A variable generating a terminal (e.g.; X->x)
        A variable generating two variables (e.g.; X->YZ)
        Start symbol generating lambda
        '''
        cls.add_new_root(terms, variables, prods, '<S0>', root)
        cls.useless_prod(terms, variables, prods, remained_chars)

    @classmethod
    def converter_char2var(cls, terms, variables, prods):
        transisions = {}
        char2var = {}
        transision_term = []
        transision_var = []
        for variable, transision in prods:
            tmp = ""
            for trs in transision:
                tmp += trs
            if variable in transisions:
                transisions[variable].add(tmp)
            else:
                transisions[variable] = {tmp, }
            if tmp in char2var:
                char2var[tmp].add(variable)
            else:
                char2var[tmp] = {variable, }
            if not len(transision) is 1:
                transision_var.append([variable, "".join(transision)])
            else:
                transision_term.append([variable, next(iter(transision))])
        return transisions, char2var, transision_term, transision_var


def main():
    lines = [input() for line in range(int(input()))]
    terms = set()
    variables = set()
    prods = set()
    remained_chars = set((f'JKW{i}' for i in range(10000)))
    root = lines[0].split('->')[0].strip()
    Grammar.parse_input(lines, terms, variables, prods)
    Grammar.simplify(terms, variables, prods, remained_chars, root)
    inp = input()
    transisions, char2var, transision_term, transision_var = Grammar.converter_char2var(
        terms, variables, prods)
    var0 = [va[0] for va in transision_var]
    var1 = [va[1] for va in transision_var]
    answ = Grammar.Check(transisions, inp, char2var,
                         transision_term, transision_var, var0, var1)
    print(answ)


if __name__ == '__main__':
    main()