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
CARROSSEL DE NOTÍCIAS DA HOME
-------------------------------------------------------------------------- */

function configurarCarrosselNoticias() {
  const carousel = document.querySelector(".hero-carousel");

  if (!carousel) return;

  const slides = carousel.querySelectorAll(".hero-slide");
  const indicadores = carousel.querySelectorAll(".hero-indicador");

  if (slides.length <= 1) return;

  const anterior = carousel.querySelector(".hero-carousel-prev");
  const proximo = carousel.querySelector(".hero-carousel-next");

  let slideAtual = 0;
  let intervalo;

  function mostrarSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.toggle("ativo", i === index);
    });

    indicadores.forEach((indicador, i) => {
      indicador.classList.toggle("ativo", i === index);
    });

    slideAtual = index;
  }

  function proximoSlide() {
    const novoIndice = (slideAtual + 1) % slides.length;
    mostrarSlide(novoIndice);
  }

  function slideAnterior() {
    const novoIndice =
      (slideAtual - 1 + slides.length) % slides.length;

    mostrarSlide(novoIndice);
  }

  function iniciarAutoPlay() {
    clearInterval(intervalo);

    intervalo = setInterval(() => {
      proximoSlide();
    }, 6000);
  }

  anterior?.addEventListener("click", () => {
    slideAnterior();
    iniciarAutoPlay();
  });

  proximo?.addEventListener("click", () => {
    proximoSlide();
    iniciarAutoPlay();
  });

  indicadores.forEach((indicador, index) => {
    indicador.addEventListener("click", () => {
      mostrarSlide(index);
      iniciarAutoPlay();
    });
  });

  carousel.addEventListener("mouseenter", () => {
    clearInterval(intervalo);
  });

  carousel.addEventListener("mouseleave", () => {
    iniciarAutoPlay();
  });

  mostrarSlide(0);
  iniciarAutoPlay();
}

/* --------------------------------------------------------------------------
   FILTRO DE UNIDADES DE SAÚDE
   -------------------------------------------------------------------------- */

function configurarFiltroUnidades() {
  const filtros = document.querySelectorAll(".filtro-unidades button[data-filtro]");
  const grid = document.getElementById("grid-unidades");

  if (!filtros.length || !grid) return;

  const cards = grid.querySelectorAll(".card-unidade[data-tipo]");

  // Mensagem exibida quando um filtro não encontra nenhuma unidade
  const semResultado = document.createElement("div");
  semResultado.className = "bloco-info";
  semResultado.style.display = "none";
  semResultado.innerHTML =
    "<strong>Nenhuma unidade encontrada para esse filtro.</strong>" +
    "<p style=\"margin-top:0.5rem\">Tente selecionar outra categoria ou clique em \"Todas\".</p>";
  grid.after(semResultado);

  function aplicarFiltro(tipoSelecionado) {
    let visiveis = 0;

    cards.forEach((card) => {
      const corresponde =
        tipoSelecionado === "todos" || card.dataset.tipo === tipoSelecionado;

      card.style.display = corresponde ? "" : "none";

      if (corresponde) visiveis += 1;
    });

    semResultado.style.display = visiveis === 0 ? "" : "none";
  }

  filtros.forEach((botao) => {
    botao.addEventListener("click", () => {
      filtros.forEach((b) => b.classList.remove("ativo"));
      botao.classList.add("ativo");

      aplicarFiltro(botao.dataset.filtro);
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {

  configurarCarrosselNoticias();
  configurarFiltroUnidades();
});