lines = []
l = -1
vars = []
import os
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

os.system("pip install colorama")

def code(code):
    # with open(f"modules.mits", "r", encoding="utf-8") as f:
    #     for line in f:
    #         if line != "\n":
    #             lines.append(line.replace("\n", ""))
    #     print(lines)
    #     if "__MitsLoader__" in lines:
    #         pass
    #     else:
    #         print("\33[31mFile can't be launched, missing init point key.")
    #         exit()

    def calc(fileline, calc):
        try:
            result = eval(f"{calc}")
            print(str(result).replace("None", ""))
            return result
        except Exception as e:
            print(Fore.RED + f"Line {fileline} error :\n'{calc}' can't be calculed.")
            exit()

    def CheckVar(fileline, var):
        splited_var = var.split(" ")
        if splited_var[0].endswith(":"):
            VarContent = var.replace(splited_var[0], "")
            if '"' in VarContent:
                InitVar("-1", splited_var[0].replace(":", ""), VarContent, tp="lt")
            else:
                if "*" in VarContent or "/" in VarContent or "+" in VarContent or "-" in VarContent:
                    InitVar("-1", splited_var[0].replace(":", ""), VarContent, tp="calc")

    def InitVar(fileline, varname, content, tp="lt"):
        if tp == "lt":
            vars.append(varname + " $£" + content)
        elif tp == "calc":
            vars.append(f"{varname} $£ {eval(str(content.replace(' ', '')))}")

    def DelVar(fileline, var):
        try:
            v = vars.index(var)
            pass
        except:
            print(Fore.RED + f"Line {fileline} error :\nVar '{var}' can't be found.")
            exit()

    def UseVar(varname):
        varname = varname.replace(" ", "")
        for element in vars:
            if varname in element:
                print(element.split("$£")[1].replace('"', ''))
                return

        print(Fore.RED + f"Line -1 error :\nVar '{varname}' can't be found.")

    def say(fileline, line):
        tosay = line.replace("say;", "")
        if '"' in tosay:
            tosay= tosay.replace('"', '')
            print(tosay)
            return tosay
        elif "{" in line and "}" in line:
            tosay = tosay.replace("{", '').replace("}", "")
            if "calc;" in line:
                tosay = tosay.replace("calc;", '').replace(" ", "")
                calc("-1", tosay)
            elif ":" in line:
                tosay = tosay.replace(":", "")
                UseVar(tosay)

    if code.startswith("--") and code.endswith("--"):
        pass
    if code.startswith("say;"):
        say(l, code)
    if code.startswith("del;"):
        DelVar(l, code.split(";")[0])
    if ":" in code:
        CheckVar(l, code)