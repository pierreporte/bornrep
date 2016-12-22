# BORNREP 1.0
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

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog

class Àpropos(simpledialog.Dialog):
    def __init__(self, master):
        super().__init__(master, title="À propos de Bornrep")

    def body(self, master):
        tk.Label(master, text="Bornrep", font="Times 20 bold italic", relief=tk.RIDGE, borderwidth=2).grid(row=0, sticky="NWE", ipady=10, ipadx=10)
        tk.Label(master, text="Version 1.0").grid(row=1, sticky="NWES", pady=10)
        tk.Label(master, text="Générateur de repère pour graphiques").grid(row=2, pady=(0, 10))
        tk.Label(master, text="Écrit par Thomas Duchesne").grid(row=3)
        tk.Label(master, text="Inspiré par Cyrille BORNE").grid(row=4)
        tk.Label(master, text="© 2016, Thomas Duchesne").grid(row=5, pady=(10, 0))
        tk.Label(master, text="Logiciel sous licence Zlib").grid(row=6)

    def buttonbox(self):
        tk.Button(self, text="Fermer", command=self.destroy).pack(padx=5, pady=5)
        self.bind("<Return>", self.destroy)
        self.bind("<Escape>", self.destroy)
