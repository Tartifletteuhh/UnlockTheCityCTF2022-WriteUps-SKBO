import asyncio
import websockets
import threading
import ast

# CTF{CapTA1n-cRUCh} level 2
# CTF{capt41n-h00k!} level 3
# CTF{c4pt41N-m0rG4N} level 4
# CTF{C4pt41N-4MErIc4} level 5
# CTF{CaPT41n-j4Ck-sp4rR0w}

url = "wss://478b717e4a89f2c87accb2f666aff5ea.challenge.hackazon.org/ws"
mdp = 'CTF{C4pt41N-4MErIc4}'
level = 5

ship = [0,1,2,3,4,5]

def delete():
    while True:
        input()
        del ship[0]

async def produce():
    
    async with websockets.connect(url) as ws:
        await ws.send('{"type": "START_GAME","level": %i, "password":"%s"}'% (level, mdp))
        await ws.recv()
        
        rec = await ws.recv()
        x = ast.literal_eval(rec.replace('\n','').replace('\r','').replace('false','False').replace('true','True').replace('null','None'))
        ships = x['ships']
        stop_vertical = 0
        
        for bateau in ships:                      # put the ships vertically
            name_ship = bateau['type']
            id_ship = bateau['id']
            direction = bateau['direction']
            
            if name_ship == 'SHIP_2': # left boat
                await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
                await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
                continue
            
            elif name_ship == 'SHIP_6' or name_ship =='SHIP_3':  # middle boat; top right boat
                if direction == 'UP':
                    await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
                    await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
                elif direction == 'RIGHT':
                    await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
                elif direction == 'LEFT':
                    await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
                    await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
                    await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
                    
              
        stop_5 = 0
        stop_4 = 0
        stop_1 = 0
                         
        while stop_vertical != 3:
            rec = await ws.recv()
            x = ast.literal_eval(rec.replace('\n','').replace('\r','').replace('false','False').replace('true','True').replace('null','None'))
            ships = x['ships']
                
            for bateau in ships:
                id_ship = bateau['id']
                name_ship = bateau['type']
                if name_ship == 'SHIP_5' and stop_5 == 0: # bottom left boat
                    id_ship_5 = id_ship
                    x_ship_5 = bateau['area'][0]['x']
                    if x_ship_5 < 550: 
                        await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship_5)
                        stop_vertical += 1
                        stop_5 = 1
                        
                elif name_ship == 'SHIP_1': # top middle boat
                    id_ship_1 = id_ship
                    x_ship_1 = bateau['area'][1]['x']
                    if x_ship_1 > 1100 and stop_1 == 0: 
                        await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship_1)
                        stop_vertical += 1
                        stop_1 = 1
                        
                elif name_ship == 'SHIP_4': # bottom right boat
                    id_ship_4 = id_ship
                    x_ship_4 = bateau['area'][0]['x'] 
                    if x_ship_4 < 1300 and stop_4 == 0: 
                        await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship_4)
                        stop_vertical += 1
                        stop_4 = 1

                
            
        while True:   # check if the ships are getting out of the defined border
                
            rec = await ws.recv()
            x = ast.literal_eval(rec.replace('\n','').replace('\r','').replace('false','False').replace('true','True').replace('null','None'))
            ships = x['ships']
               
            for bateau in ships:
                
                direction = bateau['direction']
                id_ship = bateau['id']

                if id_ship in ship:
                    if direction == 'UP':
                        y = bateau['area'][0]['y']
                        if y <= 720:
                            await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
                            await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
                            
                    elif direction == 'DOWN':
                        y = bateau['area'][1]['y']
                        if y >= 1100:
                            await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
                            await ws.send('{"type": "SHIP_STEER", "shipId": %i}' %id_ship)
            for i in range(8):
                await ws.recv()
                             
            


                                                                                   
threading.Thread(target=delete).start()       
asyncio.get_event_loop().run_until_complete(produce())