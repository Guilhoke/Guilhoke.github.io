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

document.addEventListener("DOMContentLoaded", () => {

  configurarCarrosselNoticias();
});