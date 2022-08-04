import json

class HTML_update:
    def __init__(self):
        self.path = './html/Ari_Shogi_Server.html'

    def get_Players(self):
        self.players = []
        with open('./Players/Players.json', 'r') as f:
            players = json.load(f)
        for k, v in players.items():
            a = {'name': k}
            with open(v, 'r') as f:
                a.update(json.load(f))
            self.players.append(a)
        self.players = sorted(self.players, key= lambda x: x['rate'], reverse=True)
        return

    def update(self):
        self.get_Players()
        text  = """<!DOCTYPE html>
                        <html lang="ja">
                        <head>
                        <meta charset="UTF-8">
                        <title lang="ja">Ari Shogi Server</title>
                        </head>
                        <body>
                        <article>
                        <table summary="プレーヤの一覧" border="1" bgcolor="yellow" align="center" width="500px">
                        <caption>Players</caption>
                        <thead>
                        <tr>
                        <th id="name"><font color="green">Name</font></th>
                        <th id="rate"><font color="purple">rate</font></th>
                        <th id="games"><font color="deepskyblue">games<font></th>
                        <th id="wins"><font color="red">wins</font></th>
                        <th id="draws"><font color="black">draws</font></th>
                        <th id="losses"><font color="blue">losses</font></th>
                        </tr>
                        </thead>
                        <tbody>
                        """
        for player in self.players:
            text += """<tr align="center">
                            <td headers="name">{}</td>
                            <td headers="rate">{}</td>
                            <td headers="games">{}</td>
                            <td headers="wins">{}</td>
                            <td headers"draws">{}</td>
                            <td headers"losses">{}</td>
                            </tr>""".format(player['name'], int(player['rate']), player['games'], player['wins'], player['draws'], player['losses'])
        text += """</tbody></article></body></html>"""
        with open(self.path, 'w') as f:
            f.write(text)
        return

if __name__ == '__main__':
    HTML_update().update()
