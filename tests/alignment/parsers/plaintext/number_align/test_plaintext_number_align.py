import json
from pathlib import Path

from openpecha.alignment.parsers.plaintext.number_align import (
    PlainTextNumberAlignedParser,
)

expected_source_segments = [
    "1. v1大方廣佛華嚴經·v2入不思議解脫境界普賢行願品",
    "2. 梵文名為：阿雅 拔雜 札雅 巴倪 達拿 喇雜",
    "3. 藏文名為：帕巴 嗓缽 倔巴 夢浪 給 嘉缽",
    "4. 禮敬聖文殊童子",
    "5. 所有十方世界中，三世一切人師子，我以清淨身語意，一切遍禮盡無餘。",
    "6. 普賢行願威神力，普現一切如來前，一身復現刹塵身，一一遍禮刹塵佛。",
    "7. 於一塵中塵數佛，各處菩薩眾會中，無盡法界塵亦然，深信諸佛皆充滿。",
    "8. 各以一切音聲海，普出無盡妙言辭，盡於未來一切劫，讚佛甚深功德海。",
    "9. 以諸最勝妙華鬘，伎樂塗香及傘蓋，如是最勝莊嚴具，我以供養諸如來。",
    "10. 最勝衣服最勝香，末香燒香與燈燭，一一皆如妙高聚，我悉供養諸如來。",
]
expected_target_segments = [
    "<sapche>乙二 正頌\n丙一 頌正示行願\n丁一 正頌行願\n戊一 頌第一願</sapche>",
    "4. 行願之名雖有十義，意祇有七，以後三合故。初二句頌所禮，次一句頌能禮，第四句明周遍，第五句辯遍因。謂所以能如是周遍者，全仗普賢行願威神之力故也。後三句別顯禮相。謂一一佛所，各有多身；一一己身，能起多禮。",
    "1-3. 經云：一一如來所，一切剎塵禮。即此意也。",
    "<sapche>乙二 正頌\n丙一 頌正示行願\n丁一 正頌行願\n戊一 頌第一願</sapche>",
    "1-3,5. 行願之名雖有十義，意祇有七，以後三合故。初二句頌所禮，次一句頌能禮，第四句明周遍，第五句辯遍因。謂所以能如是周遍者，全仗普賢行願威神之力故也。後三句別顯禮相。謂一一佛所，各有多身；一一己身，能起多禮。",
    "6. 經云：一一如來所，一切剎塵禮。即此意也。",
]


expected_mapping_ann_indicies = {
    "root_indicies": [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
    ],
    "root_sapche_indicies": [],
    "comment_indicies": [
        (2, [1, 2, 3]),
        (4, [1, 2, 3, 5]),
        (1, [4]),
        (5, [6]),
    ],
    "comment_sapche_indicies": [
        (0, 8, 38),
        (3, 8, 38),
    ],
}


def test_parse_to_segments():
    DATA = Path(__file__).parent / "data"

    root_file = DATA / "003-ch.txt"
    align_file = DATA / "004-ch-1-諦閑.txt"
    metadata_file = DATA / "metadata.json"

    parser = PlainTextNumberAlignedParser.from_files(
        root_file, align_file, metadata_file
    )

    assert not hasattr(parser, "source_segments")
    assert not hasattr(parser, "target_segments")

    assert not hasattr(parser, "mapping_ann_indices")

    parser.parse_text_into_segments()

    assert hasattr(parser, "source_segments")
    assert hasattr(parser, "target_segments")

    assert parser.source_segments == expected_source_segments
    assert parser.target_segments == expected_target_segments

    assert hasattr(parser, "mapping_ann_indicies")
    assert (
        parser.mapping_ann_indicies["root_indicies"]
        == expected_mapping_ann_indicies["root_indicies"]
    )
    assert (
        parser.mapping_ann_indicies["root_sapche_indicies"]
        == expected_mapping_ann_indicies["root_sapche_indicies"]
    )
    assert (
        parser.mapping_ann_indicies["comment_indicies"]
        == expected_mapping_ann_indicies["comment_indicies"]
    )
    assert (
        parser.mapping_ann_indicies["comment_sapche_indicies"]
        == expected_mapping_ann_indicies["comment_sapche_indicies"]
    )


def test_parse_pecha():
    DATA = Path(__file__).parent / "data"
    metadata_file = DATA / "metadata.json"

    source_text = (DATA / "003-ch.txt").read_text(encoding="utf-8")
    target_text = (DATA / "004-ch-1-諦閑.txt").read_text(encoding="utf-8")
    with open(metadata_file) as f:
        metadata = json.load(f)

    parser = PlainTextNumberAlignedParser(source_text, target_text, metadata)
    parser.source_segments = expected_source_segments
    parser.target_segments = expected_target_segments
    parser.mapping_ann_indicies = expected_mapping_ann_indicies

    parser.parse(DATA)


test_parse_pecha()
