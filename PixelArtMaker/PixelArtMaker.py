## Potential Expand Topics: Opening and saving images? More animations? Reiszing Canvases? Make code more efficient!!

import sys, pygame, random, enum, time, os, webcolors
from PIL import Image, ImageDraw
 
pygame.display.set_caption("Pixel Art Maker")                             
pygame.font.init()

CANVASSIZE = (500, 500)
defaultsize = [10, 10]

# Positioning Values
rightMenuSize = 160
topMenuSize = 50
borderSize = 6
displayOffset = 5
borderOffset = 6
gap = 10
menuSize = 119

def loadimage(path, dimensions, flip, flip2):

    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, dimensions)
    if flip:
        image = pygame.transform.flip(image, flip, flip2)
    return image

def read_colours_from_file(file_path):
    colours = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Assuming each line contains a color in text format (e.g., "red", "green", etc.)
                color = line.strip().lower().replace("\\", "")
                try:
                    test = pygame.Rect(0, 0, 0, 0)
                    pygame.draw.rect(SCREEN, color, test)
                    if color not in colours:
                        colours.append(color)
                except:
                    pass
    except:
        pass
    return colours

font = pygame.font.Font("Font/SourceCodePro-Regular.ttf", 15)
SCREEN_WIDTH = CANVASSIZE[0] + borderOffset + rightMenuSize
SCREEN_HEIGHT = CANVASSIZE[1] + borderOffset + topMenuSize + displayOffset

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mouse.set_visible(False)

colours_file_path = "palletes/colour-pallete-1.rtf"  # Specify the path to your text file
colours = read_colours_from_file(colours_file_path)

bucketimage = loadimage("images/bucket.png", (20, 20), False, False)
penimage = loadimage("images/pen.png", (20, 20), True, True)
eraserimage = loadimage("images/eraser.png", (20, 20), False, False)
pickerimage = loadimage("images/picker.png", (20, 20), True, False)
cursorimage = loadimage("images/cursor.png", (35, 35), False, False)
logo = loadimage("images/logo.png", (100, 100), False, False)


pygame.display.set_icon(logo)


def create_image(grid, colors):

    cell_size = 50
    width = len(grid[0]) * cell_size
    height = len(grid) * cell_size
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            color_index = grid[i][j]
            if color_index != 0:
                color = colors[color_index - 1]  # Adjust index to match colors sheet
                draw.rectangle(
                    [(j * cell_size, i * cell_size), ((j + 1) * cell_size, (i + 1) * cell_size)],
                    fill=color,
                )
    return image

def userInputTaker(canvas, Default):

    continuebox = pygame.Rect(SCREEN_WIDTH - 145, 10, 130, 30)
    continueboxborder = pygame.Rect(continuebox.x-1, continuebox.y-1, continuebox.width + 2, continuebox.height + 2)
    sliderX = Slider([25, 20], 5, 50, 200)
    sliderY = Slider([280, 20], 5, 50, 200)
    sliders = [sliderX, sliderY]

    goback = False
    select = True
    if Default == False:
        while select:

            SCREEN.fill("dark grey")
            canvas.drawCanvas()
            canvas.penselect.run(canvas.cursor)
            canvas.colourbox.run(canvas.cursor)
            rect = canvas.menuselect.undobox
            pygame.draw.rect(SCREEN, "dark grey", rect)
            pygame.draw.rect(SCREEN, "dark grey", continuebox)
            pygame.draw.rect(SCREEN, "black", continueboxborder, 2)
            border = pygame.Rect(rect.x - 2, rect.y - 2, rect.width + 2, rect.height + 2)
            pygame.draw.rect(SCREEN, "black", border, 1)
            text1 = font.render("Undo", True, (0, 0, 0))  # Black text
            text2 = font.render("Create", True, (0, 0, 0))
            SCREEN.blit(text1, (rect.center[0] - text1.get_width()/2, rect.y + 3))
            SCREEN.blit(text2, (continuebox.center[0] - text2.get_width()/2, continuebox.y + 4))
            for slider in sliders:
                slider.run()
            canvas.cursor.run(False)            
            pygame.display.update()
            if continuebox.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    select = False
                    pygame.draw.rect(SCREEN, "green", continueboxborder, 2)
                    pygame.display.update()
                    time.sleep(0.1)
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                select = False
                goback = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    select = False
                    sys.exit()
    if Default:
        size = [defaultsize[0], defaultsize[1]]
    else:
        size = [sliderX.size, sliderY.size]

    if not goback:
        cellSize = int(min(CANVASSIZE[0] / size[0], (CANVASSIZE[1] //size[1])))
        offsetX = (CANVASSIZE[0] - cellSize * size[0]) / 2 + borderOffset/2 
        offsetY = (CANVASSIZE[1] - cellSize * size[1]) /2 + borderOffset/2 + 49
        return size, cellSize, [offsetX, offsetY], goback
    else:
        return canvas.Size, canvas.cellSize, [canvas.offsetX, canvas.offsetY], goback

class Slider():

    def __init__(self, pos, minsize, maxsize, width):

        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.slider_x = self.pos.x
        self.slider_y = self.pos.y
        self.slider_rect = pygame.Rect(self.slider_x, self.slider_y, width, 10)
        self.controller = pygame.Rect(self.slider_rect.x, self.slider_y - 3, self.slider_rect.height + 6, self.slider_rect.height + 6)
        self.dragging = False
        self.min_size = minsize
        self.max_size = maxsize
        self.size = int((maxsize-minsize)/2)

    def run(self):

        pygame.draw.rect(SCREEN, "dark grey", self.slider_rect)
        pygame.draw.rect(SCREEN, "light grey", self.controller)
        border = pygame.Rect(self.controller.x - 1, self.controller.y - 1, self.controller.width + 2, self.controller.height + 2)
        pygame.draw.rect(SCREEN, "black", border, 1)
        sizenum = font.render(str(self.size), (0, 0, 0), True)
        SCREEN.blit(sizenum, (self.slider_rect.x + self.slider_rect.width + 8, self.pos.y - 5))
        self.updateCursorSize()

    def updateCursorSize(self):

        if pygame.mouse.get_pressed()[0]:
            if self.controller.collidepoint(pygame.mouse.get_pos()) or self.slider_rect.collidepoint(pygame.mouse.get_pos()):
                self.dragging = True
        if pygame.mouse.get_pressed()[0] == False:
            self.dragging = False
        if self.dragging:
            self.controller.x =  max(min(pygame.mouse.get_pos()[0], self.slider_rect.x + self.slider_rect.width), self.slider_rect.x)

        intervals = []
        gap = ( self.slider_rect.width - self.controller.width/2 ) / self.max_size
        for i in range(0, int(self.max_size)):
            intervals.append(int(self.slider_rect.x + gap * i))
            
        self.controller.x = min(intervals, key=lambda x: abs(x - self.controller.x))
        self.size = intervals.index(self.controller.x) + self.min_size

class BrushType(enum.Enum):

    NORMAL = 1
    FILL = 2
    ERASER = 3
    PICKER = 4

class ColourBox():

    def __init__(self):

        self.coloursPerRow = 4
        self.boxSize = (rightMenuSize - gap*2) / self.coloursPerRow
        if len(colours) % 4 == 0:
            self.addon = (len(colours) // 4)
        else:
            self.addon = (len(colours) // 4+1)
        self.box = pygame.Rect(SCREEN_WIDTH - rightMenuSize + gap, 40 - borderSize/2 + 120, rightMenuSize - gap*2, self.boxSize * self.addon)
        self.border = pygame.Rect(self.box.x - borderSize/2, self.box.y - borderSize/2, self.box.width + borderSize, self.box.height + borderSize)
        self.colours = {}
        self.lastmovepos = 0
        self.setUp()

    def setUp(self):

        for colour in colours:
            self.colours.update({colour : None})
        i = 0
        self.colourGrid = []
        while i < len(colours):
            row = []
            for j in range(self.coloursPerRow):
                try:
                    row.append(colours[i])
                    i += 1
                except:
                    row.append("empty")
                    i += 1
            self.colourGrid.append(row)

    def drawBoxes(self, cursor):

        pygame.draw.rect(SCREEN, "dark grey", self.box)
        pygame.draw.rect(SCREEN, "black", self.border, 3)
        startPos = self.box
        row = 0
        col = 0
        for colour in self.colours:
            colourbox = pygame.Rect(startPos.x + row * self.boxSize, startPos.y + col * self.boxSize, self.boxSize, self.boxSize)
            self.colours[colour] = colourbox
            pygame.draw.rect(SCREEN, colour, colourbox)
            if cursor.selectedColour == colour:
                selected = pygame.Rect(startPos.x + row * self.boxSize-1, startPos.y + col * self.boxSize-1, self.boxSize+2, self.boxSize+2)
                if colour == "red":
                    pygame.draw.rect(SCREEN, "dark red", colourbox, 2)
                else:
                    pygame.draw.rect(SCREEN, "red", colourbox, 2)
            if row < self.coloursPerRow - 1:
                row += 1
            else:
                row = 0
                col += 1

    def movePosition(self, cursor):
            
        keys = pygame.key.get_pressed()
        for i, row in enumerate(self.colourGrid):
            try:
                y = row.index(cursor.selectedColour)
                if y != None:
                    x = i
            except:
                pass
        colourpos = pygame.math.Vector2(x, y)
        if keys[pygame.K_DOWN]:
            if int(colourpos.x) + 1 < len(self.colourGrid):
                if self.colourGrid[int(colourpos.x + 1)][int(colourpos.y)] != "empty":
                    colourpos.x += 1
        elif keys[pygame.K_UP]:
            if int(colourpos.x) > 0:
                colourpos.x -= 1   
        elif keys[pygame.K_RIGHT]:
            if int(colourpos.y) + 1 < int(self.coloursPerRow):
                if self.colourGrid[int(colourpos.x)][int(colourpos.y + 1)] != "empty":
                    colourpos.y += 1 
        elif keys[pygame.K_LEFT]:
            if int(colourpos.y) > 0:
                colourpos.y -= 1
        self.selectedColour = self.colourGrid[int(colourpos.x)][int(colourpos.y)]
        cursor.selectedColour = self.selectedColour
                    
    def run(self, cursor):
        
        current_time = pygame.time.get_ticks()
        if current_time - self.lastmovepos > 100:
            self.lastmovepos = pygame.time.get_ticks()
            self.movePosition(cursor)
        self.drawBoxes(cursor)

class PenSelect():

    def __init__(self, size):

        self.itemsnum = 0
        self.settings = {}
        self.cursor_size = 1
        self.max_size = 12
        self.setUp(size)
        self.dragging = False


    def setUp(self, size):

        for brush in BrushType:
            self.settings.update({brush : None})
        self.itemsnum = len(self.settings.values()) + 1
        self.boxSize = ((rightMenuSize - gap*2) / self.itemsnum)
        self.start = pygame.Rect(SCREEN_WIDTH - rightMenuSize + gap, 50 - borderSize/2 + gap, 0, 0)
        if size[0] != 0:
            self.slider = Slider([self.start.x, self.start.y + 60], 1, min(size[0], size[1]), rightMenuSize - gap*2)
        else:
            self.slider = Slider([self.start.x, self.start.y + 60], 1, 1, rightMenuSize - gap*2)

    def drawToolBar(self, cursor):

        startPos = self.start
        row = 0
        for setting in self.settings:
            settingbox = pygame.Rect(startPos.x + row * self.boxSize + gap*row, startPos.y + 12, self.boxSize, self.boxSize)
            self.settings[setting] = settingbox
            if cursor.setting == setting:
                pygame.draw.rect(SCREEN, "red", settingbox, 2)
            else:
                pygame.draw.rect(SCREEN, "black", settingbox, 1)
            row += 1
        diff = 4
        SCREEN.blit(penimage, (self.settings[BrushType.NORMAL].x + diff, self.settings[BrushType.NORMAL].y + diff))
        SCREEN.blit(bucketimage, (self.settings[BrushType.FILL].x + diff, self.settings[BrushType.FILL].y + diff))
        SCREEN.blit(eraserimage,(self.settings[BrushType.ERASER].x + diff, self.settings[BrushType.ERASER].y + diff))
        SCREEN.blit(pickerimage,(self.settings[BrushType.PICKER].x + diff, self.settings[BrushType.PICKER].y + diff))

    def run(self, cursor):

        self.slider.run()
        self.size = self.slider.size
        self.drawToolBar(cursor)


class MenuSelect():

    # New, Open, Save, Export, Flip, Rotate, Undo, Quit

    def __init__(self, canvas):

        self.canvas = canvas
        self.x_values = [canvas.toptoolbar.x + gap, canvas.toptoolbar.x + gap * 2 + menuSize,
                         canvas.toptoolbar.x + gap * 3 + 2 * menuSize,
                         canvas.toptoolbar.x + gap * 4 + 3 * menuSize,
                         canvas.toptoolbar.x + gap * 5 + 4 * menuSize]
        
        self.button_cooldown = 50  # Set the cooldown time in milliseconds (adjust as needed)
        self.last_button_press_time = {"flipx":0, "flipy":0, "rotate":0, "export":0, "new":0, "undo":0}
        self.undoReleased = True
        self.setUp()


    def setUp(self):

        canvas = self.canvas
        if canvas.Size[0] == canvas.Size[1]:
            menuSize = 120
            self.newbox = pygame.Rect(self.x_values[0], canvas.toptoolbar.y + gap/2, menuSize, canvas.toptoolbar.height - gap)
            self.exportbox = pygame.Rect(self.x_values[1] + gap/3, canvas.toptoolbar.y + gap/2, menuSize, canvas.toptoolbar.height - gap)
            self.fliphoirzontalbox = pygame.Rect(self.x_values[2] + gap/3, canvas.toptoolbar.y + gap/2, menuSize, canvas.toptoolbar.height - gap)
            self.flipverticalbox = pygame.Rect(self.x_values[3] + gap/3, canvas.toptoolbar.y + gap/2, menuSize, canvas.toptoolbar.height - gap)
            self.rotatebox = pygame.Rect(self.x_values[4] + gap/3, canvas.toptoolbar.y + gap/2, menuSize, canvas.toptoolbar.height - gap)
            self.undobox = pygame.Rect(self.x_values[4] - 6, SCREEN_HEIGHT - canvas.toptoolbar.height - 4, menuSize, canvas.toptoolbar.height - gap)
            self.boxes = [self.newbox, self.exportbox, self.fliphoirzontalbox, self.flipverticalbox, self.rotatebox, self.undobox]
            self.released = {"new":True, "export":True, "flipx":True, "flipy": True, "rotate": True, "undo":True}
            self.Names = ["New", "Export", "Flip X", "Flip Y", "Rotate", "Undo"]
    


        else:
            menuSize = 150
            for i in range(6):
                self.x_values.append(canvas.toptoolbar.x + gap*8 * i + i-1 * menuSize)
            self.newbox = pygame.Rect(self.x_values[0], canvas.toptoolbar.y + gap/2, menuSize, canvas.toptoolbar.height - gap)
            self.exportbox = pygame.Rect(self.x_values[1] + 25 + gap, canvas.toptoolbar.y + gap/2, menuSize, canvas.toptoolbar.height - gap)
            self.fliphoirzontalbox = pygame.Rect(self.x_values[2] + 50 + gap*2, canvas.toptoolbar.y + gap/2, menuSize, canvas.toptoolbar.height - gap)
            self.flipverticalbox = pygame.Rect(self.x_values[3] + 75 + gap*3, canvas.toptoolbar.y + gap/2, menuSize, canvas.toptoolbar.height - gap)
            self.undobox = pygame.Rect((canvas.toptoolbar.x + gap * 5 + 4 * 120) - 10, SCREEN_HEIGHT - canvas.toptoolbar.height - 4, 120, canvas.toptoolbar.height - gap)
            self.boxes = [self.newbox, self.exportbox, self.fliphoirzontalbox, self.flipverticalbox, self.undobox]
            self.released = {"new":True, "export":True, "flipx":True, "flipy": True, "undo":True}
            self.Names = ["New", "Export", "Flip X", "Flip Y", "Undo"]

        
    def drawBoxes(self):

        boxes = [[self.newbox, self.released.get("new")], [self.exportbox, self.released.get("export")],
                 [self.fliphoirzontalbox, self.released.get("flipx")], [self.flipverticalbox, self.released.get("flipy")]]

        if self.canvas.Size[0] == self.canvas.Size[1]:
            boxes.append([self.rotatebox, self.released.get("rotate")])

        boxes.append([self.undobox, self.released.get("undo")])

        for index, (rect, released) in enumerate(boxes):

            if released:
                 pygame.draw.rect(SCREEN, "dark grey", rect)
            else:
                pygame.draw.rect(SCREEN, (120, 120, 120), rect)
            border = pygame.Rect(rect.x - 2, rect.y - 2, rect.width + 2, rect.height + 2)
            pygame.draw.rect(SCREEN, "black", border, 1)
            text_surface = font.render(self.Names[index], True, (0, 0, 0))  # Black text
            SCREEN.blit(text_surface, (rect.center[0] - text_surface.get_width()/2, rect.y+3))


    def newBoxFunc(self, Pass):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_button_press_time["new"] >= self.button_cooldown or Pass:
            self.last_button_press_time["new"] = current_time
            if (self.newbox.collidepoint(pygame.mouse.get_pos()) or Pass):
                if (pygame.mouse.get_pressed()[0] or Pass):
                    if self.released["new"] or Pass:
                        if Pass:
                            size, cellSize, offsets, goback = userInputTaker(self.canvas, True) # return default values
                        else:
                            size, cellSize, offsets, goback = userInputTaker(self.canvas, False)
                        if not goback:
                            self.canvas.createCanvas(size, cellSize, offsets)
                            self.canvas.AddChange(None)
                        self.setUp()

                
    def rotateBoxFunc(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_button_press_time["rotate"] >= self.button_cooldown:
            self.last_button_press_time["rotate"] = current_time
            if self.rotatebox.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0] and self.released["rotate"]:
                    self.released["rotate"] = False
                    array_representation = self.canvas.gridRepresentation()                    
                    rotated_matrix = [list(row) for row in zip(*array_representation[::-1])]
                    self.canvas.AddChange(rotated_matrix)
                    self.canvas.loadGrid(rotated_matrix)

                    
    def flipHorizontalFunc(self):

        current_time = pygame.time.get_ticks()
        if current_time - self.last_button_press_time["flipx"] >= self.button_cooldown:
            self.last_button_press_time["flipx"] = current_time
            if self.fliphoirzontalbox.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0] and self.released["flipx"]:
                    self.released["flipx"] = False
                    array_representation = self.canvas.gridRepresentation()
                    flipped_matrix = [row[::-1] for row in array_representation]
                    self.canvas.AddChange(flipped_matrix)
                    self.canvas.loadGrid(flipped_matrix)

    def undoboxFunc(self):

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_button_press_time["undo"] >= self.button_cooldown:
            self.last_button_press_time["undo"] = current_time
            if self.undobox.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0] and self.released["undo"]:
                    self.released["undo"] = False
                    self.canvas.Undo()

            if (keys[pygame.K_LMETA] or keys[pygame.K_RMETA]) and keys[pygame.K_z] and self.undoReleased:
                self.canvas.Undo()
                self.undoReleased = False

        if not keys[pygame.K_z]:
            self.undoReleased = True
         

    def exportboxFunc(self):

        current_time = pygame.time.get_ticks()
        if current_time - self.last_button_press_time["export"] >= self.button_cooldown * 2:
            self.last_button_press_time["export"] = current_time
            if self.exportbox.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0] and self.released["export"]:
                    self.released["export"] = False
                    return True
                

    def flipVerticalFunc(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_button_press_time["flipy"] >= self.button_cooldown:
            self.last_button_press_time["flipy"] = current_time
            if self.flipverticalbox.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0] and self.released["flipy"]:
                    self.released["flipy"] = False
                    array_representation = self.canvas.gridRepresentation()
                    flipped_matrix = array_representation[::-1]
                    self.canvas.AddChange(flipped_matrix)
                    self.canvas.loadGrid(flipped_matrix)
                

    def draw(self):
        
        self.drawBoxes()

    def run(self):                

        self.drawBoxes()
        self.newBoxFunc(False)
        self.flipVerticalFunc()
        self.flipHorizontalFunc()
        try:
            self.rotateBoxFunc()
        except:
            pass
        self.undoboxFunc()
        if pygame.mouse.get_pressed()[0] == False:
            for i, (func, val) in enumerate(self.released.items()):
                self.released[func] = True
        

class Canvas():

    def __init__(self):

        self.Cells = pygame.sprite.Group()
        self.last_undo_time = 0
        self.undo_cooldown = 400
        self.createCanvas([0, 0], 0, [0, 0])
        self.State = 0
        self.previousStatesStack = [self.gridRepresentation()]
        self.colourbox = ColourBox()
        self.penselect = PenSelect(self.Size)

        
    def createCanvas(self, size, cellsize, offsets):

        self.Size = pygame.math.Vector2(size[0], size[1])
        self.Cells = pygame.sprite.Group()
        self.cellSize = cellsize
        self.offsetX = offsets[0]
        self.offsetY = offsets[1]
        self.border = pygame.Rect(self.offsetX - borderSize/2 + 1, self.offsetY - borderSize/2, self.cellSize * self.Size[0] + borderSize, self.cellSize * self.Size[1] + borderSize)

        for i in range(int(self.Size.x)):
            for j in range(int(self.Size.y)):
                color = "dark grey" if (i + j) % 2 == 0 else "light grey"
                self.Cells.add(Cell([i * self.cellSize + self.offsetX, j * self.cellSize + self.offsetY], color, self.cellSize))

        self.toptoolbar = pygame.Rect(gap/2, gap/2, SCREEN_WIDTH - gap, topMenuSize - gap)
        self.righttoolbar = pygame.Rect(SCREEN_WIDTH - rightMenuSize + gap/2, (self.toptoolbar.height+ 1.5*gap), rightMenuSize - gap, SCREEN_HEIGHT - self.toptoolbar.height - 24)
        self.State = 0
        self.previousStatesStack = [self.gridRepresentation()]
        self.penselect = PenSelect(self.Size)

        

    def drawCanvas(self):

        pygame.draw.rect(SCREEN, "black", self.border, 4)

        for cell in self.Cells:
            cell.display()

        pygame.draw.rect(SCREEN, "grey", self.righttoolbar)
        pygame.draw.rect(SCREEN, "grey", self.toptoolbar)


    def AddChange(self, grid):

        if grid == None:
            if self.previousStatesStack[self.State] != self.gridRepresentation():
                self.previousStatesStack.append(self.gridRepresentation())
                self.State += 1
        else:
            self.previousStatesStack.append(grid)
            self.State += 1


    def Undo(self):

        if self.State > 0:
            self.State -= 1
            self.loadGrid(self.previousStatesStack[self.State])
            self.previousStatesStack.pop()


    def loadGrid(self, grid):

        for cell in self.Cells:
            cell_pos = [int(int(cell.rect.x - self.offsetX)/self.cellSize), int(int(cell.rect.y - self.offsetY)/self.cellSize)]
            if grid[cell_pos[1]][cell_pos[0]] == 0:
                cell.activated = False
                cell.colour = cell.default_colour
            else:
                cell.activated = True
                cell.colour = colours[grid[cell_pos[1]][cell_pos[0]] - 1]
                

    def fetchCell(self, pos, size):

        startcell = None
        for cell in self.Cells:
            if cell.rect.collidepoint(pos):
                startcell = cell
        cells = []
        if startcell != None:
            collider = pygame.Rect(startcell.rect.x-int(size/2), startcell.rect.y-int(size/2), size, size)
            for cell in self.Cells:
                if cell.rect.colliderect(collider):
                    cells.append(cell)
        return cells


    def pickColour(self, pos):

        if self.getCellAtPosition(pos).activated:
            return self.getCellAtPosition(pos).colour
        else:
            return None

    def fetchColour(self, pos):

        for colour, rect in self.colourbox.colours.items():
            if rect.collidepoint(pos):
                return colour

    def fetchSetting(self, pos):

        for i, pen in enumerate(self.penselect.settings.keys()):
            if pygame.key.get_pressed()[pygame.K_0 + i + 1]:
                List = list(self.penselect.settings.keys())
                return BrushType(List[i])
        try:
            for pen, rect in self.penselect.settings.items():
                if rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                    List = list(self.penselect.settings.keys())
                    index = List.index(pen) + 1
                    return BrushType(index)
        except:
            return None

    def getCellAtPosition(self, position):

        for cell in self.Cells:
            if cell.rect.collidepoint(position):
                return cell
        return None


    def gridRepresentation(self):

        grid = []
        if (self.Size.x * self.Size.y) > 0:

            for i in range(int(self.Size.y)):
                x = []
                for j in range(int(self.Size.x)):
                    x.append(0)
                grid.append(x)

            for cell in self.Cells:
                x = int((cell.rect.x - self.offsetX)/self.cellSize)
                y = int((cell.rect.y - self.offsetY)/self.cellSize) 

                if cell.activated:
                    grid[y][x] = colours.index(cell.colour)+1
                else:
                    grid[y][x] = 0
        
        return grid

    def fillCells(self, pos, new_colour):

        startcell = self.getCellAtPosition(pos)
        grid = self.gridRepresentation()
        changed_cells = []
        if startcell != None:
            stack =[startcell]
            if startcell.activated == False:
                original_colour = 0
            else:
                original_colour = colours.index(startcell.colour)+1
            if original_colour != colours.index(new_colour)+1:
                while stack:
                    current_cell = stack.pop()
                    
                    if current_cell.activated:
                        c = colours.index(current_cell.colour) + 1
                    else:
                        c = 0
                    if c == original_colour:
                        current_cell.colour = new_colour
                        current_cell.activated = True
                        changed_cells.append(current_cell)
                        neighbors = self.getNeighbors(current_cell)
                        stack.extend(neighbors)
                                   
    def getNeighbors(self, cell):

        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            neighbor_pos = (cell.rect.x + dx * self.cellSize, cell.rect.y + dy * self.cellSize)
            for c in self.Cells:
                if c.rect.collidepoint(neighbor_pos):
                    neighbors.append(c)
        return neighbors


    def fetchPenSize(self):
        try:
            return self.penselect.size
        except:
            return 1;

    def run(self, cursor):

        self.drawCanvas()
        self.colourbox.run(cursor)
        self.penselect.run(cursor)
        

class Cell(pygame.sprite.Sprite):

    def __init__(self, pos, default, size):

        super().__init__()

        self.image = pygame.Surface((size, size))  # Adjust size as needed
        self.image.fill((255, 255, 255))  # White color for now
        self.rect = self.image.get_rect(topleft=pos)
        self.activated = False
        self.default_colour = default
        self.colour = self.default_colour

    def display(self):

        if self.activated:
            pygame.draw.rect(SCREEN, self.colour, self.rect)
        else:
            pygame.draw.rect(SCREEN, self.default_colour, self.rect)
    
class Cursor():

    def __init__(self, canvas):

        self.canvas = canvas
        self.pos = pygame.math.Vector2(0, 0)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.canvas.cellSize, self.canvas.cellSize)
        self.selectedColour = "black" # default brush colour
        self.setting = BrushType.NORMAL
        self.size = 1
        self.last_button_press_time = 0
        self.drawing = False
        self.picked = False
        self.prev = False

    def drawCursor(self, Editing):

        self.size = (self.canvas.fetchPenSize() * self.canvas.cellSize) - self.canvas.cellSize + 1
        mouse_pos = pygame.mouse.get_pos()
        cells = self.canvas.fetchCell(mouse_pos, self.size)
        centrecell = self.canvas.getCellAtPosition(mouse_pos)

        if len(cells) > 0 and Editing:
            
            if self.setting == BrushType.ERASER:
                pos = (min(cell.rect.x for cell in cells), min(cell.rect.y for cell in cells))
                size = (max(cell.rect.x for cell in cells) - min(cell.rect.x for cell in cells))
                rect = pygame.Rect(pos[0], pos[1], size + self.canvas.cellSize, size + self.canvas.cellSize)
                newcol = False
                colour = "white"
                for cell in cells:
                    if cell.colour == "white":
                        colour = "black"                
                pygame.draw.rect(SCREEN, colour, rect, 2)
                SCREEN.blit(eraserimage, (mouse_pos[0] - gap - 7, mouse_pos[1] - gap - 7))

            elif self.setting == BrushType.PICKER and not self.picked:
                rect = pygame.Rect(centrecell.rect.x, centrecell.rect.y, self.canvas.cellSize, self.canvas.cellSize)
                if centrecell.colour != "white":
                    pygame.draw.rect(SCREEN, "white", centrecell, 1)
                else:
                    pygame.draw.rect(SCREEN, "black", centrecell, 1)
                SCREEN.blit(pickerimage, (mouse_pos[0] - gap - 7, mouse_pos[1] - gap - 7))                    
                
            elif self.setting == BrushType.FILL:
                rect = pygame.Rect(centrecell.rect.x, centrecell.rect.y, self.canvas.cellSize, self.canvas.cellSize)
                if centrecell.colour != "white":
                    pygame.draw.rect(SCREEN, "white", centrecell, 1)
                else:
                    pygame.draw.rect(SCREEN, "black", centrecell, 1)
                SCREEN.blit(bucketimage, (mouse_pos[0] - gap - 7, mouse_pos[1] - gap - 7))
                
            elif self.setting == BrushType.NORMAL:

                pos = (min(cell.rect.x for cell in cells), min(cell.rect.y for cell in cells))
                size = (max(cell.rect.x for cell in cells) - min(cell.rect.x for cell in cells))
                rect = pygame.Rect(pos[0], pos[1], size + self.canvas.cellSize, size + self.canvas.cellSize)
                pygame.draw.rect(SCREEN, self.selectedColour, rect)
                border = pygame.Rect(rect.x - 1, rect.y - 1, 2, 2)
                pygame.draw.rect(SCREEN, "white", border, 4)
                SCREEN.blit(penimage, (mouse_pos[0] - gap - 7, mouse_pos[1] - gap - 7))
        else:
            if pygame.mouse.get_focused():
                SCREEN.blit(cursorimage, (mouse_pos[0], mouse_pos[1]))

    def updatePos(self):

        mouse_pos = pygame.mouse.get_pos()
        self.pos = pygame.math.Vector2(mouse_pos[0], mouse_pos[1])
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.canvas.cellSize, self.canvas.cellSize)
        self.rect.center = self.pos

    def checkForClick(self, Editing):
        
        self.drawing = False
        if self.canvas.fetchSetting(self.pos) != None:
            self.setting = self.canvas.fetchSetting(self.pos)

        if self.setting == BrushType.PICKER and pygame.mouse.get_pressed()[0] == False and self.picked:
            self.setting = BrushType.NORMAL
            self.picked = False

        
        if pygame.mouse.get_pressed()[0]:
            self.drawing = True
            if self.canvas.border.collidepoint(pygame.mouse.get_pos()) and Editing:
                
                if self.setting == BrushType.FILL:
                    self.canvas.fillCells(self.pos, self.selectedColour)
                    
                elif self.setting == BrushType.NORMAL:
                    cells = self.canvas.fetchCell(self.pos, self.size)
                    if cells != None and len(cells) != 0:
                        for cell in cells:
                            cell.colour = self.selectedColour
                            cell.activated = True

                elif self.setting == BrushType.PICKER:
                    colour = self.canvas.pickColour(self.pos)
                    if colour != None:
                        self.selectedColour = colour
                        self.canvas.colourbox.selectedColour = colour
                        self.picked = True

                elif self.setting == BrushType.ERASER:
                    cells = self.canvas.fetchCell(self.pos, self.size)
                    if cells != None and len(cells) != 0:
                        for cell in cells:
                            cell.colour = cell.default_colour
                            cell.activated = False
        else:
            self.drawing == False

        if pygame.mouse.get_pressed()[0]:
            if self.canvas.righttoolbar.collidepoint(pygame.mouse.get_pos()):
                colour = self.canvas.fetchColour(self.pos)
                prev = self.setting
                if self.setting == None:
                    self.setting = prev
                if colour != None:
                    self.selectedColour = colour
        
        if self.prev and self.drawing == False:
            self.canvas.AddChange(None)

        self.prev = self.drawing

    def run(self, Editing):

        self.checkForClick(Editing)
        self.drawCursor(Editing)
        self.updatePos()


class Simulation():

    def __init__(self):

        self.Canvas = Canvas()
        self.Cursor = Cursor(self.Canvas)
        self.Menu = MenuSelect(self.Canvas)
        self.Canvas.cursor = self.Cursor
        self.Canvas.menuselect = self.Menu
        self.iterations = 0
        self.FileName = "New File"

    def run(self):

        self.Canvas.run(self.Cursor)
        self.save()
        self.Menu.run()
        self.Cursor.run(True)

        if self.iterations == 0:
            self.Menu.newBoxFunc(True)
            pass
        if self.iterations > 0:
            pygame.display.set_caption("Pixel Art Maker - " + str(self.FileName))
        self.iterations += 1


    def save(self):
        
        if self.Menu.exportboxFunc() == True:
            while True:
                self.FileName = str(random.randint(1, 999999))  # Use a larger range for more uniqueness
                filepath = os.path.join("savedFiles/", self.FileName + ".png")
                if not os.path.exists(filepath):
                    break  # Exit the loop if the filename is unique
            RGBcolours = []
            for color_name in colours:
                colour = pygame.Color(color_name)
                r, g, b, _ = colour
                rgb_value = (r, g, b)
                RGBcolours.append(rgb_value)
            image = create_image(self.Canvas.gridRepresentation(), RGBcolours)
            image.save("savedFiles/" + str(self.FileName)+".png")
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            image.save(os.path.join(downloads_folder, str(self.FileName) + ".png"))
    

running = True
clock = pygame.time.Clock()
sim = Simulation()

while running:

    SCREEN.fill("dark grey")

    sim.run()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    clock.tick(120)

