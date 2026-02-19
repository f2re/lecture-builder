# Skill: Academic Search Patterns

Reference templates for building effective search queries for Russian academic literature.

## Russian open-access databases
```
site:cyberleninka.ru "{keywords}"
site:elib.rshu.ru "{topic}"
site:lib.spbu.ru "{discipline}" учебник
site:dl.msupress.org "{topic}"
site:elibrary.ru "{topic}" статья
site:docs.cntd.ru "{topic}" ГОСТ
```

## International open-access
```
site:arxiv.org "{topic EN}"
site:mdpi.com "{topic EN}"
site:researchgate.net "{topic EN}" pdf
site:semanticscholar.org "{topic EN}"
```

## Textbook & lecture notes patterns
```
"{topic}" filetype:pdf учебник бакалавр
"{topic EN}" textbook filetype:pdf
"{discipline}" рабочая программа site:*.edu.ru
"{topic}" лекция конспект site:rshu.ru OR site:msu.ru
```

## Date filtering
Add year range for recency: `"{topic}" 2020..2025`

## Synonym expansion
Use OR for synonyms: `"{term1}" OR "{term2}" учебник`

## Practical limits
- Max 5 queries per lecture question to avoid rate limits
- Deduplicate by URL before saving results
- Skip URLs already present in local_index.json
