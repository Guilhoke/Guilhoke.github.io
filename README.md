# PET-Saúde Digital

## Sobre o projeto

O **PET-Saúde Digital** é uma iniciativa desenvolvida no âmbito do Programa de Educação pelo Trabalho para a Saúde (PET-Saúde), com o objetivo de ampliar o acesso da população às informações relacionadas aos serviços públicos de saúde por meio de uma plataforma digital moderna, acessível e de fácil utilização.

O projeto foi concebido para centralizar conteúdos relevantes em um único ambiente, oferecendo uma experiência intuitiva tanto para cidadãos quanto para profissionais da saúde. A plataforma busca reduzir barreiras no acesso à informação, facilitar a comunicação entre os serviços públicos e a população e contribuir para a transformação digital da gestão em saúde.

Além da disponibilização de informações institucionais, o sistema foi planejado para permitir a evolução contínua da plataforma, possibilitando a integração de novos módulos, funcionalidades administrativas e serviços digitais voltados ao atendimento da comunidade.

---

## Objetivos

- Facilitar o acesso da população às informações sobre os serviços públicos de saúde.
- Promover uma experiência de navegação acessível e intuitiva.
- Centralizar conteúdos institucionais em uma única plataforma.
- Apoiar as iniciativas de transformação digital no setor público.
- Servir como base para futuras integrações e funcionalidades administrativas.

---

## Funcionalidades

Atualmente, o portal contempla funcionalidades como:

- Página inicial institucional;
- Navegação responsiva para dispositivos móveis e desktop;
- Exibição de notícias e conteúdos informativos;
- Destaques para campanhas e ações em saúde;
- Estrutura preparada para gerenciamento de conteúdo;
- Recursos de acessibilidade para melhor experiência do usuário;
- Interface moderna com foco em usabilidade.

---

## Tecnologias

O projeto foi desenvolvido utilizando tecnologias voltadas ao desenvolvimento web moderno, incluindo:

- HTML5
- CSS3
- JavaScript
- Django (estrutura da aplicação)
- Python

---

## Estrutura do projeto

A aplicação segue a organização tradicional do framework Django, utilizando:

- **Templates** para renderização das páginas;
- **Static Files** para gerenciamento de folhas de estilo, scripts, imagens e demais recursos estáticos;
- Estrutura preparada para expansão com banco de dados e autenticação de usuários.

---

## Público-alvo

A plataforma é destinada principalmente a:

- Cidadãos que buscam informações sobre os serviços municipais de saúde;
- Profissionais da saúde;
- Equipes administrativas responsáveis pela atualização dos conteúdos;
- Gestores públicos envolvidos nas ações do PET-Saúde.

---

## Acessibilidade

O desenvolvimento considera princípios de acessibilidade digital, buscando proporcionar uma navegação inclusiva para diferentes perfis de usuários. Entre os recursos implementados estão componentes responsivos, organização semântica do conteúdo e uma interface projetada para favorecer a legibilidade e a usabilidade.

---

## Evolução do projeto

A arquitetura foi concebida para permitir futuras expansões, como:

- Sistema de autenticação;
- Painel administrativo para gerenciamento de conteúdos;
- Integração com serviços municipais;
- Publicação de campanhas e notícias;
- Novos módulos voltados à saúde digital.

---

## Configuração e deploy

### 1. Variáveis de ambiente

Nenhum segredo fica no código. Tudo vem de um arquivo `.env` na raiz do
projeto, que **não é versionado**. Use o `.env.example` como modelo:

```bash
cp .env.example .env
```

Gere valores próprios para cada ambiente (nunca reaproveite os de outro):

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

```bash
python -c "import secrets,string; a=string.ascii_lowercase+string.digits; print('painel-'+''.join(secrets.choice(a) for _ in range(24))+'/')"
```

No servidor, restrinja a leitura do arquivo:

```bash
chmod 600 .env
```

As variáveis marcadas como obrigatórias (`DJANGO_SECRET_KEY`, `ADMIN_URL`,
`DJANGO_ALLOWED_HOSTS`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) derrubam o
processo na inicialização se estiverem vazias em produção — é proposital, para
impedir que o site suba com valores de exemplo.

### 2. Rota do painel administrativo

O painel **não** fica em `/admin/`. O caminho real vem de `ADMIN_URL` no
`.env` e não existe em lugar nenhum do repositório. Para trocá-lo, basta
editar o `.env` e reiniciar a aplicação.

Opcionalmente, `ADMIN_IPS_PERMITIDOS` restringe o painel a IPs ou faixas
(ex.: a rede da prefeitura ou a VPN). Quem estiver fora da lista recebe
**404**, e não 403 — um 403 confirmaria que existe um painel naquele endereço.

### 3. Banco de dados (MySQL)

Crie o banco e o usuário com `utf8mb4` (necessário para acentuação e para os
emojis usados nos cards de serviço):

```sql
CREATE DATABASE saude_pirai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

```sql
CREATE USER 'saude_pirai'@'localhost' IDENTIFIED BY 'senha-forte-aqui';
```

```sql
GRANT ALL PRIVILEGES ON saude_pirai.* TO 'saude_pirai'@'localhost'; FLUSH PRIVILEGES;
```

Preencha `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT` no `.env`
e aplique as migrações:

```bash
python manage.py migrate --settings=config.settings.production
```

Para trabalhar na máquina local sem subir um MySQL, use `USE_SQLITE=1` no
`.env` — esse atalho vale apenas para `config.settings.development`.

#### Migrando os dados que já estão no SQLite

```bash
python manage.py dumpdata --natural-foreign --natural-primary --exclude=contenttypes --exclude=auth.permission --indent=2 -o dados.json
```

Depois aponte o `.env` para o MySQL, rode `migrate` e importe:

```bash
python manage.py loaddata dados.json --settings=config.settings.production
```

### 4. Superusuário do painel

Em vez do `createsuperuser` interativo (que deixa a senha no histórico do
terminal), o projeto tem um comando que lê do `.env`:

```bash
python manage.py criar_admin --settings=config.settings.production
```

Ele usa `DJANGO_ADMIN_USERNAME`, `DJANGO_ADMIN_PASSWORD` e
`DJANGO_ADMIN_EMAIL`. O comando é idempotente: rodar de novo não duplica o
usuário, apenas garante que ele existe, é superusuário ativo e está com a
senha do `.env`.

### 5. Arquivos estáticos e uploads

```bash
python manage.py collectstatic --noinput --settings=config.settings.production
```

Os estáticos são servidos pelo **WhiteNoise**, com compressão e nomes com
hash (cache longo sem risco de servir CSS antigo).

Já os arquivos enviados pelo painel ficam em `core/static/` e são servidos sob
`/uploads/`. O ideal é o nginx cuidar disso:

```nginx
location /uploads/ { alias /caminho/do/projeto/core/static/; expires 30d; }
```

Enquanto essa regra não existir, o próprio Django serve `/uploads/`, para que
as imagens das notícias não apareçam quebradas no primeiro deploy. Depois de
configurar o nginx, desligue com `SERVIR_MEDIA_PELO_DJANGO=0`.

### 6. Checklist antes de publicar

```bash
python manage.py check --deploy --settings=config.settings.production
```

O único aviso esperado é o `security.W021` (HSTS preload), que fica desligado
de propósito: entrar na lista de preload dos navegadores é praticamente
irreversível. Suba `DJANGO_HSTS_SECONDS` aos poucos (comece em `3600`) e só
ligue o preload depois de confirmar que o certificado está estável.

### 7. Subindo a aplicação

```bash
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
```

`config/wsgi.py` já usa `config.settings.production` por padrão.

---
