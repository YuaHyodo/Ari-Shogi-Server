"""
This file is part of Ari-Shogi-Server

Copyright (c) 2022 YuaHyodo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from output_v1 import HTML_update
from play_game_v1 import game
from security_v1 import Security
from Player_class import Player
from  threading import Thread
from logger_v1 import logger
import numpy as np
import socket

#各種設定
HOST = '127.0.0.1'
PORT = 4081
buf_size = 1024
k = '\n'

class Server_v1:
    def __init__(self):
        #初期化
        self.log = logger()
        self.output = HTML_update()
        self.security = Security()
        self.log.clear_log()
        self.waiting_players = []
        self.playing_players = []
        self.games = []
        self.log.write('init_server')

    def login_cliant(self):
        #ログイン待機
        self.log.write('login waiting')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            try:
                cliant, addr = s.accept()
                break
            except:
                pass
        while True:
            m = str(cliant.recv(buf_size))
            if 'LOGIN' in m:
                break
            else:
                pass
        #usernameをスマートじゃない方法で抽出
        index = list(m)[8:].index(' ')
        index += 8
        username = m[8:index]
        password = m[index:-3]
        if self.security.login_check(username, password):
            self.log.write('user ' + username + ' login')
            cliant.send(str('LOGIN:' + username + ' OK' + k).encode('utf-8'))
            #待機プレーヤのlistに追加
            player = Player(cliant, username, password)
            self.waiting_players.append(player)
        else:
            self.log.write('login failed username: ' + username)
            cliant.send(('LOGIN:incorrect' + k).encode('utf-8'))
        return

    def match_make(self):
        self.log.write('start match make')
        if len(self.waiting_players) < 2:
            #プレーヤー数が不十分
            print('cancel match make')
            return
        #ランダムにマッチング
        np.random.shuffle(self.waiting_players)
        a = list(range(0, len(self.waiting_players), 2))
        for i in a:
            player1 = self.waiting_players[i]
            player2 = self.waiting_players[i + 1]
            self.games.append(game(player1, player2)) 
            self.playing_players.extend([player1, player2])
        #待機listから外す
        del self.waiting_players[0:a[-1]]
        self.log.write('make ' + str(len(self.games)) + ' matchs')
        #対局を開始する
        threads_list = []
        for g in self.games:
            thread = Thread(target=g.start)
            threads_list.append(thread)
        for t in range(len(threads_list)):
            threads_list[t].start()
            self.log.write('start game ' + self.games[t].ID)
        #すべての対局が終わるまで待機
        for t in range(len(threads_list)):
            threads_list[t].join()
            self.log.write('finish game ' + self.games[t].ID)
        self.output.update()
        return

    def test1(self):
        #テスト
        self.log.write('start test1')
        while len(self.waiting_players) < 2:
            self.login_cliant()
            self.log.write('waiting cliants:' + str(len(self.waiting_players)))
        self.match_make()
        self.log.write('finish test1')
        return

if __name__ == '__main__':
    server = Server_v1()
    server.test1()
