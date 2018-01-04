class Node:
    def __init__(self, tag):
        self.tag = tag
        self.rules = []

    def add_rule(self, production_rule):
        self.rules.append(production_rule)

    def validate(self, input_band, pos, stack):
        if pos == len(input_band):
            #print('(' + ', '.join(
            #    [str('$'), '', '', str(stack), str([]), str(stack)]) + ') acc')
            return []
        saved_pos = pos
        for rule in self.rules:
            pos = saved_pos
            accepted_rules = []
            rejected = False
            #print('(' + ', '.join([str(input_band[pos:]), str(rule), str(accepted_rules[::-1])]) + ')')
            counter = 0
            print('(' + ', '.join(
                        [str(input_band[pos:]), str(rule), str(counter), str(stack), str(accepted_rules[::-1])]) + ')')
            for ch in rule.band:
                if pos == len(input_band):
                    rejected = True
                if rejected:
                    #print(rule.band, 'is rejected for', input_band[pos:])
                    break
                if isinstance(ch, str):
                    if input_band[pos] == ch:
                        pos += 1
                    else:
                        rejected = True
                elif isinstance(ch, Node):
                    acc = ch.validate(input_band, pos, stack + [rule.id])
                    if acc is None:
                        rejected = True
                    else:
                        accepted_rules += acc
                    pos += 1
                if not rejected and pos != len(input_band):
                    counter += 1
                    print('(' + ', '.join(
                        [str(input_band[pos:]), str(rule), str(counter), str(stack), str(accepted_rules[::-1])]) + ')')
            if not rejected:
                accepted_rules += [rule.id]
                if pos == len(input_band):
                    print('(' + ', '.join(
                        [str(input_band[pos:]), str(rule), str(counter), str(stack), str(accepted_rules[::-1])]) + ') acc')
                else:
                    pass
                    #print('(' + ', '.join([str(input_band[pos:]), str(rule), str(stack), str(accepted_rules[::-1])]) + ')')
                return accepted_rules
            print('(' + ', '.join([str(input_band[pos:]), str(rule), str(counter), str(stack), str(accepted_rules[::-1])]) + ') back')
        return None

class Rule:
    def __init__(self, id, band):
        self.id = id
        self.band = band

    def __str__(self):
        string = ''
        for ch in self.band:
            if isinstance(ch, str):
                string += ch
            else:
                string += ch.tag
        return string

class Tree:
    def __init__(self, lines):
        self.root = None
        self.rules = []
        self.nodes = {}
        for line in lines:
            tag = line.split('->')[0]
            if tag not in self.nodes:
                self.nodes[tag] = Node(tag)
        id = 1
        for line in lines:
            tag, rule = line.split('->')
            processed = []

            for ch in rule:
                if ch == '\n':
                    continue
                if ch not in self.nodes:
                    processed.append(ch)
                else:
                    processed.append(self.nodes[ch])
            self.rules.append(processed)
            self.nodes[tag].add_rule(Rule(id, processed))
            id += 1
        self.root = self.nodes[lines[0].split('->')[0]]

    def validate(self, input_band):
        print ('input', 'rule', 'rule-pos', 'stack', 'accepted')
        result = self.root.validate(input_band, 0, [])
        if result is not None:
            rtr_str = ''
            prods = [r for r in result[::-1]]
            unknown = []
            while len(prods):
                crt = prods.pop(0) - 1
                displacement = unknown.pop(0) if len(unknown) else 0
                line = '' + '  ' * displacement
                counter = 0
                for ch in self.rules[crt]:
                    if isinstance(ch, str):
                        line += ch + ' '
                    else:
                        line += ch.tag + ' '
                        unknown.append(displacement + counter)
                    counter += 1
                rtr_str += line + '\n'
            return rtr_str
        return 'Sequence is not accepted'
