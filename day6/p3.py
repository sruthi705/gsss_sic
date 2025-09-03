states = ['Tamil Nadu', 'Kerala', 'Andhra pradesh', 'karnataka', 'Telangana', 'Goa']
capitals = ['Chennai', 'tiruvanathapuram', 'Amaravathi', 'Bengaluru', 'Hyderabad', 'panaji']

print("STATE", (" " * 20), "CAPITALS")
print("-" * 50)

for state, capital in zip(states, capitals):
    print(state.ljust(25), capital)