
set devicefamily @DEVICE_FAMILY@
set device @DEVICE@

set_global_assignment -name FAMILY $devicefamily
set_global_assignment -name DEVICE $device
set_global_assignment -name TOP_LEVEL_ENTITY @TOP_LEVEL_ENTITY@
set_global_assignment -name SDC_FILE @SDC_FILE@
