
from dataclasses import dataclass

@dataclass 
class Battery:  
    capacity_kwh : float = 10.0
    soc : float = 0.5 # state of charge(from 0 to 1.0)
    max_charge_kw : float = 3.0
    max_discharge_kw : float = 3.0
    eff : float = 0.95
    soc_max : float = 0.95
    soc_min : float = 0.2

    def stored_energy(self) -> float: #function for stored energy at any time
        return self.soc * self.capacity_kwh #current stored energy = soc times capacity 
    
    def charge(self, power: float, t_h: float) -> float: #charge function
        power = min(max(power, 0.0), self.max_charge_kw) #keep charge between 0 and max charge
        
        current_energy =  self.stored_energy() 
        max_allowed = self.soc_max * self.capacity_kwh #battery allowed storage
        room_left =  max_allowed - current_energy #storage left in battery

        if room_left <= 0.0:
            return 0.0
        
        energy_in = power * t_h
        energy_stored =  energy_in * self.eff
        actual_stored = min(energy_stored,room_left) #only store based on how much room is left

        self.soc += actual_stored /self.capacity_kwh #update the state of soc
        return actual_stored #return amount of energy stored 
    
    def discharge(self, power: float, t_h: float) -> float: #discharge function
        power = min(max(power, 0.0), self.max_discharge_kw)

        current_energy = self.stored_energy()
        min_allowed = self.soc_min * self.capacity_kwh
        available_energy = current_energy - min_allowed

        if available_energy <= 0.0 :
            return  0.0
        
        energy_out = power * t_h
        energy_removed = energy_out /self.eff
        actual_removed = min(energy_removed,available_energy)
        actual_delivered = actual_removed * self.eff

        self.soc -=actual_removed /self.capacity_kwh
        return actual_delivered
    


        
        





