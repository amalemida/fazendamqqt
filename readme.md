# Projeto MQTT

# Criar um ambiente virtual
```
python3 -m venv .temperatura
````
# Instalar os seguintes pacotes no ambiente virtual criado

```
pip install counterfit
```
```
pip install counterfit_connection
```
```
pip install counterfit_shims_seeed_python_dht
```

# ativar o ambiente virtual no MAC ou Linux

```
source .venv/bin/activate
``` 

# ativar o ambiente virtual no MAC ou Linux

```
.venv\scripts\activate
```

# Comandos pata executar o aplicativo

```
counterfit
```
- Configurar os sensores na porta http://localhost:5000

```
python client/app.py
```
```
python server/app.py
```