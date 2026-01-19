# Modelo de Pull Request para Git Flow

**Nota:** Este modelo é projetado para alinhar-se com o fluxo de trabalho do Git Flow. Por favor, certifique-se de que a nomenclatura do seu branch e o alvo estejam alinhados com isso.

## 1\. Informações do Branch

- **Branch de Origem:** \[ex: feature/nova-funcionalidade, hotfix/bug-crítico\]

- **Branch de Destino:** \[ex: develop, main\]

## 2\. Descrição

- Forneça uma descrição clara e concisa das mudanças incluídas neste pull request.

- Explique o _porquê_ das mudanças. Que problema isso resolve?

## 3\. Problemas/Issues Relacionados

- Liste quaisquer problemas ou issues relacionados.

- Use palavras-chave como Closes, Fixes ou Resolves para fechá-los automaticamente ao mesclar.

  - Exemplo: Closes #123, Fixes ISSUE-456

## 4\. Tipo de Mudança

- Que tipo de mudança é esta?

  - \[ \] Nova Funcionalidade

  - \[ \] Correção de Bug

  - \[ \] Hotfix (correção urgente para produção)

  - \[ \] Refatoração (melhoria de código, sem nova funcionalidade)

  - \[ \] Documentação (mudanças na documentação)

  - \[ \] Outro (por favor, especifique)

## 5\. Mudanças no Código

- Descreva as principais mudanças no código.

- Destaque quaisquer mudanças significativas na lógica, novas classes/funções ou modificações nas existentes.

- Se as mudanças forem complexas, forneça uma visão geral de alto nível ou trechos de código.

## 6\. Testes

- Descreva os testes que você realizou para validar suas mudanças.

- Inclua detalhes sobre:

  - Testes unitários

  - Testes de integração

  - Testes manuais

  - Quaisquer novos testes adicionados

- Especifique quaisquer ferramentas ou frameworks de teste utilizados.

## 7\. Capturas de Tela (Opcional)

- Se as mudanças afetarem a interface do usuário, inclua capturas de tela ou GIFs.

- Isso ajuda os revisores a visualizar as mudanças.

## 8\. Lista de Verificação

- Antes de enviar, certifique-se de que você concluiu o seguinte:

  - \[ \] O código segue os padrões de codificação do projeto.

  - \[ \] Todos os testes passam com sucesso.

  - \[ \] A documentação foi atualizada, se necessário.

  - \[ \] O branch está atualizado com o branch de destino.

  - \[ \] Eu revisei meu próprio código.

  - \[ \] Eu adicionei comentários ao meu código onde necessário.

  - \[ \] Eu abordei todos os comentários dos revisores (se aplicável).

## 9\. Notas Adicionais

- Inclua qualquer outra informação relevante, como:

  - Dependências adicionadas ou atualizadas

  - Quaisquer problemas ou limitações conhecidas

  - Instruções especiais para revisores

  - Considerações sobre implantação

## 10\. Revisores

- Marque os revisores apropriados para este pull request. (\`@username\`)