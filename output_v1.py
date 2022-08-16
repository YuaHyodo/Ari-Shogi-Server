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
