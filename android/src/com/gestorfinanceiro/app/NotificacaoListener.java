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
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class NotificacaoListener extends NotificationListenerService {

    public static final String PREFS_NAME = "fin_notif_queue";
    public static final String KEY_PENDING = "pending";
    public static final String KEY_LOGS = "logs";
    public static final String KEY_KNOWN_CARDS = "known_cards";

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        if (sbn == null || sbn.getNotification() == null) return;

        Notification notif = sbn.getNotification();
        if ((notif.flags & Notification.FLAG_GROUP_SUMMARY) != 0) return;

        String pkg = sbn.getPackageName() != null ? sbn.getPackageName().toLowerCase(Locale.ROOT) : "";

        // Ignorar mensageiros e redes sociais
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

        String title = charSeqToStr(extras.getCharSequence(Notification.EXTRA_TITLE));
        String text = charSeqToStr(extras.getCharSequence(Notification.EXTRA_TEXT));
        String bigText = charSeqToStr(extras.getCharSequence(Notification.EXTRA_BIG_TEXT));
        String body = !bigText.isEmpty() ? bigText : text;

        if (title.isEmpty() && body.isEmpty()) return;

        processarNotificacao(getApplicationContext(), null, pkg, title, body);
    }

    private static String charSeqToStr(CharSequence cs) {
        return cs == null ? "" : cs.toString().trim();
    }

    public static String removerAcentos(String s) {
        if (s == null) return "";
        String norm = Normalizer.normalize(s, Normalizer.Form.NFD);
        return norm.replaceAll("[\\p{InCombiningDiacriticalMarks}]", "");
    }

    public static synchronized boolean processarNotificacao(Context ctx, String cartaoOverride, String pkg, String title, String body) {
        String fullText = (title + " " + body).trim();
        String norm = removerAcentos(fullText).toLowerCase(Locale.ROOT);

        registrarLog(ctx, pkg, title, body);

        // Ignorar avisos promocionais, recebimentos, lembretes de fatura ou estornos
        if (norm.contains("recebeu") || norm.contains("recebido") || norm.contains("recebida")
                || norm.contains("cashback") || norm.contains("rendeu") || norm.contains("rendimento")
                || norm.contains("aproveite") || norm.contains("oferta") || norm.contains("promocao")
                || norm.contains("fatura fechada") || norm.contains("fatura disponivel")
                || norm.contains("vence em") || norm.contains("vencimento") || norm.contains("pague sua fatura")
                || norm.contains("lembrete") || norm.contains("codigo") || norm.contains("verificacao")
                || norm.contains("estorno") || norm.contains("cancelad") || norm.contains("recusad")) {
            return false;
        }

        // Exigir valor monetário em R$
        double valor = extrairValor(fullText);
        if (valor <= 0.0 || valor > 500000.0) {
            return false;
        }

        // Exigir contexto de compra/pagamento/gasto
        boolean isPurchase = norm.contains("compra") || norm.contains("aprovad")
                || norm.contains("pagou") || norm.contains("pagamento")
                || norm.contains("gastou") || norm.contains("credito")
                || norm.contains("debito") || norm.contains("cartao")
                || norm.contains("passou") || norm.contains("autorizad")
                || norm.contains("realizad") || norm.contains("estabelecimento");

        if (!isPurchase) {
            return false;
        }

        // Identificar cartão
        String cartao = cartaoOverride;
        if (cartao == null || cartao.isEmpty()) {
            // Tentar casar com os cartões configurados pelo usuário no app
            try {
                SharedPreferences prefs = ctx.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
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
            } else {
                cartao = "Cartão";
            }
        }

        String local = extrairEstabelecimento(title, body);
        long now = System.currentTimeMillis();

        SharedPreferences prefs = ctx.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        try {
            String rawPending = prefs.getString(KEY_PENDING, "[]");
            JSONArray pending = new JSONArray(rawPending);

            // Evitar duplicata (mesmo valor e cartão dentro de 2 minutos)
            long lastTs = prefs.getLong("last_ts", 0);
            String lastCard = prefs.getString("last_card", "");
            double lastVal = Double.longBitsToDouble(prefs.getLong("last_val", 0));

            if (cartaoOverride == null && (now - lastTs) < 120000L && lastCard.equals(cartao) && Math.abs(lastVal - valor) < 0.01) {
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
            item.put("local", local);
            item.put("tipo", "Notificação");

            pending.put(item);

            prefs.edit()
                    .putString(KEY_PENDING, pending.toString())
                    .putLong("last_ts", now)
                    .putString("last_card", cartao)
                    .putLong("last_val", Double.doubleToRawLongBits(valor))
                    .apply();

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

    private static String extrairEstabelecimento(String title, String body) {
        String combined = body != null && !body.isEmpty() ? body : title;
        // Padrões comuns: "em LOJA", "no estabelecimento LOJA", "para LOJA", "no local LOJA"
        Pattern p = Pattern.compile(
                "(?:estabelecimento:?|no local|em|para|no|na)\\s+([A-Za-z0-9À-ÿ][A-Za-z0-9À-ÿ\\s.\\*\\-_'/]{1,45}?)(?=\\s+(?:no valor|valor|às|as|no dia|dia|em \\d|com o|com seu|no cart|cartão|cartao|via|pelo|R\\$)|[.,!]|$)",
                Pattern.CASE_INSENSITIVE
        );
        Matcher m = p.matcher(combined);
        while (m.find()) {
            String cand = m.group(1) != null ? m.group(1).trim() : "";
            String normCand = removerAcentos(cand).toLowerCase(Locale.ROOT);
            if (cand.length() >= 2
                    && !normCand.startsWith("seu cartao")
                    && !normCand.startsWith("cartao")
                    && !normCand.startsWith("credito")
                    && !normCand.startsWith("debito")
                    && !normCand.startsWith("valor")
                    && !normCand.startsWith("conta")) {
                return cand;
            }
        }

        // Se o título parecer nome de loja (não for genérico)
        if (title != null && !title.isEmpty()) {
            String nt = removerAcentos(title).toLowerCase(Locale.ROOT);
            if (!nt.contains("compra") && !nt.contains("mercado pago") && !nt.contains("itau") && !nt.contains("pagou") && !nt.contains("nubank")) {
                return title.length() > 45 ? title.substring(0, 45) : title;
            }
        }
        return "Compra Automática";
    }

    private static void registrarLog(Context ctx, String pkg, String title, String body) {
        try {
            SharedPreferences prefs = ctx.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
            JSONArray logs = new JSONArray(prefs.getString(KEY_LOGS, "[]"));
            JSONObject log = new JSONObject();
            log.put("hora", new SimpleDateFormat("dd/MM HH:mm", Locale.getDefault()).format(new Date()));
            log.put("app", pkg);
            log.put("titulo", title);
            log.put("texto", body);

            JSONArray next = new JSONArray();
            next.put(log);
            for (int i = 0; i < Math.min(logs.length(), 14); i++) {
                next.put(logs.get(i));
            }
            prefs.edit().putString(KEY_LOGS, next.toString()).apply();
        } catch (Exception ignored) {}
    }
}
