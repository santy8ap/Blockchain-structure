# 🪙 MiCoin – Blockchain en Python

![Blockchain Banner](https://github.com/user-attachments/assets/8b0b86c3f-dummy-banner-example)

> 🚀 Proyecto educativo de **criptomoneda y blockchain** desarrollado en **Python + Flask**, inspirado en la arquitectura de Bitcoin.  
> Crea tus propios nodos, valida transacciones y mina bloques directamente desde tu computadora.

---

## 📚 Índice
- [📖 Descripción](#-descripción)
- [⚙️ Requisitos](#️-requisitos)
- [💻 Instalación](#-instalación)
- [🚀 Uso rápido](#-uso-rápido)
- [🔗 Endpoints principales (API REST)](#-endpoints-principales-api-rest)
- [🧱 Ejemplo de flujo completo](#-ejemplo-de-flujo-completo)
- [📂 Estructura del proyecto](#-estructura-del-proyecto)
- [👨‍💻 Autor](#-autor)
- [📜 Licencia](#-licencia)

---

## 📖 Descripción

**MiCoin** es una implementación ligera de una **blockchain descentralizada**, donde cada nodo:
- Mantiene su propia copia del blockchain 📜  
- Puede registrar transacciones 🔁  
- Puede minar nuevos bloques ⛏️  
- Se sincroniza con otros nodos conectados 🔗  

El proyecto busca **entender la lógica detrás de las criptomonedas**, más que crear una red comercial.

---

## ⚙️ Requisitos

Asegúrate de tener instalado:
- 🐍 **Python 3.10+**
- 📦 **pip**
- 🌐 **curl** (para probar la API)
- 🧰 Linux, macOS o WSL (Windows Subsystem for Linux)

---

## 💻 Instalación

```bash
# 1️⃣ Clonar el repositorio
git clone https://github.com/tuusuario/micoin.git
cd micoin

# 2️⃣ Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3️⃣ Instalar dependencias
pip install -r requirements.txt

🚀 Uso rápido

Puedes iniciar un nodo ejecutando:

python -m mi_coin.node -p 5000

El servidor Flask correrá en:

http://127.0.0.1:5000

También puedes automatizar todo con el script:

./iniciar_micoin.sh 5000

Este script:

Activa el entorno virtual ✅

Inicia el nodo 🌐

Registra otros nodos 🔗

Genera una wallet 💰

| Método | Endpoint            | Descripción                                        |
| :----- | :------------------ | :------------------------------------------------- |
| `GET`  | `/`                 | Verifica que el nodo esté corriendo                |
| `GET`  | `/chain`            | Muestra toda la cadena de bloques                  |
| `GET`  | `/mine`             | Mina un nuevo bloque                               |
| `POST` | `/transactions/new` | Crea una nueva transacción                         |
| `POST` | `/nodes/register`   | Registra nuevos nodos                              |
| `GET`  | `/nodes/resolve`    | Sincroniza la cadena más larga                     |
| `GET`  | `/wallet/new`       | Crea una nueva wallet con claves pública y privada |


🧱 Ejemplo de flujo completo

1️⃣ Inicia tu nodo principal:

python -m mi_coin.node -p 5000

2️⃣ Crea una nueva wallet:

curl http://127.0.0.1:5000/wallet/new

3️⃣ Registra otros nodos:

curl -X POST -H "Content-Type: application/json" \
-d '{"nodes":["http://127.0.0.1:5001","http://127.0.0.1:5002"]}' \
http://127.0.0.1:5000/nodes/register


Mina tu primer bloque:

curl http://127.0.0.1:5000/mine

micoin/
├── mi_coin/
│   ├── __init__.py
│   ├── blockchain.py      # Lógica principal de la blockchain
│   ├── node.py            # Servidor Flask y rutas API
│   └── wallet.py          # Generación y firma de transacciones
├── iniciar_micoin.sh      # Script automático de inicio
├── requirements.txt
└── README.md

Santi 2a
💼 Estudiante de Ingeniería en Sistemas
💡 Apasionado por la tecnología, la programación y el desarrollo blockchain.
📫 GitHub

📜 Licencia

Este proyecto se distribuye bajo la licencia MIT.
Puedes usarlo, modificarlo y compartirlo libremente con fines educativos o personales

🌟 “El mejor modo de predecir el futuro es construirlo.” – Alan Kay
