# Gestor Financeiro Offline (Android APK & PWA)

Um aplicativo financeiro pessoal **100% offline, gratuito e privado**, criado para controlar faturas de cartões de crédito, definir tetos mensais, visualizar gráficos por categoria e melhorar hábitos financeiros — **sem enviar seus dados para nenhum servidor ou nuvem**.

---

## 🔒 Privacidade e Segurança em Primeiro Lugar

- **Sem permissão de Internet no Android:** O arquivo `AndroidManifest.xml` não solicita `INTERNET`. Seus extratos e faturas nunca saem do aparelho.
- **Processamento 100% Local:** A leitura de arquivos Excel (`.xlsx`), `.csv`, `.ofx` e texto é feita inteiramente no seu telefone.
- **Proteção de Dados:** Backups exportados em `.csv` possuem sanitização contra injeção de fórmulas em planilhas, e todas as entradas são escapadas contra XSS.
- **Sem Dados Embutidos:** Ao abrir pela primeira vez, um assistente inicial configura o aplicativo para o **seu uso** (seu nome, seu limite e seus cartões).

---

## ✨ Funcionalidades

- **🔔 Leitor Automático de Compras (Offline):** Intercepta notificações bancárias de compras em tempo real (Nubank, Itaú, Mercado Pago, Inter, C6, Santander, Bradesco, PicPay, etc.) e cadastra seus gastos automaticamente sem precisar abrir o app nem digitar nada!
- **Assistente de Configuração Inicial:** Personalize seu nome, teto mensal de gastos e adicione quantos cartões quiser (Nubank, Itaú, Mercado Pago, Inter, C6, Santander, etc.).
- **Histórico Mensal & Comparativo:** Navegue entre meses (`◀ Mês ▶`) para consultar faturas passadas e ver a variação percentual em relação ao mês anterior.
- **Editar Compras & Regras Automáticas:** Toque em qualquer compra para corrigir valores/categorias e salve regras do tipo *"Sempre classificar esta loja assim"* para importações futuras.
- **Parcelamentos & Metas por Categoria:** Lance compras parceladas (`1x` a `12x`) projetadas automaticamente nos próximos meses e crie tetos individuais por categoria.
- **Subir Faturas para Atualizar o Preço:**
  - Envie arquivos exportados pelo seu banco (`.xlsx`, `.xls`, `.csv`, `.ofx`, `.txt`), cole texto ou ajuste só o valor fechado.
  - Pré-visualização interativa com seleção de itens, troca de categoria por linha e escolha do mês de destino.
- **Proteção por PIN (4 dígitos) & Botão Voltar Nativo:** Trave a abertura do app com PIN opcional nas configurações e navegue entre abas/modais usando o botão voltar do Android.
- **Gráficos, Hábitos & Backup:** Gráficos interativos, detector de micro-compras, simulador de economia e exportação/restauração em `.json` ou `.csv`.

---

## 📲 Como Instalar e Ativar a Captura Automática no Android

1. Acesse a aba **Releases** deste repositório no GitHub e baixe o arquivo **`GestorFinanceiro.apk`**.
2. Toque no arquivo baixado no seu celular Android para instalar.
3. Na primeira abertura, configure seu perfil e cartões.
4. **Ativação da Captura Automática de Notificações (Android 13+):**
   - O Android restringe por padrão o acesso a notificações em aplicativos instalados fora da Play Store (*sideload*).
   - O próprio app exibe um banner com 2 passos simples:
     1. Toque em **"1. Liberar Restritas"**: abrirá as Informações do App. Toque nos **três pontinhos (⋮)** no topo direito e selecione **"Permitir configurações restritas"** (confirme com sua digital/PIN).
     2. Volte ao app e toque em **"2. Ativar Leitor"**: marque a chavinha do **Gestor Financeiro**.
   - Pronto! A partir desse momento, qualquer compra ou pagamento aprovado no seu cartão será capturado e categorizado no app na hora.

---

## 🛠️ Como Compilar Automaticamente no GitHub

Este repositório já inclui o workflow `.github/workflows/build-apk.yml`:
1. Faça um **Fork** deste repositório (ou suba os arquivos para sua conta no GitHub).
2. A cada push na branch `main`, o **GitHub Actions** compila o APK automaticamente na nuvem.
3. Ao criar uma tag de versão (ex: `v2.0.0`), o APK compilado e assinado é publicado automaticamente na aba **Releases**.

### Compilar Localmente no Windows
Se você tiver o Android SDK (`build-tools` e `platforms/android-34`) e JDK instalados:
```powershell
.\scripts\build_apk.ps1
```
O APK será gerado em `build\GestorFinanceiro.apk` (que está protegido no `.gitignore` junto com sua chave local `.keystore`).

---

## 📚 Documentação Técnica e Especificação de Arquitetura

O projeto conta com um manual técnico abrangente em PDF (18 páginas), formatado nos padrões de documentação de referência da indústria de software (SAS / Whitepaper):
- **Download do Manual:** [Manual_Tecnico_Gestor_Financeiro.pdf](docs/Manual_Tecnico_Gestor_Financeiro.pdf)
- **Conteúdo Coberto:** Filosofia *Zero-Cloud* e modelo de ameaças STRIDE, diagramas de arquitetura em camadas, funcionamento interno do `NotificationListenerService`, algoritmos de parsing e extração heurística por regex, sanitização contra CWE-1236, pipeline de compilação determinística sem Gradle e manual de operação.

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
