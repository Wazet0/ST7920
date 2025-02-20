from machine import Pin, SPI
from st7920 import ST7920
from utime import sleep

def image():
    buf = bytearray()
    with open("image.txt", "r") as f:
        data = f.read()
        data = data.replace(" ", "")
        data = data.split(",")
        for b in data:
            buf.append(int(b, 2))
    return buf

spi = SPI(2, baudrate=2_000_000)
cs = Pin(34)
rst = Pin(1)

st = ST7920(spi, cs, rst)

st.rect(0, 0, 128, 64, 1)
st.text("ST7920", 38, 32)
st.show()
sleep(3)
st.fill(0)
st.show()
st.load_buf(image())
st.show()