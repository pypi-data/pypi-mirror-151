import clear
import codes
import colors
from cookieutils import key
import keys


input("Press enter to oscls")
clear.oscls()
input("Press enter to pcls")
clear.pcls()

input("Run codes")
print(codes.hex(10))
print(codes.uuid())
print(codes.custom(20, True, True, True, True))
print(codes.custom(20, custom=["<",">"]))

input("run colors")
print(colors.color("xterm", 124, 19))
print(colors.color("both",  colors.hex_to_xterm("#f41c18"), colors.rgb_to_xterm((24, 50, 244))))

input("run key")
print("press g")
if keys.get()["data"] == "g":
    print("YES")
else:
    quit("NO!")
print("press backspace")
if keys.get()["data"] == key.CKey.backspace:
    print("YES")
else:
    quit("NO!")