# p1ufcg

`p1ufcg` é um pacote com ferramentas para o apoio às disciplinas de
Programação 1 da Computação@UFCG.

## Como instalar

```
pip3 install p1ufcg
```

## Inclui...

A ideia é que o `p1ufcg` inclua de uma única vez vários pacotes e
módulos que são úteis no contexto da disciplina, facilitando sua
instalação por parte do estudante. Abaixo uma lista do que é
instalado com a atual versão.

### comandos `p1`

Estes comandos permitem interagir com o site de atividades da
disciplina, através do shell, em interface de linha de comando.

- `p1 login`: para fazer login no site
- `p1 logout`: para fazer logout
- `p1 checkout`: para baixar o diretório e arquivos de atividades
- `p1 commit`: para registrar respostas de atividades

### packages

Pacotes com ferramentas para testes que são instalados:

- [tst](https://github.com/daltonserey/tst)
- [pytest](https://docs.pytest.org) e [pytest-tst](https://pypi.org/project/pytest-tst/)

### módulos

- [Array](array.md)
