import sys
import ctypes
import platform
from enum import IntEnum

if sys.platform.startswith('win'):
    LibDexCapSuit = ctypes.cdll.LoadLibrary("../contrib/dexcap-sdk-cpp/libs/windows/DexCap.dll")
else:
    LibDexCapSuit = ctypes.cdll.LoadLibrary(f"../contrib/dexcap-sdk-cpp/libs/linux/{platform.machine()}/libDexCap.so")

class AdapterType(IntEnum):
    """Supported connection adapters"""
    INVALID   = 0x00
    WIREDUSB  = 0x01
    WIRELESS  = 0x02
    COMMONUSB = 0x03
    BLUETOOTH = 0x04
    MODBUSUSB = 0x06


class DeviceType(IntEnum):
    UnDefn = 0x00
    LGlove = 0x01
    RGlove = 0x02
    UpBody = 0x04
    JSBody = 0x0A
    IMUnit = 0x08
    WRecvr = 0x20


class DexReturn(IntEnum):
    DEX_ERROR = -1,
    DEX_INVALID_DEVICE = -2,
    DEX_INVALID_INSTANCE = -3,
    DEX_INVALID_DATA_FMT = -4,
    DEX_DEV_TYPE_MISMATCH = -5,

    DEX_SUCCESS = 0,
    DEX_SUCCESS_WITH_INFO = 1,
    DEX_REQUEST_TIMEOUT = 2,
    DEX_SEC_ON_WITHOUT_KEY = 3,
    DEX_BLE_CONN_UNSECURED = 4,
    DEX_STRING_TRUNCATED = 6,
    DEX_NO_DATA = 100,


class Joystick(ctypes.Structure):
    _fields_ = [
        ("RockerX", ctypes.c_uint16, 16),
        ("RockerY", ctypes.c_uint16, 16),
        ("TgrDistA", ctypes.c_uint16, 16),
        ("TgrDistB", ctypes.c_uint16, 16),
        ("ButtonA", ctypes.c_uint8, 1),
        ("ButtonB", ctypes.c_uint8, 1),
        ("RockerZ", ctypes.c_uint8, 1),
        ("TriggerA", ctypes.c_uint8, 1),
        ("TriggerB", ctypes.c_uint8, 1),
        ("Reserved", ctypes.c_uint16, 11),
    ]

class SkeletonArmsData(ctypes.Structure):
    _fields_ = [
        ("LArm1", ctypes.c_uint16),
        ("LArm2", ctypes.c_uint16),
        ("LArm3", ctypes.c_uint16),
        ("LArm4", ctypes.c_uint16),
        ("LArm5", ctypes.c_uint16),
        ("LArm6", ctypes.c_uint16),
        ("LArm7", ctypes.c_uint16),
        ("RArm1", ctypes.c_uint16),
        ("RArm2", ctypes.c_uint16),
        ("RArm3", ctypes.c_uint16),
        ("RArm4", ctypes.c_uint16),
        ("RArm5", ctypes.c_uint16),
        ("RArm6", ctypes.c_uint16),
        ("RArm7", ctypes.c_uint16),
        ("LJoyS", Joystick),
        ("RJoyS", Joystick),
        ("timestamp", ctypes.c_uint64),
    ]

class MainBatteryState(ctypes.Structure):
    _fields_ = [
        ("Currency",     ctypes.c_int16),
        ("Voltage",      ctypes.c_uint16),
        ("RemainPower",  ctypes.c_uint16),
        ("Temperature",  ctypes.c_uint16),
        ("StatusBitmap", ctypes.c_uint16),
        ("Reserved", ctypes.c_uint16),
    ]

class SystemStatus(ctypes.Structure):
    _fields_ = [
        ("Enabled", ctypes.c_bool, 1),
        ("Reserved1", ctypes.c_ubyte, 2),
        ("WifiState", ctypes.c_bool, 1),
        ("BootState", ctypes.c_bool, 1),
        ("NeedCharge", ctypes.c_bool, 1),
        ("UDPState", ctypes.c_bool, 1),
        ("LJoyConn", ctypes.c_bool, 1),
        ("RJoyConn", ctypes.c_bool, 1),
        ("Reserved2", ctypes.c_bool, 7),
    ]

class SuitStatusData(ctypes.Structure):
    _fields_ = [
        ("jointData", SkeletonArmsData),
        ("mainBatteryState", MainBatteryState),
        ("systemStatus", SystemStatus),
    ]


DEXCAP_SUIT_HANDLE = ctypes.c_void_p
SUT_DATA_PTR = ctypes.POINTER(SuitStatusData)
BAT_DATA_PTR = ctypes.POINTER(MainBatteryState)
SYS_DATA_PTR = ctypes.POINTER(SystemStatus)

AdapterType_c = ctypes.c_int
DeviceType_c = ctypes.c_int
DeviceType_c_ptr = ctypes.POINTER(DeviceType_c)
