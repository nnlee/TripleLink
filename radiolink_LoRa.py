#
#  Tests link margin by increasing power in 1 dB steps, printing transmitted power and RSSI, and
#  alternating which radio is transmitting and which is receiving.  Use PUTTY and log all received messages
#  for easy data analysis, or just look for the first transmitted power to be received reliably.
#  Pete 230914
import board
import busio
import digitalio
import adafruit_rfm9x
import time
RADIO_FREQ_MHZ = 915.0
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D9)
reset = digitalio.DigitalInOut(board.D10)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, RADIO_FREQ_MHZ)
timedout = 0.0
while True:
    for i in range(5, 20, 1):
        rfm9x.tx_power = i
        print (rfm9x.tx_power, end = "; ")
        for j in range (100):
            rfm9x.send(bytes(f"Hello world! {i}", "utf-8"))
    print("Sent hello world message!")
    ncount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    while True:
        packet = rfm9x.receive(timeout=1.0+timedout)
        if packet is None:
		# Packet has not been received (yet)
            print()
            print("Received nothing! Transmitting again...")
            timedout = 12.0
            break
        else:
		# Received a packet!
            packet_text = str(packet, "ascii")
            print("{0}".format(packet_text[13:]), end="")
            #print('RSSI: {0}'.format(rfm9x.rssi))
            timedout = 0.0
