# usiamo come unita' di misura il nano metro
# ogni nanocristallo e' circa 20 nm di diametro

MINR = 18.0/2.0
MAXR = 20.0/2.0

R = (MAXR+MINR)/2.0

botx = 0.0 
topx = 500.0
boty = 0.0 
topy = 500.0
botz = 0.0 
topz = 500.0

start_deltaz = R/2.0
dtetha_start = 0.01
min_decrement = 0.0002
min_dtetha = 0.0001

# il numero di volte che tiro la sfera 
# ovviamente influenza la porosita'
drop_sphere_n_times = 50

# se voglio aggiungere qualche sfera in cima, 
# ma non serve se cambio il modo di valutare 
# la porosita'
to_fill_the_top = False
sphere_to_fill_the_top = 50


# se voglio aumentare il raggio alla fine 
# metto a true
increase_radius = False
# percentuale aumento raggio sfera
perc_aug = 0.025
