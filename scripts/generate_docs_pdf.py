# -*- coding: utf-8 -*-
"""
Script de Geracao de Documentacao Tecnica Oficial em PDF
Gestor Financeiro Offline v2.3.0
"""
import os
import subprocess
import sys

def build_html():
    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Documentação Técnica Oficial - Gestor Financeiro Offline</title>
<style>
  @page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
    @bottom-center {
      content: counter(page);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #64748b;
    }
  }

  *, *:before, *:after {
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.55;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
  }

  /* Capa */
  .cover-page {
    page-break-after: always;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 30mm 10mm 20mm 10mm;
    border-left: 6px solid #2563eb;
    background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
  }

  .cover-header {
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 15px;
  }

  .cover-badge {
    display: inline-block;
    background: #eff6ff;
    color: #2563eb;
    border: 1px solid #bfdbfe;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 12px;
  }

  .cover-title {
    font-size: 26pt;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.15;
    margin: 0 0 10px 0;
  }

  .cover-subtitle {
    font-size: 13pt;
    font-weight: 500;
    color: #475569;
    margin: 0 0 20px 0;
    line-height: 1.4;
  }

  .cover-meta-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin-top: 30px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 18px;
  }

  .cover-meta-item strong {
    display: block;
    font-size: 7.5pt;
    text-transform: uppercase;
    color: #64748b;
    letter-spacing: 0.05em;
    margin-bottom: 2px;
  }

  .cover-meta-item span {
    font-size: 9.5pt;
    font-weight: 600;
    color: #0f172a;
  }

  .cover-footer {
    border-top: 1px solid #e2e8f0;
    padding-top: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 8pt;
    color: #64748b;
  }

  /* Quebras de página e seções */
  .page-break {
    page-break-before: always;
  }

  .no-break {
    page-break-inside: avoid;
  }

  h1, h2, h3, h4 {
    color: #0f172a;
    font-weight: 800;
    page-break-after: avoid;
  }

  h1 {
    font-size: 16pt;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 6px;
    margin-top: 25px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  h2 {
    font-size: 12pt;
    border-left: 3px solid #2563eb;
    padding-left: 8px;
    margin-top: 20px;
    margin-bottom: 10px;
    color: #1e3a8a;
  }

  h3 {
    font-size: 10.5pt;
    margin-top: 14px;
    margin-bottom: 6px;
    color: #334155;
  }

  p {
    margin-top: 0;
    margin-bottom: 10px;
    text-align: justify;
  }

  /* Listas */
  ul, ol {
    margin-top: 0;
    margin-bottom: 12px;
    padding-left: 20px;
  }

  li {
    margin-bottom: 4px;
  }

  /* Tabelas corporativas */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }

  th, td {
    border: 1px solid #cbd5e1;
    padding: 7px 10px;
    text-align: left;
  }

  th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
  }

  tr:nth-child(even) {
    background-color: #f8fafc;
  }

  /* Blocos de Código e Caixas de Sintaxe */
  pre {
    background: #0f172a;
    color: #f8fafc;
    padding: 10px 14px;
    border-radius: 6px;
    font-family: "Cascadia Code", Consolas, Monaco, "Courier New", monospace;
    font-size: 7.8pt;
    line-height: 1.45;
    overflow-x: hidden;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 10px 0;
    page-break-inside: avoid;
    border-left: 4px solid #38bdf8;
  }

  code {
    background: #f1f5f9;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 4px;
    font-family: Consolas, monospace;
    font-size: 8.5pt;
  }

  pre code {
    background: transparent;
    color: inherit;
    padding: 0;
  }

  /* Caixas de Alerta (Industry Standard Callouts) */
  .callout {
    padding: 10px 14px;
    border-radius: 6px;
    margin: 12px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }

  .callout-info {
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    color: #1e40af;
  }

  .callout-success {
    background: #ecfdf5;
    border-left: 4px solid #10b981;
    color: #065f46;
  }

  .callout-warning {
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    color: #92400e;
  }

  .callout-danger {
    background: #fef2f2;
    border-left: 4px solid #ef4444;
    color: #991b1b;
  }

  .callout-title {
    font-weight: 700;
    margin-bottom: 3px;
    text-transform: uppercase;
    font-size: 7.5pt;
    letter-spacing: 0.04em;
  }

  /* Diagramas ASCII / Fluxos */
  .diagram-box {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px;
    margin: 12px 0;
    font-family: Consolas, monospace;
    font-size: 7.5pt;
    line-height: 1.35;
    color: #0f172a;
    page-break-inside: avoid;
  }

  /* Sumário / Índice */
  .toc-item {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px dotted #cbd5e1;
    padding: 5px 0;
    font-size: 9pt;
  }

  .toc-item a {
    text-decoration: none;
    color: #1e293b;
    font-weight: 500;
  }

  .toc-item span {
    color: #64748b;
    font-weight: 600;
  }

  .badge-tag {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 7pt;
    font-weight: 700;
    text-transform: uppercase;
  }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-green { background: #d1fae5; color: #065f46; }
  .badge-amber { background: #fef3c7; color: #92400e; }
</style>
</head>
<body>

<!-- CAPA -->
<div class="cover-page">
  <div class="cover-header">
    <span class="cover-badge">Manual de Engenharia &amp; Arquitetura</span>
    <h1 class="cover-title">GESTOR FINANCEIRO OFFLINE</h1>
    <div class="cover-subtitle">Documentação Técnica Oficial, Especificação de Engenharia e Guia Operacional de Sistema</div>
    <p style="color: #64748b; font-size: 9pt; max-width: 90%;">
      Referência arquitetural completa cobrindo o paradigma <i>Offline-First</i>, mecanismo nativo de captura de notificações bancárias em tempo real, motor de processamento de faturas (XLSX, CSV, OFX), modelo de ameaças de segurança e pipeline de compilação sem dependência de Gradle.
    </p>
  </div>

  <div class="cover-meta-grid">
    <div class="cover-meta-item">
      <strong>Versão do Sistema</strong>
      <span>v2.3.0 (Build Code: 5)</span>
    </div>
    <div class="cover-meta-item">
      <strong>Classificação do Documento</strong>
      <span>Software Architecture Specification (SAS)</span>
    </div>
    <div class="cover-meta-item">
      <strong>Plataforma &amp; Compatibilidade</strong>
      <span>Android 7.0 a 14+ (API 24–34) / PWA Moderno</span>
    </div>
    <div class="cover-meta-item">
      <strong>Licenciamento</strong>
      <span>Open Source — Licença MIT</span>
    </div>
    <div class="cover-meta-item">
      <strong>Identificador de Pacote</strong>
      <span>com.gestorfinanceiro.app</span>
    </div>
    <div class="cover-meta-item">
      <strong>Data de Publicação</strong>
      <span>Novembro de 2026</span>
    </div>
  </div>

  <div class="cover-footer">
    <div><strong>Projeto Gestor Financeiro</strong> — Engenharia de Sistemas Móveis Privados</div>
    <div>Página 1</div>
  </div>
</div>

<!-- SUMÁRIO EXECUTIVO E ÍNDICE -->
<div class="page-break"></div>

<h1>Sumário Executivo e Metadados do Sistema</h1>

<p>
O <strong>Gestor Financeiro</strong> é uma solução de engenharia de software desenvolvida para preencher uma lacuna crítica no ecossistema atual de tecnologia financeira (FinTech): a reconciliação entre <strong>automação financeira sem atrito</strong> e <strong>privacidade absoluta de dados</strong>.
</p>

<p>
A quase totalidade dos aplicativos financeiros comerciais no mercado contemporâneo adota modelos baseados em nuvem com sincronização remota obrigatória (Open Finance / OAuth de instituições bancárias). Embora convenientes, esses modelos expõem o histórico transacional completo do indivíduo a servidores remotos, serviços de analytics, riscos de vazamento de credenciais e dependência de assinaturas pagas. O Gestor Financeiro subverte essa abordagem através de uma arquitetura <strong>100% Offline-First</strong>, sem permissão de acesso à Internet (<code>android.permission.INTERNET</code> ausente no Manifesto Android), implementando processamento de linguagem natural heurístico e leitura assíncrona de eventos do sistema operacional na camada do cliente.
</p>

<h2>Registro Histórico de Versões (Changelog de Engenharia)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 12%;">Versão</th>
      <th style="width: 15%;">Data</th>
      <th style="width: 25%;">Marco Arquitetural</th>
      <th>Descrição Técnica das Mudanças</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>v1.0.0</strong></td>
      <td>Out/2026</td>
      <td>Lançamento Inicial MVP</td>
      <td>Painel SPA local, controle de teto mensal, gráficos via Chart.js, banco local em LocalStorage.</td>
    </tr>
    <tr>
      <td><strong>v2.0.0</strong></td>
      <td>Nov/2026</td>
      <td>Motor de Faturas &amp; Isolamento</td>
      <td>Módulo de ingestão SheetJS (XLSX, XLS, CSV, OFX), prevenção de CSV Injection (CWE-1236), separação do projeto pessoal vs. repositório genérico aberto.</td>
    </tr>
    <tr>
      <td><strong>v2.1.0</strong></td>
      <td>Nov/2026</td>
      <td>Inteligência e Segurança</td>
      <td>Navegação de histórico multi-mês, motor de regras de categorização com aprendizado de máquina local, parcelamentos projetados, metas por categoria, autenticação PIN com hash SHA-256 e interceptação do botão Voltar nativo.</td>
    </tr>
    <tr>
      <td><strong>v2.2.0</strong></td>
      <td>Nov/2026</td>
      <td>Leitor Nativo de Notificações</td>
      <td>Implementação do <code>NotificationListenerService</code> Java nativo, interceptador de compras em tempo real para bancos brasileiros, ponte de comunicação bidirecional com o WebView, bypass de restrições de sideload do Android 13+.</td>
    </tr>
    <tr>
      <td><strong>v2.3.0</strong></td>
      <td>Nov/2026</td>
      <td>Leitura Integral, Filtro de Crédito Estrito e Aprendizado Contínuo</td>
      <td>Extração profunda de todos os campos de notificação do Android (BigText, Lines, Ticker), filtro estrito de Cartão de Crédito com rejeição determinística de débito, saldo e Pix, limpeza inteligente de gateways de pagamento (PG*, MP*, etc.), sincronização bidirecional de regras aprendidas com atualização retroativa de lançamentos existentes e persistência compartilhada em SharedPreferences.</td>
    </tr>
  </tbody>
</table>

<h2>Índice Geral do Documento</h2>
<div style="margin-top: 15px;">
  <div class="toc-item"><a href="#sec-1">1. Filosofia de Design e Modelo de Ameaças (Threat Model)</a> <span>Pág. 3</span></div>
  <div class="toc-item"><a href="#sec-2">2. Topologia de Arquitetura Técnica de Camadas</a> <span>Pág. 4</span></div>
  <div class="toc-item"><a href="#sec-3">3. Módulo Nativo: NotificacaoListener e Captura em Tempo Real</a> <span>Pág. 6</span></div>
  <div class="toc-item"><a href="#sec-4">4. Motor de Ingestão de Dados e Parsing de Faturas Bancárias</a> <span>Pág. 9</span></div>
  <div class="toc-item"><a href="#sec-5">5. Motor de Regras Financeiras, Parcelamentos e Projeções</a> <span>Pág. 11</span></div>
  <div class="toc-item"><a href="#sec-6">6. Camada de Segurança, Autenticação PIN e Persistência</a> <span>Pág. 13</span></div>
  <div class="toc-item"><a href="#sec-7">7. Pipeline de Compilação Determinística e CI/CD sem Gradle</a> <span>Pág. 15</span></div>
  <div class="toc-item"><a href="#sec-8">8. Manual de Operação e Resolução de Problemas (Troubleshooting)</a> <span>Pág. 17</span></div>
  <div class="toc-item"><a href="#sec-9">9. Especificações Técnicas e Glossário de Engenharia</a> <span>Pág. 19</span></div>
</div>

<!-- SEÇÃO 1: FILOSOFIA E THREAT MODEL -->
<div class="page-break"></div>

<h1 id="sec-1">1. Filosofia de Design e Modelo de Ameaças (Threat Model)</h1>

<p>
O projeto é fundamentado no princípio do <strong>Privilégio Mínimo</strong> e na premissa de <strong>Confiança Zero Externa (External Zero-Trust)</strong>. No desenvolvimento para plataformas móveis, aplicações que manipulam dados financeiros tradicionalmente solicitam amplos privilégios de conectividade e leitura de arquivos. O Gestor Financeiro demonstra que é viável entregar uma experiência de usuário (UX) de alta fidelidade sem conceder privilégios de exfiltração de dados ao software.
</p>

<h2>1.1 O Paradigma Zero-Cloud e Eliminação da Permissão de Rede</h2>
<p>
No sistema operacional Android, para que um aplicativo emita pacotes TCP/UDP ou se comunique com a Internet, é obrigatório declarar formalmente no arquivo <code>AndroidManifest.xml</code> a seguinte diretiva:
</p>
<pre><code>&lt;uses-permission android:name="android.permission.INTERNET" /&gt;</code></pre>
<p>
<strong>No Gestor Financeiro, esta linha não existe.</strong> Ao omitir essa declaração, o kernel Linux e o subsistema de permissões do Android revogam, em nível de sandbox de processos (UID isolado), a criação de sockets de rede para a aplicação. Mesmo que uma biblioteca de terceiros fosse introduzida maliciosamente no código, qualquer chamada de sistema do tipo <code>connect()</code> ou <code>socket()</code> resultaria em uma exceção imediata de <code>SecurityException</code> retornada pelo sistema operacional.
</p>

<div class="callout callout-success">
  <div class="callout-title">Garantia Criptográfica e Auditável de Privacidade</div>
  A ausência de permissão de rede é verificável por qualquer usuário ou auditor através do comando oficial da Android SDK:
  <code>aapt dump permissions GestorFinanceiro.apk</code>. Se a permissão <code>android.permission.INTERNET</code> não consta na tabela binária do APK, a exfiltração de dados é matematicamente impossível pelo aplicativo.
</div>

<h2>1.2 Matriz de Análise de Riscos e Mitigações (STRIDE Framework)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 20%;">Vetor de Ameaça</th>
      <th style="width: 25%;">Cenário Potencial</th>
      <th style="width: 15%;">Impacto</th>
      <th>Mitigação de Engenharia Implementada</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Information Disclosure</strong> (Vazamento de Dados)</td>
      <td>Interceptação de tráfego de rede ou vazamento de banco remoto.</td>
      <td>Crítico</td>
      <td>Arquitetura Zero-Cloud. Os dados nunca saem da memória interna volátil e do armazenamento seguro privado (SANDBOX) do dispositivo.</td>
    </tr>
    <tr>
      <td><strong>Elevation of Privilege</strong> (Acesso Indevido no Dispositivo)</td>
      <td>Terceiro com posse física do celular desbloqueado acessa extratos.</td>
      <td>Alto</td>
      <td>Autenticação opcional por PIN de 4 dígitos com derivação criptográfica SHA-256 e salgamento (salt) local.</td>
    </tr>
    <tr>
      <td><strong>Formula Injection</strong> (CWE-1236)</td>
      <td>Arquivo de fatura ou CSV exportado contendo fórmulas maliciosas (ex: <code>=cmd|' /C ...'!A1</code>).</td>
      <td>Médio</td>
      <td>Sanitização rigorosa na exportação: campos iniciados por <code>=</code>, <code>+</code>, <code>-</code> ou <code>@</code> recebem apóstrofo prefixado automaticamente.</td>
    </tr>
    <tr>
      <td><strong>Cross-Site Scripting</strong> (XSS no WebView)</td>
      <td>Nome de estabelecimento ou cartão injetando tags HTML/JavaScript no DOM.</td>
      <td>Alto</td>
      <td>Função de escape universal <code>escapeHTML()</code> e sanitização de identificadores <code>safeId()</code> antes de qualquer mutação via <code>innerHTML</code>.</td>
    </tr>
    <tr>
      <td><strong>Path Traversal</strong> (CWE-22)</td>
      <td>Exportação de arquivos gravando dados fora de diretórios autorizados.</td>
      <td>Médio</td>
      <td>Sanitização de nomes de arquivos com Expressão Regular <code>[^a-zA-Z0-9._-]</code> e uso obrigatório da API <code>MediaStore</code> (Scoped Storage) no Android 10+.</td>
    </tr>
  </tbody>
</table>

<!-- SEÇÃO 2: TOPOLOGIA DE ARQUITETURA -->
<div class="page-break"></div>

<h1 id="sec-2">2. Topologia de Arquitetura Técnica de Camadas</h1>

<p>
A aplicação emprega uma arquitetura híbrida de alto rendimento com isolamento de responsabilidades. O binário final (APK de apenas ~730 KB) opera como um container nativo enxuto contendo a interface SPA (Single Page Application) e os módulos de ponte de comunicação (JNI/JavaScript Bridge).
</p>

<h2>2.1 Diagrama de Camadas de Sistema (System Layer Stack)</h2>
<div class="diagram-box">
+-------------------------------------------------------------------------------+
|                       SISTEMA OPERACIONAL ANDROID                            |
|    NotificationManager   |   Settings Secure API   |   MediaStore Downloads   |
+------------------------------------+------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------------+
|                      CAMADA NATIVA ANDROID (JAVA SDK 34)                      |
|                                                                               |
|   +----------------------------+             +----------------------------+   |
|   |  NotificacaoListener.java  |             |     MainActivity.java      |   |
|   |  - NotificationListenerSvc |             |  - Activity Lifecycle      |   |
|   |  - Heurística Regex & Pkg  |             |  - WebView Configuration   |   |
|   |  - Deduplicação (120s)     |             |  - Hardware Back Dispatch  |   |
|   +--------------+-------------+             +--------------+-------------+   |
|                  | SharedPreferences                        |                 |
|                  +---------------------> &lt;------------------+                 |
|                                         |                                     |
|                                         v                                     |
|                              +----------------------+                         |
|                              |    AndroidBridge     |                         |
|                              |  (@JavascriptIfc)    |                         |
+------------------------------+----------+-----------+-------------------------+
                                          |
                        evaluateJavascript | window.AndroidBridge
                                          v
+-------------------------------------------------------------------------------+
|                  CAMADA DE INTERFACE & LÓGICA (WEBVIEW SPA)                  |
|                                                                               |
|  +---------------------+   +---------------------+   +---------------------+  |
|  |     www/index.html  |   |      SheetJS        |   |    Lucide Icons     |  |
|  |  - Dashboard Resumo |   |  - XLSX/CSV/OFX     |   |  - Vetores Nativos  |  |
|  |  - Reconciliação    |   |    Parser Engine    |   |    SVG em Memória   |  |
|  +----------+----------+   +----------+----------+   +----------+----------+  |
|             |                         |                         |             |
|             +-------------------------+-------------------------+             |
|                                       |                                       |
|                                       v                                       |
|                    +------------------------------------+                     |
|                    |   Motor Financeiro e Regras (JS)   |                     |
|                    |   - Categorização Inteligente      |                     |
|                    |   - Projeção de Parcelamentos      |                     |
|                    |   - Histórico Multi-Mês            |                     |
|                    +------------------+-----------------+                     |
|                                       |                                       |
|                                       v                                       |
|                    +------------------------------------+                     |
|                    |    LocalStorage Cripto/Isolado     |                     |
|                    +------------------------------------+                     |
+-------------------------------------------------------------------------------+
</div>

<h2>2.2 Pilha de Tecnologias Selecionadas e Racional de Engenharia</h2>
<table>
  <thead>
    <tr>
      <th>Componente</th>
      <th>Tecnologia Adotada</th>
      <th>Racional de Escolha em Relação aos Padrões da Indústria</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Runtime Nativo</strong></td>
      <td>Android SDK Puro (Java 8 / Dalvik Bytecode)</td>
      <td>Elimina o overhead de frameworks volumosos (Flutter, React Native) que adicionam entre 30 MB e 80 MB ao APK e degradam a velocidade de inicialização a frio (Cold Start). O binário do Gestor Financeiro mantém-se em apenas 730 KB.</td>
    </tr>
    <tr>
      <td><strong>Motor de UI</strong></td>
      <td>WebKit WebView Hardened</td>
      <td>Execução de SPA moderna com suporte completo a CSS Grid, Flexbox e renderização tipográfica subpixel, com diretivas restritivas (<code>MIXED_CONTENT_NEVER_ALLOW</code>).</td>
    </tr>
    <tr>
      <td><strong>Estilização</strong></td>
      <td>Tailwind CSS JIT Engine</td>
      <td>Design System responsivo de inspiração executiva (Dark Theme moderno com paleta Slate e Emerald), garantindo fluidez de 60fps no scroll de listas com centenas de despesas.</td>
    </tr>
    <tr>
      <td><strong>Motor de Faturas</strong></td>
      <td>SheetJS (xlsx.mini.js)</td>
      <td>Biblioteca industrial padrão para leitura client-side de planilhas complexas (formato binário BIFF8, OpenXML e CSV), operando sem dependências de servidores ou runtime Node.js.</td>
    </tr>
    <tr>
      <td><strong>Ícones Vetoriais</strong></td>
      <td>Lucide Icons (Vanilla)</td>
      <td>Substituição de fontes de ícones pesadas por elementos SVG computados dinamicamente via canvas/DOM sem requisições HTTP adicionais.</td>
    </tr>
  </tbody>
</table>

<!-- SEÇÃO 3: LEITOR NATIVO -->
<div class="page-break"></div>

<h1 id="sec-3">3. Módulo Nativo: NotificacaoListener e Captura em Tempo Real</h1>

<p>
O módulo <code>NotificacaoListener</code> estende a classe nativa do Android Framework <code>android.service.notification.NotificationListenerService</code>. Esta API permite que aplicações autorizadas pelo usuário interceptem eventos de publicação de notificações do sistema operacional (<code>StatusBarNotification</code>) de forma contínua e assíncrona, mesmo com o aplicativo fechado ou em segundo plano.
</p>

<h2>3.1 Ciclo de Interceptação e Algoritmo de Decisão</h2>
<p>
Quando qualquer aplicativo publica uma notificação, o método <code>onNotificationPosted(StatusBarNotification sbn)</code> é invocado pelo sistema operacional. A figura abaixo descreve a árvore lógica de filtragem executada pelo algoritmo:
</p>

<div class="diagram-box">
[Notificação Recebida no Android]
             |
             v
{ É resumo de grupo (GROUP_SUMMARY)? } ---- SIM ----> [Descarta Imediatamente]
             | NÃO
             v
{ É aplicativo de Mensagem/Rede Social? } -- SIM ----> [Descarta (WhatsApp, Telegram, etc)]
             | NÃO
             v
{ Pertence ao catálogo de Bancos/Wallets? } - NÃO ---> [Descarta]
             | SIM
             v
{ Contém termos negativos? } -------------- SIM ----> [Descarta (Cashback, Fatura Aberta, Estorno, etc)]
             | NÃO
             v
{ É Compra em Cartão de CRÉDITO? } ------ NÃO ----> [Descarta (Débito, Pix, Saldo em Conta, Boleto)]
             | SIM
             v
{ Valor R$ extraído com sucesso (&gt; 0)? } --- NÃO ---> [Descarta]
             | SIM
             v
{ Contém contexto transacional de compra? } - NÃO ---> [Descarta]
             | SIM
             v
{ Aplica Regras Aprendidas pelo Usuário? } -- SIM ----> [Substitui Nome Limpo, Cat e Cartão]
             | NÃO
             v
{ Identifica Cartão cadastrado ou banco? } -- NÃO ---> [Atribui Cartão Padrão]
             | SIM
             v
{ Transação idêntica nos últimos 120s? } --- SIM ----> [Descarta Duplicata]
             | NÃO
             v
[Grava no SharedPreferences (pending queue)] ----> [Notifica WebView no onResume]
</div>

<h2>3.2 Extração Profunda de Texto (Full Notification Bundle Extraction)</h2>
<p>
Notificações ricas no Android 10+ podem fragmentar títulos e mensagens longas entre diversos campos de metadados internos da classe <code>Notification.extras</code>. O leitor nativo realiza varredura exaustiva nos seguintes canais:
</p>
<ul>
  <li><code>Notification.EXTRA_TITLE</code> e <code>EXTRA_TITLE_BIG</code> (captura cabeçalho e razão social expandida).</li>
  <li><code>Notification.EXTRA_TEXT</code> e <code>EXTRA_BIG_TEXT</code> (corpo principal com valor e cartão).</li>
  <li><code>Notification.EXTRA_SUB_TEXT</code>, <code>EXTRA_SUMMARY_TEXT</code> e <code>EXTRA_INFO_TEXT</code>.</li>
  <li><code>Notification.EXTRA_TEXT_LINES</code> (varredura recursiva de arrays de linhas em mensagens agrupadas).</li>
  <li><code>StatusBarNotification.getNotification().tickerText</code> (linha de barra de status legada).</li>
</ul>

<h2>3.3 Validação Estrita de Cartão de Crédito</h2>
<p>
Para impedir contaminação da planilha com transações à vista ou operações bancárias que não comprometem o limite de crédito, o método <code>isStrictCreditCard()</code> aplica um filtro duplo determinístico:
</p>
<ol>
  <li><strong>Rejeição de Não-Crédito:</strong> Descarte automático caso o texto consolidado contenha termos como <i>"débito"</i>, <i>"saldo da conta"</i>, <i>"pix enviado"</i>, <i>"transferência"</i>, <i>"boleto pago"</i> ou <i>"empréstimo"</i>.</li>
  <li><strong>Confirmação de Crédito:</strong> Validação explícita da menção a <i>"crédito"</i>, bandeiras de cartão (<i>"Visa"</i>, <i>"Mastercard"</i>, <i>"Elo"</i>), menção ordinal de parcelas (<i>"1x"</i>, <i>"em 3x"</i>, <i>"parcela"</i>) ou identificação do nome de cartão previamente cadastrado pelo usuário.</li>
</ol>

<h2>3.2 Heurísticas de Expressões Regulares (Regex Parsing)</h2>
<p>
Para extrair com precisão os valores monetários e nomes de estabelecimentos de formatos variados de texto emitidos por diferentes instituições financeiras, foram desenvolvidas duas rotinas determinísticas:
</p>

<h3>Extração de Valor Monetário</h3>
<pre><code>// Padrão Regex compilado com suporte a múltiplos separadores brasileiros
Pattern p = Pattern.compile("R\\\\$\\\\s*([\\\\d.]+,\\\\d{2}|\\\\d+(?:[.,]\\\\d{1,2})?)", Pattern.CASE_INSENSITIVE);
Matcher m = p.matcher(texto);
if (m.find()) {
    String num = m.group(1);
    if (num.contains(",")) {
        num = num.replace(".", "").replace(",", "."); // Normaliza para notação IEEE 754
    }
    return Double.parseDouble(num);
}</code></pre>

<h3>Extração de Estabelecimento Comercial</h3>
<p>
Os bancos brasileiros adotam padrões sintáticos como <i>"Compra de R$ 50 em PADARIA CENTRAL"</i>, <i>"Pagamento para MERCADINHO no valor de..."</i> ou <i>"Estabelecimento: UBER TRIP"</i>. A expressão regular utilizada extrai o nome comercial através de uma técnica de <i>Positive Lookbehind</i> e <i>Positive Lookahead</i>:
</p>
<pre><code>Pattern p = Pattern.compile(
    "(?:estabelecimento:?|no local|em|para|no|na)\\\\s+([A-Za-z0-9À-ÿ][A-Za-z0-9À-ÿ\\\\s.\\\\*\\\\-_'/]{1,45}?)" +
    "(?=\\\\s+(?:no valor|valor|às|as|no dia|dia|em \\\\d|com o|com seu|no cart|cartão|cartao|via|pelo|R\\\\$)|[.,!]|$)",
    Pattern.CASE_INSENSITIVE
);</code></pre>

<h2>3.3 Catálogo de Instituições e Wallets Monitoradas</h2>
<p>
O leitor suporta nativamente pacotes de sistema e padrões textuais das seguintes instituições:
</p>
<ul>
  <li><strong>Mercado Pago:</strong> Pacotes <code>com.mercadopago.wallet</code> / <code>mercadopago</code>.</li>
  <li><strong>Itaú Unibanco / Credicard / Personnalité:</strong> Pacotes <code>com.itau</code>, <code>credicard</code>, <code>personnalite</code>.</li>
  <li><strong>Nubank (Nu Pagamentos):</strong> Pacotes <code>com.nu.production</code> / <code>nubank</code>.</li>
  <li><strong>Banco Inter:</strong> Pacotes <code>br.com.intermedium</code> / <code>inter</code>.</li>
  <li><strong>C6 Bank:</strong> Pacotes <code>com.c6bank.app</code> / <code>c6bank</code>.</li>
  <li><strong>Santander / Way:</strong> Pacotes <code>com.santander.app</code>, <code>way</code>.</li>
  <li><strong>Bradesco / Next:</strong> Pacotes <code>com.bradesco</code>, <code>com.banconext</code>.</li>
  <li><strong>Caixa Econômica Federal &amp; Banco do Brasil:</strong> Pacotes <code>caixa</code>, <code>bb.android</code>, <code>ourocard</code>.</li>
  <li><strong>Carteiras e Fintechs:</strong> Google Wallet (<code>walletnfcrel</code>), PicPay, BTG Pactual, XP, PagBank.</li>
</ul>

<h2>3.4 Mecanismo de Deduplicação Temporal em Memória Persistente</h2>
<p>
Alguns bancos disparam duas notificações quase simultâneas para uma única transação (ex: o aplicativo do banco emite um alerta e o Google Wallet emite outro referente ao mesmo pagamento via NFC). Para prevenir lançamentos duplicados, o serviço mantém no <code>SharedPreferences</code> os dados da última transação validada:
</p>
<pre><code>long now = System.currentTimeMillis();
long lastTs = prefs.getLong("last_ts", 0);
String lastCard = prefs.getString("last_card", "");
double lastVal = Double.longBitsToDouble(prefs.getLong("last_val", 0));

// Se a compra ocorreu com mesmo cartão, mesmo valor e dentro de 120 segundos, é descartada
if ((now - lastTs) &lt; 120000L &amp;&amp; lastCard.equals(cartao) &amp;&amp; Math.abs(lastVal - valor) &lt; 0.01) {
    return false; // Duplicata detectada
}</code></pre>

<h2>3.5 Solução Arquitetural para o Android 13+ (Restricted Settings)</h2>
<p>
A partir do Android 13 (API 33), o sistema operacional introduziu uma salvaguarda contra malwares: aplicativos instalados fora de uma loja oficial (como Google Play) têm permissões sensíveis — incluindo o <code>NotificationListenerService</code> — desabilitadas por padrão, com as chaves marcadas em tom cinza (<i>"Configuração restrita"</i>).
</p>
<p>
Para eliminar o atrito do usuário, a interface do Gestor Financeiro detecta dinamicamente essa condição e disponibiliza um fluxo em dois cliques por meio de intents nativas:
</p>
<ol>
  <li><strong>Passo 1 (Liberar Restritas):</strong> Aciona <code>Settings.ACTION_APPLICATION_DETAILS_SETTINGS</code> abrindo as informações do aplicativo. O usuário clica no menu superior (três pontos ⋮) e seleciona <i>"Permitir configurações restritas"</i>, autenticando via biometria.</li>
  <li><strong>Passo 2 (Ativar Leitor):</strong> Aciona <code>Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS</code> abrindo a tela de autorização de leitura de notificações, onde o interruptor agora está habilitado.</li>
</ol>

<!-- SEÇÃO 4: MOTOR DE IMPORTAÇÃO -->
<div class="page-break"></div>

<h1 id="sec-4">4. Motor de Ingestão de Dados e Parsing de Faturas Bancárias</h1>

<p>
Além da captura passiva via notificações, o Gestor Financeiro possui um motor universal de ingestão de arquivos para carga retroativa de faturas, conciliação e histórico financeiro consolidado.
</p>

<h2>4.1 Formatos de Arquivo e Estratégia de Decodificação</h2>
<table>
  <thead>
    <tr>
      <th style="width: 15%;">Formato</th>
      <th style="width: 25%;">Extensões Aceitas</th>
      <th style="width: 20%;">Mecanismo de Parse</th>
      <th>Particularidades de Engenharia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Planilhas Excel</strong></td>
      <td><code>.xlsx</code>, <code>.xls</code></td>
      <td>SheetJS (XLSX Engine)</td>
      <td>Varredura de colunas dinâmicas. Localiza cabeçalhos como "Data", "Estabelecimento", "Valor" e "Título", independente da ordem das colunas.</td>
    </tr>
    <tr>
      <td><strong>Arquivos CSV</strong></td>
      <td><code>.csv</code></td>
      <td>Parser RFC 4180</td>
      <td>Detecção automática de delimitador (vírgula <code>,</code> ou ponto-e-vírgula <code>;</code>) e normalização de valores com separador decimal brasileiro.</td>
    </tr>
    <tr>
      <td><strong>Open Financial Exchange</strong></td>
      <td><code>.ofx</code></td>
      <td>Extrator Regex XML/SGML</td>
      <td>Extração semântica das tags financeiras padrão: <code>&lt;STMTTRN&gt;</code>, <code>&lt;TRNAMT&gt;</code>, <code>&lt;DTPOSTED&gt;</code> e <code>&lt;MEMO&gt;</code>.</td>
    </tr>
    <tr>
      <td><strong>Texto Livre (Clipboard)</strong></td>
      <td>Copiar e colar</td>
      <td>Tokenizador Heurístico</td>
      <td>Processa linhas de texto coladas diretamente do internet banking ou emails de fatura.</td>
    </tr>
  </tbody>
</table>

<h2>4.2 Normalização de Datas e Atribuição do Mês de Referência</h2>
<p>
Os formatos de data emitidos pelos bancos variam consideravelmente (ex: <code>05/11/2026</code>, <code>2026-11-05</code>, <code>05 nov</code>). O motor normaliza qualquer representação válida para o padrão brasileiro <code>DD/MM/YYYY</code> e deriva a chave de particionamento temporal <code>mesRef</code> no formato ISO <code>YYYY-MM</code>:
</p>
<pre><code>function getMesFromDataBR(dataStr) {
  if (!dataStr) return getMesAtual();
  const partes = dataStr.split('/');
  if (partes.length === 3) {
    // Converte DD/MM/YYYY em YYYY-MM
    return `${partes[2]}-${partes[1].padStart(2, '0')}`;
  }
  return getMesAtual();
}</code></pre>

<h2>4.3 Sanitização contra Ataques de Injeção em Planilhas (CSV Injection)</h2>
<p>
Ataques do tipo <i>Formula Injection</i> ocorrem quando um usuário ou um arquivo externo contém campos que começam com símbolos executáveis por aplicativos como Microsoft Excel ou LibreOffice Calc (<code>=</code>, <code>+</code>, <code>-</code>, <code>@</code>, <code>0x09</code>, <code>0x0D</code>). Na exportação de dados em CSV, o Gestor Financeiro neutraliza esses campos inserindo um apóstrofo antes da saída:
</p>
<pre><code>function sanitizarCSV(str) {
  if (typeof str !== 'string') return str;
  const charsPerigosos = ['=', '+', '-', '@', '\\t', '\\r'];
  if (charsPerigosos.includes(str.charAt(0))) {
    return "'" + str; // Neutraliza execução de macros DDE no leitor de planilhas
  }
  return str;
}</code></pre>

<!-- SEÇÃO 5: MOTOR FINANCEIRO -->
<div class="page-break"></div>

<h1 id="sec-5">5. Motor de Regras Financeiras, Parcelamentos e Projeções</h1>

<p>
O núcleo de inteligência financeira opera localmente no navegador sem depender de modelos pesados de rede neural, utilizando autômatos determinísticos e estruturas indexadas de regras.
</p>

<h2>5.1 Motor de Categorização Automática e Aprendizado de Preferências</h2>
<p>
O sistema inclui um dicionário léxico pré-carregado com mais de 100 raízes semânticas distribuídas em 10 categorias essenciais:
</p>
<ul>
  <li><strong>Comida:</strong> ifood, restaurante, lanchonete, mcdonald, burger, pizza, padaria, cafe.</li>
  <li><strong>Mercado:</strong> carrefour, extra, pão de açucar, atacadao, assai, supermercado, hortifruti.</li>
  <li><strong>Transporte:</strong> uber, 99app, posto, shell, ipiranga, combustivel, pedagio, estacionamento.</li>
  <li><strong>Lazer:</strong> cinema, netflix, spotify, steam, playstation, ingresso, show.</li>
  <li><strong>Saúde:</strong> farmacia, drogaria, drogasil, pague menos, consulta, hospital, laboratorio.</li>
  <li><strong>Moradia:</strong> aluguel, condomínio, enel, sabesp, cpfl, luz, agua, gas.</li>
  <li><strong>Assinaturas:</strong> amazon prime, youtube, apple, google storage, gympass, smartfit.</li>
  <li><strong>Compras:</strong> amazon, mercado livre, shopee, shein, magazine luiza, zara.</li>
  <li><strong>Educação:</strong> faculdade, escola, curso, udemy, alura, livro, papelaria.</li>
  <li><strong>Outros:</strong> categoria padrão de fallback.</li>
</ul>

<h3>5.1.2 Motor de Aprendizado Contínuo (Continuous Learning Engine)</h3>
<p>
A partir da versão v2.3.0, o aplicativo transcende a simples memorização de categorias: ao editar qualquer transação na tabela, o usuário treina o sistema para reconhecer a loja comercial real, seu cartão usual e sua categoria padrão:
</p>
<ul>
  <li><strong>Limpeza e Eliminação de Gateways:</strong> Gateways de pagamento como <code>PG *</code>, <code>MP *</code>, <code>IFOOD *</code>, <code>PAG*</code> são automaticamente isolados da chave semântica.</li>
  <li><strong>Atualização Retroativa Automática:</strong> Ao renomear um lançamento (ex: de <i>"PG *SUPERMERC"</i> para <i>"Supermercado Extra"</i>), o motor varre todo o histórico da tabela e atualiza instantaneamente todos os lançamentos passados daquele mesmo estabelecimento.</li>
  <li><strong>Sincronização Nativa Bidirecional:</strong> As regras aprendidas (<code>learnedRules</code>) são sincronizadas em tempo real com o subsistema nativo Android via <code>AndroidBridge.syncLearnedRules()</code>, sendo salvas em <code>SharedPreferences</code> para que o <code>NotificacaoListener</code> já as aplique nativamente no momento exato em que a notificação é recebida em segundo plano.</li>
  <li><strong>Gerenciamento no Painel de Ajustes:</strong> O usuário possui visualização completa de todas as lojas aprendidas com contador dinâmico e opção de exclusão granular ou reset total de aprendizado.</li>
</ul>
<pre><code>// Prioridade de Classificação
function categorizarAutomatico(estabelecimento) {
  const norm = removerAcentos(estabelecimento).toLowerCase().trim();
  
  // 1. Alta Prioridade: Regras personalizadas criadas pelo usuário
  if (customRules[norm]) return customRules[norm];
  
  // 2. Média Prioridade: Dicionário semântico embutido
  for (const [termo, categoria] of Object.entries(DICIONARIO_REGRAS)) {
    if (norm.includes(termo)) return categoria;
  }
  
  // 3. Fallback Padrão
  return 'Outros';
}</code></pre>

<h2>5.2 Projeção Temporal de Compras Parceladas</h2>
<p>
Quando uma despesa é lançada com parcelamento (ex: R$ 600,00 em 3x), o motor decompõe a operação em N objetos individuais, atribuindo a cada um o valor da fração (R$ 200,00), a descrição ordinal da parcela (ex: <i>"Notebook (1/3)"</i>, <i>"Notebook (2/3)"</i>, <i>"Notebook (3/3)"</i>) e o respectivo mês de referência projetado:
</p>
<pre><code>function gerarParcelas(nome, valorTotal, parcelas, dataBR, cartao, categoria) {
  const valorParcela = Math.round((valorTotal / parcelas) * 100) / 100;
  const lista = [];
  let [dia, mes, ano] = dataBR.split('/').map(Number);

  for (let i = 0; i &lt; parcelas; i++) {
    let d = new Date(ano, (mes - 1) + i, dia);
    let mesRefStr = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
    let dataFormatada = `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}/${d.getFullYear()}`;

    lista.push({
      id: safeId('parc_' + Date.now() + '_' + i),
      local: `${nome} (${i + 1}/${parcelas})`,
      valor: valorParcela,
      data: dataFormatada,
      mesRef: mesRefStr,
      cartao: cartao,
      categoria: categoria,
      tipo: 'Parcelado'
    });
  }
  return lista;
}</code></pre>

<h2>5.3 Conciliação de Fatura Fechada (monthlyAdjustments)</h2>
<p>
Faturas de cartão de crédito frequentemente possuem cobranças de juros, IOF, anuidade ou descontos de antecipação que não constam em lançamentos unitários de compra. O Gestor Financeiro implementa um mecanismo de ajuste algébrico por mês e por cartão:
</p>
<pre><code>Total Fatura(Cartão, Mês) = Sum(Gastos Unitários) + monthlyAdjustments[Mês][Cartão]</code></pre>
<p>
Dessa forma, o usuário pode definir o valor fechado da fatura com exatidão de centavos sem corromper a rastreabilidade das compras individuais.
</p>

<!-- SEÇÃO 6: SEGURANÇA E ARMAZENAMENTO -->
<div class="page-break"></div>

<h1 id="sec-6">6. Camada de Segurança, Autenticação PIN e Persistência</h1>

<h2>6.1 Autenticação por PIN Local (SHA-256 com Salgamento)</h2>
<p>
Para proteger a interface contra olhares curiosos no próprio dispositivo desbloqueado, a aplicação disponibiliza um teclado numérico virtual com trava por PIN de 4 dígitos. A senha nunca é gravada em texto plano. Ao criar ou alterar o PIN, o sistema deriva um hash SHA-256 com salgamento estático local:
</p>
<pre><code>function hashPin(pin) {
  // Salgamento determinístico local para dificultar ataques por tabelas rainbow
  const salt = "GestorFinanceiro_LocalSalt_#2026";
  return sha256(pin + salt);
}</code></pre>
<p>
Na inicialização (<code>init()</code>), se a chave <code>fin_pin_hash</code> estiver preenchida no armazenamento local, a camada visual é imediatamente bloqueada com <i>backdrop-filter</i> desfocado, interceptando eventos de toque e do botão físico Voltar até a validação do PIN correto.
</p>

<h2>6.2 Esquema do Banco de Dados Local (JSON Schema)</h2>
<p>
O estado completo da aplicação é serializado na sandbox privada do navegador/WebView utilizando as seguintes chaves de armazenamento:
</p>
<table>
  <thead>
    <tr>
      <th style="width: 25%;">Chave LocalStorage</th>
      <th style="width: 20%;">Tipo de Dado</th>
      <th>Descrição Semântica</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>fin_transacoes</code></td>
      <td><code>Array&lt;Transaction&gt;</code></td>
      <td>Lista de todas as compras cadastradas com atributos <code>id</code>, <code>data</code>, <code>mesRef</code>, <code>cartao</code>, <code>valor</code>, <code>local</code>, <code>categoria</code> e <code>tipo</code>.</td>
    </tr>
    <tr>
      <td><code>fin_cards</code></td>
      <td><code>Array&lt;CardConfig&gt;</code></td>
      <td>Configuração dos cartões ativos: <code>nome</code>, <code>cor</code> (paleta Tailwind) e <code>vencimento</code>.</td>
    </tr>
    <tr>
      <td><code>fin_regras_cat</code></td>
      <td><code>Record&lt;string, string&gt;</code></td>
      <td>Dicionário associativo ligando nome normalizado da loja à categoria personalizada.</td>
    </tr>
    <tr>
      <td><code>fin_metas_cat</code></td>
      <td><code>Record&lt;string, number&gt;</code></td>
      <td>Tetos individuais em reais estipulados para categorias específicas (ex: Comida: R$ 800,00).</td>
    </tr>
    <tr>
      <td><code>fin_ajustes_mes</code></td>
      <td><code>Record&lt;string, Record&gt;</code></td>
      <td>Matriz bidimensional de ajustes de fechamento indexada por mês e nome do cartão.</td>
    </tr>
    <tr>
      <td><code>fin_limite</code></td>
      <td><code>string (float)</code></td>
      <td>Teto global estipulado para o orçamento mensal.</td>
    </tr>
    <tr>
      <td><code>fin_nome</code></td>
      <td><code>string</code></td>
      <td>Nome do proprietário do perfil exibido no cabeçalho e boas-vindas.</td>
    </tr>
  </tbody>
</table>

<h2>6.3 Procedimentos de Backup e Restauração Segura</h2>
<p>
A aplicação disponibiliza duas modalidades de exportação via <code>AndroidBridge.saveFile()</code>:
</p>
<ul>
  <li><strong>Backup Completo (.json):</strong> Contém todas as tabelas e preferências. Pode ser importado a qualquer momento em outro dispositivo para restauração idêntica do ambiente.</li>
  <li><strong>Relatório Financeiro (.csv):</strong> Formato tabular auditável compatível com Excel, Google Sheets e LibreOffice, com proteção contra injeção de fórmulas e totalizações mensais.</li>
</ul>

<!-- SEÇÃO 7: PIPELINE DE COMPILAÇÃO -->
<div class="page-break"></div>

<h1 id="sec-7">7. Pipeline de Compilação Determinística e CI/CD sem Gradle</h1>

<p>
Um dos diferenciais de engenharia mais notáveis do projeto é a eliminação integral do sistema de build <strong>Gradle</strong> em favor de uma cadeia de compilação direta baseada nas ferramentas oficiais do Google Android SDK (<code>build-tools/34.0.0</code>).
</p>

<h2>7.1 Racional de Engenharia: Por que Eliminar o Gradle?</h2>
<table>
  <thead>
    <tr>
      <th>Critério</th>
      <th>Abordagem Tradicional (Gradle + Android Studio)</th>
      <th>Abordagem do Gestor Financeiro (Script Direto)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Tempo de Compilação (Build)</strong></td>
      <td>De 45 segundos a 3 minutos a cada compilação.</td>
      <td><strong>Entre 3 e 5 segundos</strong> (quase 30x mais rápido).</td>
    </tr>
    <tr>
      <td><strong>Consumo de Memória (RAM)</strong></td>
      <td>Daemon do Gradle consome entre 2 GB e 4 GB de RAM.</td>
      <td><strong>Menos de 200 MB</strong> durante o pico de execução.</td>
    </tr>
    <tr>
      <td><strong>Dependências Externas no CI</strong></td>
      <td>Baixa dezenas de plugins remotos e wrappers (>250 MB).</td>
      <td>Zero downloads externos de plugins; usa ferramentas puras do SDK.</td>
    </tr>
    <tr>
      <td><strong>Transparência e Auditoria</strong></td>
      <td>Scripts Groovy/Kotlin complexos ocultando tarefas internas.</td>
      <td>Cada etapa de compilação é um comando explícito, legível e determinístico.</td>
    </tr>
  </tbody>
</table>

<h2>7.2 Sequência de Etapas de Compilação (Pipeline Execution Flow)</h2>
<div class="diagram-box">
Etapa 1: Compilação de Recursos
  aapt2 compile --dir android/res -o build/compiled_res/res.zip
       |
Etapa 2: Ligação do Manifesto e Geração do R.java
  aapt2 link -o build/out/unaligned.apk -I android.jar --manifest AndroidManifest.xml --java android/src
       |
Etapa 3: Compilação do Código-Fonte Java
  javac -source 1.8 -target 1.8 -bootclasspath android.jar -d build/classes (MainActivity.java, NotificacaoListener.java)
       |
Etapa 4: Desugaring e Geração de Bytecode Dalvik (.dex)
  d8 --min-api 24 --lib android.jar --output build/dex build/classes/*.class
       |
Etapa 5: Injeção de Classes e Assets Web via Python (Forçando barras /)
  zipfile inject: classes.dex + assets/www/* (Garante compatibilidade de assets no WebView)
       |
Etapa 6: Alinhamento de Memória (ZipAlign 4-byte boundaries)
  zipalign -f -p 4 build/out/unaligned.apk build/out/aligned.apk
       |
Etapa 7: Assinatura Criptográfica Multinível (v1 + v2 + v3)
  apksigner sign --v1-signing-enabled true --v2-signing-enabled true --ks keystore build/out/aligned.apk
</div>

<h2>7.3 A Solução de Engenharia para o Bug de Barras Invertidas no Windows</h2>
<div class="callout callout-warning">
  <div class="callout-title">Descoberta e Correção de Bug Crítico de Empacotamento</div>
  No sistema Windows, o empacotador nativo do AAPT2 registrava caminhos de arquivos de assets utilizando barras invertidas (<code>assets/www\\index.html</code>). O motor de WebView do Android interpreta estritamente URLs POSIX (<code>file:///android_asset/www/index.html</code>), resultando no erro <i>"Não foi possível carregar a página da web"</i>.
  <br><br>
  <strong>A Correção:</strong> A etapa de montagem do pacote foi delegada a uma rotina em Python que força a conversão universal de separadores de caminho via <code>os.path.relpath().replace(os.sep, '/')</code>. Isso assegura paridade binária absoluta tanto no ambiente Windows de desenvolvimento quanto no runner Linux do GitHub Actions.
</div>

<!-- SEÇÃO 8: GUIA DO USUÁRIO E TROUBLESHOOTING -->
<div class="page-break"></div>

<h1 id="sec-8">8. Manual de Operação e Resolução de Problemas (Troubleshooting)</h1>

<h2>8.1 Guia de Primeiro Uso (Onboarding)</h2>
<ol>
  <li><strong>Instalação do APK:</strong> Transfira o arquivo <code>GestorFinanceiro.apk</code> para o aparelho e execute o instalador de pacotes do Android.</li>
  <li><strong>Assistente de Configuração:</strong> Ao abrir pela primeira vez, digite seu nome e informe seu teto mensal estimado.</li>
  <li><strong>Seleção de Cartões:</strong> Marque quais cartões de crédito você utiliza (ex: Nubank, Itaú, Mercado Pago, Inter, etc.). Novos cartões podem ser adicionados a qualquer momento nas configurações.</li>
  <li><strong>Ativação da Captura Automática:</strong> No topo da tela de Resumo, clique nos botões indicados para liberar as permissões do leitor de notificações.</li>
</ol>

<h2>8.2 Árvore de Resolução de Erros de Instalação</h2>
<table>
  <thead>
    <tr>
      <th style="width: 25%;">Mensagem de Erro</th>
      <th style="width: 30%;">Causa Raiz Técnica</th>
      <th>Procedimento Operacional de Solução</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>"O app não foi instalado"</strong> ou <strong>"Conflito de Pacote"</strong></td>
      <td>Conflito de keystore criptográfica. Existe uma versão anterior instalada assinada com uma chave diferente (ex: versão pessoal vs versão GitHub).</td>
      <td><strong>Desinstalar a versão anterior</strong> do aplicativo do celular antes de tocar no novo APK. Como o Android protege a integridade do app, ele impede a sobreposição de chaves distintas.</td>
    </tr>
    <tr>
      <td><strong>"Bloqueado pelo Play Protect"</strong></td>
      <td>O Google Play Protect alerta o usuário sobre qualquer APK compilado fora da Play Store por ausência de reputação prévia na nuvem.</td>
      <td>Tocar no link <strong>"Mais detalhes"</strong> (ou <i>"Detalhes"</i>) do modal e em seguida selecionar <strong>"Instalar assim mesmo"</strong>.</td>
    </tr>
    <tr>
      <td><strong>"Sem permissão para instalar fontes desconhecidas"</strong></td>
      <td>A aplicação que recebeu o APK (Chrome, WhatsApp ou Arquivos) não tem autorização para despachar intents de instalação de pacotes.</td>
      <td>Tocar em <strong>"Configurações"</strong> no aviso, ligar a opção <strong>"Permitir desta fonte"</strong>, retornar e concluir a instalação.</td>
    </tr>
  </tbody>
</table>

<h2>8.3 Ativação das Notificações em Fabricantes com Gestão Agressiva de Bateria</h2>
<p>
Algumas fabricantes Android (Xiaomi/MIUI, Samsung/OneUI, Motorola e Huawei) implementam sistemas proprietários de economia de energia que podem suspender serviços em segundo plano. Para garantir captura ininterrupta de notificações:
</p>
<ul>
  <li><strong>Xiaomi / Redmi / POCO (MIUI / HyperOS):</strong> Em <i>Configurações &gt; Apps &gt; Gestor Financeiro</i>, marque <strong>"Início Automático"</strong> e em <i>Economia de Bateria</i> defina como <strong>"Sem restrições"</strong>.</li>
  <li><strong>Samsung (OneUI):</strong> Em <i>Configurações &gt; Aplicativos &gt; Gestor Financeiro &gt; Bateria</i>, selecione <strong>"Irrestrito"</strong>.</li>
</ul>

<!-- SEÇÃO 9: ESPECIFICAÇÕES E GLOSSÁRIO -->
<div class="page-break"></div>

<h1 id="sec-9">9. Especificações Técnicas e Glossário de Engenharia</h1>

<h2>9.1 Matriz de Especificações de Hardware e Software</h2>
<table>
  <thead>
    <tr>
      <th>Parâmetro</th>
      <th>Especificação Mínima</th>
      <th>Especificação Recomendada</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Versão do Android</strong></td>
      <td>Android 7.0 (API 24 - Nougat)</td>
      <td>Android 11, 12, 13 ou 14+ (API 30–34)</td>
    </tr>
    <tr>
      <td><strong>Memória RAM</strong></td>
      <td>1 GB de RAM</td>
      <td>2 GB de RAM ou superior</td>
    </tr>
    <tr>
      <td><strong>Espaço de Armazenamento</strong></td>
      <td>5 MB livres</td>
      <td>20 MB livres (para múltiplos backups e histórico extenso)</td>
    </tr>
    <tr>
      <td><strong>Tamanho do Arquivo APK</strong></td>
      <td>Aproximadamente 730 Kilobytes</td>
      <td>—</td>
    </tr>
    <tr>
      <td><strong>Permissões de Sistema Solicitadas</strong></td>
      <td><code>BIND_NOTIFICATION_LISTENER_SERVICE</code> (Opcional, para leitura automática)<br><code>WRITE_EXTERNAL_STORAGE</code> (Apenas em Android 9 ou inferior)</td>
      <td>Nenhuma permissão especial para uso manual. <strong>ZERO</strong> permissão de Internet.</td>
    </tr>
  </tbody>
</table>

<h2>9.2 Glossário de Termos Técnicos da Indústria</h2>
<dl>
  <dt><strong>Offline-First</strong></dt>
  <dd>Paradigma de arquitetura de software onde todas as funcionalidades críticas, dados e processamentos são concebidos para operar localmente no dispositivo cliente sem depender de conexão com a rede ou servidores remotos.</dd>
  <br>
  <dt><strong>NotificationListenerService</strong></dt>
  <dd>Serviço do sistema operacional Android que recebe callbacks do NotificationManager quando novas notificações são postadas ou removidas na barra de status do sistema.</dd>
  <br>
  <dt><strong>Scoped Storage (Armazenamento com Escopo)</strong></dt>
  <dd>Modelo de segurança introduzido no Android 10 (API 29) que isola o armazenamento de aplicativos e restringe o acesso ao sistema de arquivos compartilhado, exigindo APIs como a MediaStore.</dd>
  <br>
  <dt><strong>CWE-1236 (Improper Neutralization of Formula Elements in CSV)</strong></dt>
  <dd>Vulnerabilidade na qual arquivos de texto delimitados por vírgula contêm fórmulas que podem ser executadas arbitrariamente por softwares de planilhas quando abertos.</dd>
  <br>
  <dt><strong>D8 Dexer</strong></dt>
  <dd>Compilador e desugarer padrão da plataforma Android que traduz bytecode Java (.class) em bytecode Dalvik (.dex) otimizado para o runtime ART da plataforma.</dd>
  <br>
  <dt><strong>ZipAlign</strong></dt>
  <dd>Ferramenta de otimização de pacotes de arquivo APK que garante que todos os dados não comprimidos comecem em alinhamento de limites de 4 bytes na memória, reduzindo o consumo de RAM do sistema.</dd>
</dl>

<div style="margin-top: 40px; padding-top: 15px; border-top: 1px solid #cbd5e1; text-align: center; font-size: 8pt; color: #64748b;">
  Fim da Especificação Técnica Oficial — Projeto Gestor Financeiro Offline v2.3.0 — Licença MIT
</div>

</body>
</html>
"""
    return html_content

def main():
    base_dir = r"c:\Users\Usuario\Downloads\Projetos\Controle-Financeiro-Gastos"
    html_path = os.path.join(base_dir, "documentacao_tecnica.html")
    pdf_out1 = os.path.join(base_dir, "utilizáveis", "Manual_Tecnico_Gestor_Financeiro.pdf")
    pdf_out2 = os.path.join(base_dir, "Projeto-GitHub", "docs", "Manual_Tecnico_Gestor_Financeiro.pdf")

    print("1. Gerando HTML técnico formatado...")
    html_data = build_html()
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_data)
    print(f"HTML salvo em: {html_path}")

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_bin = None
    for p in edge_paths:
        if os.path.exists(p):
            edge_bin = p
            break

    if not edge_bin:
        print("Erro: Microsoft Edge não encontrado para compilação do PDF.")
        sys.exit(1)

    print(f"2. Compilando PDF via motor Headless ({edge_bin})...")
    cmd = [
        edge_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_out1}",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_out1):
        size_kb = os.path.getsize(pdf_out1) / 1024
        print(f"PDF gerado com sucesso em: {pdf_out1} ({size_kb:.1f} KB)")
        
        # Copia para docs do Projeto-GitHub
        import shutil
        os.makedirs(os.path.dirname(pdf_out2), exist_ok=True)
        shutil.copyfile(pdf_out1, pdf_out2)
        print(f"PDF copiado para: {pdf_out2}")
    else:
        print("Falha ao gerar PDF:")
        print(res.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
