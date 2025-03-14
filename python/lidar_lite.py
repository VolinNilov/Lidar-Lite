import smbus
import time
import keyboard
import matplotlib.pyplot as plt

class Lidar_Lite():
  def __init__(self):
    self.address = 0x62
    self.distWriteReg = 0x00
    self.distWriteVal = 0x04
    self.distReadReg1 = 0x8f
    self.distReadReg2 = 0x10
    self.velWriteReg = 0x04
    self.velWriteVal = 0x08
    self.velReadReg = 0x09

  def connect(self, bus):
    try:
      self.bus = smbus.SMBus(bus)
      time.sleep(0.5)
      return 0
    except:
      return -1

  def writeAndWait(self, register, value):
    self.bus.write_byte_data(self.address, register, value);
    time.sleep(0.02)

  def readAndWait(self, register):
    res = self.bus.read_byte_data(self.address, register)
    time.sleep(0.02)
    return res

  def readDistAndWait(self, register):
    res = self.bus.read_i2c_block_data(self.address, register, 2)
    time.sleep(0.02)
    return (res[0] << 8 | res[1])

  def getDistance(self):
    self.writeAndWait(self.distWriteReg, self.distWriteVal)
    dist = self.readDistAndWait(self.distReadReg1)
    return dist

  def getVelocity(self):
    self.writeAndWait(self.distWriteReg, self.distWriteVal)
    self.writeAndWait(self.velWriteReg, self.velWriteVal)
    vel = self.readAndWait(self.velReadReg)
    return self.signedInt(vel)

  def signedInt(self, value):
    if value > 127:
      return (256-value) * (-1)
    else:
      return value

  def exit_requested(self, key):
      """
      Checks whether the specified key has been pressed.
      Returns True if the key has been pressed.

      :param key: String representing the key to check (e.g., 'q', 'esc')
      :raises TypeError: If the key parameter is not a string

      Use example:
        try:
          print ("Start reading data ...")
          while not lidar.exit_requested('q'):
              if connected < -1:
                  print("Not Connected")
              print(lidar.getDistance())
              print(lidar.getVelocity())
          print ("END.")
        except Exception as e:
          print ("END.")
          print(f"Error: {e}")
      """
      if not isinstance(key, str):
          raise TypeError("Key parameter must be a STRING")
      
      return keyboard.is_pressed(key)

  def generate_graph(time_stamps, distances_array, velocities_array):
      """
      Creates and saves two graphs on one image:
      1. Distance vs. time
      2. Velocity vs. time

      :param time_stamps: list of timestamps
      :param distances_array: list of distance values
      :param velocities_array: list of velocity values
      """
      try:
          # Data verification
          if not all([len(time_stamps), len(distances_array), len(velocities_array)]):
              raise ValueError("One of the data arrays is empty.")
          if not (len(time_stamps) == len(distances_array) == len(velocities_array)):
              raise ValueError("The data arrays have different lengths.")

          # Create an image
          plt.figure(figsize=(12, 8))
          
          # Distance graph
          plt.subplot(2, 1, 1)
          plt.plot(time_stamps, distances_array, 'b-', linewidth=1.5)
          plt.title('Distance Measurement', fontsize=12)
          plt.xlabel('Time, seconds', fontsize=10)
          plt.ylabel('Distance, cm', fontsize=10)
          plt.grid(True, linestyle='--', alpha=0.7)
          plt.tick_params(axis='both', which='major', labelsize=9)

          # Velocity ​​graph
          plt.subplot(2, 1, 2)
          plt.plot(time_stamps, velocities_array, 'r-', linewidth=1.5)
          plt.title('Velocity Measurement', fontsize=12)
          plt.xlabel('Time, seconds', fontsize=10)
          plt.ylabel('Velocity, cm/s', fontsize=10)
          plt.grid(True, linestyle='--', alpha=0.7)
          plt.tick_params(axis='both', which='major', labelsize=9)

          # Formatting and saving
          plt.tight_layout(pad=3.0)
          current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
          plot_name = f"graph/lidar_plot_{current_time}.png"
          
          plt.savefig(plot_name, dpi=300, bbox_inches='tight')
          plt.close()
          
          print(f"\nThe graphs were successfully saved as: {plot_name}")

      except Exception as e:
          print(f"Error generating graphs: {str(e)}")
          raise