# BORNOGRAPHE (prototype)
# Générateur de fond de graphique pour Cyrille BORNE (https://cyrille-borne.com)
#
# Copyright (C) 2016 thomas Duchesne (thomas@duchesne.io)
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

import itertools
import pyx
from pyx.unit import tocm

# Les deux fonctions suivantes sont issues du module Goulib, de Philippe
# Guglielmetti <goulib@goulu.net>. La fonction linspace() a été légèrement
# modifiée : la gestion des itérables a été retirée.
# https://github.com/goulu/Goulib/blob/master/Goulib/itertools2.py

def arange(start,stop=None,step=1):
    """ range for floats or other types (`numpy.arange` without numpy)
    :param start: optional number. Start of interval. The interval includes this value. The default start value is 0.
    :param stop: number. End of interval. The interval does not include this value, except in some cases where step is not an integer and floating point round-off affects the length of out.
    :param step: optional number. Spacing between values. For any output out, this is the distance between two adjacent values, out[i+1] - out[i]. The default step size is 1.
    :result: iterator
    """
    if stop is None:
        stop=start
        start=0
    r = start
    step=abs(step)
    if stop<start :
        while r > stop:
            yield r
            r -= step
    else:
        while r < stop:
            yield r
            r += step

def linspace(start,end,n=100):
    """ iterator over n values linearly interpolated between (and including) start and end
    `numpy.linspace` without numpy
    :param start: number, or iterable vector
    :param end: number, or iterable vector
    :param n: int number of interpolated values
    :result: iterator
    """

    # like http://www.mathworks.com/help/matlab/ref/linspace.html
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.linspace.html has more options
    if start==end: #generate n times the same value for consistency
        return itertools.repeat(start,n)
    else: #make sure we generate n values including start and end
        step=float(end-start)/(n-1)
        return arange(start,end+step/2,step)

class Graphique():
    def __init__(self, x_min, x_max, y_min, y_max, titre_x="", titre_y="", pas_x=1, pas_y=1, longueur_pas_x=1, longueur_pas_y=1, div_x=1, div_y=1, quadrillage_x=True, quadrillage_y=True):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.titre_x = titre_x
        self.titre_y = titre_y
        self.pas_x = pas_x
        self.pas_y = pas_y
        self.longueur_pas_x = longueur_pas_x
        self.longueur_pas_y = longueur_pas_y
        self.div_x = div_x
        self.div_y = div_y
        self.quadrillage_x = quadrillage_x
        self.quadrillage_y = quadrillage_y

        self._image = pyx.canvas.canvas()
        self._généré = False

        pyx.text.set(cls=pyx.text.LatexRunner, texenc="utf-8")
        pyx.text.preamble(r"\usepackage[utf8]{inputenc}")

    def générer(self):
        axes = [pyx.path.line(self.x_min*self.longueur_pas_x/self.pas_x, 0, self.x_max*self.longueur_pas_x/self.pas_x + 0.5, 0),
                pyx.path.line(0, self.y_min*self.longueur_pas_y/self.pas_y, 0, self.y_max*self.longueur_pas_y/self.pas_y + 0.5)]


        graduations = list()
        quadrillage = list()
        nombres = list()

        # Positions extrêmales du haut et du bas des boîtes de textes des
        # graduations sur l’axe x. Seront utilisées pour positionner le titre
        # des axes afin d’éviter une superposition.
        encombrement_nombres_x = {"haut": 0.0, "bas": 0.0}
        encombrement_nombres_y = {"droite": 0.0, "gauche": 0.0}

        for x in range(self.x_min, self.x_max + 1, self.pas_x):
            graduations.append(pyx.path.line(x*self.longueur_pas_x/self.pas_x, -0.1, x*self.longueur_pas_x/self.pas_x, 0.1))
            nombre = pyx.text.text(x*self.longueur_pas_x/self.pas_x, -0.2, "$" + str(x)+ "$", [pyx.text.halign.boxcenter, pyx.text.valign.top])
            nombres.append(nombre)
            
            haut, bas = tocm(nombre.bbox().top()), tocm(nombre.bbox().bottom())
            if haut > encombrement_nombres_x["haut"]:
                encombrement_nombres_x["haut"] = haut
            if bas < encombrement_nombres_x["bas"]:
                encombrement_nombres_x["bas"] = bas

        if self.quadrillage_x:
            for x in linspace(self.x_min, self.x_max, (self.x_max - self.x_min)*self.div_x/self.pas_x + 1):
                quadrillage.append(pyx.path.line(x*self.longueur_pas_x/self.pas_x, self.y_min*self.longueur_pas_y/self.pas_y, x*self.longueur_pas_x/self.pas_x, self.y_max*self.longueur_pas_y/self.pas_y))

        for y in range(self.y_min, self.y_max + 1, self.pas_y):
            graduations.append(pyx.path.line(-0.1, y*self.longueur_pas_y/self.pas_y, 0.1, y*self.longueur_pas_y/self.pas_y))
            nombre = pyx.text.text(-0.2, y*self.longueur_pas_y/self.pas_y, "$" + str(y) + "$", [pyx.text.halign.boxright, pyx.text.valign.middle])
            nombres.append(nombre)

            gauche, droite = tocm(nombre.bbox().left()), tocm(nombre.bbox().right())
            if gauche < encombrement_nombres_y["gauche"]:
                encombrement_nombres_y["gauche"] = gauche
            if droite < encombrement_nombres_y["droite"]:
                encombrement_nombres_y["droite"] = droite

        titre_axe_x = pyx.text.text(self.x_max*self.longueur_pas_x/self.pas_x, encombrement_nombres_x["bas"] - 0.3, self.titre_x, [pyx.text.halign.right, pyx.text.valign.top])
        titre_axe_y = pyx.text.text(encombrement_nombres_y["gauche"] - 0.3, self.y_max*self.longueur_pas_y/self.pas_y, self.titre_y, [pyx.text.halign.right])

        if self.quadrillage_y:
            for y in linspace(self.y_min, self.y_max, (self.y_max - self.y_min)*self.div_y/self.pas_y + 1):
                quadrillage.append(pyx.path.line(self.x_min*self.longueur_pas_x/self.pas_x, y*self.longueur_pas_y/self.pas_y, self.x_max*self.longueur_pas_x/self.pas_x, y*self.longueur_pas_y/self.pas_y))

        for axe in axes:
            self._image.stroke(axe, [pyx.style.linewidth.Thick, pyx.deco.earrow()])

        ap_texte = [pyx.color.rgb.white, pyx.style.linewidth.THIck, pyx.deco.filled([pyx.color.rgb.white])]
        rotation = [pyx.trafo.rotate(90, x=encombrement_nombres_y["gauche"] - 0.3, y=self.y_max*self.longueur_pas_y/self.pas_y)]

        self._image.stroke(titre_axe_x.bbox().path(), ap_texte)
        self._image.insert(titre_axe_x)
        self._image.stroke(titre_axe_y.bbox().path(), ap_texte + rotation)
        self._image.insert(titre_axe_y, rotation)

        for graduation in graduations:
            self._image.stroke(graduation, [pyx.style.linewidth.Thick])

        for ligne in quadrillage:
            self._image.stroke(ligne, [pyx.style.linestyle.dashed])

        for nombre in nombres:
            self._image.stroke(nombre.bbox().path(), [pyx.color.rgb.white, pyx.style.linewidth.THIck, pyx.deco.filled([pyx.color.rgb.white])])
            self._image.insert(nombre)

        self._généré = True

    def enregistrer_SVG(self, fichier):
        if not self._généré:
            self.générer()

        self._image.writeSVGfile(fichier)

    def enregistrer_PNG(self, fichier, résolution=None):
        if not self._généré:
            self.générer()

        if résolution is None:
            self._image.writeGSfile(fichier)
        else:
            self._image.writeGSfile(fichier, resolution=résolution)
