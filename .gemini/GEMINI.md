# Система генерации лекций

## О проекте
Многоагентная система для создания лекционных материалов вузовского уровня.

## Структура входных данных
- `input/lecture_config.md` — ОБЯЗАТЕЛЬНО заполнить перед запуском
- `input/existing_refs.md` — дополнительные источники (опционально)

## Шаблон lecture_config.md
```yaml
topic: "Тема лекции"
discipline: "Название дисциплины"
specialty: "09.03.01 Информатика и вычислительная техника"
course: "2 курс, 3 семестр"
hours: 2
fgos_version: "ФГОС 3++"
competencies:
  - "ОПК-2: способен разрабатывать алгоритмы..."
  - "ПК-1: ..."
audience_level: "бакалавры 2 курса"
questions:
  - "1. Понятие и классификация..."
  - "2. Основные методы..."
  - "3. Применение в..."
language: ru
formulas_required: true
```

## Быстрый старт

### Автоматический режим (рекомендуется)
Запусти оркестратор — он выполнит весь пайплайн автоматически:
```
@agents/orchestrator.md
```

### Ручной режим (для отладки отдельных шагов)
1. @agents/literature-analyst.md
2. @agents/query-builder.md
3. @agents/section-writer.md (для каждого вопроса)
4. @agents/document-assembler.md
5. @agents/reviewer.md
6. @agents/editor.md

## Выходные файлы
| Файл | Описание |
|------|----------|
| `output/lecture_final.md` | Финальная лекция |
| `output/image_prompts.md` | Промпты для иллюстраций |
| `output/bibliography.json` | Аннотированная библиография |
| `output/edit_log.md` | Лог всех правок |
| `output/figures_index.json` | Индекс иллюстраций |

## Язык: русский
