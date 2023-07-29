# This thing can crash easily. I haven't found the cause(s).
# Also leaks memory (BinderCards don't get cleared when selecting a new binder, ExpansionCards don't get cleared when loading a new expansion), so save and exit frequently I suppose.
# For the life of me, I can't figure out how to make it stop, sorry.
from tkinter import *
from tkinter import ttk
from datetime import datetime
import os
import math
import ptcgExpansionDictionary as expansionDictionary

EXPANSIONMENUCOLCOUNT = 3
EXPANSIONMENUROWCOUNT = 4
BINDERPAGEWIDTH = 3
BINDERPAGEHEIGHT = 3

UNDOBUFFER_SIZE = 100

# Don't change these. UndoBuffer control codes.
BUFFER_DO = 0
BUFFER_UNDO = 1
BUFFER_REDO = 2
BUFFER_START = 0
BUFFER_SWAP = 1
BUFFER_REPLACE = 2
BUFFER_REMOVE = 3

mousePos = (0, 0)
def updateMousePos(event):
  global mousePos
  mousePos = (event.x_root, event.y_root)

def sortCardsNumericalKey(card):
  asciiNumbers = [i for i in range(48, 58)]
  val = 0
  i = 1
  while True:
    if ord(card[:-4][-i]) in asciiNumbers:
      val += int(card[:-4][-i]) * (10 ** (i-1))
    else:
      break
    i += 1
  
  # Special designations (RC, SV, etc.) get more letters before val.
  if card[:-4][-i] != "_":
    val += 300
  
  return val 

class Window:
  def __init__(self):
    self.root = Tk()
    self.root.title("DigitalBinder")
    self.root.geometry("1500x800+80+50")   # set starting size of window
    #self.root.minsize(1500, 800)          # width x height
    #self.root.maxsize(1500, 800)          # width x height
    self.root.config(bg="lightgrey")
    
    # For when a card is being dragged.
    self.selectedCard = None
    self.cardToBeCleared = False

    # Expansion menu.
    self.expFrame = Frame(self.root, bg="lightgrey", bd=5, relief=GROOVE)
    self.expFrame.grid(row=0, column=0, sticky=N+W)
    self.exp = Expansion(self.expFrame, self)

    # Separators.
    '''
    Label(self.root, bg="lightgrey").grid(row=0,
                                     column=EXPANSIONMENUCOLCOUNT + 1,
                                     ipadx=75)
    Frame(self.root, bg="black").grid(row=1,
                                 column=EXPANSIONMENUCOLCOUNT + 2 + BINDERPAGEWIDTH,
                                 ipadx=10,
                                 rowspan=BINDERPAGEHEIGHT,
                                 sticky=N+S)
    '''

    # Binder menu.
    self.binderFrame = Frame(self.root, bg="lightgrey", bd=5, relief=GROOVE)
    self.binderFrame.grid(row=0, column=1, padx=100, sticky=N+E)
    
    # Binder separator
    self.binderFrameSeparator = Frame(self.binderFrame, bg="black")
    self.binderFrameSeparator.grid(row=1, column=BINDERPAGEWIDTH, ipadx=10, rowspan=BINDERPAGEHEIGHT, sticky=N+S)
    
    self.binder = Binder(self.binderFrame, self)
    self.root.bind("<Motion>", self.clearCard)
    self.root.bind("<Right>", self.binder.nextPage)
    self.root.bind("<Left>", self.binder.prevPage)
    self.root.bind("<Control-KeyPress-z>", self.binder.undo)
    self.root.bind("<Control-KeyPress-Z>", self.binder.undo)
    self.root.bind("<Control-Shift-KeyPress-z>", self.binder.redo)
    self.root.bind("<Control-Shift-KeyPress-Z>", self.binder.redo)
    self.root.bind("<Control-KeyPress-y>", self.binder.redo)
    self.root.bind("<Control-KeyPress-Y>", self.binder.redo)
  
  def clearCard(self, event):
    updateMousePos(event)
    if self.cardToBeCleared:
      self.selectedCard = None

class Expansion:
  def __init__(self, parent, window):
    self.parent = parent
    self.window = window
    self.offs = 0
    self.maxOffs = 0
    self.cards = list()

    # Menu.
    self.textVar = StringVar()
    self.textVar.set("Select expansion")
    self.vals = [key for key, value in expansionDictionary.dict.items()]
    self.menu = ttk.Combobox(self.parent, values=self.vals, textvariable=self.textVar, exportselection=0, width=40)
    self.menu.state(['readonly'])
    self.menu.bind("<<ComboboxSelected>>", self.refresh)
    self.menu.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=W)
    
    # Buttons.
    textVarTop = StringVar()
    textVarTop.set("^^")
    self.topButton = Button(self.parent, command=self.moveToTop, textvariable=textVarTop)
    self.topButton.grid(row=1, column=EXPANSIONMENUCOLCOUNT, padx=5, pady=5, sticky=W+N)
    self.topButton["state"] = "disabled"
    
    textVarBottom = StringVar()
    textVarBottom.set("v v")
    self.bottomButton = Button(self.parent, command=self.moveToBottom, textvariable=textVarBottom)
    self.bottomButton.grid(row=EXPANSIONMENUROWCOUNT, column=EXPANSIONMENUCOLCOUNT, padx=5, pady=5, sticky=W+S)
    self.bottomButton["state"] = "disabled"
    
    textVarUp = StringVar()
    textVarUp.set(" ^ ")
    self.upButton = Button(self.parent, command=self.moveUp, textvariable=textVarUp)
    self.upButton.grid(row=2, column=EXPANSIONMENUCOLCOUNT, ipadx=1, padx=5, pady=5, sticky=W+N)
    self.upButton["state"] = "disabled"
    
    textVarDown = StringVar()
    textVarDown.set(" v ")
    self.downButton = Button(self.parent, command=self.moveDown, textvariable=textVarDown)
    self.downButton.grid(row=EXPANSIONMENUROWCOUNT-1, column=EXPANSIONMENUCOLCOUNT, ipadx=2, padx=5, pady=5, sticky=W+S)
    self.downButton["state"] = "disabled"

  
  def initCards(self, expansionPath):
    path = os.getcwd()+"/cards/" + expansionPath
    imgPaths = [f for f in os.listdir(path) if os.path.isfile("cards/" + expansionPath + "/" + f)]
    imgPaths.sort(key=sortCardsNumericalKey)
    self.cards = [ExpansionCard(parent=self.parent,
                                expansion=self,
                                expansionPath=expansionPath,
                                imgPath=imgPath)
                                for imgPath in imgPaths]
  
  def drawCards(self):
    # Clear current cards.
    for card in self.cards:
      card.unDrawCard()
    
    for i in range(EXPANSIONMENUROWCOUNT * EXPANSIONMENUCOLCOUNT):
      if self.offs+i >= len(self.cards):
        return
      else:
        self.cards[self.offs+i].drawCard(i)
  
  # Refresh cards displayed.
  def refresh(self, event):
    self.offs = 0
    self.topButton["state"] = "normal"
    self.bottomButton["state"] = "normal"
    self.upButton["state"] = "normal"
    self.downButton["state"] = "normal"
    for card in self.cards:
      card.unDrawCard()
    self.initCards(expansionDictionary.dict[event.widget.get()])
    
    self.maxOffs = len(self.cards) - (EXPANSIONMENUROWCOUNT * EXPANSIONMENUCOLCOUNT)
    mod = len(self.cards) % EXPANSIONMENUCOLCOUNT
    if mod != 0:
        self.maxOffs += EXPANSIONMENUCOLCOUNT - mod
    
    self.drawCards()
  
  def scroll(self, event):
    prevOffs = self.offs
    self.offs -= EXPANSIONMENUCOLCOUNT * int(event.delta / 120)   # I'm just going to assume windows.
    
    if self.offs > self.maxOffs:
      self.offs = self.maxOffs
    if self.offs < 0:
      self.offs = 0
    if prevOffs != self.offs:
      self.drawCards()
      
  def moveToTop(self):
    if self.offs == 0:
      return
    self.offs = 0
    self.drawCards()
  
  def moveToBottom(self):
    if self.offs == self.maxOffs:
      return
    self.offs = self.maxOffs
    self.drawCards()
  
  def moveUp(self):
    if self.offs == 0:
      return
    self.offs -= EXPANSIONMENUCOLCOUNT
    if self.offs < 0:
      self.offs = 0
    self.drawCards()
  
  def moveDown(self):
    if self.offs == self.maxOffs:
      return
    self.offs += EXPANSIONMENUCOLCOUNT
    if self.offs > self.maxOffs:
      self.offs = self.maxOffs
    self.drawCards()

class ExpansionCard:
  def __init__(self, parent, expansion, expansionPath, imgPath):
    self.parent = parent
    self.expansion = expansion
    self.dragger = None
    self.hover = False
    self.relImgPath = expansionPath + "/" + imgPath
    imgPath = os.getcwd() + "/cards/" + self.relImgPath
    self.imgBig = PhotoImage(file=imgPath)
    self.imgSmall = self.imgBig.subsample(2,2)
    self.label = Label(self.parent, image=self.imgSmall, bg="lightgrey")
    self.label.bind("<Button-1>", self.select)
    self.label.bind("<Motion>", self.drag)
    self.label.bind("<ButtonRelease-1>", self.deselect)
    self.label.bind("<Enter>", self.enlarge)
    self.label.bind("<Leave>", self.shrink)
    self.label.bind("<MouseWheel>", self.scroll)

  # Draw card using grid.
  def drawCard(self, loc):
    row = int(loc/EXPANSIONMENUCOLCOUNT) + 1
    col = loc%EXPANSIONMENUCOLCOUNT
    self.label.grid(row=row, column=col, padx=5, pady=5, sticky=W)
    return

  # Remove card using grid.
  def unDrawCard(self):
    self.label.grid_remove()

  # Enlarge card.
  def enlarge(self, event):
    self.hover = True
    #self.label.configure(image=self.imgBig)

  # Shrink card.
  def shrink(self, event):
    self.hover = False
    #self.label.configure(image=self.imgSmall)
  
  def scroll(self, event):
    # If scrolling is zero, then we're not really scrolling.
    # If none of the displayed cards are hovered over, we can't scroll.
    if not event.delta or not self.hover:
      return
    self.expansion.scroll(event)
  
  def select(self, event):
    self.dragger = Label(self.expansion.window.root, image=self.imgBig, bg="lightgrey")
    self.dragger.place(x=mousePos[0]-self.expansion.window.root.winfo_x(), y=mousePos[1]-self.expansion.window.root.winfo_y(), anchor='center')
    self.expansion.window.selectedCard = self
    self.expansion.window.cardToBeCleared = False
    return
  
  def drag(self, event):
    global mousePos
    if not self.dragger:
      return
    self.dragger.place(x=mousePos[0]-self.expansion.window.root.winfo_x(), y=mousePos[1]-self.expansion.window.root.winfo_y(), anchor='center')
  
  def deselect(self, event):
    self.dragger.destroy()
    self.dragger = None
    self.expansion.window.cardToBeCleared = True
    return

# For linked list.
class UndoBufferElement:
  def __init__(self, flag, contents):
    self.flag = flag
    self.contents = contents
    self.prev = None
    self.next = None

class Binder:
  def __init__(self, parent, window):
    self.parent = parent
    self.window = window
    self.pages = list()
    self.vals = os.listdir(os.getcwd()+"/binders/")
    self.vals = [f for f in self.vals if os.path.isfile("binders/" + f)]
    self.bind = ttk.Combobox(self.parent, values=self.vals, exportselection=0)
    self.bind.current([0])
    self.bind.state(['readonly'])
    self.bind.bind("<<ComboboxSelected>>", self.load)
    self.bind.grid(row=0, column=BINDERPAGEWIDTH, columnspan=BINDERPAGEWIDTH*2, padx=5, pady=5, sticky=E)
    
    # Undo/Redo buffer.
    self.undoBufferStart = UndoBufferElement(BUFFER_START, None)
    self.undoBufferCurrent = self.undoBufferStart
    self.undoIndex = 0
    
    # Buttons.
    text = StringVar()
    text.set(">")
    self.buttonNextPage = Button(self.parent, textvariable=text, command=self.nextPage)
    self.buttonNextPage.grid(row=BINDERPAGEHEIGHT+1,
                             column=BINDERPAGEWIDTH*2 - 1,
                             padx=5, pady=5, sticky=N+E)
    text = StringVar()
    text.set(">>")
    self.buttonLastPage = Button(self.parent, textvariable=text, command=self.lastPage)
    self.buttonLastPage.grid(row=BINDERPAGEHEIGHT+1,
                             column=BINDERPAGEWIDTH*2,
                             padx=5, pady=5, sticky=N+E)
    text = StringVar()
    text.set("<")
    self.buttonPrevPage = Button(self.parent, textvariable=text, command=self.prevPage)
    self.buttonPrevPage.grid(row=BINDERPAGEHEIGHT+1,
                             column=1,
                             padx=5, pady=5, sticky=N+W)
    text = StringVar()
    text.set("<<")
    self.buttonFirstPage = Button(self.parent, textvariable=text, command=self.firstPage)
    self.buttonFirstPage.grid(row=BINDERPAGEHEIGHT+1,
                              column=0,
                              padx=5, pady=5, sticky=N+W)
    text = StringVar()
    text.set("Save")
    self.buttonSave = Button(self.parent, textvariable=text, command=self.save)
    self.buttonSave.grid(row=1,
                         column=BINDERPAGEWIDTH*2+1,
                         padx=5, pady=5, sticky=N+E)
    
    # Load binder.
    self.load()
  
  def addToUndoBuffer(self, card1, card2, flag):
    if flag == BUFFER_SWAP:
      contents = (card1, card2)
    elif flag == BUFFER_REPLACE:
      contents = (card1,
                 (card1.imgBig, card1.imgSmall, self.lines[card1.offs2]),
                 (card2.imgBig, card2.imgSmall, card2.relImgPath))
    elif flag == BUFFER_REMOVE:
      imgPath = os.getcwd() + "/cards/Placeholder.png"
      imgBig = PhotoImage(file=imgPath)
      imgSmall = imgBig.subsample(2,2)
      line = "Placeholder.png\n"
      contents = (card1,
                 (card1.imgBig, card1.imgSmall, self.lines[card1.offs2]),
                 (imgBig, imgSmall, line))
    undo = UndoBufferElement(flag, contents)
    
    # Clear now-inaccessible states.
    undoBufferElement = self.undoBufferCurrent
    while undoBufferElement.next:
      undoBufferElement = undoBufferElement.next
      undoBufferElement.prev = None
    
    self.undoBufferCurrent.next = undo
    undo.prev = self.undoBufferCurrent
    self.undoBufferCurrent = undo
    
    # Remove first element if buffer is full.
    if self.undoIndex >= UNDOBUFFER_SIZE:
      self.undoBufferStart = self.undoBufferStart.next
      self.undoBufferStart.prev = None
    else:
      self.undoIndex += 1
  
  def swap(self, card1, card2):
    temp = card1.imgBig
    card1.imgBig = card2.imgBig
    card2.imgBig = temp
    
    temp = card1.imgSmall
    card1.imgSmall = card2.imgSmall
    card2.imgSmall = temp
    
    temp = self.lines[card1.offs2]
    self.lines[card1.offs2] = self.lines[card2.offs2]
    self.lines[card2.offs2] = temp
    
    card2.label.configure(image=card2.imgSmall)
    card1.label.configure(image=card1.imgSmall)
  
  def replace(self, card, imgBig, imgSmall, path):
    card.imgBig = imgBig
    card.imgSmall = imgSmall
    self.lines[card.offs2] = path + '\n'
    card.label.configure(image=card.imgSmall)
    
  def remove(self, card):
    imgPath = os.getcwd() + "/cards/Placeholder.png"
    card.imgBig = PhotoImage(file=imgPath)
    card.imgSmall = card.imgBig.subsample(2,2)
    self.lines[card.offs2] = "Placeholder.png\n"
    card.label.configure(image=card.imgSmall)
  
  # Do action.
  def do(self, binderCard):
    selectedCard = self.window.selectedCard
    if type(selectedCard) is BinderCard:
      self.addToUndoBuffer(binderCard, selectedCard, BUFFER_SWAP)       # Update undo/redo buffer.
      self.swap(binderCard, selectedCard)
    elif type(selectedCard) is ExpansionCard:
      self.addToUndoBuffer(binderCard, selectedCard, BUFFER_REPLACE)    # Update undo/redo buffer.
      self.replace(binderCard, selectedCard.imgBig, selectedCard.imgSmall, selectedCard.relImgPath)
    elif selectedCard == None:
      self.addToUndoBuffer(binderCard, None, BUFFER_REMOVE)             # Update undo/redo buffer.
      self.remove(binderCard)
    self.window.selectedCard = None
  
  # Undo action.
  def undo(self, event):
    if self.undoIndex == 0:
      return
    
    contents = self.undoBufferCurrent.contents
    if self.undoBufferCurrent.flag == BUFFER_SWAP:
      # Swap back.
      self.swap(contents[0], contents[1])
    elif self.undoBufferCurrent.flag == BUFFER_REPLACE:
      # Remove.
      self.remove(contents[0])
    elif self.undoBufferCurrent.flag == BUFFER_REMOVE:
      # Replace.
      self.replace(contents[0], contents[1][0], contents[1][1], contents[1][2])
    
    self.undoBufferCurrent = self.undoBufferCurrent.prev
    self.undoIndex -= 1
  
  def redo(self, event):
    if self.undoBufferCurrent.next == None:
      return
    
    self.undoBufferCurrent = self.undoBufferCurrent.next
    self.undoIndex += 1
    
    contents = self.undoBufferCurrent.contents
    if self.undoBufferCurrent.flag == BUFFER_SWAP:
      # Swap back.
      self.swap(contents[0], contents[1])
    elif self.undoBufferCurrent.flag == BUFFER_REPLACE:
      # Replace.
      self.replace(contents[0], contents[2][0], contents[2][1], contents[2][2])
    elif self.undoBufferCurrent.flag == BUFFER_REMOVE:
      # Remove.
      self.remove(contents[0])
  
  # Loads pages.
  def load(self, event=None):
  
    # Clear Undo/Redo buffer.
    undoBufferElement = self.undoBufferStart
    while undoBufferElement.next:
      undoBufferElement = undoBufferElement.next
      undoBufferElement.prev = None
    self.undoBufferStart = UndoBufferElement(BUFFER_START, None)
    self.undoBufferCurrent = self.undoBufferStart
    self.undoIndex = 0
    
    # Clear BinderCards.
    [page.unload() for page in self.pages]  
    f = open("binders/" + self.bind.get())
    self.lines = f.readlines()
    f.close()
    
    self.onPage = 0
    self.pageCount = math.ceil(len(self.lines) / (BINDERPAGEWIDTH * BINDERPAGEHEIGHT))
    self.pages = [BinderPage(self.parent, self, i) for i in range(self.pageCount+1)]
    self.refresh()
  
  def refresh(self):
    self.pages[self.onPage].load()
    if self.onPage+1 <= self.pageCount:
      self.pages[self.onPage+1].load()
  
  def nextPage(self, event=None):
    if self.onPage >= self.pageCount-1:
      return
    self.pages[self.onPage].unload()
    if self.onPage+1 <= self.pageCount:
      self.pages[self.onPage+1].unload()
    self.onPage += 2
    self.refresh()
  
  def lastPage(self, event=None):
    if self.onPage >= self.pageCount-1:
      return
    self.pages[self.onPage].unload()
    if self.onPage+1 <= self.pageCount:
      self.pages[self.onPage+1].unload()
    self.onPage = (self.pageCount>>1)<<1
    self.refresh()
  
  def prevPage(self, event=None):
    if self.onPage <= 1:
      return
    self.pages[self.onPage].unload()
    if self.onPage+1 <= self.pageCount:
      self.pages[self.onPage+1].unload()
    self.onPage -= 2
    self.refresh()
  
  def firstPage(self, event=None):
    if self.onPage <= 1:
      return
    self.pages[self.onPage].unload()
    if self.onPage+1 <= self.pageCount:
      self.pages[self.onPage+1].unload()
    self.onPage = 0
    self.refresh()
  
  def save(self):
    # Make backup first.
    f = open("binders/" + self.bind.get(), 'r')
    lines = f.readlines()
    f.close()
    
    time = str(datetime.now())
    time = time.replace(" ", "-")
    time = time.replace(":", "-")
    time = time.replace(".", "-")
    
    path = "binders/backups/" + self.bind.get()[:-4] + "-" + time + ".txt"
    if os.path.isfile(path):
      print("Error, backupfile already exists, can't save.")
      return
    
    f = open(path, 'w')
    [f.write(line) for line in lines]
    f.close()
    
    # Now overwrite original file.
    f = open("binders/" + self.bind.get(), 'w')
    [f.write(line) for line in self.lines]
    f.close()
    
    return

class BinderPage:
  def __init__(self, parent, binder, offs):
    self.parent = parent
    self.binder = binder
    self.offs = offs
    self.cards = [BinderCard(self.parent, self, i) for i in range(BINDERPAGEWIDTH * BINDERPAGEHEIGHT)]
  
  def unload(self):
    for i in range(BINDERPAGEWIDTH * BINDERPAGEHEIGHT):
      self.cards[i].unload()
  
  def load(self):
    for i in range(BINDERPAGEWIDTH * BINDERPAGEHEIGHT):
      self.cards[i].load()

class BinderCard:
  def __init__(self, parent, page, offs):
    self.parent = parent
    self.page = page
    self.offs = offs
    self.dragger = None
    self.offs2 = (self.page.offs-1) * BINDERPAGEWIDTH * BINDERPAGEHEIGHT + self.offs
    if self.offs2 >= len(self.page.binder.lines) or self.page.offs == 0:
      relImgPath = "/cards/Placeholder.png"
    else:
      relImgPath = "/cards/" + self.page.binder.lines[self.offs2].rstrip()
    imgPath = os.getcwd() + relImgPath
    self.imgBig = PhotoImage(file=imgPath)
    self.imgSmall = self.imgBig.subsample(2,2)
    if self.page.offs == 0:
      self.label = Label(self.parent, image=self.imgSmall, bg="lightgrey", bd=5)
    else:
      self.label = Label(self.parent, image=self.imgSmall, bg="lightgrey", bd=5, relief=GROOVE)
  
  def copy(self):
    return BinderCard(self.parent, self.page, self.offs)
  
  def unload(self):
    self.label.grid_remove()
  
  def load(self):
    row = int(1 + (self.offs / BINDERPAGEHEIGHT))
    col = int(self.offs % BINDERPAGEWIDTH)
    if (self.page.offs & 1):
      col += BINDERPAGEWIDTH+1        # For right page.
    self.label.grid(row=row, column=col, padx=5, pady=5, sticky=W)
    self.label.bind("<Enter>", self.change)
    self.label.bind("<Button-1>", self.select)
    self.label.bind("<Motion>", self.drag)
    self.label.bind("<ButtonRelease-1>", self.deselect)
    self.label.bind("<Button-3>", self.clear)
  
  def select(self, event):
    self.dragger = Label(self.page.binder.window.root, image=self.imgBig, bg="lightgrey")
    self.dragger.place(x=mousePos[0]-self.page.binder.window.root.winfo_x(), y=mousePos[1]-self.page.binder.window.root.winfo_y(), anchor='center')
    self.page.binder.window.selectedCard = self
    self.page.binder.window.cardToBeCleared = False
    return
  
  def drag(self, event):
    global mousePos
    if not self.dragger:
      return
    self.dragger.place(x=mousePos[0]-self.page.binder.window.root.winfo_x(), y=mousePos[1]-self.page.binder.window.root.winfo_y(), anchor='center')
  
  def deselect(self, event):
    self.dragger.destroy()
    self.dragger = None
    self.page.binder.window.cardToBeCleared = True
    return
  
  def change(self, event):
    selectedCard = self.page.binder.window.selectedCard
    if (not selectedCard or self.offs2 >= len(self.page.binder.lines) or self.page.offs == 0):
      return
    self.page.binder.do(self)
  
  def clear(self, event):
    if ((self.offs2 >= len(self.page.binder.lines)) or
        (self.page.offs == 0) or
        (self.page.binder.lines[self.offs2] == "Placeholder.png\n")):
      return
    self.page.binder.do(self)

# Main window.
window = Window()
window.root.mainloop()