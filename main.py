from logo_ce import command_engine
ce = command_engine()

while(True):
    if ce.onPC:
        ce.pu()
        while(True):
            ce.run_command(input("?"),ce)
    else:
        ce.pu() 
        while(True):
            ce.bluetooth(ce)