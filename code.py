# Last revised: 2023-11-17
# Added error handling and counter, augmented transmission packet to provide error count to the other station

import board
import busio
import digitalio
import adafruit_rfm69
import neopixel
import time
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1)
pixels.fill((1, 0, 0))
print('='*10 + "Restarting link budget script" + '='*10)
RADIO_FREQ_MHZ = 915.0
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)
rfm69 = adafruit_rfm69.RFM69(spi, cs, reset, RADIO_FREQ_MHZ)
timedout = 0.0
ncount = []
nhist = 0
nerr = 0
tokens = ['0','0','0','0','0']
pixels.fill((0, 0, 0))
while True:
    try:
        print("Switching to receiving mode")
        ncount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        nhist += 1
        while True:
            packet = rfm69.receive(timeout=1.0+timedout+7)
            if packet is None:
            # Packet has not been received (yet)
                print("Receiver timeout!\n")
                timedout = 12.0
                break
            else:
            # Received a packet!
                pixels.fill((0, 1, 0))
                packet_text = str(packet, "ascii")
                #print("Received (ASCII): {0}".format(packet_text), end="; ")
                tokens = packet_text.split(' ')
                print("{0} ".format(tokens[-2]), end="")
                ncount[int(tokens[-2])+2] += 1
                #print('RSSI: {0}'.format(rfm69.rssi))
                timedout = 0.0
                pixels.fill((0, 0, 0))
        print(f"Histogram # {nhist}:")
        print("Power [dBm]: " + ' '.join(["{:>3}".format(n) for n in range(-2, 20, 1)]))
        print("Count [num]: " + ' '.join(["{:>3}".format(n) for n in ncount])+"\n")
        print("Local errors: {0}; Remote errors: {1}".format(nerr,tokens[-3]))
        print("Sending 'hello world' message\nTx power level [dBm]:")
        for i in range(-2, 20, 1):
            rfm69.tx_power = i
            print(i, end="; ")
            for j in range(100):
                pixels.fill((0, 0, 1))
                rfm69.send(bytes(f"Hello world! {nerr} {i} ", "utf-8"))
                pixels.fill((0, 0, 0))
        print("Sent 'hello world' message!")
    except:
        nerr += 1
        print('error')
