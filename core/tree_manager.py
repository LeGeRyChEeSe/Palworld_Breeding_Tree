from graphviz import Digraph
from core.variables_manager import VariablesManager, resourcePath
from core.graph_manager import GraphManager
from PIL import Image
from os import path, environ
from functools import lru_cache
from collections import OrderedDict
import threading
import graphviz

class LRUImageCache:
    """Cache LRU thread-safe pour les images avec limite de mémoire"""
    def __init__(self, max_size_mb=100):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.current_size = 0
        self.cache = OrderedDict()
        self.lock = threading.Lock()
    
    def get(self, key):
        with self.lock:
            if key in self.cache:
                # Déplacer vers la fin (plus récemment utilisé)
                value = self.cache.pop(key)
                self.cache[key] = value
                return value
        return None
    
    def put(self, key, value, size_bytes=0):
        with self.lock:
            # Si la clé existe déjà, la supprimer
            if key in self.cache:
                self.current_size -= self.cache[key]['size']
                del self.cache[key]
            
            # Éviction si nécessaire
            while self.current_size + size_bytes > self.max_size_bytes and self.cache:
                oldest_key, oldest_value = self.cache.popitem(last=False)
                self.current_size -= oldest_value['size']
            
            # Ajouter le nouvel élément
            self.cache[key] = {'value': value, 'size': size_bytes}
            self.current_size += size_bytes
    
    def clear(self):
        with self.lock:
            self.cache.clear()
            self.current_size = 0

class TreeManager:
    def __init__(self):
        self.variablesManager = VariablesManager()
        self.graphManager = GraphManager()
        self.iconsPath = self.variablesManager.iconsPath
        self.cachePath = self.variablesManager.cachePath
        self.imagesCache = LRUImageCache(max_size_mb=100)
        
        # Configuration explicite du chemin Graphviz
        graphviz_path = resourcePath(path.join("Graphviz", "bin"))
        if path.exists(graphviz_path):
            environ["PATH"] = graphviz_path + path.pathsep + environ.get("PATH", "")
            # Configuration alternative pour la bibliothèque graphviz
            try:
                # Éviter les erreurs Pylance en utilisant getattr
                backend_execute = getattr(graphviz.backend, 'execute', None)
                if backend_execute:
                    engines = getattr(backend_execute, 'ENGINES', None)
                    if engines and hasattr(engines, '__setitem__'):
                        engines['dot'] = path.join(graphviz_path, 'dot.exe')
            except (AttributeError, Exception):
                pass

    def getNoneImage(self):
        return path.join(
            self.iconsPath,
            "DarkNone.png" if self.variablesManager.getConfig("darkMode") else "LightNone.png"
        )

    def AssemblePalsIcons(self, parentsList):
        # Créer une clé de cache unique pour cette combinaison
        cacheKey = "_".join(sorted(parentsList))
        cached_result = self.imagesCache.get(cacheKey)
        if cached_result:
            return cached_result['value']

        destPath = path.join(self.cachePath,cacheKey+".png")
        images = []
        
        # Charger toutes les images en une fois avec gestion d'erreurs
        for x in parentsList:
            try:
                imagePath = self.getGenderImage(x) if (" f" in x or " m" in x) else path.join(self.iconsPath,x+".png")
                if path.exists(imagePath):
                    images.append(Image.open(imagePath))
                else:
                    images.append(Image.open(self.getNoneImage()))
            except Exception:
                images.append(Image.open(self.getNoneImage()))

        # Limiter le nombre de parents secondaires à 4 par ligne
        rows = [images[i:i + 4] for i in range(0, len(images), 4)]
        # Calculer les dimensions une seule fois
        totalWidth = max(sum(im.size[0] for im in row) + (len(row) - 1) * 2 for row in rows)  # 2 pixels pour le séparateur
        totalHeight = sum(max(im.size[1] for im in row) for row in rows) + (len(rows) - 1) * 2  # 2 pixels pour le séparateur

        # Créer l'image finale et les séparateurs
        newImage = Image.new('RGBA', (totalWidth, totalHeight))
        separator = Image.new('RGBA', (2, 100), self.variablesManager.getColor("primaryColor"))
        horizontalSeparator = Image.new('RGBA', (totalWidth, 2), self.variablesManager.getColor("primaryColor"))

        # Assembler les images en ajoutant les nouvelles lignes en haut
        yOffset = totalHeight
        for row in reversed(rows):
            yOffset -= max(rowImage.size[1] for rowImage in row)
            xOffset = 0
            for idx, image in enumerate(row):
                newImage.paste(image, (xOffset, yOffset))
                xOffset += image.size[0]
                if idx < len(row) - 1 or len(row) < len(rows[0]):
                    newImage.paste(separator, (xOffset, yOffset))
                    xOffset += 2
            yOffset -= 2
            if row != rows[0]:
                newImage.paste(horizontalSeparator, (0, yOffset))

        newImage.save(destPath)
        # Calculer la taille approximative du fichier pour le cache
        file_size = path.getsize(destPath) if path.exists(destPath) else 1024
        self.imagesCache.put(cacheKey, destPath, file_size)
        return destPath

    def getGenderImage(self, pal):
        cached_result = self.imagesCache.get(pal)
        if cached_result:
            return cached_result['value']

        destPath = path.join(self.cachePath,pal + ".png")
        basePal = pal.replace(" f", "").replace(" m", "")
        gender = pal.split(" ")[1]
        
        try:
            palImagePath = path.join(self.iconsPath,basePal + ".png")
            genderImagePath = path.join(self.iconsPath,gender + ".png")
            
            if not path.exists(palImagePath) or not path.exists(genderImagePath):
                return self.getNoneImage()
                
            palImage = Image.open(palImagePath)
            genderImage = Image.open(genderImagePath).reduce(10)
        except Exception:
            return self.getNoneImage()
        
        newImage = Image.new('RGBA', palImage.size)
        newImage.paste(palImage, (0, 0))
        newImage.paste(genderImage, (0, 0), genderImage)
        newImage.save(destPath, "PNG")
        
        # Calculer la taille du fichier pour le cache
        file_size = path.getsize(destPath) if path.exists(destPath) else 1024
        self.imagesCache.put(pal, destPath, file_size)
        return destPath

    def getShortestGraphs(self, way: list, size: str):
        if len(way) < 2:
            return self.getNoneImage()

        graph = Digraph(
            node_attr={
                'shape': 'box',
                'label': '',
                "style": 'filled',
                "fillcolor": 'transparent',
                "color": self.variablesManager.getColor("primaryColor")
            },
            edge_attr={'color': self.variablesManager.getColor("primaryColor")},
            graph_attr={
                "bgcolor": 'transparent',
                "ratio": '1',
                "size": f"{int(size)/96},{int(size)/96}!"
            }
        )
        # Préparer toutes les images nécessaires en une seule fois
        nodesToCreate = {}
        for i, (parent, child) in enumerate(zip(way, way[1:])):
            parentsList, gender = self.graphManager.getSecondParents(parent, child)
            
            # Parent principal
            parentId = f"{parent}0{i}"
            if gender is not None:
                parentWithGender = f"{parent} {gender}"
                nodesToCreate[parentId] = self.getGenderImage(parentWithGender)
            else:
                nodesToCreate[parentId] = path.join(self.iconsPath,parent+".png")

            # Second parent
            parent1Id = f"{parent}1{i}"
            if len(parentsList) > 1:
                nodesToCreate[parent1Id] = self.AssemblePalsIcons(parentsList)
            else:
                pal = parentsList[0]
                if " f" in pal or " m" in pal:
                    nodesToCreate[parent1Id] = self.getGenderImage(pal)
                else:
                    nodesToCreate[parent1Id] = path.join(self.iconsPath,pal+".png")

            # Enfant
            childId = f"{child}0{i+1}"
            nodesToCreate[childId] = path.join(self.iconsPath,child+".png")

        # Créer tous les nœuds
        for nodeId, imagePath in nodesToCreate.items():
            graph.node(nodeId, image=imagePath)

        # Créer toutes les arêtes
        for i, (parent, child) in enumerate(zip(way, way[1:])):
            parent0Id = f"{parent}0{i}"
            parent1Id = f"{parent}1{i}"
            childId = f"{child}0{i+1}"
            graph.edge(parent1Id, childId)
            graph.edge(parent0Id, childId)

        outputPath = path.join(self.cachePath,"tree")
        graph.render(outputPath, format='png', cleanup=True, engine='dot', directory="./")
        return outputPath+".png"