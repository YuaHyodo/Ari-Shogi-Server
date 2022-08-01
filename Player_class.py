import json
import time

class Player:
    def __init__(self, connect, name, password):
        self.connect = connect#接続
        self.name = name#名前
        self.password = password#パスワード
        self.buf_size = 1024#バフサイズ
        self.load_player_data()#プレーヤーデータの読み込み

    def update_player_data(self, result):
        #リザルトを反映させる
        self.player_data['games'] += 1 
        if result == 'win':
            self.player_data['wins'] += 1
        elif result == 'draw':
            self.player_data['draws'] += 1
        else:
            self.player_data['loses'] += 1
        return

    def load_player_data(self):
        #プレーヤー一覧に名前があるか？
        with open('./Players/Players.json', 'r') as f:
            players = json.load(f)
        self.new_player = False
        if self.name in players.keys():
            #あるならデータを読み込んで終わる
            self.path = players[self.name]
            with open(self.path, 'r') as f:
                self.player_data = json.load(f)
            return
        #無いなら初期値を設定する
        self.new_player = True 
        self.path = './Players/Player/' + self.name + '.json'
        self.player_data = {'rate': 1500, 'games': 0, 'wins': 0, 'draws': 0, 'loses': 0}
        return

    def write_player_data(self):
        #もし、新規プレーヤーならプレーヤー一覧に入れる必要がある
        if self.new_player:
            with open('./Players/Players.json', 'r') as f:
                players = json.load(f)
            players[self.name] = self.path
            with open('./Players/Players.json', 'w') as f:
                players = json.dump(players, f)
        #反映したものを記録
        with open(self.path, 'w') as f:
            json.dump(self.player_data, f)
        return

    def send_message(self, message):
        #メッセージを送る関数
        if '\n' not in message:
            #改行をつける
            message += '\n'
        self.connect.send(message.encode('utf-8'))
        return

    def recv_message(self):
        #メッセージを受け取る関数
        message = self.connect.recv(self.buf_size)
        return str(message)

    def get_move(self):
        #指し手を受け取る関数
        #また、消費時間を計測している
        start_time = time.time()
        while True:
            move = self.recv_message()
            if 'TORYO' in move:#投了
                return '%TORYO', int(time.time() - start_time)
            if 'KACHI' in move:#勝ち宣言
                return '%KACHI', int(time.time() - start_time)
            if 'CHUDAN' in move:#中断
                return '%CHUDAN', int(time.time() - start_time)
            if len(move) >= 7:#指して
                break
        #とりあえず動けば良い
        return move[2:9], int(time.time() - start_time)

    
