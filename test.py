import pickle

user_balances = {}

filename = "balances"
outfile = open(filename, "wb")
pickle.dump(user_balances, outfile)
outfile.close()
print("File created")