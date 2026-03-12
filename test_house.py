from agent import Household

h = Household(h_id=1)

print("Test 1: deficit case")
result1 = h.run_slot(demand=1.5, pv=0.4, t_h=0.5)
print(result1)

print("\nTest 2: surplus case")
result2 = h.run_slot(demand=0.5, pv=1.4, t_h=0.5)
print(result2)