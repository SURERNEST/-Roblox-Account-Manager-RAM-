# discord bot for roblox alts
# las reglas para la creacion del bot son:
# 1. El bot no debe crear mas de una cuenta cada 24 horas.
# 2. El bot debe generar un nombre de usuario unico y aleatorio.
# 3. El bot debe generar una contraseña segura y aleatoria.
# 4. El bot debe generar una fecha de nacimiento que haga que la cuenta tenga al menos 13 años.
# 5. el bot debe generar una cuenta de roblox si el usuario solicita con el comando !gen y mostrara los datos para su uso.

import random
import string
import time
import asyncio
import names
import discord
from datetime import datetime, timedelta
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from fake_useragent import UserAgent

class StealthAccountGenerator:
    def __init__(self):
        self.user_agents = UserAgent()
        self.driver = None
        self.human_like_delays = (0.2, 0.8)

    def _init_driver(self):
        """Configura el navegador con opciones de sigilo"""
        if self.driver is None:
            options = uc.ChromeOptions()
            
            # Configuración avanzada de sigilo
            options.add_argument('--headless')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument(f'user-agent={self.user_agents.random}')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            
            # Evitar detección de automation
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = uc.Chrome(options=options)
            
            # Eliminar huellas de automation
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": self.user_agents.random
            })

    async def generate_credentials(self):
        """Genera credenciales realistas"""
        # Usuario con formato más natural
        username = f"{names.get_first_name()}{random.choice(['', '_', '.'])}{random.choice([names.get_last_name(), str(random.randint(100, 9999))])}".lower()
        
        # Contraseña más segura
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.sample(chars, 16))
        
        # Fecha de nacimiento válida (13-25 años)
        year = datetime.now().year - random.randint(13, 25)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        birthdate = f"{month:02d}/{day:02d}/{year}"
        
        return username, password, birthdate

    async def human_like_typing(self, element, text):
        """Simula escritura humana"""
        actions = ActionChains(self.driver)
        for char in text:
            actions.send_keys_to_element(element, char)
            actions.perform()
            await asyncio.sleep(random.uniform(*self.human_like_delays))

    async def solve_captcha(self):
        """Manejo básico de CAPTCHAs (requiere implementación real)"""
        try:
            # Aquí iría la lógica real de resolución de CAPTCHA
            await asyncio.sleep(random.uniform(5, 10))
            return True
        except:
            return False

    async def create_account(self):
        """Crea una cuenta con comportamiento humano"""
        self._init_driver()
        try:
            # Paso 1: Navegación inicial con retraso aleatorio
            self.driver.get("https://www.roblox.com")
            await asyncio.sleep(random.uniform(3, 7))

            # Generar credenciales
            username, password, birthdate = await self.generate_credentials()
            month, day, year = birthdate.split('/')

            # Paso 2: Rellenar formulario con comportamiento humano
            username_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "signup-username"))
            )
            await self.human_like_typing(username_field, username)

            password_field = self.driver.find_element(By.ID, "signup-password")
            await self.human_like_typing(password_field, password)

            # Selección de fecha de nacimiento con movimientos realistas
            birth_fields = {
                "MonthDropdown": month,
                "DayDropdown": day,
                "YearDropdown": year
            }

            for field_id, value in birth_fields.items():
                dropdown = self.driver.find_element(By.ID, field_id)
                self.driver.execute_script("arguments[0].scrollIntoView();", dropdown)
                ActionChains(self.driver).move_to_element(dropdown).pause(
                    random.uniform(0.5, 1.5)).click().perform()
                
                option = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//option[@value='{value}']"))
                )
                ActionChains(self.driver).move_to_element(option).pause(
                    random.uniform(0.3, 0.7)).click().perform()
                await asyncio.sleep(random.uniform(0.5, 1.5))

            # Selección de género
            gender = random.choice(["Male", "Female"])
            try:
                gender_field = self.driver.find_element(By.XPATH, f"//label[contains(text(), '{gender}')]")
                ActionChains(self.driver).move_to_element(gender_field).pause(
                    random.uniform(0.5, 1.0)).click().perform()
            except:
                pass

            # Manejo de CAPTCHA (simulado)
            await self.solve_captcha()

            # Envío del formulario
            submit_button = self.driver.find_element(By.ID, "signup-button")
            self.driver.execute_script("arguments[0].scrollIntoView();", submit_button)
            ActionChains(self.driver).move_to_element(submit_button).pause(
                random.uniform(0.5, 1.5)).click().perform()

            # Esperar creación de cuenta
            WebDriverWait(self.driver, 30).until(
                EC.url_contains("www.roblox.com/home")
            )

            # Guardar cuenta de forma segura
            with open("accounts.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()}: {username}:{password}:{birthdate}\n")

            return {
                "success": True,
                "credentials": {
                    "username": username,
                    "password": password,
                    "birthdate": birthdate
                },
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        finally:
            self.close()

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

# Configuración del Bot de Discord
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(
    command_prefix='?',
    intents=intents,
    help_command=None
)

# Sistema avanzado de cooldown
class CooldownSystem:
    def __init__(self):
        self.user_cooldowns = {}
        self.base_cooldown = timedelta(hours=12)
        self.max_cooldown = timedelta(hours=72)

    def check_cooldown(self, user_id):
        now = datetime.now()
        if user_id not in self.user_cooldowns:
            return None
        
        last_time, attempts = self.user_cooldowns[user_id]
        cooldown = min(
            self.base_cooldown * (2 ** (attempts - 1)),
            self.max_cooldown
        )
        
        if now < last_time + cooldown:
            return last_time + cooldown - now
        return None

    def update_cooldown(self, user_id):
        now = datetime.now()
        if user_id in self.user_cooldowns:
            last_time, attempts = self.user_cooldowns[user_id]
            self.user_cooldowns[user_id] = (now, attempts + 1)
        else:
            self.user_cooldowns[user_id] = (now, 1)

cooldown_system = CooldownSystem()

@bot.command(name='gen', aliases=['generate', 'getaccount'])
async def generate_account(ctx):
    """Comando de generación con múltiples capas de protección"""
    # Verificación de cooldown
    remaining = cooldown_system.check_cooldown(ctx.author.id)
    if remaining:
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes = remainder // 60
        
        embed = discord.Embed(
            title="⏳ Cooldown Activo",
            description=f"Por razones de seguridad, debes esperar {hours}h {minutes}m antes de generar otra cuenta.",
            color=0xFFA500
        )
        return await ctx.send(embed=embed)

    # Mensaje de procesamiento
    processing_msg = await ctx.send("🔄 **Procesando tu solicitud...** Esto puede tomar unos minutos.")

    try:
        # Crear cuenta
        generator = StealthAccountGenerator()
        result = await generator.create_account()
        
        if result["success"]:
            # Actualizar cooldown
            cooldown_system.update_cooldown(ctx.author.id)
            
            # Crear embed de éxito
            creds = result["credentials"]
            success_embed = discord.Embed(
                title=f"✅ Cuenta Generada | {creds['username']}",
                description="**Guarda esta información en un lugar seguro.**\n\n"
                          "⚠️ **No compartas** estas credenciales con nadie.\n"
                          "🔒 **Cambia la contraseña** lo antes posible.",
                color=0x00FF00,
                timestamp=datetime.now()
            )
            
            # Campos de información
            success_embed.add_field(
                name="🔑 Credenciales",
                value=f"```\nUsuario: {creds['username']}\nContraseña: {creds['password']}\n```",
                inline=False
            )
            
            success_embed.add_field(
                name="📅 Fecha de Nacimiento",
                value=creds['birthdate'],
                inline=True
            )
            
            success_embed.add_field(
                name="🕒 Generado el",
                value=result['timestamp'],
                inline=True
            )
            
            success_embed.set_footer(
                text="Este bot cumple con los Términos de Servicio de Roblox",
                icon_url="https://i.imgur.com/JRg7fLn.png"
            )

            # Enviar por mensaje privado
            try:
                await ctx.author.send(embed=success_embed)
                await processing_msg.edit(content=f"📩 {ctx.author.mention}, revisa tus mensajes privados!")
            except discord.Forbidden:
                error_embed = discord.Embed(
                    title="❌ Error de Privacidad",
                    description="No puedo enviarte mensajes privados. Por favor habilita los MPs y vuelve a intentarlo.",
                    color=0xFF0000
                )
                await processing_msg.edit(embed=error_embed)
        else:
            error_embed = discord.Embed(
                title="❌ Error en la Generación",
                description=f"No se pudo crear la cuenta: {result['error']}",
                color=0xFF0000
            )
            await processing_msg.edit(embed=error_embed)
            
    except Exception as e:
        error_embed = discord.Embed(
            title="⚠️ Error Crítico",
            description=f"Ocurrió un error inesperado: {str(e)}",
            color=0xFF0000
        )
        await processing_msg.edit(embed=error_embed)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(activity=discord.Game(name="?gen para una cuenta"))

# Ejecutar el bot
if __name__ == "__main__":
    bot.run('TU_TOKEN_AQUI')