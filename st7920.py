from machine import Pin
from micropython import const
import framebuf
from utime import sleep_us, sleep_ms

SYNC_CHAR = const(0b11111_00_0) #11111_RW-RS_0
INIT = const((0b0011_0000, 0b0000_1100, 0b0011_0100, 0b0011_0110)) #basic, display control, extend, extend
WIDTH = const(128)
HEIGHT = const(64)
FRAMEBUF_SIZE = const(WIDTH * HEIGHT // 8)

class ST7920(framebuf.FrameBuffer):
    def __init__(self, spi, cs, rst):
        self.spi = spi
        self.cs = cs
        self.rst = rst
        self.cs.init(Pin.OUT, 0)
        self.rst.init(Pin.OUT, 0)
        
        self.buf = bytearray(FRAMEBUF_SIZE)
        super().__init__(self.buf, WIDTH, HEIGHT, framebuf.MONO_HLSB)        
        self.init()
        
    def init(self):
        self.cs.value(1)
        self.rst.value(0)
        sleep_ms(100)
        self.rst.value(1)
        
        for cmd in INIT:
            self.write(0, 0, cmd)
        self.clear_buf()
        self.show()
        self.cs.value(0)
    
    def write(self, rs, rw, data):
        cmd = bytearray(3)
        cmd[0] = SYNC_CHAR | (rw << 2) | (rs << 1)
        cmd[1] = data & 0b1111_0000
        cmd[2] = (data << 4) & 0b1111_0000
        self.spi.write(cmd)
        sleep_us(80)
    
    def set_pos(self, x, y):
        self.write(0, 0, 0b1000_0000 | y)
        self.write(0, 0, 0b1000_0000 | x)
        
    def set_data(self, d1, d2):
        self.write(1, 0, d1)
        self.write(1, 0, d2)
    
    def clear_buf(self):
        self.load_buf(bytearray(FRAMEBUF_SIZE))
        
    def load_buf(self, buf):
        for i in range(FRAMEBUF_SIZE): self.buf[i] = buf[i]
        
    def get_buf(self):
        return self.buf
    
    def show(self):
        self.cs.value(1)
        for i in range(0, FRAMEBUF_SIZE, 2):
            y = i // 16
            x = i // 2 - y * 8
            if y >= HEIGHT // 2:
                x += 8
                y -= HEIGHT // 2
            self.set_pos(x, y)
            self.set_data(self.buf[i], self.buf[i+1])
        self.cs.value(0)