import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# ========= CONFIG =========
BASE_URL = "http://127.0.0.1:5000"  # Local o Render
SCREENSHOT_DIR = "screenshots"

BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ========= DRIVER (BRAVE) =========
options = webdriver.ChromeOptions()
options.binary_location = BRAVE_PATH
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

service = Service()  # Selenium Manager (NO webdriver-manager)

driver = webdriver.Chrome(
    service=service,
    options=options
)

# ========= HELPERS =========
def screenshot(nombre):
    path = os.path.join(SCREENSHOT_DIR, f"{nombre}.png")
    driver.save_screenshot(path)
    print(f"📸 Captura guardada: {path}")

def esperar(segundos=2):
    time.sleep(segundos)

# ========= LOGIN =========
def login(email, password, nombre_captura):
    driver.get(f"{BASE_URL}/login")
    esperar()

    driver.find_element(By.NAME, "correo").clear()
    driver.find_element(By.NAME, "correo").send_keys(email)

    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.TAG_NAME, "button").click()
    esperar()

    screenshot(nombre_captura)

# ========= CLIENTE =========
def ver_pedidos_cliente():
    driver.get(f"{BASE_URL}/mis_pagos")
    esperar()
    screenshot("cliente_pedidos")

def cliente_crea_incidencia(id_pedido):
    driver.get(f"{BASE_URL}/incidencia/{id_pedido}")
    esperar()

    driver.find_element(By.NAME, "tipo").send_keys("Producto dañado")
    driver.find_element(By.NAME, "comentario").send_keys(
        "El producto llegó en mal estado"
    )

    driver.find_element(By.TAG_NAME, "button").click()
    esperar()

    screenshot("cliente_incidencia_creada")

def ver_incidencias_cliente():
    driver.get(f"{BASE_URL}/mis-incidencias")
    esperar()
    screenshot("cliente_incidencias")

# ========= VENDEDOR =========
def vendedor_ver_incidencias():
    driver.get(f"{BASE_URL}/vendedor/incidencias")
    esperar()
    screenshot("vendedor_incidencias")

def vendedor_cambiar_estado_incidencia(nuevo_estado="Aceptada"):
    select = driver.find_element(By.TAG_NAME, "select")
    select.click()
    select.send_keys(nuevo_estado)
    esperar()

    screenshot(f"incidencia_estado_{nuevo_estado}")

# ========= EJECUCIÓN =========
try:
    # 🔐 CLIENTE
    login("cliente@test.com", "12345", "login_cliente")
    ver_pedidos_cliente()
    cliente_crea_incidencia(id_pedido=55)
    ver_incidencias_cliente()

    # Limpiar sesión
    driver.delete_all_cookies()
    esperar()

    # 🔐 VENDEDOR
    login("jose@test.com", "12345", "login_vendedor")
    vendedor_ver_incidencias()
    vendedor_cambiar_estado_incidencia("Aceptada")

finally:
    print("✅ Pruebas automatizadas finalizadas")
    driver.quit()
