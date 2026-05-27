/* ==========================================================================
   ARQUIVO DE DADOS - SAÚDE DIGITAL PIRAÍ
   ==========================================================================
   ESTE É O ÚNICO ARQUIVO QUE VOCÊ PRECISA EDITAR PARA ATUALIZAR O SITE.

   COMO EDITAR:
   1) Para adicionar uma NOVA unidade, copie um bloco { ... } inteiro,
      cole logo abaixo e mude as informações.
   2) Para REMOVER uma unidade, apague todo o bloco { ... } incluindo
      a vírgula no final.
   3) Para EDITAR, basta trocar o texto dentro das aspas.
   4) NUNCA apague aspas, vírgulas, chaves { } ou colchetes [ ].
      Eles são parte do código.
   5) Para pegar coordenadas do Google Maps: clique com botão direito
      no local desejado no Google Maps e copie os dois números que
      aparecem (latitude e longitude).
   ========================================================================== */


/* --------------------------------------------------------------------------
   UNIDADES DE SAÚDE
   -------------------------------------------------------------------------- */
const UNIDADES = [
  {
    nome: "USF Santanésia",
    tipo: "Unidade de Saúde da Família",
    endereco: "Rua Edson Mota, nº 03",
    telefone: "2411-1233",
    lat: -22.6275,
    lng: -43.8985,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "Unidade da Fazendinha",
    tipo: "Unidade de Saúde",
    endereco: "Est. Hugo Lemgruber Portugal, s/n",
    telefone: "",
    lat: -22.6300,
    lng: -43.9000,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "USF Rosa Machado",
    tipo: "Unidade de Saúde da Família",
    endereco: "Rua D, nº 49",
    telefone: "2431-1009",
    lat: -22.6280,
    lng: -43.8970,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "Unidade de Sanatório da Serra",
    tipo: "Unidade de Saúde",
    endereco: "Estrada Sanatório da Serra, nº 7103",
    telefone: "",
    lat: -22.6400,
    lng: -43.9100,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "USF Ponte das Laranjeiras",
    tipo: "Unidade de Saúde da Família",
    endereco: "Rua Beira Lago, nº 73",
    telefone: "2411-9366",
    lat: -22.6320,
    lng: -43.9020,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "USF Casa Amarela",
    tipo: "Unidade de Saúde da Família",
    endereco: "Rua Bulhões de Carvalho, nº 349",
    telefone: "2411-9348",
    lat: -22.6290,
    lng: -43.8990,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "USF Centro",
    tipo: "Unidade de Saúde da Família",
    endereco: "Rua Capitão Manoel Torres, nº 33",
    telefone: "2411-9337",
    lat: -22.6285,
    lng: -43.8980,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "USF Jaqueira",
    tipo: "Unidade de Saúde da Família",
    endereco: "Rua B, nº 415",
    telefone: "2431-1170",
    lat: -22.6350,
    lng: -43.9050,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "USF Varjão",
    tipo: "Unidade de Saúde da Família",
    endereco: "Rua do Varjão, nº 186",
    telefone: "2431-6623",
    lat: -22.6360,
    lng: -43.9060,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "USF Cacaria",
    tipo: "Unidade de Saúde da Família",
    endereco: "Estrada da Cacaria, nº 590",
    telefone: "2431-7500",
    lat: -22.6500,
    lng: -43.9200,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "Unidade da Serra do Matoso",
    tipo: "Unidade de Saúde",
    endereco: "Largo do Matoso, s/n",
    telefone: "",
    lat: -22.6450,
    lng: -43.9150,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "USF Caiçaras",
    tipo: "Unidade de Saúde da Família",
    endereco: "Rua da Represa, nº 79",
    telefone: "2431-5069",
    lat: -22.6380,
    lng: -43.9080,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "USF Ribeirão das Lajes",
    tipo: "Unidade de Saúde da Família",
    endereco: "Ribeirão das Lajes, nº 120 A",
    telefone: "2431-7410",
    lat: -22.6700,
    lng: -43.9000,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "USF Arrozal",
    tipo: "Unidade de Saúde da Família",
    endereco: "Rua Isaura Rosa, nº 58",
    telefone: "3333-1322",
    lat: -22.5500,
    lng: -43.8000,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "Hospital Flávio Leal (HFL)",
    tipo: "Hospital",
    endereco: "Rua Roberto Silveira, nº 50",
    telefone: "2411-9450",
    lat: -22.6270,
    lng: -43.8975,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "Centro de Atenção Psicossocial (CAPS)",
    tipo: "Centro Especializado",
    endereco: "Rua Bulhões de Carvalho, nº 1241",
    telefone: "2411-9342",
    lat: -22.6295,
    lng: -43.8995,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "Fisioterapia de Arrozal",
    tipo: "Centro Especializado",
    endereco: "Rua Izaura Rosa, nº 59 Fundos",
    telefone: "3333-1921",
    lat: -22.5510,
    lng: -43.8010,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "Pronto Socorro de Arrozal",
    tipo: "Pronto Socorro",
    endereco: "Rua Izaura Rosa, nº 59 Frente",
    telefone: "3333-1935",
    lat: -22.5505,
    lng: -43.8005,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "Centro de Especialidades Médicas",
    tipo: "Centro Especializado",
    endereco: "Rua Moacyr Barbosa, nº 73",
    telefone: "2411-9328",
    lat: -22.6288,
    lng: -43.8982,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "SAD - Serviço de Atenção Domiciliar",
    tipo: "Serviço Especializado",
    endereco: "Rua Moacyr Barbosa, nº 73",
    telefone: "2411-9331",
    lat: -22.6288,
    lng: -43.8982,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "SEMAIA",
    tipo: "Serviço Especializado",
    endereco: "Rua Manoel Alexandre de Lima, nº 10",
    telefone: "2411-9342",
    lat: -22.6292,
    lng: -43.8988,
    foto: "img/unidade-placeholder.jpg"
  },
  {
    nome: "Vigilância Epidemiológica, Sanitária e Ambiental",
    tipo: "Vigilância em Saúde",
    endereco: "Rua Moacyr Barbosa, nº 98",
    telefone: "2411-9320",
    lat: -22.6289,
    lng: -43.8983,
    foto: "img/unidade-placeholder.jpg"
  }
];


/* --------------------------------------------------------------------------
   NOTÍCIAS
   Para adicionar uma nova notícia, copie um bloco { ... } e cole no
   TOPO da lista (a primeira aparece em destaque na home).
   -------------------------------------------------------------------------- */
const NOTICIAS = [
  {
    titulo: "Campanha de Vacinação contra a Gripe começa em Piraí",
    data: "20/05/2026",
    resumo: "Secretaria Municipal de Saúde inicia campanha em todas as unidades de saúde do município. Compareça à unidade mais próxima.",
    categoria: "Vacinação",
    link: "#"
  },
  {
    titulo: "Mutirão de Mamografia atende 200 mulheres em Piraí",
    data: "15/05/2026",
    resumo: "Ação aconteceu no Centro de Especialidades Médicas e atendeu mulheres entre 50 e 69 anos.",
    categoria: "Prevenção",
    link: "#"
  },
  {
    titulo: "PET-Saúde: novos profissionais integram a rede municipal",
    data: "10/05/2026",
    resumo: "Programa de Educação pelo Trabalho para a Saúde fortalece atendimento na atenção primária do município.",
    categoria: "PET-Saúde",
    link: "#"
  },
  {
    titulo: "Hospital Flávio Leal recebe novos equipamentos",
    data: "05/05/2026",
    resumo: "Investimento de mais de R$ 500 mil em modernização da rede hospitalar municipal.",
    categoria: "Infraestrutura",
    link: "#"
  }
];


/* --------------------------------------------------------------------------
   EVENTOS
   Para adicionar um novo evento, copie um bloco { ... } e cole na lista.
   -------------------------------------------------------------------------- */
const EVENTOS = [
  {
    titulo: "Dia D da Vacinação",
    data: "10/06/2026",
    horario: "08:00 às 17:00",
    local: "Todas as Unidades de Saúde",
    descricao: "Dia dedicado à atualização da caderneta de vacinação para todas as idades."
  },
  {
    titulo: "Capacitação de Agentes Comunitários",
    data: "15/06/2026",
    horario: "09:00 às 12:00",
    local: "Centro de Especialidades Médicas",
    descricao: "Treinamento sobre acolhimento humanizado e PET-Saúde."
  },
  {
    titulo: "Junho Vermelho - Doação de Sangue",
    data: "20/06/2026",
    horario: "08:00 às 14:00",
    local: "Hospital Flávio Leal",
    descricao: "Campanha de incentivo à doação de sangue em parceria com o HEMORIO."
  },
  {
    titulo: "Roda de Conversa - Saúde Mental",
    data: "25/06/2026",
    horario: "14:00 às 16:00",
    local: "CAPS Piraí",
    descricao: "Bate-papo sobre cuidados em saúde mental abertos à comunidade."
  }
];


/* --------------------------------------------------------------------------
   SERVIÇOS EXTERNOS (links da fachada)
   -------------------------------------------------------------------------- */
const SERVICOS = [
  {
    nome: "Resultados de Exames",
    descricao: "Acesse os resultados dos seus exames laboratoriais online.",
    icone: "🧪",
    link: "https://www.netlaudo.com.br/consulta/home/netlaudo.aspx"
  },
  {
    nome: "Agendamento de Mamografia",
    descricao: "Solicite agendamento para mamografia no Centro de Especialidades.",
    icone: "🎀",
    link: "#"
  },
  {
    nome: "Vacinação",
    descricao: "Confira o calendário e as campanhas de vacinação do município.",
    icone: "💉",
    link: "#"
  },
  {
    nome: "Atendimento Psicossocial (CAPS)",
    descricao: "Serviços de saúde mental e atendimento psicossocial.",
    icone: "🧠",
    link: "#"
  },
  {
    nome: "Pronto Socorro",
    descricao: "Em casos de emergência, dirija-se ao pronto socorro mais próximo.",
    icone: "🚑",
    link: "#"
  },
  {
    nome: "Atenção Domiciliar (SAD)",
    descricao: "Serviço de Atenção Domiciliar para pacientes elegíveis.",
    icone: "🏠",
    link: "#"
  }
];


/* --------------------------------------------------------------------------
   TELEFONES IMPORTANTES
   -------------------------------------------------------------------------- */
const TELEFONES = {
  secretaria: "24-2411-9300",
  ouvidoriaSaude: "2411-9328",
  ouvidoriaHFL: "2411-9475"
};
