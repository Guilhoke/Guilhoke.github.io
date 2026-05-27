/* ==========================================================================
   SCRIPT PRINCIPAL - SAÚDE DIGITAL PIRAÍ
   ==========================================================================
   Este arquivo controla:
   - Menu mobile (botão hamburguer)
   - Botões de aumento/redução de texto (acessibilidade)
   - Barra de pesquisa
   - Renderização dinâmica de unidades, notícias, eventos e serviços
     (puxa do arquivo dados.js)
   ========================================================================== */


/* --------------------------------------------------------------------------
   ACESSIBILIDADE — Aumento e Redução de Texto
   -------------------------------------------------------------------------- */
(function controleTexto() {
  const root = document.documentElement;
  let tamanhoAtual = parseInt(localStorage.getItem('saude-pirai-fonte') || '16');

  function aplicarTamanho() {
    root.style.setProperty('--tamanho-base', tamanhoAtual + 'px');
    localStorage.setItem('saude-pirai-fonte', tamanhoAtual);
  }

  aplicarTamanho();

  document.querySelectorAll('[data-acao="aumentar-fonte"]').forEach(btn => {
    btn.addEventListener('click', () => {
      if (tamanhoAtual < 22) { tamanhoAtual += 2; aplicarTamanho(); }
    });
  });

  document.querySelectorAll('[data-acao="diminuir-fonte"]').forEach(btn => {
    btn.addEventListener('click', () => {
      if (tamanhoAtual > 12) { tamanhoAtual -= 2; aplicarTamanho(); }
    });
  });

  document.querySelectorAll('[data-acao="resetar-fonte"]').forEach(btn => {
    btn.addEventListener('click', () => { tamanhoAtual = 16; aplicarTamanho(); });
  });
})();


/* --------------------------------------------------------------------------
   MENU MOBILE
   -------------------------------------------------------------------------- */
(function menuMobile() {
  const btn = document.querySelector('.menu-toggle');
  const menu = document.querySelector('.menu');
  if (!btn || !menu) return;
  btn.addEventListener('click', () => {
    menu.classList.toggle('aberto');
    btn.setAttribute('aria-expanded', menu.classList.contains('aberto'));
  });
})();


/* --------------------------------------------------------------------------
   BARRA DE PESQUISA
   Procura nos títulos de notícias, eventos, serviços e unidades.
   -------------------------------------------------------------------------- */
(function barraPesquisa() {
  const forms = document.querySelectorAll('.busca');
  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = form.querySelector('input');
      const termo = (input.value || '').trim().toLowerCase();
      if (!termo) return;
      window.location.href = 'paginas/busca.html?q=' + encodeURIComponent(termo);
    });
  });
})();


/* --------------------------------------------------------------------------
   RENDERIZADORES
   Estas funções verificam se elementos existem na página atual
   e, se existirem, preenchem com dados de dados.js
   -------------------------------------------------------------------------- */

// ----- SERVIÇOS -----
function renderServicos() {
  const container = document.getElementById('grid-servicos');
  if (!container || typeof SERVICOS === 'undefined') return;
  container.innerHTML = SERVICOS.map((s, i) => `
    <a href="${s.link}" target="${s.link.startsWith('http') ? '_blank' : '_self'}" rel="noopener" class="card-servico fade-up" style="animation-delay:${i * 0.08}s">
      <div class="icone">${s.icone}</div>
      <h3>${s.nome}</h3>
      <p>${s.descricao}</p>
      <span class="acessar">Acessar →</span>
    </a>
  `).join('');
}

// ----- NOTÍCIAS -----
function renderNoticias(limite) {
  const container = document.getElementById('grid-noticias');
  if (!container || typeof NOTICIAS === 'undefined') return;
  const lista = limite ? NOTICIAS.slice(0, limite) : NOTICIAS;
  container.innerHTML = lista.map((n, i) => `
    <article class="card-noticia ${i === 0 && limite ? 'destaque' : ''} fade-up" style="animation-delay:${i * 0.08}s">
      <div class="imagem">📰</div>
      <div class="conteudo">
        <span class="categoria">${n.categoria}</span>
        <h3>${n.titulo}</h3>
        <p class="data">📅 ${n.data}</p>
        <p>${n.resumo}</p>
      </div>
    </article>
  `).join('');
}

// ----- EVENTOS -----
function renderEventos(limite) {
  const container = document.getElementById('lista-eventos');
  if (!container || typeof EVENTOS === 'undefined') return;
  const lista = limite ? EVENTOS.slice(0, limite) : EVENTOS;
  container.innerHTML = lista.map((e, i) => {
    const [dia, mes] = e.data.split('/');
    const meses = ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ'];
    const mesNome = meses[parseInt(mes) - 1] || mes;
    return `
      <article class="card-evento fade-up" style="animation-delay:${i * 0.08}s">
        <div class="data-box">
          <span class="dia">${dia}</span>
          <span class="mes">${mesNome}</span>
        </div>
        <div>
          <h3>${e.titulo}</h3>
          <div class="info">
            <span>🕐 ${e.horario}</span>
            <span>📍 ${e.local}</span>
          </div>
          <p>${e.descricao}</p>
        </div>
      </article>
    `;
  }).join('');
}

// ----- UNIDADES -----
function renderUnidades(filtro = 'todos') {
  const container = document.getElementById('grid-unidades');
  if (!container || typeof UNIDADES === 'undefined') return;

  const iconePorTipo = {
    'Hospital': '🏥',
    'Unidade de Saúde da Família': '🏠',
    'Unidade de Saúde': '🏥',
    'Centro Especializado': '⚕️',
    'Pronto Socorro': '🚑',
    'Serviço Especializado': '🩺',
    'Vigilância em Saúde': '🔬'
  };

  const lista = filtro === 'todos'
    ? UNIDADES
    : UNIDADES.filter(u => u.tipo === filtro);

  if (lista.length === 0) {
    container.innerHTML = '<p style="text-align:center;color:var(--cor-texto-claro);grid-column:1/-1;padding:3rem">Nenhuma unidade encontrada para esse filtro.</p>';
    return;
  }

  container.innerHTML = lista.map((u, i) => `
    <article class="card-unidade fade-up" style="animation-delay:${i * 0.05}s">
      <div class="imagem-unidade">
        ${iconePorTipo[u.tipo] || '🏥'}
        <span class="tipo-tag">${u.tipo}</span>
      </div>
      <div class="conteudo-unidade">
        <h3>${u.nome}</h3>
        <div class="info-linha">
          <span class="ico">📍</span>
          <span>${u.endereco}</span>
        </div>
        ${u.telefone ? `
          <div class="info-linha">
            <span class="ico">📞</span>
            <span>${u.telefone}</span>
          </div>
        ` : ''}
        <div class="acoes">
          <a href="https://www.google.com/maps/search/?api=1&query=${u.lat},${u.lng}" target="_blank" rel="noopener">Ver no Mapa</a>
          ${u.telefone ? `<a href="tel:${u.telefone.replace(/\D/g, '')}" class="secundario">Ligar</a>` : ''}
        </div>
      </div>
    </article>
  `).join('');
}

// ----- FILTROS DE UNIDADES -----
function configurarFiltrosUnidades() {
  const filtros = document.querySelectorAll('.filtro-unidades button');
  if (filtros.length === 0) return;

  filtros.forEach(btn => {
    btn.addEventListener('click', () => {
      filtros.forEach(b => b.classList.remove('ativo'));
      btn.classList.add('ativo');
      renderUnidades(btn.dataset.filtro);
    });
  });
}

// ----- TELEFONES IMPORTANTES (na home) -----
function renderTelefones() {
  const container = document.getElementById('lista-telefones');
  if (!container || typeof TELEFONES === 'undefined') return;
  container.innerHTML = `
    <li><span>Secretaria Municipal de Saúde</span><strong>${TELEFONES.secretaria}</strong></li>
    <li><span>Ouvidoria da Saúde</span><strong>${TELEFONES.ouvidoriaSaude}</strong></li>
    <li><span>Ouvidoria Hospital Flávio Leal</span><strong>${TELEFONES.ouvidoriaHFL}</strong></li>
  `;
}


/* --------------------------------------------------------------------------
   BUSCA - Página de resultados
   -------------------------------------------------------------------------- */
function renderResultadosBusca() {
  const container = document.getElementById('resultados-busca');
  if (!container) return;

  const params = new URLSearchParams(window.location.search);
  const termo = (params.get('q') || '').toLowerCase();
  const titulo = document.getElementById('termo-busca');
  if (titulo) titulo.textContent = termo;

  if (!termo) {
    container.innerHTML = '<p>Digite algo na barra de pesquisa para começar.</p>';
    return;
  }

  let resultados = [];

  if (typeof UNIDADES !== 'undefined') {
    UNIDADES.forEach(u => {
      if ((u.nome + ' ' + u.endereco + ' ' + u.tipo).toLowerCase().includes(termo)) {
        resultados.push({ tipo: 'Unidade', titulo: u.nome, descricao: u.endereco, link: 'unidades.html' });
      }
    });
  }
  if (typeof NOTICIAS !== 'undefined') {
    NOTICIAS.forEach(n => {
      if ((n.titulo + ' ' + n.resumo).toLowerCase().includes(termo)) {
        resultados.push({ tipo: 'Notícia', titulo: n.titulo, descricao: n.resumo, link: '#' });
      }
    });
  }
  if (typeof EVENTOS !== 'undefined') {
    EVENTOS.forEach(e => {
      if ((e.titulo + ' ' + e.descricao + ' ' + e.local).toLowerCase().includes(termo)) {
        resultados.push({ tipo: 'Evento', titulo: e.titulo, descricao: e.descricao, link: 'eventos.html' });
      }
    });
  }
  if (typeof SERVICOS !== 'undefined') {
    SERVICOS.forEach(s => {
      if ((s.nome + ' ' + s.descricao).toLowerCase().includes(termo)) {
        resultados.push({ tipo: 'Serviço', titulo: s.nome, descricao: s.descricao, link: s.link });
      }
    });
  }

  if (resultados.length === 0) {
    container.innerHTML = `
      <div class="bloco-info">
        <strong>Nenhum resultado encontrado para "${termo}".</strong>
        <p style="margin-top:0.5rem">Tente buscar por palavras como: vacina, unidade, exames, mamografia, CAPS, etc.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <p style="margin-bottom:1.5rem;color:var(--cor-texto-claro)">${resultados.length} resultado(s) encontrado(s)</p>
    ${resultados.map(r => `
      <a href="${r.link}" class="card-servico" style="margin-bottom:1rem">
        <span class="categoria" style="display:inline-block;background:var(--cor-fundo-suave);color:var(--cor-primaria);font-size:0.7rem;font-weight:600;padding:0.25rem 0.6rem;border-radius:4px;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem">${r.tipo}</span>
        <h3>${r.titulo}</h3>
        <p>${r.descricao}</p>
      </a>
    `).join('')}
  `;
}


/* --------------------------------------------------------------------------
   FORMULÁRIO DE OUVIDORIA - Apenas demonstração
   Em produção, conectar a um backend ou serviço de e-mail.
   -------------------------------------------------------------------------- */
function configurarOuvidoria() {
  const form = document.getElementById('form-ouvidoria');
  if (!form) return;
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Sua mensagem foi registrada. Em breve entraremos em contato.\n\nObs: este formulário é apenas demonstrativo. Para integração com e-mail/sistema, é preciso conectar a um servidor.');
    form.reset();
  });
}


/* --------------------------------------------------------------------------
   INICIALIZAÇÃO
   Tudo que precisa rodar quando a página carrega
   -------------------------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
  renderServicos();
  renderNoticias(4);
  renderEventos();
  renderUnidades();
  renderTelefones();
  configurarFiltrosUnidades();
  renderResultadosBusca();
  configurarOuvidoria();
});
