import eizoGS320

filenames=["ende.png","ende_training_left.png","ende_training_right.png","instructions1.png","instructions2_left.png","instructions2_right.png","instructions3.png","new_block.png"]

for filename in filenames:
   eizoGS320.convert_to_eizo_picture("instructions/"+filename, "instructions/conv"+str(filename)+".png")
