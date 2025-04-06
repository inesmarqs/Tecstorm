# 🛒 Shop-Wise

**Shop-Wise** é uma plataforma inteligente de compras de supermercado que combina **FastAPI** no backend com **Next.js (React + TypeScript)** no frontend, oferecendo uma experiência personalizada, segura e interativa para o utilizador.

O sistema permite:

- Adicionar produtos ao carrinho via **leitura de código de barras (simulada por MQTT)**
- Gestão de **alergénios** e **recomendações com IA**
- **Comunicação em tempo real** via WebSocket
- Interface moderna com **componentização** em React

---

## 🎯 Funcionalidades principais

- 🛒 **Carrinho de Compras**
  - Produtos adicionados/removidos automaticamente por UID
  - Cálculo total e individual
- ❌ **Blacklist de Alergénios**
  - Sistema rejeita produtos com ingredientes perigosos
- 🤖 **IA com LLaMA 3**
  - Recomendação automática de produtos seguros alternativos
- 🌐 **Tempo Real**
  - WebSocket para notificações imediatas no frontend
  - MQTT para comunicação com dispositivos físicos
- 🖥️ **Frontend com Next.js**
  - Interface modular com componentes como:
    - `BottomBar`, `cartItems`, `BlackListItem`, `AlternativeItemPopUp`
  - Contextos globais: `ClientContext`, `WebSocketContext`
  - Páginas organizadas por funcionalidade (`/cart`, `/login`, etc.)

---

## ⚙️ Passos para Executar

### ✅ 1. Instalação de Dependências

Instala todos os pacotes necessários para backend e frontend.

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd shop-wise
npm install
```

---

### 📝 2. Atualizar o IP no Frontend

Edita a configuração do frontend para usar o IP correto da máquina onde o backend está a correr (por exemplo, `192.168.x.x`).

---

### 🚀 3. Backend

```bash
cd backend/

# Reset à base de dados
python3 -m database.delete_database
python3 -m database.create_database

# Preenchimento com dados simulados
python3 -m scrape_data.populate_database
python3 -m scrape_data.add_even_more_products

# Arrancar o servidor FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

### 💻 4. Frontend

```bash
cd shop-wise
npm run dev
```

---

### 📡 5. Mosquitto (MQTT Broker)

Certifica-te que o Mosquitto está instalado. Depois, corre:

```bash
sudo systemctl start mosquitto
```

Para simular uma mensagem enviada pelo sistema de leitura de código de barras:

```bash
mosquitto_pub -h 127.0.0.1 -p 1883 -t test/tecstorm -m '{"uid": "abc123", "barcode": "8436048963861"}'
```

---

## 📦 Estrutura do Projeto

```
Shop-Wise/
├── backend/
│   ├── main.py
│   ├── database/
│   ├── scrape_data/
│   ├── ai_services.py
│   ├── websocket_manager.py
│   └── mqtt_server.py
├── shop-wise/           # Frontend React
│   ├── src/app/
│   │   ├── cart/
│   │   ├── login/
│   │   ├── context/
│   │   ├── BlackListItem/
│   │   ├── AlternativeItemPopUp/
│   │   └── BottomBar/
└── README.md
```

---

## ✅ Requisitos

- Python 3.8+
- Node.js + npm
- Mosquitto
- SQLite (embutido no Python via SQLAlchemy)

---

## 📬 Contacto

Para dúvidas ou sugestões, entrar em contacto com a equipa de desenvolvimento 🚀