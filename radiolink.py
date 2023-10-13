import board
import busio
import digitalio
import adafruit_rfm69
import time
RADIO_FREQ_MHZ = 915.0
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)
rfm69 = adafruit_rfm69.RFM69(spi, cs, reset, RADIO_FREQ_MHZ)
timedout = 0.0
ncount = []
nhist = 0
while True:
	print(f"{nhist} Histogram: {ncount}")
	nhist += 1
	for i in range(-2, 20, 1):
		rfm69.tx_power = i
		print (rfm69.tx_power, end = "; ")
		for j in range (100):
			rfm69.send(bytes(f"Hello world! {i} ", "utf-8"))
	print("Sent hello world message!")
	ncount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	while True:
		packet = rfm69.receive(timeout=1.0+timedout+7)
		if packet is None:
		# Packet has not been received (yet)
			print()
			print("Received nothing! Transmitting again...")
			timedout = 12.0
			break
		else:
		# Received a packet!
			packet_text = str(packet, "ascii")
			#print("Received (ASCII): {0}".format(packet_text), end="; ")
			print("{0}".format(packet_text[13:]), end="")
			ncount[int("{0}".format(packet_text[13:]))+2] += 1
			#print('RSSI: {0}'.format(rfm69.rssi))
			timedout = 0.0
