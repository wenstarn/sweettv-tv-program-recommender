# Business & Algorithmic Analysis: SWEET.TV

This English edition presents the same computed classical-method results as the
original analysis. No recommendation, metric or source CSV has been changed.
Programme titles are quoted in their source language; category labels in the
narrative are faithful English translations. The tables and case studies below
come from the existing English final report and the unchanged CSV evidence.

## Recommended Strategy

The selected strategy is History + CF + ALS + PPR + Schedule with its original
popularity fallback: audited MAP@5 **0.367811**, versus **0.279391** for popularity.
The absolute difference is **0.088420** (31.65% relative). The simpler History + CF
hybrid scores **0.366323**, only **0.001489** lower. These are offline metric
differences, not measured satisfaction or revenue effects. For user A the selected
mixture achieves AP@5 **0.52**; for B it scores **0**, below History at **0.146667**.

## Temporal Boundary and Recorded Provenance

The notebook originally splits qualified records by **broadcast start**, which can allow part of a training broadcast's watched interval to extend beyond the boundary. The separate audit finds **420** training broadcast records ending after the boundary; **411** actually contain post-boundary watched seconds, totalling **976,815 seconds**. The original notebook's later check for dates after 27 July does not test this 18 May boundary problem.

For the primary audited analysis, the already-merged training viewing intervals are clipped at **2020-05-18 00:00:00** and the same 80% threshold is reapplied against the original complete broadcast duration. This removes **318** qualified training records, leaving **316,416**, versus **316,734** in the original split. A crossing broadcast may remain only if 80% was already observed before the boundary. No algorithm or hyperparameter is changed. This necessary data correction is reported separately from exact notebook reproduction, and the notebook is left unchanged. Validation remains at **295,026** qualified records.

Classical time profiles already clip historical session end times at the cutoff. Knowing the validation broadcast schedule is an explicit availability assumption; knowing validation viewing behaviour is not allowed in the audited training/profile branch. The original-protocol branch is retained solely for reproduction and diagnosis.

## Shared Candidates and Metric

The original history/popularity family uses a 6,361-ID validation schedule catalog. Original hybrids restrict scoring and fallback to **1,874** future-scheduled IDs seen in the original training interactions; the audited equivalent is **1,867**. The primary comparison restricts **all** methods to this same 1,867-ID catalog, preserving primary scores, normalisation, tie handling, and fallback rules. An additional column retains evaluation under each method's original catalog. On these files, this common-catalog restriction changes **zero users' Top-5 for every audited method**; differences from the reproduced notebook are therefore due to the boundary correction and its downstream fitted factors/graph, not an observed Top-5 catalog effect.

For a prediction list (L_u), the notebook cell-30 metric is

\[
AP@5(u)=\frac1{5}\sum_{k=1}^{5}\left(\frac{\sum_{j=1}^k 1[L_{uj}\in G_u]}{k}\right)1[L_{uk}\in G_u],\quad
MAP@5=\frac1{|U|}\sum_{u\in U}AP@5(u).
\]

Each target has five distinct IDs, and all exported prediction lists are checked for uniqueness. Thus the guarded metric in cell 29 is equivalent on these inputs. An arbitrary held-out viewing outside the five targets is not a MAP hit: `hit_validation` and `hit_validation_top5` are retained separately.

The shared catalog contains **19,107/20,150 targets (94.82%)**. This is an eligibility-based upper bound on recall and an upper bound on attainable MAP, not an achieved recommendation score. No missing target is silently removed from the metric denominator.

## Method Comparison, Coverage and Recorded Costs

### 5.1. Classical and hybrid validation results

| Method | Notebook saved | Notebook reproduced | Audited common catalog | Absolute gain over popularity (audited) |
| --- | --- | --- | --- | --- |
| History + CF + ALS + PPR + Schedule | 0.367920 | 0.367920 | 0.367811 | 0.088420 |
| History + CF + ALS + Schedule | 0.367550 | 0.367550 | 0.367395 | 0.088004 |
| History + CF + Schedule | 0.366347 | 0.366347 | 0.366323 | 0.086931 |
| History + Schedule + Time | 0.359069 | 0.359069 | 0.358985 | 0.079594 |
| History + Schedule | 0.359027 | 0.359027 | 0.358943 | 0.079552 |
| User History | 0.346917 | 0.346917 | 0.346836 | 0.067445 |
| History + Time | 0.336535 | 0.336535 | 0.336462 | 0.057070 |
| Personalized PageRank | 0.318375 | 0.318375 | 0.318473 | 0.039082 |
| Global Popularity | 0.279391 | 0.279391 | 0.279391 | 0.000000 |
| Implicit ALS | 0.260887 | 0.260887 | 0.259294 | -0.020098 |
| Item-based CF | 0.206023 | 0.206023 | 0.205923 | -0.073468 |

All eleven reproduced original metrics agree with the saved notebook values within **1e-6**, their printed precision. In the audited comparison the four-component hybrid gains **0.088420** absolute MAP (31.65% relative) over popularity. This is a relative change in an offline metric, not a revenue or engagement lift. Adding ALS to H + CF gives 0.001073; adding PPR to that mixture gives 0.000416.

Standalone CF and ALS underperform popularity here, while PPR exceeds it. Their contribution as hybrid components differs from their standalone score: history anchors direct repeat preferences and a small collaborative term can adjust ordering. Schedule weighting improves history from 0.346836 to 0.358943; adding the classical time term yields only 0.000042 more with schedule, while time alone lowers history to 0.336462. These observations support schedule-aware repetition and complementarity; they do not show that more complex models always improve results. Configuration selection reused this holdout, so significance and independent generalisation are not established.

### 5.2. Coverage and popularity concentration

| Method | Unique recommended IDs | Catalog coverage | Seen-in-history share | Mean popularity rank |
| --- | --- | --- | --- | --- |
| History + CF + ALS + PPR + Schedule | 358 | 0.191751 | 0.858610 | 17.497816 |
| History + CF + ALS + Schedule | 363 | 0.194430 | 0.847593 | 17.920149 |
| History + CF + Schedule | 458 | 0.245313 | 0.901588 | 23.937866 |
| History + Schedule + Time | 564 | 0.302089 | 0.964665 | 34.143573 |
| History + Schedule | 565 | 0.302625 | 0.964665 | 34.126253 |
| User History | 621 | 0.332619 | 0.964665 | 37.976328 |
| History + Time | 873 | 0.467595 | 0.964665 | 57.536328 |
| Personalized PageRank | 509 | 0.272630 | 0.962680 | 25.064516 |
| Global Popularity | 5 | 0.002678 | 0.573300 | 3.000000 |
| Implicit ALS | 245 | 0.131227 | 0.720347 | 18.546948 |
| Item-based CF | 154 | 0.082485 | 0.534541 | 11.054690 |

Catalog coverage means the fraction of the 1,867 eligible IDs appearing in any validation Top-5. Seen-in-history share is measured per recommended user–item pair. Mean popularity rank uses the train-popularity fallback order; a smaller rank means more popular items. Popularity recommends just five IDs globally (0.2678% coverage). The winning hybrid recommends 358 IDs (19.1751%), with 85.8610% already seen by the recipient. History + time reaches more distinct IDs (873, 46.7595%) but lower MAP. Diversity and metric quality are therefore separate outcomes. CF is particularly popularity-oriented by the mean-rank measure (11.05), despite being personalised.

### 5.3. Measured computation and scalability

| Method | Shared stages (s) | Shared PPR pass (s) | Catalog alignment / ranking (s) |
| --- | --- | --- | --- |
| History + CF + ALS + PPR + Schedule | 29.837801 | 21.343696 | 3.814675 |
| History + CF + ALS + Schedule | 1.521363 | 0.000000 | 1.566213 |
| History + CF + Schedule | 0.652053 | 0.000000 | 1.125415 |
| History + Schedule + Time | 1.843300 | 0.000000 | 0.902485 |
| History + Schedule | 1.843300 | 0.000000 | 0.925920 |
| User History | 1.843300 | 0.000000 | 0.907606 |
| History + Time | 1.843300 | 0.000000 | 0.916632 |
| Personalized PageRank | 0.262466 | 21.343696 | 0.084809 |
| Global Popularity | 1.843300 | 0.000000 | 1.783507 |
| Implicit ALS | 0.899768 | 0.000000 | 1.529714 |
| Item-based CF | 0.194071 | 0.000000 | 1.163247 |

These are measured **shared pipeline stages**, not isolated model-training benchmarks or per-request latency. Preparation took **26.925 s**; the full two-protocol analysis took **191.927 s**. The CF construction stage took 0.194 s and the ALS training-plus-score stage 0.706 s. A shared PPR inference pass took **21.344 s**; cell 36 recomputed PPR and prepared the four-way mixture in 28.870 s. The shared PPR column and cell-36 cost describe separate repeated work in the faithful pipeline; they are not a requirement to repeat that computation in a deployed service. Dependency stages are reused and columns must not be added across methods. Several stages include score extraction, normalisation, or other work. The comparison records no peak RAM, isolated original training time, p95 latency, or monetary serving cost.

Popularity needs aggregate counters and one shared ranked list; repeat-history needs per-user counts. CF constructs a sparse audience-similarity product and keeps 50 outgoing neighbours per item; worst-case similarity construction can densify before pruning. ALS stores 64 factors per trained user/item and requires iterative fitting, followed by dot products. PPR performs up to 100 sparse graph multiplications per batch, explaining the measured offline overhead. These are code-level computational properties, not extrapolated production timing estimates. The two-way hybrid is a credible lower-cost alternative because its audited MAP is only 0.001489 below the winner; the marginal PPR gain over the three-way hybrid is 0.000416.

## Users, Histories, Targets and All Top-5 Recommendations

This section uses only the classical methods and the audited business-analysis artifacts. All recommendations below come from the same common catalog and the same two users; no model fitting or user reselection was performed for this report. Programme titles are quoted exactly from supplied metadata. Category labels are faithful English translations: Children = Детям; News / information = Инфо; Entertainment = Развлечения; Educational / factual = Познавательное; Series = Сериалы; Films = Фильмы; Other = Другое.

### 6.1. Quantitative user selection

Both users belong to validation and have at least 20 train interactions and five distinct train programmes. A maximises the dominant-category share among users whose dominant category is unchanged across the two train halves separated at 13 April 2020; ties use view count and then string ID. B maximises category entropy among the remaining eligible users, then unique-show count, then string ID. Selection uses only audited historical observations, not validation accuracy. The selected IDs are retained in the published `business_analysis/verify_results.py`. HHI is the sum of squared category shares and entropy is measured in bits.

| Profile | User ID | Train views | Unique shows | Categories | Largest category share | Entropy (bits) | HHI | Early views | Late views |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 11319785650938584699 | 76 | 23 | 1 | 1.000000 | -0.000000 | 1.000000 | 36 | 40 |
| B | 5911263612844924182 | 47 | 27 | 7 | 0.191489 | 2.717923 | 0.158895 | 35 | 12 |

| User | Category | Views | Share |
| --- | --- | --- | --- |
| A | Children | 76 | 1.000000 |
| B | Educational / factual | 9 | 0.191489 |
| B | Series | 9 | 0.191489 |
| B | News / information | 8 | 0.170213 |
| B | Entertainment | 8 | 0.170213 |
| B | Children | 6 | 0.127660 |
| B | Films | 4 | 0.085106 |
| B | Other | 3 | 0.063830 |

A has 76 qualified views across 23 programmes, all in Children, with 36 views in the early half and 40 in the late half. This supports category-level stability, not an inferred age or household composition. B has 47 views across 27 programmes and seven categories, maximum category share 19.15%, entropy 2.718 bits, and HHI 0.159. B is diverse rather than a cold-start example; category-level stationarity is not established.

### 6.2. User A: `11319785650938584699` — history, targets, and recommendations

Most frequent historical programmes:

| Programme ID | Source title | Category | Train views |
| --- | --- | --- | --- |
| 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children | 17 |
| 12001732 | М/с 'Пингвины из 'Мадагаскара'. | Children | 9 |
| 12002955 | М/с 'Свинка Пеппа', 1 с. 'Лужи'. | Children | 9 |
| 12002951 | Марафон. М/с 'Леди Баг и Супер-Кот'. | Children | 5 |
| 12001717 | М/с 'Барашек Шон'. | Children | 4 |
| 12002761 | М/с 'Утиные истории'. | Children | 3 |
| 12002809 | М/с 'Ниндзяго: Мастера Кружитцу'. | Children | 3 |
| 12002922 | М/с 'София Прекрасная'. 'Плавучий дворец'. | Children | 3 |

Five held-out targets (frequency order; binary relevance for evaluation):

| Target order | Programme ID | Source title | Category |
| --- | --- | --- | --- |
| 1 | 12001732 | М/с 'Пингвины из 'Мадагаскара'. | Children |
| 2 | 12002809 | М/с 'Ниндзяго: Мастера Кружитцу'. | Children |
| 3 | 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children |
| 4 | 12002957 | М/с 'Суперкрылья: Джетт и его друзья'. | Children |
| 5 | 12002832 | Узнавайка. М/с 'Елена - принцесса Авалора'. | Children |

#### User A: every implemented method’s Top-5

The method labels below follow Section 3. H denotes History; every mixture shown includes schedule weighting. **Target hit** means membership of the five evaluation targets; **Any view** means any qualified held-out viewing. **Train n** is the user’s historical count. All 110 exported rows have real title/category metadata and primary scores; no selected-user row uses fallback. Scores have different scales across methods.

| Method | Rank | Programme ID | Source title | Category | Score | Target hit | Any view | Train n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Popularity | 1 | 2400480 | ТСН. Неделя. | News / information | 39941.000000 | No | No | 0 |
| Popularity | 2 | 240081 | Факты. День. | News / information | 27032.000000 | No | No | 0 |
| Popularity | 3 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 26199.000000 | No | Yes | 2 |
| Popularity | 4 | 20088 | 'Завтрак с 1+1'. Информационно-развлекательная программа. | Entertainment | 12796.000000 | No | No | 0 |
| Popularity | 5 | 2400508 | Сегодня. Итоги с Олегом Панютой. | News / information | 10829.000000 | No | No | 0 |
| History | 1 | 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children | 17.000000 | Yes | Yes | 17 |
| History | 2 | 12001732 | М/с 'Пингвины из 'Мадагаскара'. | Children | 9.000000 | Yes | Yes | 9 |
| History | 3 | 12002955 | М/с 'Свинка Пеппа', 1 с. 'Лужи'. | Children | 9.000000 | No | No | 9 |
| History | 4 | 12002951 | Марафон. М/с 'Леди Баг и Супер-Кот'. | Children | 5.000000 | No | Yes | 5 |
| History | 5 | 12001717 | М/с 'Барашек Шон'. | Children | 4.000000 | No | No | 4 |
| History + schedule | 1 | 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children | 111.911011 | Yes | Yes | 17 |
| History + schedule | 2 | 12002955 | М/с 'Свинка Пеппа', 1 с. 'Лужи'. | Children | 56.019301 | No | No | 9 |
| History + schedule | 3 | 12001732 | М/с 'Пингвины из 'Мадагаскара'. | Children | 45.443403 | Yes | Yes | 9 |
| History + schedule | 4 | 12002951 | Марафон. М/с 'Леди Баг и Супер-Кот'. | Children | 17.726960 | No | Yes | 5 |
| History + schedule | 5 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 17.683810 | No | Yes | 2 |
| History + time | 1 | 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children | 17.027744 | Yes | Yes | 17 |
| History + time | 2 | 12002955 | М/с 'Свинка Пеппа', 1 с. 'Лужи'. | Children | 9.012906 | No | No | 9 |
| History + time | 3 | 12001732 | М/с 'Пингвины из 'Мадагаскара'. | Children | 9.008850 | Yes | Yes | 9 |
| History + time | 4 | 12002951 | Марафон. М/с 'Леди Баг и Супер-Кот'. | Children | 5.015022 | No | Yes | 5 |
| History + time | 5 | 12001717 | М/с 'Барашек Шон'. | Children | 4.009569 | No | No | 4 |
| History + schedule + time | 1 | 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children | 112.093648 | Yes | Yes | 17 |
| History + schedule + time | 2 | 12002955 | М/с 'Свинка Пеппа', 1 с. 'Лужи'. | Children | 56.099631 | No | No | 9 |
| History + schedule + time | 3 | 12001732 | М/с 'Пингвины из 'Мадагаскара'. | Children | 45.488089 | Yes | Yes | 9 |
| History + schedule + time | 4 | 12002951 | Марафон. М/с 'Леди Баг и Супер-Кот'. | Children | 17.780219 | No | Yes | 5 |
| History + schedule + time | 5 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 17.712694 | No | Yes | 2 |
| Item CF | 1 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 68.606255 | No | Yes | 2 |
| Item CF | 2 | 12001734 | М/с 'Волшебные покровители', 161 с. 'Женат на мамочке'. | Children | 51.286121 | No | No | 0 |
| Item CF | 3 | 12002896 | М/с 'Вспыш и чудо-машинки', 1 сезон, 15 с. 'Авто-Рейнджеры'. | Children | 47.285885 | No | No | 0 |
| Item CF | 4 | 12001732 | М/с 'Пингвины из 'Мадагаскара'. | Children | 45.877964 | Yes | Yes | 9 |
| Item CF | 5 | 12002805 | М/с 'Моланг', 1 сезон, 33 с. | Children | 42.166168 | No | No | 0 |
| H + CF | 1 | 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children | 1.919890 | Yes | Yes | 17 |
| H + CF | 2 | 12001732 | М/с 'Пингвины из 'Мадагаскара'. | Children | 1.187955 | Yes | Yes | 9 |
| H + CF | 3 | 12002955 | М/с 'Свинка Пеппа', 1 с. 'Лужи'. | Children | 1.175867 | No | No | 9 |
| H + CF | 4 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 0.914288 | No | Yes | 2 |
| H + CF | 5 | 12002951 | Марафон. М/с 'Леди Баг и Супер-Кот'. | Children | 0.700692 | No | Yes | 5 |
| ALS | 1 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 2.141044 | No | Yes | 2 |
| ALS | 2 | 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children | 2.129653 | Yes | Yes | 17 |
| ALS | 3 | 12002955 | М/с 'Свинка Пеппа', 1 с. 'Лужи'. | Children | 2.064251 | No | No | 9 |
| ALS | 4 | 12002809 | М/с 'Ниндзяго: Мастера Кружитцу'. | Children | 2.033751 | Yes | Yes | 3 |
| ALS | 5 | 12001863 | М/с 'Смешарики'. 'Место в истории'. | Children | 2.033169 | No | No | 0 |
| H + CF + ALS | 1 | 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children | 1.844628 | Yes | Yes | 17 |
| H + CF + ALS | 2 | 12001732 | М/с 'Пингвины из 'Мадагаскара'. | Children | 1.285648 | Yes | Yes | 9 |
| H + CF + ALS | 3 | 12002955 | М/с 'Свинка Пеппа', 1 с. 'Лужи'. | Children | 1.242444 | No | No | 9 |
| H + CF + ALS | 4 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 1.211121 | No | Yes | 2 |
| H + CF + ALS | 5 | 12002809 | М/с 'Ниндзяго: Мастера Кружитцу'. | Children | 0.830672 | Yes | Yes | 3 |
| PPR | 1 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 0.032254 | No | Yes | 2 |
| PPR | 2 | 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children | 0.026504 | Yes | Yes | 17 |
| PPR | 3 | 12002955 | М/с 'Свинка Пеппа', 1 с. 'Лужи'. | Children | 0.024201 | No | No | 9 |
| PPR | 4 | 12001732 | М/с 'Пингвины из 'Мадагаскара'. | Children | 0.022885 | Yes | Yes | 9 |
| PPR | 5 | 12002806 | М/с 'Октонавты', 1 сезон. | Children | 0.022612 | No | No | 2 |
| H + CF + ALS + PPR | 1 | 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children | 1.836622 | Yes | Yes | 17 |
| H + CF + ALS + PPR | 2 | 12001732 | М/с 'Пингвины из 'Мадагаскара'. | Children | 1.319889 | Yes | Yes | 9 |
| H + CF + ALS + PPR | 3 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 1.316616 | No | Yes | 2 |
| H + CF + ALS + PPR | 4 | 12002955 | М/с 'Свинка Пеппа', 1 с. 'Лужи'. | Children | 1.277147 | No | No | 9 |
| H + CF + ALS + PPR | 5 | 12002809 | М/с 'Ниндзяго: Мастера Кружитцу'. | Children | 0.888205 | Yes | Yes | 3 |

### 6.3. User B: `5911263612844924182` — history, targets, and recommendations

Most frequent historical programmes:

| Programme ID | Source title | Category | Train views |
| --- | --- | --- | --- |
| 200337 | 'Утро с 'Интером'. | Entertainment | 4 |
| 10003159 | Премьера. Т/с 'Ничто не случается дважды', 1 с. | Series | 4 |
| 1100411 | Премьера. 'Вещдок. Особый случай. Око за око'. | Educational / factual | 3 |
| 2400480 | ТСН. Неделя. | News / information | 3 |
| 5200303 | 'Следствие вели...' с Леонидом Каневским. | Educational / factual | 3 |
| 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 3 |
| 300358 | Скетч-шоу 'На троих', 7 сезон. | Entertainment | 2 |
| 1000381 | Т/с 'CSI: Место преступления', 7 сезон, 6 и 7 с. | Series | 2 |

Five held-out targets (frequency order; binary relevance for evaluation):

| Target order | Programme ID | Source title | Category |
| --- | --- | --- | --- |
| 1 | 1100411 | Премьера. 'Вещдок. Особый случай. Око за око'. | Educational / factual |
| 2 | 5200303 | 'Следствие вели...' с Леонидом Каневским. | Educational / factual |
| 3 | 500315 | Ток-шоу 'Касается каждого'. | Entertainment |
| 4 | 10001261 | Т/с 'Мыслить как преступник', 1 сезон, 1 и 2 с. | Series |
| 5 | 90043056 | Х/ф 'Живите в радости'. | Films |

#### User B: every implemented method’s Top-5

The method labels below follow Section 3. H denotes History; every mixture shown includes schedule weighting. **Target hit** means membership of the five evaluation targets; **Any view** means any qualified held-out viewing. **Train n** is the user’s historical count. All 110 exported rows have real title/category metadata and primary scores; no selected-user row uses fallback. Scores have different scales across methods.

| Method | Rank | Programme ID | Source title | Category | Score | Target hit | Any view | Train n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Popularity | 1 | 2400480 | ТСН. Неделя. | News / information | 39941.000000 | No | No | 3 |
| Popularity | 2 | 240081 | Факты. День. | News / information | 27032.000000 | No | No | 1 |
| Popularity | 3 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 26199.000000 | No | No | 3 |
| Popularity | 4 | 20088 | 'Завтрак с 1+1'. Информационно-развлекательная программа. | Entertainment | 12796.000000 | No | No | 0 |
| Popularity | 5 | 2400508 | Сегодня. Итоги с Олегом Панютой. | News / information | 10829.000000 | No | No | 2 |
| History | 1 | 200337 | 'Утро с 'Интером'. | Entertainment | 4.000000 | No | No | 4 |
| History | 2 | 10003159 | Премьера. Т/с 'Ничто не случается дважды', 1 с. | Series | 4.000000 | No | No | 4 |
| History | 3 | 1100411 | Премьера. 'Вещдок. Особый случай. Око за око'. | Educational / factual | 3.000000 | Yes | Yes | 3 |
| History | 4 | 2400480 | ТСН. Неделя. | News / information | 3.000000 | No | No | 3 |
| History | 5 | 5200303 | 'Следствие вели...' с Леонидом Каневским. | Educational / factual | 3.000000 | Yes | Yes | 3 |
| History + schedule | 1 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 26.525715 | No | No | 3 |
| History + schedule | 2 | 2400480 | ТСН. Неделя. | News / information | 17.582951 | No | No | 3 |
| History + schedule | 3 | 200337 | 'Утро с 'Интером'. | Entertainment | 16.015602 | No | No | 4 |
| History + schedule | 4 | 12001734 | М/с 'Волшебные покровители', 161 с. 'Женат на мамочке'. | Children | 12.309573 | No | No | 2 |
| History + schedule | 5 | 10003159 | Премьера. Т/с 'Ничто не случается дважды', 1 с. | Series | 10.583005 | No | No | 4 |
| History + time | 1 | 10003159 | Премьера. Т/с 'Ничто не случается дважды', 1 с. | Series | 4.009078 | No | No | 4 |
| History + time | 2 | 200337 | 'Утро с 'Интером'. | Entertainment | 4.002379 | No | No | 4 |
| History + time | 3 | 1100411 | Премьера. 'Вещдок. Особый случай. Око за око'. | Educational / factual | 3.004930 | Yes | Yes | 3 |
| History + time | 4 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 3.004580 | No | No | 3 |
| History + time | 5 | 5200303 | 'Следствие вели...' с Леонидом Каневским. | Educational / factual | 3.004463 | Yes | Yes | 3 |
| History + schedule + time | 1 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 26.566209 | No | No | 3 |
| History + schedule + time | 2 | 2400480 | ТСН. Неделя. | News / information | 17.605917 | No | No | 3 |
| History + schedule + time | 3 | 200337 | 'Утро с 'Интером'. | Entertainment | 16.025129 | No | No | 4 |
| History + schedule + time | 4 | 12001734 | М/с 'Волшебные покровители', 161 с. 'Женат на мамочке'. | Children | 12.331091 | No | No | 2 |
| History + schedule + time | 5 | 10003159 | Премьера. Т/с 'Ничто не случается дважды', 1 с. | Series | 10.607025 | No | No | 4 |
| Item CF | 1 | 240081 | Факты. День. | News / information | 33.991272 | No | No | 1 |
| Item CF | 2 | 2400480 | ТСН. Неделя. | News / information | 33.955814 | No | No | 3 |
| Item CF | 3 | 2400508 | Сегодня. Итоги с Олегом Панютой. | News / information | 30.505856 | No | No | 2 |
| Item CF | 4 | 20088 | 'Завтрак с 1+1'. Информационно-развлекательная программа. | Entertainment | 28.727901 | No | No | 0 |
| Item CF | 5 | 2400467 | 'Викна-Новости'. | News / information | 28.336012 | No | No | 2 |
| H + CF | 1 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 1.706010 | No | No | 3 |
| H + CF | 2 | 2400480 | ТСН. Неделя. | News / information | 1.617547 | No | No | 3 |
| H + CF | 3 | 200337 | 'Утро с 'Интером'. | Entertainment | 1.546019 | No | No | 4 |
| H + CF | 4 | 10003159 | Премьера. Т/с 'Ничто не случается дважды', 1 с. | Series | 1.263839 | No | No | 4 |
| H + CF | 5 | 1100411 | Премьера. 'Вещдок. Особый случай. Око за око'. | Educational / factual | 1.129772 | Yes | Yes | 3 |
| ALS | 1 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 2.311317 | No | No | 3 |
| ALS | 2 | 12002856 | М/с 'Элвиннн!!! и бурундуки'. | Children | 2.033850 | No | No | 0 |
| ALS | 3 | 2400480 | ТСН. Неделя. | News / information | 1.997695 | No | No | 3 |
| ALS | 4 | 12001734 | М/с 'Волшебные покровители', 161 с. 'Женат на мамочке'. | Children | 1.917963 | No | No | 2 |
| ALS | 5 | 6200371 | 'ДжеДАИ'. | Educational / factual | 1.880224 | No | No | 1 |
| H + CF + ALS | 1 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 1.698236 | No | No | 3 |
| H + CF + ALS | 2 | 2400480 | ТСН. Неделя. | News / information | 1.669483 | No | No | 3 |
| H + CF + ALS | 3 | 200337 | 'Утро с 'Интером'. | Entertainment | 1.478029 | No | No | 4 |
| H + CF + ALS | 4 | 2400508 | Сегодня. Итоги с Олегом Панютой. | News / information | 1.241261 | No | No | 2 |
| H + CF + ALS | 5 | 10003159 | Премьера. Т/с 'Ничто не случается дважды', 1 с. | Series | 1.189738 | No | No | 4 |
| PPR | 1 | 2400480 | ТСН. Неделя. | News / information | 0.029218 | No | No | 3 |
| PPR | 2 | 240081 | Факты. День. | News / information | 0.025725 | No | No | 1 |
| PPR | 3 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 0.025361 | No | No | 3 |
| PPR | 4 | 2400508 | Сегодня. Итоги с Олегом Панютой. | News / information | 0.022025 | No | No | 2 |
| PPR | 5 | 2400467 | 'Викна-Новости'. | News / information | 0.020931 | No | No | 2 |
| H + CF + ALS + PPR | 1 | 12001682 | М/с 'Губка Боб Квадратные Штаны'. | Children | 1.696602 | No | No | 3 |
| H + CF + ALS + PPR | 2 | 2400480 | ТСН. Неделя. | News / information | 1.694840 | No | No | 3 |
| H + CF + ALS + PPR | 3 | 200337 | 'Утро с 'Интером'. | Entertainment | 1.450676 | No | No | 4 |
| H + CF + ALS + PPR | 4 | 2400508 | Сегодня. Итоги с Олегом Панютой. | News / information | 1.272883 | No | No | 2 |
| H + CF + ALS + PPR | 5 | 2400467 | 'Викна-Новости'. | News / information | 1.188190 | No | No | 2 |

### 6.4. Per-user outcome comparison

| User | Method | AP@5 | Target hits | Any validation views | Categories | Previously seen | Popularity overlap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | Popularity | 0.000000 | 0 | 1 | 3 | 1 | 5 |
| B | Popularity | 0.000000 | 0 | 0 | 3 | 4 | 5 |
| A | History | 0.400000 | 2 | 3 | 1 | 5 | 0 |
| B | History | 0.146667 | 2 | 2 | 4 | 5 | 1 |
| A | History + schedule | 0.333333 | 2 | 4 | 1 | 5 | 1 |
| B | History + schedule | 0.000000 | 0 | 0 | 4 | 5 | 2 |
| A | History + time | 0.333333 | 2 | 3 | 1 | 5 | 0 |
| B | History + time | 0.146667 | 2 | 2 | 4 | 5 | 1 |
| A | History + schedule + time | 0.333333 | 2 | 4 | 1 | 5 | 1 |
| B | History + schedule + time | 0.000000 | 0 | 0 | 4 | 5 | 2 |
| A | Item CF | 0.050000 | 1 | 2 | 1 | 2 | 1 |
| B | Item CF | 0.000000 | 0 | 0 | 2 | 4 | 4 |
| A | H + CF | 0.400000 | 2 | 4 | 1 | 5 | 1 |
| B | H + CF | 0.040000 | 1 | 1 | 5 | 5 | 2 |
| A | ALS | 0.200000 | 2 | 3 | 1 | 4 | 1 |
| B | ALS | 0.000000 | 0 | 0 | 3 | 4 | 2 |
| A | H + CF + ALS | 0.520000 | 3 | 4 | 1 | 5 | 1 |
| B | H + CF + ALS | 0.000000 | 0 | 0 | 4 | 5 | 3 |
| A | PPR | 0.200000 | 2 | 3 | 1 | 5 | 1 |
| B | PPR | 0.000000 | 0 | 0 | 2 | 5 | 4 |
| A | H + CF + ALS + PPR | 0.520000 | 3 | 4 | 1 | 5 | 1 |
| B | H + CF + ALS + PPR | 0.000000 | 0 | 0 | 3 | 5 | 3 |

### 6.5. Successful and failed recommendations: mechanisms and experience

**User A: strong thematic consistency can still produce weak ranking.** Popularity offers three news IDs (2400480, 240081, 2400508), breakfast programme 20088, and the Children programme 12001682. None is a target: AP@5 is 0, although 12001682 is viewed during validation. History restores 12002856, “М/с 'Элвиннн!!! и бурундуки'.”, and 12001732, “М/с 'Пингвины из 'Мадагаскара'.”, at ranks 1 and 2, giving AP@5 0.40. Their train counts are 17 and 9. This is direct evidence for retaining repeat candidates rather than filtering all seen items.

Item CF recommends only Children programmes, yet reaches AP@5 0.05: it pushes historically unseen 12001734, 12002896, and 12002805 into three positions, while the only target hit, 12001732, is at rank 4. Audience similarity supplies plausible thematic discovery but fails to recover this user's most frequent future IDs. Category agreement alone is insufficient evidence of relevance.

The selected four-component hybrid puts targets 12002856 and 12001732 first and second, then places 12002809, “М/с 'Ниндзяго: Мастера Кружитцу'.”, at rank 5. Its three target hits give AP@5 **(1 + 1 + 3/5)/5 = 0.52**, matching the three-component hybrid. The fifth programme had only three train views, so this change goes beyond choosing the five largest user counts. Programme 12001682 at rank 3 is viewed but is outside the target five. Conversely 12002955, “М/с 'Свинка Пеппа', 1 с. 'Лужи'.”, had nine train views but no qualified validation view: its high history and schedule score is a concrete failed repeat prediction. The omitted targets 12002957 and 12002832 show that the hybrid is incomplete even for this stable category profile.

**User B: broad history is vulnerable to schedule and popularity amplification.** The held-out target set contains factual IDs 1100411 and 5200303, entertainment ID 500315, series ID 10001261, and film ID 90043056. History includes 1100411 and 5200303 at ranks 3 and 5, each with three train views. AP@5 is **((1/3) + (2/5))/5 = 0.146667**; History + Time achieves the same value. However its two first-ranked historical repeats, 200337 and 10003159, are not viewed in validation, so history also has clear failures.

Schedule weighting elevates Children programme 12001682 and news ID 2400480, resulting in zero target hits. The four-component hybrid recommends 12001682, 2400480, 200337, 2400508, and 2400467: all were in B's train history, but none has a qualified validation view. Its AP@5 is **0**, despite being the global winner. Three of its five IDs overlap the popularity list; PPR and Item CF overlap popularity on four IDs. This observed failure is consistent with repeated and broadly popular programmes overwhelming B's factual/series/film interests; the data does not establish an underlying causal preference change.

**Diversity and user experience.** For A, every personalised list contains one category; popularity spans three categories but performs worse. For B, H + CF spans five categories and scores 0.04, whereas History spans four categories and scores 0.146667; more category diversity alone does not ensure better MAP. Returning familiar titles can support continuing a viewing routine, while CF's unseen-in-history titles can support discovery. These are plausible experience implications of the displayed lists, not measured satisfaction effects. The global winner's failure on B argues for monitoring heterogeneous users; it does not validate an untested adaptive gating algorithm.

## Final Classical Strategy Choice

**I would select the implemented history + item-CF + ALS + PPR hybrid with schedule weighting and its existing popularity fallback as SWEET.TV's base recommendation strategy.** The fixed weights are **0.50 / 0.40 / 0.05 / 0.05** and schedule exponent **0.10**. The decision is based on the audited classical MAP@5 of **0.367811**, the strong lift over popularity, and the concrete recovery of A's repeated Children programmes, including lower-count 12002809. The three independent personalised methods satisfy the classical-method comparison independently of the additional learned scorer.

This choice is conditional on operational constraints, not on a claim that the most complicated mixture is always best. H + CF achieves **0.366323**, and H + CF + ALS **0.367395**, while PPR is the most expensive measured shared inference pass. Those already-implemented configurations are justified alternatives when the marginal 0.001489 or 0.000416 MAP is not worth refresh cost; no production latency threshold has been measured. History and CF provide an interpretable repeat/audience explanation, while latent factors and graph propagation add less transparent adjustments. Popularity provides a deterministic low-history fallback, but cannot personalise a truly new user, and the common catalog does not solve new-item cold start. The supported base catalog must be stated explicitly rather than presented as complete coverage of future television.

B is a direct counterexample to universal hybrid superiority: the selected mixture returns five non-viewed repeats and AP@5 0, while History reaches 0.146667. The result calls for monitoring users with diverse histories and considering a future independently tested policy change. It does not justify inventing or claiming to have evaluated such a policy in this project.

## Limitations and Verification Scope

These conclusions use one temporal holdout that was also used for parameter
selection. Two contrasting users illustrate mechanisms, not population-wide
satisfaction. The common catalog excludes future programmes without qualified
training history and covers 94.82% of held-out targets. Popularity concentration,
incomplete metadata, sparse histories and imperfect repeat predictions remain
limitations. A programme viewed outside the five metric targets is not a MAP hit;
absence of a hit is not evidence of dislike.

The original generation audit recorded 411 training records with post-cutoff
watching, and 318 removed after clipping. The published verifier recalculates MAP,
catalog coverage and case-study consistency from exported evidence; it does not
independently repeat raw interaction preparation or prove absence of temporal
leakage. The manifest records the historical audit and its source/input hashes.
Full preparation and training scripts remain outside this reduced Git package.

No new training, parameter search, online evaluation, revenue estimate or
statistical-significance test was performed for this English edition.

## Evidence and Verification

- [Package documentation](../README.md) and [standalone verifier](../verify_results.py).
- [Comparison](method_comparison.csv), [profiles](user_profiles.csv), [recommendations](user_recommendations.csv), and [user metrics](user_method_metrics.csv).
- [Train-history counts](selected_user_history.csv) and [selected targets](selected_user_targets.csv).
- [All validation rankings](validation_predictions.csv), [all validation targets](validation_targets.csv), [candidate catalog](candidate_catalog.csv), and [historical manifest](run_manifest.json).

Run `python business_analysis/verify_results.py` from the repository root.
