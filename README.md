**Roblox Account Manager (RAM) - Requisitos de Instalación**  

Para que el bot funcione correctamente, instala los siguientes componentes:  

### 📋 **Requisitos Previos**  
1. **Python 3.9 o superior**  
   - Descarga: [python.org](https://www.python.org/downloads/)  
   - Verifica instalación:  
     ```bash
     python --version
     ```  

2. **Navegador Chromium/Chrome** (versión compatible con Selenium)  
   - Asegúrate de tener Chrome instalado o usa:  
     ```bash
     sudo apt-get install chromium-browser  # Linux
     ```  

3. **Git (opcional, para clonar el repo)**  
   ```bash
   sudo apt-get install git  # Linux
   ```  

---  

### 🔧 **Instalación de Dependencias**  
Ejecuta en la terminal:  

```bash
pip install -r requirements.txt
```  

#### 📜 **Contenido de `requirements.txt`**  
```
selenium==4.0.0
undetected-chromedriver==3.5.0
discord.py==2.3.2
fake-useragent==1.1.3
names==0.3.0
python-dotenv==1.0.0
```  

---  

### ⚙️ **Configuración Adicional**  
1. **WebDriver para Chrome/Chromium**:  
   - Asegúrate de que la versión de `chromedriver` coincida con tu navegador.  
   - Descarga: [Chromedriver](https://chromedriver.chromium.org/)  

2. **Variables de Entorno** (opcional):  
   Crea un archivo `.env` con:  
   ```ini
   DISCORD_TOKEN=tu_token_aquí
   ```  

---  

### 🚀 **Ejecución**  
```bash
python main.py
```  

---  

**⚠️ Nota:**  
- Usa entornos virtuales (`venv`) para evitar conflictos.  
- En Linux, instala dependencias del sistema:  
  ```bash
  sudo apt-get install -y libxss1 libappindicator1 libindicator7  # Para headless Chrome
  ```  

---  

**📌 Soporte:**  
Si tienes errores, verifica:  
- Versiones compatibles de Chrome/Chromedriver.  
- Permisos de ejecución (`chmod +x main.py`).  

---  

**Caracteres:** 1,498 (ajustable según necesidades).  

*Incluye solo lo esencial, con comandos claros y enlaces oficiales. Opcional: añadir GIF o capturas de instalación.*
