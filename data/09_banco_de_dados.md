# Banco de Dados Relacional

## Modelo Relacional

Proposto por Edgar F. Codd em 1970, o modelo relacional organiza
dados em tabelas (também chamadas de relações). Cada tabela tem
linhas (tuplas/registros) e colunas (atributos/campos). Esse modelo
domina a indústria de bancos de dados há décadas, e é a base de
sistemas como PostgreSQL, MySQL, Oracle, SQL Server e SQLite.

## Conceitos Fundamentais

- Tabela: estrutura que armazena dados sobre uma entidade (ex:
  alunos, disciplinas, matrículas).
- Chave Primária (Primary Key, PK): identifica unicamente cada linha
  da tabela. Não pode ser nula nem duplicada.
- Chave Estrangeira (Foreign Key, FK): coluna que referencia a PK de
  outra tabela, estabelecendo relacionamentos.
- Índice: estrutura auxiliar (geralmente B-Tree) que acelera buscas
  em colunas específicas.

## Linguagem SQL

SQL (Structured Query Language) é a linguagem padrão para interagir
com bancos relacionais. Divide-se em:

- DDL (Data Definition Language): CREATE, ALTER, DROP — define
  estrutura.
- DML (Data Manipulation Language): SELECT, INSERT, UPDATE, DELETE —
  manipula dados.
- DCL (Data Control Language): GRANT, REVOKE — controle de acesso.
- TCL (Transaction Control Language): COMMIT, ROLLBACK — controle de
  transações.

## Normalização

Normalização é o processo de organizar tabelas para eliminar
redundâncias e anomalias. As principais formas normais são:

- 1FN (Primeira Forma Normal): todos os valores são atômicos (não há
  listas dentro de células).
- 2FN: além da 1FN, todos os atributos não-chave dependem totalmente
  da chave primária (elimina dependência parcial).
- 3FN: além da 2FN, não há dependências transitivas (atributos
  não-chave não dependem de outros não-chave).
- BCNF (Boyce-Codd): forma mais rigorosa da 3FN.

Na prática, a maioria dos bancos é desenhada até a 3FN, e às vezes se
faz desnormalização proposital para ganhar performance em consultas.

## Propriedades ACID

Transações em bancos relacionais garantem quatro propriedades:

- Atomicidade: a transação acontece por inteiro ou nada acontece.
- Consistência: o banco passa de um estado válido para outro válido.
- Isolamento: transações concorrentes não interferem umas nas outras.
- Durabilidade: uma vez confirmada, a transação persiste mesmo após
  falhas.

## Joins

Joins combinam dados de várias tabelas:

- INNER JOIN: só registros que dão match nas duas tabelas.
- LEFT/RIGHT OUTER JOIN: todos da tabela à esquerda/direita, com
  NULL onde não houver correspondência.
- FULL OUTER JOIN: união de tudo.
- CROSS JOIN: produto cartesiano.

## Índices e Performance

Índices aceleram SELECT mas tornam INSERT/UPDATE/DELETE mais lentos
(porque o índice precisa ser atualizado). Boa prática: indexar
colunas usadas em WHERE, JOIN e ORDER BY, mas com moderação.

## Relacionais vs NoSQL

Bancos relacionais são ótimos para dados estruturados com
relacionamentos claros e necessidade de consistência forte (ACID).
Bancos NoSQL (MongoDB, Cassandra, Redis) trocam parte dessas
garantias por escalabilidade horizontal, esquema flexível ou
desempenho específico. A escolha depende do problema.
