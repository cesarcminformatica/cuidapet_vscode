<<<<<<< HEAD

# CuidaPet — Workspace para VS Code (Jornada 1 — Mariana)

Projeto Django pronto para rodar no VS Code com:
- Cadastro Tutor/Cuidador
- Cadastro de Pet
- Busca de Cuidadores (cidade/UF, espécie, disponibilidade)
- Agendamento (cálculo simples de valor)
- **Mensagens e fotos** por agendamento (upload em `media/atualizacoes/`)
- Avaliação de serviço

## Requisitos
- Python 3.10+
- VS Code + extensão Python (opcional)

## Como rodar
```bash
cd cuidapet_vscode
python -m venv .venv
# Ativar venv
#  - Windows (PowerShell): .venv\Scripts\Activate.ps1
#  - Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/services.json  # serviços CACHORRO/GATO
python manage.py createsuperuser
python manage.py runserver
```
Acesse:
- `http://127.0.0.1:8000/` — cadastro/login
- `http://127.0.0.1:8000/tutor/home/` — área da tutora (após login)

## Dicas
- Cadastre **Disponibilidades** e **Serviços** para cuidadores em **/admin** para a busca funcionar.
- Uploads ficam em `media/` (servir em DEBUG habilitado nas URLs do projeto).
=======
# cuidapet
>>>>>>> 001a082866825bcb6dbf77da860a6dfdcc601b32
