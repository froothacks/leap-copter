import math
import os, sys, inspect, threading, time
import serial

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2 ** 32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap


class SampleListener(Leap.Listener):
    def __init__(self):
        super(SampleListener, self).__init__()
        self.ser = None

    def limit_inputs(self, angle):
        threshold = 0.25 * math.pi
        if angle > threshold:
            angle = threshold
        elif angle < -threshold:
            angle = -threshold
        return angle

    def on_connect(self, controller):
        self.ser = serial.Serial('COM4', 9600)
        print "Connected"

    def on_frame(self, controller):
        frame = controller.frame()

        hands = frame.hands
        hand = hands[0]
        pitch = hand.direction.pitch
        yaw = hand.direction.yaw
        roll = hand.palm_normal.roll

        pitch = self.limit_inputs(pitch)
        yaw = self.limit_inputs(yaw)
        roll = self.limit_inputs(roll)
        print ">>", pitch, pitch * 180/math.pi

        pitch = self.convertRange(pitch, -45, 45)
        yaw = self.convertRange(yaw, -45, 45)
        roll = self.convertRange(roll, -45, 45)
        print pitch

        self.toSerial(pitch, yaw, roll)

    def toSerial(self, pitchRads, yawRads, rollRads):
        # data = [112, pitchRads, 114, rollRads, 116, yawRads]
        self.ser.reset_input_buffer()
        # return
        time.sleep(0.05)
        self.ser.write(b"o")

    def convertRange(self, x, in_min, in_max, out_min=1, out_max=255):
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
