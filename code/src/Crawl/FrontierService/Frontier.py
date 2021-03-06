# -*- coding: utf-8 -*-
__author__ = 'hanxuan'

from Utils.ulog import log

from multiprocessing.connection import Listener

from multiprocessing.connection import Client

from multiprocessing import Process

from multiprocessing import Manager

from Crawl.MemShareManager import MemShareManager

from Utils.network import get_host

from FrontQueue import FrontQueue

from Utils.uredis import rs

import time

import math


class Frontier(object):

    PULL_IN_PORT = 9000
    PUSH_OUT_PORT = 9001
    BACK_QUEUE_MIN = 20000

    BACK_FRONT_RATIO = 0.1

    BACK_QUEUE_DOMAIN_MIN = 14

    def __init__(self, time_span):
        log.info('********** FRONTIER STARTED **********')
        mgr = MemShareManager()
        mgr.start()
        self.front_queue = mgr.FrontQueue()
        self.back_queue = mgr.BackQueue(time_span)
        self.filter = mgr.URLFilter()
        self.time_span = Manager().Value('l', time_span)
        self.authkey = 'han.xuan'

    def start(self):
        p1 = Process(target=self.pull_in)
        p2 = Process(target=self.front_to_back_process)
        p3 = Process(target=self.push_out)
        # p4 = Process(target=self.simu)
        p1.start(); p2.start(); p3.start();
        # p4.start()
        p1.join(); p2.join(); p3.join();
        # p4.join()

    def pull_in(self):
        address = ('127.0.0.1', Frontier.PULL_IN_PORT)
        listener = Listener(address, authkey=self.authkey)
        connection = listener.accept()
        log.info('Frontier : connection accepted from {}'.format(listener.address))
        while True:
            try:
                url = connection.recv_bytes()
                log.debug('url pull in: {}'.format(url))
                if self.filter.pass_check(url):
                    self.front_queue.push_one(url)
                    log.debug('pass_check: {}'.format(url))
            except Exception,e:
                log.warning('Frontier PULL IN ERROR: {}'.format(e))
                continue
        connection.close()
        listener.close()

    def front_to_back_process(self):
        while True:
            # if self.back_queue.size() > max(Frontier.BACK_QUEUE_MIN, self.front_queue.size() * Frontier.BACK_FRONT_RATIO):
            # log.info('BACK_QUEUE ({}) > ({}), FRONT_QUEUE ({}), DOMAIN IN BACK_QUEUE ({}) ,sleep {}'.
            #          format(self.back_queue.size(), self.front_queue.size() * Frontier.BACK_FRONT_RATIO, self.front_queue.size(),
            #                 self.back_queue.domain_count(), self.time_span.value / 1000))
            if self.back_queue.domain_count() >= Frontier.BACK_QUEUE_DOMAIN_MIN:
                log.info('BACK_QUEUE_DOMAIN ({}) > BACK_QUEUE_DOMAIN_MIN ({})'.
                         format(self.back_queue.size(), Frontier.BACK_QUEUE_DOMAIN_MIN))
                log.info('BACK_QUEUE ({}) > ({}), FRONT_QUEUE ({}), DOMAIN IN BACK_QUEUE ({}) ,sleep {}'.
                         format(self.back_queue.size(), self.front_queue.size() * Frontier.BACK_FRONT_RATIO, self.front_queue.size(),
                                self.back_queue.domain_count(), self.time_span.value / 1000))
                time.sleep(self.time_span.value / 1000)
            level_url = self.front_queue.pop_one()
            if level_url:
                level, url = level_url
                domain = get_host(url)
                if level: level = math.floor((level * 1.0 + self.new_level(url)) / 2)
                self.back_queue.push_one(domain, (level, url))
                log.debug('F2B: level:{}, url:{}'.format(level, url))

    def push_out(self):
        address = ('127.0.0.1', Frontier.PUSH_OUT_PORT)
        connection = Client(address, authkey=self.authkey)
        log.info('Frontier : connection established from {}'.format(address))
        counter = 0
        while True:
            url = self.back_queue.push_out()
            if url:
                try:
                    connection.send_bytes(url)
                    if counter % 2000 == 0:
                        log.info('FRONTIER PUSH TOTAL: {}'.format(counter))
                        counter += 1
                except Exception,e:
                    log.warning('Frontier PUSH OUT ERROR:{}'.format(e))
                    continue
        connection.close()

    @staticmethod
    def new_level(url):
        n_level = FrontQueue.LEVEL_LOW
        if rs.exists(url):
            in_link_count = min(int(rs.get(url)), FrontQueue.IN_LINK_MAX)
            log.debug("------------- REDIS {}-------------".format(in_link_count))
            n_level = FrontQueue.LEVEL_LOW - 1 - (in_link_count - FrontQueue.LEVEL_HIGH) * 5.0 / \
                                              (FrontQueue.IN_LINK_MAX - FrontQueue.LEVEL_HIGH)
        return n_level

    # def randomword1(self, len):
    #     return ''.join(random.choice(string.lowercase) for i in range(len))
    #
    # def randomword2(self, len):
    #     return ''.join(random.choice(string.octdigits) for i in range(len))
    #
    # def simu(self):
    #     log.info('in simu')
    #
    #     address = ('127.0.0.1', Frontier.PUSH_OUT_PORT)
    #     listener = Listener(address, authkey=self.authkey)
    #     connection1 = listener.accept()
    #
    #     address = ('127.0.0.1', Frontier.PULL_IN_PORT)
    #     connection = Client(address, authkey=self.authkey)
    #     while True:
    #         url = 'http://' + self.randomword1(10)
    #         connection.send_bytes(url)
    #         log.info('simu created: {}'.format(url))
    #         time.sleep(10)
    #     connection.close()


if __name__ == '__main__':
    Frontier(1000).start()

    # print Frontier.get_host('http://play.facebook.com')