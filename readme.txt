REL_0_0_0   : prima di usare glyph3d
REL_0_0_1   : dopo provo ad implementare direttamente quanto descritto  in 
              Comp. Mechanics. WCCM VI Sept. 5-10 2004 China
REL_0_0_2   : split in due programmi stacker per generare e poi il visualizzatore
REL_0_0_3   : prima di iniziare ad usare configurazioni e dimensioni di particella
              piu' realistiche e di splittare coordination.py in piu' files
REL_0_0_4   : dopo aver splittato e messo i moduli in modules
REL_0_0_5   : tag intermedio prima si inserire il calcolo della PSD piu' accurato
REL_0_0_5_b : prima di committari alcuni fix, forse fix
REL_0_0_5_c : forse fissato un problema in psd_accurate, ma voglio ora
              ristrutturare il codice cosi'; che  tutti i due metodi si basino
              sull'insieme dei punti nel vuoto.  
REL_0_0_6   : Prima di iniziare ad implementare PSD sulla falsa riga di 
              psdsolv
REL_0_0_7   : Implementato il calcolo del PSD
REL_0_0_8   : Visualizzazione nanoparticelle TiO2 con classe associata 
REL_0_0_9   : Prima di iniziare ad aggiungere funzioni a corredo della
              parte nanparticella tio2
REL_0_1_0   : Aggiunta la determinazione del punto inside 
REL_0_1_1   : Prima di iniziare a fare qualche test con dim e situazioni
              realistiche
REL_0_1_2   : Prima di implementare pore_size ad ispirazione diretta di Lagemat
REL_0_1_3   : Prima implementazione con metodo collision detection per psd 
              nanocristalli
REL_0_1_4   : Prima di partire con il test con sfere a dim variabile
REL_0_1_5   : Prima di committare cambiamenti in psd_using_tr
REL_0_1_5_a : Sovrascrivo il psd_using_tr visualizer
REL_0_1_6   : Backup prima di apportare modiche a psd tr per i nanocristalli

REL_0_1_7   : Prima di partire con una ristrutturazione in funzione della
              parallelizzabilita' dei vari calcoli

REL_0_2_0   : remove old results

REL_0_2_2   : prima di risistemare il source per arrivare ad una configurazione con 
              volumq di intersezione nullo e quasi

stacker.py            : genera la configurazione e scrive il risultato in un file
stacker_random.py     : genera la configurazione e scrive il risultato in un file
                        ma invece di R fisso usa MINR e MAXR uniforme 
visualize.py          : visualizza la configrazione ottenuta leggendo da file
visualize_diff_r.py   : visualizza la configrazione ottenuta leggendo da file
                        anche sfere di raggio diverso 
anim.py               : test animation, le sfere vengono aggiunte una alla volta 
                        mentre le legge da file
dropandroll.py        : tento di animare il drop and roll
slice.py              : trova i cerchi di intersezione di un piano parallelo al 
                        piano XY.
radial_dist_func.py   : genera la funzione di sitribuzione radiale leggendo da
                        final_config.txt le posizione delle sfere ed i
                        raggi. 
                        plot "radial_distribution.txt" using 1:2:(1000) smooth acsplines
                        maggiore e' il peso maggiore la somiglianza con una linea
                        che semplicemente unisce i punti
coordination.py       : Leggendo da final_config.txt determina la coordinazione
                        semplicemente confrontando tutte le particelle una ad una.
                        Quindi una coordinazione che server essenzilmente come
                        verifica di errori o meno. Anche la porosita' e' calcolata 
                        in modo non ncessariamente corretto, ma come semplice
                        rapporto di volumi
coord_w_radial.py     : Calcola la coordinazione usando solo le particelle interne
                        determinate dalla funziona che clacola la funzione di
                        distribuzione radiale. E poi considera come taching le
                        sfere piu' o meno vicnne, non solo quelle che si toccano
                        completamente
porosity.py           : Calcolo la porosita' tagliando a fette il cubo ed usando
                        un metodo MC per calcolare rapporto tra volume occupatp e 
                        libero.
                        Calcolo la porosita' anche usando una grigli di punti fitta a
                        piacere e contanto i punti fuori e dentro le sfere
void_space.py         : can be used to plot void space as a collection of small
                        spheres
build_test_model.py   : Questo costruisce un test mnodel da usare per pore_size.py
                        per capire se stiamo calcolando correttamente la PSD o
                        meno. 
psd.py                : Calcolare il PSD 
increaseradius.py     : Aumenta le dimensioni del raggio del file
                        final_config.txt di una percentuale data.
pore_size.py          : approccio semplice per la determinazione della PSD. Lo
                        uso  adesso che ho un metodo PSD che giudico affidabile
                        anche perche' nel caso dei nanocristalli intederei usare 
                        un approccio di questo tipo per la psd 

psd_using_tr_read_points.py :  Per le sfere ma legge i punti su cui fare il
                               calcolo come input
 

nanoparticle_randomly_place.py : partendo dalla configurazione delle sfere
                                 randomizza le ruotazioni. In output stampa:
                                 x y x r p2.x p2.y p2.z tetha 
nanoparticle_visualize.py : visualizza le nanoparticelle
study_a_pair.py           : dato in input 1 intero che identifica la
                            nanoparticella ne calcola i vicini, li visualizza e
                            poi esegue altri calcoli (volume di sovrapposizione)
study_a_sphere.py         : dato in input 1 intero che identifica la
                            nanoparticella ne e data una sfera calcola la 
                            sovrapposzione
closest_point.py          : dato in input 1 intero che identifica la
                            nanoparticella e dato un punto calcola 
                            la sfera di raggio massimo che e' centrata nel punto 
                            e non tocca la nanoparticella con ClosetPoint
psd_nanop.py              : Psd calculation for nanoparticles
nanoparticle_touch_vis.py : visualizza due particelle che si toccano se trovate
                            ed eventualemnete i punti inise e le sfere
nanoparticle_touch.py     : Conta quante nanoparticelle tocca ognuna
filter_pore_radius.py     : Partendo da pore_radius_list di psd_nanop.py,
                            riapplica un filtro basato sull'approccio naif 
                            punto superficie sfera per eliminare evenetuali pori
                            troppo grandi. 

compute_psd.py            : leggendo da un file i raggi delle sfere nel poro 
                            prodotte usando o psd o psd_nano calcola il psd_diff
                            e psd_cumm 

psd_using_tr.py           : Pore size distribution using TR method 
psd_using_tr_visualize.py : Pore size distribution using TR method questo e' il
                            tool che serve solo a visualizzare
psd_using_tr_nano.py      : Pore size distribution using TR method da usare con
                            le nanoparticelle invece che con le sfere
psd_using_tr_nano_vis.py  : Pore size distribution using TR method da usare con
                            le nanoparticelle visualizza

split_initial_config.py   : Splitta la configurazione iniziale delle
                            nanoparticelle  impaccate. Cosi' che posso fare il calcolo 
                            della PSD su sottoblocchi 

psd_nanop_splitted.py     : Lavora nel calcolo del PSD per nanoparticelle su
                            cluster splittati. Quindi numero di punti esatto e
                            rifiltra aposteriori come filter_pore_radius.py

compute_particle_dist.py  : Calcola il raggio medio delle particelle e la distribuzione

visualize_single_nanop.py : mi serve per vedere se la rotazione dei punti interni funziona

nanoparticle_replace.py   : Questo dovrebbe a partire dalle configurazioni ad esempio
                            splittate , ricostruire il packing muovendo ogni nanoparticella
                            di modo che ad esempio non ne tocchi nessuna o ne tocchi altre
                            solo con u determinato volume di sovrapposizione

nanoparticle_point_surface.py   : Visualizza i punti in superficie, che poi uso per 
                                  calcolare la superficie sovrapposta

nanoparticle_volume_inter.py  : Calcola il volume di intersezione per tutte le
                                particelle, ed anche la superficie

nanoparticle_coordination.py  : Calcola in realta' tutto come nanoparticle_volume_inter.py
                                vorrei essere molto piu' veloce semplicemente 
                                mettendo i punti particella per particella man mano 
                                che serve e poi scaricare tutto cosi' non devo usare
                                molta memoria

coord_w_radial_integration.py : calcola il coordination number proprio integrando, particella per 
                                particella la g(r)

nanoparticle_replace_surface.py   : ricostruire il packing muovendo ogni nanoparticella di modo che
                                    il rapporto tra le frazioni di superficie 101 e 001 sia correttamente 
                                    circa 20

visualize_single_nanop_sphere.py : Visualizza una singola parteicella e la sfera corrispondente 

nanoparticle_replace_surface_step2.py : Onde migliorare il rapporto medio ottenuto devo fare passaggi
                                        successivi, e questo e' sicuramente uno in cui prendo particella
                                        per particella e ruoto a differenza del primo in cui riarto dalla
                                        prima particella e aggiungo man mano le altre.

nanoparticle_replace_surface_non_random_step2.py : Posso generare le rotazioni in modo esaustivo ad esempio:
                                             genero tutti i punto sulla sfera e quelli sono p2 e poi tetha 
                                             (angolo di rotazione) semplicemente mi sposto di step 2*PI/n
                                             a seconda di quello che voglio. 

nanoparticle_replace_surface_non_random_step2_fixed.py : come sopra solo che in questo caso vengono
                                                         taggati i vicini e quindi non piu' mossi

nanoparticle_replace_surface_step2_fixed.py : come sopra ma random

nanoparticle_replace_surface_step2_fixed_nona.py : come sopra ma mette fixed solo le nanoparticelle che 
                                                   toccano quella che muovo quindi in conclusione ne muove
                                                   di piu' di quello sopra, quindi non rimane fixed solo
                                                   la coordinazione


per usare pyOpt: export PYTHONPATH=$PYTHONPATH:/home/redo/AssegnoFilippo/stacker/pyopt/pyOpt-1.0.1

-------------------------------------------------------------------------------------
OLD 
-------------------------------------------------------------------------------------

pore_size_accurate.py : Calcola la pore size. Usando il metodo piu complesso.
                        Quindi per ogni punto nella griglia considera la sfera
                        piu' grande che contiene lui ma centrata anche nei
                        vicini
pore_size.py          : Calcola la pore size. Usando il metodo semplice e quindi
                        data la griglia di punti semplicemente considera la sfera
                        piu' grande centrata nel punto. In realta' il modo in
                        cui sono valutate vpor e psd non credo sia ben definito.
Ricordati di considerare anche l'orientazione dei nanocristalli nel
randomwalk. Di fatto da come sono distribuiti gli stati, se due 
nanocristalli sono impilati l'uno sopra la'ltro forse consucono poco.

quindi si potrebbe tentare anche di determinare una qualche 
possibilita' di transizione tra nanocristalli impaccati deiversamente 
e quindi anche con porosita' e PSD. Impilati uno sopra l'altro porosita'
presumibilmente maggiore e psd di un qualche tipo.

=====================================================================

PRIMO LAVORO

studio proprieta' delle sfere e come cambia quando passo ai nanocristalli

