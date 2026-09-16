# -*- coding: utf-8 -*-
"""Os consultores do plano Me Diz o Que Fazer.

Mora aqui, junto dos documentos prontos, e não em `gerador/`: o gerador produz
modelo, e não sabe o nome de ninguém. Quem sabe é esta pasta.

O texto é o que cada um escreveu, na íntegra e sem corte. A divisão em campos
não reescreve nada — só diz em que parte da página cada trecho entra:

    frase           uma frase do próprio texto, repetida em destaque ao lado do
                    retrato. Continua no corpo, no lugar de origem: é citação
                    de chamada, não substituição
    proposito       o texto de "Sobre mim e meu propósito", parágrafo a parágrafo
    formacao_paras  o texto de formação e qualificações, por extenso
    trajetoria      o texto de trajetória no mercado financeiro
    fora_paras      o texto de "fora do escritório"
    fora_lista      os itens que o último parágrafo anuncia, quando há
    graduacao       a leitura rápida da faixa de credenciais da abertura
    pos             idem, especializações. Vazio some da faixa
    certificacoes   idem, como etiquetas
    marcos          a trajetória em linha do tempo, ao lado do texto corrido.
                    Cada marco é um trecho do próprio texto, não um resumo dele
    interesses      os assuntos de "fora do escritório" como etiquetas
    whatsapp        o número de atendimento, já formatado; `None` quando não há
    email           o e-mail de contato

Parágrafo longo às vezes vira dois — quebra de parágrafo, sem tirar nem trocar
palavra. Onde o original tem lista, ela continua lista.

Para acrescentar um consultor, some uma entrada aqui e rode `gerar.py`.
"""

CONSULTORES = [
    dict(
        slug="alan-santanna",
        nome="Alan Sant'Anna",
        nome_completo="Alan Feitosa Sant'Anna",
        papel="Consultor de investimentos",
        whatsapp="+55 (62) 4014-0663",
        email="alan.sa@auvpconsultoria.com.br",
        frase="Minha missão é absorver toda a complexidade matemática e analítica do mercado e "
              "traduzi-la em estratégias simples, seguras e personalizadas para os seus objetivos.",
        proposito=[
            "Sou um verdadeiro apaixonado por educação financeira e pelo poder que os "
            "investimentos têm de transformar a vida das pessoas. Meu propósito no mercado vai "
            "muito além de apenas indicar ativos, meu objetivo é garantir que você compreenda o "
            "cenário econômico, tendo total clareza e segurança sobre as escolhas que fazemos "
            "juntos.",
            "Para entregar soluções consistentes, tenho uma abordagem educativa, consultiva "
            "aliada a um profundo rigor técnico. Minha missão é absorver toda a complexidade "
            "matemática e analítica do mercado e traduzi-la em estratégias simples, seguras e "
            "personalizadas para os seus objetivos.",
        ],
        formacao_paras=[
            "<strong>Graduação:</strong> Bacharelado em Ciências Econômicas pelo IBMEC.",
            "<strong>Pós-graduação / Especializações:</strong> Cursando especializações em "
            "Ciência de Dados (Google Data Analytics) e Análise de Dados (SQL e Power BI) "
            "aplicadas a negócios, além de formações avançadas em Finanças Comportamentais. "
            "Estudando para o CNPI, a fim de aumentar ainda mais a minha bagagem técnica no "
            "mercado financeiro.",
            "<strong>Certificações:</strong> CPA (Certificado Profissional Anbima), C-PRO R "
            "(Certificação Profissional Anbima de Relacionamento), C-Pro I (Certificação "
            "Profissional Anbima de Investimento) e FBB100 (Correspondente Bancário Completo "
            "FEBRABAN + LGPD).",
        ],
        trajetoria=[
            "Atuo como profissional no mercado financeiro desde 2022, construí minha carreira "
            "gerenciando e estruturando carteiras para clientes Pessoa Física (Alta Renda e "
            "Varejo) e Pessoa Jurídica.",
            "Meu diferencial é ter uma abordagem técnica, com alta capacidade analítica "
            "fundamentada em dados, com conhecimentos de modelagem financeira (Valuation, fluxo "
            "de caixa), leitura de demonstrações contábeis aliados à visão macroeconômica.",
        ],
        fora_paras=[
            "Sempre fui muito curioso e valorizo demais viver novas experiências e conhecer "
            "outras culturas, o que me fez viajar bastante, algo que me marcou foi meu "
            "intercâmbio em Cambridge. Mesmo sempre tendo sido apaixonado pelo mercado "
            "financeiro e investido por conta própria desde novo, antes de fazer disso a minha "
            "profissão, passei quase 10 anos empreendendo. Ter vivido isso na prática me deu uma "
            "verdadeira &ldquo;visão de dono&rdquo;, sei exatamente quais são as dores e os "
            "desafios de se tocar um negócio no Brasil.",
            "Também tenho um lado mais observador e criativo. Trabalhei como fotógrafo "
            "profissional por alguns anos, uma experiência que me ensinou a olhar com mais "
            "cuidado para os detalhes. No meu tempo livre, a música é a minha grande válvula de "
            "escape. Para equilibrar o profissional com a qualidade de vida, gosto de ir na "
            "academia e andar de bicicleta.",
        ],
        graduacao=["Ciências Econômicas — IBMEC"],
        pos=["Ciência de Dados (Google Data Analytics), em curso",
             "Análise de Dados com SQL e Power BI, em curso",
             "Finanças Comportamentais"],
        certificacoes=["CPA", "C-Pro I", "C-Pro R", "FBB100"],
        marcos=[
            ("Antes do mercado", "Passei quase 10 anos empreendendo, o que me deu uma verdadeira "
                                 "&ldquo;visão de dono&rdquo;."),
            ("Por alguns anos", "Trabalhei como fotógrafo profissional."),
            ("Desde 2022", "Atuo no mercado financeiro, estruturando carteiras para pessoa "
                           "física e pessoa jurídica."),
            ("Hoje", "Consultor de investimentos na AUVP Capital."),
        ],
        interesses=["Viagens", "Intercâmbio em Cambridge", "Empreendedorismo", "Fotografia",
                    "Música", "Academia", "Ciclismo"],
    ),
    dict(
        slug="andre-arruda",
        nome="André Arruda",
        nome_completo="André Arruda",
        papel="Consultor de investimentos",
        whatsapp="+55 (62) 4014-0690",
        email="andre.arruda@auvpconsultoria.com.br",
        frase="O trabalho de um consultor deve ir além de recomendar investimentos, deve também "
              "alinhar as expectativas, entender cada perfil de investidor e finalmente informar "
              "e até mesmo educar.",
        proposito=[
            "Prazer, sou o André Arruda e atuo hoje como consultor de investimentos aqui na AUVP "
            "Capital, mas nem sempre foi assim. Minha vida profissional começou na gráfica de meu "
            "avô, num tempo em que computadores e celulares ainda não eram tão desenvolvidos como "
            "hoje e a principal prateleira de informações eram as bibliotecas e livrarias. Minha "
            "função? Diagramador. Acredito que foi a partir daí que comecei a gostar de aprender "
            "e me informar, paixão que resultou na minha formação como jornalista e "
            "consequentemente me trouxe até aqui.",
            "Da mesma maneira que como jornalista meu propósito é informar de maneira confiável e "
            "imparcial, atualmente como consultor também compartilho desse mesmo propósito. "
            "Afinal, o trabalho de um consultor deve ir além de recomendar investimentos, deve "
            "também alinhar as expectativas, entender cada perfil de investidor e finalmente "
            "informar e até mesmo educar, sobre cada passo que será tomado nos investimentos e "
            "principalmente, fazer tudo isso de maneira honesta.",
        ],
        formacao_paras=[
            "<strong>Graduação:</strong> Jornalismo.",
            "<strong>Pós-graduação:</strong> Investimentos Finanças e Banking.",
            "<strong>Certificações:</strong> CPA, C-Pro I e C-Pro R.",
        ],
        trajetoria=[
            "Foi durante a pandemia que decidi que iria deixar o mercado da comunicação, que foi "
            "muito afetado na época e que iria investir meu tempo para aprender mais sobre "
            "economia e principalmente investimentos.",
            "Em 2022 formalizei essa mudança com minha primeira certificação no mercado, a antiga "
            "CEA. E dei inicio a minha jornada como Consultor Independente, foram quase quatro "
            "anos atuando dessa forma, até me encontrar onde estou hoje, aqui na AUVP.",
        ],
        fora_paras=[
            "Para além do âmbito profissional, sou uma pessoa que gosta de estar com quem amo, "
            "seja família e amigos. Meu lugar preferido no mundo é a Praia de Itamambuca em "
            "Ubatuba, lugar onde estive desde que consigo me lembrar e pode parecer "
            "&ldquo;clubismo&rdquo;, mas é a praia mais bonita que conheço também. Meu esporte "
            "favorito é o surf e acho que cresci no lugar certo, afinal Ubatuba é popularmente "
            "conhecida como a capital do surf do Brasil.",
            "Também amo viajar e conhecer novas paisagens, culturas e pessoas. E se não estou "
            "saindo com meus amigos, família, nem na praia ou conhecendo novos lugares, é bem "
            "provável que esteja ouvindo música ou assistindo um filme, então vou finalizar essa "
            "apresentação deixando uma sugestão de música e de filme, respectivamente:",
        ],
        fora_lista=["<em>Time</em> — Pink Floyd", "<em>Cinema Paradiso</em>"],
        graduacao=["Jornalismo"],
        pos=["Investimentos Finanças e Banking"],
        certificacoes=["CPA", "C-Pro I", "C-Pro R"],
        marcos=[
            ("No começo", "Diagramador."),
            ("Pandemia", "Decidi deixar o mercado da comunicação para aprender sobre economia e "
                         "investimentos."),
            ("2022", "Primeira certificação no mercado, a antiga CEA, e o início como consultor "
                     "independente."),
            ("Hoje", "Consultor de investimentos na AUVP Capital."),
        ],
        interesses=["Família e amigos", "Praia de Itamambuca", "Surf", "Viagens", "Música",
                    "Cinema"],
    ),
    dict(
        slug="bolivar-oliveira",
        nome="Bolívar Oliveira",
        nome_completo="Bolívar Luiz Pereira d'Oliveira",
        papel="Consultor de investimentos",
        whatsapp=None,
        email="bolivar.oliveira@investidorsardinha.com.br",
        frase="Educação financeira não se resume a ensinar alguém a investir, mas a oferecer "
              "conhecimento para que cada pessoa possa tomar decisões melhores e construir um "
              "futuro mais próspero para si e para sua família.",
        proposito=[
            "Olá! Sou Bolívar, consultor de investimentos da AUVP apaixonado pelo mercado "
            "financeiro, pela educação e pelo impacto que o conhecimento pode gerar na vida das "
            "pessoas. Minha trajetória no mercado financeiro começou em 2023, inicialmente como "
            "investidor e estudante e evoluiu para uma atuação profissional cada vez mais próxima "
            "dos investidores e de suas necessidades.",
            "Desenvolvi experiência prática com educação financeira, análise e compreensão de "
            "diferentes produtos e estratégias de investimento, relacionamento com investidores e "
            "tradução de conceitos complexos em decisões mais claras e conscientes. Essa "
            "vivência, somada à minha experiência trabalhando na AUVP e às certificações "
            "ANBIMA, "
            "consolidou minha paixão pelo mercado e meu propósito de atuar diretamente na "
            "construção e orientação patrimonial dos investidores.",
            "Acredito que educação financeira não se resume a ensinar alguém a investir, mas a "
            "oferecer conhecimento para que cada pessoa possa tomar decisões melhores e construir "
            "um futuro mais próspero para si e para sua família.",
        ],
        formacao_paras=[
            "Tive experiências acadêmicas em Marketing e Direito e fui aluno da AUVP Escola. "
            "Também possuo o Certificado Profissional ANBIMA e o Certificado Profissional ANBIMA "
            "de Relacionamento, além de inglês fluente.",
            "Busco manter uma rotina constante de aprendizado e atualização, especialmente em um "
            "mercado tão dinâmico.",
        ],
        trajetoria=[
            "Antes de atuar no mercado financeiro, trabalhei por mais de dois anos como instrutor "
            "de inglês em diferentes escolas e anteriormente por cerca de um ano e meio com "
            "atendimento ao público. Essas experiências desenvolveram minha comunicação, didática "
            "e capacidade de criar relacionamentos com pessoas de diferentes perfis.",
            "Como Consultor de Investimentos na AUVP Capital, coloco essa experiência a serviço "
            "dos investidores, ajudando cada cliente a compreender melhor suas decisões e "
            "construir uma estratégia patrimonial alinhada aos seus objetivos.",
        ],
        fora_paras=[
            "Fora do trabalho, tenho interesses bastante variados. Valorizo profundamente minha "
            "família, meus amigos e os princípios que construí ao longo da vida.",
            "Procuro viver com curiosidade, aprendizado constante e propósito, buscando construir "
            "uma vida pessoal e profissional que me traga realização, significado e a "
            "oportunidade de gerar valor para as pessoas ao meu redor.",
        ],
        graduacao=["Experiências acadêmicas em Marketing e Direito"],
        pos=["Investimentos Avançados &amp; Análise de Ativos"],
        certificacoes=["CPA", "C-Pro I", "C-Pro R"],
        marcos=[
            ("Antes do mercado", "Cerca de um ano e meio com atendimento ao público."),
            ("Por mais de dois anos", "Instrutor de inglês em diferentes escolas."),
            ("2023", "Início da trajetória no mercado financeiro."),
            ("Hoje", "Consultor de investimentos na AUVP Capital."),
        ],
        interesses=["Família", "Amigos", "Curiosidade", "Aprendizado constante",
                    "Inglês fluente", "AUVP Escola"],
    ),
    dict(
        slug="danilo-barbosa",
        nome="Danilo Barbosa",
        nome_completo="Danilo Miranda Barbosa",
        papel="Consultor de investimentos",
        whatsapp="+55 (62) 3095-8115",
        email="danilo.barbosa@auvpconsultoria.com.br",
        frase="O meu grande objetivo é ajudar você a tirar o foco exclusivo das necessidades "
              "imediatas do seu &lsquo;eu do presente&rsquo; para construirmos, juntos, um "
              "planejamento estratégico de longo prazo voltado para o seu &lsquo;eu do "
              "futuro&rsquo;.",
        proposito=[
            "Olá! Eu sou Danilo Barbosa, seu consultor de investimentos aqui na AUVP.",
            "Nesta jornada, vamos construir juntos o seu futuro financeiro, tijolo a tijolo, "
            "focando sempre no que o seu &lsquo;eu do futuro&rsquo; espera das decisões e "
            "atitudes tomadas hoje. Vamos traçar esse caminho com muita responsabilidade, "
            "planejamento e estratégia, visando seus objetivos e à constância no longo prazo. É "
            "dessa forma que você conseguirá alcançar o que almeja com tranquilidade e sem correr "
            "riscos desnecessários.",
            "Por fim, vejo que investir é uma ferramenta fundamental não só para potencializar "
            "seus resultados, mas também para proteger você financeiramente dos reveses que "
            "ocorrem na vida. Portanto, saiba que comigo você terá um olhar maduro e totalmente "
            "livre de conflito de interesses sobre o seu patrimônio. O meu grande objetivo é "
            "ajudar você a tirar o foco exclusivo das necessidades imediatas do seu &lsquo;eu do "
            "presente&rsquo; para construirmos, juntos, um planejamento estratégico de longo "
            "prazo voltado para o seu &lsquo;eu do futuro&rsquo;.",
            "Conte comigo sempre!",
        ],
        formacao_paras=[
            "<strong>Graduação:</strong> Administração de Empresas e Gestão Financeira.",
            "<strong>Pós-graduação:</strong> Análise de Dados.",
            "<strong>Certificações:</strong> CPA, C-Pro I e C-Pro R.",
        ],
        trajetoria=[
            "Iniciei no mundo dos investimentos em 2016 e, desde então, sempre me dediquei não "
            "apenas aos aportes e estudos sobre o tema, mas também a compartilhar essa "
            "experiência com muitas pessoas, o que depois se tornou o meu trabalho.",
            "Com o tempo, pude acompanhar a trajetória de diversos desses investidores que "
            "realizaram seus sonhos: a compra da casa própria, a festa de casamento, a aquisição "
            "do primeiro carro ou, até mesmo, o simples alívio de ter clareza sobre o rumo das "
            "próprias finanças. Tenha certeza de que essas realizações são tão importantes para "
            "mim, como consultor, quanto são para você!",
        ],
        fora_paras=[
            "Fora dos investimentos, sou apaixonado por música, leitura e viagens. Minha banda "
            "favorita é o &ldquo;Queen&rdquo; — inclusive, tenho a guitarra signature do "
            "guitarrista da banda, Brian May. Entretanto, meu gosto musical não se restringe "
            "apenas ao rock, mas também gosto do pop, MPB, um pouco de sertanejo "
            "&ldquo;raiz&rdquo;, blues, soul, música clássica e outros. Sei tocar violão, "
            "guitarra e baixo, sendo este o meu primeiro instrumento musical.",
            "Por parte dos livros, além do tema de investimentos, gosto de psicologia — Dan "
            "Ariely e Jordan Peterson são alguns dos meus autores favoritos — filosofia, "
            "história, biografias e outros diferentes que me despertam atenção.",
            "Sobre viagens, já visitei 5 países na Europa e também os EUA — Espanha e Inglaterra "
            "foram os meus favoritos. Embora viagem internacional seja uma &ldquo;moda "
            "instagramável&rdquo;, o que eu mais gosto é de conversar com pessoas de diferentes "
            "nacionalidades. Sei falar inglês e estou aprendendo francês atualmente.",
            "Por fim, gosto muito de ficar com a família e sair com os amigos sempre que posso, "
            "pois ninguém é de ferro! Falando tudo isso, até parece que sou um &ldquo;nerd&rdquo; "
            "antissocial, mas sou uma pessoa normal como qualquer outra. Acho que isso descreve "
            "bem o que eu gosto além dos investimentos, embora eu quase tenha me esquecido de "
            "dizer que o feijão deve ser colocado por cima do arroz.",
        ],
        graduacao=["Administração de Empresas", "Gestão Financeira"],
        pos=["Análise de Dados"],
        certificacoes=["CPA", "C-Pro I", "C-Pro R"],
        marcos=[
            ("2016", "Início no mundo dos investimentos."),
            ("Desde então", "Aportes, estudo e o hábito de compartilhar a experiência com muitas "
                            "pessoas."),
            ("Depois", "O que era hábito se tornou o meu trabalho."),
            ("Hoje", "Consultor de investimentos na AUVP Capital."),
        ],
        interesses=["Música", "Violão, guitarra e baixo", "Queen", "Leitura",
                    "Psicologia e filosofia", "Viagens", "Inglês e francês", "Família e amigos"],
    ),
    dict(
        slug="erika-barreto",
        nome="Erika Barreto",
        nome_completo="Erika Kettelyn Leite Barreto",
        papel="Consultora de investimentos",
        whatsapp="+55 (62) 3030-4145",
        email="erika.barreto@auvpconsultoria.com.br",
        frase="No dia a dia, busco ser didática para desmistificar o mercado financeiro. Gosto de "
              "conversar de forma clara e de fácil entendimento.",
        proposito=[
            "Prazer, me chamo Erika Barreto! Atuo como consultora de investimentos aqui na AUVP "
            "há mais de um ano. Sou movida pela vontade de aprender e, com o mercado financeiro, "
            "entendi que também gosto de ensinar.",
            "No dia a dia, busco ser didática para desmistificar o mercado financeiro. Gosto de "
            "conversar de forma clara e de fácil entendimento. Acredito que as decisões "
            "financeiras sobre o próprio patrimônio devem ser tomadas com clareza, por isso gosto "
            "muito de responder às perguntas que as pessoas têm depois de estudar.",
        ],
        formacao_paras=[
            "<strong>Graduação:</strong> Gestão financeira.",
            "<strong>Certificações:</strong> CPA, C-PRO R e C-PRO I.",
        ],
        trajetoria=[
            "Conheci o mercado financeiro por volta de 2019, quando passei a economizar focada em "
            "fazer um intercâmbio. Depois disso, com o dinheiro acumulado durante a pandemia, "
            "decidi que precisava fazer aquele valor render.",
            "Foi onde comecei a estudar e acompanhar de perto o trabalho do Investidor Sardinha. "
            "Isso me despertou um grande interesse pela área, o que me motivou a estudar e me "
            "especializar.",
        ],
        fora_paras=[
            "Fora do escritório, gosto de viajar para conhecer culturas diferentes, leio muito e "
            "sou viciada em quebra-cabeças. Para desacelerar da cidade grande, passo diversos "
            "finais de semana no interior com o meu avô, além de gostar muito de ir à praia.",
        ],
        graduacao=["Gestão financeira"],
        pos=[],
        certificacoes=["CPA", "C-Pro R", "C-Pro I"],
        marcos=[
            ("2019", "Conheci o mercado financeiro economizando para fazer um intercâmbio."),
            ("Pandemia", "Decidi que precisava fazer render o dinheiro acumulado."),
            ("Depois", "Comecei a estudar e a acompanhar de perto o trabalho do Investidor "
                       "Sardinha."),
            ("Hoje", "Consultora de investimentos na AUVP Capital."),
        ],
        interesses=["Viagens", "Culturas diferentes", "Leitura", "Quebra-cabeças",
                    "Fins de semana no interior", "Praia"],
    ),
    dict(
        slug="nasser-tanure",
        nome="Nasser Tanure",
        nome_completo="Nasser Tanure Amantes",
        papel="Consultor de investimentos",
        whatsapp="+55 (62) 3095-8142",
        email="nasser.tanure@auvpconsultoria.com.br",
        frase="Para mim, investir vai muito além de planilhas e rentabilidade; trata-se de "
              "educação e planejamento de vida.",
        proposito=[
            "Olá! Sou Nasser, consultor de investimentos e um profissional dedicado a entender as "
            "necessidades financeiras e os objetivos de cada investidor. O que realmente me move "
            "no mercado financeiro é a paixão por utilizar os investimentos como uma ponte para "
            "ajudar as pessoas a realizarem seus sonhos. Para mim, investir vai muito além de "
            "planilhas e rentabilidade; trata-se de educação e planejamento de vida.",
            "Essa veia educacional é algo que carrego com muito orgulho e que me inspira "
            "profundamente, herança da minha mãe, que dedicou a vida inteira à profissão de "
            "professora. Acredito que, ao educar financeiramente, consigo empoderar as pessoas "
            "para que tomem as melhores decisões para o futuro de suas famílias. Sou também uma "
            "pessoa bastante comunicativa e de fácil relacionamento, características que "
            "aprimorei muito durante o ano em que morei na Irlanda e na minha experiência morando "
            "em república estudantil na faculdade, o que me ensinou a conectar de forma genuína "
            "com pessoas de diferentes perfis e culturas.",
        ],
        formacao_paras=[
            "<strong>Graduação:</strong> Engenharia de Produção pela Universidade Federal de Ouro "
            "Preto (UFOP).",
            "<strong>Pós-graduação:</strong> MBA em Gestão de Investimentos e, atualmente, "
            "cursando um MBA em Gestão de Negócios.",
            "<strong>Certificações:</strong> CPA, C Pro-R e C Pro-I.",
        ],
        trajetoria=[
            "Minha vivência no mercado financeiro é ampla e robusta. Construí minha base "
            "trabalhando em outros segmentos financeiros e corporativos fora da esfera "
            "tradicional de investimentos, como em processos de turnaround de empresas, o que me "
            "proporcionou uma visão sistêmica sobre alocação de recursos, fluxo de caixa e "
            "economia.",
        ],
        fora_paras=[
            "Acredito que a disciplina necessária para construir um bom patrimônio é a mesma que "
            "aplico no meu estilo de vida. Fora do escritório, mantenho uma rotina ativa "
            "dedicando meu tempo à prática de musculação e à corrida. Além disso, sou um grande "
            "fã de leitura, com foco especial em obras de desenvolvimento pessoal, e gosto de "
            "relaxar assistindo a bons (ou não, rsrs) jogos de futebol. Esses interesses me "
            "ajudam a manter o foco, o equilíbrio e sempre rendem ótimas conversas!",
        ],
        graduacao=["Engenharia de Produção — UFOP"],
        pos=["MBA em Gestão de Investimentos", "MBA em Gestão de Negócios, em curso"],
        certificacoes=["CPA", "C-Pro I", "C-Pro R"],
        marcos=[
            ("Formação", "Engenharia de Produção pela Universidade Federal de Ouro Preto."),
            ("Antes dos investimentos", "Outros segmentos financeiros e corporativos, como "
                                        "processos de turnaround de empresas."),
            ("Um ano na Irlanda", "Onde aprimorei a comunicação e o relacionamento com pessoas de "
                                  "diferentes perfis e culturas."),
            ("Hoje", "Consultor de investimentos na AUVP Capital."),
        ],
        interesses=["Musculação", "Corrida", "Leitura", "Desenvolvimento pessoal", "Futebol",
                    "Um ano na Irlanda"],
    ),
    dict(
        slug="yuri-machado",
        nome="Yuri Machado",
        nome_completo="Yuri Medeiros Candol Machado",
        papel="Consultor de investimentos",
        whatsapp="+55 (62) 4014-0683",
        email="yuri.medeiros@auvpconsultoria.com.br",
        frase="Acredito que uma boa relação profissional é construída com confiança, "
              "transparência e proximidade. Por isso, busco sempre entender as necessidades de "
              "cada pessoa antes de pensar em qualquer estratégia ou solução.",
        proposito=[
            "Sou Yuri Machado, formado em Administração de Empresas e apaixonado pelo mercado "
            "financeiro e pelo universo dos investimentos.",
            "Sempre acreditei que a forma como lidamos com o dinheiro pode transformar "
            "diretamente a nossa qualidade de vida e as possibilidades que construímos para o "
            "futuro. Foi essa visão que despertou em mim o interesse pelo mercado financeiro e me "
            "motivou a buscar cada vez mais conhecimento e especialização na área de "
            "investimentos.",
            "Para mim, investir vai muito além de números, gráficos e rentabilidade. Investir "
            "representa planejamento, segurança, liberdade e a possibilidade de transformar a "
            "vida dos meus clientes. Como consultor de investimentos, meu propósito é ajudar "
            "pessoas a compreenderem melhor suas escolhas financeiras e a construírem estratégias "
            "que façam sentido para seus objetivos e para o momento de vida de cada uma.",
            "Acredito que uma boa relação profissional é construída com confiança, transparência "
            "e proximidade. Por isso, busco sempre entender as necessidades de cada pessoa antes "
            "de pensar em qualquer estratégia ou solução.",
        ],
        formacao_paras=[
            "<strong>Graduação:</strong> Administração de Empresas pela Universidade Veiga de "
            "Almeida.",
            "<strong>Certificação:</strong> CEA — Especialista em Investimentos, certificação da "
            "ANBIMA.",
        ],
        trajetoria=[
            "Minha trajetória profissional foi construída no ambiente corporativo, onde "
            "desenvolvi experiências importantes relacionadas à organização, análise, "
            "planejamento e relacionamento com pessoas.",
            "Ao longo desse caminho, meu interesse pelo mercado financeiro se tornou cada vez "
            "maior. Comecei a estudar investimentos e a entender, na prática, como o conhecimento "
            "financeiro pode fazer diferença na vida das pessoas. Foi então que decidi direcionar "
            "minha carreira para a área de investimentos.",
            "Há três anos, tirei a certificação necessária e fui para o mercado de trabalho. "
            "Comecei atuando como planejador financeiro. Mais tarde, passei no processo "
            "seletivo para vagas em grandes instituições, uma delas a AUVP. A minha "
            "escolha foi, sem dúvidas, a AUVP Capital, onde já atuo há dois anos. Essa "
            "escolha representa não apenas um objetivo profissional, mas também algo que está "
            "diretamente ligado aos meus interesses e à forma como enxergo o futuro: ajudar "
            "pessoas a tomarem decisões e a construírem seus próprios caminhos financeiros em "
            "busca da liberdade.",
        ],
        fora_paras=[
            "Acredito que disciplina e constância são fundamentais para alcançar bons resultados, "
            "tanto na vida profissional quanto na pessoal.",
            "Gosto de manter uma rotina equilibrada e tenho na prática de atividades físicas uma "
            "parte importante do meu dia a dia. A musculação me ensinou muito sobre disciplina, "
            "paciência e consistência, valores que também considero fundamentais quando falamos "
            "sobre investimentos e construção de patrimônio.",
            "Também gosto de viajar, conhecer novos lugares e viver experiências diferentes. "
            "Acredito que conhecer novas culturas e sair da rotina ajuda a ampliar nossa visão de "
            "mundo.",
            "Além disso, valorizo muito os momentos com amigos e família. Para mim, construir "
            "patrimônio e conquistar objetivos financeiros significa ter liberdade para aproveitar "
            "melhor a vida e as pessoas que fazem parte dela.",
            "Porque, no fim, investir não é apenas sobre dinheiro. É sobre construir "
            "possibilidades para viver a vida que você deseja.",
        ],
        graduacao=["Administração de Empresas — Universidade Veiga de Almeida"],
        pos=[],
        certificacoes=["CPA", "C-Pro I", "C-Pro R"],
        marcos=[
            ("Antes", "Trajetória no ambiente corporativo, em organização, análise, planejamento "
                      "e relacionamento com pessoas."),
            ("Há três anos", "Certificação e entrada no mercado, como planejador financeiro."),
            ("Depois", "Aprovado em grandes instituições — e a escolha foi a AUVP Capital."),
            ("Hoje", "Consultor de investimentos na AUVP Capital, há quase dois anos."),
        ],
        interesses=["Disciplina e constância", "Musculação", "Rotina equilibrada", "Viagens",
                    "Novas culturas", "Amigos e família"],
    ),
]
