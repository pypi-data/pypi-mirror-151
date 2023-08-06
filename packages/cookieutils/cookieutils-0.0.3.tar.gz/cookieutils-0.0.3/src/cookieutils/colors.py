def color(text:str, color:int=15, bgcolor:int=None):
    if bgcolor:
        return(f"\033[48;5;{bgcolor}m\033[38;5;{color}m{text}\033[0;0m")
    else:
        return(f"\033[38;5;{str(color)}m{str(text)}\033[0;0m")




def rgb_to_xterm(rgb:tuple):
    r, g, b = rgb
    N = []
    for i, n in enumerate([47, 68, 40, 40, 40, 21]):
        N.extend([i]*n)
    mx = max(r, g, b)    
    mn = min(r, g, b)

    if (mx-mn)*(mx+mn) <= 6250:
        c = 24 - (252 - ((r+g+b) // 3)) // 10
        if 0 <= c <= 23:
            
            return 232 + c

    return 16 + 36*N[r] + 6*N[g] + N[b]

def hex_to_xterm(hex):

    if hex.startswith("#"):
        hex = hex.lstrip('#')

    return rgb_to_xterm(tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)))
