import asyncio
import threading
import concurrent.futures
import os


from boundary_scan_base import ConnectorBoundaryScanBase
from panduza_platform.extlibs.bsdl import bsdl,bsdlJson
from panduza_platform.log.driver import driver_logger

from pyftdi.ftdi import Ftdi
from pyftdi.jtag import JtagEngine
from pyftdi.bits import BitSequence


###########################################################################
###########################################################################
class BsdlSemantics:
    def map_string(self, ast):
        parser = bsdl.bsdlParser()
        ast = parser.parse(''.join(ast), "port_map")
        return ast

    def grouped_port_identification(self, ast):
        parser = bsdl.bsdlParser()
        ast = parser.parse(''.join(ast), "group_table")
        return ast
    

###########################################################################
###########################################################################

class BitSettingsContainer:
    def __init__(self):
        self.bit_settings = {}


###########################################################################
###########################################################################


def get_bit_settings(bit_state_dict, boundary_reg):
    byte_array = list(boundary_reg)

    for bit in bit_state_dict.keys():

        if bit_state_dict[bit] == 1:
            byte_array[bit] = 1
        else:
            byte_array[bit] = 0
    return BitSequence(byte_array)


def get_bsdl_file(bsdl_folder):
        list_bsdl_files = os.listdir(bsdl_folder)
        bsdl_file_directory = []
        bsdl_file = []
        for i in range(len(list_bsdl_files)):
            bsdl_file_directory.append(os.path.join(bsdl_folder,list_bsdl_files[i]))
            f = open(bsdl_file_directory[i],"r") 
            bsdl_file.append(f.read())

        return bsdl_file

def get_idcode_from_bsdl(bsdl_folder):
        
        parser = bsdl.bsdlParser()
        list_bsdl_files = os.listdir(bsdl_folder)
        bsdl_file = get_bsdl_file(bsdl_folder)
        
        idcode_bsdl= []

        for i in range(len(list_bsdl_files)):
            json = parser.parse(bsdl_file[i], "bsdl_description", semantics=BsdlSemantics(), parseinfo=False).asjson()
            json_bsdl = bsdlJson.BsdlJson(json)

            idcode_bsdl.append(json_bsdl.idcode)
        
        return idcode_bsdl

###########################################################################
###########################################################################
class ConnectorBoundaryScanFtdi(ConnectorBoundaryScanBase):
    """The serial modbus client connector centralize access to a given port as a modbus client
    """

    # Hold instances mutex
    __MUTEX = asyncio.Lock()

    # Contains instances
    __INSTANCES = {}

    ###########################################################################

    # Local logs
    log = driver_logger("ConnectorBoundaryScanFtdi")

    @staticmethod
    async def Get(**kwargs):

        """Singleton main getter
        
        :Keyword Arguments:

        * *usb_vendor* (``str``) --
            ID_VENDOR_ID
        * *usb_model* (``str``) --
            ID_MODEL_ID
        * *usb_serial_short* (``str``) --
            ID_SERIAL_SHORT
        
        """

        # Log
        ConnectorBoundaryScanFtdi.log.debug(f"Get connector for {kwargs}")

        async with ConnectorBoundaryScanFtdi.__MUTEX:
             # Log
            ConnectorBoundaryScanFtdi.log.debug(f"Lock acquired !")
        
            
            if (len(Ftdi.list_devices())) < 1 :
                raise Exception("can't detect the FTDI")
            
            
            if "usb_vendor" in kwargs:
                    usb_vendor = kwargs["usb_vendor"]
            elif "usb_model" in kwargs:
                usb_model = kwargs["usb_model"]
            elif "usb_serial_short" in kwargs:
                usb_serial_short = kwargs["usb_serial_short"] 
            elif "jtag_frequency" in kwargs:
                jtag_frequency = kwargs["jtag_frequency"]
            elif "jtag_bsdl_folder" in kwargs:
                jtag_bsdl_folder = kwargs["jtag_bsdl_folder"] 
            else:
                raise Exception("no way to identify the informations given in tre tree.json")
            
            instance_name = str(f"{usb_vendor}_{usb_model}_{usb_serial_short}")
            

            # Check if instance already exists
            if instance_name in ConnectorBoundaryScanFtdi.__INSTANCES:
                return ConnectorBoundaryScanFtdi.__INSTANCES[instance_name]
            
            try:
                new_instance = ConnectorBoundaryScanFtdi(key=instance_name,               
                                            usb_vendor=usb_vendor,
                                            usb_model=usb_model,
                                            usb_serial_short=usb_serial_short,
                                            jtag_frequency=jtag_frequency,
                                            jtag_bsdl_folder=jtag_bsdl_folder
                                            )
                ConnectorBoundaryScanFtdi.__INSTANCES[instance_name] = new_instance

            except Exception as e:
                raise Exception('Error during initialization').with_traceback(
                    e.__traceback__)

            # Return the newly created instance
            ConnectorBoundaryScanFtdi.log.info(f"Creation of instance {instance_name}")
            return ConnectorBoundaryScanFtdi.__INSTANCES[instance_name]
    

    
    def __init__(self,**kwargs):
        """Constructor
        """

        bit_settings = BitSettingsContainer()

        # Init local mutex
        self._mutex = asyncio.Lock()
        
        # Init Thread
        self.executor = concurrent.futures.ThreadPoolExecutor() #######################

        parser = bsdl.bsdlParser()
        
        # Get paramete/usr/share/code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.htmlrs
        usb_vendor = kwargs.get('usb_vendor', "0403")
        usb_model = kwargs.get('usb_model', "6014")
        jtag_frequency = kwargs.get('jtag_frequency', 6E6)
        jtag_bsdl_folder = kwargs.get('jtag_bsdl_folder', "/home/rethusan/Panduza/panduza-py/platform/deploy/etc_panduza/BSDL")
           
        # Init engine
        self.engine = JtagEngine(frequency=float(jtag_frequency))
        self.engine.configure(f'ftdi://0x{usb_vendor}:0x{usb_model}/1')
        self.engine.reset()

        # Get idcodes
        idcode_bsdl = get_idcode_from_bsdl(jtag_bsdl_folder)       
        idcode_detected = self.idcode()    # retrieve the idcodes in order and store them in a dictionnary (key = device_number ; value = idcode)
        
        self.total_devices = self.scan()

        # Get bsdl files
        bsdl_file = get_bsdl_file(jtag_bsdl_folder)

        idcode = []
        idcode_modified = []

        self.bsdl_dict = {}
        
        # remove the first 4 bits of the idcodes (= idcode without 4-bit version number)
        for n in range (len(idcode_detected)):
            idcode.append(idcode_detected[n])
            idcode_modified.append(hex(int(idcode_detected[n][-7:],16)))    
        
        # store the correct bsdl files in order 
        for j in range(len(idcode_modified)):
            for k in range(len(idcode_bsdl)) :

                if idcode_modified[j] == idcode_bsdl[k]:
                    self.bsdl_dict[j] = bsdl_file[k]


        if (len(self.bsdl_dict) != self.total_devices):
            raise Exception("can't reach bsdl files of some devices")

        # definition of dictionnaries and lists
 
        self.json  = {}             # store the bsdl file convert in json file
        self.json_bsdl  = {}        # in order to use bsdl_lib

        self.bypass_opcode = {}
        self.sample_opcode = {}
        self.extest_opcode = {}

        self.instruct = {}          # the instruction to send at the jtag ftdi

        self.ir_length = []
        self.boundary_length = []


        # Get informations from bsdl files
        for k in sorted(self.bsdl_dict.keys()):
            self.json[k] = parser.parse(self.bsdl_dict.get(k), "bsdl_description", semantics=BsdlSemantics(), parseinfo=False).asjson()
            self.json_bsdl[k] = bsdlJson.BsdlJson(self.json[k])
            
            self.bypass_opcode[k] = self.json_bsdl[k].get_opcode('BYPASS')
            self.extest_opcode[k] = self.json_bsdl[k].get_opcode('EXTEST')
            self.sample_opcode[k] = self.json_bsdl[k].get_opcode('SAMPLE')
            
            self.ir_length.append(self.json_bsdl[k].instruction_length)
            self.boundary_length.append(self.json_bsdl[k].boundary_length)
            self.instruct[k] = (self.bypass_opcode[k],self.ir_length[k])
            
        
        self.length_instruct = sum(self.ir_length)
        self.total_boundary_length = sum(self.boundary_length)

        
        self.init_bit_settings()


    ###########################################################################
    ###########################################################################


    async def read_number_of_devices(self):
        """
        """
        async with self._mutex:
            #self.scan()
            
            # t = threading.Thread(target=self.scan)
            # t.start()
            # #t.join()
            # while t.is_alive():
            #      await asyncio.sleep(0.1)
            #      print("Waiting for the thread to complete...")

            # print("finished")

             with self.executor as executor :
                # Submit the scan function to the executor
                future = executor.submit(self.scan)
                
                # Wait for the future to complete
                while not future.done():
                    await asyncio.sleep(0.1)
                    print("Waiting for the thread scan to complete...")
                
                # Retrieve the result from the future
                result = future.result()
                print("Result:", result)
    
    
    async def get_idcode(self):
        """
        """
        async with self._mutex:

             with self.executor as executor :
                # Submit the idcode function to the executor
                future = executor.submit(self.idcode)
                
                # Wait for the future to complete
                while not future.done():
                    await asyncio.sleep(0.1)
                    print("Waiting for the thread idcode to complete...")
                
                # Retrieve the result from the future
                result = future.result()
                print("Result:", result)



    
    
    async def read_pin(self, device_number, pin, direction):
        """
        """
        async with self._mutex:
            with self.executor as executor:
                # Submit the read function to the executor
                future = executor.submit(self.read,device_number, pin, direction)
                
                # Wait for the future to complete
                while not future.done():
                    await asyncio.sleep(0.1)
                    print("Waiting for the thread read to complete...")
                
                # Retrieve the result from the future
                result = future.result()
                print("Result:", result)

    

    async def write_pin(self, device_number, pin, value):
        """
        """
        async with self._mutex:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Submit the write function to the executor
                future = executor.submit(self.write,device_number, pin, value)
                
                # Wait for the future to complete
                while not future.done():
                    await asyncio.sleep(0.1)
                    print("Waiting for the thread write to complete...")
                
                # Retrieve the result from the future
                result = future.result()
                #print("Result:", result)
            

    

    ###########################################################################
    ###########################################################################

    def scan(self):
        number_of_devices = 0
        self.engine.reset()
        self.engine.change_state('shift_dr')
        idcode = self.engine._ctrl.read(32)
        
        while int(idcode) != 0:
            number_of_devices += 1
            idcode = self.engine._ctrl.read(32)           
        
        self.engine.change_state('update_dr')
        self.engine.go_idle()

        return number_of_devices
    
    def idcode(self):
        number_of_devices = 0
        idcode_hex = {}

        self.engine.reset()
        self.engine.change_state('shift_dr')
        idcode = self.engine._ctrl.read(32)
        idcode_hex[number_of_devices] = str(f"0x{format(int(idcode),'08X')}")
        
        while int(idcode) != 0:
            number_of_devices += 1
            idcode = self.engine._ctrl.read(32)
            if int(int(idcode)>0): 
                idcode_hex[number_of_devices] = str(f"0x{format(int(idcode),'08X')}")          
        
        self.engine.change_state('update_dr')
        self.engine.go_idle()

        return idcode_hex

    def read(self,device_number,pin,direction):
        global bit_settings
        boundary_scan = self.sample(device_number)
        #print(boundary_scan)                       
        for bit in range(0, self.boundary_length[device_number]):
            cell = self.json_bsdl[device_number].boundary_register[str(bit)]
            cell_spec = cell["cell_spec"]
            if cell_spec["port_id"] == pin:
                if direction == "in" and cell_spec["function"].upper() == "INPUT": 

                    byte_array_scan = list(boundary_scan)
                    #print(byte_array_scan) 

                    if byte_array_scan[bit] == 1 :
                        #print(pin + " (input) is turn on ")
                        self.extest(bit_settings,device_number)
                        return True
                    else :
                        #print(pin + " (input) is turn off")
                        self.extest(bit_settings,device_number)
                        return False
                    
                elif direction == "out" and cell_spec["function"].upper() == "OUTPUT3":

                    byte_array = list(bit_settings)
                
                    if byte_array[bit] == 1 :
                        #print(pin + " (output) is turn on")
                        self.extest(bit_settings,device_number)
                        return True
                    else :
                        #print(pin + " (output) is turn off")
                        self.extest(bit_settings,device_number)
                        return False

    
    def write (self, device_number,pin,value):
        bit_state_dict = {}
        for bit in range(0, self.boundary_length[device_number]):
            cell = self.json_bsdl[device_number].boundary_register[str(bit)]
            cell_spec = cell["cell_spec"]
            if cell_spec["port_id"] == pin:
                if cell_spec["function"].upper() == "OUTPUT3":
                    disable_spec = cell["input_or_disable_spec"]                      
                    control_cell_number = int(disable_spec["control_cell"]) 
                    disable_value = int(disable_spec["disable_value"])
                    enable_value = 0 if disable_value == 1 else 1
                    bit_state_dict[control_cell_number] = enable_value
                    bit_state_dict[bit] = value

        global bit_settings
        
        boundary_reg = self.readback(1) ###############################

        bit_settings = get_bit_settings(bit_state_dict, boundary_reg) 
                    
        self.extest(bit_settings,device_number) 



    def init_bit_settings(self):
        global bit_settings
        self.engine.capture_dr()
        bit_settings = self.engine.read_dr(self.total_boundary_length)
        self.engine.go_idle()

        return bit_settings


    def readback(self,flag):
        """fonction qui permet de lire les registres actuels"""

        global bit_settings
        if flag == 0 :          ###############################
            self.engine.capture_dr()
            
            self.engine.go_idle()
            flag = 1
        else :
            boundary_reg  = bit_settings          

        return boundary_reg 

    def sample(self,device_number):
        """fonction qui permet d'effectuer le BoundaryScan et qui renvoi le bitstream"""

        instruction = self.instruction(device_number,"sample")
        self.engine.capture_ir()
        self.engine.write_ir(instruction)
        self.engine.capture_dr()
        
        boundary_scan = self.engine.read_dr(self.boundary_length[device_number])

        boundary_scan_shift = bin(int(boundary_scan) >>device_number)
        boundary_scan_shift = int(boundary_scan_shift,2)
        boundary_scan_shift = format(boundary_scan_shift,f'0{self.boundary_length[device_number]}b')
        bit_sequence = BitSequence(boundary_scan_shift,msb=True)

        return bit_sequence    
    
    def extest(self,bit_settings,device_number):
        """ fonction qui permet d'effectuer le BoundaryScan et d'écrire sur les registres """
    
        instruction = self.instruction(device_number,"extest")
        self.engine.capture_ir()
        self.engine.write_ir(instruction)
        self.engine.capture_dr()
        
        bit_settings_shift = bin(int(bit_settings) >> self.total_devices-device_number-1) # total devices = 3
        bit_settings_shift = int(bit_settings_shift,2)
        bit_settings_shift = format(bit_settings_shift,f'0{self.boundary_length[device_number]}b')
        bit_settings = BitSequence(bit_settings_shift,msb=True)

        print(bit_settings)
        self.engine.write_dr(bit_settings)  

    
    def instruction (self,device_number,mode):
            
            tab = []
            instruct = self.instruct.copy()   ###############

            #print(instruct)
            if mode == "extest":
                instruct[device_number] = (self.extest_opcode[device_number],) + instruct[device_number][1:]
                
            elif mode == "sample":
                instruct[device_number] = (self.sample_opcode[device_number],) + instruct[device_number][1:]
            
            for k in sorted(instruct.keys(),reverse = True):
                
                tab.append(BitSequence(int(instruct[k][0]),length = instruct[k][1]))
                #print(tab)
                result = ''.join(str(element)[3:] for element in tab)
                #print(result)
                
                if len(tab) == self.total_devices: 
                    #print(BitSequence(str(result), msb=True,length=self.length_instruct))
                    return BitSequence(str(result), msb=True,length=self.length_instruct)
                                                          
            else :             
                raise Exception ("unknown mode")


