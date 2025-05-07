from .reader import Reader
from .writer import Writer
from .data import InData, OutData

class Navigator:

    def __init__(self, reader: Reader, writer: Writer) -> None:
        self.reader = reader
        self.writer = writer

    def _get_elevator(self,
            curr_pitch: float,
            target_pitch: float,
            step_size: float) -> float:
        delta_pitch = target_pitch - curr_pitch
        elevator = -step_size * (delta_pitch / 360.0)
        return elevator

    def _get_aileron(self,
            curr_roll: float,
            target_roll: float,
            step_size: float) -> float:
        delta_roll = target_roll - curr_roll
        aileron = +step_size * (delta_roll / 360.0)
        return aileron

    def pitch_towards(self,
            target_pitch: float,
            step_size: float,
            agl_thresh: float,
            vel_thresh: float,
            max_iter: int) -> None:
        """
            Controls the elevator to steer towards a given angle
            `target_pitch` -- the angle to rotate towards, in degrees
            `step_size` -- how much to rotate each iteration, as a percentage
            `agl_thresh` -- a threshold for when the angle is close enough to the target, in degrees
            `vel_thresh` -- a threshold for when the angular velocity is close enough to zero, in degrees/sec
            `max_iter` -- max amount of iterations before stopping
        """
        for _ in range(max_iter):
            in_data = self.reader.read()
            if abs(in_data.pitch - target_pitch) <= agl_thresh and abs(in_data.pitch_rate) <= vel_thresh:
                break
            elevator = self._get_elevator(in_data.pitch, target_pitch, step_size)
            out_data = OutData.from_indata(in_data)
            out_data.elevator = elevator
            self.writer.write(out_data)

    def roll_towards(self,
            target_roll: float,
            step_size: float,
            agl_thresh: float,
            vel_thresh: float,
            max_iter: int) -> None:
        """
            Controls the ailerons to steer towards a given angle
            `target_roll` -- the angle to rotate towards, in degrees
            `step_size` -- how much to rotate each iteration, as a percentage
            `agl_thresh` -- a threshold for when the angle is close enough to the target, in degrees
            `vel_thresh` -- a threshold for when the angular velocity is close enough to zero, in degrees/sec
            `max_iter` -- max amount of iterations before stopping
        """
        for _ in range(max_iter):
            in_data = self.reader.read()
            if abs(in_data.roll - target_roll) <= agl_thresh and abs(in_data.roll_rate) <= vel_thresh:
                break
            aileron = self._get_aileron(in_data.roll, target_roll, step_size)
            out_data = OutData.from_indata(in_data)
            out_data.aileron = aileron
            self.writer.write(out_data)

    def rotate_towards(self,
            target_pitch: float,
            target_roll: float,
            step_size: float,
            agl_thresh: float,
            vel_thresh: float,
            max_iter: int):
        """
            Controls the elevator and ailerons to rotate towards some pitch and roll
            `target_pitch` -- the pitch to rotate towards, in degrees
            `target_roll` -- the roll to rotate towards, in degrees
            `step_size` -- how much to rotate each iteration, as a percentage
            `agl_threshold` -- a threshold for when the angle is close enough to the target, in degrees
            `vel_threshold` -- a threshold for when the angular velocity is close enough to zero, in degrees/sec
            `max_iter` -- max amount of iterations before stopping
        """

        for _ in range(max_iter):

            in_data = self.reader.read()

            out_data = OutData.from_indata(in_data)

            curr_pitch = in_data.pitch
            curr_roll = in_data.roll

            curr_pitch_rate = in_data.pitch_rate
            curr_roll_rate = in_data.roll_rate

            pitch_done = (abs(curr_pitch - target_pitch) <= agl_thresh and
                          abs(curr_pitch_rate) <= vel_thresh)

            roll_done = (abs(curr_roll - target_roll) <= agl_thresh and
                          abs(curr_roll_rate) <= vel_thresh)

            if pitch_done and roll_done:
                break

            if not pitch_done:
                out_data.elevator = self._get_elevator(curr_pitch, target_pitch, step_size)

            if not roll_done:
                out_data.aileron = self._get_aileron(curr_roll, target_roll, step_size)

            self.writer.write(out_data)
