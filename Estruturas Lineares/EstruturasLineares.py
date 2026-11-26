# ==============================================================================
# 1. CLASSE BASE (ESTRUTURA LINEAR)
# Define o "molde" e as regras comuns para todas as listas e filas.
# ==============================================================================
class EstruturaLinear:
    def __init__(self, iteravel=None, capacidade=None):
        self.tamanho = 0              # Contador de quantos nós existem na estrutura
        self.capacidade = capacidade  # Limite máximo de itens (None = sem limite)
        
        # Variáveis de memória usadas apenas pelo método consultaProximo(chave)
        # para lembrar onde a última busca parou quando há chaves repetidas:
        self._ultimo_no = None
        self._ultima_chave = None

        # Se o usuário passar uma lista/tupla na criação (ex: Lista([10, 20])),
        # percorre esse iterável e insere cada item no fim da estrutura.
        if iteravel:
            for item in iteravel:
                self.insereNoFim(item)

    def _chave(self, dado):
        """
        Extrai a chave de busca do 'dado'.
        Se o dado for um objeto complexo com atributo .chave (ex: Pedido, PalavraIndice),
        retorna dado.chave. Se for um tipo simples (ex: int 10, str 'Ana'), retorna o próprio dado.
        """
        return dado.chave if hasattr(dado, 'chave') else dado

    def __len__(self):
        """Permite usar len(estrutura) nativamente no Python."""
        return self.tamanho

    def estaVazia(self):
        """Retorna True se não houver nenhum nó (Underflow se tentar remover)."""
        return self.tamanho == 0

    def estaCheia(self):
        """Retorna True se atingiu a capacidade máxima definida (Overflow se tentar inserir)."""
        return self.capacidade is not None and self.tamanho >= self.capacidade

    def _checkOverflow(self):
        """Trava de segurança chamada antes de qualquer inserção."""
        if self.estaCheia():
            raise OverflowError("Estrutura cheia (Overflow).")

    def _checkUnderflow(self):
        """Trava de segurança chamada antes de qualquer remoção ou consulta."""
        if self.estaVazia():
            raise IndexError("Estrutura vazia (Underflow).")

    def __getitem__(self, pos):
        """Permite ler elementos usando colchetes, ex: x = lista[1]."""
        return self.consultaPosicao(pos)

    def __setitem__(self, pos, valor):
        """Permite alterar elementos usando colchetes, ex: lista[1] = 99."""
        self.atualizaPosicao(pos, valor)

    def ordena(self):
        """
        Ordena os elementos em ordem crescente usando Bubble Sort (bolha).
        Compara pares vizinhos (j e j+1) e chama swap(j) se estiverem fora de ordem.
        """
        for i in range(self.tamanho):
            trocou = False
            for j in range(1, self.tamanho - i):
                if self._chave(self[j]) > self._chave(self[j + 1]):
                    self.swap(j)
                    trocou = True
            if not trocou:  # Se passou pela lista sem fazer trocas, já está ordenada
                break


# ==============================================================================
# 2. LISTA ENCADEADA SIMPLES
# Cada nó conhece apenas o PRÓXIMO nó (sentido único: inicio -> ... -> fim).
# ==============================================================================
class NoSimples:
    def __init__(self, dado):
        self.dado = dado  # Informação armazenada dentro do nó
        self.prox = None  # Referência (ponteiro) para o próximo NoSimples (ou None)


class ListaEncadeadaSimples(EstruturaLinear):
    def __init__(self, iteravel=None, capacidade=None):
        self.inicio = None  # Aponta para o 1º nó da lista
        self.fim = None     # Aponta para o último nó da lista
        super().__init__(iteravel, capacidade)

    def _obterNo(self, pos):
        """
        Método interno que caminha de nó em nó a partir do início até chegar
        na 'pos' desejada (indexação começa em 1). Retorna o objeto NoSimples.
        """
        if pos < 1 or pos > self.tamanho:
            raise IndexError("Posição fora dos limites (out of bound).")
        aux = self.inicio
        for _ in range(1, pos):
            aux = aux.prox
        return aux

    # --- INSERÇÕES ---
    def insereNoInicio(self, dado):
        """Cria um nó e o coloca na frente do atual self.inicio (custo O(1))."""
        self._checkOverflow()
        novo = NoSimples(dado)
        if not self.inicio:               # Caso 1: lista estava vazia
            self.inicio = self.fim = novo
        else:                             # Caso 2: lista já tem elementos
            novo.prox = self.inicio       # O novo nó aponta para o antigo primeiro
            self.inicio = novo            # O início da lista passa a ser o novo nó
        self.tamanho += 1

    def insereNoFim(self, dado):
        """Cria um nó e o engata logo após o atual self.fim (custo O(1))."""
        self._checkOverflow()
        novo = NoSimples(dado)
        if not self.inicio:               # Caso 1: lista estava vazia
            self.inicio = self.fim = novo
        else:                             # Caso 2: engata no último nó e atualiza self.fim
            self.fim.prox = novo
            self.fim = novo
        self.tamanho += 1

    def insereNaPosicao(self, dado, pos):
        """Insere um novo nó exatamente na posição 'pos', empurrando os seguintes."""
        self._checkOverflow()
        if pos < 1 or pos > self.tamanho + 1:
            raise IndexError("Posição fora dos limites.")
        if pos == 1:
            return self.insereNoInicio(dado)
        if pos == self.tamanho + 1:
            return self.insereNoFim(dado)

        # Para inserir no meio, precisamos parar um nó ANTES (pos - 1)
        ant = self._obterNo(pos - 1)
        novo = NoSimples(dado)
        novo.prox = ant.prox  # O novo nó aponta para quem estava na posição
        ant.prox = novo       # O nó anterior passa a apontar para o novo nó
        self.tamanho += 1

    def insereDepoisDaChave(self, chave, dado):
        """Procura o nó com a 'chave' e insere o novo 'dado' logo depois dele."""
        self._checkOverflow()
        aux = self.inicio
        while aux:
            if self._chave(aux.dado) == chave:
                if aux == self.fim:
                    return self.insereNoFim(dado)
                novo = NoSimples(dado)
                novo.prox = aux.prox
                aux.prox = novo
                self.tamanho += 1
                return
            aux = aux.prox
        raise KeyError("Chave não encontrada.")

    # --- ATUALIZAÇÕES ---
    def atualiza(self, chave, dadoNovo):
        """Localiza o primeiro nó com a 'chave' e substitui seu conteúdo (dado)."""
        aux = self.inicio
        while aux:
            if self._chave(aux.dado) == chave:
                aux.dado = dadoNovo
                return
            aux = aux.prox
        raise KeyError("Chave não encontrada.")

    def atualizaPosicao(self, pos, dadoNovo):
        """Vai direto ao nó da posição 'pos' e troca o dado guardado nele."""
        self._obterNo(pos).dado = dadoNovo

    # --- REMOÇÕES ---
    def deletaDoInicio(self):
        """Remove o primeiro nó, avança self.inicio e devolve o dado removido (O(1))."""
        self._checkUnderflow()
        removido = self.inicio
        dado = removido.dado
        self.inicio = self.inicio.prox  # O 2º nó vira o 1º
        if not self.inicio:             # Se a lista ficou vazia, zera o fim também
            self.fim = None
        del removido                    # Apaga a referência do nó para liberar memória
        self.tamanho -= 1
        return dado

    def deletaDoFim(self):
        """
        Remove o último nó (O(n)). Na lista simples precisamos caminhar até o
        penúltimo nó porque o último nó não tem ponteiro para trás.
        """
        self._checkUnderflow()
        if self.tamanho == 1:
            return self.deletaDoInicio()
        penultimo = self._obterNo(self.tamanho - 1)
        removido = self.fim
        dado = removido.dado
        penultimo.prox = None   # Corta a ligação com o antigo último nó
        self.fim = penultimo    # O penúltimo passa a ser o novo fim
        del removido
        self.tamanho -= 1
        return dado

    def deletaPosicao(self, pos):
        """Remove o nó da posição 'pos' ligando o anterior diretamente ao próximo."""
        self._checkUnderflow()
        if pos == 1:
            return self.deletaDoInicio()
        if pos == self.tamanho:
            return self.deletaDoFim()
        ant = self._obterNo(pos - 1)
        removido = ant.prox
        dado = removido.dado
        ant.prox = removido.prox  # "Pula" o nó removido
        del removido
        self.tamanho -= 1
        return dado

    def deleta(self, chave):
        """Busca um nó pela 'chave', remove-o da cadeia e retorna seu dado."""
        self._checkUnderflow()
        if self._chave(self.inicio.dado) == chave:
            return self.deletaDoInicio()
        aux = self.inicio
        while aux.prox:
            if self._chave(aux.prox.dado) == chave:
                removido = aux.prox
                dado = removido.dado
                if removido == self.fim:
                    self.fim = aux
                aux.prox = removido.prox
                del removido
                self.tamanho -= 1
                return dado
            aux = aux.prox
        raise KeyError("Chave não encontrada.")

    # --- CONSULTAS E PERCURSO ---
    def consultaInicio(self):
        """Apenas espia o dado do 1º nó sem removê-lo."""
        self._checkUnderflow()
        return self.inicio.dado

    def consultaFim(self):
        """Apenas espia o dado do último nó sem removê-lo."""
        self._checkUnderflow()
        return self.fim.dado

    def consultaPosicao(self, pos):
        """Retorna o dado armazenado no nó da posição 'pos'."""
        return self._obterNo(pos).dado

    def consulta(self, chave):
        """
        Busca a primeira ocorrência da 'chave' e salva o nó encontrado em
        self._ultimo_no caso o usuário queira buscar repetições depois.
        """
        aux = self.inicio
        while aux:
            if self._chave(aux.dado) == chave:
                self._ultimo_no = aux
                self._ultima_chave = chave
                return aux.dado
            aux = aux.prox
        return None

    def consultaProximo(self, chave):
        """Continua a busca a partir do nó seguinte ao último encontrado."""
        if self._ultima_chave != chave or not self._ultimo_no:
            return self.consulta(chave)
        aux = self._ultimo_no.prox
        while aux:
            if self._chave(aux.dado) == chave:
                self._ultimo_no = aux
                return aux.dado
            aux = aux.prox
        return None

    def __iter__(self):
        """Torna a lista iterável em laços 'for item in lista:'."""
        aux = self.inicio
        while aux:
            yield aux.dado  # Entrega o dado atual e pausa até a próxima volta do loop
            aux = aux.prox

    def swap(self, pos):
        """Troca os dados entre os nós 'pos' e 'pos + 1' sem precisar religar ponteiros."""
        no1 = self._obterNo(pos)
        no2 = self._obterNo(pos + 1)
        no1.dado, no2.dado = no2.dado, no1.dado

    # --- OPERAÇÕES ESPECÍFICAS DA LISTA SIMPLES ---
    def concatenar(self, outra):
        """Engata o fim desta lista ao início de 'outra' em O(1) e esvazia 'outra'."""
        if outra.estaVazia():
            return
        if self.estaVazia():
            self.inicio, self.fim = outra.inicio, outra.fim
        else:
            self.fim.prox = outra.inicio
            self.fim = outra.fim
        self.tamanho += outra.tamanho
        outra.inicio = outra.fim = None
        outra.tamanho = 0

    def separar(self, pos):
        """Corta a lista na posição 'pos', devolvendo uma nova lista com a 2ª metade."""
        if pos <= 1 or pos > self.tamanho:
            raise IndexError("Posição de corte inválida.")
        nova = ListaEncadeadaSimples()
        corte = self._obterNo(pos - 1)       # Nó imediatamente anterior ao corte
        nova.inicio, nova.fim = corte.prox, self.fim
        nova.tamanho = self.tamanho - (pos - 1)
        corte.prox = None                    # Encerra a primeira lista no ponto de corte
        self.fim = corte
        self.tamanho = pos - 1
        return nova

    def inserirListaEntre(self, pos, outra):
        """Encaixa todos os nós de 'outra' logo após o nó da posição 'pos'."""
        if outra.estaVazia():
            return
        alvo = self._obterNo(pos)
        outra.fim.prox = alvo.prox  # O fim da lista inserida aponta para o resto da original
        alvo.prox = outra.inicio    # O nó alvo aponta para o início da lista inserida
        if alvo == self.fim:
            self.fim = outra.fim
        self.tamanho += outra.tamanho
        outra.inicio = outra.fim = None
        outra.tamanho = 0


# ==============================================================================
# 3. LISTA ENCADEADA DUPLA (E CIRCULAR)
# Cada nó conhece o PRÓXIMO (prox) e o ANTERIOR (ant).
# Se circular=True, o último nó aponta de volta para o primeiro (formando um anel).
# ==============================================================================
class NoDuplo:
    def __init__(self, dado):
        self.dado = dado  # Conteúdo guardado no nó
        self.prox = None  # Ponteiro para o nó seguinte
        self.ant = None   # Ponteiro para o nó anterior


class ListaEncadeadaDupla(EstruturaLinear):
    def __init__(self, iteravel=None, capacidade=None, circular=False):
        self.inicio = None
        self.fim = None
        self.circular = circular  # Define se as pontas se conectam
        super().__init__(iteravel, capacidade)

    def _fecharCiclo(self):
        """Se a lista for circular, garante que fim.prox == inicio e inicio.ant == fim."""
        if self.circular and self.tamanho > 0:
            self.fim.prox = self.inicio
            self.inicio.ant = self.fim

    def _obterNo(self, pos):
        """Localiza o nó na posição 'pos' (base 1)."""
        if pos < 1 or pos > self.tamanho:
            raise IndexError("Posição fora dos limites.")
        aux = self.inicio
        for _ in range(1, pos):
            aux = aux.prox
        return aux

    def insereNoInicio(self, dado):
        """Insere na frente ajustando 'prox' do novo e 'ant' do antigo início."""
        self._checkOverflow()
        novo = NoDuplo(dado)
        if not self.inicio:
            self.inicio = self.fim = novo
        else:
            novo.prox = self.inicio
            self.inicio.ant = novo
            self.inicio = novo
        self.tamanho += 1
        self._fecharCiclo()

    def insereNoFim(self, dado):
        """Insere no final ajustando 'ant' do novo e 'prox' do antigo fim."""
        self._checkOverflow()
        novo = NoDuplo(dado)
        if not self.inicio:
            self.inicio = self.fim = novo
        else:
            novo.ant = self.fim
            self.fim.prox = novo
            self.fim = novo
        self.tamanho += 1
        self._fecharCiclo()

    def insereNaPosicao(self, dado, pos):
        """Insere no meio ligando os 4 ponteiros envolvidos (ant e prox dos vizinhos)."""
        self._checkOverflow()
        if pos == 1:
            return self.insereNoInicio(dado)
        if pos == self.tamanho + 1:
            return self.insereNoFim(dado)
        atual = self._obterNo(pos)
        novo = NoDuplo(dado)
        novo.ant, novo.prox = atual.ant, atual
        atual.ant.prox = novo
        atual.ant = novo
        self.tamanho += 1

    def atualiza(self, chave, dadoNovo):
        """Busca pela chave (usando range(tamanho) para não travar se for circular)."""
        aux = self.inicio
        for _ in range(self.tamanho):
            if self._chave(aux.dado) == chave:
                aux.dado = dadoNovo
                return
            aux = aux.prox
        raise KeyError("Chave não encontrada.")

    def atualizaPosicao(self, pos, dadoNovo):
        self._obterNo(pos).dado = dadoNovo

    def deletaDoInicio(self):
        """Remove do início em O(1) e refaz o ciclo se a lista for circular."""
        self._checkUnderflow()
        removido = self.inicio
        dado = removido.dado
        if self.tamanho == 1:
            self.inicio = self.fim = None
        else:
            self.inicio = self.inicio.prox
            self.inicio.ant = None
        del removido
        self.tamanho -= 1
        self._fecharCiclo()
        return dado

    def deletaDoFim(self):
        """Remove do fim em O(1)! Diferente da lista simples, aqui temos self.fim.ant."""
        self._checkUnderflow()
        removido = self.fim
        dado = removido.dado
        if self.tamanho == 1:
            self.inicio = self.fim = None
        else:
            self.fim = self.fim.ant
            self.fim.prox = None
        del removido
        self.tamanho -= 1
        self._fecharCiclo()
        return dado

    def deletaPosicao(self, pos):
        """Remove o nó da posição 'pos' fazendo seus vizinhos apontarem um para o outro."""
        self._checkUnderflow()
        if pos == 1:
            return self.deletaDoInicio()
        if pos == self.tamanho:
            return self.deletaDoFim()
        removido = self._obterNo(pos)
        dado = removido.dado
        removido.ant.prox = removido.prox
        removido.prox.ant = removido.ant
        del removido
        self.tamanho -= 1
        return dado

    def deleta(self, chave):
        """Remove o primeiro nó que tiver a 'chave'."""
        self._checkUnderflow()
        aux = self.inicio
        for _ in range(self.tamanho):
            if self._chave(aux.dado) == chave:
                if aux == self.inicio:
                    return self.deletaDoInicio()
                if aux == self.fim:
                    return self.deletaDoFim()
                dado = aux.dado
                aux.ant.prox = aux.prox
                aux.prox.ant = aux.ant
                del aux
                self.tamanho -= 1
                return dado
            aux = aux.prox
        raise KeyError("Chave não encontrada.")

    def consultaInicio(self):
        self._checkUnderflow()
        return self.inicio.dado

    def consultaFim(self):
        self._checkUnderflow()
        return self.fim.dado

    def consultaPosicao(self, pos):
        return self._obterNo(pos).dado

    def consulta(self, chave):
        aux = self.inicio
        for _ in range(self.tamanho):
            if self._chave(aux.dado) == chave:
                self._ultimo_no = aux
                self._ultima_chave = chave
                return aux.dado
            aux = aux.prox
        return None

    def consultaProximo(self, chave):
        if self._ultima_chave != chave or not self._ultimo_no:
            return self.consulta(chave)
        aux = self._ultimo_no.prox
        while aux and aux != self.inicio:  # Para se der a volta completa na circular
            if self._chave(aux.dado) == chave:
                self._ultimo_no = aux
                return aux.dado
            aux = aux.prox
        return None

    def __iter__(self):
        """Percorre exatamente 'self.tamanho' nós (evita loop infinito se circular=True)."""
        aux = self.inicio
        for _ in range(self.tamanho):
            yield aux.dado
            aux = aux.prox

    def swap(self, pos):
        no1 = self._obterNo(pos)
        no2 = self._obterNo(pos + 1)
        no1.dado, no2.dado = no2.dado, no1.dado


# ==============================================================================
# 4. FILA SIMPLES (QUEUE) E FILA DUPLA (DEQUE)
# Reutilizam os métodos das listas, expondo apenas as operações típicas de fila.
# ==============================================================================
class FilaSimples(ListaEncadeadaSimples):
    """Política FIFO (First-In, First-Out): entra no fim, sai do início (ambos O(1))."""
    def enfileirar(self, dado): self.insereNoFim(dado)
    def desenfileirar(self): return self.deletaDoInicio()
    def frente(self): return self.consultaInicio()


class FilaDupla(ListaEncadeadaDupla):
    """Deque (Double-Ended Queue): permite entrar e sair pelos dois lados em O(1)."""
    def enfileirarInicio(self, dado): self.insereNoInicio(dado)
    def enfileirarFim(self, dado): self.insereNoFim(dado)
    def desenfileirarInicio(self): return self.deletaDoInicio()
    def desenfileirarFim(self): return self.deletaDoFim()


# ==============================================================================
# 5. APLICAÇÃO 1: ÍNDICE INVERTIDO (LISTA DE LISTA ENCADEADA SIMPLES)
# Estrutura: Lista principal de palavras -> cada nó guarda outra lista com (linha, pos).
# ==============================================================================

class PalavraIndice:
    """
    Representa o DADO (no.dado) armazenado dentro de cada nó da lista principal.
    Em vez de guardar apenas uma string solta, guardamos um objeto que reúne
    a palavra (chave) e a sua própria lista encadeada de posições no texto.
    """
    def __init__(self, palavra):
        # A própria palavra em minúsculo serve como 'chave' de busca.
        # É esse atributo que os métodos consulta() e ordena() da ListaEncadeadaSimples
        # leem automaticamente através do método auxiliar _chave(dado).
        self.chave = palavra

        # Cada palavra ganha sua própria ListaEncadeadaSimples vazia para armazenar
        # os pares (num_linha, pos_na_linha) onde ela aparecer ao longo do arquivo.
        self.ocorrencias = ListaEncadeadaSimples()

    def __str__(self):
        """
        Define como o objeto é impresso no terminal quando fazemos print(item).
        Percorre a sublista 'self.ocorrencias' (usando o __iter__ da lista simples)
        e formata cada tupla ligando-as com setas '->' para mostrar o encadeamento.
        """
        cadeia = " -> ".join(f"(Linha {l}, Pos {p})" for l, p in self.ocorrencias)
        return f"[{self.chave}] -> {cadeia}"


class IndiceInvertido:
    """
    Gerencia o índice completo do documento. Possui uma única lista encadeada
    externa (self.palavras) cujos nós contêm objetos do tipo PalavraIndice.
    """
    def __init__(self):
        # Lista encadeada principal (vocabulário de palavras únicas encontradas no texto)
        self.palavras = ListaEncadeadaSimples()

    def indexarArquivo(self, caminho):
        """
        Lê um arquivo .TXT, quebra o texto em linhas e palavras e preenche
        a estrutura de lista de listas.
        """
        # Abre o arquivo em modo leitura ('r') com codificação UTF-8 para aceitar acentos
        with open(caminho, "r", encoding="utf-8") as f:

            # enumerate(f, start=1) entrega cada linha do arquivo já numerada a partir de 1
            for num_linha, linha in enumerate(f, start=1):

                # 1. Limpeza de pontuação: substitui sinais gráficos por vazio ("")
                # para evitar que "Python." e "Python" sejam tratadas como palavras diferentes.
                for c in ".,!?;:()\"'-":
                    linha = linha.replace(c, "")

                # 2. Normalização e quebra em palavras:
                # .lower() transforma tudo em minúsculo ("Python" -> "python").
                # .split() separa a linha nos espaços em branco, gerando as palavras.
                # enumerate(..., start=1) numera a posição da palavra dentro daquela linha (1ª, 2ª, 3ª...).
                for pos, palavra in enumerate(linha.lower().split(), start=1):

                    # 3. Busca na lista principal:
                    # Verifica se já existe algum nó em self.palavras com chave == palavra.
                    # Se existir, 'item' recebe a referência para o objeto PalavraIndice encontrado.
                    # Se não existir, 'item' recebe None.
                    item = self.palavras.consulta(palavra)

                    # 4. Caso a palavra seja nova no texto:
                    if not item:
                        item = PalavraIndice(palavra)      # Cria o pacote (palavra + sublista vazia)
                        self.palavras.insereNoFim(item)    # Cria um NoSimples e engata no fim da lista principal

                    # 5. Registro da ocorrência (funciona tanto para palavra nova quanto repetida):
                    # Acessa a sublista 'ocorrencias' daquele nó e insere a tupla (linha, posição)
                    # no final dela em tempo constante O(1), graças ao ponteiro 'fim' da lista.
                    item.ocorrencias.insereNoFim((num_linha, pos))

    def buscar(self, palavra):
        """
        Responde à pergunta 'onde no texto esta palavra aparece?'.
        Converte a busca para minúsculo e usa o método consulta() da lista principal.
        Retorna o objeto PalavraIndice (se achar) ou None (se a palavra não existir no texto).
        """
        return self.palavras.consulta(palavra.lower())

    def exibirIndice(self):
        """
        Ordena o vocabulário em ordem alfabética e imprime todas as palavras
        seguidas de suas listas encadeadas de ocorrências.
        """
        # Reaproveita o Bubble Sort (ordena) da EstruturaLinear. Como cada item tem
        # self.chave = palavra (string), o Python compara as strings em ordem alfabética.
        self.palavras.ordena()

        # Percorre a lista principal usando o __iter__ e chama o __str__ de cada PalavraIndice
        for item in self.palavras:
            print(item)
# ==============================================================================
# 6. APLICAÇÃO 2: EDITOR DE FIGURAS GEOMÉTRICAS PLANAS
# Cada figura é uma ListaEncadeadaDupla (circular se fechada) onde cada nó
# guarda uma coordenada [x, y].
# ==============================================================================
class FiguraPlana:
    def __init__(self, nome, pontos, fechada=True):
        self.chave = nome        # Nome da figura (usado como chave de busca/remoção)
        self.fechada = fechada   # Se True, o último vértice liga de volta ao primeiro
        # Cada nó guarda uma lista mutável [x, y] para facilitar alterações de posição
        self.vertices = ListaEncadeadaDupla([[float(x), float(y)] for x, y in pontos], circular=fechada)

    def perimetro(self):
        """Soma a distância euclidiana entre cada par de vértices consecutivos."""
        total = 0.0
        atual = self.vertices.inicio
        # Figura fechada tem 'n' lados; figura aberta tem 'n - 1' lados
        arestas = len(self.vertices) if self.fechada else len(self.vertices) - 1
        for _ in range(arestas):
            p1, p2 = atual.dado, atual.prox.dado
            total += ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
            atual = atual.prox
        return total

    def transladar(self, xv, yv, inicio=1, fim=None):
        """Desloca todos os vértices (ou apenas do índice 'inicio' até 'fim') por (xv, yv)."""
        fim = fim or len(self.vertices)
        for i in range(inicio, fim + 1):
            p = self.vertices[i]
            p[0] += xv
            p[1] += yv

    def escalar(self, fator):
        """Amplia ou reduz a figura em relação ao seu centro geométrico (centroide)."""
        n = len(self.vertices)
        cx = sum(p[0] for p in self.vertices) / n  # Média de X
        cy = sum(p[1] for p in self.vertices) / n  # Média de Y
        for p in self.vertices:
            p[0] = cx + (p[0] - cx) * fator
            p[1] = cy + (p[1] - cy) * fator

    def concatenarFigura(self, aresta1, outra, aresta2):
        """
        Une duas figuras removendo as duas arestas adjacentes (aresta1 e aresta2)
        e religando os ponteiros das extremidades para formar um único polígono.
        """
        no1_a = self.vertices._obterNo(aresta1)
        no1_b = no1_a.prox
        no2_a = outra.vertices._obterNo(aresta2)
        no2_b = no2_a.prox

        # Liga as pontas externas da figura 1 com as da figura 2 (apagando o lado interno)
        no1_a.prox, no2_b.ant = no2_b, no1_a
        no2_a.prox, no1_b.ant = no1_b, no2_a

        self.vertices.inicio, self.vertices.fim = no1_a, no1_b
        self.vertices.tamanho += len(outra.vertices)
        self.vertices._fecharCiclo()

    def sweepLado(self, aresta, trajetoria):
        """
        Desliza o lado escolhido (vértices pA e pB) ao longo dos pontos de 'trajetoria'.
        Cria os vértices intermediários de ida (acompanhando pA) e volta (acompanhando pB).
        """
        noA = self.vertices._obterNo(aresta)
        noB = noA.prox
        pA, pB = list(noA.dado), list(noB.dado)  # Copia as coordenadas originais do lado

        # Calcula quanto cada ponto da trajetória anda em relação ao ponto inicial dela
        desloc = [(x - trajetoria[0][0], y - trajetoria[0][1]) for x, y in trajetoria[1:]]

        # Monta os novos nós: primeiro os pontos do lado A indo, depois os do lado B voltando
        novos = [NoDuplo([pA[0] + dx, pA[1] + dy]) for dx, dy in desloc] + \
                [NoDuplo([pB[0] + dx, pB[1] + dy]) for dx, dy in reversed(desloc)]

        # Encaixa todos os novos nós entre noA e noB
        cursor = noA
        for novo in novos:
            novo.ant, novo.prox = cursor, cursor.prox
            cursor.prox.ant = novo
            cursor.prox = novo
            cursor = novo
            self.vertices.tamanho += 1

        if noB == self.vertices.inicio:
            self.vertices.fim = noB.ant
        self.vertices._fecharCiclo()

    def __str__(self):
        pts = " -> ".join(f"({p[0]:.1f},{p[1]:.1f})" for p in self.vertices)
        return f"{self.chave} [Perímetro={self.perimetro():.2f}]: {pts}"


class EditorGeometrico:
    """Gerencia uma lista encadeada dupla de figuras planas."""
    def __init__(self):
        self.figuras = ListaEncadeadaDupla()

    def criarFigura(self, nome, pontos, fechada=True):
        fig = FiguraPlana(nome, pontos, fechada)
        self.figuras.insereNoFim(fig)
        return fig

    def carregarArquivo(self, caminho):
        """Lê figuras de um arquivo .txt/.csv no formato: Nome;x1,y1;x2,y2;..."""
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(";")
                if len(partes) >= 3:
                    pts = [[float(v) for v in par.split(",")] for par in partes[1:]]
                    # Se o último ponto for igual ao primeiro, fecha a figura automaticamente
                    self.criarFigura(partes[0], pts, fechada=(pts[0] == pts[-1]))


# ==============================================================================
# 7. APLICAÇÃO 3: FILA DO BANDEJÃO
# Usa FilaSimples (FIFO) onde cada nó guarda um objeto Pedido.
# ==============================================================================
class Pedido:
    """Dado armazenado em cada nó da fila do bandejão."""
    def __init__(self, dre, nome, retiradaMin):
        self.chave = dre            # DRE do aluno (chave única para busca/desistência)
        self.nome = nome
        self.retirada = retiradaMin # Horário previsto em minutos acumulados (ex: 720 = 12:00)

    def __str__(self):
        h, m = int(self.retirada // 60) % 24, int(self.retirada % 60)
        return f"[{self.chave} - {self.nome} | Retirada: {h:02d}:{m:02d}]"


class SistemaBandejao:
    def __init__(self, tempoMedio=2.0, horaAtual=720.0):
        self.fila = FilaSimples()
        self.tempoMedio = tempoMedio  # Tempo médio de atendimento por pessoa (em minutos)
        self.horaAtual = horaAtual    # Relógio atual da simulação (720 min = 12:00)

    def tempoEspera(self):
        """Calcula quanto tempo um novo usuário vai esperar antes de entrar na fila."""
        return len(self.fila) * self.tempoMedio

    def entrar(self, dre, nome):
        """Calcula o horário de retirada do prato e enfileira o pedido no fim."""
        p = Pedido(dre, nome, self.horaAtual + self.tempoEspera() + self.tempoMedio)
        self.fila.enfileirar(p)
        return p

    def _ajustar(self, delta, inicio=1):
        """Soma ou subtrai 'delta' minutos na previsão de todos a partir da posição 'inicio'."""
        for i in range(inicio, len(self.fila) + 1):
            self.fila[i].retirada += delta

    def desistir(self, dre):
        """Remove o desistente pelo DRE e antecipa o horário de quem estava atrás dele."""
        pos = next((i for i in range(1, len(self.fila) + 1) if self.fila[i].chave == dre), -1)
        if pos == -1:
            raise KeyError("Usuário não está na fila.")
        self.fila.deleta(dre)
        self._ajustar(-self.tempoMedio, pos)  # Quem estava atrás ganha o tempo de 1 atendimento

    def atender(self, atraso=0.0, faltou=False):
        """
        Retira o primeiro da fila (FIFO) e recalcula o tempo dos demais:
        - Se 'faltou=True': o próximo entra imediatamente (adianta todos em tempoMedio).
        - Se houver 'atraso' (+ ou -): ajusta o relógio e a previsão de toda a fila.
        """
        atendido = self.fila.desenfileirar()
        if faltou:
            self._ajustar(-self.tempoMedio)
        else:
            self.horaAtual += self.tempoMedio + atraso
            if atraso:
                self._ajustar(atraso)
        return atendido


# ==============================================================================
# 8. TESTE VISUAL DIRETO
# ==============================================================================
if __name__ == "__main__":
    print("=== 1. ÍNDICE INVERTIDO ===")
   # with open("texto.txt", "w", encoding="utf-8") as f:
    #    f.write("Estrutura de dados em Python.\nPython usa listas encadeadas.")
    #idx = IndiceInvertido()
    #idx.indexarArquivo("texto.txt")
    #print(idx.buscar("python"))
    "REFATORAÇÃO: LOOP PARA VERIFICAR SE ARQUIVO FOI CRIADO"
    caminho_txt = "texto.txt"

    # Verifica se o arquivo já existe sem usar 'import os':
    try:
        # Tenta abrir apenas para leitura; se existir, não altera nada
        with open(caminho_txt, "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        # Só entra aqui se o arquivo NÃO existir: cria o texto padrão inicial
        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write("Estrutura de dados em Python.\nPython usa listas encadeadas.")

    # Lê e indexa o que estiver dentro do arquivo (seja o criado agora ou o editado por você)
    indice = IndiceInvertido()
    indice.indexarArquivo(caminho_txt)
    indice.exibirIndice()
    print("\n=== 2. EDITOR GEOMÉTRICO ===")
    ed = EditorGeometrico()
    q1 = ed.criarFigura("Quad1", [(0, 0), (2, 0), (2, 2), (0, 2)])
    q2 = ed.criarFigura("Quad2", [(3, 0), (5, 0), (5, 2), (3, 2)])
    q1.concatenarFigura(2, q2, 4)
    print("Concatenação (8 vértices):", q1)

    q3 = ed.criarFigura("QuadSweep", [(0, 0), (2, 0), (2, 2), (0, 2)])
    q3.sweepLado(2, [(2, 0), (4, 2), (6, 0)])
    print("Sweep:", q3)

    print("\n=== 3. FILA DO BANDEJÃO ===")
    band = SistemaBandejao(tempoMedio=3.0, horaAtual=720.0)
    band.entrar("111", "Ana")
    band.entrar("222", "Bruno")
    band.entrar("333", "Carla")
    print("Fila inicial:", [str(x) for x in band.fila])
    band.desistir("222")
    print("Após Bruno desistir:", [str(x) for x in band.fila])
    band.atender(atraso=5.0)
    print("Após atendimento com 5 min de atraso:", [str(x) for x in band.fila])