from pycparser import c_parser, c_ast
import pandas as pd
import os
import re
import sys
from gensim.models.word2vec import Word2Vec
import pickle
from tree import ASTNode, SingleNode
import numpy as np


def get_sequences(node, sequence):
    current = SingleNode(node)
    sequence.append(current.get_token())
    for _, child in node.children():
        get_sequences(child, sequence)
    if current.get_token().lower() == 'compound':
        sequence.append('End')


def get_blocks(node, block_seq):
    children = node.children()
    name = node.__class__.__name__
    if name in ['FuncDef', 'If', 'For', 'While', 'DoWhile']:
        block_seq.append(ASTNode(node))
        if name is not 'For':
            skip = 1
        else:
            skip = len(children) - 1

        for i in range(skip, len(children)):
            child = children[i][1]
            if child.__class__.__name__ not in ['FuncDef', 'If', 'For', 'While', 'DoWhile', 'Compound']:
                block_seq.append(ASTNode(child))
            get_blocks(child, block_seq)
    elif name is 'Compound':
        block_seq.append(ASTNode(name))
        for _, child in node.children():
            if child.__class__.__name__ not in ['If', 'For', 'While', 'DoWhile']:
                block_seq.append(ASTNode(child))
            get_blocks(child, block_seq)
        block_seq.append(ASTNode('End'))
    else:
        for _, child in node.children():
            get_blocks(child, block_seq)


def get_blocks_full_ast(node, block_seq):
    """
    获取完整的ast序列，把它本身转化为一颗可用于模型的ast，序列必然长度为一,用于粒度对比实验
    :param node:
    :param block_seq:
    :return:
    """
    block_seq.append(ASTNode(node))


def get_blocks_min_ast_node(node, block_seq):
    block_seq.append(node)
    for _, child in node.children():
        get_blocks(child, block_seq)


if __name__ == "__main__" :
    codeFile = "D://ABS/ProgramData/1/13.txt"
    code = ""
    with open(codeFile, encoding = "utf8") as f:
        code = "".join(f.readlines())

    from pycparser import c_parser
    parser = c_parser.CParser()
    ast = parser.parse(code)

    fullast = []
    get_blocks_full_ast(ast, fullast)
    minast = []
    get_blocks_min_ast_node(ast, minast)

    bestast = []
    get_blocks(ast, bestast)
    a=3



































