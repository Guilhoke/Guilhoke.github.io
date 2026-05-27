# 🏥 Saúde Digital Piraí — Manual de Manutenção

Bem-vindo! Este documento explica **como manter o site atualizado** mesmo se você só domina o básico de HTML.

---

## 📁 Estrutura do projeto!

```
saude-digital-pirai/
├── index.html              ← Página inicial (HOME)
├── paginas/                ← Todas as outras páginas
│   ├── unidades.html
│   ├── servicos.html
│   ├── eventos.html
│   ├── ouvidoria.html
│   ├── duvidas.html
│   ├── profissionais.html
│   ├── servidor.html
│   ├── transparencia.html
│   └── busca.html
├── css/
│   └── estilo.css          ← Visual do site (cores, fontes, etc.)
├── js/
│   ├── dados.js            ← ⭐ AQUI VOCÊ EDITA TUDO DO SITE ⭐
│   ├── componentes.js      ← Menu, cabeçalho e rodapé
│   └── script.js           ← Funcionamento dinâmico
└── img/
    └── (suas imagens aqui)
```

---

## ⭐ O ARQUIVO MAIS IMPORTANTE: `js/dados.js`

**Quase tudo que você precisa atualizar está aqui.** Abra esse arquivo em qualquer editor de texto (Bloco de Notas, VS Code, Notepad++).

### ➕ Como adicionar uma NOVA unidade de saúde

1. Abra `js/dados.js`
2. Procure pela lista `UNIDADES`
3. Copie um bloco completo (do `{` até `},`) e cole logo abaixo:

```javascript
{
  nome: "Nome da Nova Unidade",
  tipo: "Unidade de Saúde da Família",
  endereco: "Rua Exemplo, nº 123",
  telefone: "2411-0000",
  lat: -22.6280,
  lng: -43.8980,
  foto: "img/unidade-placeholder.jpg"
},
```

**Sobre as coordenadas (lat e lng):**
- Abra o [Google Maps](https://www.google.com/maps)
- Clique com **botão direito** no local exato da unidade
- Os dois números que aparecem em cima são as coordenadas (latitude e longitude)
- Copie eles para os campos `lat` e `lng`

### ➖ Como REMOVER uma unidade

Apague o bloco inteiro `{ ... },` da unidade que quer remover. **Atenção:** inclua a vírgula no final.

### ✏️ Como EDITAR uma unidade

Mude apenas o texto **dentro das aspas**. Não mexa em vírgulas, chaves nem aspas.

---

### 📰 Como adicionar uma NOTÍCIA

Mesmo processo, mas na lista `NOTICIAS`. **A primeira notícia da lista aparece em destaque na home!**

```javascript
{
  titulo: "Título da notícia",
  data: "20/05/2026",
  resumo: "Resumo curto da notícia.",
  categoria: "Vacinação",
  link: "#"
},
```

### 📅 Como adicionar um EVENTO

Na lista `EVENTOS`:

```javascript
{
  titulo: "Nome do Evento",
  data: "10/06/2026",
  horario: "08:00 às 17:00",
  local: "Local do evento",
  descricao: "Descrição completa."
},
```

### 🔗 Como adicionar um SERVIÇO

Na lista `SERVICOS`:

```javascript
{
  nome: "Nome do Serviço",
  descricao: "Descrição curta.",
  icone: "🩺",
  link: "https://link-externo.com"
},
```

---

## ⚠️ REGRAS DE OURO (não quebre o site)

1. **Sempre mantenha as aspas `" "`** envolvendo os textos
2. **Sempre mantenha a vírgula `,`** no final de cada linha (exceto a última de cada bloco)
3. **Não apague as chaves `{ }` nem os colchetes `[ ]`**
4. Se for usar aspas dentro de um texto, use **aspas simples**: `"Ele disse 'olá'"`
5. **Sempre faça uma cópia do arquivo antes de editar** (Ctrl+C, Ctrl+V no Windows)
6. Depois de salvar, **abra o site no navegador** para conferir se nada quebrou

---

## 🎨 Como mudar as cores do site

Abra `css/estilo.css`. No início do arquivo você verá:

```css
:root {
  --cor-primaria: #0a4d8c;        /* Azul institucional principal */
  --cor-primaria-escura: #073864; /* Azul escuro para hover */
  --cor-secundaria: #00a39a;      /* Verde-água */
  ...
}
```

Para mudar uma cor, basta trocar o código hexadecimal (`#0a4d8c`). Use sites como [coolors.co](https://coolors.co) para escolher cores.

## 🔤 Como mudar o tamanho do texto padrão

No mesmo arquivo `css/estilo.css`:

```css
--tamanho-base: 16px;
```

Mude o `16px` para outro valor (ex: `18px`).

---

## 🧩 Como mudar o MENU principal

Abra `js/componentes.js`. Procure por `itensMenu`. Cada item tem este formato:

```javascript
{ texto: 'Início',  href: base + 'index.html',  id: 'index' },
```

Para adicionar um item novo, copie uma linha e cole abaixo.

---

## 📞 Como mudar TELEFONES IMPORTANTES

No final do arquivo `js/dados.js`:

```javascript
const TELEFONES = {
  secretaria: "24-2411-9300",
  ouvidoriaSaude: "2411-9328",
  ouvidoriaHFL: "2411-9475"
};
```

---

## 🌐 Como publicar o site

O site é puramente HTML/CSS/JS (não precisa de servidor especial). Você pode:

1. **Hospedar no GitHub Pages** (grátis): coloque os arquivos em um repositório no GitHub e ative GitHub Pages nas configurações
2. **Hospedar em qualquer servidor** (Hostinger, Locaweb, etc): faça upload dos arquivos via FTP
3. **Testar localmente**: basta clicar duas vezes no arquivo `index.html`

---

## 🆘 Algo quebrou! O que fazer?

1. **Não entre em pânico.** Geralmente é uma vírgula esquecida ou aspas faltando.
2. Abra o site no navegador, pressione **F12** e veja a aba "Console" — ela mostra o erro.
3. Compare o arquivo que você editou com a versão original (a cópia que você fez antes 😉).
4. Se nada funcionar, restaure a cópia de backup.

---

## 📋 Recursos do site

- ✅ **Menu** com barra de pesquisa
- ✅ **Botões de acessibilidade** (aumentar/diminuir texto)
- ✅ **Banner de emergência** (telefones SAMU, bombeiros)
- ✅ **Busca interna** em notícias, unidades, serviços e eventos
- ✅ **Filtros** na página de unidades
- ✅ **Links para Google Maps** automáticos a partir das coordenadas
- ✅ **Responsivo** (funciona em celular e computador)
- ✅ **FAQ interativo** (dúvidas frequentes)
- ✅ **Formulário de Ouvidoria** (precisa ser integrado a um e-mail/backend para funcionar de verdade)

---

## 💡 Dicas finais

- Use o **VS Code** (grátis): ele colore o código e mostra erros automaticamente.
- Antes de salvar, sempre faça **Ctrl+Z** se algo der errado.
- Mantenha uma **cópia de backup** sempre que for fazer uma mudança grande.

---

**Desenvolvido para a Secretaria Municipal de Saúde de Piraí** 🏥
