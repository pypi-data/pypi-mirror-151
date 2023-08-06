# Cryptide

This Python package gonna help you in CTF of cryptography

## Installation

    $ pip install cryptide

## All function are here :
### ASCII
* get_ascii_readable_stat
* get_unascii_stat
* unascii_stoper
* ascii_readable_stoper


### Bytes
* bytes_representation

### IC
###### Index of coincidence
* compute_ic
```python
text = """
Demain, dès l'aube, à l'heure où blanchit la campagne,
Je partirai. Vois-tu, je sais que tu m'attends.
J'irai par la forêt, j'irai par la montagne.
Je ne puis demeurer loin de toi plus longtemps.
Je marcherai les yeux fixés sur mes pensées,
Sans rien voir au dehors, sans entendre aucun bruit,
Seul, inconnu, le dos courbé, les mains croisées,
Triste, et le jour pour moi sera comme la nuit.
Je ne regarderai ni l'or du soir qui tombe,
Ni les voiles au loin descendant vers Harfleur,
Et quand j'arriverai, je mettrai sur ta tombe
Un bouquet de houx vert et de bruyère en fleur.
Victor Hugo - Les Contemplations
"""
compute_ic(text, beautifier=True)
# 0.06934214326978624
```
The option beautifier gonna asciifier your input data. 
for exemple this text will be reformat in :
```python
text = """
demain, des l'aube, a l'heure ou blanchit la campagne,
je partirai. vois-tu, je sais que tu m'attends.
j'irai par la foret, j'irai par la montagne.
je ne puis demeurer loin de toi plus longtemps.
je marcherai les yeux fixes sur mes pensees,
sans rien voir au dehors, sans entendre aucun bruit,
seul, inconnu, le dos courbe, les mains croisees,
triste, et le jour pour moi sera comme la nuit.
je ne regarderai ni l'or du soir qui tombe,
ni les voiles au loin descendant vers harfleur,
et quand j'arriverai, je mettrai sur ta tombe
un bouquet de houx vert et de bruyere en fleur.
"""
```
* checker_ic  
Use it to stop your BF when the data can be the good data
```python
checker_ic(0.038)
# None

checker_ic(0.078)
# True
```

* what_ic
This function will find the language of the index of coincidence give in input
```python
what_ic(0.08)
# DUTCH
```
* checker_and_compute_ic
* list_aggregation

