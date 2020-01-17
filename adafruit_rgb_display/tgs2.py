#!/usr/bin/env python3
import sys
import rply
from rply.token import Token

def dbg(lvl, *args, **kwargs):
    if lvl <= DEBUG_LVL:
        print('\t'*DBG_INDENT, 'DBGOUT :', *args,)
        for key, value in kwargs.items():
            print('\t'*DBG_INDENT, '\t', kye, ' = ', value)

# build the lexer
lg = rply.LexerGenerator()

left_paren = 'LPAREN'
right_paren = 'RPAREN'
var_name = 'VARNAME'
number_lit = 'NUMBER'
string_lit = 'STRING'
attribute_accessor = 'ATTRACSR'

set_kwarg = 'set'
func_kwarg = 'func'
as_kwarg = 'as'
args_kwarg = 'args'
vargs_kwarg = 'vargs'
foreach_kwarg = 'foreach'
while_kwarg = 'while'


lang_kwargs =   [
                set_kwarg, as_kwarg, args_kwarg, # var name affecting
                func_kwarg, foreach_kwarg, while_kwarg#loops
                ]

token_types = [left_paren, right_paren,
                number_lit, string_lit,
                var_name, attribute_accessor,
                *lang_kwargs]

#parens
lg.add(left_paren, r'\(')
lg.add(right_paren, r'\)')

#numbers
lg.add(number_lit, r'0[xX][0-9a-fA-F]*') # hex numbers
lg.add(number_lit, r'0[bB][01]*') #  bin number
lg.add(number_lit, r'\d+\.\d+') # float numbers
lg.add(number_lit, r'\d+') # ints numbers

#string literals
lg.add(string_lit, r'(""")(.*?)\1')
lg.add(string_lit, r"(''')(.*?)\1")
lg.add(string_lit, r'(")(.*?)\1')
lg.add(string_lit, r"(')(.*?)\1")

#strings #!FIXME: add strings
#lg.add('STRING', r'')

#var accessors
lg.add(attribute_accessor, r'\.') # getattr operator
#for kwarg in lang_kwargs:
#    lg.add(kwarg.upper(), kwarg.lower())
lg.add(var_name, r'[a-zA-Z_\-\+/*][a-zA-Z0-9_\-\+/*]*') # any var name conforming to python rules


lg.ignore(r'\s') # ignore whitespace but make it toek breaking
lg.ignore(r'#.*[\n\r]*') # single line comments
#lg.ignore(r'###[.\s]*###') # multiline w/ triple #

lexer = lg.build()

class obj_dict(dict):
    def push(self, value):

class tag():
    pass

class open_paren_tag(tag):
    pass

####################

stacks = obj_dict()

###

def pop_args(num = None):
    out = []
    while 1:
        var = stacks.peek().pop()pop()
        if type(var) == open_paren_tag:
            return out
        else:
            out.append(var)

def bt_set_attr_fn(inst, key, value):
    stacks.peek()




bt_class_obj = obj_dict(
    __name__  = 'class',
    __class__ = { },
    set       = bt_set_attr_fn,
    #'____'
)

bt_class_obj['__class__'] = bt_class_obj

def bt_number_call_fn(inst):
    arg = stacks.peek().pop()
    if arg['__class__'] == bt_number_cl:
        return


bt_number_cl = obj_dict(
    __name__  = 'number',
    __class__ = bt_class_obj,
    __call__ = bt_number_call_fn
)

bt_func_cl = obj_dict()

bt_print_obj = obj_dict(
    __name__ = 'print',
    __class__ = bt_func_cl,
    #'__call__' = print_call_fn,
)

std_module = obj_dict(
    print = bt_print_obj,
)

##++

def new_module():
    return obj_dict(**std_module)

def parse(tokens, scope = None):
    """
    """
    stacks.push(scope)
    while (1):
        if len(tokens) == 0:
            break
        tok = tokens.pop(0)
    stacks.pop()




tokens = [tok for tok in lexer.lex(open('./examples_scripts/test0.tgs', 'r').read())]
[print(tok) for tok in tokens]

parse(tokens, new_module())
