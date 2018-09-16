import math
import os, sys, inspect, threading, time
import serial

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2 ** 32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap


class SampleListener(Leap.Listener):

    def limit_inputs(self, angle):
        threshold = 0.25 * math.pi
        if angle > threshold:
            angle = threshold
        elif angle < -threshold:
            angle = -threshold
        return angle

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):
        frame = controller.frame()

        hands = frame.hands
        hand = hands[0]
        pitch = hand.direction.pitch
        yaw = hand.direction.yaw
        roll = hand.palm_normal.roll

        print self.limit_inputs(pitch), self.limit_inputs(yaw), self.limit_inputs(roll)
        self.toSerial(self.limit_inputs(pitch), self.limit_inputs(yaw), self.limit_inputs(roll))

    def toSerial(self, pitchRads, yawRads, rollRads):
        ser = serial.Serial()
        ser.baudrate = 19200
        ser.port = 'COM11'
        data = ["P", pitchRads, "R", rollRads, "Y", yawRads]
        ser.open()
        ser.write(data)
        # serial.Serial('COM3', 38400, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

    def convertRange(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
