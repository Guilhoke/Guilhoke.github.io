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

const CARROSSEL_INTERVALO_MS = 6000;

// Distância mínima, em pixels, para um arrasto contar como troca de slide.
// Abaixo disso tratamos como toque acidental durante a rolagem da página.
const CARROSSEL_LIMIAR_ARRASTO = 50;

function configurarCarrosselNoticias() {
  const carousel = document.querySelector(".hero-carousel");

  if (!carousel) return;

  const slides = Array.from(carousel.querySelectorAll(".hero-slide"));
  const indicadores = Array.from(carousel.querySelectorAll(".hero-indicador"));

  if (slides.length <= 1) return;

  const anterior = carousel.querySelector(".hero-carousel-prev");
  const proximo = carousel.querySelector(".hero-carousel-next");

  // Quem pediu redução de movimento no sistema não recebe troca automática:
  // continua podendo navegar pelas setas, indicadores e swipe.
  const movimentoReduzido = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  );

  let slideAtual = 0;
  let intervalo = null;
  let pausadoPeloUsuario = false;

  function mostrarSlide(index) {
    slideAtual = (index + slides.length) % slides.length;

    slides.forEach((slide, i) => {
      const ativo = i === slideAtual;

      slide.classList.toggle("ativo", ativo);

      // Impede que leitores de tela e a navegação por Tab alcancem o
      // conteúdo (inclusive o link "Saiba mais") dos slides escondidos.
      slide.setAttribute("aria-hidden", ativo ? "false" : "true");
      slide.inert = !ativo;
    });

    indicadores.forEach((indicador, i) => {
      const ativo = i === slideAtual;

      indicador.classList.toggle("ativo", ativo);
      indicador.setAttribute("aria-selected", ativo ? "true" : "false");
    });
  }

  function irPara(index) {
    mostrarSlide(index);
    reiniciarAutoPlay();
  }

  function pararAutoPlay() {
    clearInterval(intervalo);
    intervalo = null;
  }

  function reiniciarAutoPlay() {
    pararAutoPlay();

    // Não roda com movimento reduzido, com a aba em segundo plano (onde o
    // navegador estrangula os timers e os slides "pulam" ao voltar), nem
    // enquanto o usuário está lendo/interagindo com o carrossel.
    if (movimentoReduzido.matches) return;
    if (document.hidden) return;
    if (pausadoPeloUsuario) return;

    intervalo = setInterval(() => mostrarSlide(slideAtual + 1), CARROSSEL_INTERVALO_MS);
  }

  function pausar() {
    pausadoPeloUsuario = true;
    pararAutoPlay();
  }

  function retomar() {
    pausadoPeloUsuario = false;
    reiniciarAutoPlay();
  }

  anterior?.addEventListener("click", () => irPara(slideAtual - 1));
  proximo?.addEventListener("click", () => irPara(slideAtual + 1));

  indicadores.forEach((indicador, index) => {
    indicador.addEventListener("click", () => irPara(index));
  });

  // Mouse: pausa ao passar por cima. `(hover: hover)` evita que celulares,
  // onde um toque dispara mouseenter e nunca mouseleave, travem o autoplay.
  if (window.matchMedia("(hover: hover)").matches) {
    carousel.addEventListener("mouseenter", pausar);
    carousel.addEventListener("mouseleave", retomar);
  }

  // Teclado: pausa enquanto algum controle está focado e permite navegar
  // com as setas.
  carousel.addEventListener("focusin", pausar);
  carousel.addEventListener("focusout", (evento) => {
    if (!carousel.contains(evento.relatedTarget)) retomar();
  });

  carousel.addEventListener("keydown", (evento) => {
    if (evento.key === "ArrowLeft") {
      evento.preventDefault();
      irPara(slideAtual - 1);
    } else if (evento.key === "ArrowRight") {
      evento.preventDefault();
      irPara(slideAtual + 1);
    }
  });

  // Aba em segundo plano: não adianta trocar slide que ninguém vê.
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) pararAutoPlay();
    else reiniciarAutoPlay();
  });

  // Swipe no celular. Usamos Pointer Events (cobre toque, caneta e mouse) e
  // só tratamos como swipe quando o movimento é mais horizontal que vertical
  // — assim rolar a página verticalmente sobre o carrossel continua normal.
  let xInicial = null;
  let yInicial = null;

  carousel.addEventListener(
    "pointerdown",
    (evento) => {
      if (evento.pointerType === "mouse") return;

      xInicial = evento.clientX;
      yInicial = evento.clientY;

      pausar();
    },
    { passive: true }
  );

  function finalizarArrasto(evento) {
    if (xInicial === null) return;

    const deltaX = evento.clientX - xInicial;
    const deltaY = evento.clientY - yInicial;

    xInicial = null;
    yInicial = null;

    if (
      Math.abs(deltaX) > CARROSSEL_LIMIAR_ARRASTO &&
      Math.abs(deltaX) > Math.abs(deltaY)
    ) {
      mostrarSlide(deltaX < 0 ? slideAtual + 1 : slideAtual - 1);
    }

    retomar();
  }

  carousel.addEventListener("pointerup", finalizarArrasto, { passive: true });

  carousel.addEventListener(
    "pointercancel",
    () => {
      xInicial = null;
      yInicial = null;
      retomar();
    },
    { passive: true }
  );

  // Se o usuário mudar a preferência de movimento com a página aberta.
  movimentoReduzido.addEventListener("change", reiniciarAutoPlay);

  mostrarSlide(0);
  reiniciarAutoPlay();
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