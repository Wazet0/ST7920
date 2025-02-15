from machine import Pin, SPI
from st7920 import ST7920

def image():
    buf = bytearray()
    with open("image.txt", "r") as f:
        data = f.read()
        data = data.replace(" ", "")
        data = data.split(",")
        for b in data:
            buf.append(int(b, 2))
    return buf
p = Pin(15, Pin.OUT)
spi = SPI(2, baudrate=2_000_000)
cs = Pin(34, Pin.OUT)
rst = Pin(1, Pin.OUT, 1)

st = ST7920(spi, cs, rst)

p.value(1)
st.rect(0, 0, 128, 64, 1)
st.text("ST7920", 38, 32)
st.show()
st.fill(0)
st.show()
st.display_buf(image())

p.value(0)