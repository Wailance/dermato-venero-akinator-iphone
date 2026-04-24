"""Large dermatovenerology knowledge base for triage-style scoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


SOURCE_REFERENCES: List[str] = [
    "WHO ICD-10 (dermatology blocks L00-L99): https://icd.who.int/browse10/2016/en#/L00-L99",
    "WHO ICD-10 (venereal diseases A50-A64): https://icd.who.int/browse10/2016/en#/A50-A64",
    "CDC STI Treatment Guidelines 2021: https://www.cdc.gov/std/treatment-guidelines/default.htm",
    "DermNet diagnostic index: https://dermnetnz.org/topics",
]


@dataclass(frozen=True)
class Profile:
    summary: str
    tests: List[str]
    recommendations: List[str]
    tag_weights: Dict[str, int]


PROFILES: Dict[str, Profile] = {
    "sti_ulcerative": Profile(
        summary="Возможна ИППП с язвенно-эрозивным синдромом.",
        tests=[
            "NAAT/ПЦР из очага при наличии активных элементов",
            "Серология сифилиса (RPR/VDRL + трепонемный тест)",
            "Скрининг на ВИЧ, HBV, HCV по показаниям",
        ],
        recommendations=[
            "Очный осмотр дерматовенеролога в ближайшее время",
            "Партнер-уведомление и временное воздержание до верификации",
            "Лечение только после клинического подтверждения и протокола региона",
        ],
        tag_weights={
            "loc_genital": 3,
            "lesion_ulcer": 4,
            "lesion_vesicles": 3,
            "pain_yes": 2,
            "sex_risk_yes": 3,
            "fever_yes": 1,
        },
    ),
    "sti_discharge": Profile(
        summary="Вероятен уретрит/цервицит инфекционной природы.",
        tests=[
            "NAAT на N. gonorrhoeae и C. trachomatis",
            "Тест на M. genitalium по показаниям",
            "Скрининг на ВИЧ и сифилис",
        ],
        recommendations=[
            "Эмпирическая терапия по локальным клинрекомендациям",
            "Лечение и тестирование половых партнеров",
            "Контроль симптомов и тест-of-cure по показаниям",
        ],
        tag_weights={
            "loc_genital": 3,
            "discharge_dysuria_yes": 5,
            "sex_risk_yes": 3,
            "pain_yes": 1,
            "fever_yes": 1,
        },
    ),
    "scabies_like": Profile(
        summary="Паразитарный зудящий дерматоз, часто с контактной передачей.",
        tests=[
            "Дерматоскопия/микроскопия соскоба при возможности",
            "Оценка бытовых и половых контактов",
        ],
        recommendations=[
            "Лечить пациента и тесные контакты одновременно",
            "Санобработка текстиля и постельных принадлежностей",
            "Контроль через 1-2 недели",
        ],
        tag_weights={
            "loc_hands_wrists": 3,
            "itch_night": 5,
            "contact_case_yes": 4,
            "lesion_papules_burrows": 4,
            "loc_genital": 1,
        },
    ),
    "fungal_ring": Profile(
        summary="Вероятный дерматомикоз с кольцевидными/шелушащимися очагами.",
        tests=[
            "КОН-тест/микроскопия соскоба",
            "Посев грибов при атипичном/рецидивирующем течении",
        ],
        recommendations=[
            "Топический антимикотик по очной схеме",
            "При распространении рассмотреть системную терапию",
            "Исключить источник реинфекции (обувь, животные, спортзалы)",
        ],
        tag_weights={
            "lesion_annular_scale": 5,
            "itch_moderate": 2,
            "loc_folds": 2,
            "loc_feet": 3,
            "loc_scalp": 2,
            "loc_trunk_limbs": 1,
        },
    ),
    "candida_fold": Profile(
        summary="Вероятен кандидоз складок/слизистых.",
        tests=[
            "Микроскопия/посев при возможности",
            "Оценка фоновых факторов (диабет, иммуносупрессия, антибиотики)",
        ],
        recommendations=[
            "Топические азолы/нистатин по очной схеме",
            "Снижение окклюзии, тщательная сушка складок",
            "Коррекция метаболических факторов риска",
        ],
        tag_weights={
            "loc_folds": 4,
            "loc_genital": 3,
            "itch_moderate": 2,
            "lesion_moist_erythema": 5,
            "discharge_dysuria_yes": 1,
        },
    ),
    "psoriasiform": Profile(
        summary="Псориазиформный воспалительный дерматоз.",
        tests=[
            "Клиническая оценка BSA/PASI",
            "Скрининг псориатического артрита",
            "Биопсия при диагностических сомнениях",
        ],
        recommendations=[
            "Топическая противовоспалительная терапия по протоколу",
            "Эмоленты и контроль триггеров",
            "При среднетяжелом/тяжелом течении рассмотреть системное лечение",
        ],
        tag_weights={
            "lesion_sharply_demarcated_plaques": 5,
            "loc_scalp": 2,
            "loc_extensors": 3,
            "itch_moderate": 1,
            "chronic_recurrent_yes": 2,
            "loc_folds": 2,
            "loc_palms_soles": 2,
        },
    ),
    "eczematous": Profile(
        summary="Экзематозный дерматит (атопический/контактный/дисгидротический).",
        tests=[
            "Клиническая оценка и исключение микоза/чесотки",
            "Patch-тесты при подозрении на аллерген",
        ],
        recommendations=[
            "Исключить триггер и восстановить барьер кожи",
            "Топические стероиды/ингибиторы кальциневрина по показаниям",
            "Эмоленты и контроль рецидивов",
        ],
        tag_weights={
            "itch_moderate": 3,
            "itch_night": 2,
            "trigger_new_product_yes": 4,
            "loc_hands_wrists": 2,
            "loc_face": 1,
            "lesion_eczema": 4,
            "chronic_recurrent_yes": 1,
        },
    ),
    "bacterial_pyoderma": Profile(
        summary="Бактериальная кожная инфекция (пиодермия/целлюлитный спектр).",
        tests=[
            "Клиническая оценка глубины инфекции",
            "Посев отделяемого/гноя при наличии",
            "ОАК/CRP при системной реакции",
        ],
        recommendations=[
            "Локальная или системная антибактериальная терапия по протоколу",
            "Оценка показаний к хирургической обработке",
            "Контроль динамики через 24-72 часа",
        ],
        tag_weights={
            "lesion_pustules_crusts": 4,
            "pain_yes": 3,
            "fever_yes": 2,
            "loc_face": 1,
            "loc_trunk_limbs": 2,
        },
    ),
    "viral_exanthem": Profile(
        summary="Вероятная вирусная экзантема/везикулезный дерматоз.",
        tests=[
            "Клиническая верификация + ПЦР при атипичном течении",
            "Оценка эпидконтактов",
        ],
        recommendations=[
            "Изоляционные меры при контагиозных инфекциях",
            "Симптоматическая терапия",
            "При тяжелом течении - госпитализация по показаниям",
        ],
        tag_weights={
            "fever_yes": 3,
            "lesion_vesicles": 3,
            "lesion_pustules_crusts": 2,
            "loc_trunk_limbs": 2,
            "loc_face": 1,
            "contact_case_yes": 1,
        },
    ),
    "urticaria_drug": Profile(
        summary="Острая аллергическая/лекарственная кожная реакция.",
        tests=[
            "Анамнез новых препаратов/экспозиций",
            "Оценка системного поражения (слизистые, температура, печеночные тесты)",
        ],
        recommendations=[
            "Отмена подозреваемого триггера",
            "Антигистаминные, при необходимости системные ГКС по схеме",
            "Срочная помощь при признаках анафилаксии/тяжелой кожной реакции",
        ],
        tag_weights={
            "trigger_new_product_yes": 3,
            "lesion_wheals": 5,
            "itch_moderate": 2,
            "fever_yes": 1,
            "lesion_mucosal_involvement": 3,
        },
    ),
    "bullous_autoimmune": Profile(
        summary="Возможный аутоиммунный буллезный дерматоз.",
        tests=[
            "Биопсия кожи + прямой иммуннофлюоресцентный тест",
            "Серологические аутоантитела по показаниям",
        ],
        recommendations=[
            "Срочная консультация дерматолога",
            "Системная иммуносупрессивная терапия по подтвержденному диагнозу",
            "Профилактика инфекционных осложнений и уход за кожей",
        ],
        tag_weights={
            "lesion_vesicles": 3,
            "lesion_bullae": 5,
            "pain_yes": 2,
            "lesion_mucosal_involvement": 3,
            "chronic_recurrent_yes": 1,
        },
    ),
    "acneiform": Profile(
        summary="Акнеформный дерматоз/фолликулярное воспаление.",
        tests=[
            "Клиническая оценка степени тяжести",
            "Гормональная оценка по показаниям",
        ],
        recommendations=[
            "Базовый уход и комедонолитическая терапия",
            "Топические ретиноиды/бензоилпероксид +/- антибиотик по схеме",
            "Системная терапия при тяжелом течении",
        ],
        tag_weights={
            "loc_face": 3,
            "loc_trunk_limbs": 1,
            "lesion_papules_pustules": 4,
            "chronic_recurrent_yes": 2,
            "pain_yes": 1,
        },
    ),
    "pigmentary": Profile(
        summary="Пигментное нарушение (депигментация/гиперпигментация).",
        tests=[
            "Осмотр в лампе Вуда по показаниям",
            "Оценка эндокринных/поствоспалительных причин",
        ],
        recommendations=[
            "Фотозащита ежедневно",
            "Локальная терапия по типу пигментного нарушения",
            "Контроль динамики в дерматологическом наблюдении",
        ],
        tag_weights={
            "lesion_pigment_change": 5,
            "loc_face": 2,
            "loc_trunk_limbs": 1,
            "itch_none": 2,
            "chronic_recurrent_yes": 1,
        },
    ),
    "neoplasm_alert": Profile(
        summary="Новообразование кожи, требующее дерматоонкологической верификации.",
        tests=[
            "Дерматоскопия",
            "Эксцизионная/инцизионная биопсия по показаниям",
        ],
        recommendations=[
            "Не затягивать очную консультацию",
            "Оценка ABCDE-критериев/роста/кровоточивости",
            "Маршрутизация к онкодерматологу при подозрении на злокачественность",
        ],
        tag_weights={
            "lesion_nodule_or_tumor": 5,
            "lesion_ulcer": 2,
            "pain_yes": 1,
            "chronic_recurrent_yes": 1,
            "loc_face": 1,
            "loc_trunk_limbs": 1,
        },
    ),
    "hair_nail": Profile(
        summary="Патология волос/ногтей.",
        tests=[
            "Трихоскопия/дерматоскопия по показаниям",
            "Микология ногтя/волос при подозрении на грибковую этиологию",
            "Лабораторный скрининг дефицитов и эндокринных причин",
        ],
        recommendations=[
            "Этиотропная терапия после уточнения причины",
            "Длительное наблюдение из-за медленной динамики",
            "Коррекция сопутствующих факторов (стресс, дефициты, уход)",
        ],
        tag_weights={
            "loc_hair_scalp_nails": 5,
            "chronic_recurrent_yes": 2,
            "itch_moderate": 1,
            "loc_scalp": 2,
            "loc_feet": 1,
        },
    ),
}


RAW_CONDITIONS: List[Dict[str, str]] = [
    # STI and venereology
    {"key": "genital_herpes", "title": "Генитальный герпес (HSV-1/2)", "icd10": "A60.0", "profile": "sti_ulcerative", "category": "ИППП"},
    {"key": "syphilis_primary", "title": "Сифилис первичный", "icd10": "A51.0", "profile": "sti_ulcerative", "category": "ИППП"},
    {"key": "syphilis_secondary", "title": "Сифилис вторичный", "icd10": "A51.4", "profile": "sti_ulcerative", "category": "ИППП"},
    {"key": "gonococcal_urethritis", "title": "Гонококковый уретрит", "icd10": "A54.0", "profile": "sti_discharge", "category": "ИППП"},
    {"key": "chlamydial_infection", "title": "Хламидийная урогенитальная инфекция", "icd10": "A56.0", "profile": "sti_discharge", "category": "ИППП"},
    {"key": "mycoplasma_genitalium", "title": "Урогенитальная инфекция M. genitalium", "icd10": "A49.3", "profile": "sti_discharge", "category": "ИППП"},
    {"key": "trichomoniasis", "title": "Трихомониаз урогенитальный", "icd10": "A59.0", "profile": "sti_discharge", "category": "ИППП"},
    {"key": "lymphogranuloma_venereum", "title": "Лимфогранулема венерическая", "icd10": "A55", "profile": "sti_ulcerative", "category": "ИППП"},
    {"key": "chancroid", "title": "Мягкий шанкр", "icd10": "A57", "profile": "sti_ulcerative", "category": "ИППП"},
    {"key": "granuloma_inguinale", "title": "Паховая гранулема (донованоз)", "icd10": "A58", "profile": "sti_ulcerative", "category": "ИППП"},
    {"key": "anogenital_warts", "title": "Аногенитальные бородавки (HPV)", "icd10": "A63.0", "profile": "sti_ulcerative", "category": "ИППП"},
    {"key": "molluscum_genital", "title": "Контагиозный моллюск (аногенитальный)", "icd10": "B08.1", "profile": "viral_exanthem", "category": "ИППП"},
    {"key": "pediculosis_pubis", "title": "Лобковый педикулез", "icd10": "B85.3", "profile": "scabies_like", "category": "ИППП"},
    # Mycoses and yeast
    {"key": "tinea_corporis", "title": "Дерматофития гладкой кожи (tinea corporis)", "icd10": "B35.4", "profile": "fungal_ring", "category": "Микозы"},
    {"key": "tinea_cruris", "title": "Паховая дерматофития (tinea cruris)", "icd10": "B35.6", "profile": "fungal_ring", "category": "Микозы"},
    {"key": "tinea_pedis", "title": "Микоз стоп (tinea pedis)", "icd10": "B35.3", "profile": "fungal_ring", "category": "Микозы"},
    {"key": "tinea_manuum", "title": "Микоз кистей (tinea manuum)", "icd10": "B35.2", "profile": "fungal_ring", "category": "Микозы"},
    {"key": "tinea_capitis", "title": "Микоз волосистой части головы (tinea capitis)", "icd10": "B35.0", "profile": "fungal_ring", "category": "Микозы"},
    {"key": "tinea_barbae", "title": "Микоз бороды и усов (tinea barbae)", "icd10": "B35.0", "profile": "fungal_ring", "category": "Микозы"},
    {"key": "onychomycosis", "title": "Онихомикоз", "icd10": "B35.1", "profile": "hair_nail", "category": "Микозы"},
    {"key": "candidal_intertrigo", "title": "Кандидоз складок (интертриго)", "icd10": "B37.2", "profile": "candida_fold", "category": "Микозы"},
    {"key": "vulvovaginal_candidiasis", "title": "Вульвовагинальный кандидоз", "icd10": "B37.3", "profile": "candida_fold", "category": "Микозы"},
    {"key": "balanitis_candida", "title": "Кандидозный баланит", "icd10": "B37.4", "profile": "candida_fold", "category": "Микозы"},
    {"key": "pityriasis_versicolor", "title": "Отрубевидный лишай", "icd10": "B36.0", "profile": "fungal_ring", "category": "Микозы"},
    # Eczematous and inflammatory
    {"key": "atopic_dermatitis", "title": "Атопический дерматит", "icd10": "L20.9", "profile": "eczematous", "category": "Экзема/дерматит"},
    {"key": "allergic_contact_dermatitis", "title": "Аллергический контактный дерматит", "icd10": "L23.9", "profile": "eczematous", "category": "Экзема/дерматит"},
    {"key": "irritant_contact_dermatitis", "title": "Ирритантный контактный дерматит", "icd10": "L24.9", "profile": "eczematous", "category": "Экзема/дерматит"},
    {"key": "seborrheic_dermatitis", "title": "Себорейный дерматит", "icd10": "L21.9", "profile": "eczematous", "category": "Экзема/дерматит"},
    {"key": "nummular_eczema", "title": "Монетовидная экзема", "icd10": "L30.0", "profile": "eczematous", "category": "Экзема/дерматит"},
    {"key": "dyshidrotic_eczema", "title": "Дисгидротическая экзема", "icd10": "L30.1", "profile": "eczematous", "category": "Экзема/дерматит"},
    {"key": "stasis_dermatitis", "title": "Стаз-дерматит", "icd10": "I83.1", "profile": "eczematous", "category": "Экзема/дерматит"},
    {"key": "lichen_simplex", "title": "Ограниченный нейродермит (lichen simplex)", "icd10": "L28.0", "profile": "eczematous", "category": "Экзема/дерматит"},
    {"key": "prurigo", "title": "Пруриго", "icd10": "L28.2", "profile": "eczematous", "category": "Экзема/дерматит"},
    # Psoriasiform and papulosquamous
    {"key": "plaque_psoriasis", "title": "Псориаз вульгарный (бляшечный)", "icd10": "L40.0", "profile": "psoriasiform", "category": "Папулосквамозные"},
    {"key": "guttate_psoriasis", "title": "Псориаз каплевидный", "icd10": "L40.4", "profile": "psoriasiform", "category": "Папулосквамозные"},
    {"key": "inverse_psoriasis", "title": "Псориаз инверсный", "icd10": "L40.8", "profile": "psoriasiform", "category": "Папулосквамозные"},
    {"key": "palmoplantar_psoriasis", "title": "Пальмоплантарный псориаз", "icd10": "L40.3", "profile": "psoriasiform", "category": "Папулосквамозные"},
    {"key": "pustular_psoriasis", "title": "Псориаз пустулезный", "icd10": "L40.1", "profile": "psoriasiform", "category": "Папулосквамозные"},
    {"key": "lichen_planus", "title": "Красный плоский лишай", "icd10": "L43.9", "profile": "psoriasiform", "category": "Папулосквамозные"},
    {"key": "pityriasis_rosea", "title": "Розовый лишай Жибера", "icd10": "L42", "profile": "psoriasiform", "category": "Папулосквамозные"},
    {"key": "prp", "title": "Красный волосяной отрубевидный лишай (PRP)", "icd10": "L44.0", "profile": "psoriasiform", "category": "Папулосквамозные"},
    # Bacterial infections
    {"key": "impetigo", "title": "Импетиго", "icd10": "L01.0", "profile": "bacterial_pyoderma", "category": "Бактериальные"},
    {"key": "ecthyma", "title": "Эктима", "icd10": "L08.0", "profile": "bacterial_pyoderma", "category": "Бактериальные"},
    {"key": "erysipelas", "title": "Рожа", "icd10": "A46", "profile": "bacterial_pyoderma", "category": "Бактериальные"},
    {"key": "cellulitis", "title": "Целлюлит кожи и подкожной клетчатки", "icd10": "L03.9", "profile": "bacterial_pyoderma", "category": "Бактериальные"},
    {"key": "folliculitis", "title": "Фолликулит", "icd10": "L73.9", "profile": "bacterial_pyoderma", "category": "Бактериальные"},
    {"key": "furuncle", "title": "Фурункул", "icd10": "L02.9", "profile": "bacterial_pyoderma", "category": "Бактериальные"},
    {"key": "carbuncle", "title": "Карбункул", "icd10": "L02.9", "profile": "bacterial_pyoderma", "category": "Бактериальные"},
    {"key": "hidradenitis_suppurativa", "title": "Гнойный гидраденит (acne inversa)", "icd10": "L73.2", "profile": "bacterial_pyoderma", "category": "Бактериальные"},
    {"key": "erythrasma", "title": "Эритразма", "icd10": "L08.1", "profile": "bacterial_pyoderma", "category": "Бактериальные"},
    # Viral
    {"key": "herpes_zoster", "title": "Опоясывающий герпес", "icd10": "B02.9", "profile": "viral_exanthem", "category": "Вирусные"},
    {"key": "varicella", "title": "Ветряная оспа", "icd10": "B01.9", "profile": "viral_exanthem", "category": "Вирусные"},
    {"key": "mpox", "title": "Оспа обезьян (mpox)", "icd10": "B04", "profile": "viral_exanthem", "category": "Вирусные"},
    {"key": "hand_foot_mouth", "title": "Энтеровирусная инфекция кистей, стоп и рта", "icd10": "B08.4", "profile": "viral_exanthem", "category": "Вирусные"},
    {"key": "viral_warts", "title": "Вирусные бородавки", "icd10": "B07", "profile": "viral_exanthem", "category": "Вирусные"},
    {"key": "molluscum_general", "title": "Контагиозный моллюск", "icd10": "B08.1", "profile": "viral_exanthem", "category": "Вирусные"},
    {"key": "measles_exanthem", "title": "Корь с кожной экзантемой", "icd10": "B05.9", "profile": "viral_exanthem", "category": "Вирусные"},
    {"key": "rubella_exanthem", "title": "Краснуха с экзантемой", "icd10": "B06.9", "profile": "viral_exanthem", "category": "Вирусные"},
    # Parasitic
    {"key": "scabies_classic", "title": "Чесотка классическая", "icd10": "B86", "profile": "scabies_like", "category": "Паразитарные"},
    {"key": "scabies_crusted", "title": "Чесотка норвежская", "icd10": "B86", "profile": "scabies_like", "category": "Паразитарные"},
    {"key": "pediculosis_capitis", "title": "Педикулез волосистой части головы", "icd10": "B85.0", "profile": "scabies_like", "category": "Паразитарные"},
    {"key": "pediculosis_corporis", "title": "Педикулез туловища", "icd10": "B85.1", "profile": "scabies_like", "category": "Паразитарные"},
    # Urticaria and drug reactions
    {"key": "acute_urticaria", "title": "Острая крапивница", "icd10": "L50.9", "profile": "urticaria_drug", "category": "Аллергические/лекарственные"},
    {"key": "chronic_urticaria", "title": "Хроническая крапивница", "icd10": "L50.8", "profile": "urticaria_drug", "category": "Аллергические/лекарственные"},
    {"key": "drug_eruption", "title": "Лекарственная токсикодермия", "icd10": "L27.0", "profile": "urticaria_drug", "category": "Аллергические/лекарственные"},
    {"key": "fixed_drug_eruption", "title": "Фиксированная лекарственная эритема", "icd10": "L27.1", "profile": "urticaria_drug", "category": "Аллергические/лекарственные"},
    {"key": "sjs_ten", "title": "Синдром Стивенса-Джонсона/ТЭН", "icd10": "L51.1", "profile": "urticaria_drug", "category": "Аллергические/лекарственные"},
    {"key": "dress", "title": "DRESS-синдром", "icd10": "L27.0", "profile": "urticaria_drug", "category": "Аллергические/лекарственные"},
    # Bullous and autoimmune
    {"key": "bullous_pemphigoid", "title": "Буллезный пемфигоид", "icd10": "L12.0", "profile": "bullous_autoimmune", "category": "Буллезные/аутоиммунные"},
    {"key": "pemphigus_vulgaris", "title": "Пузырчатка вульгарная", "icd10": "L10.0", "profile": "bullous_autoimmune", "category": "Буллезные/аутоиммунные"},
    {"key": "dermatitis_herpetiformis", "title": "Дерматит герпетиформный Дюринга", "icd10": "L13.0", "profile": "bullous_autoimmune", "category": "Буллезные/аутоиммунные"},
    # Acne/rosacea/perioral
    {"key": "acne_vulgaris", "title": "Акне вульгарное", "icd10": "L70.0", "profile": "acneiform", "category": "Акнеформные"},
    {"key": "acne_conglobata", "title": "Конглобатные акне", "icd10": "L70.1", "profile": "acneiform", "category": "Акнеформные"},
    {"key": "rosacea", "title": "Розацеа", "icd10": "L71.9", "profile": "acneiform", "category": "Акнеформные"},
    {"key": "perioral_dermatitis", "title": "Периоральный дерматит", "icd10": "L71.0", "profile": "acneiform", "category": "Акнеформные"},
    {"key": "pseudofolliculitis", "title": "Псевдофолликулит", "icd10": "L73.1", "profile": "acneiform", "category": "Акнеформные"},
    # Pigmentary
    {"key": "vitiligo", "title": "Витилиго", "icd10": "L80", "profile": "pigmentary", "category": "Пигментные"},
    {"key": "melasma", "title": "Мелазма", "icd10": "L81.1", "profile": "pigmentary", "category": "Пигментные"},
    {"key": "postinflammatory_hyperpigmentation", "title": "Поствоспалительная гиперпигментация", "icd10": "L81.0", "profile": "pigmentary", "category": "Пигментные"},
    {"key": "lentigo", "title": "Лентиго", "icd10": "L81.4", "profile": "pigmentary", "category": "Пигментные"},
    # Hair and nail
    {"key": "alopecia_areata", "title": "Очаговая алопеция", "icd10": "L63.9", "profile": "hair_nail", "category": "Волосы/ногти"},
    {"key": "androgenetic_alopecia", "title": "Андрогенетическая алопеция", "icd10": "L64.9", "profile": "hair_nail", "category": "Волосы/ногти"},
    {"key": "telogen_effluvium", "title": "Телогеновое выпадение волос", "icd10": "L65.0", "profile": "hair_nail", "category": "Волосы/ногти"},
    {"key": "paronychia", "title": "Паронихия", "icd10": "L03.0", "profile": "hair_nail", "category": "Волосы/ногти"},
    {"key": "trachyonychia", "title": "Трахионихия", "icd10": "L60.3", "profile": "hair_nail", "category": "Волосы/ногти"},
    # Neoplasms and precancers
    {"key": "actinic_keratosis", "title": "Актинический кератоз", "icd10": "L57.0", "profile": "neoplasm_alert", "category": "Новообразования"},
    {"key": "basal_cell_carcinoma", "title": "Базальноклеточный рак кожи", "icd10": "C44.9", "profile": "neoplasm_alert", "category": "Новообразования"},
    {"key": "squamous_cell_carcinoma", "title": "Плоскоклеточный рак кожи", "icd10": "C44.9", "profile": "neoplasm_alert", "category": "Новообразования"},
    {"key": "cutaneous_melanoma", "title": "Меланома кожи", "icd10": "C43.9", "profile": "neoplasm_alert", "category": "Новообразования"},
    {"key": "keratoacanthoma", "title": "Кератоакантома", "icd10": "L85.8", "profile": "neoplasm_alert", "category": "Новообразования"},
    {"key": "seborrheic_keratosis", "title": "Себорейный кератоз", "icd10": "L82.1", "profile": "neoplasm_alert", "category": "Новообразования"},
    {"key": "dermatofibroma", "title": "Дерматофиброма", "icd10": "D23.9", "profile": "neoplasm_alert", "category": "Новообразования"},
    {"key": "cherry_angioma", "title": "Вишневая ангиома", "icd10": "D18.0", "profile": "neoplasm_alert", "category": "Новообразования"},
    # Connective tissue / vasculopathy spectrum
    {"key": "discoid_lupus", "title": "Дискоидная красная волчанка", "icd10": "L93.0", "profile": "psoriasiform", "category": "Аутоиммунные"},
    {"key": "cutaneous_lupus_other", "title": "Кожная красная волчанка (другие формы)", "icd10": "L93.2", "profile": "psoriasiform", "category": "Аутоиммунные"},
    {"key": "dermatomyositis_skin", "title": "Кожные проявления дерматомиозита", "icd10": "M33.1", "profile": "psoriasiform", "category": "Аутоиммунные"},
    {"key": "morphea", "title": "Локализованная склеродермия (морфея)", "icd10": "L94.0", "profile": "psoriasiform", "category": "Аутоиммунные"},
    {"key": "vasculitis_cutaneous", "title": "Кожный васкулит", "icd10": "L95.9", "profile": "bacterial_pyoderma", "category": "Сосудистые/прочие"},
    {"key": "venous_ulcer", "title": "Венозная язва голени", "icd10": "I83.0", "profile": "bacterial_pyoderma", "category": "Сосудистые/прочие"},
    {"key": "arterial_ulcer", "title": "Артериальная язва кожи", "icd10": "L98.4", "profile": "bacterial_pyoderma", "category": "Сосудистые/прочие"},
]


CONDITION_TAG_ADJUSTMENTS: Dict[str, Dict[str, int]] = {
    # Better STI disambiguation
    "genital_herpes": {
        "lesion_vesicles": 5,
        "pain_yes": 2,
        "ulcer_painful_yes": 2,
        "ulcer_painless_yes": -3,
        "grouped_vesicles_yes": 6,
        "painless_chancre_yes": -5,
        "inguinal_nodes_yes": 1,
    },
    "syphilis_primary": {
        "lesion_ulcer": 5,
        "ulcer_painless_yes": 5,
        "pain_yes": -3,
        "ulcer_painful_yes": -2,
        "painless_chancre_yes": 6,
        "grouped_vesicles_yes": -5,
        "inguinal_nodes_yes": 3,
        "palms_soles_rash_yes": 2,
    },
    "syphilis_secondary": {
        "loc_palms_soles": 5,
        "fever_yes": 2,
        "lesion_ulcer": -2,
        "ulcer_painless_yes": -1,
        "palms_soles_rash_yes": 5,
        "inguinal_nodes_yes": 2,
    },
    "chancroid": {
        "lesion_ulcer": 4,
        "ulcer_painful_yes": 4,
        "pain_yes": 3,
        "ulcer_painless_yes": -3,
        "painless_chancre_yes": -4,
        "grouped_vesicles_yes": -2,
        "inguinal_nodes_yes": 4,
    },
    "anogenital_warts": {"lesion_nodule_or_tumor": 4, "pain_yes": -2, "lesion_ulcer": -2},
    "gonococcal_urethritis": {"discharge_dysuria_yes": 3, "pain_yes": 1, "inguinal_nodes_yes": 1},
    "chlamydial_infection": {"discharge_dysuria_yes": 2, "pain_yes": 0, "inguinal_nodes_yes": 1},
    "trichomoniasis": {"discharge_dysuria_yes": 2, "itch_moderate": 1},
    # Common look-alikes
    "scabies_classic": {"itch_night": 3, "contact_case_yes": 3, "lesion_papules_burrows": 3},
    "scabies_crusted": {"itch_night": 2, "lesion_pustules_crusts": 2, "chronic_recurrent_yes": 2},
    "tinea_pedis": {
        "loc_feet": 4,
        "lesion_annular_scale": 2,
        "active_scaly_border_yes": 4,
        "prior_antifungal_helped_yes": 3,
    },
    "tinea_capitis": {
        "loc_scalp": 4,
        "loc_hair_scalp_nails": 2,
        "active_scaly_border_yes": 3,
        "prior_antifungal_helped_yes": 3,
    },
    "onychomycosis": {"loc_hair_scalp_nails": 4, "chronic_recurrent_yes": 2},
    "candidal_intertrigo": {
        "loc_folds": 4,
        "lesion_moist_erythema": 3,
        "candidal_satellite_yes": 5,
        "prior_antifungal_helped_yes": 4,
    },
    "vulvovaginal_candidiasis": {
        "loc_genital": 4,
        "discharge_dysuria_yes": 2,
        "itch_moderate": 1,
        "candidal_satellite_yes": 4,
        "prior_antifungal_helped_yes": 4,
    },
    "plaque_psoriasis": {
        "lesion_sharply_demarcated_plaques": 3,
        "chronic_recurrent_yes": 2,
        "silvery_scale_yes": 4,
        "symmetric_distribution_yes": 3,
        "family_atopy_yes": -1,
    },
    "inverse_psoriasis": {"loc_folds": 3, "lesion_sharply_demarcated_plaques": 2},
    "palmoplantar_psoriasis": {"loc_palms_soles": 4},
    "pustular_psoriasis": {"lesion_pustules_crusts": 3, "fever_yes": 1},
    "allergic_contact_dermatitis": {
        "trigger_new_product_yes": 3,
        "lesion_eczema": 2,
        "silvery_scale_yes": -2,
        "symmetric_distribution_yes": -1,
    },
    "irritant_contact_dermatitis": {
        "trigger_new_product_yes": 2,
        "lesion_eczema": 2,
        "silvery_scale_yes": -2,
        "symmetric_distribution_yes": -1,
    },
    "atopic_dermatitis": {
        "chronic_recurrent_yes": 2,
        "itch_night": 1,
        "family_atopy_yes": 4,
        "symmetric_distribution_yes": 2,
    },
    "acute_urticaria": {"lesion_wheals": 4, "wheals_transient_yes": 4, "chronic_recurrent_yes": -1},
    "chronic_urticaria": {"lesion_wheals": 4, "wheals_transient_yes": 3, "chronic_recurrent_yes": 2},
    "drug_eruption": {"trigger_new_product_yes": 3, "fever_yes": 2},
    "sjs_ten": {"lesion_mucosal_involvement": 6, "fever_yes": 4, "trigger_new_product_yes": 3},
    "dress": {"fever_yes": 5, "trigger_new_product_yes": 3, "lesion_mucosal_involvement": 2},
    "pemphigus_vulgaris": {"lesion_bullae": 4, "lesion_mucosal_involvement": 4},
    "bullous_pemphigoid": {"lesion_bullae": 4, "itch_moderate": 2, "lesion_mucosal_involvement": -1},
    "acne_vulgaris": {"lesion_papules_pustules": 3, "comedones_yes": 4, "loc_face": 2},
    "acne_conglobata": {"lesion_papules_pustules": 4, "pain_yes": 2, "chronic_recurrent_yes": 2},
    "rosacea": {"loc_face": 4, "comedones_yes": -3, "itch_none": 1, "symmetric_distribution_yes": 1},
    "vitiligo": {"lesion_pigment_change": 3, "itch_none": 2},
    "melasma": {"lesion_pigment_change": 3, "loc_face": 2},
    "cutaneous_melanoma": {
        "lesion_nodule_or_tumor": 4,
        "chronic_recurrent_yes": 2,
        "pain_yes": -1,
        "symmetric_distribution_yes": -2,
    },
    "basal_cell_carcinoma": {"lesion_nodule_or_tumor": 3, "lesion_ulcer": 2, "symmetric_distribution_yes": -2},
    "herpes_zoster": {"dermatomal_pain_yes": 6, "lesion_vesicles": 2, "loc_trunk_limbs": 2},
}


def build_knowledge_base() -> Dict[str, dict]:
    kb: Dict[str, dict] = {}
    for row in RAW_CONDITIONS:
        profile = PROFILES[row["profile"]]
        merged_weights = dict(profile.tag_weights)
        specific_weights = CONDITION_TAG_ADJUSTMENTS.get(row["key"], {})
        for tag, delta in specific_weights.items():
            merged_weights[tag] = merged_weights.get(tag, 0) + delta
        kb[row["key"]] = {
            "key": row["key"],
            "title": row["title"],
            "icd10": row["icd10"],
            "category": row["category"],
            "summary": profile.summary,
            "tests": profile.tests,
            "recommendations": profile.recommendations,
            "tag_weights": merged_weights,
        }
    return kb


KNOWLEDGE_BASE: Dict[str, dict] = build_knowledge_base()
