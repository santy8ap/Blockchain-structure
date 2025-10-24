#!/bin/bash
# === Script de inicio automático para criptomoneda ===
# Autor: Santi  

# --- CONFIGURACIÓN ---
PROYECTO="/home/santi/Documentos/blockchain"
VENV="$PROYECTO/venv"
PUERTO=${1:-5000}  # Puedes pasar el puerto como parámetro (por defecto 5000)

echo "🚀 Iniciando entorno virtual..."
source "$VENV/bin/activate"

echo "📂 Moviéndonos al proyecto..."
cd "$PROYECTO"

echo "🌐 Iniciando nodo en el puerto $PUERTO..."
python -m mi_coin.node -p $PUERTO &
PID=$!

# Esperar a que Flask arranque
sleep 3

echo "🔗 Registrando nodos vecinos..."
curl -s -X POST -H "Content-Type: application/json" \
-d '{"nodes":["http://127.0.0.1:5001","http://127.0.0.1:5002"]}' \
http://127.0.0.1:$PUERTO/nodes/register

echo "💰 Creando nueva wallet..."
curl -s http://127.0.0.1:$PUERTO/wallet/new > "$PROYECTO/wallet_$PUERTO.json"

echo "✅ Nodo $PUERTO iniciado correctamente."
echo "📄 Wallet guardada en: $PROYECTO/wallet_$PUERTO.json"
echo "🧠 PID del nodo: $PID"
echo "Para detenerlo: kill $PID"
