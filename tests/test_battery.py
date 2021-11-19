from PowerModels.PowerTrain.Battery import Battery

def test_battery():
    controls = [0.2, 0.2, 0.2, 0.2]
    batt = Battery(25.0, 0, 0.004 / 3600)
    voltage, dod = batt.new_control(controls) # List of [0-1] values [0.00001, ..., 0.999999]
    print(voltage, dod)