
from robobopy.Robobo import Robobo
from robobopy.utils.Sounds import Sounds
from robobopy.utils.BlobColor import BlobColor
from robobopy.utils.IR import IR

####################################
###### Parte del cilindro de color
####################################

def turn_until_see_blob(rob, color):
    speed = 5
    rob.moveWheels(speed, -speed)
    while rob.readColorBlob(color).size == 0:
        rob.wait(0.01)
        print(rob.readColorBlob(color))
    rob.stopMotors()


def say_blob_position(rob, color):
    blob = rob.readColorBlob(color)
    rob.sayText("Puedo ver el objeto rojo")
    if blob.posx < 45:
        rob.sayText("Está a la izquierda")
    elif blob.posx > 55:
        rob.sayText("Está a la derecha")
    else:
        rob.sayText("Está en el medio")


def turn_to_blob(rob, color):
    speed = 3
    rob.sayText("Giro hacia el objeto")
    blob = rob.readColorBlob(color)
    if blob.posx > 55:
        rob.moveWheels(0, speed)
    elif blob.posx < 45:
        rob.moveWheels(speed, 0)

    while (rob.readColorBlob(color).posx < 45) or (rob.readColorBlob(color).posx > 55):
        rob.wait(0.01)

    rob.stopMotors()


def move_to_ball(rob, color, maxArea):
    speed = 10
    rob.sayText("Allá voy!")
    rob.moveWheels(speed, speed)
    print(rob.readColorBlob(color))
    while rob.readColorBlob(color).size < maxArea:
        print(rob.readColorBlob(color))
        rob.wait(0.01)

    rob.stopMotors()

def pickup_ball(rob, color):
    closeIR = 1200
    # Ajustar valor IR y añadir comprobación
    # de que sigue centrado el color para poder
    # cogerlo con el pusher
    rob.moveWheels(5, 5)
    while rob.readIRSensor(IR.FrontC) < closeIR:
        print(rob.readIRSensor(IR.FrontC))
        rob.wait(0.01)    
    rob.stopMotors()   
    rob.sayText("Te cogí")
    rob.playSound(Sounds.APPROVE) 

def main():
    robobo = Robobo("localhost")
    robobo.connect()

    ####### Parte del color
    BLOB_COLOR = BlobColor.RED
    MAX_AREA = 400
    robobo.resetColorBlobs()
    #                      Red, green, blue, custom
    robobo.setActiveBlobs(True, False, False, False)

    robobo.movePanTo(0, 15)
    robobo.moveTiltTo(90, 15)

    turn_until_see_blob(robobo, BLOB_COLOR)    
    say_blob_position(robobo, BLOB_COLOR)
    turn_to_blob(robobo, BLOB_COLOR)
    robobo.moveTiltTo(100, 15)
    move_to_ball(robobo, BLOB_COLOR, MAX_AREA)
    turn_to_blob(robobo, BLOB_COLOR)
    pickup_ball(robobo, BLOB_COLOR)

if __name__ == "__main__":
    main()
