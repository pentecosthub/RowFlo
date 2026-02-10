"""
FTMS (Fitness Machine Service) Rower Implementation
Implements Bluetooth FTMS protocol for rowing machines
"""

import dbus
import dbus.service
from adapters.ble import ble
import struct
import logging

logger = logging.getLogger(__name__)

# FTMS Service and Characteristic UUIDs
FTMS_SERVICE_UUID = "00001826-0000-1000-8000-00805f9b34fb"
ROWER_DATA_UUID = "00002ad1-0000-1000-8000-00805f9b34fb"
FITNESS_MACHINE_FEATURE_UUID = "00002acc-0000-1000-8000-00805f9b34fb"
FITNESS_MACHINE_CONTROL_POINT_UUID = "00002ad9-0000-1000-8000-00805f9b34fb"
FITNESS_MACHINE_STATUS_UUID = "00002ada-0000-1000-8000-00805f9b34fb"


class FTMSRowerDataCharacteristic(ble.Characteristic):
    """
    FTMS Rower Data Characteristic (UUID 0x2AD1)
    Notifies connected devices with rowing data
    """
    
    def __init__(self, bus, index, service):
        ble.Characteristic.__init__(
            self, bus, index, ROWER_DATA_UUID,
            ["notify"], service
        )
        self.notifying = False
        
    def encode_rower_data(self, metrics):
        """
        Encode rowing metrics into FTMS Rower Data format
        
        Format (little-endian):
        - Flags (2 bytes)
        - Stroke Rate (1 byte) - strokes per minute
        - Stroke Count (2 bytes) - total strokes
        - Total Distance (3 bytes) - meters
        - Instantaneous Pace (2 bytes) - seconds per 500m
        - Average Pace (2 bytes) - seconds per 500m
        - Instantaneous Power (2 bytes) - watts
        - Average Power (2 bytes) - watts
        - Resistance Level (2 bytes)
        - Total Energy (2 bytes) - kcal
        - Energy Per Hour (2 bytes) - kcal/hour
        - Energy Per Minute (1 byte) - kcal/minute
        - Heart Rate (1 byte) - bpm (optional)
        - Metabolic Equivalent (1 byte) - 0.1 MET resolution
        - Elapsed Time (2 bytes) - seconds
        - Remaining Time (2 bytes) - seconds
        """
        
        # Flags determine which fields are present
        # For now, we'll include the most common fields
        flags = 0x0000
        flags |= (1 << 0)  # More Data (not used for rower)
        flags |= (1 << 1)  # Average Stroke present
        flags |= (1 << 2)  # Total Distance Present
        flags |= (1 << 3)  # Instantaneous Pace present
        flags |= (1 << 4)  # Average Pace Present
        flags |= (1 << 5)  # Instantaneous Power present
        flags |= (1 << 6)  # Average Power present
        flags |= (1 << 7)  # Resistance Level present
        flags |= (1 << 8)  # Total Energy present
        flags |= (1 << 9)  # Energy Per Hour present
        flags |= (1 << 10) # Energy Per Minute present
        flags |= (1 << 11) # Heart Rate present
        flags |= (1 << 12) # Metabolic Equivalent present
        flags |= (1 << 13) # Elapsed Time present
        flags |= (1 << 14) # Remaining Time present
        
        # Extract metrics with defaults
        stroke_rate = int(metrics.get('stroke_rate', 0))  # strokes/min
        stroke_count = int(metrics.get('stroke_count', 0))
        total_distance = int(metrics.get('total_distance', 0))  # meters
        inst_pace = int(metrics.get('instantaneous_pace', 0))  # seconds per 500m
        avg_pace = int(metrics.get('average_pace', 0))  # seconds per 500m
        inst_power = int(metrics.get('instantaneous_power', 0))  # watts
        avg_power = int(metrics.get('average_power', 0))  # watts
        resistance = int(metrics.get('resistance_level', 0))
        total_energy = int(metrics.get('total_energy', 0))  # kcal
        energy_per_hour = int(metrics.get('energy_per_hour', 0))  # kcal/hour
        energy_per_minute = int(metrics.get('energy_per_minute', 0))  # kcal/min
        heart_rate = int(metrics.get('heart_rate', 0))  # bpm
        metabolic_eq = int(metrics.get('metabolic_equivalent', 10))  # 0.1 MET
        elapsed_time = int(metrics.get('elapsed_time', 0))  # seconds
        remaining_time = int(metrics.get('remaining_time', 0))  # seconds
        
        # Pack data (little-endian format)
        data = struct.pack('<HBHIHHhhhhHHBBBHH',
            flags,
            stroke_rate,
            stroke_count,
            total_distance & 0xFFFFFF,
            inst_pace,
            avg_pace,
            inst_power,
            avg_power,
            resistance,
            total_energy,
            energy_per_hour,
            energy_per_minute,
            heart_rate,
            metabolic_eq,
            elapsed_time,
            remaining_time
        )        
        return list(data)
    
    def update_rower_data(self, metrics):
        """Update and notify with new rower data"""
        if self.notifying:
            value = self.encode_rower_data(metrics)
            self.PropertiesChanged(ble.GATT_CHRC_IFACE, {"Value": value}, [])
    
    def StartNotify(self):
        if self.notifying:
            return
        self.notifying = True
        logger.info("FTMS Rower Data notifications started")

    def StopNotify(self):
        if not self.notifying:
            return
        self.notifying = False
        logger.info("FTMS Rower Data notifications stopped")


class FitnessMachineFeatureCharacteristic(ble.Characteristic):
    """
    Fitness Machine Feature Characteristic (UUID 0x2ACC)
    Describes capabilities of the fitness machine
    """
    
    def __init__(self, bus, index, service):
        ble.Characteristic.__init__(
            self, bus, index, FITNESS_MACHINE_FEATURE_UUID,
            ["read"], service
        )
    
    def ReadValue(self, options):
        """
        Return supported features
        
        Fitness Machine Features (8 bytes):
        - Bytes 0-3: Fitness Machine Features
        - Bytes 4-7: Target Setting Features
        """
        # Fitness Machine Features
        features = 0x00000000
        features |= (1 << 0)   # Average Speed Supported
        features |= (1 << 1)   # Cadence Supported
        features |= (1 << 2)   # Total Distance Supported
        features |= (1 << 3)   # Inclination Supported
        features |= (1 << 4)   # Elevation Gain Supported
        features |= (1 << 5)   # Pace Supported
        features |= (1 << 6)   # Step Count Supported
        features |= (1 << 7)   # Resistance Level Supported
        features |= (1 << 8)   # Stride Count Supported
        features |= (1 << 9)   # Expended Energy Supported
        features |= (1 << 10)  # Heart Rate Measurement Supported
        features |= (1 << 11)  # Metabolic Equivalent Supported
        features |= (1 << 12)  # Elapsed Time Supported
        features |= (1 << 13)  # Remaining Time Supported
        features |= (1 << 14)  # Power Measurement Supported
        
        # Target Setting Features
        target_settings = 0x00000000
        target_settings |= (1 << 1)  # Resistance Target Supported
        target_settings |= (1 << 3)  # Power Target Supported
        
        value = struct.pack('<II', features, target_settings)
        logger.info("FTMS Feature read: features=0x{:08x}, targets=0x{:08x}".format(
            features, target_settings))
        return list(value)


class FTMSRowerService(ble.Service):
    """
    FTMS Service for Rower
    Main service that contains all FTMS characteristics
    """
    
    def __init__(self, bus, index):
        ble.Service.__init__(self, bus, index, FTMS_SERVICE_UUID, True)
        
        # Add characteristics
        self.rower_data = FTMSRowerDataCharacteristic(bus, 0, self)
        self.add_characteristic(self.rower_data)
        
        self.fitness_machine_feature = FitnessMachineFeatureCharacteristic(bus, 1, self)
        self.add_characteristic(self.fitness_machine_feature)
        
        logger.info("FTMS Rower Service initialized")
    
    def update_metrics(self, metrics):
        """Update rowing metrics and notify clients"""
        self.rower_data.update_rower_data(metrics)


class FTMSRowerApplication(ble.Application):
    """
    FTMS Application
    Container for FTMS services
    """
    
    def __init__(self, bus):
        ble.Application.__init__(self, bus)
        self.ftms_service = FTMSRowerService(bus, 0)
        self.add_service(self.ftms_service)
        logger.info("FTMS Rower Application created")
    
    def update_metrics(self, metrics):
        """Update rowing metrics"""
        self.ftms_service.update_metrics(metrics)


def main(metrics_queue, control_queue):
    """
    Main entry point for FTMS broadcaster
    
    Args:
        metrics_queue: Queue to receive rowing metrics from S4 reader
        control_queue: Queue to receive control commands
    """
    import dbus.mainloop.glib
    from gi.repository import GLib
    
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    
    # Find Bluetooth adapter
    adapter = ble.find_adapter(bus)
    if not adapter:
        logger.error("No Bluetooth adapter found")
        return
    
    logger.info("Using Bluetooth adapter: {}".format(adapter))
    
    # Create FTMS application
    app = FTMSRowerApplication(bus)
    
    # Register GATT application
    adapter_obj = bus.get_object(ble.BLUEZ_SERVICE_NAME, adapter)
    service_manager = dbus.Interface(adapter_obj, ble.GATT_MANAGER_IFACE)
    
    try:
        service_manager.RegisterApplication(
            app.get_path(), {},
            reply_handler=lambda: logger.info("FTMS GATT application registered"),
            error_handler=lambda error: logger.error("Failed to register FTMS: {}".format(error))
        )
    except Exception as e:
        logger.error("Exception registering FTMS GATT: {}".format(e))
        return
    
    # Create and register advertisement
    adv = ble.Advertisement(bus, 0, "peripheral")
    adv.add_service_uuid(FTMS_SERVICE_UUID)
    adv.add_local_name("RowFlo FTMS")
    
    ad_manager = dbus.Interface(adapter_obj, ble.LE_ADVERTISING_MANAGER_IFACE)
    
    try:
        ad_manager.RegisterAdvertisement(
            adv.get_path(), {},
            reply_handler=lambda: logger.info("FTMS advertisement registered"),
            error_handler=lambda error: logger.error("Failed to register advertisement: {}".format(error))
        )
    except Exception as e:
        logger.error("Exception registering advertisement: {}".format(e))
        return
    
    # Main loop to process metrics
    mainloop = GLib.MainLoop()
    
    def process_metrics():
        """Process metrics from queue"""
        try:
            while not metrics_queue.empty():
                metrics = metrics_queue.get_nowait()
                app.update_metrics(metrics)
        except Exception as e:
            logger.error("Error processing metrics: {}".format(e))
        return True
    
    # Poll metrics queue every 100ms
    GLib.timeout_add(100, process_metrics)
    
    try:
        mainloop.run()
    except KeyboardInterrupt:
        mainloop.quit()
    
    logger.info("FTMS service stopped")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import queue
    
    # Test mode
    test_queue = queue.Queue()
    control_queue = queue.Queue()
    
    # Put some test metrics
    test_metrics = {
        'stroke_rate': 20,
        'stroke_count': 100,
        'total_distance': 500,
        'instantaneous_pace': 120,
        'average_pace': 125,
        'instantaneous_power': 150,
        'average_power': 145,
        'total_energy': 50,
        'elapsed_time': 300
    }
    test_queue.put(test_metrics)
    
    main(test_queue, control_queue)
