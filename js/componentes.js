/* ==========================================================================
   COMPONENTES REUTILIZÁVEIS - CABEÇALHO E RODAPÉ
   ==========================================================================
   Este arquivo gera automaticamente o cabeçalho e rodapé em todas as páginas.

   PARA EDITAR O MENU:
   - Mude os textos e os "href" na variável "itensMenu" abaixo.

   PARA EDITAR O RODAPÉ:
   - Mude o conteúdo HTML dentro de gerarRodape().

   IMPORTANTE: o "caminho" é ajustado automaticamente para que as páginas
   internas (dentro da pasta /paginas) encontrem os arquivos corretos.
   ========================================================================== */

(function componentesSite() {

  // Detecta se a página atual está dentro da pasta /paginas
  const estaEmSubpasta = window.location.pathname.includes('/paginas/');
  const base = estaEmSubpasta ? '../' : '';
  const basePag = estaEmSubpasta ? '' : 'paginas/';

  // Identifica qual página está ativa para destacar no menu
  const arquivoAtual = window.location.pathname.split('/').pop().replace('.html', '') || 'index';

  // ----- ITENS DO MENU PRINCIPAL -----
  const itensMenu = [
    { texto: 'Início',         href: base + 'index.html',          id: 'index' },
    { texto: 'Serviços',       href: basePag + 'servicos.html',    id: 'servicos' },
    { texto: 'Unidades',       href: basePag + 'unidades.html',    id: 'unidades' },
    { texto: 'Eventos',        href: basePag + 'eventos.html',     id: 'eventos' },
    { texto: 'Profissionais',  href: basePag + 'profissionais.html', id: 'profissionais' },
    { texto: 'Servidor',       href: basePag + 'servidor.html',    id: 'servidor' },
    { texto: 'Ouvidoria',      href: basePag + 'ouvidoria.html',   id: 'ouvidoria' },
    { texto: 'Dúvidas',        href: basePag + 'duvidas.html',     id: 'duvidas' },
    { texto: 'Transparência',  href: basePag + 'transparencia.html', id: 'transparencia' }
  ];

  function gerarCabecalho() {
    return `
      <!-- BARRA DE ACESSIBILIDADE -->
      <div class="barra-topo">
        <div class="container">
          <div>
            <span>Prefeitura Municipal de Piraí</span> • <span>Secretaria de Saúde</span>
          </div>
          <div class="acessibilidade">
            <span class="label-acc">Acessibilidade:</span>
            <button data-acao="diminuir-fonte" title="Diminuir texto" aria-label="Diminuir texto">A−</button>
            <button data-acao="resetar-fonte" title="Restaurar tamanho" aria-label="Restaurar tamanho">A</button>
            <button data-acao="aumentar-fonte" title="Aumentar texto" aria-label="Aumentar texto">A+</button>
          </div>
        </div>
      </div>

      <!-- CABEÇALHO COM LOGO E BUSCA -->
      <header class="cabecalho">
        <div class="container">
          <a href="${base}index.html" class="logo">
            <img src="img/logo.jpg" alt="Logo Saúde Digital Piraí" class="logo-imagem">
            <div class="logo-texto">
              <h1>Saúde Digital Piraí</h1>
              <p>Secretaria Municipal de Saúde</p>
            </div>
          </a>

          <form class="busca" role="search">
            <input type="search" placeholder="Pesquisar no site..." aria-label="Pesquisar" />
            <button type="submit" aria-label="Pesquisar">🔍</button>
          </form>
        </div>
      </header>

      <!-- NAVEGAÇÃO PRINCIPAL -->
      <nav class="navbar" aria-label="Menu principal">
        <div class="container">
          <button class="menu-toggle" aria-label="Abrir menu" aria-expanded="false">☰ Menu</button>
          <ul class="menu">
            ${itensMenu.map(item => `
              <li><a href="${item.href}" class="${arquivoAtual === item.id ? 'ativo' : ''}">${item.texto}</a></li>
            `).join('')}
          </ul>
        </div>
      </nav>
    `;
  }

  function gerarRodape() {
    return `
      <footer class="rodape">
        <div class="container">
          <div class="rodape-grid">
            <div>
              <h4>Saúde Digital Piraí</h4>
              <p style="line-height:1.7">Portal oficial da Secretaria Municipal de Saúde de Piraí. Informação, serviços e cuidado para todos os munícipes.</p>
              <p style="margin-top:1rem">
                <strong style="color:white">📞 ${typeof TELEFONES !== 'undefined' ? TELEFONES.secretaria : '24-2411-9300'}</strong>
              </p>
            </div>
            <div>
              <h4>Acesso Rápido</h4>
              <ul>
                <li><a href="${basePag}servicos.html">Serviços</a></li>
                <li><a href="${basePag}unidades.html">Unidades de Saúde</a></li>
                <li><a href="${basePag}eventos.html">Eventos</a></li>
                <li><a href="${basePag}ouvidoria.html">Ouvidoria</a></li>
              </ul>
            </div>
            <div>
              <h4>Para o Cidadão</h4>
              <ul>
                <li><a href="https://www.netlaudo.com.br/consulta/home/netlaudo.aspx" target="_blank" rel="noopener">Resultados de Exames</a></li>
                <li><a href="${basePag}duvidas.html">Dúvidas Frequentes</a></li>
                <li><a href="${basePag}transparencia.html">Transparência</a></li>
                <li><a href="${basePag}profissionais.html">Profissionais</a></li>
              </ul>
            </div>
            <div>
              <h4>Para o Servidor</h4>
              <ul>
                <li><a href="${basePag}servidor.html">Portal do Servidor</a></li>
                <li><a href="${basePag}servidor.html">PET-Saúde</a></li>
                <li><a href="${basePag}ouvidoria.html">Reclamações</a></li>
              </ul>
            </div>
          </div>
          <div class="rodape-creditos">
            <p>© 2026 Prefeitura Municipal de Piraí — Secretaria Municipal de Saúde. Todos os direitos reservados.</p>
            <p style="margin-top:0.4rem">Endereço: Rua Moacyr Barbosa, nº 98 — Centro, Piraí — RJ</p>
          </div>
        </div>
      </footer>
    `;
  }

  function gerarBannerEmergencia() {
    return `
      <div class="banner-emergencia">
        <div class="container">
          <strong>🚨 EMERGÊNCIA:</strong>
          <span>SAMU <a href="tel:192">192</a></span>
          <span>Bombeiros <a href="tel:193">193</a></span>
          <span>Pronto Socorro Arrozal <a href="tel:33331935">3333-1935</a></span>
        </div>
      </div>
    `;
  }

  // Insere automaticamente os componentes
  const headerSlot = document.getElementById('site-header');
  if (headerSlot) headerSlot.innerHTML = gerarCabecalho();

  const emergenciaSlot = document.getElementById('site-emergencia');
  if (emergenciaSlot) emergenciaSlot.innerHTML = gerarBannerEmergencia();

  const footerSlot = document.getElementById('site-footer');
  if (footerSlot) footerSlot.innerHTML = gerarRodape();

})();
