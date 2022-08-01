"""
メッセージをlistに格納して、それを順番に送るようにすると
まだマシになりそうなので、あとでやる。
"""
import cshogi
import shogi as pyshogi
import time

#改行を表す
k = '\n'

class game:
    def __init__(self, player1, player2, time_setting={'total': 300, 'inc': 10}):
        self.player1 = player1#先手
        self.player2 = player2#後手
        self.time_setting = time_setting#時間設定
        self.ID = 'game-' + player1.name + '-VS-' +player2.name + '-' + str(time.time()).replace('.', '')#ゲームID
        self.file_name = './games/' + self.ID + '.csa'#保存先ファイル名
        self.file_text = ''#ファイルに書き込む文章

    def write(self):#ファイルに書き込む
        with open(self.file_name, 'w') as f:
            f.write(self.file_text)
        return

    def start(self):#startという名前だが、これで完結している
        #ゲームサマリー(ゲームの情報に関するメッセージ)を各プレーヤに送信
        self.send_gamesummary(player_color='+')
        self.send_gamesummary(player_color='-')
        agree = [False, False]
        #返事待ち
        while True:
            m = self.player1.recv_message()
            if 'AGREE' in m:
                agree[0] = True
                break
            if 'REJECT' in m:
                break
        while True:
            m = self.player2.recv_message()
            if 'AGREE' in m:
                agree[1] = True
                break
            if 'REJECT' in m:
                break
        #両方agreeしたか？
        if agree[0] and agree[1]:
            #したのでスタート
            self.player1.send_message('START:' + self.ID + k)
            self.player2.send_message('START:' + self.ID + k)
        else:
            #どちらかが拒否したので停止
            if not agree[0]:
                r_name = self.player1.name
            else:
                r_name = self.player2.name
            self.player1.send_message('REJECT:' + self.ID + ' by ' + r_name + k)
            self.player2.send_message('REJECT:' + self.ID + ' by ' + r_name + k)
            return 'REJECT'
        #開始
        self.main_loop()
        return

    def send_gamesummary(self, player_color='+'):
        summary = 'BEGIN Game_Summary'
        summary += k
        summary += 'Protocol_Version: 1.2'
        summary += k
        summary += 'Format: Shogi 1.0'
        summary += k
        summary += ('Game_ID:' + self.ID)
        summary += k
        summary += ('Name+:' + self.player1.name)
        summary += k
        summary += ('Name-:' + self.player2.name)
        summary += k
        summary += ('Your_Turn:' + player_color)
        summary += k
        summary += 'To_Move:+'
        summary += k
        summary += 'Max_Moves:512'
        summary += k
        summary += 'BEGIN Time'
        summary += k
        summary += ('Total_Time:' + str(self.time_setting['total']))
        summary += k
        summary += ('Increment:' + str(self.time_setting['inc']))
        summary += k
        summary += 'END Time'
        summary += k
        summary += 'BEGIN Position'
        summary += k
        summary += 'P1-KY-KE-GI-KI-OU-KI-GI-KE-KY'
        summary += k
        summary += 'P2 * -HI *  *  *  *  * -KA *'
        summary += k
        summary += 'P3-FU-FU-FU-FU-FU-FU-FU-FU-FU'
        summary += k
        summary += 'P4 *  *  *  *  *  *  *  *  *'
        summary += k
        summary += 'P5 *  *  *  *  *  *  *  *  *'
        summary += k
        summary += 'P6 *  *  *  *  *  *  *  *  *'
        summary += k
        summary += 'P7+FU+FU+FU+FU+FU+FU+FU+FU+FU'
        summary += k
        summary += 'P8 * +KA *  *  *  *  * +HI *'
        summary += k
        summary += 'P9+KY+KE+GI+KI+OU+KI+GI+KE+KY'
        summary += k
        summary += 'P+'
        summary += k
        summary += 'P-'
        summary += k
        summary += 'END Position'
        summary += k
        summary += 'END Game_Summary'
        summary += k
        if player_color == '+':
            self.player1.send_message(summary)
        else:
            self.player2.send_message(summary)
        self.file_text += summary
        return

    def main_loop(self):
        #メインループ(不完全)
        #合法手チェック用
        board = cshogi.Board()
        board2 = pyshogi.Board()
        #残りの持ち時間
        player1_time = self.time_setting['total']
        player2_time = self.time_setting['total']
        #色々
        result = [None, None]
        moves_list = []
        c = 0
        while True:
            #手数が一定以上になったら引き分け
            if c >= 512:
                self.player1.send_message('#MAX_MOVES')
                self.player2.send_message('#MAX_MOVES')
                self.player1.send_message('#CENSORED')
                self.player2.send_message('#CENSORED')
                result = ['draw', 'draw']
                break
            #先手の行動
            move, t = self.player1.get_move()
            #時間などの管理
            player1_time -= t
            player1_time += self.time_setting['inc']
            c += 1
            #時間が切れたか？
            if player1_time <= 0:
                self.player1.send_message('#TIME_UP')
                self.player2.send_message('#TIME_UP')
                self.player1.send_message('#LOSE')
                self.player2.send_message('#WIN')
                self.file_text += ('%TIME_UP' + k)
                result = ['lose', 'win']
                break
            #投了したか？
            if move == '%TORYO':
                self.player1.send_message('%TORYO,T' + str(t))
                self.player2.send_message('%TORYO,T' + str(t))
                self.player1.send_message('#RESIGN')
                self.player2.send_message('#RESIGN')
                self.player1.send_message('#LOSE')
                self.player2.send_message('#WIN')
                self.file_text += ('%TORYO' + k)
                break
            #%CHUDANは反則行為とする
            if move == '%CHUDAN':
                self.player1.send_message('#ILLEGAL_ACTION')
                self.player2.send_message('#ILLEGAL_ACTION')
                self.player1.send_message('#LOSE')
                self.player2.send_message('#WIN')
                self.file_text += ('%ILLEGAL_MOVE' + k)
                result = ['lose', 'win']
                break
            #入玉宣言関係
            if move == '%KACHI':
                self.player1.send_message('%KACHI,T' + str(t))
                self.player2.send_message('%KACHI,T' + str(t))
                if board.is_nyugyoku():
                    self.player1.send_message('#JISHOGI')
                    self.player2.send_message('#JISHOGI')
                    self.player1.send_message('#WIN')
                    self.player2.send_message('#LOSE')
                    self.file_text += ('%KACHI' + k)
                    self.file_text += ('%JISHOGI' + k)
                    result = ['win', 'lose']
                else:
                    self.player1.send_message('#ILLEGAL_MOVE')
                    self.player2.send_message('#ILLEGAL_MOVE')
                    self.player1.send_message('#LOSE')
                    self.player2.send_message('#WIN')
                    self.file_text += ('%ILLEGAL_MOVE' + k)
                    result = ['lose', 'win']
                break
            #手番を変更
            message = move + ',T' + str(t)
            self.player1.send_message(message)
            self.player2.send_message(message)
            self.file_text += (move + k)
            
            #後手番
            if c >= 512:
                self.player1.send_message('#MAX_MOVES')
                self.player2.send_message('#MAX_MOVES')
                self.player1.send_message('#CENSORED')
                self.player2.send_message('#CENSORED')
                result = ['draw', 'draw']
                break
            move, t = self.player2.get_move()
            player2_time -= t
            player2_time += self.time_setting['inc']
            c += 1
            if player2_time <= 0:
                self.player2.send_message('#TIME_UP')
                self.player1.send_message('#TIME_UP')
                self.player2.send_message('#LOSE')
                self.player1.send_message('#WIN')
                self.file_text += ('%TIME_UP' + k)
                result = ['win', 'lose']
                break
            if move == '%TORYO':
                self.player2.send_message('%TORYO,T' + str(t))
                self.player1.send_message('%TORYO,T' + str(t))
                self.player2.send_message('#RESIGN')
                self.player1.send_message('#RESIGN')
                self.player2.send_message('#LOSE')
                self.player1.send_message('#WIN')
                self.file_text += ('%TORYO' + k)
                result = ['win', 'lose']
                break
            if move == '%CHUDAN':
                self.player2.send_message('#ILLEGAL_ACTION')
                self.player1.send_message('#ILLEGAL_ACTION')
                self.player2.send_message('#LOSE')
                self.player1.send_message('#WIN')
                self.file_text += ('%ILLEGAL_MOVE' + k)
                result = ['win', 'lose']
                break
            if move == '%KACHI':
                self.player2.send_message('%KACHI,T' + str(t))
                self.player1.send_message('%KACHI,T' + str(t))
                if board.is_nyugyoku():
                    self.player2.send_message('#JISHOGI')
                    self.player1.send_message('#JISHOGI')
                    self.player2.send_message('#WIN')
                    self.player1.send_message('#LOSE')
                    self.file_text += ('%KACHI' + k)
                    self.file_text += ('%JISHOGI' + k)
                    result = ['lose', 'win']
                else:
                    self.player2.send_message('#ILLEGAL_MOVE')
                    self.player1.send_message('#ILLEGAL_MOVE')
                    self.player2.send_message('#LOSE')
                    self.player1.send_message('#WIN')
                    self.file_text += ('%ILLEGAL_MOVE' + k)
                    result = ['win', 'lose']
                break
            message = move + ',T' + str(t)
            self.player2.send_message(message)
            self.player1.send_message(message)
            self.file_text += (move + k)
        #棋譜を保存
        self.write()
        #リザルトを反映
        self.player1.update_player_data(result[0])
        self.player2.update_player_data(result[1])
        self.player1.write_player_data()
        self.player2.write_player_data()
        return

    
