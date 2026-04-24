#!/usr/bin/env python3
"""Dermatovenerology akinator powered by a large knowledge base."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from knowledge_base import KNOWLEDGE_BASE, SOURCE_REFERENCES

TOP_RESULTS = 4
ADAPTIVE_MAX_QUESTIONS = 3
MIN_TOTAL_SIGNAL = 8
MIN_MATCHED_TAGS = 2
HIGH_SCORE_SINGLE_TAG = 55


@dataclass(frozen=True)
class Option:
    text: str
    tag_scores: Dict[str, int]


@dataclass(frozen=True)
class Question:
    key: str
    text: str
    options: List[Option]


BASE_QUESTIONS: List[Question] = [
    Question(
        key="location",
        text="Где в первую очередь локализованы изменения?",
        options=[
            Option("Аногенитальная зона", {"loc_genital": 4}),
            Option("Складки/пах/под молочными железами", {"loc_folds": 4}),
            Option("Кисти/запястья/межпальцевые промежутки", {"loc_hands_wrists": 4}),
            Option("Волосистая часть головы/волосы/ногти", {"loc_hair_scalp_nails": 4, "loc_scalp": 2}),
            Option("Лицо", {"loc_face": 4}),
            Option("Туловище/конечности", {"loc_trunk_limbs": 4}),
            Option("Ладони/подошвы", {"loc_palms_soles": 4, "loc_feet": 2}),
            Option("Другая локализация / затрудняюсь ответить", {}),
        ],
    ),
    Question(
        key="itch",
        text="Насколько выражен зуд?",
        options=[
            Option("Зуда нет", {"itch_none": 3}),
            Option("Умеренный зуд", {"itch_moderate": 3}),
            Option("Сильный зуд, особенно ночью", {"itch_night": 4}),
            Option("Затрудняюсь оценить / не подходит", {}),
        ],
    ),
    Question(
        key="pain",
        text="Есть ли боль, жжение или выраженная болезненность очагов?",
        options=[
            Option("Да", {"pain_yes": 3}),
            Option("Нет", {}),
            Option("Не уверен(а) / не подходит", {}),
        ],
    ),
    Question(
        key="lesion_type",
        text="Какая морфология преобладает?",
        options=[
            Option("Пузырьки/эрозии", {"lesion_vesicles": 4}),
            Option("Крупные пузыри", {"lesion_bullae": 4}),
            Option("Кольцевидные шелушащиеся очаги", {"lesion_annular_scale": 4}),
            Option("Четко очерченные бляшки с шелушением", {"lesion_sharply_demarcated_plaques": 4}),
            Option("Экзематозное воспаление/мокнутие", {"lesion_eczema": 4}),
            Option("Ярко-красные влажные очаги в складках", {"lesion_moist_erythema": 4, "lesion_eczema": 2}),
            Option("Папулы/ходы/расчесы", {"lesion_papules_burrows": 4}),
            Option("Папулы/пустулы (акнеформные)", {"lesion_papules_pustules": 4}),
            Option("Пустулы/корки/гной", {"lesion_pustules_crusts": 4}),
            Option("Волдыри (как крапивница)", {"lesion_wheals": 4}),
            Option("Язва/шанкр/глубокий дефект", {"lesion_ulcer": 4}),
            Option("Узел/опухолевидный рост", {"lesion_nodule_or_tumor": 4}),
            Option("Пигментное пятно/депигментация", {"lesion_pigment_change": 4}),
            Option("Ничего из перечисленного / смешанная картина", {}),
        ],
    ),
    Question(
        key="urogenital",
        text="Есть ли уретральные/вагинальные выделения или выраженное жжение/боль при мочеиспускании?",
        options=[
            Option("Да", {"discharge_dysuria_yes": 5}),
            Option("Нет", {}),
            Option("Не знаю / неприменимо", {}),
        ],
    ),
    Question(
        key="sex_risk",
        text="Если это применимо: был ли незащищенный сексуальный контакт за последние 3 месяца?",
        options=[
            Option("Да", {"sex_risk_yes": 4}),
            Option("Нет", {}),
            Option("Не уверен(а) / неприменимо", {}),
        ],
    ),
    Question(
        key="contact",
        text="У близких контактов есть похожие симптомы?",
        options=[
            Option("Да", {"contact_case_yes": 4}),
            Option("Нет", {}),
            Option("Не знаю", {}),
        ],
    ),
    Question(
        key="trigger",
        text="Есть связь с новым препаратом, косметикой, химией, латексом, бельем?",
        options=[
            Option("Да", {"trigger_new_product_yes": 4}),
            Option("Нет", {}),
            Option("Не знаю", {}),
        ],
    ),
    Question(
        key="systemic",
        text="Есть ли температура или общее выраженное недомогание?",
        options=[
            Option("Да", {"fever_yes": 3}),
            Option("Нет", {}),
            Option("Не знаю / не измерял(а)", {}),
        ],
    ),
    Question(
        key="mucosa",
        text="Задействованы слизистые (рот/гениталии/глаза)?",
        options=[
            Option("Да", {"lesion_mucosal_involvement": 4}),
            Option("Нет", {}),
            Option("Не знаю / неприменимо", {}),
        ],
    ),
    Question(
        key="distribution",
        text="Как распределены очаги?",
        options=[
            Option("Преимущественно симметрично с обеих сторон", {"symmetric_distribution_yes": 3}),
            Option("Преимущественно односторонне/локально", {}),
            Option("Сложно оценить / не подходит", {}),
        ],
    ),
    Question(
        key="palms_soles_rash",
        text="Есть ли элементы сыпи на ладонях или подошвах (именно сыпь, не только сухость)?",
        options=[
            Option("Да", {"palms_soles_rash_yes": 4, "loc_palms_soles": 2}),
            Option("Нет", {}),
            Option("Не знаю / не осматривал(а)", {}),
        ],
    ),
    Question(
        key="inguinal_nodes",
        text="Есть ли увеличенные/болезненные паховые лимфоузлы?",
        options=[
            Option("Да", {"inguinal_nodes_yes": 4}),
            Option("Нет", {}),
            Option("Не знаю", {}),
        ],
    ),
    Question(
        key="prior_antifungal",
        text="Было ли явное улучшение на противогрибковых средствах ранее?",
        options=[
            Option("Да", {"prior_antifungal_helped_yes": 4}),
            Option("Нет/ухудшение", {}),
            Option("Не применял(а) / не знаю", {}),
        ],
    ),
    Question(
        key="atopy",
        text="Есть личный/семейный атопический фон (атопический дерматит, астма, аллергический ринит)?",
        options=[
            Option("Да", {"family_atopy_yes": 4}),
            Option("Нет", {}),
            Option("Не знаю", {}),
        ],
    ),
    Question(
        key="ulcer_pain",
        text="Если есть язва/эрозия: она болезненная или нет?",
        options=[
            Option("Болезненная", {"ulcer_painful_yes": 4, "pain_yes": 1}),
            Option("Безболезненная", {"ulcer_painless_yes": 4}),
            Option("Нет язвы/эрозии или не знаю", {}),
        ],
    ),
    Question(
        key="wheal_behavior",
        text="Если есть волдыри: они исчезают в пределах ~24 часов и появляются в новых местах?",
        options=[
            Option("Да", {"wheals_transient_yes": 4}),
            Option("Нет", {}),
            Option("Волдырей нет / не знаю", {}),
        ],
    ),
    Question(
        key="comedones",
        text="Есть комедоны (черные/белые точки)?",
        options=[
            Option("Да", {"comedones_yes": 4}),
            Option("Нет", {}),
            Option("Не знаю / не уверен(а)", {}),
        ],
    ),
    Question(
        key="chronic",
        text="Какой характер течения лучше подходит?",
        options=[
            Option("Острое (до 2 недель, без рецидивов)", {}),
            Option("Подострое (2-6 недель)", {}),
            Option("Хроническое/рецидивирующее (дольше 6 недель или повторяется)", {"chronic_recurrent_yes": 3}),
            Option("Не знаю", {}),
        ],
    ),
]


ADAPTIVE_QUESTIONS: List[Question] = [
    Question(
        key="grouped_vesicles",
        text="Есть ли сгруппированные болезненные пузырьки/эрозии в аногенитальной зоне (типично для HSV)?",
        options=[
            Option("Да", {"grouped_vesicles_yes": 5, "lesion_vesicles": 2}),
            Option("Нет", {}),
            Option("Неприменимо", {}),
        ],
    ),
    Question(
        key="painless_chancre",
        text="Есть ли плотная безболезненная язва (тип шанкра)?",
        options=[
            Option("Да", {"painless_chancre_yes": 5, "ulcer_painless_yes": 3}),
            Option("Нет", {}),
            Option("Неприменимо", {}),
        ],
    ),
    Question(
        key="scaly_border",
        text="Есть ли активный приподнятый шелушащийся край очага?",
        options=[
            Option("Да", {"active_scaly_border_yes": 4}),
            Option("Нет", {}),
            Option("Неприменимо", {}),
        ],
    ),
    Question(
        key="satellite_pustules",
        text="Есть ли сателлитные пустулы/эрозии вокруг влажного очага в складке?",
        options=[
            Option("Да", {"candidal_satellite_yes": 4, "lesion_moist_erythema": 2}),
            Option("Нет", {}),
            Option("Неприменимо", {}),
        ],
    ),
    Question(
        key="silvery_scale",
        text="На бляшках есть плотное серебристое шелушение?",
        options=[
            Option("Да", {"silvery_scale_yes": 4}),
            Option("Нет", {}),
            Option("Неприменимо", {}),
        ],
    ),
    Question(
        key="dermatomal_pain",
        text="Была жгучая/стреляющая боль по ходу нерва до высыпаний (односторонне)?",
        options=[
            Option("Да", {"dermatomal_pain_yes": 5}),
            Option("Нет", {}),
            Option("Неприменимо", {}),
        ],
    ),
]

ADAPTIVE_QUESTION_GATES: Dict[str, List[str]] = {
    "grouped_vesicles": ["loc_genital", "lesion_vesicles", "lesion_ulcer"],
    "painless_chancre": ["loc_genital", "lesion_ulcer"],
    "scaly_border": ["lesion_annular_scale", "loc_folds", "loc_feet", "loc_scalp"],
    "satellite_pustules": ["lesion_moist_erythema", "loc_folds"],
    "silvery_scale": ["lesion_sharply_demarcated_plaques", "chronic_recurrent_yes", "loc_palms_soles"],
    "dermatomal_pain": ["lesion_vesicles", "pain_yes", "loc_trunk_limbs"],
}

BASE_QUESTION_GATES: Dict[str, List[str]] = {
    "palms_soles_rash": ["loc_palms_soles", "sex_risk_yes", "lesion_ulcer"],
    "inguinal_nodes": ["loc_genital", "sex_risk_yes", "lesion_ulcer", "discharge_dysuria_yes"],
    "prior_antifungal": ["lesion_annular_scale", "lesion_moist_erythema", "loc_folds", "loc_feet", "loc_scalp"],
    "atopy": ["lesion_eczema", "itch_moderate", "itch_night", "trigger_new_product_yes"],
    "ulcer_pain": ["lesion_ulcer"],
    "wheal_behavior": ["lesion_wheals"],
    "comedones": ["lesion_papules_pustules", "loc_face", "loc_trunk_limbs"],
}


def ask(question: Question) -> Option:
    print(f"\n{question.text}")
    for i, option in enumerate(question.options, start=1):
        print(f"  {i}. {option.text}")
    while True:
        raw = input("Введите номер варианта: ").strip()
        if not raw.isdigit():
            print("Нужна цифра варианта. Попробуйте снова.")
            continue
        index = int(raw) - 1
        if 0 <= index < len(question.options):
            return question.options[index]
        print("Такого варианта нет. Попробуйте снова.")


def should_ask_question(question: Question, user_tags: Dict[str, int], gates: Dict[str, List[str]] | None = None) -> bool:
    if not gates:
        return True
    required_tags = gates.get(question.key)
    if not required_tags:
        return True
    return any(tag in user_tags for tag in required_tags)


def collect_tag_scores(
    questions: List[Question],
    user_tags: Dict[str, int] | None = None,
    gates: Dict[str, List[str]] | None = None,
) -> Dict[str, int]:
    if user_tags is None:
        user_tags = {}
    for question in questions:
        if not should_ask_question(question, user_tags, gates):
            continue
        selected = ask(question)
        for tag, score in selected.tag_scores.items():
            user_tags[tag] = user_tags.get(tag, 0) + score
    return user_tags


def compute_condition_scores(user_tags: Dict[str, int]) -> List[Tuple[dict, float, List[str]]]:
    if sum(user_tags.values()) < MIN_TOTAL_SIGNAL:
        return []

    results: List[Tuple[dict, float, List[str]]] = []
    for condition in KNOWLEDGE_BASE.values():
        raw_score = 0.0
        matched_tags: List[str] = []
        positive_weight_tags = 0
        for tag, weight in condition["tag_weights"].items():
            if weight > 0:
                positive_weight_tags += 1
            if tag in user_tags:
                contribution = user_tags[tag] * weight
                raw_score += contribution
                if contribution > 0:
                    matched_tags.append(tag)

        if raw_score <= 0:
            continue

        # Coverage factor improves precision for top-1: broad matches rank lower
        # than conditions that match multiple specific markers.
        denom = max(positive_weight_tags, 1)
        coverage = min(len(matched_tags) / denom, 1.0)
        final_score = raw_score * (0.7 + 0.3 * coverage)
        # Require at least two supporting features unless score is very strong.
        if len(matched_tags) < MIN_MATCHED_TAGS and final_score < HIGH_SCORE_SINGLE_TAG:
            continue
        results.append((condition, final_score, matched_tags))

    results.sort(key=lambda item: (item[1], len(item[2])), reverse=True)
    return results


def question_discrimination(question: Question, candidates: List[dict]) -> float:
    option_ranges: List[float] = []
    for option in question.options:
        impacts: List[float] = []
        for condition in candidates:
            impact = 0.0
            for tag, score in option.tag_scores.items():
                impact += score * condition["tag_weights"].get(tag, 0)
            impacts.append(impact)
        if impacts:
            option_ranges.append(max(impacts) - min(impacts))
    return max(option_ranges) if option_ranges else 0.0


def pick_adaptive_questions(
    results: List[Tuple[dict, float, List[str]]], user_tags: Dict[str, int], max_questions: int
) -> List[Question]:
    if len(results) < 2:
        return []
    candidate_conditions = [condition for condition, _score, _tags in results[:3]]
    scored_questions: List[Tuple[Question, float]] = []
    for question in ADAPTIVE_QUESTIONS:
        gate = ADAPTIVE_QUESTION_GATES.get(question.key, [])
        if gate and not any(tag in user_tags for tag in gate):
            continue
        score = question_discrimination(question, candidate_conditions)
        if score > 0:
            scored_questions.append((question, score))
    scored_questions.sort(key=lambda item: item[1], reverse=True)
    return [question for question, _score in scored_questions[:max_questions]]


def adaptive_question_count(results: List[Tuple[dict, float, List[str]]]) -> int:
    if len(results) < 2:
        return 0
    margin = results[0][1] - results[1][1]
    if margin < 8:
        return 3
    if margin < 16:
        return 2
    return 1


def humanize_tag(tag: str) -> str:
    mapping = {
        "loc_genital": "аногенитальная локализация",
        "loc_folds": "локализация в складках",
        "loc_hands_wrists": "локализация на кистях/запястьях",
        "loc_hair_scalp_nails": "вовлечение волос/ногтей",
        "loc_scalp": "локализация на коже головы",
        "loc_face": "локализация на лице",
        "loc_trunk_limbs": "локализация на туловище/конечностях",
        "loc_palms_soles": "локализация на ладонях/подошвах",
        "loc_feet": "локализация на стопах",
        "itch_none": "отсутствие зуда",
        "itch_moderate": "умеренный зуд",
        "itch_night": "ночной зуд",
        "pain_yes": "болезненность",
        "lesion_vesicles": "пузырьки/эрозии",
        "lesion_bullae": "крупные пузыри",
        "lesion_annular_scale": "кольцевидные шелушащиеся очаги",
        "lesion_sharply_demarcated_plaques": "четкие шелушащиеся бляшки",
        "lesion_eczema": "экзематозная морфология",
        "lesion_moist_erythema": "влажные эритематозные очаги в складках",
        "lesion_papules_burrows": "папулы/ходы/расчесы",
        "lesion_papules_pustules": "акнеформные папуло-пустулы",
        "lesion_pustules_crusts": "пустулы/корки",
        "lesion_wheals": "волдыри",
        "lesion_ulcer": "язвенный элемент",
        "lesion_nodule_or_tumor": "узел/опухолевидный элемент",
        "lesion_pigment_change": "пигментные изменения",
        "discharge_dysuria_yes": "выделения/дизурия",
        "sex_risk_yes": "незащищенный половой контакт",
        "contact_case_yes": "наличие похожих симптомов у контактов",
        "trigger_new_product_yes": "связь с новым триггером",
        "fever_yes": "системные проявления/лихорадка",
        "lesion_mucosal_involvement": "поражение слизистых",
        "ulcer_painful_yes": "болезненная язва/эрозия",
        "ulcer_painless_yes": "безболезненная язва/эрозия",
        "wheals_transient_yes": "волдыри транзиторные (<24ч)",
        "comedones_yes": "наличие комедонов",
        "grouped_vesicles_yes": "сгруппированные болезненные пузырьки",
        "painless_chancre_yes": "типичный безболезненный шанкр",
        "active_scaly_border_yes": "активный шелушащийся край очага",
        "candidal_satellite_yes": "сателлитные элементы вокруг влажного очага",
        "silvery_scale_yes": "серебристое шелушение бляшек",
        "dermatomal_pain_yes": "односторонняя дерматомная боль до сыпи",
        "symmetric_distribution_yes": "симметричное распределение очагов",
        "palms_soles_rash_yes": "сыпь на ладонях/подошвах",
        "inguinal_nodes_yes": "паховая лимфаденопатия",
        "prior_antifungal_helped_yes": "улучшение на антимикотиках",
        "family_atopy_yes": "атопический фон",
        "chronic_recurrent_yes": "хроническое/рецидивирующее течение",
    }
    return mapping.get(tag, tag)


def show_sources() -> None:
    print("\nИспользованные источники для базы знаний:")
    for item in SOURCE_REFERENCES:
        print(f"- {item}")


def confidence_assessment(results: List[Tuple[dict, float, List[str]]], user_tags: Dict[str, int]) -> Tuple[str, str]:
    if not results:
        return "низкая", "нет достаточных данных для ранжирования"

    total_signal = sum(user_tags.values())
    top_score = results[0][1]
    top_matches = len(results[0][2])
    second_score = results[1][1] if len(results) > 1 else 0.0
    margin = top_score - second_score

    if total_signal < 14:
        return "низкая", f"мало информативных ответов (суммарный сигнал: {total_signal})"
    if top_score >= 70 and margin >= 15 and top_matches >= 4:
        return "высокая", f"выраженный отрыв от 2-го места ({margin:.1f}) и много совпавших признаков ({top_matches})"
    if top_score >= 45 and margin >= 7 and top_matches >= 3:
        return "средняя", f"есть отрыв от 2-го места ({margin:.1f}), но часть признаков неспецифична"
    return "низкая", f"небольшой отрыв от 2-го места ({margin:.1f}) или мало специфичных совпадений ({top_matches})"


def show_result(results: List[Tuple[dict, float, List[str]]], user_tags: Dict[str, int]) -> None:
    print("\n" + "=" * 84)
    print("РЕЗУЛЬТАТ (большая база знаний: дерматология + ИППП, предварительная гипотеза)")
    print("=" * 84)

    if not results:
        print("Недостаточно данных для ранжирования. Нужен очный осмотр и базовая диагностика.")
        return

    top = results[:TOP_RESULTS]
    print(f"\nПроанализировано состояний: {len(KNOWLEDGE_BASE)}")
    if TOP_RESULTS == 1:
        print("Наиболее вероятный вариант:")
    else:
        print(f"Топ-{TOP_RESULTS} вероятных вариантов:")

    confidence, confidence_reason = confidence_assessment(results, user_tags)
    print(f"\nУверенность модели: {confidence}")
    print(f"Почему так: {confidence_reason}")

    for idx, (condition, score, matched_tags) in enumerate(top, start=1):
        print(f"\n{idx}) {condition['title']} [{condition['icd10']}]")
        print(f"   Категория: {condition['category']}")
        print(f"   Скоринг: {score:.1f}")
        print(f"   Клиническая логика: {condition['summary']}")
        if matched_tags:
            reasons = ", ".join(humanize_tag(tag) for tag in matched_tags[:4])
            print(f"   Совпавшие признаки: {reasons}")
        print("   Что подтвердить:")
        for test in condition["tests"][:3]:
            print(f"   - {test}")
        print("   Первичная тактика:")
        for item in condition["recommendations"][:3]:
            print(f"   - {item}")

    alert_categories = {"ИППП", "Новообразования", "Буллезные/аутоиммунные"}
    critical = [item for item in top if item[0]["category"] in alert_categories]
    if critical:
        print("\nВНИМАНИЕ: в топе есть состояния, требующие ускоренной очной верификации.")
        print("Не откладывайте очный прием и лабораторную/морфологическую диагностику.")


def main() -> None:
    print("Дермато-Венеро Акинатор (knowledge-base edition)")
    print("-" * 84)
    print("Скрининговый инструмент для предварительного клинического ориентирования.")
    print("Не является медицинским заключением и не заменяет очный прием.")
    print(f"Размер базы знаний: {len(KNOWLEDGE_BASE)} состояний.")
    show_sources()

    user_tags = collect_tag_scores(BASE_QUESTIONS, gates=BASE_QUESTION_GATES)
    initial_results = compute_condition_scores(user_tags)

    # Adaptive phase: ask only questions that better separate current leaders.
    count = min(adaptive_question_count(initial_results), ADAPTIVE_MAX_QUESTIONS)
    adaptive = pick_adaptive_questions(initial_results, user_tags, count)
    if adaptive:
        print(f"\nУточняющий этап: {len(adaptive)} вопрос(а) для повышения точности.")
        user_tags = collect_tag_scores(adaptive, user_tags=user_tags)

    results = compute_condition_scores(user_tags)
    show_result(results, user_tags)

    print("\nЕсли есть быстрое ухудшение, высокая температура, поражение слизистых,")
    print("некроз/распространенные буллы, беременность или иммунодефицит - срочно к врачу.")


if __name__ == "__main__":
    main()
