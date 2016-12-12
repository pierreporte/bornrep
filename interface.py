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

import sys
import tempfile
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

from graphique import Graphique

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.titre_x = tk.StringVar()
        self.x_min = tk.IntVar()
        self.x_max=  tk.IntVar()
        self.pas_x = tk.IntVar()
        self.div_x = tk.IntVar()
        self.type_longueur_x = tk.StringVar()
        self.longueur_pas_x = tk.DoubleVar()
        self.longueur_totale_x = tk.DoubleVar()
        self.quadrillage_x = tk.BooleanVar()

        self.titre_y = tk.StringVar()
        self.y_min = tk.IntVar()
        self.y_max=  tk.IntVar()
        self.pas_y = tk.IntVar()
        self.div_y = tk.IntVar()
        self.type_longueur_y = tk.StringVar()
        self.longueur_pas_y = tk.DoubleVar()
        self.longueur_totale_y = tk.DoubleVar()
        self.quadrillage_y = tk.BooleanVar()

        self.fichier_prévisualisation = tempfile.NamedTemporaryFile(mode="w+b", prefix="bornographe_", suffix=".png")
        # Il faut que le fichier temporaire soit une image avant de l’utiliser.
        Image.new("RGBA", (1, 1)).save(self.fichier_prévisualisation.name)

        self.bind_all("<Control-q>", self.quitter)
        self.bind_all("<Alt-F4>", self.quitter)
        self.bind_all("<Control-n>", self.nouveau_graphique)
        self.bind_all("<F5>", self.génerer)
        self.bind_all("<Control-e>", self.exporter_graphique)

        self.master.title("Bornographe")
        self.créer_interface()
        self.initialisation_variables()
        self.màj_interface()
        self.génerer()

    def quitter(self, event=None):
        sys.exit(0)

    def initialisation_variables(self, titre_x="Axe des abscisses ($x$)", x_min=0, x_max=10, pas_x=1, div_x=1, type_longueur_x="pas", longueur_pas_x=1.0, longueur_totale_x=10.0, quadrillage_x=True,
                                       titre_y="Axe des ordonnées ($y$)", y_min=0, y_max=10, pas_y=1, div_y=1, type_longueur_y="pas", longueur_pas_y=1.0, longueur_totale_y=10.0, quadrillage_y=True):
        self.titre_x.set(titre_x)
        self.x_min.set(x_min)
        self.x_max.set(y_max)
        self.pas_x.set(pas_x)
        self.div_x.set(div_x)
        self.type_longueur_x.set(type_longueur_x)
        self.longueur_pas_x.set(longueur_pas_x)
        self.longueur_totale_x.set(longueur_totale_x)
        self.quadrillage_x.set(quadrillage_x)

        self.titre_y.set(titre_y)
        self.y_min.set(y_min)
        self.y_max.set(y_max)
        self.pas_y.set(pas_y)
        self.div_y.set(div_y)
        self.type_longueur_y.set(type_longueur_y)
        self.longueur_pas_y.set(longueur_pas_y)
        self.longueur_totale_y.set(longueur_totale_y)
        self.quadrillage_y.set(quadrillage_y)

    def nouveau_graphique(self, event=None):
        if messagebox.askyesno("Attention", "Si vous créez un nouveau graphique, le travail en cours sera effacé définitivement.\n\nVoulez-vous continuer ?", icon=messagebox.WARNING):
            self.initialisation_variables()
            self.génerer()
    
    def exporter_graphique(self, event=None):
        fichier = filedialog.asksaveasfilename(title="Exporter le graphique", filetypes=[("Image SVG", "*.svg")], defaultextension=".svg")
        if fichier:
            self.graphique.enregistrer_SVG(fichier)

    def màj_interface(self, event=None):
        x_min = self.x_min.get()
        x_max = self.x_max.get()
        y_min = self.y_min.get()
        y_max = self.y_max.get()
        dx = x_max - x_min
        dy = y_max - y_min
        pas_x = self.pas_x.get()
        pas_y = self.pas_y.get()
        lpx = self.longueur_pas_x.get()
        ltx = self.longueur_totale_x.get()
        lpy = self.longueur_pas_y.get()
        lty = self.longueur_totale_y.get()

        if self.type_longueur_x.get() == "pas":
            self.x_spinbox_longueur_pas.configure(state=tk.NORMAL)
            self.x_spinbox_longueur_totale.configure(state=tk.DISABLED)
            self.longueur_totale_x.set(lpx*dx/pas_x)
        else:
            self.x_spinbox_longueur_pas.configure(state=tk.DISABLED)
            self.x_spinbox_longueur_totale.configure(state=tk.NORMAL)
            self.longueur_pas_x.set(ltx*pas_x/dx)

        if self.type_longueur_y.get() == "pas":
            self.y_spinbox_longueur_pas.configure(state=tk.NORMAL)
            self.y_spinbox_longueur_totale.configure(state=tk.DISABLED)
            self.longueur_totale_y.set(lpy*dy/pas_y)
        else:
            self.y_spinbox_longueur_pas.configure(state=tk.DISABLED)
            self.y_spinbox_longueur_totale.configure(state=tk.NORMAL)
            self.longueur_pas_y.set(lty*pas_y/dy)

        if self.quadrillage_x.get():
            self.x_spinbox_divisions.configure(state=tk.NORMAL)
        else:
            self.x_spinbox_divisions.configure(state=tk.DISABLED)

        if self.quadrillage_y.get():
            self.y_spinbox_divisions.configure(state=tk.NORMAL)
        else:
            self.y_spinbox_divisions.configure(state=tk.DISABLED)

    def génerer(self):
        self.texte_barre_état["text"] = "Mise à jour en cours"

        self.graphique = Graphique(
            x_min=self.x_min.get(),
            x_max=self.x_max.get(),
            y_min=self.y_min.get(),
            y_max=self.y_max.get(),
            titre_x=self.titre_x.get(),
            titre_y=self.titre_y.get(),
            pas_x=self.pas_x.get(),
            pas_y=self.pas_y.get(),
            longueur_pas_x=self.longueur_pas_x.get(),
            longueur_pas_y=self.longueur_pas_y.get(),
            div_x=self.div_x.get(),
            div_y=self.div_y.get(),
            quadrillage_x=self.quadrillage_x.get(),
            quadrillage_y=self.quadrillage_y.get()
        )

        self.graphique.enregistrer_PNG(self.fichier_prévisualisation.name)

        image = Image.open(self.fichier_prévisualisation.name)
        self.prévisualisation = ImageTk.PhotoImage(image)
        self.canvas_affichage.configure(scrollregion=(0, 0, image.size[0], image.size[1]))
        self.canvas_affichage.create_image(0, 0, image=self.prévisualisation, anchor=tk.NW)

        self.texte_barre_état["text"] = "Prêt"

    def créer_interface(self):
        # Fenêtre principale
        # ==================
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.resizable(True, True)
        self.master.geometry("900x600")

        # Création des widgets
        # ====================

        # Barre d’outils
        # --------------
        self.barre_outils = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.bouton_nouveau = tk.Button(self.barre_outils, text="Nouveau", command=self.nouveau_graphique, relief=tk.FLAT)
        self.bouton_génerer = tk.Button(self.barre_outils, text="Générer", command=self.génerer, relief=tk.FLAT)
        self.bouton_exporter = tk.Button(self.barre_outils, text="Exporter", command=self.exporter_graphique, relief=tk.FLAT)

        # Zone de contrôle
        # ----------------
        self.zone_contrôle = tk.Frame(self)

        # Axe des abscisses
        self.axe_x = tk.LabelFrame(self.zone_contrôle, text="Axe des abscisses")
        self.x_label_titre = tk.Label(self.axe_x, text="Titre")
        self.x_entry_titre = tk.Entry(self.axe_x, textvariable=self.titre_x)
        self.x_label_minimum = tk.Label(self.axe_x, text="Minimum")
        self.x_spinbox_minimum = tk.Spinbox(self.axe_x, from_=-sys.maxsize, to=0, textvariable=self.x_min, command=self.màj_interface)
        self.x_label_maximum = tk.Label(self.axe_x, text="Maximum")
        self.x_spinbox_maximum = tk.Spinbox(self.axe_x, from_=0, to=sys.maxsize, textvariable=self.x_max, command=self.màj_interface)
        self.x_label_pas = tk.Label(self.axe_x, text="Pas")
        self.x_spinbox_pas = tk.Spinbox(self.axe_x, from_=1, to=sys.maxsize, textvariable=self.pas_x, command=self.màj_interface)
        self.x_label_divisions = tk.Label(self.axe_x, text="Divisions")
        self.x_spinbox_divisions = tk.Spinbox(self.axe_x, from_=1, to=sys.maxsize, textvariable=self.div_x, command=self.màj_interface)
        self.x_radiobutton_longueur_pas = tk.Radiobutton(self.axe_x, text="Longueur du pas (cm)", variable=self.type_longueur_x, value="pas", command=self.màj_interface)
        self.x_spinbox_longueur_pas = tk.Spinbox(self.axe_x, to=sys.maxsize, format="%.1f", increment=0.1, textvariable=self.longueur_pas_x, command=self.màj_interface)
        self.x_radiobutton_longueur_totale = tk.Radiobutton(self.axe_x, text="Longueur totale (cm)", variable=self.type_longueur_x, value="totale", command=self.màj_interface)
        self.x_spinbox_longueur_totale = tk.Spinbox(self.axe_x, to=sys.maxsize, format="%.1f", increment=0.1, textvariable=self.longueur_totale_x, command=self.màj_interface)
        self.x_checkbox_quadrillage = tk.Checkbutton(self.axe_x, text="Quadrillage", variable=self.quadrillage_x, command=self.màj_interface)

        # Axe des ordonnées
        self.axe_y = tk.LabelFrame(self.zone_contrôle, text="Axe des ordonnées")
        self.y_label_titre = tk.Label(self.axe_y, text="Titre")
        self.y_entry_titre = tk.Entry(self.axe_y, textvariable=self.titre_y)
        self.y_label_minimum = tk.Label(self.axe_y, text="Minimum")
        self.y_spinbox_minimum = tk.Spinbox(self.axe_y, from_=-sys.maxsize, to=0, textvariable=self.y_min, command=self.màj_interface)
        self.y_label_maximum = tk.Label(self.axe_y, text="Maximum")
        self.y_spinbox_maximum = tk.Spinbox(self.axe_y, from_=0, to=sys.maxsize, textvariable=self.y_max, command=self.màj_interface)
        self.y_label_pas = tk.Label(self.axe_y, text="Pas")
        self.y_spinbox_pas = tk.Spinbox(self.axe_y, from_=1, to=sys.maxsize, textvariable=self.pas_y, command=self.màj_interface)
        self.y_label_divisions = tk.Label(self.axe_y, text="Divisions")
        self.y_spinbox_divisions = tk.Spinbox(self.axe_y, from_=1, to=sys.maxsize, textvariable=self.div_y, command=self.màj_interface)
        self.y_radiobutton_longueur_pas = tk.Radiobutton(self.axe_y, text="Longueur du pas (cm)", variable=self.type_longueur_y, value="pas", command=self.màj_interface)
        self.y_spinbox_longueur_pas = tk.Spinbox(self.axe_y, to=sys.maxsize, format="%.1f", increment=0.1, textvariable=self.longueur_pas_y, command=self.màj_interface)
        self.y_radiobutton_longueur_totale = tk.Radiobutton(self.axe_y, text="Longueur totale (cm)", variable=self.type_longueur_y, value="totale", command=self.màj_interface)
        self.y_spinbox_longueur_totale = tk.Spinbox(self.axe_y, to=sys.maxsize, format="%.1f", increment=0.1, textvariable=self.longueur_totale_y, command=self.màj_interface)
        self.y_checkbox_quadrillage = tk.Checkbutton(self.axe_y, text="Quadrillage", variable=self.quadrillage_y, command=self.màj_interface)


        # Zone de prévisualisation
        # ------------------------
        self.zone_prévisualisation = tk.Frame(self, relief=tk.SUNKEN, borderwidth=1)
        self.canvas_affichage = tk.Canvas(self.zone_prévisualisation, width=50, height=50)
        self.barre_défil_h = tk.Scrollbar(self.zone_prévisualisation, orient=tk.HORIZONTAL, command=self.canvas_affichage.xview)
        self.barre_défil_v = tk.Scrollbar(self.zone_prévisualisation, orient=tk.VERTICAL, command=self.canvas_affichage.yview)
        self.canvas_affichage.config(xscrollcommand=self.barre_défil_h.set, yscrollcommand=self.barre_défil_v.set)

        # Barre d’état
        # ------------
        self.barre_état = tk.Frame(self, relief=tk.SUNKEN, borderwidth=1)
        self.texte_barre_état = tk.Label(self.barre_état, text="Prêt")

        # Composition de la fenêtre
        # =========================
        self.grid(sticky=(tk.W, tk.E, tk.N, tk.S))
        self.barre_outils.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.zone_contrôle.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.zone_prévisualisation.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.W, tk. E))
        self.barre_état.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))


        # Barre d’outils
        # --------------
        self.bouton_nouveau.grid(row=0, column=0)
        self.bouton_génerer.grid(row=0, column=1)
        self.bouton_exporter.grid(row=0, column=2)
        
        # Zone de contrôle
        # ----------------
        self.axe_x.grid(row=0, column=0, sticky=tk.N)
        self.axe_y.grid(row=1, column=0, sticky=tk.N)

        # Axe des abscisses
        self.x_label_titre.grid(row=0, column=0, sticky=tk.W)
        self.x_entry_titre.grid(row=0, column=1, columnspan=3, sticky=(tk.W, tk.E))
        self.x_label_minimum.grid(row=1, column=0, sticky=tk.W)
        self.x_spinbox_minimum.grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.x_label_maximum.grid(row=2, column=0, sticky=tk.W)
        self.x_spinbox_maximum.grid(row=2, column=1, sticky=(tk.W, tk.E))
        self.x_label_pas.grid(row=3, column=0, sticky=tk.W)
        self.x_spinbox_pas.grid(row=3, column=1, sticky=(tk.W, tk.E))
        self.x_label_divisions.grid(row=4, column=0, sticky=tk.W)
        self.x_spinbox_divisions.grid(row=4, column=1, sticky=(tk.W, tk.E))
        self.x_radiobutton_longueur_pas.grid(row=5, column=0, sticky=tk.W)
        self.x_spinbox_longueur_pas.grid(row=5, column=1)
        self.x_radiobutton_longueur_totale.grid(row=6, column=0, sticky=tk.W)
        self.x_spinbox_longueur_totale.grid(row=6, column=1)
        self.x_checkbox_quadrillage.grid(row=7, column=0, columnspan=2, sticky=tk.W)
        
        # Axe des ordonnées
        self.y_label_titre.grid(row=0, column=0, sticky=tk.W)
        self.y_entry_titre.grid(row=0, column=1, columnspan=3, sticky=(tk.W, tk.E))
        self.y_label_minimum.grid(row=1, column=0, sticky=tk.W)
        self.y_spinbox_minimum.grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.y_label_maximum.grid(row=2, column=0, sticky=tk.W)
        self.y_spinbox_maximum.grid(row=2, column=1, sticky=(tk.W, tk.E))
        self.y_label_pas.grid(row=3, column=0, sticky=tk.W)
        self.y_spinbox_pas.grid(row=3, column=1, sticky=(tk.W, tk.E))
        self.y_label_divisions.grid(row=4, column=0, sticky=tk.W)
        self.y_spinbox_divisions.grid(row=4, column=1, sticky=(tk.W, tk.E))
        self.y_radiobutton_longueur_pas.grid(row=5, column=0, sticky=tk.W)
        self.y_spinbox_longueur_pas.grid(row=5, column=1)
        self.y_radiobutton_longueur_totale.grid(row=6, column=0, sticky=tk.W)
        self.y_spinbox_longueur_totale.grid(row=6, column=1)
        self.y_checkbox_quadrillage.grid(row=7, column=0, columnspan=2, sticky=tk.W)

        # Zone de prévisualisation
        # ------------------------
        self.canvas_affichage.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.barre_défil_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.barre_défil_h.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Barre d’état
        # ------------
        self.texte_barre_état.grid(sticky=tk.W)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.zone_prévisualisation.grid_columnconfigure(0, weight=1)
        self.zone_prévisualisation.grid_columnconfigure(1, weight=0)
        self.zone_prévisualisation.grid_rowconfigure(0, weight=1)
        self.zone_prévisualisation.grid_rowconfigure(1, weight=0)
