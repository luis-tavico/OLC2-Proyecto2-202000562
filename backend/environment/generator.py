class Generator:
    def __init__(self):
        self.Temporal = 0
        self.Label = 0
        self.Code = []
        self.Data = []
        self.FinalCode = []
        self.Natives = []
        self.FuncCode = []
        self.TempList = []
        self.PrintStringFlag = True
        self.ConcatStringFlag = True
        self.BreakLabel = ""
        self.BreakLabels = []
        self.ContinueLabels = []
        self.ContinueLabel = ""
        self.MainCode = False

    def get_code(self):
        return self.Code

    def get_final_code(self):
        self.add_headers()
        self.add_footers()
        outstring = "".join(self.Code)
        outstring += "".join(self.FuncCode)
        return outstring
    
    def add_functions_code(self, code):
        self.FuncCode += code

    def call_function(self, name):
        self.Code.append(f"\tjal ra, {name}\n")

    def add_end_function(self):
        self.Code.append("\tret\n")

    def get_temps(self):
        return self.TempList

    def add_break(self, lvl):
        self.BreakLabel = lvl

    def add_code(self, code):
        self.Code.append(code)
    
    def add_data_code(self, code):
        self.Data.append(code)

    def add_continue(self, lvl):
        self.ContinueLabel = lvl

    def new_temp(self):
        self.Temporal += 4
        return self.Temporal

    def new_label(self):
        temp = self.Label
        self.Label += 1
        return "L" + str(temp)

    def add_br(self):
        self.Code.append("\n")

    def comment(self, txt):
        self.Code.append(f"### {txt} \n")

    def variable_data(self, name, type, value):
        self.Data.append(f"{name}: .{type} {value} \n")

    def add_li(self, left, right):
        self.Code.append(f"\tli {left}, {right}\n")

    def add_la(self, left, right):
        self.Code.append(f"\tla {left}, {right}\n")

    def add_lw(self, left, right):
        self.Code.append(f"\tlw {left}, {right}\n")

    def add_sw(self, left, right):
        self.Code.append(f"\tsw {left}, {right}\n")

    def add_slli(self, target, left, right):
        self.Code.append(f"\tslli {target}, {left}, {right}\n")

    def add_blt(self, left, right, target):
        self.Code.append(f"\tblt {left}, {right}, {target}\n")

    def add_bgt(self, left, right, target):
        self.Code.append(f"\tbgt {left}, {right}, {target}\n")

    def add_bge(self, left, right, target):
        self.Code.append(f"\tbge {left}, {right}, {target}\n")

    def add_ble(self, left, right, target):
        self.Code.append(f"\tble {left}, {right}, {target}\n")

    def add_beq(self, left, right, target):
        self.Code.append(f"\tbeq {left}, {right}, {target}\n")

    def add_bne(self, left, right, target):
        self.Code.append(f"\tbne {left}, {right}, {target}\n")

    def add_jump(self, lvl):
        self.Code.append(f"\tj {lvl}\n")

    def new_body_label(self, lvl):
        self.Code.append(f"\t{lvl}:\n")

    def add_move(self, left, right):
        self.Code.append(f"\tmv {left}, {right}\n")

    def add_operation(self, operation, target, left, right):
        self.Code.append(f"\t{operation} {target}, {left}, {right}\n")

    def add_system_call(self):
        self.Code.append('\tecall\n')

    def add_function(self, name):
        self.Code.append(f"\n{name}:\n")

    def add_headers(self):
        self.Code.insert(0,'\n.text\n.globl _start\n\n_start:\n')
        self.Data.insert(0,'.data\n')
        self.variable_data('str_number', 'string', '\"number\"')
        self.variable_data('str_string', 'string', '\"string\"')
        self.variable_data('str_boolean', 'string', '\"boolean\"')
        self.variable_data('str_true', 'string', '\"true\"')
        self.variable_data('str_false', 'string', '\"false\"')
        self.variable_data('str_l_sq_bt', 'string', '\"[\"')
        self.variable_data('str_r_sq_bt', 'string', '\"]\"')
        self.Code[:0] = self.Data
            
    def add_footers(self):
        self.Code.append('\n\tli a0, 0\n')
        self.Code.append('\tli a7, 93\n')
        self.Code.append('\tecall\n')