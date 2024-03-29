import pathlib
import Environment as env
import importlib
import sys

# 'dut_dir': directory where you store your LBoS source files
# dut_dir = "./Week1/"
# dut_dir = "./Week2/"
# dut_dir = "./Week3/"
# dut_dir = "Week4/"
# dut_dir = "./Week5/"
# dut_dir = "./TestSolutions/"
# dut_dir = "./BookSolution/"
# dut_dir = "./Practice/"
dut_dir = ""

# 'myDut': Device Under Test, a python file with '.py' must exist in 'dut_dir'
# myDut = "Dut_ConditionVariable"
# myDut = "Dut37_ReusableBarrier_SemOnly"
myDut = "Dut64_ModusHall_ConVar_Error2"
# myDut = "Dut44_5_DiningPhilosophers_Tanenbaum"
# myDut = "Dut44_DiningPhilosophers_CondVar"
# myDut = "Dut42_ReaderWriter_CondVar"
# myDut = "Dut_Racecondition"
# myDut = "Dut64_ModusHall_Original"
# myDut = "Dut64_ModusHall_CondVar"
# myDut = "Dut62_Unisex_NoStarvation_CondVar"

if __name__ == '__main__':
    sys.path.append(dut_dir)

    dut = importlib.import_module(myDut)
    dut.setup()
    env.GuiCreate(pathlib.Path(dut_dir, myDut + ".py"))

    env.GuiMainloop()
