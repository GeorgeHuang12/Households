from battery import Battery, battery_setting

class Household:
    def __init__(self, h_id: int, avg_demand: float):
        self.h_id = h_id

        battery_capacity_kwh, max_charge_kw, max_discharge_kw = battery_setting(avg_demand)
        self.h_id = h_id
        self.battery = Battery(capacity_kwh=battery_capacity_kwh, max_charge_kw=max_charge_kw, max_discharge_kw = max_discharge_kw)


    def run_slot(self, demand: float, pv: float, t_h: float) -> dict:
        energy_before =  demand - pv
        battery_charged = 0.0 #energy abosorbed by battery
        battery_discharged = 0.0 #energy delivered by battery

        reserve_soc = 0.5

        if energy_before > 0: #if energy defict, discharge battery
            power = energy_before / t_h #change from energy to power
            battery_discharged  = self.battery.discharge(power, t_h)
        
        elif energy_before < 0: #if energy surplus, charge battery
            surplus = abs(energy_before)

            if self.battery.soc < reserve_soc:
                power = surplus / t_h
                battery_charged = self.battery.charge(power, t_h)
        
        energy_after = demand - pv - battery_discharged + battery_charged #calculate final energy after discharged or charged from battery

        #both won't happen if energy after = 0
        import_energy = max(0.0, energy_after) #if energy after is postive, import from grid
        export_energy = max(0.0, -energy_after) #if energy after is negative, export from grid

        return {
            "h_id": self.h_id,
            "demand": demand,
            "pv": pv,
            "battery_charged": battery_charged,
            "battery_discharged": battery_discharged,
            "energy_before": energy_before,
            "energy_after": energy_after,
            "import_energy": import_energy,
            "export_energy": export_energy,
            "soc": self.battery.soc
        }
