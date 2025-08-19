#!/usr/bin/env python3
"""Script pour récupérer la version depuis core/__init__.py"""
import sys
import os

# Ajouter le répertoire racine du projet au path pour pouvoir importer core
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from core import __version__
    print(__version__)
except ImportError as e:
    print("Erreur lors de l'import de la version:", e, file=sys.stderr)
    sys.exit(1)