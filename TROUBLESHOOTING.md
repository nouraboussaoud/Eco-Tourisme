# 🔧 TROUBLESHOOTING GUIDE - Eco-Tourism Platform

## ❌ ERREUR: ModuleNotFoundError: No module named 'google'

### Solution Rapide (30 secondes)

```powershell
# En PowerShell, dans le dossier backend:
pip install google-generativeai

# Puis relancez:
python main.py
```

### Solution Complète (2 minutes)

```powershell
# 1. Vérifier Python
python --version
# Output: Python 3.x.x

# 2. Vérifier venv est activé
# Vous devriez voir (venv) au début de la ligne PowerShell

# 3. Réinstaller toutes les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# 4. Vérifier installation
pip list | findstr google-generativeai

# 5. Relancer
python main.py
```

---

## ❌ ERREUR: "venv" not found

### Solution
```powershell
# Créer venv
python -m venv venv

# Activer venv
.\venv\Scripts\Activate.ps1

# Installer dépendances
pip install -r requirements.txt
```

---

## ❌ ERREUR: "pip" not found ou "python" not found

### Solution
1. Installer Python: https://www.python.org/downloads/
2. **IMPORTANT**: Cocher "Add Python to PATH" lors de l'installation
3. Redémarrer PowerShell/CMD
4. Essayer: `python --version`

---

## ❌ ERREUR: "Port 8000 already in use"

### Solution
```powershell
# Trouver le processus
Get-Process | findstr python

# Arrêter le processus
taskkill /PID <PID> /F

# Ou simplement changer le port dans config.py
BACKEND_PORT=8001
```

---

## ❌ ERREUR: Frontend "npm ERR"

### Solution
```powershell
# Nettoyer npm cache
npm cache clean --force

# Supprimer node_modules
Remove-Item -Recurse -Force node_modules

# Réinstaller
npm install

# Lancer
npm run dev
```

---

## ❌ ERREUR: Fuseki "Port 3030 already in use"

### Solution
```cmd
# CMD (pas PowerShell)
netstat -ano | findstr :3030
taskkill /PID <PID> /F

# Puis relancer Fuseki
fuseki-server --mem /eco-tourism
```

---

## ✅ VÉRIFICATIONS RAPIDES

### Tester Backend
```powershell
curl http://localhost:8000/health

# Expected output:
# {"status":"healthy","timestamp":"...","services":{...}}
```

### Tester Frontend
```powershell
# Ouvrir dans navigateur:
http://localhost:3000

# Expected: Page EcoTravel charge
```

### Tester Fuseki
```powershell
# Ouvrir dans navigateur:
http://localhost:3030

# Expected: Interface Fuseki Admin
```

---

## 📋 CHECKLIST DE DÉMARRAGE

- [ ] Python 3.8+ installé
- [ ] venv créé: `python -m venv venv`
- [ ] venv activé: `.\venv\Scripts\Activate.ps1`
- [ ] Dépendances installées: `pip install -r requirements.txt`
- [ ] Fuseki lancé: `fuseki-server --mem /eco-tourism`
- [ ] Backend lancé: `python main.py`
- [ ] Frontend lancé: `npm run dev`
- [ ] Application accessible: http://localhost:3000

---

## 🆘 SUPPORT

Erreur non listée?

1. Vérifier les logs:
   - Backend: Console Python
   - Frontend: `npm run dev` output
   - Fuseki: Console Fuseki

2. Essayer réinstallation complète:
   ```powershell
   Remove-Item -Recurse venv
   Remove-Item -Recurse node_modules
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   cd ../frontend
   npm install
   ```

3. Vérifier fichiers de configuration:
   - `backend/config.py`
   - `frontend/vite.config.js`

---

## 💡 ASTUCES

### Redémarrage Rapide
```powershell
# Arrêter tout (Ctrl+C dans chaque terminal)
# Puis:
python main.py          # Terminal 1
npm run dev             # Terminal 2
fuseki-server...        # Terminal 3
```

### Vérifier Versions
```powershell
python --version        # 3.8+
node --version         # 16+
npm --version          # 7+
```

### Logs Verbeux
```powershell
# Backend (plus d'infos)
python -u main.py

# Frontend (plus d'infos)
npm run dev -- --debug
```

---

**Status**: Document de troubleshooting
**Dernière mise à jour**: Novembre 2025
**Version**: 1.0.0
