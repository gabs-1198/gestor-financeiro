package com.gestorfinanceiro.app;

import android.app.Notification;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;

import org.json.JSONArray;
import org.json.JSONObject;

import java.text.Normalizer;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Iterator;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class NotificacaoListener extends NotificationListenerService {

    public static final String PREFS_NAME = "fin_notif_queue";
    public static final String KEY_PENDING = "pending";
    public static final String KEY_LOGS = "logs";
    public static final String KEY_KNOWN_CARDS = "known_cards";
    public static final String KEY_LEARNED_RULES = "learned_rules";

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        if (sbn == null || sbn.getNotification() == null) return;

        Notification notif = sbn.getNotification();
        if ((notif.flags & Notification.FLAG_GROUP_SUMMARY) != 0) return;

        String pkg = sbn.getPackageName() != null ? sbn.getPackageName().toLowerCase(Locale.ROOT) : "";

        // Ignorar mensageiros, redes sociais e navegadores
        if (pkg.contains("whatsapp") || pkg.contains("telegram") || pkg.contains("instagram")
                || pkg.contains("facebook") || pkg.contains("twitter") || pkg.contains("discord")
                || pkg.contains("youtube") || pkg.contains("tiktok")) {
            return;
        }

        // Reconhecer aplicativos bancários e carteiras digitais populares
        boolean isBankApp = pkg.contains("mercadopago")
                || pkg.contains("itau")
                || pkg.contains("credicard")
                || pkg.contains("nubank")
                || pkg.contains("intermedium")
                || pkg.contains("c6bank")
                || pkg.contains("santander")
                || pkg.contains("bradesco")
                || pkg.contains("caixa")
                || pkg.contains("bb.android")
                || pkg.contains("picpay")
                || pkg.contains("neon")
                || pkg.contains("btg")
                || pkg.contains("xp")
                || pkg.contains("pagseguro")
                || pkg.contains("pagbank")
                || pkg.contains("digio")
                || pkg.contains("next")
                || pkg.contains("walletnfcrel")
                || pkg.contains("wallet")
                || pkg.contains("bank")
                || pkg.contains("card");

        if (!isBankApp) return;

        Bundle extras = notif.extras;
        if (extras == null) return;

        // Leitura COMPLETA de todos os campos textuais da notificação
        String title = charSeqToStr(extras.getCharSequence(Notification.EXTRA_TITLE));
        String titleBig = charSeqToStr(extras.getCharSequence(Notification.EXTRA_TITLE_BIG));
        if (title.isEmpty()) title = titleBig;

        String text = charSeqToStr(extras.getCharSequence(Notification.EXTRA_TEXT));
        String bigText = charSeqToStr(extras.getCharSequence(Notification.EXTRA_BIG_TEXT));
        String subText = charSeqToStr(extras.getCharSequence(Notification.EXTRA_SUB_TEXT));
        String summaryText = charSeqToStr(extras.getCharSequence(Notification.EXTRA_SUMMARY_TEXT));
        String infoText = charSeqToStr(extras.getCharSequence(Notification.EXTRA_INFO_TEXT));
        String ticker = notif.tickerText != null ? charSeqToStr(notif.tickerText) : "";

        // TextLines (notificações estilo InboxStyle com múltiplas linhas)
        StringBuilder linesBuilder = new StringBuilder();
        CharSequence[] textLines = extras.getCharSequenceArray(Notification.EXTRA_TEXT_LINES);
        if (textLines != null) {
            for (CharSequence line : textLines) {
                if (line != null && line.length() > 0) {
                    linesBuilder.append(" ").append(line.toString().trim());
                }
            }
        }

        StringBuilder bodyBuilder = new StringBuilder();
        if (!bigText.isEmpty()) {
            bodyBuilder.append(bigText);
            if (!text.isEmpty() && !bigText.contains(text)) {
                bodyBuilder.append(" ").append(text);
            }
        } else if (!text.isEmpty()) {
            bodyBuilder.append(text);
        }
        if (!subText.isEmpty() && !bodyBuilder.toString().contains(subText)) {
            bodyBuilder.append(" ").append(subText);
        }
        if (!summaryText.isEmpty() && !bodyBuilder.toString().contains(summaryText)) {
            bodyBuilder.append(" ").append(summaryText);
        }
        if (!infoText.isEmpty() && !bodyBuilder.toString().contains(infoText)) {
            bodyBuilder.append(" ").append(infoText);
        }
        if (linesBuilder.length() > 0) {
            bodyBuilder.append(linesBuilder);
        }
        if (!ticker.isEmpty() && !bodyBuilder.toString().contains(ticker)) {
            bodyBuilder.append(" ").append(ticker);
        }

        String body = bodyBuilder.toString().trim();
        String fullText = (title + " " + body).trim();

        if (fullText.isEmpty()) return;

        processarNotificacao(getApplicationContext(), null, pkg, title, body, fullText);
    }

    private static String charSeqToStr(CharSequence cs) {
        return cs == null ? "" : cs.toString().trim();
    }

    public static String removerAcentos(String s) {
        if (s == null) return "";
        String norm = Normalizer.normalize(s, Normalizer.Form.NFD);
        return norm.replaceAll("[\\p{InCombiningDiacriticalMarks}]", "");
    }

    public static synchronized boolean processarNotificacao(Context ctx, String cartaoOverride, String pkg, String title, String body, String fullText) {
        String norm = removerAcentos(fullText).toLowerCase(Locale.ROOT);

        // 1. Filtrar avisos promocionais, informativos, faturas, rendimentos, códigos e estornos
        if (norm.contains("recebeu") || norm.contains("recebido") || norm.contains("recebida")
                || norm.contains("cashback") || norm.contains("rendeu") || norm.contains("rendimento")
                || norm.contains("aproveite") || norm.contains("oferta") || norm.contains("promocao")
                || norm.contains("fatura fechada") || norm.contains("fatura disponivel")
                || norm.contains("vence em") || norm.contains("vencimento da fatura") || norm.contains("pague sua fatura")
                || norm.contains("fatura paga") || norm.contains("pagamento de fatura")
                || norm.contains("lembrete") || norm.contains("codigo") || norm.contains("verificacao")
                || norm.contains("estorno") || norm.contains("cancelad") || norm.contains("recusad")
                || norm.contains("bloquead") || norm.contains("limite aumentado")) {
            registrarLog(ctx, pkg, title, body, "Descartado: Aviso não transacional / estorno / fatura");
            return false;
        }

        // 2. EXCLUIR DÉBITO, PIX, BOLETO E SALDO EM CONTA (Exigir estritamente CARTÃO DE CRÉDITO)
        boolean isExplicitDebit = norm.contains("debito")
                || norm.contains("no debito")
                || norm.contains("cartao de debito")
                || norm.contains("funcao debito")
                || norm.contains("debito em conta")
                || norm.contains("debitado da sua conta");

        boolean isPixOrTransfer = norm.contains("pix")
                || norm.contains("transferencia")
                || norm.contains("transferiu")
                || norm.contains("ted")
                || norm.contains("doc");

        boolean isBoleto = norm.contains("boleto")
                || norm.contains("pagamento de conta")
                || norm.contains("codigo de barras");

        boolean isSaldoConta = norm.contains("saldo da conta")
                || norm.contains("saldo em conta")
                || norm.contains("usando seu saldo")
                || norm.contains("com seu saldo");

        if (isExplicitDebit || isPixOrTransfer || isBoleto || isSaldoConta) {
            registrarLog(ctx, pkg, title, body, "Descartado: Não é crédito (detectado débito/pix/saldo)");
            return false;
        }

        // 3. Exigir valor monetário em R$
        double valor = extrairValor(fullText);
        if (valor <= 0.0 || valor > 500000.0) {
            registrarLog(ctx, pkg, title, body, "Descartado: Valor em R$ não encontrado ou inválido");
            return false;
        }

        // 4. Exigir contexto de compra/pagamento
        boolean hasPurchaseContext = norm.contains("compra")
                || norm.contains("aprovad")
                || norm.contains("pagou")
                || norm.contains("pagamento")
                || norm.contains("gastou")
                || norm.contains("passou")
                || norm.contains("autorizad")
                || norm.contains("realizad")
                || norm.contains("estabelecimento");

        if (!hasPurchaseContext) {
            registrarLog(ctx, pkg, title, body, "Descartado: Sem contexto de compra");
            return false;
        }

        // 5. Validação de Crédito / Cartão
        boolean mentionsCredit = norm.contains("credito")
                || norm.contains("cartao de credito")
                || norm.contains("funcao credito")
                || norm.contains("credito a vista")
                || norm.contains("parcelado")
                || norm.contains("parcela")
                || norm.contains("fatura")
                || norm.contains("limite disponivel");

        boolean mentionsCardOrBrand = norm.contains("cartao")
                || norm.contains("visa")
                || norm.contains("mastercard")
                || norm.contains("master")
                || norm.contains("elo")
                || norm.contains("amex")
                || norm.contains("black")
                || norm.contains("platinum")
                || norm.contains("gold")
                || norm.contains("final ");

        boolean isCreditCardApp = pkg.contains("credicard")
                || pkg.contains("way")
                || pkg.contains("cartoes")
                || pkg.contains("walletnfcrel");

        SharedPreferences prefs = ctx.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);

        // 6. Consultar REGRAS APRENDIDAS das edições do usuário
        String learnedJson = prefs.getString(KEY_LEARNED_RULES, "{}");
        String learnedLocal = null;
        String learnedCartao = null;
        String learnedCategoria = null;

        try {
            JSONObject learned = new JSONObject(learnedJson);
            Iterator<String> keys = learned.keys();
            while (keys.hasNext()) {
                String k = keys.next();
                if (k.length() >= 2 && norm.contains(k.toLowerCase(Locale.ROOT))) {
                    JSONObject rule = learned.optJSONObject(k);
                    if (rule != null) {
                        learnedLocal = rule.optString("local", "").trim();
                        learnedCartao = rule.optString("cartao", "").trim();
                        learnedCategoria = rule.optString("categoria", "").trim();
                        break;
                    }
                }
            }
        } catch (Exception ignored) {}

        // Identificar cartão
        String cartao = cartaoOverride;
        if (cartao == null || cartao.isEmpty()) {
            if (learnedCartao != null && !learnedCartao.isEmpty()) {
                cartao = learnedCartao;
            } else {
                // Tentar casar com os cartões configurados pelo usuário
                try {
                    String knownJson = prefs.getString(KEY_KNOWN_CARDS, "[]");
                    JSONArray kc = new JSONArray(knownJson);
                    for (int i = 0; i < kc.length(); i++) {
                        String cName = kc.optString(i, "").trim();
                        if (cName.length() >= 2) {
                            String normC = removerAcentos(cName).toLowerCase(Locale.ROOT);
                            if (norm.contains(normC) || pkg.contains(normC.replaceAll("\\s+", ""))) {
                                cartao = cName;
                                break;
                            }
                        }
                    }
                } catch (Exception ignored) {}
            }
        }

        if (cartao == null || cartao.isEmpty()) {
            if (pkg.contains("mercadopago") || norm.contains("mercado pago") || norm.contains("mercadopago")) {
                cartao = "Mercado Pago";
            } else if (pkg.contains("itau") || pkg.contains("credicard") || norm.contains("itau") || norm.contains("personnalite")) {
                cartao = "Itaú";
            } else if (pkg.contains("nubank") || norm.contains("nubank") || norm.contains("roxinho")) {
                cartao = "Nubank";
            } else if (pkg.contains("intermedium") || norm.contains("inter")) {
                cartao = "Banco Inter";
            } else if (pkg.contains("c6bank") || norm.contains("c6")) {
                cartao = "C6 Bank";
            } else if (pkg.contains("santander") || norm.contains("santander") || norm.contains("way")) {
                cartao = "Santander";
            } else if (pkg.contains("bradesco") || norm.contains("bradesco") || norm.contains("next")) {
                cartao = "Bradesco";
            } else if (pkg.contains("caixa") || norm.contains("caixa")) {
                cartao = "Caixa";
            } else if (pkg.contains("bb.android") || norm.contains("banco do brasil") || norm.contains("ourocard")) {
                cartao = "Banco do Brasil";
            } else if (pkg.contains("picpay") || norm.contains("picpay")) {
                cartao = "PicPay";
            } else if (mentionsCardOrBrand || mentionsCredit || isCreditCardApp) {
                cartao = "Cartão";
            } else {
                registrarLog(ctx, pkg, title, body, "Descartado: Cartão não identificado");
                return false;
            }
        }

        // Identificar local real da compra
        String rawLocalCandidate = extrairEstabelecimento(title, body, fullText);
        String localFinal = (learnedLocal != null && !learnedLocal.isEmpty()) ? learnedLocal : rawLocalCandidate;

        long now = System.currentTimeMillis();

        try {
            String rawPending = prefs.getString(KEY_PENDING, "[]");
            JSONArray pending = new JSONArray(rawPending);

            // Evitar duplicata (mesmo valor e cartão dentro de 2 minutos)
            long lastTs = prefs.getLong("last_ts", 0);
            String lastCard = prefs.getString("last_card", "");
            double lastVal = Double.longBitsToDouble(prefs.getLong("last_val", 0));

            if (cartaoOverride == null && (now - lastTs) < 120000L && lastCard.equals(cartao) && Math.abs(lastVal - valor) < 0.01) {
                registrarLog(ctx, pkg, title, body, "Descartado: Duplicata dentro de 2 minutos");
                return false;
            }

            Date d = new Date(now);
            String dataBR = new SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(d);
            String mesRef = new SimpleDateFormat("yyyy-MM", Locale.getDefault()).format(d);

            JSONObject item = new JSONObject();
            item.put("id", "notif_" + now);
            item.put("data", dataBR);
            item.put("mesRef", mesRef);
            item.put("cartao", cartao);
            item.put("valor", valor);
            item.put("local", localFinal);
            item.put("rawLocal", rawLocalCandidate);
            item.put("rawTexto", fullText);
            item.put("categoria", learnedCategoria != null ? learnedCategoria : "");
            item.put("tipo", "Notificação");
            item.put("metodo", "Crédito");

            pending.put(item);

            prefs.edit()
                    .putString(KEY_PENDING, pending.toString())
                    .putLong("last_ts", now)
                    .putString("last_card", cartao)
                    .putLong("last_val", Double.doubleToRawLongBits(valor))
                    .apply();

            registrarLog(ctx, pkg, title, body, "Capturado com Sucesso: " + localFinal + " - R$ " + valor + " (" + cartao + ")");
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    private static double extrairValor(String texto) {
        Pattern p = Pattern.compile("R\\$\\s*([\\d.]+,\\d{2}|\\d+(?:[.,]\\d{1,2})?)", Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(texto);
        if (m.find()) {
            String num = m.group(1);
            if (num != null) {
                if (num.contains(",")) {
                    num = num.replace(".", "").replace(",", ".");
                }
                try {
                    return Double.parseDouble(num);
                } catch (NumberFormatException ignored) {}
            }
        }
        return 0.0;
    }

    public static String extrairEstabelecimento(String title, String body, String fullText) {
        String combined = body != null && !body.isEmpty() ? body : fullText;

        // 1. Padrões com palavras-chave de estabelecimento no corpo
        Pattern p = Pattern.compile(
                "(?:no estabelecimento:?|na loja:?|no site:?|no local:?|em|para|no|na)\\s+([A-Za-z0-9À-ÿ][A-Za-z0-9À-ÿ\\s.\\*\\-_'#/]{1,55}?)" +
                "(?=\\s+(?:no valor|valor|às|as|no dia|dia|em \\d|com o|com seu|no cart|cartão|cartao|com cartão|com cartao|via|pelo|final \\d|R\\$)|[.,!?;]|\n|$)",
                Pattern.CASE_INSENSITIVE
        );
        Matcher m = p.matcher(combined);
        while (m.find()) {
            String cand = m.group(1) != null ? m.group(1).trim() : "";
            String limpo = limparNomeLoja(cand);
            if (isNomeValido(limpo)) {
                return limpo;
            }
        }

        // 2. Se o título parecer o nome da loja (quando o app coloca o nome da loja no título)
        if (title != null && !title.isEmpty()) {
            String nt = removerAcentos(title).toLowerCase(Locale.ROOT);
            boolean isGenericTitle = nt.contains("compra") || nt.contains("pagamento") || nt.contains("notificacao")
                    || nt.contains("mercado pago") || nt.contains("itau") || nt.contains("nubank")
                    || nt.contains("cartao") || nt.contains("aviso") || nt.contains("banco")
                    || nt.contains("financeiro") || nt.contains("carteira");

            if (!isGenericTitle) {
                String limpo = limparNomeLoja(title);
                if (isNomeValido(limpo)) {
                    return limpo;
                }
            }
        }

        // 3. Padrão alternativo: "compra de R$ XX em LOJA"
        Pattern p2 = Pattern.compile("R\\$\\s*[\\d.,]+\\s+(?:em|na|no|para)\\s+([A-Za-z0-9À-ÿ][A-Za-z0-9À-ÿ\\s.\\*\\-_'/]{1,40}?)", Pattern.CASE_INSENSITIVE);
        Matcher m2 = p2.matcher(fullText);
        if (m2.find()) {
            String limpo = limparNomeLoja(m2.group(1));
            if (isNomeValido(limpo)) {
                return limpo;
            }
        }

        return "Compra em Cartão";
    }

    private static String limparNomeLoja(String raw) {
        if (raw == null) return "";
        String s = raw.trim();

        // Remover prefixos comuns de gateways e maquininhas
        s = s.replaceAll("^(?i)(?:pg\\s*\\*|pag\\s*\\*|pagar\\.me\\s*\\*|mp\\s*\\*|mercadopago\\s*\\*|paypal\\s*\\*|sumup\\s*\\*|cielo\\s*\\*|getnet\\s*\\*|rede\\s*\\*|stone\\s*\\*|ifood\\s*\\*|uber\\s*\\*)", "").trim();

        // Remover resíduos de final de texto
        s = s.replaceAll("(?i)\\s+(?:no dia|dia \\d+|às \\d+|as \\d+|com seu|no valor|final \\d+).*$", "").trim();
        s = s.replaceAll("[.,\\-*!;:/]+$", "").trim();

        // Se estiver tudo em maiúsculas e tiver mais de 3 letras, converter para Title Case
        if (s.length() > 3 && s.equals(s.toUpperCase(Locale.ROOT))) {
            s = toTitleCase(s);
        }

        return s;
    }

    private static boolean isNomeValido(String nome) {
        if (nome == null || nome.length() < 2) return false;
        String norm = removerAcentos(nome).toLowerCase(Locale.ROOT);
        return !norm.startsWith("seu cartao")
                && !norm.startsWith("cartao")
                && !norm.startsWith("credito")
                && !norm.startsWith("debito")
                && !norm.startsWith("valor")
                && !norm.startsWith("conta")
                && !norm.equals("mercado pago")
                && !norm.equals("itau");
    }

    private static String toTitleCase(String input) {
        StringBuilder sb = new StringBuilder();
        String[] words = input.toLowerCase(Locale.ROOT).split("\\s+");
        for (int i = 0; i < words.length; i++) {
            String w = words[i];
            if (w.isEmpty()) continue;
            // Preservar siglas conhecidas
            if (w.equals("ltda") || w.equals("s/a") || w.equals("sa") || w.equals("me") || w.equals("epp") || w.equals("br")) {
                sb.append(w.toUpperCase(Locale.ROOT));
            } else if (i > 0 && (w.equals("de") || w.equals("da") || w.equals("do") || w.equals("dos") || w.equals("das") || w.equals("e") || w.equals("em"))) {
                sb.append(w);
            } else {
                sb.append(Character.toUpperCase(w.charAt(0))).append(w.substring(1));
            }
            if (i < words.length - 1) sb.append(" ");
        }
        return sb.toString();
    }

    private static void registrarLog(Context ctx, String pkg, String title, String body, String status) {
        try {
            SharedPreferences prefs = ctx.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
            JSONArray logs = new JSONArray(prefs.getString(KEY_LOGS, "[]"));
            JSONObject log = new JSONObject();
            log.put("hora", new SimpleDateFormat("dd/MM HH:mm", Locale.getDefault()).format(new Date()));
            log.put("app", pkg);
            log.put("titulo", title);
            log.put("texto", body);
            log.put("status", status != null ? status : "Interceptado");

            JSONArray next = new JSONArray();
            next.put(log);
            for (int i = 0; i < Math.min(logs.length(), 19); i++) {
                next.put(logs.get(i));
            }
            prefs.edit().putString(KEY_LOGS, next.toString()).apply();
        } catch (Exception ignored) {}
    }
}
