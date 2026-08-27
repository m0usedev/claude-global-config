#!/bin/bash
# Statusline para Claude Code:
# modelo | thinking on/off | % contexto | % tokens (rate limit 5h) | tiempo hasta reset

input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
THINKING=$(echo "$input" | jq -r 'if .thinking.enabled == true then "🧠 ON" else "🧠 OFF" end')

CTX_PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

# Rate limit de 5 horas (porcentaje de tokens consumidos y hora de reset)
RATE_PCT=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
RESETS_AT=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty')

if [ -n "$RATE_PCT" ]; then
    RATE_PCT_FMT=$(printf '%.0f' "$RATE_PCT")
else
    RATE_PCT_FMT="--"
fi

if [ -n "$RESETS_AT" ]; then
    NOW=$(date +%s)
    DIFF=$((RESETS_AT - NOW))
    if [ "$DIFF" -gt 0 ]; then
        HRS=$((DIFF / 3600))
        MINS=$(((DIFF % 3600) / 60))
        RESET_FMT="${HRS}h ${MINS}m"
    else
        RESET_FMT="reiniciando..."
    fi
else
    RESET_FMT="--"
fi

echo "[$MODEL] | $THINKING | 📊 ctx: ${CTX_PCT}% | 🎯 tokens: ${RATE_PCT_FMT}% | ⏳ reset en: ${RESET_FMT}"