import busio
import digitalio
import microcontroller
from kmk.hid import HID_REPORT_SIZES, HIDReportTypes

import time

from kmk.modules import Module
from kmk.modules.pmw3360_firmware import firmware
from kmk.keys import KC, AX


class PointingDevice:
    MB_LMB = 1
    MB_RMB = 2
    MB_MMB = 4
    _evt = bytearray(HID_REPORT_SIZES[HIDReportTypes.MOUSE] + 1)

    def __init__(self):
        self.key_states = {}
        self.hid_pending = False
        self.report_device = memoryview(self._evt)[0:1]
        self.report_device[0] = HIDReportTypes.MOUSE
        self.button_status = memoryview(self._evt)[1:2]
        self.report_x = memoryview(self._evt)[2:3]
        self.report_y = memoryview(self._evt)[3:4]
        self.report_w = memoryview(self._evt)[4:]


class REG:
    Product_ID = 0x0
    Revision_ID = 0x1
    Motion = 0x02
    Delta_X_L = 0x03
    Delta_X_H = 0x04
    Delta_Y_L = 0x05
    Delta_Y_H = 0x06
    Config1 = 0x0F
    Config2 = 0x10
    Angle_Tune = 0x11
    SROM_Enable = 0x13
    Observation = 0x24
    SROM_ID = 0x2A
    Power_Up_Reset = 0x3A
    Motion_Burst = 0x50
    SROM_Load_Burst = 0x62
    Lift_Config = 0x63


class PMW3360(Module):
    tsww = tswr = 180
    baud = 2000000
    cpol = 1
    cpha = 1
    DIR_WRITE = 0x80
    DIR_READ = 0x7F

    def __init__(self, cs, sclk, miso, mosi, invert_x=False, invert_y=False, flip_xy=False):
        print("In pmw3360 __init__ again")
        self.pointing_device = PointingDevice()
        self.cs = digitalio.DigitalInOut(cs)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.spi = busio.SPI(clock=sclk, MOSI=mosi, MISO=miso)
        self.invert_x = invert_x
        self.invert_y = invert_y
        self.flip_xy = flip_xy
        self.scroll_control = False
        self.volume_control = False
        self.v_scroll_ctr = 0
        self.scroll_res = 8

    def start_v_scroll(self, enabled=True):
        self.scroll_control = enabled

    def start_volume_control(self, enabled=True):
        self.volume_control = enabled

    def pmw3360_start(self):
        self.cs.value = False

    def pmw3360_stop(self):
        self.cs.value = True

    def pmw3360_write(self, reg, data):
        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=self.baud, polarity=self.cpol, phase=self.cpha)
            self.pmw3360_start()
            self.spi.write(bytes([reg | self.DIR_WRITE, data]))
            # microcontroller.delay_us(35)
        finally:
            self.spi.unlock()
            self.pmw3360_stop()
        microcontroller.delay_us(self.tswr)

    def pmw3360_read(self, reg):
        result = bytearray(1)
        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=self.baud, polarity=self.cpol, phase=self.cpha)
            self.pmw3360_start()
            self.spi.write(bytes([reg & self.DIR_READ]))
            microcontroller.delay_us(160)
            self.spi.readinto(result)
            microcontroller.delay_us(1)
        finally:
            self.spi.unlock()
            self.pmw3360_stop()
        microcontroller.delay_us(19)
        return result[0]

    def pwm3360_upload_srom(self):
        print("Uploading pmw3360 FW")
        self.pmw3360_write(REG.Config2, 0x0)
        self.pmw3360_write(REG.SROM_Enable, 0x1D)
        time.sleep(0.01)
        self.pmw3360_write(REG.SROM_Enable, 0x18)

        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=self.baud, polarity=self.cpol, phase=self.cpha)
            self.pmw3360_start()
            self.spi.write(bytes([REG.SROM_Load_Burst | self.DIR_WRITE]))
            microcontroller.delay_us(15)

            for b in firmware:
                self.spi.write(bytes([b]))
                microcontroller.delay_us(15)
        except Error:
            print("Received error on firmware write")
        finally:
            print("Firmware done")
            microcontroller.delay_us(200)
            self.spi.unlock()
            self.pmw3360_stop()

        self.pmw3360_read(REG.SROM_ID)
        self.pmw3360_write(REG.Config2, 0)  # set to wired mouse mode
        microcontroller.delay_us(1)

    def delta_to_int(self, high, low):
        comp = (high << 8) | low
        if comp & 0x8000:
            return (-1) * (0xFFFF + 1 - comp)
        return comp

    def pmw3360_read_motion(self):
        result = bytearray(12)
        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=self.baud, polarity=self.cpol, phase=self.cpha)
            self.pmw3360_start()
            self.spi.write(bytes([REG.Motion_Burst & self.DIR_READ]))
            microcontroller.delay_us(35)
            self.spi.readinto(result)

        finally:
            self.spi.unlock()
            self.pmw3360_stop()
        microcontroller.delay_us(20)
        return result

    def during_bootup(self, keyboard):
        print("firmware during_bootup() called")

        print("Debugging not enabled")

        self.pmw3360_start()

        microcontroller.delay_us(40)

        self.pmw3360_stop()

        microcontroller.delay_us(40)

        self.pmw3360_write(REG.Power_Up_Reset, 0x5A)
        time.sleep(0.1)
        self.pmw3360_read(REG.Motion)
        self.pmw3360_read(REG.Delta_X_L)
        self.pmw3360_read(REG.Delta_X_H)
        self.pmw3360_read(REG.Delta_Y_L)
        self.pmw3360_read(REG.Delta_Y_H)

        self.pwm3360_upload_srom()

        time.sleep(0.1)

        self.pmw3360_write(REG.Config1, 0x06)  # set x/y resolution to 700 cpi
        # self.pmw3360_write(REG.Config2, 0)  # set to wired mouse mode
        self.pmw3360_write(REG.Angle_Tune, -25)  # set to wired mouse mode
        self.pmw3360_write(REG.Lift_Config, 0x02)  # set to wired mouse mode

        if keyboard.debug_enabled:
            print('PMW3360 Product ID ', hex(self.pmw3360_read(REG.Product_ID)))
            print('PMW3360 Revision ID ', hex(self.pmw3360_read(REG.Revision_ID)))
            if self.pmw3360_read(REG.Observation) & 0x40:
                print('PMW3360: Sensor is running SROM')
                print('PMW3360: SROM ID: ', hex(self.pmw3360_read(REG.SROM_ID)))
            else:
                print('PMW3360: Sensor is not running SROM!')
        print("Finished with firmware download")
        # return


    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        motion = self.pmw3360_read_motion()
        # print(motion)
        if motion[0] & 0x80:
            if motion[0] & 0x07:
                print("Motion weirdness")
                self.pmw3360_write(REG.Motion_Burst, 0)
                return
            if self.flip_xy:
                delta_x = self.delta_to_int(motion[5], motion[4])
                delta_y = self.delta_to_int(motion[3], motion[2])
            else:
                delta_x = self.delta_to_int(motion[3], motion[2])
                delta_y = self.delta_to_int(motion[5], motion[4])

            if self.invert_x:
                delta_x *= -1
            if self.invert_y:
                delta_y *= -1

            if delta_x < 0:
                self.pointing_device.report_x[0] = (delta_x & 0xFF) | 0x80
            else:
                self.pointing_device.report_x[0] = delta_x & 0xFF

            if delta_y < 0:
                self.pointing_device.report_y[0] = (delta_y & 0xFF) | 0x80
            else:
                self.pointing_device.report_y[0] = delta_y & 0xFF

            print('Delta: ', delta_x, ' ', delta_y)

            if(not self.scroll_control and not self.volume_control):
                self.pointing_device.hid_pending = True
                keyboard._hid_helper.hid_send(self.pointing_device._evt)
            elif self.scroll_control:
                #   vertical scroll
                self.v_scroll_ctr += 1
                if self.v_scroll_ctr >= self.scroll_res:
                    if delta_y > 0:
                        keyboard.tap_key(KC.MW_DN)

                    if delta_y < 0:
                        keyboard.tap_key(KC.MW_UP)

                    self.v_scroll_ctr = 0
            else:
                self.v_scroll_ctr += 1
                if self.v_scroll_ctr >= self.scroll_res:
                    if delta_y > 0:
                        keyboard.tap_key(KC.VOLD)

                    if delta_y < 0:
                        keyboard.tap_key(KC.VOLU)

                    self.v_scroll_ctr = 0

            self.pointing_device.report_x[0] = 0
            self.pointing_device.report_y[0] = 0

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return



