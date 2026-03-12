from battery import Battery

b = Battery()

print("Initial SOC:", b.soc)

stored = b.charge(power = 3.0, t_h=1)
print("Stored:", stored)
print("SOC after charge:", b.soc)

delivered = b.discharge(power = 2.0, dt_h=1)
print("Delivered:", delivered)
print("SOC after discharge:", b.soc)