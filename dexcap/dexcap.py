from ctypes import *
from .typedefs import *


class DexCapSuit:
    def __init__(self, adapter_type: AdapterType):
        self.instance = DEXCAP_SUIT_HANDLE()
        self.available = False
        self.adapter_type = adapter_type

        LibDexCapSuit.dexcap_create_suit_instance.argtypes = [ctypes.POINTER(DEXCAP_SUIT_HANDLE)]
        LibDexCapSuit.dexcap_create_suit_instance.restype = c_int

        LibDexCapSuit.dexcap_connect.argtypes = [c_void_p, c_char_p, DeviceType_c_ptr]
        LibDexCapSuit.dexcap_connect.restype = c_int

        LibDexCapSuit.dexcap_is_device_connected.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_is_device_connected.restype = c_bool

        LibDexCapSuit.dexcap_disconnect.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_disconnect.restype = c_int

        LibDexCapSuit.dexcap_start_sampling.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_start_sampling.restype = c_int

        LibDexCapSuit.dexcap_is_sampling_started.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_is_sampling_started.restype = c_bool

        LibDexCapSuit.dexcap_stop_sampling.argtypes = [c_void_p]
        LibDexCapSuit.dexcap_stop_sampling.restype = c_int

        LibDexCapSuit.dexcap_get_status_data.argtypes = [c_void_p, SUT_DATA_PTR]
        LibDexCapSuit.dexcap_get_status_data.restype = c_int

        LibDexCapSuit.dexcap_get_main_battery_state.argtypes = [c_void_p, BAT_DATA_PTR]
        LibDexCapSuit.dexcap_get_main_battery_state.restype = c_int

        LibDexCapSuit.dexcap_get_system_status.argtypes = [c_void_p, SYS_DATA_PTR]
        LibDexCapSuit.dexcap_get_system_status.restype = c_int

        LibDexCapSuit.dexcap_get_diagnostics.argtypes = [c_void_p, POINTER(c_int), c_char_p, c_uint64, POINTER(c_uint64)]
        LibDexCapSuit.dexcap_get_diagnostics.restype = c_int

        ret_code = LibDexCapSuit.dexcap_create_suit_instance(ctypes.byref(self.instance), self.adapter_type)
        self.available = (DexReturn(ret_code) is DexReturn.DEX_SUCCESS)

    def __del__(self):
        return

    def is_available(self):
        return self.available

    def get_adapter_type(self):
        return self.adapter_type

    def connect(self, adapter_name: str) -> DeviceType:
        device_type  = DeviceType_c(DeviceType.UnDefn.value)
        adapter_name_b = adapter_name.encode('utf-8')
        return_code = DexReturn(LibDexCapSuit.dexcap_connect(self.instance,
                                                             ctypes.c_char_p(adapter_name_b),
                                                             ctypes.byref(device_type)))

        if return_code is DexReturn.DEX_SUCCESS:
            actual_type = DeviceType(device_type.value)
            if actual_type is DeviceType.UpBody or actual_type is DeviceType.JSBody:
                return actual_type

        return DeviceType.UnDefn

    def disconnect(self) -> DexReturn:
        return LibDexCapSuit.dexcap_disconnect(self.instance)

    def is_device_connected(self) -> bool:
        return LibDexCapSuit.dexcap_is_device_connected(self.instance)

    def start_sampling(self) -> DexReturn:
        return_code = DexReturn(LibDexCapSuit.dexcap_start_sampling(self.instance))
        return return_code

    def is_sampling_started(self) -> bool:
        return LibDexCapSuit.dexcap_is_sampling_started(self.instance)

    def stop_sampling(self) -> DexReturn:
        return DexReturn(LibDexCapSuit.dexcap_stop_sampling(self.instance))

    def get_status_data(self) -> (bool, SuitStatusData):
        data = SuitStatusData()
        data_ptr = SUT_DATA_PTR(data)
        return_code = DexReturn(LibDexCapSuit.dexcap_get_status_data(self.instance, data_ptr))
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_main_battery_state(self) -> (bool, MainBatteryState):
        data = MainBatteryState()
        data_ptr = BAT_DATA_PTR(data)
        return_code = DexReturn(LibDexCapSuit.dexcap_get_main_battery_state(self.instance, data_ptr))
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_system_status(self) -> (bool, SystemStatus):
        data = SystemStatus()
        data_ptr = SYS_DATA_PTR(data)
        return_code = DexReturn(LibDexCapSuit.dexcap_get_system_status(self.instance, data_ptr))
        if return_code is DexReturn.DEX_SUCCESS:
            return True, data

        return False, data

    def get_diagnostics(self) -> (int, str):
        err_code = ctypes.c_int(0)
        err_info = str()
        err_info_p = ctypes.c_char_p(err_info.encode('utf-8'))
        err_info_len = ctypes.c_uint64(128)
        LibDexCapSuit.dexcap_get_diagnostics(self.instance,
                                             byref(err_code),
                                             err_info_p,
                                             128,
                                             byref(err_info_len))

        return err_code.value, err_info
