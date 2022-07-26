hex = ""

with open("hexa","r") as f:
    hex = f.readline()  
      
with open("test.txt","wb") as file:
    byte_array = bytearray.fromhex(hex)
    file.write(byte_array)