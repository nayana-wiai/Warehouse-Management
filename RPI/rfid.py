import board
import busio
from digitalio import DigitalInOut

from adafruit_pn532.spi import PN532_SPI

def readIDs(ids):
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs_pin = DigitalInOut(board.D5)
    pn532 = PN532_SPI(spi, cs_pin, debug=False)

    #ic, ver, rev, support = pn532.get_firmware_version()
    #print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

    pn532.SAM_configuration()

    f = open("transfers/rfids.txt")

    """
    ids = []
    for line in f:
        line = line.replace("[","").replace("]","").replace("\n","")
        id = line.split(", ")
        ids.append(id)
    print(ids)
    """

    foundIDs = []

    print('Waiting for RFID/NFC card...')
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        #print('.', end="")

        # Try again if no card is available.
        if uid is None:
            continue

        foundID = [hex(i) for i in uid]
        #print('Found card with UID:', foundID)

        if foundID in ids:
            print("Found card with UID:", foundID)
            foundIDs.append(foundID)
            return foundID
        else:
            return None


