import socket
import cv2
import pickle

class RovCam():
    """The camera module responsible for all camera connections to ROV, based on reusable sockets and openCV."""

    # max length of a single packet (which is more than enough to send over a full frame)
    # must be set the same on both sender and receiver
    MAX_DATAGRAM = 120000
    FRONT = 5000
    ARM = 5100
    MISC1 = 5200
    MISC2 = 5300

    def __init__(self, cam, silent=False):
        """Camera constructor takes in the RovCam.CAM type and silent boolean to specify the camera and mode of operation,
        CAM constants are: RovCam.FRONT, RovCam.ARM, RovCam.MISC1, RovCam.MISC2"""
        if cam not in (self.FRONT, self.ARM, self.MISC1, self.MISC2):
            raise ValueError('given camera must be a defined RovCam constant "RovCam.FRONT", RovCam.ARM" or "RovCam.MISC2".')
        self.port = cam
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(("", self.port))
        self.__silentMode = silent
        if not self.__silentMode:
            print("ROV CAM : Connected successfully")

    def __str__(self):
        return f"ROV Camera instance connected on rov camera {self.port}"

    def read(self):
        """BLOCKING function, wait for rov to send image data, returns FRAME"""
        # TODO: handle errors
        data, _ = self.s.recvfrom(self.MAX_DATAGRAM)
        data = pickle.loads(data)
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return frame