# Subtitle Rules

## Goal

Subtitles should be readable edited speech. They preserve meaning and rhythm, but they do not preserve every hesitation from ASR.

## Cleanup Rules

- Correct names, locations, book titles, products, organizations, and domain terms.
- Correct gender pronouns.
- Remove sentence-opening fillers such as 啊、嗯、呃、哎呀 when they do not carry meaning.
- Remove thinking fillers such as 然后、那个、就是 when they are only stalls.
- Remove repeated starts and obvious stutters.
- Preserve meaningful repetition when it carries emotion, usually no more than 3 times.
- If raw audio breaks off mid-sentence and the subtitle would be incomprehensible, lightly complete the missing object in the subtitle or rewrite as a clean spoken sentence.

## Punctuation Rules

For final burned Chinese subtitles:

- Use half-width spaces where written Chinese would normally use commas.
- Do not use sentence-final punctuation.
- Avoid ordinary punctuation marks such as `，。！？；：“”《》（）`.
- Keep book-title brackets only in non-burned notes if needed. In burned subtitles, prefer plain book titles.

Example:

```text
Raw:
啊，我觉得《我们可以坦然生长》，其实不是一本简单的励志书。

Final subtitle:
我觉得 我们可以坦然生长
不是一本简单的励志书
```

## Line Rules

- Default max visible line: around 16 Chinese characters.
- Avoid leaving a 2-3 character orphan line.
- Do not split names, book titles, fixed terms, or tight parallel phrases.
- Split at breath pauses, speaker changes, or long gaps over 1 second.
- Keep one meaning unit per cue when possible.

## Timing Rules

- Subtitle should appear with speech, not before the viewer hears the idea.
- 花字/quote overlays should enter after the spoken idea arrives, not before it.
- If emotion is more important than text, move the text away from the face or remove it.

## QA

Run:

```bash
python3 scripts/subtitle_qa.py path/to/subtitles.srt --max-chars 16
```

Add known ASR mistakes:

```bash
python3 scripts/subtitle_qa.py subtitles.srt \
  --bad-term 何菜头=和菜头 \
  --bad-term 段瑞=段睿 \
  --bad-term 两元六号=郎园六号
```

