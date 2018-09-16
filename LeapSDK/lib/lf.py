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
        radsPi = math.pi/4
        hands = frame.hands
        hand = hands[0]
        if not hand.is_valid:
            # Turn control to HELP
            self.toSerial(0,0,0)

        pitch = hand.direction.pitch
        yaw = hand.direction.yaw
        roll = hand.palm_normal.roll

        handpos = hand.palm_position
        throt = handpos.y
        pitch = self.limit_inputs(pitch)

        roll = self.limit_inputs(roll)
        # print ">>", roll, pitch, throt
        pitch = self.convertRange(pitch, -radsPi, radsPi)
        throt = self.convertRange(throt, 100, 450)
        roll = self.convertRange(roll, radsPi, -radsPi)
        # print roll

        self.toSerial(pitch, roll, throt)

    def toSerial(self, pitchRads, rollRads, throttle):
        data = [112, pitchRads, 114, rollRads, 116, throttle]
        print data
        self.ser.reset_input_buffer()
        # return
        time.sleep(0.05)
        self.ser.write(data)

    def convertRange(self, x, in_min, in_max, out_min=1, out_max=255):
        r = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        return max(min(int(r), out_max), out_min)


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
