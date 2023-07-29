# Generates URLs of pokémon cards of the official ptcg database.
# Download by using wget on wsl:
#
# wget -r -nv --no-parent -i <urlFileName>.txt -o out.txt
#
# Output will be sent to "out.txt".

# Unseen Forces, Unown cards, https://assets.pokemon.com/assets/cms2/img/cards/web/EX10/EX10_EN_Unown_A.png etc.
EX = ("EX", [109, 100, 100, 97, 102, 116, 111, 108, 107, 117, 114, 93, 111, 100, 101, 108])

POP = ("POP", [17, 17, 17, 17, 17, 17, 17, 17, 17])

DP = ("DP", [130, 124, 132, 106, 100, 146, 106])

PL = ("PL", [133, 120, 153, 111])

# These seem to use HGSS before the iterator, and always use two digits with leading zero if applicable.
# e.g. https://assets.pokemon.com/assets/cms2/img/cards/web/HSP/HSP_EN_HGSS02.png
HSP = ("HSP", [25])   

HGSS = ("HGSS", [124, 96, 91, 103, 106])

# BW plus leading 0 for single digit, not for double though.
BWP = ("BWP", [101])

BW = ("BW", [115, 98, 102, 103, 111, 128, 21, 153, 138, 122, 105, 140])

# XY plus leading 0 for single digit, not for double though.
XYP = ("XYP", [178])

# "a" trailing after number. Numbers seem arbitrary?
XYA = ("XYA", [6])

# Starts at 0 instead of 1.
XY = ("XY", [39, 146, 109, 113, 122, 164, 34, 110, 100, 164, 123, 115, 125, 116, 113])

# SM plus leading 0 for single digit, not for double though.
SMP = ("SMP", [244])

# SV preceding number.
SMA = ("SMA", [94])

# hidden fates is 115 (11.5?)
SM = ("SM", [163, 169, 169, 78, 124, 173, 146, 183, 78, 236, 196, 18, 234, 258, 69, 271])

# SWSH plus leading 00 for single digit, 0 for double.
SWSHP = ("SWSHP", [307])

# Trainer Gallery are 'separate expansions' and have TG preceding card number.
# Shining fates has 45 (4.5?). SV and double leading zeroes precedes number for the shiny vault.
SWSH = ("SWSH", [216, 209, 201, 80, 203, 73, 122, 183, 233, 237, 25, 25, 284, 186, 30, 216, 30, 88, 217, 30, 215, 30, 160, 70])

# Leading zero in expansion number. No leading zeroes to card numbers.
SV = ("SV0", [258, 279])


# Params.
cards = [EX, POP, DP, PL, HSP, HGSS, BWP, BW, XYP, XYA, XY, SMP, SMA, SM, SWSHP, SWSH, SV]
lang = "EN"
path = "https://assets.pokemon.com/assets/cms2/img/cards/web/"


# I'll try to do one (nested) loop for each "Series" (like all the EX expansions would be a series).
# EX.
f = open("ex.txt", "w")
series = 0
for i, expansionSize in enumerate(cards[series][1]):
  if i+1 == 10:
    for j in range(0, 26):
      f.write(path + "EX10/EX10_EN_Unown_" + chr(ord('A') + j) + ".png\n")
    f.write(path + "EX10/EX10_EN_Unown_!.png\n")
    f.write(path + "EX10/EX10_EN_Unown_?.png\n")
  for j in range(1, expansionSize+1):
    f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_" + str(j) + ".png\n")
f.close()

# POP.
f = open("pop.txt", "w")
series += 1
for i, expansionSize in enumerate(cards[series][1]):
  if i+1 == 9:
    for j in range(1, expansionSize+1):
      f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + "_" + str(i+1) + "_Cards_" + str(j) + ".png\n")
  else:
    for j in range(1, expansionSize+1):
      f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_" + str(j) + ".png\n")
f.close()

# DP.
f = open("dp.txt", "w")
series += 1
for i, expansionSize in enumerate(cards[series][1]):
  if i+1 == 7:
    expansionSize -= 3
    for j in range(1, 4):
      f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_SH" + str(j) + ".png\n")
  for j in range(1, expansionSize+1):
    f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_" + str(j) + ".png\n")
f.close()

# Platinum.
f = open("pl.txt", "w")
series += 1
for i, expansionSize in enumerate(cards[series][1]):
  if i+1 == 1:
    expansionSize -= 3
    for j in range(4, 7):
      f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_SH" + str(j) + ".png\n")
  if i+1 == 2:
    expansionSize -= 6
    for j in range(1, 7):
      f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_RT" + str(j) + ".png\n")
  if i+1 == 3:
    expansionSize -= 3
    for j in range(7, 10):
      f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_SH" + str(j) + ".png\n")
  if i+1 == 4:
    expansionSize -= 12
    for j in range(1, 10):
      f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_AR" + str(j) + ".png\n")
    for j in range(10, 13):
      f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_SH" + str(j) + ".png\n")
  for j in range(1, expansionSize+1):
    f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_" + str(j) + ".png\n")
f.close()

# HGSS Promo.
f = open("hs.txt", "w")
series += 1
for i, expansionSize in enumerate(cards[series][1]):
  for j in range(1, expansionSize+1):
    s = "_HGSS0" if j < 10 else "_HGSS"
    f.write(path + cards[series][0] + "/" + cards[series][0] + "_" + lang + s + str(j) + ".png\n")
# HGSS Main.
series += 1
for i, expansionSize in enumerate(cards[series][1]):
  if i+1 == 5:
    expansionSize -= 11
    for j in range(1, 12):
      f.write(path + "COL1/COL1_" + lang + "_SL" + str(j) + ".png\n")
    for j in range(1, expansionSize+1):
      f.write(path + "COL1/COL1_" + lang + "_" + str(j) + ".png\n")
  else:
    expansionSize -= 1
    s = "_FOUR.png\n"
    if i+1 == 1:
      s = "_ONE.png\n"
    elif i+1 == 2:
      s = "_TWO.png\n"
    elif i+1 == 3:
      s = "_THREE.png\n"
    f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + s)
    for j in range(1, expansionSize+1):
      f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_" + str(j) + ".png\n")
f.close()

# BW Promo.
f = open("bw.txt", "w")
series += 1
for i, expansionSize in enumerate(cards[series][1]):
  for j in range(1, expansionSize+1):
    s = "_BW0" if j < 10 else "_BW"
    f.write(path + cards[series][0] + "/" + cards[series][0] + "_" + lang + s + str(j) + ".png\n")
# BW Main.
series += 1
incr = 1
for i, expansionSize in enumerate(cards[series][1]):
  if i+incr == 1:
    expansionSize -= 1
    f.write(path + cards[series][0] + str(i+incr) + "/" + cards[series][0] + str(i+incr) + "_" + lang + "_PIKA.png\n")
  if i+incr == 11:
    expansionSize -= 25
    for j in range(1, 26):
      f.write(path + cards[series][0] + str(i+incr) + "/" + cards[series][0] + str(i+incr) + "_" + lang + "_RC" + str(j) + ".png\n")
  if i+1 == 7:
    incr -= 1
    for j in range(1, expansionSize+1):
      f.write(path + "DV1/DV1_" + lang + "_" + str(j) + ".png\n")
  else:
    for j in range(1, expansionSize+1):
      f.write(path + cards[series][0] + str(i+incr) + "/" + cards[series][0] + str(i+incr) + "_" + lang + "_" + str(j) + ".png\n")
f.close()

# XY Promo.
f = open("xy.txt", "w")
series += 1
for i, expansionSize in enumerate(cards[series][1]):
  for j in range(1, expansionSize+1):
    s = "_XY0" if j < 10 else "_XY"
    f.write(path + cards[series][0] + "/" + cards[series][0] + "_" + lang + s + str(j) + ".png\n")
# XY Alternate. Not worth it, manually downloaded these six.
#
# XY Main.
series += 2
incr = 0
for i, expansionSize in enumerate(cards[series][1]):
  if i == 6:
    incr -= 1
    for j in range(1, expansionSize+1):
      f.write(path + "DC1/DC1_" + lang + "_" + str(j) + ".png\n")
  elif i == 11:
    incr -= 1
    expansionSize -= 32
    for j in range(1, 33):
      f.write(path + "G1/G1_" + lang + "_RC" + str(j) + ".png\n")
    for j in range(1, expansionSize+1):
      f.write(path + "G1/G1_" + lang + "_" + str(j) + ".png\n")
  else:
    for j in range(1, expansionSize+1):
      f.write(path + cards[series][0] + str(i+incr) + "/" + cards[series][0] + str(i+incr) + "_" + lang + "_" + str(j) + ".png\n")
f.close()

# SM Promo.
f = open("sm.txt", "w")
series += 1
for i, expansionSize in enumerate(cards[series][1]):
  for j in range(1, expansionSize+1):
    s = "_SM0" if j < 10 else "_SM"
    f.write(path + cards[series][0] + "/" + cards[series][0] + "_" + lang + s + str(j) + ".png\n")
# SM Alternate.
series += 1
for i, expansionSize in enumerate(cards[series][1]):
  for j in range(1, expansionSize+1):
    f.write(path + cards[series][0] + "/" + cards[series][0] + "_" + lang + "_SV" + str(j) + ".png\n")
# SM Main.
series += 1
incr = 1
for i, expansionSize in enumerate(cards[series][1]):
  if i+1 == 15:
    incr -= 1
    for j in range(1, expansionSize+1):
      f.write(path + "SM115/SM115_" + lang + "_" + str(j) + ".png\n")
  elif i+1 == 12:
    incr -= 1
    for j in range(1, expansionSize+1):
      f.write(path + "DET/DET_" + lang + "_" + str(j) + ".png\n")
  elif i+1 == 9:
    incr -= 1
    for j in range(1, expansionSize+1):
      f.write(path + "SM75/SM75_" + lang + "_" + str(j) + ".png\n")
  elif i+1 == 4:
    incr -= 1
    for j in range(1, expansionSize+1):
      f.write(path + "SM35/SM35_" + lang + "_" + str(j) + ".png\n")
  else:
    for j in range(1, expansionSize+1):
      f.write(path + cards[series][0] + str(i+incr) + "/" + cards[series][0] + str(i+incr) + "_" + lang + "_" + str(j) + ".png\n")
f.close()

# SWSH Promo.
f = open("swsh.txt", "w")
series += 1
for i, expansionSize in enumerate(cards[series][1]):
  for j in range(1, expansionSize+1):
    s = "_SWSH"
    if j < 100:
      s += "0"
    if j < 10:
      s += "0"
    f.write(path + cards[series][0] + "/" + cards[series][0] + "_" + lang + s + str(j) + ".png\n")
# SWSH Main.
series += 1
incr = 1
for i, expansionSize in enumerate(cards[series][1]):
  if i+1 == 24:
    incr -= 1
    for j in range(1, expansionSize+1):
      s = "_GG0" if j < 10 else "_GG"
      f.write(path + "SWSH12PT5GG/SWSH12PT5GG_" + lang + s + str(j) + ".png\n")
  elif i+1 == 23:
    incr -= 1
    for j in range(1, expansionSize+1):
      f.write(path + "SWSH12PT5/SWSH12PT5_" + lang + "_" + str(j) + ".png\n")
  elif i+1 == 22:
    incr -= 1
    for j in range(1, expansionSize+1):
      s = "_TG0" if j < 10 else "_TG"
      f.write(path + "SWSH12TG/SWSH12TG_" + lang + s + str(j) + ".png\n")
  elif i+1 == 18:
    incr -= 1
    for j in range(1, expansionSize+1):
      f.write(path + "PGO/PGO_" + lang + "_" + str(j) + ".png\n")
  elif i+1 == 12:
    incr -= 1
    # There is zero rhyme or reason to this order, so we're downloading these manually.
    #for j in range(1, expansionSize+1):
      #f.write(path + "CELC/CELC_" + lang + "_" + str(j) + ".png\n")
  elif i+1 == 11:
    incr -= 1
    for j in range(1, expansionSize+1):
      f.write(path + "CEL/CEL_" + lang + "_" + str(j) + ".png\n")
  elif i+1 == 7:
    incr -= 1
    for j in range(1, expansionSize+1):
      s = "_SV"
      if j < 100:
        s += "0"
      if j < 10:
        s += "0"
      f.write(path + "SWSH45/SWSH45_" + lang + s + str(j) + ".png\n")
  elif i+1 == 6:
    incr -= 1
    for j in range(1, expansionSize+1):
      f.write(path + "SWSH45/SWSH45_" + lang + "_" + str(j) + ".png\n")
  elif i+1 == 4:
    incr -= 1
    for j in range(1, expansionSize+1):
      f.write(path + "SWSH35/SWSH35_" + lang + "_" + str(j) + ".png\n")
  elif ((i+1 == 15) + (i+1 == 17) or (i+1 == 20)):
    incr -= 1
    for j in range(1, 31):
      s = "_TG0" if j < 10 else "_TG"
      f.write(path + cards[series][0] + str(i+incr) + "/" + cards[series][0] + str(i+incr) + "_" + lang + s + str(j) + ".png\n")
  else:
    for j in range(1, expansionSize+1):
      f.write(path + cards[series][0] + str(i+incr) + "/" + cards[series][0] + str(i+incr) + "_" + lang + "_" + str(j) + ".png\n")
f.close()

# SV
f = open("sv.txt", "w")
series += 1
for i, expansionSize in enumerate(cards[series][1]):
  for j in range(1, expansionSize+1):
    f.write(path + cards[series][0] + str(i+1) + "/" + cards[series][0] + str(i+1) + "_" + lang + "_" + str(j) + ".png\n")
f.close()