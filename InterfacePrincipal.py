import math
import time
import pygame as pg

pg.init()
pg.font.init()


arial_font = pg.font.SysFont('Arial', 32)
arial_font_title = pg.font.SysFont('Arial', 48)
arial_font_alert = pg.font.SysFont('Arial', 30)
arial_font_small = pg.font.SysFont('Arial', 24)

screen = pg.display.set_mode((600, 1024))
#pg.mouse.set_visible(0)
pgClock = pg.time.Clock()


def contador(n):
    if n == True:
        start_time = time.time()
        start_time = int(start_time)
        return start_time
    else:
        end_time = time.time()
        end_time = int(end_time)
        return end_time

def calculoValor(start,end):
    valor = (end - start)*(2/3600)
    print(f'Total a pagar: R$ {valor:.2f}')
    return ''



slot1, slot2, slot3, slot4, slot5, slot6 = False, False, False, False, False, False
slot = [False, False, False, False, False, False]
passwords = [0 for x in slot]
start_time = [time.time() for x in slot]
end_time = [time.time() for x in slot]

intro_animation_time = time.time()

screen_offset = 0 # The ofset for changing screen animation
last_screen_offset = 0 # The last screen offset used before animation
screen_offset_animation_time = time.time() # Time of start of the animation of the changing of screen

interface = 0 # Type of interface, like password changing or FAV selection.

end_program = False

class interfaceInput:
    inputs = []
    has_pressed = False
    has_pressedAKey = False
    touched_id = -1
    cursor_animation_time = time.time() # Animation time of the little cursor
    keyBoardPos = 1024
    focus_animation_time = time.time() # Animation time of fucus animation
    editing = -1
    last_editing = -1
    KEYBOARD_TOP = 624
    def __init__(self):
        return
    def render(self, screen):
        j = 0
        pos = pg.mouse.get_pos()
        entered = -1
        for i in self.inputs:
            pg.draw.rect(screen, (240, 240, 240), pg.rect.Rect(i[0], i[1], i[2], 46), border_radius=8)
            if arial_font.size(i[3])[0] < i[2]:
                renderPygameText(arial_font, screen, i[3], (i[0] + 8, i[1] + 4)) # Renders input content
            elif i[2] // 10 < len(i[3]):
                renderPygameText(arial_font, screen, i[3][:i[2] // 10], (i[0] + 8, i[1] + 4)) # Renders input content cutted
            else:
                renderPygameText(arial_font, screen, i[3][:i[2] // 20], (i[0] + 8, i[1] + 4)) # Renders input content cutted
            if pg.mouse.get_pressed()[0] and not self.has_pressed and not self.has_pressedAKey and self.touched_id == -1:
                if pos[0] >= i[0] and pos[1] >= i[1] and pos[0] < i[0] + i[2] and pos[1] < i[1] + 46:
                    self.cursor_animation_time = time.time()
                    if self.editing == -1:
                        self.focus_animation_time = time.time()
                    self.last_editing = self.editing
                    self.editing = j
                    self.touched_id = j
            if j == self.editing:
                if int((time.time() - self.cursor_animation_time) * 2) % 2 == 0:
                    pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(i[0] + 8 + arial_font.size(i[3])[0], i[1] + 8, 3, 30), border_radius=1)
                if i[4] == "numeric": # Detects the type of input
                    if time.time() - self.focus_animation_time < .4:
                        self.keyBoardPos = cubic_bezier(1024, self.KEYBOARD_TOP - 100, self.KEYBOARD_TOP - 10, self.KEYBOARD_TOP, (time.time() - self.focus_animation_time) / .4)
                        # print(self.keyBoardPos)
                    else:
                        self.keyBoardPos = self.KEYBOARD_TOP
                    entered = renderNumericFavKeyboard(screen, (149, self.keyBoardPos), self.has_pressed) # Reads the input from numeric keyboard
                    # print(entered)
                    if entered >= 0 and entered <= 9 and not self.has_pressed and not self.has_pressedAKey and (len(i[3]) < i[5] or i[5] < 0): # Avoids repeating typing when holding a key
                        self.inputs[j][3] += str(entered)
                    elif entered == 11 and not self.has_pressed and not self.has_pressedAKey and len(i[3]): # Erase key
                        self.inputs[j][3] = self.inputs[j][3][:-1]
                elif i[4] == "text": # Detects the type of input
                    if time.time() - self.focus_animation_time < .4:
                        self.keyBoardPos = cubic_bezier(1024, self.KEYBOARD_TOP - 100, self.KEYBOARD_TOP - 10, self.KEYBOARD_TOP, (time.time() - self.focus_animation_time) / .4)
                        # print(self.keyBoardPos)
                    else:
                        self.keyBoardPos = self.KEYBOARD_TOP
                    entered = renderAlphaKeyboard(screen, (0, self.keyBoardPos), self.has_pressed) # Reads the input from numeric keyboard
                    # print(entered)
                    if entered >= 48 and entered <= 96 and not self.has_pressed and not self.has_pressedAKey and (len(i[3]) < i[5] or i[5] < 0): # Avoids repeating typing when holding a key
                        self.inputs[j][3] += chr(entered)
                    elif entered == 11 and not self.has_pressed and not self.has_pressedAKey and len(i[3]): # Erase key
                        self.inputs[j][3] = self.inputs[j][3][:-1]
            j += 1
        
        # Animates keyboard when no input is focused
        ret = False # Return value
        if entered == 10 and pg.mouse.get_pressed()[0] and not self.has_pressed:
            ret = True
        if self.editing < 0 and self.keyBoardPos < 1024 and time.time() - self.focus_animation_time < .4:
            self.keyBoardPos = cubic_bezier(self.KEYBOARD_TOP, self.KEYBOARD_TOP, 1034, 1024, (time.time() - self.focus_animation_time) / .4)
            # print(self.last_editing)
            if self.inputs[self.last_editing][4] == "numeric" and self.last_editing >= 0:
                renderNumericFavKeyboard(screen, (149, self.keyBoardPos), self.has_pressed) # Just renders the numeric keyboard
            if self.inputs[self.last_editing][4] == "text" and self.last_editing >= 0:
                renderAlphaKeyboard(screen, (0, self.keyBoardPos), self.has_pressed) # Just renders the numeric keyboard
        self.has_pressed = pg.mouse.get_pressed()[0] # Gets if the screen was already touched
        self.has_pressedAKey = True in pg.key.get_pressed() # Gets if a key was already pressed
        if self.touched_id == -1 and not self.has_pressed and pg.mouse.get_pressed()[0] and (entered < 0 or entered > 11): # Unfocus an input
            self.last_editing = self.editing
            self.editing = -1
            self.focus_animation_time = time.time()
        if not self.has_pressed: # Resets the "touched_id". It allows to select another input
            self.touched_id = -1
        return ret

    def focus(self, id):
        if self.editing == -1:
            self.focus_animation_time = time.time()
            self.cursor_animation_time = time.time()
        self.last_editing = self.editing
        self.editing = id
        if self.editing < 0:
            self.editing = -1
            self.focus_animation_time = time.time()

    def add(self, position=(0, 0), width=300, value="", typeOf="text", max=-1):
        self.inputs.append([position[0], position[1], width, value, typeOf, max])
    def setPosition(self, id, position):
        self.inputs[id][0] = position[0]
        self.inputs[id][1] = position[1]
    def getValue(self, id):
        if id >= len(self.inputs):
            return
        return self.inputs[id][3]
    
    def setValue(self, id, text):
        if id >= len(self.inputs):
            return
        self.inputs[id][3] = text

def renderPygameText(pgFont, screen, text, position=(0,0), color=(0,0,0)):
    text_surface = pgFont.render(text, False, color)
    screen.blit(text_surface, position)

def cubic_bezier(p1, p2, p3, p4, t):
    return (1 - t)** 3 * p1 + 3 * (1 - t)**2 * t * p2 + 3 * (1 - t) * t ** 2 * p3 + t ** 3 * p4

hexagonCoords = [(math.cos(math.radians(ang)), math.sin(math.radians(ang))) for ang in range(0, 360, 60)]

def isInsideAHex(pos, size, pt):
    size = (abs(size[0]), abs(size[1]))
    hxc = [(point[0] * size[0] + pos[0], point[1] * size[1] + pos[1]) for point in hexagonCoords]
    # pg.draw.polygon(screen, (255, 0, 0), hxc) # Test of area
    if pt[0] >= hxc[4][0] and pt[1] >= hxc[4][1] and pt[0] < hxc[1][0] and pt[1] < hxc[1][1]:
        return True
    coef = (hxc[4][1] - hxc[3][1]) / (hxc[4][0] - hxc[3][0]) # Linear coeficient for detection of triangle
    # print((pt[0] - hxc[3][0]) * coef + hxc[3][1] - pt[1])
    # pg.draw.line(screen, (255, 0, 0), (0, (0 - hxc[3][0]) * coef + hxc[3][1]), (800, (800 - hxc[3][0]) * coef + hxc[3][1])) # Test border
    if (pt[0] - hxc[3][0]) * coef + hxc[3][1] - pt[1] <= 0 and (pt[0] - hxc[3][0]) * (-coef) + hxc[3][1] - pt[1] >= 0 and pt[0] >= hxc[3][0] and pt[0] < hxc[4][0]: # Checks if the point is inside the triangle using linear equation
        return True
    elif (pt[0] - hxc[5][0]) * (-coef) + hxc[5][1] - pt[1] <= 0 and (pt[0] - hxc[1][0]) * coef + hxc[1][1] - pt[1] >= 0 and pt[0] < hxc[0][0] and pt[0] >= hxc[1][0]: # Checks if the point is inside the triangle using linear equation
        return True
    return False
    

# Numeric Keyboard Variables

numericKeyAnimationTime = [time.time() for x in range(12)] # Animation time for numeric keyboard key
numericKeyId = -1
numericKeyTouched = False

inps = interfaceInput()
inps.add((225, 315), 150, typeOf = "numeric", max=9) # Adds the password input
inps.add((10, 315), 580, typeOf = "text", max=256) # Adds the e-mail input

def renderNumericKeyboard(screen, position=(0, 0), press=False):
    global numericKeyId;
    global numericKeyTouched
    global numericKeyAnimationTime;
    global arial_font;
    pos = pg.mouse.get_pos()
    pressed = pg.mouse.get_pressed()
    # Keeps the key stored until the user releases the screen
    if numericKeyId >= 0 and numericKeyId < 9:
        key = numericKeyId + 1
    elif numericKeyId == 9:
        key = 10
    elif numericKeyId == 10:
        key = 0
    elif numericKeyId == 11:
        key = 11
    else:
        key = -1
    # print(pressed[pg.K_LEFT])
    # print(press)
    pg.draw.rect(screen, (240, 240, 240), pg.rect.Rect(position[0], position[1], 302, 402))
    for i in range(9):
        if pressed[0]:
            if pos[0] >= position[0] + (i % 3) * 100 + 2 and pos[1] >= position[1] + (i // 3) * 100 + 2 and pos[0] < position[0] + (i % 3) * 100 + 100 and pos[1] < position[1] + (i // 3) * 100 + 100:
                # Avoids mistaken pressed keys affect the first key pressed
                if numericKeyId == -1:
                    numericKeyId = i
                if numericKeyId == i:
                    key = i + 1
                    numericKeyAnimationTime[i] = time.time()
                elif numericKeyId != -1:
                    key = numericKeyId + 1
        #pg.draw.rect(screen, (200 - (key == (i - 1)) * 100, 200 - (key == (i - 1)) * 100, 200 - (key == (i - 1)) * 100), pg.rect.Rect(position[0] + (i % 3) * 100 + 2, position[1] + (i // 3) * 100 + 2, 98, 98))
        deltaAnimation = time.time() - numericKeyAnimationTime[i]
        if deltaAnimation < .4:
            pg.draw.rect(screen, [100 + 250 * deltaAnimation for x in range(3)], pg.rect.Rect(position[0] + (i % 3) * 100 + 2, position[1] + (i // 3) * 100 + 2, 98, 98))
        else:
            pg.draw.rect(screen, (200, 200, 200), pg.rect.Rect(position[0] + (i % 3) * 100 + 2, position[1] + (i // 3) * 100 + 2, 98, 98))
        renderPygameText(arial_font, screen, str(i+1), (51 - arial_font.size(str(i+1))[0] // 2 + position[0] + (i % 3) * 100, position[1] + (i // 3) * 100 + 32))
    end_chars = ["OK", "0", "←"] # Keys at the bottom ofthe numeric keyboard
    for i in range(3):
        if pressed[0]:
            if pos[0] >= position[0] + i * 100 + 2 and pos[1] >= position[1] + 302 and pos[0] < position[0] + i * 100 + 100 and pos[1] < position[1] + 400:
                # The verification made to avoid mistaken keys being considerated pressed
                if numericKeyId == -1:
                    numericKeyId = i + 9
                if numericKeyId == i + 9:
                    if i == 0:
                        key = 10
                    elif i == 1:
                        key = 0
                    else:
                        key = 11
                    numericKeyAnimationTime[i + 9] = time.time()
        deltaAnimation = time.time() - numericKeyAnimationTime[i + 9]
        if deltaAnimation < .4:
            pg.draw.rect(screen, [100 + 250 * deltaAnimation for x in range(3)], pg.rect.Rect(2 + position[0] + 100 * i, 302 + position[1], 98, 98))
        else:
            pg.draw.rect(screen, (200, 200, 200), pg.rect.Rect(2 + position[0] + 100 * i, 302 + position[1], 98, 98))
        renderPygameText(arial_font, screen, end_chars[i], (51 - arial_font.size(end_chars[i])[0] // 2 + position[0] + 100 * i, position[1] + 334))
    
    # Sets the pressed indicator to True to make the pressed button being read just one time
    numericKeyTouched = pressed[0]
    # Resets the last button ID identifier when none of the keys are being pressed
    # print(numericKeyId)
    if not numericKeyTouched:
        numericKeyId = -1
    return key

# FAV Keyboard Variables

favKeyAnimationTime = [time.time() for x in range(6)] # Animation time for numeric keyboard key
favKeyId = -1
favKeyTouched = False

def renderFavKeyboard(screen, position=(0, 0), press=False, animatePos = 6, opacity=1.0):
    global favKeyId;
    global favKeyTouched;
    global favKeyAnimationTime;
    global arial_font;
    pos = pg.mouse.get_pos()
    pressed = pg.mouse.get_pressed()
    key = -1
    if opacity > 1:
        opacity = 1
    elif opacity < 0:
        opacity = 0
    # print(pressed[pg.K_LEFT])
    # print(press)
    #pg.draw.rect(screen, (240, 240, 240), pg.rect.Rect(position[0], position[1], 302, 402))
    for i in range(6):
        iSin = math.sin(i * math.pi / 3 - math.pi / 6 * 5)
        iCos = math.cos(i * math.pi / 3 - math.pi / 6 * 5)
        if pressed[0]:
            #if pos[0] >= position[0] + iCos * 124 + hexagonCoords[4][0] * 64 and pos[1] >= position[1] + iSin * 124 + hexagonCoords[4][1] * 64 and pos[0] < position[0] + iCos * 124 + hexagonCoords[1][0] * 64 and pos[1] < position[1] + iSin * 124 + hexagonCoords[1][1] * 64:
            if isInsideAHex((position[0] + iCos * 124, position[1] + iSin * 124), (64, 64), pos):
                # Avoids mistaken pressed keys affect the first key pressed
                if favKeyId == -1:
                    favKeyId = i
                if favKeyId == i:
                    key = i + 1
                    favKeyAnimationTime[i] = time.time()
                elif favKeyId != -1:
                    key = favKeyId + 1
                #Changes the color acording the "animationPos", used for "initilization animations"
        if i > animatePos:
            favKeyAnimationTime[i] = time.time()
        #pg.draw.rect(screen, (200 - (key == (i - 1)) * 100, 200 - (key == (i - 1)) * 100, 200 - (key == (i - 1)) * 100), pg.rect.Rect(position[0] + (i % 3) * 100 + 2, position[1] + (i // 3) * 100 + 2, 98, 98))
        deltaAnimation = time.time() - favKeyAnimationTime[i]
        if deltaAnimation < .4:
            pg.draw.polygon(screen, [100 + 250 * deltaAnimation * opacity + 155 * (1.0 - opacity) for x in range(3)], [(point[0] * 64 + position[0] + iCos * 124, point[1] * 64 + position[1] + iSin * 124) for point in hexagonCoords])
            # pg.draw.rect(screen, [100 + 250 * deltaAnimation for x in range(3)], pg.rect.Rect(position[0] + (i % 3) * 100 + 2, position[1] + (i // 3) * 100 + 2, 98, 98))
        else:
            # pg.draw.rect(screen, (200, 200, 200), pg.rect.Rect(position[0] + (i % 3) * 100 + 2, position[1] + (i // 3) * 100 + 2, 98, 98))
            pg.draw.polygon(screen, (255 - 55 * opacity, 255 - 55 * opacity, 255 - 55 * opacity), [(point[0] * 64 + position[0] + iCos * 124, point[1] * 64 + position[1] + iSin * 124) for point in hexagonCoords])
        # print(int(255 - opacity * 255))
        renderPygameText(arial_font, screen, str(i+1), (-arial_font.size(str(i+1))[0] // 2 + position[0] + iCos * 124, position[1] + iSin * 124 - 16), (int(255 - opacity * 255), int(255 - opacity * 255), int(255 - opacity * 255)))
    
    # Sets the pressed indicator to True to make the pressed button being read just one time
    favKeyTouched = pressed[0]
    # Resets the last button ID identifier when none of the keys are being pressed
    # print(favKeyId)
    if not favKeyTouched:
        favKeyId = -1
    return key

# Numeric FAV Keyboard Variables

numericFavKeyAnimationTime = [time.time() for x in range(12)] # Animation time for numeric keyboard key
numericFavKeyId = -1
numericFavKeyTouched = False


def renderNumericFavKeyboard(screen, position=(0, 0), press=False):
    global numericFavKeyId;
    global numericFavKeyTouched
    global numericFavKeyAnimationTime;
    global arial_font;
    pos = pg.mouse.get_pos()
    pressed = pg.mouse.get_pressed()
    # Keeps the key stored until the user releases the screen
    if numericFavKeyId >= 0 and numericFavKeyId < 9:
        key = numericFavKeyId + 1
    elif numericFavKeyId == 9:
        key = 10
    elif numericFavKeyId == 10:
        key = 0
    elif numericFavKeyId == 11:
        key = 11
    else:
        key = -1
    
    if not pressed[0]:
        if key == -1:
            for i in range(10):
                if pg.key.get_pressed()[48 + i]:
                    key = i
                    numericFavKeyId = i + 10 * (i == 0)
    

    # print(pressed[pg.K_LEFT])
    # print(press)
    # pg.draw.rect(screen, (240, 240, 240), pg.rect.Rect(position[0], position[1], 302, 402))
    
    for i in range(9):
        if pressed[0]:
            if isInsideAHex((position[0] + 49 + (i % 3) * 100, position[1] + 49 + (i // 3) * 100 - (i % 3 == 1) * 49), (49, 49), pos):
                # Avoids mistaken pressed keys affect the first key pressed
                if numericFavKeyId == -1:
                    numericFavKeyId = i
                if numericFavKeyId == i:
                    key = i + 1
                    numericFavKeyAnimationTime[i] = time.time()
                elif numericFavKeyId != -1:
                    key = numericFavKeyId + 1
        #pg.draw.rect(screen, (200 - (key == (i - 1)) * 100, 200 - (key == (i - 1)) * 100, 200 - (key == (i - 1)) * 100), pg.rect.Rect(position[0] + (i % 3) * 100 + 2, position[1] + (i // 3) * 100 + 2, 98, 98))
        deltaAnimation = time.time() - numericFavKeyAnimationTime[i]
        if deltaAnimation < .4:
            #pg.draw.rect(screen, [100 + 250 * deltaAnimation for x in range(3)], pg.rect.Rect(position[0] + (i % 3) * 100 + 2, position[1] + (i // 3) * 100 + 2, 98, 98))
            pg.draw.polygon(screen, [100 + 250 * deltaAnimation for x in range(3)], [(position[0] + 49 + (i % 3) * 100 + 49 * points[0], position[1] + 49 + (i // 3) * 100 - (i % 3 == 1) * 49 + 49 * points[1]) for points in hexagonCoords])
        else:
            pg.draw.polygon(screen, [200 for x in range(3)], [(position[0] + 49 + (i % 3) * 100 + 49 * points[0], position[1] + 49 + (i // 3) * 100 - (i % 3 == 1) * 49 + 49 * points[1]) for points in hexagonCoords])
        renderPygameText(arial_font, screen, str(i+1), (49 - arial_font.size(str(i+1))[0] // 2 + position[0] + (i % 3) * 100, position[1] + (i // 3) * 100 + 30 - (i % 3 == 1) * 49))
    end_chars = ["OK", "0", "←"] # Keys at the bottom ofthe numeric keyboard
    for i in range(3):
        if pressed[0]:
            #if pos[0] >= position[0] + i * 100 + 2 and pos[1] >= position[1] + 302 and pos[0] < position[0] + i * 100 + 100 and pos[1] < position[1] + 400:
            if isInsideAHex((position[0] + 49 + i * 100, position[1] + 351 - (i == 1) * 49), (49, 49), pos):
                # The verification made to avoid mistaken keys being considerated pressed
                if numericFavKeyId == -1:
                    numericFavKeyId = i + 9
                if numericFavKeyId == i + 9:
                    if i == 0:
                        key = 10
                    elif i == 1:
                        key = 0
                    else:
                        key = 11
                    numericFavKeyAnimationTime[i + 9] = time.time()
        deltaAnimation = time.time() - numericFavKeyAnimationTime[i + 9]
        if deltaAnimation < .4:
            #pg.draw.rect(screen, [100 + 250 * deltaAnimation for x in range(3)], pg.rect.Rect(2 + position[0] + 100 * i, 302 + position[1], 98, 98))
            pg.draw.polygon(screen, [100 + 250 * deltaAnimation for x in range(3)], [(position[0] + 49 + i * 100 + 49 * points[0], position[1] + 351 - (i == 1) * 49 + 49 * points[1]) for points in hexagonCoords])
        else:
            #pg.draw.rect(screen, (200, 200, 200), pg.rect.Rect(2 + position[0] + 100 * i, 302 + position[1], 98, 98))
            pg.draw.polygon(screen, (200, 200, 200), [(position[0] + 49 + i * 100 + 49 * points[0], position[1] + 351 - (i == 1) * 49 + 49 * points[1]) for points in hexagonCoords])
        renderPygameText(arial_font, screen, end_chars[i], (51 - arial_font.size(end_chars[i])[0] // 2 + position[0] + 100 * i, position[1] + 334 - (i == 1) * 49))
    
    # Sets the pressed indicator to True to make the pressed button being read just one time
    numericFavKeyTouched = pressed[0]
    # Resets the last button ID identifier when none of the keys are being pressed
    # print(numericFavKeyId)
    if not numericFavKeyTouched:
        numericFavKeyId = -1
    return key

# Alphanumeric Keyboard Variables

alphaKeyAnimationTime = [time.time() for x in range(80)] # Animation time for numeric keyboard key
alphaKeyId = -1
alphaKeyTouched = False
alphaKeyShift = False
lineKeys = ["qwertyuiop", "asdfghjkl", "zxcvbnm,."]

def renderAlphaKeyboard(screen, position=(0, 0), press=False):
    global numericKeyId;
    global numericKeyTouched
    global numericKeyAnimationTime;
    global arial_font;
    global lineKeys
    pos = pg.mouse.get_pos()
    pressed = pg.mouse.get_pressed()
    # Keeps the key stored until the user releases the screen
    key = numericKeyId
    
    pg.draw.rect(screen, (240, 240, 240), pg.rect.Rect(position[0], position[1], 800, 402))
    for i in range(len(lineKeys)):
        for j in range(len(lineKeys[i])):
            pg.draw.rect(screen, (200, 200, 200), pg.rect.Rect(position[0] + j * 600 / len(lineKeys[i]) + i * 10, position[1] + i * 38, 600 / len(lineKeys[i]) - 1, 36))
            renderPygameText(arial_font, screen, lineKeys[i][j], (position[0] + j * 600 / len(lineKeys[i]) + i * 10 + 5, position[1] + i * 38 + 2), (0, 0, 0))
    # print(pressed[pg.K_LEFT])
    # print(press)
    return key

# Alert variables

alerts = []
alertTime = time.time()

def alert(text, duration=5, color=(255, 0, 0)):
    global alertTime
    alerts.append([text, duration, color])
    alertTime = time.time()

def alertUpdate(screen):
    global alertTime
    global alerts
    if len(alerts): # Renders some alert if it exists
        if time.time() - alertTime < alerts[-1][1]: # Checks if it is still in time
            size = arial_font_alert.size(alerts[-1][0])
            pg.draw.polygon(screen, (0, 0, 40), ((284 - size[0] // 2, 512), (296 - size[0] // 2, 490), (304 + size[0] // 2, 490), (316 + size[0] // 2, 512), (304 + size[0] // 2, 532), (296 - size[0] // 2, 532)))
            renderPygameText(arial_font_alert, screen, alerts[-1][0], (300 - size[0] // 2, 490), alerts[-1][2])
        else:
            alertTime += alerts[-1][1]
            alerts.pop()
    

favNum = 0 # Selected FAV number.
payment_animation_time = time.time()

while not end_program:
    pressed = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            end_program = True;
        if event.type == pg.MOUSEBUTTONDOWN: # Read the mousebutton
            pressed = True
    # Render Interface
    #pressed = pg.key.get_pressed()
    # print(pressed[pg.K_LEFT])
    if interface == 0 and time.time() - screen_offset_animation_time >= 1: # Settings of interface 0 (select screen) when the animation of the screen ended
        favNum = -1
        inps.setValue(0, "")
    if screen_offset < 800: # Screen selector
        if time.time() - intro_animation_time < .8: # Animates the title at the start of the screen
            renderPygameText(arial_font, screen, "HolderComb", (300 - arial_font.size("HolderComb")[0] // 2 - (screen_offset - 64) * (screen_offset > 64), cubic_bezier(-64, -63, 16, 16, (time.time() - intro_animation_time) / .8)))
        else:
            renderPygameText(arial_font, screen, "HolderComb", (300 - arial_font.size("HolderComb")[0] // 2 - (screen_offset - 64) * (screen_offset > 64), 16))
        # Render titles
        if time.time() - intro_animation_time >= 1 and time.time() - intro_animation_time < 1.4:
            renderPygameText(arial_font, screen, "Selecione um compartimento", (300 - arial_font.size("Selecione um compartimento")[0] // 2 - (screen_offset - 32) * (screen_offset > 32), 60), [255 * (.4 - time.time() + intro_animation_time + 1) / .4 for x in range(3)])
        elif time.time() - intro_animation_time >= 1.4:
            renderPygameText(arial_font, screen, "Selecione um compartimento", (300 - arial_font.size("Selecione um compartimento")[0] // 2 - (screen_offset - 32) * (screen_offset > 32), 60))
            # renderNumericKeyboard(screen, (149, 400), pressed)
            # Animates the FAV keyboard
            enteredFav = 0 # The entered FAV number by user
            if time.time() - intro_animation_time < 3.9:
                enteredFav = renderFavKeyboard(screen, (300 - screen_offset, 612), pressed, (time.time() - intro_animation_time) * 4 - 9.6, (time.time() - intro_animation_time) - 1.4)
            else:
                enteredFav = renderFavKeyboard(screen, (300 - screen_offset, 612), pressed, 6)
        # Controll of FAV
        if pressed and enteredFav > 0:
            favNum = enteredFav
            print(f"Favo selecionado: {favNum}")
            interface = 1
            screen_offset_animation_time = time.time()
    if screen_offset >=400 and screen_offset < 1200 and (last_screen_offset == 800 or interface == 1): # Screen of password rederization
        renderPygameText(arial_font_title, screen, f"Favo {favNum}", (300 - arial_font.size(f"Favo {favNum}")[0] // 2 - (screen_offset - 800), 16))
        renderPygameText(arial_font, screen, "Digite sua senha", (300 - arial_font.size("Digite sua senha")[0] // 2 - (screen_offset - 800), 265))
        renderPygameText(arial_font_small, screen, "< Voltar", (16 - (screen_offset - 800), 16), (128,118, 0))
        inps.setPosition(0, [225 - (screen_offset - 800), 315])
        inps.setPosition(1, (10 - screen_offset + 1600, 315))
        if inps.render(screen): # Gets if "OK" was pressed
            if len(inps.getValue(0)) >= 4:
                if slot[favNum - 1]: # FAV is locked
                    if inps.getValue(0) == str(passwords[favNum - 1]): # Correct password
                        slot[favNum - 1] = False
                        print(f"Desbloqueado slot {favNum}")
                        interface = 2
                        payment_animation_time = time.time()
                        screen_offset_animation_time = time.time()
                        inps.focus(-1)
                    else:
                        alert("Senha incorreta", 2, (255, 0, 0))
                else: # FAV is unlocked
                    
                    slot[favNum - 1] = True
                    passwords[favNum - 1] = int(inps.getValue(0))
                    start_time[favNum - 1] = time.time()
                    print(f"Registrado slot {favNum}")
                    interface = 0
                    screen_offset_animation_time = time.time()
                    inps.focus(-1)

            elif len(inps.getValue(0)) > 0:
                alert("A senha deve conter, pelo menos, quatro dígitos", 5, (250, 250, 250))
            elif inps.getValue(0) == "" or (pg.mouse.get_pos()[0] < arial_font_small.size("< Voltar")[0] + 16 and pg.mouse.get_pos()[1] < arial_font_small.size("< Voltar")[1] + 16 and pressed):
                interface = 0
                screen_offset_animation_time = time.time()
                inps.focus(-1)
    if screen_offset > 1200 and (last_screen_offset == 1600 or interface == 2): # Payment screen
        if time.time() - payment_animation_time >= 1.0 and time.time() - payment_animation_time < 1.8: # Animates the title at the start of the screen
            renderPygameText(arial_font_title, screen, "Pagamento", (300 - arial_font_title.size("Pagamento")[0] // 2 - (screen_offset - 1600), cubic_bezier(-64, -63, 16, 16, (time.time() - payment_animation_time - 1) / .8)))
        elif time.time() - payment_animation_time >= 1.8:
            renderPygameText(arial_font_title, screen, "Pagamento", (300 - arial_font_title.size("Pagamento")[0] // 2 - (screen_offset - 1600), 16))
        if time.time() - payment_animation_time >= 1 and time.time() - intro_animation_time < 1.4:
            renderPygameText(arial_font, screen, "Digite o seu e-mail para realizar o pagamento", (300 - arial_font.size("Digite o seu e-mail para realizar o pagamento")[0] // 2 - (screen_offset - 1600), 265), [255 * (.4 - time.time() + payment_animation_time + 1) / .4 for x in range(3)])
        elif time.time() - payment_animation_time >= 1.4:
            renderPygameText(arial_font, screen, "Digite o seu e-mail para realizar o pagamento", (300 - arial_font.size("Digite o seu e-mail para realizar o pagamento")[0] // 2 - (screen_offset - 1600), 265), (0, 0, 0))
        if time.time() - payment_animation_time > 300 and interface == 2: # Uses the same time as used in animation to come back to title screen when the user gives no command for a while. It doesn't cofirms any payment
            interface = -1
            intro_animation_time = time.time()
            screen_offset_animation_time = time.time()
        inps.setPosition(0, [225 - (screen_offset - 800), 315])
        inps.setPosition(1, (10 - screen_offset + 1600, 315))
        if inps.render(screen): # When the e-mail is entered
            interface = 3
            screen_offset_animation_time = time.time()
        if interface == 2:
            inps.focus(1)

        

    # Control of screen offset
    #if interface == 1 and time.time() - screen_offset_animation_time < 1:
    #    screen_offset = int(cubic_bezier(last_screen_offset, last_screen_offset + 10, 790, 800, time.time() - screen_offset_animation_time))
    if interface >= 0: # Checks if it is to do regular animation or "return animation"
        if time.time() - screen_offset_animation_time < 1:
            screen_offset = int(cubic_bezier(last_screen_offset, last_screen_offset + 10, interface * 800 - 10, interface * 800, time.time() - screen_offset_animation_time)) # Animates the screen
        if time.time() - screen_offset_animation_time >= 1:
            last_screen_offset = interface * 800
            screen_offset = last_screen_offset
    else: # Animates the "return animation" (the animation of going directly to the main screen)
        if time.time() - screen_offset_animation_time < 1:
            screen_offset = int(cubic_bezier(last_screen_offset, last_screen_offset + 10, (last_screen_offset - 800) * 800 - 10, last_screen_offset - 800, time.time() - screen_offset_animation_time)) # Animates the screen
        if time.time() - screen_offset_animation_time >= 1:
            interface = 0
            last_screen_offset = interface * 800
            screen_offset = last_screen_offset
        intro_animation_time = time.time()
    # Update alerts
    alertUpdate(screen)
    # Update display
    pg.display.update()
    pgClock.tick(60)
    screen.fill((255, 255, 255))

'''
while True:
    #Apenas a demonstração se tá ocupado ou livre
    if slot1 == True:
        str1 = "1 - Ocupado"
    else:
        str1 = "1 - Livre  "
        
    if slot2 == True:
        str2 = "2 - Ocupado"
    else:
        str2 = "2 - Livre  "
        
    if slot3 == True:
        str3 = "3 - Ocupado"
    else:
        str3 = "3 - Livre  "
        
    if slot4 == True:
        str4 = "4 - Ocupado"
    else:
        str4 = "4 - Livre  "
        
    if slot5 == True:
        str5 = "5 - Ocupado"
    else:
        str5 = "5 - Livre  "
        
    if slot6 == True:
        str6 = "6 - Ocupado"
    else:
        str6 = "6 - Livre  "
    x = "Escolha seu slot:"    
    print(f"{x:^20}")
    print(f"  {str1}           {str4}")
    print(f"{str2}               {str5}")
    print(f"  {str3}           {str6}")

    aux = int(input())
    #A partir daqui *define* se o ármario tá ocupado ou livre
    #Também define as senhas
    if aux == 1:
        if slot1 == True:
            tentativa = input("Coloque sua senha: ")
            if tentativa == senha_slot1:
                print("Aberto!")
                slot1 = False
                n = slot1
                end1 = contador(n)
                print(calculoValor(start1,end1))
                time.sleep(2)
            elif tentativa == "d09809800909": #Um exemplo de caso esqueça a senha (Ficaria na mão de um segurança da UnB)
                print("Aberto!")
                time.sleep(2)
                slot1 = False
            else:
                print("Senha inválida")
                time.sleep(2)
        else:    
            while True:
                senha = input('Cadastre uma senha: ')
                if senha != "":
                    senha_slot1 = senha
                    print("Senha cadastrada com sucesso!")
                    n = slot1
                    start1 = contador(n)
                    time.sleep(2)
                    break
                else:
                    print("Senha inválida")
                    time.sleep(2)
            senha = ''
            slot1 = True
            
    elif aux == 2:
        if slot2 == True:
            tentativa = input("Coloque sua senha: ")
            if tentativa == senha_slot2:
                print("Aberto!")
                slot2 = False
                n = slot2
                end2 = contador(n)
                print(calculoValor(start2,end2))
                time.sleep(2)
               
            else:
                print("Senha inválida")
                time.sleep(2)
        else:   
            while True:
                senha = input('Cadastre uma senha: ')
                if senha != "":
                    senha_slot2 = senha
                    print("Senha cadastrada com sucesso!")
                    n = slot2
                    start2 = contador(n)
                    time.sleep(2)
                    break
                else:
                    print("Senha inválida")
                    time.sleep(2)
            senha = ''
            slot2 = True
    elif aux == 3:
        if slot3 == True:
            tentativa = input("Coloque sua senha: ")
            if tentativa == senha_slot3:
                print("Aberto!")
                slot3 = False
                n = slot3
                end3 = contador(n)
                print(calculoValor(start3,end3))
                time.sleep(2)
            else:
                print("Senha inválida")
                time.sleep(2)
        else:    
            while True:
                senha = input('Cadastre uma senha: ')
                if senha != "":
                    senha_slot3 = senha
                    print("Senha cadastrada com sucesso!")
                    n = slot3
                    start3 = contador(n)
                    time.sleep(2)
                    break
                else:
                    print("Senha inválida")
                    time.sleep(2)
            senha = ''
            slot3 = True
    elif aux == 4:
        if slot4 == True:
            tentativa = input("Coloque sua senha: ")
            if tentativa == senha_slot4:
                print("Aberto!")
                slot4 = False
                n = slot4
                end4 = contador(n)
                print(calculoValor(start4,end4))
                time.sleep(2)            
            else:
                print("Senha inválida")
                time.sleep(2)
        else:    
            while True:
                senha = input('Cadastre uma senha: ')
                if senha != "":
                    senha_slot4 = senha
                    print("Senha cadastrada com sucesso!")
                    n = slot4
                    start4 = contador(n)
                    time.sleep(2)
                    break
                else:
                    print("Senha inválida")
                    time.sleep(2)
            senha = ''
            slot4 = True
    elif aux == 5:
        if slot5 == True:
            tentativa = input("Coloque sua senha: ")
            if tentativa == senha_slot5:
                print("Aberto!")
                slot5 = False
                n = slot5
                end5 = contador(n)
                print(calculoValor(start5,end5))
                time.sleep(2)
            else:
                print("Senha inválida")
                time.sleep(2)
        else:    
            while True:
                senha = input('Cadastre uma senha: ')
                if senha != "":
                    senha_slot5 = senha
                    print("Senha cadastrada com sucesso!")
                    n = slot5
                    start5 = contador(n)
                    time.sleep(2)
                    break
                else:
                    print("Senha inválida")
                    time.sleep(2)
            senha = ''
            slot5 = True
    elif aux == 6:
        if slot6 == True:
            tentativa = input("Coloque sua senha: ")
            if tentativa == senha_slot6:
                print("Aberto!")
                slot6 = False
                n = slot6
                end6 = contador(n)
                print(calculoValor(start6,end6))
                time.sleep(2)
            else:
                print("Senha inválida")
                time.sleep(2)
        else:    
            while True:
                senha = input('Cadastre uma senha: ')
                if senha != "":
                    senha_slot6 = senha
                    print("Senha cadastrada com sucesso!")
                    n = slot6
                    start6 = contador(n)
                    time.sleep(2)
                    break
                else:
                    print("Senha inválida")
                    time.sleep(2)
            senha = ''
            slot6 = True
'''