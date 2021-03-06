__author__ = 'Xuan Han'

from OkapiTF import OkapiTF

from OkapiTF_IDF import OkapiTfIDF

from OkapiBM25 import OkapiBM25

from LMLaplace import LMLaplace

from LMJelinekMercer import LMJelinekMercer

from OkapiBM25PRF import OkapiBM25PRF

from BLMLaplace import BLMLaplace

from MetaSearch import MetaSearch

from LMDirichlet import LMDirichlet

import os.path

query_file_path = "/Users/hanxuan/Dropbox/neu/summer15/information retrieval/data/AP_DATA/query_desc.51-100.short.txt"


def okapi_tf():
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.okapi'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break

        tf = OkapiTF(current_line)

        tf.term_regulate()

        tf.score()

        tf.print_result(output_file)


def okapi_tf_idf():
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.okapi.tf.idf'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break

        tf_idf = OkapiTfIDF(current_line)

        tf_idf.term_regulate()

        tf_idf.score()

        tf_idf.print_result(output_file)


def okapi_bm25():
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.okapi.bm25'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break

        bm25 = OkapiBM25(current_line)

        bm25.term_regulate()

        bm25.score()

        bm25.print_result(output_file)


def lmlapalce():
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.lm.laplace'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break

        lml = LMLaplace(current_line)

        lml.term_regulate()

        lml.score()

        lml.print_result(output_file)


def lmjm():
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.lm.jm'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break

        lmjem = LMJelinekMercer(current_line)

        lmjem.term_regulate()

        lmjem.score()

        lmjem.print_result(output_file)


def okapi_bm25_prf():
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.okapi.bm25.prf'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break

        bm25_prf = OkapiBM25PRF(current_line)

        bm25_prf.term_regulate()

        bm25_prf.score()

        bm25_prf.score_again()

        bm25_prf.print_result(output_file)


def okapi_bm25_prf_loop():
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.okapi.bm25.prf.loop'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break
        bm25_prf_loop = OkapiBM25PRF(current_line)

        bm25_prf_loop.term_regulate()

        bm25_prf_loop.loop()

        bm25_prf_loop.print_result(output_file)

def bigram():
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.bigram.laplace'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break
        bi = BLMLaplace(current_line)

        bi.term_regulate()

        bi.score()

        bi.print_result(output_file)

def meta_search_borda_fuse():
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.meta.bordafuse'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break
        meta = MetaSearch(current_line)

        meta.term_regulate()

        meta.score()

        meta.borda_fuse()

        meta.print_result(output_file)

def meta_search_combmnz():
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.meta.combmnz'
    if os.path.exists(output_file):
        os.remove(output_file)
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break
        meta = MetaSearch(current_line)

        meta.term_regulate()

        meta.score()

        meta.combmnz()

        meta.print_result(output_file)

def lmdirichlet():
    input_file = open(query_file_path, 'r')
    output_file = 'Results/output.lm.dirichlet'
    if os.path.exists(output_file):
        os.remove(output_file)
    # term_freq_short = dict()
    while 1:
        current_line = input_file.readline()
        if current_line == '':
            break
        dirichlet = LMDirichlet(current_line)

        dirichlet.term_regulate()

        # for term in dirichlet.query_terms:
        #     if term_freq.has_key(term):
        #         term_freq_short[term] = term_freq[term]

    # output = open('term_freq_short.cpkl', 'wb', 1024 * 1024)
    # cPickle.dump(term_freq_short, output, protocol=cPickle.HIGHEST_PROTOCOL)
    # print(len(term_freq_short))
    # output.close()

        dirichlet.score()

        dirichlet.print_result(output_file)


if __name__ == '__main__':

    # okapi_tf()
    #
    # okapi_tf_idf()
    #
    # okapi_bm25()
    #
    # lmlapalce()
    #
    # lmjm()
    #
    # okapi_bm25_prf()
    #
    # okapi_bm25_prf_loop()
    #
    # meta_search_borda_fuse()
    #
    # meta_search_combmnz()
    #
    bigram()
    #
    # lmdirichlet()


