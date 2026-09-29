import time
from time import sleep

from dexcap import *


def main():
    dexcap_suit = DexCapSuit(AdapterType.WIREDUSB)
    if dexcap_suit.is_available() is not True:
        print('DexCapSuit instance created failed')
        return

    wde = WiredDeviceEnumerator()
    dev_candidates_count = wde.number_of_device_candidates()
    print('There are {} USB devices may be DexCap product'.format(dev_candidates_count))

    suit_available = False
    device_candidates = wde.get_device_candidates()
    for adapter_name in device_candidates:
        device_type = dexcap_suit.connect(adapter_name)
        if device_type is DeviceType.UnDefn:
            print('Device {} is not recognized as a DexCap device, either this device is busy, not working or malfunctioning'.format(adapter_name))
            continue

        print('Device {} is connected, Device Type: {}'.format(adapter_name, device_type.name))
        suit_available = True

    if not suit_available:
        return

    return_code = dexcap_suit.start_sampling()
    if return_code is not DexReturn.DEX_SUCCESS and return_code is not DexReturn.DEX_SUCCESS_WITH_INFO:
        print('Sampling starts failed')
        return

    timeout = False
    start_ts = time.time()
    while not timeout:
        suit_status_data = dexcap_suit.get_status_data()
        if suit_status_data[0] is not True:
            continue

        data = suit_status_data[1]
        print('[L Arm]: ', end=' ')
        print('jnt1={}, jnt2={}, jnt3={}, jnt4={}, jnt5={}, jnt6={}, jnt7={}'
              .format(data.jointData.LArm1,
                      data.jointData.LArm2,
                      data.jointData.LArm3,
                      data.jointData.LArm4,
                      data.jointData.LArm5,
                      data.jointData.LArm6,
                      data.jointData.LArm7), end='\n')

        print('[R Arm]: ', end=' ')
        print('jnt1={}, jnt2={}, jnt3={}, jnt4={}, jnt5={}, jnt6={}, jnt7={}'
              .format(data.jointData.RArm1,
                      data.jointData.RArm2,
                      data.jointData.RArm3,
                      data.jointData.RArm4,
                      data.jointData.RArm5,
                      data.jointData.RArm6,
                      data.jointData.RArm7), end='\n')

        print('[L Joy]: ', end=' ')
        print('RockerX={}, RockerY={}, RockerZ={}'.format(data.jointData.LJoyS.RockerX,
                                                          data.jointData.LJoyS.RockerY,
                                                          data.jointData.LJoyS.RockerZ), end='\n')

        print('[R Joy]: ', end=' ')
        print('RockerX={}, RockerY={}, RockerZ={}'.format(data.jointData.RJoyS.RockerX,
                                                          data.jointData.RJoyS.RockerY,
                                                          data.jointData.RJoyS.RockerZ), end='\n')

        print('[Sys Stat]: ', end=' ')
        print('L JoyStick={}, R JoyStick={}, Wifi={}'.format('Connected' if data.systemStatus.LJoyConn else 'NOT Connected',
                                                             'Connected' if data.systemStatus.RJoyConn else 'NOT Connected',
                                                             'Connected' if data.systemStatus.WifiState else 'NOT Connected'), end='\n')

        print('Battery Curr={}, Battery Voltage={}, Battery Temper={}'.format(data.mainBatteryState.Currency,
                                                             data.mainBatteryState.Voltage,
                                                             data.mainBatteryState.Temperature), end='\n')

        print('=============================================\n')

        duration = time.time() - start_ts
        timeout = duration >= 30
        sleep(0.1)

    dexcap_suit.stop_sampling()
    dexcap_suit.disconnect()


if __name__ == '__main__':
    main()
