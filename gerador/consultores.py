# -*- coding: utf-8 -*-
"""Dados dos consultores do plano Me Diz o Que Fazer.

O conteúdo vem dos documentos de apresentação escritos pelos próprios
consultores. Cada tipo de informação está num campo diferente porque a página
os apresenta de formas diferentes:

    frase       declaração de propósito, em destaque ao lado do retrato
    proposito   o resto do texto de propósito, em corpo de leitura
    marcos      a trajetória como linha do tempo, (quando, o que aconteceu)
    interesses  fatos curtos de "fora do escritório", como etiquetas
    fora        uma frase que amarra os interesses

Os marcos foram extraídos da trajetória que cada um escreveu, mantendo as
datas e a ordem do original. O texto de propósito segue na voz de cada um.
Para acrescentar um consultor, some uma entrada aqui e ele passa a existir no
build sem mais nenhuma mudança.
"""

CONSULTORES = [
    dict(
        slug="alan-santanna",
        nome="Alan Sant'Anna",
        nome_completo="Alan Feitosa Sant'Anna",
        papel="Consultor de investimentos",
        frase="Minha missão é absorver toda a complexidade matemática e analítica do mercado "
              "e traduzi-la em estratégias simples, seguras e personalizadas para os seus objetivos.",
        proposito=[
            "Sou apaixonado por educação financeira e pelo poder que os investimentos têm de "
            "transformar a vida das pessoas. Meu propósito vai muito além de indicar ativos: é "
            "garantir que você compreenda o cenário econômico, com total clareza e segurança "
            "sobre as escolhas que fazemos juntos.",
            "Para isso tenho uma abordagem educativa e consultiva, aliada a rigor técnico e a "
            "alta capacidade analítica fundamentada em dados — modelagem financeira, leitura de "
            "demonstrações contábeis e visão macroeconômica.",
        ],
        marcos=[
            ("Até 2022", "Quase dez anos empreendendo — o que me deu uma verdadeira visão de "
                      "dono: sei quais são as dores de tocar um negócio no Brasil."),
            ("Em paralelo", "Alguns anos como fotógrafo profissional, experiência que me ensinou a "
                      "olhar com mais cuidado para os detalhes."),
            ("2022", "Entrada no mercado financeiro, gerenciando e estruturando carteiras para "
                     "pessoa física — alta renda e varejo — e pessoa jurídica."),
            ("Hoje", "Consultor na AUVP Capital, com valuation, fluxo de caixa e leitura de "
                     "balanço no dia a dia da recomendação."),
        ],
        interesses=["Viagens", "Intercâmbio em Cambridge", "Fotografia",
                    "Música", "Ciclismo", "Academia"],
        fora="Sempre fui curioso e valorizo viver novas experiências e conhecer outras culturas. "
             "A música é a minha grande válvula de escape.",
        graduacao=["Bacharelado em Ciências Econômicas — IBMEC"],
        pos=[
            "Ciência de Dados (Google Data Analytics), em curso",
            "Análise de Dados com SQL e Power BI, em curso",
            "Finanças Comportamentais",
        ],
        certificacoes=["CPA", "C-Pro I", "C-Pro R", "FBB100"],
    ),
    dict(
        slug="andre-arruda",
        nome="André Arruda",
        nome_completo="André Arruda",
        papel="Consultor de investimentos",
        frase="O trabalho de um consultor deve ir além de recomendar investimentos: deve alinhar "
              "expectativas, informar e até educar sobre cada passo — e fazer tudo isso de "
              "maneira honesta.",
        proposito=[
            "Minha vida profissional começou na gráfica do meu avô, num tempo em que a principal "
            "prateleira de informações eram as bibliotecas. Minha função? Diagramador. Foi a "
            "partir dali que começou o gosto por aprender e me informar, que resultou na minha "
            "formação como jornalista e me trouxe até aqui.",
            "Da mesma maneira que, como jornalista, meu propósito era informar de forma confiável "
            "e imparcial, como consultor compartilho do mesmo propósito.",
        ],
        marcos=[
            ("Início", "Diagramador na gráfica do avô, onde nasceu o gosto por aprender e informar."),
            ("Depois", "Formação e atuação como jornalista."),
            ("Pandemia", "Deixa o mercado da comunicação para estudar economia e investimentos."),
            ("2022", "Primeira certificação, a antiga CEA, e início como consultor independente."),
            ("Hoje", "Depois de quase quatro anos atuando por conta própria, consultor na AUVP Capital."),
        ],
        interesses=["Surfe", "Praia de Itamambuca", "Viagens", "Música", "Cinema", "Família e amigos"],
        fora="Meu lugar preferido no mundo é Itamambuca, em Ubatuba, e meu esporte favorito é o "
             "surfe. Fica a sugestão de música e de filme: <em>Time</em>, do Pink Floyd, e "
             "<em>Cinema Paradiso</em>.",
        graduacao=["Jornalismo"],
        pos=["Investimentos, Finanças e Banking"],
        certificacoes=["CPA", "C-Pro I", "C-Pro R"],
    ),
    dict(
        slug="bolivar-oliveira",
        nome="Bolívar Oliveira",
        nome_completo="Bolívar Oliveira",
        papel="Consultor de investimentos",
        frase="Educação financeira não se resume a ensinar alguém a investir, mas a oferecer "
              "conhecimento para que cada pessoa tome decisões melhores e construa um futuro mais "
              "próspero para si e para sua família.",
        proposito=[
            "Sou apaixonado pelo mercado financeiro, pela educação e pelo impacto que o "
            "conhecimento pode gerar na vida das pessoas.",
            "Desenvolvi experiência prática com educação financeira, análise de diferentes "
            "produtos e estratégias, relacionamento com investidores e tradução de conceitos "
            "complexos em decisões mais claras e conscientes.",
        ],
        marcos=[
            ("Antes", "Mais de dois anos como instrutor de inglês e, antes disso, um ano e meio "
                      "no atendimento ao público — onde desenvolvi comunicação e didática."),
            ("2023", "Entrada no mercado financeiro, primeiro como investidor e estudante."),
            ("Desde então", "Formação pela AUVP Escola e certificações ANBIMA."),
            ("Hoje", "Consultor na AUVP Capital, ajudando cada cliente a compreender melhor as "
                     "próprias decisões."),
        ],
        interesses=["Família", "Inglês fluente", "Aprendizado constante", "Princípios"],
        fora="Valorizo profundamente minha família, meus amigos e os princípios que construí ao "
             "longo da vida. Procuro viver com curiosidade e propósito.",
        graduacao=["Experiências acadêmicas em Marketing e em Direito", "Aluno da AUVP Escola"],
        pos=["Inglês fluente"],
        certificacoes=["CPA", "C-Pro I", "C-Pro R"],
    ),
    dict(
        slug="danilo-barbosa",
        nome="Danilo Barbosa",
        nome_completo="Danilo Barbosa",
        papel="Consultor de investimentos",
        frase="Vamos construir juntos o seu futuro financeiro, tijolo a tijolo, focando sempre no "
              "que o seu <em>eu do futuro</em> espera das decisões tomadas hoje.",
        proposito=[
            "Vamos traçar esse caminho com responsabilidade, planejamento e estratégia, visando "
            "seus objetivos e a constância no longo prazo. É assim que se alcança o que se almeja "
            "com tranquilidade e sem correr riscos desnecessários.",
            "Investir é uma ferramenta fundamental não só para potencializar seus resultados, mas "
            "também para proteger você dos reveses da vida. Comigo você terá um olhar maduro e "
            "livre de conflito de interesses sobre o seu patrimônio.",
        ],
        marcos=[
            ("2016", "Começo no mundo dos investimentos, entre aportes e estudo do tema."),
            ("Depois", "Passo a compartilhar essa experiência com muitas pessoas — o que acabou "
                       "se tornando o meu trabalho."),
            ("Hoje", "Consultor na AUVP Capital, acompanhando investidores que realizaram a casa "
                     "própria, o casamento, o primeiro carro ou o simples alívio de ter clareza."),
        ],
        interesses=["Música", "Violão, guitarra e baixo", "Queen", "Leitura",
                    "Viagens", "Inglês e francês"],
        fora="Tenho a guitarra <em>signature</em> do Brian May. Nos livros gosto de psicologia, "
             "filosofia e biografias; em viagem, o que mais gosto é conversar com pessoas de "
             "outras nacionalidades.",
        graduacao=["Administração de Empresas", "Gestão Financeira"],
        pos=["Análise de Dados"],
        certificacoes=["CPA", "C-Pro I", "C-Pro R"],
    ),
    dict(
        slug="erika-barreto",
        nome="Erika Barreto",
        nome_completo="Erika Barreto",
        papel="Consultora de investimentos",
        frase="As decisões financeiras sobre o próprio patrimônio devem ser tomadas com clareza. "
              "Por isso gosto muito de responder às perguntas que as pessoas têm depois de estudar.",
        proposito=[
            "Sou movida pela vontade de aprender e, com o mercado financeiro, entendi que também "
            "gosto de ensinar.",
            "No dia a dia, busco ser didática para desmistificar o mercado. Gosto de conversar de "
            "forma clara e de fácil entendimento.",
        ],
        marcos=[
            ("2019", "Conheço o mercado financeiro economizando com o foco em fazer um intercâmbio."),
            ("Pandemia", "Com o dinheiro acumulado, decido fazer aquele valor render e começo a "
                         "estudar, acompanhando de perto o trabalho do Investidor Sardinha."),
            ("Depois", "O interesse pela área vira especialização."),
            ("Hoje", "Consultora na AUVP Capital há mais de um ano."),
        ],
        interesses=["Viagens", "Leitura", "Quebra-cabeças", "Praia", "Fins de semana no interior"],
        fora="Gosto de viajar para conhecer culturas diferentes e sou viciada em quebra-cabeças. "
             "Para desacelerar da cidade grande, passo fins de semana no interior com o meu avô.",
        graduacao=["Gestão Financeira"],
        pos=[],
        certificacoes=["CPA", "C-Pro I", "C-Pro R"],
    ),
    dict(
        slug="nasser-tanure",
        nome="Nasser Tanure",
        nome_completo="Nasser Tanure Amantes",
        papel="Consultor de investimentos",
        frase="Investir vai muito além de planilhas e rentabilidade: trata-se de educação e de "
              "planejamento de vida.",
        proposito=[
            "O que me move é a paixão por usar os investimentos como uma ponte para ajudar as "
            "pessoas a realizarem seus sonhos. Essa veia educacional é herança da minha mãe, que "
            "dedicou a vida inteira à profissão de professora.",
            "Acredito que, ao educar financeiramente, consigo empoderar as pessoas para que tomem "
            "as melhores decisões para o futuro de suas famílias.",
        ],
        marcos=[
            ("Antes", "Processos de turnaround de empresas e outros segmentos financeiros e "
                      "corporativos, fora da esfera tradicional de investimentos — o que me deu "
                      "visão sistêmica de alocação de recursos, fluxo de caixa e economia."),
            ("Irlanda", "Um ano morando fora, onde apurei a comunicação com pessoas de perfis e "
                        "culturas diferentes."),
            ("Hoje", "Consultor na AUVP Capital, dedicado a entender as necessidades e os "
                     "objetivos de cada investidor."),
        ],
        interesses=["Musculação", "Corrida", "Leitura", "Desenvolvimento pessoal", "Futebol"],
        fora="A disciplina necessária para construir um bom patrimônio é a mesma que aplico no meu "
             "estilo de vida. Esses interesses me ajudam a manter foco e equilíbrio.",
        graduacao=["Engenharia de Produção — UFOP"],
        pos=["MBA em Gestão de Investimentos", "MBA em Gestão de Negócios, em curso"],
        certificacoes=["CPA", "C-Pro I", "C-Pro R"],
    ),
    dict(
        slug="yuri-machado",
        nome="Yuri Machado",
        nome_completo="Yuri Machado",
        papel="Consultor de investimentos",
        frase="Investir representa planejamento, segurança, liberdade e a possibilidade de "
              "transformar a vida dos meus clientes.",
        proposito=[
            "Sempre acreditei que a forma como lidamos com o dinheiro pode transformar a nossa "
            "qualidade de vida e as possibilidades que construímos para o futuro.",
            "Acredito que uma boa relação profissional é construída com confiança, transparência e "
            "proximidade. Por isso busco sempre entender as necessidades de cada pessoa antes de "
            "pensar em qualquer estratégia.",
        ],
        marcos=[
            ("Antes", "Ambiente corporativo, com experiência em organização, análise, planejamento "
                      "e relacionamento com pessoas."),
            ("Há 3 anos", "Tiro a certificação necessária e entro no mercado como planejador "
                          "financeiro na W1."),
            ("Depois", "Aprovado em processos seletivos de grandes instituições, como Bradesco e "
                       "Itaú, e também da AUVP."),
            ("Hoje", "A escolha foi a AUVP Capital, onde atuo há quase dois anos."),
        ],
        interesses=["Musculação", "Disciplina e constância", "Viagens", "Família e amigos"],
        fora="A musculação me ensinou muito sobre disciplina, paciência e consistência — valores "
             "que também considero fundamentais na construção de patrimônio.",
        graduacao=["Administração de Empresas — Universidade Veiga de Almeida"],
        pos=[],
        certificacoes=["CEA — Especialista em Investimentos, ANBIMA"],
    ),
]
