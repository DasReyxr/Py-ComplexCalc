import numpy as np 
MAT_MTR = []
MAT_ALM = []
CIE_MTR = []
CIE_ALM = []
ESP_MTR = []
ESP_ALM = []
ALM =[]
i=0
def esc(esc_var):   #Via de escape
    if esc_var == "132":
        print("Sesión Terminada")
        exit()
class Alumno:
    def registrar_user(self,nombre,promedio,carrera,semestre,id,materia): #Métodos
        #global i
        self.nombre = nombre #Atributo
        self.promedio = promedio
        self.carrera = carrera
        self.semestre = semestre
        self.id= id
        self.materia = materia
        usuario=[self.nombre,self.carrera,self.semestre,self.id]
        
        return usuario
    def calcular_rol(self):
        if(self.promedio>8.5):
            self.rol = "Maestro"
        else:
            self.rol = "Alumno"
    def asignar_materia(self):
        

        if(self.materia) in ['Español','español']:
            print("Españolaaaaaa")
            if(self.rol) in ['Maestro']:
                ESP_MTR.append(self.nombre)
                return ESP_MTR 
            if(self.rol) in ['Alumno']:
                ESP_ALM.append(self.nombre)
                return ESP_ALM 
                
        if(self.materia) in ['Ciencias', 'ciencias']:
            print("cienciaaaaas")
            if(self.rol) in ['Maestro']:
                CIE_MTR.append(self.nombre)
                return CIE_MTR 
            if(self.rol) in ['Alumno']:
                CIE_ALM.append(self.nombre)
                return CIE_ALM 
     
        if(self.materia) in ['Matemáticas','MATEMATICAS','matematicas','Matematicas']:
            
            if(self.rol) in ['Maestro']:
                MAT_MTR.append(self.nombre)
                return MAT_MTR
            if(self.rol) in ['Alumno']:
                MAT_ALM.append(self.nombre) 
                return MAT_ALM
            
    def asignar_profe(self):
        global i
        if(len(MAT_MTR)>0) and (len(MAT_ALM)>0):
            if (MAT_MTR[i] != '') and (MAT_ALM[i] != ''):
                print(f"{MAT_ALM[i]}, Tu profesor es {MAT_MTR[i]}")
                i+=1

    def mostrar_info(self):
        print(f"------------\n Nombre: {self.nombre} ID: {self.id} \nPromedio: {self.promedio} \nCarrera:{self.carrera} Semestre:{self.semestre}\nRol {self.rol} \n------------")        

#Instancia 1
var_true = True

while(var_true):
    ask_name = input("Ingresa Nombre completo: ")
    for ask in [ask_name,ask_id,ask_cal,ask_car,ask_sem,ask_mat]:
        esc(str(ask))
    ask_id = int(input("Ingresa ID: "))
    for ask in [ask_name,ask_id,ask_cal,ask_car,ask_sem,ask_mat]:
        esc(str(ask))
    ask_cal  =float( input("Ingresa promedio: "))
    for ask in [ask_name,ask_id,ask_cal,ask_car,ask_sem,ask_mat]:
        esc(str(ask))
    ask_car = input("Ingresa tu carrera: ")
    for ask in [ask_name,ask_id,ask_cal,ask_car,ask_sem,ask_mat]:
        esc(str(ask))
    ask_sem = int(input("Ingresa tu semestre: "))
    for ask in [ask_name,ask_id,ask_cal,ask_car,ask_sem,ask_mat]:
        esc(str(ask))
    ask_mat = input("Ingresa la materia que gustas repasar o enseñar: ")
    for ask in [ask_name,ask_id,ask_cal,ask_car,ask_sem,ask_mat]:
        esc(str(ask))
    inst_1 = Alumno()
    inst_1.registrar_user(ask_name,ask_cal,ask_car,ask_sem,ask_id,ask_mat)
    # ALM.append(usuario)
    inst_1.calcular_rol()
    inst_1.mostrar_info()
    inst_1.asignar_materia()
    inst_1.asignar_profe()
    # print(usuario)
    


