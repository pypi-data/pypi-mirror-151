import pjer
import handydandy
model = [1,1,1,0
        ,0,1,1,1
        ,1,1,1,1
        ,1,0,1,0]

pjer.prefs.setTitle("pjer_test")
pjer.prefs.screensize(480,720)

pjer.sprite(model,100).draw(0,100,10)
pjer.sprite(model,100).move(0,100,10,10,10)
pjer.sprite(model,100).undraw(10,110,10)
handydandy.userinput.pause()