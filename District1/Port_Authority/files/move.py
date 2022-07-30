import asyncio
import websockets
import ast
import threading

# CTF{CapTA1n-cRUCh} level 2
# CTF{capt41n-h00k!} level 3
# CTF{c4pt41N-m0rG4N} level 4
# CTF{C4pt41N-4MErIc4} level 5
url = "wss://77319f73847bb7ddada62a109c116545.challenge.hackazon.org/ws"
mdp = 'CTF{C4pt41N-4MErIc4}'
level = 5
text = ""

def input_move():
    global text
    while True:
        text = input()
        

async def produce():  
    global text
    ship = 0  
    x1 = 1000
    y = 0
    async with websockets.connect(url) as ws:
        await ws.recv()
        print('connected')
        while True:
            
            if text == "":
                await ws.recv()
                
            else:
                if "a" in text:
                    for i in range(len(text)):
                        await ws.send('{"type": "SHIP_STEER", "shipId": %i}' % ship)
                        
                if text == "z":
                    await ws.recv()
                    
                    while y < 558:
                        rec = await ws.recv()
                        x = ast.literal_eval(rec.replace('\n','').replace('\r','').replace('false','False').replace('true','True').replace('null','None'))
                        ships = x['ships']
                
                        for bateau in ships:
                            id_ship = bateau['id']
                            if id_ship == ship:
                                y = (bateau['area'][1]['y'] - bateau['area'][0]['y']) / 2 + bateau['area'][0]['y']
                                
                                                          
                    await ws.send('{"type": "SHIP_STEER", "shipId": %i}' % ship)
                    
                    while x1 > 231:
                        rec = await ws.recv()
                        x = ast.literal_eval(rec.replace('\n','').replace('\r','').replace('false','False').replace('true','True').replace('null','None'))
                        ships = x['ships']
                
                        for bateau in ships:
                            id_ship = bateau['id']
                            if id_ship == ship:
                                x1 = (bateau['area'][1]['x'] - bateau['area'][0]['x']) / 2 + bateau['area'][0]['x']
                    await ws.send('{"type": "SHIP_STEER", "shipId": %i}' % ship)
                    x1 = 1000
                    y = 0
                    ship += 1
                                                    
                if text == "e":
                    break
                text = ""

        while True:
            print(await ws.recv())

threading.Thread(target=input_move).start()
asyncio.get_event_loop().run_until_complete(produce())