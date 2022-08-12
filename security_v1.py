import json

class Security:
    """
    セキュリティ関連の機能を追加する部分になる予定だが、
    その辺には疎いので全然追加されないと思う

    そもそも、あのfloodgateもパスワードを平文で流しているので、
    セキュリティとかそんなにいらないと思う。
    """
    def __init__(self, white_list_file='./Players/White_list.json'):
        self.white_list_file = white_list_file
        self.load_white_list()

    def load_white_list(self):
        #white "list"だが、型はdict
        with open(self.white_list_file, 'r') as f:
            self.white_list = json.load(f)
        return

    def login_check(self, username, password):
        """
        ログインしても良いならTrue, ダメならFalse
        """
        username = ''.join(username.split(' '))
        password = ''.join(password.split(' '))
        if username not in self.white_list.keys():
            #リストに名前なし
            return False
        if password != self.white_list[username]:
            #パスワードが違う
            return False
        return True

    def add_user(self, username, password):
        """
        ユーザーを追加する
        """
        self.white_list[username] = password
        with open(self.white_list_file, 'w') as f:
            json.dump(self.white_list, f)
        return

    def delete_user(self, username):
        self.white_list.pop(username)
        with open(self.white_list_file, 'w') as f:
            json.dump(self.white_list, f)
        return

if __name__ == '__main__':
    print('Ari-Shogi-Server security_v1')
    S = Security()
    while True:
        command = input('command:')
        if command == 'add_user':
            S.add_user(input('username:'), input('password:'))
        if command == 'delete_user':
            S.delete_user(input('username:'))
        if command == 'print_white_list':
            print(S.white_list)
        if command == 'quit':
            break
