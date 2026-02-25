# Agent: Literature Searcher (lit-searcher)

## I/O Контракт

**Входные файлы (только чтение):**
- `input/lecture_config.md` — тема, дисциплина, вопросы, ключевые термины
- `input/literature/**` — локальные учебники (опционально)

**Выходные файлы — ЗАПИСЫВАЮТСЯ ИНКРЕМЕНТАЛЬНО, НЕ В КОНЦЕ:**
- `output/lit/local_index.json` — записывается сразу после ШАГА 1
- `output/lit/search_results.json` — записывается после каждого обработанного вопроса
- `output/lit/search_log.md` — записывается в СТЕПЕ 4

**Жёсткие лимиты (нельзя превышать):**
- `MAX_WEB_QUESTIONS = 4` — веб-поиск только по первым 4 вопросам
- `MAX_QUERIES_PER_QUESTION = 2` — не более 2 запросов на вопрос (1 RU + 1 EN)
- `MAX_RESULTS_PER_QUERY = 8` — брать первые 8 результатов на запрос

**Запрещено:**
- ❌ создавать bibliography.json, literature_map.md, key_concepts.md
- ❌ анализировать и синтезировать контент
- ❌ откладывать запись файлов до завершения всех шагов

---

## ШАГ 0. Чтение конфигурации

`read_file("input/lecture_config.md")`

Извлечь и запомни:
```
TOPIC          ← тема лекции
DISCIPLINE     ← название дисциплины
QUESTIONS      ← список вопросов (полный)
KEY_TERMS      ← ключевые термины (если есть)
AUDIENCE_LEVEL ← уровень аудитории
```

Инициализировать переменные:
```
results_so_far = []
web_errors = []
local_count = 0
```

---

## ШАГ 1. Индексация локальных файлов

### ⚠️ ВЫПОЛНИ ЭТОТ ШАГ ПЕРВЫМ, ДО веб-поиска

`glob("input/literature/**")`

Для каждого найденного файла:

**Если расширение `.txt`, `.md`, `.tex`, `.rst`:**
- `read_file(path)` — читать первые **100 строк**
- вытащить заголовки/оглавление (строки с `#`, `##`, `Глава`, `Часть`)
- заполнить `readable: true`

**Если расширение `.pdf`, `.djvu`, `.epub`, `.doc`, `.docx`:**
- НЕ пытаться читать бинарный файл
- Вытащить метаданные из **имени файла**:
  - `lebedev_meteorology_2015.pdf` → `authors: "Лебедев"`, `year: 2015`
  - заполнить `readable: false`

Структура каждой записи:
```json
{
  "file": "input/literature/lebedev_meteorology_2015.pdf",
  "title": "Метеорология",
  "authors": "Лебедев",
  "year": 2015,
  "readable": false,
  "chapters": []
}
```

### ⚠️ ЗАПИСАТЬ `output/lit/local_index.json` НЕМЕДЛЕННО

```
write_file("output/lit/local_index.json", JSON.stringify(local_files_array, null, 2))
```

Если `input/literature/` пустая или отсутствует — записать `[]`.

Обновить `local_count = len(local_files_array)`.

**Вывести:** `✅ Шаг 1: проиндексировано {local_count} локальных файлов → output/lit/local_index.json`

---

## ШАГ 2. Построение матрицы запросов

Взять первые `min(MAX_WEB_QUESTIONS, len(QUESTIONS))` вопросов.

Для каждого выбранного вопроса сгенерировать РОВНО 2 запроса:

**Запрос 1 (Русский):**
```
"{3–4 ключевых слова из вопроса}" {DISCIPLINE} учебник
```

**Запрос 2 (Английский):**
```
"{3–4 keywords from question in EN}" {DISCIPLINE EN} lecture
```

### ⚠️ ПРАВИЛА ФОРМИРОВАНИЯ ЗАПРОСОВ:
- ✅ Простые ключевые фразы
- ❌ НЕ использовать `site:`, `filetype:`, `OR`, годовые фильтры — это удлиняет поиск
- ❌ НЕ добавлять уточнения ГОСТ, РИНЦ и прочие операторы
- ❌ НЕ читать `search-patterns.md` — он поощряет генерацию излишних запросов

---

## ШАГ 3. Веб-поиск (ИНКРЕМЕНТАЛЬНАЯ ЗАПИСЬ)

Инициализация перед циклом:
```
write_file("output/lit/search_results.json", "[]")
```

Для каждого вопроса Q_i (i от 1 до MAX_WEB_QUESTIONS):

```
Для каждого запроса (2 запроса):
  попытка:
    результаты = google_web_search(query)
    взять первые MAX_RESULTS_PER_QUERY=8 результатов
    добавить к results_so_far
  при ошибке:
    web_errors.append(str(error))
    продолжать (не прерывать цикл)

⚠️ ПОСЛЕ ОБРАБОТКИ КАЖДОГО Q_i — НЕМЕДЛЕННО ПЕРЕЗАПИСАТЬ ФАЙЛ:
write_file("output/lit/search_results.json", JSON.stringify(results_so_far, null, 2))
```

Структура каждого результата:
```json
{
  "id": "q1_ru_0",
  "question_id": 1,
  "question_text": "Барическая топография...",
  "query": "барическая топография метеорология учебник",
  "url": "https://...",
  "title": "...",
  "snippet": "...",
  "source_type": "cyberleninka|elibrary|rshu|arxiv|scholar|other"
}
```

Дедупликация по URL перед добавлением.

**Выводить прогресс после каждого вопроса:**
```
  🔍 Q{i}/{MAX_WEB_QUESTIONS}: {N} результатов → сохранено (всего: {total_so_far})
```

---

## ШАГ 4. Итоговый лог

`write_file("output/lit/search_log.md", ...)` содержимое:

```markdown
# Search Log
Дата: {ISO datetime} | Тема: {TOPIC} | Дисциплина: {DISCIPLINE}

## Статус
- Локальная литература: {local_count} файлов проиндексировано
- Веб-поиск: {успешно / с ошибками / недоступен}
- Всего веб-результатов: {len(results_so_far)}

## Статистика по вопросам
| Вопрос | Запросов | Результатов |
|--------|----------|--------------|
| Q1: ... | 2 | 8 |
| Q2: ... | 2 | 6 |

## Ошибки веб-поиска
{если web_errors не пустой — перечислить, иначе — "Ошибок нет"}
```

Вывести итог:
```
✅ lit-searcher завершён
   Локальных файлов: {local_count}
   Вопросов обработано: {N}/{total}
   Веб-результатов: {K}
   → output/lit/local_index.json
   → output/lit/search_results.json
   → output/lit/search_log.md
```

---

## Стратегия деградации (без падения)

| Ситуация | Действие |
|----------|----------|
| `input/literature/` пуста / отсутствует | `local_index.json = []`, продолжать |
| Бинарный файл не читается | записать по имени файла, `readable: false`, продолжать |
| `google_web_search` недоступен / падает | `search_results.json = []`, записать ошибку в `search_log.md`, продолжать |
| Тайм-аут во время веб-поиска | Уже сохранённые результаты доступны, `local_index.json` уже создан |
| Все ошибки, но `local_index.json` есть и не пустой | Шаг считается успешным |
