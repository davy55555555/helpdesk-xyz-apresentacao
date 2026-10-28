# HelpDesk XYZ

Projeto acadêmico de Análise e Projeto de Sistemas da UDF. A proposta organiza chamados de suporte técnico e relaciona a melhoria do atendimento à infraestrutura digital, como contribuição indireta ao ODS 9.

## Protótipo local

O protótipo demonstra a abertura e a consulta de chamados, atribuição a um técnico, comentários, resolução e cancelamento. Ele usa apenas a biblioteca padrão do Python 3.9 ou superior.

1. Baixe `app.py` deste repositório.
2. Em um terminal, execute `python3 app.py` na pasta onde o arquivo foi salvo.
3. Abra `http://127.0.0.1:8501` no navegador.
4. Para encerrar, pressione `Ctrl+C` no terminal.

Para a demonstração, abra um chamado como Cliente, selecione Administrador para atribuí-lo e depois selecione Técnico para comentar e resolver.

## Limitações

A escolha de perfil simula a autenticação, com identidades fictícias. Não há senha, cadastro de usuários, anexos ou armazenamento persistente: os chamados desaparecem quando o programa é encerrado. Não informe dados pessoais reais. O código é um protótipo acadêmico, não um serviço de produção.

## Materiais

- `01_casos_de_uso.drawio` a `07_objetos.drawio`: diagramas editáveis no draw.io.
- `Apresentacao_HelpDesk_XYZ.pdf`: slides para visualização.
- `Apresentacao_HelpDesk_XYZ.pptx`: slides editáveis.
- `app.py`: aplicação demonstrativa local.

A documentação completa é mantida separadamente para a entrega acadêmica. O protótipo demonstra uma parte dos requisitos documentados; as funcionalidades não implementadas estão descritas acima.
