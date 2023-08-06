# -*- coding: utf-8 -*-
# pylint: disable=C0303
"""
This module contains a HTMLExportWord Model
"""
from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from itertools import groupby
from typing import Union, Optional, List

from loglan_db import db
from loglan_db.model_db.addons.addon_word_getter import AddonWordGetter
from loglan_db.model_db.base_event import BaseEvent
from loglan_db.model_db.base_word import BaseWord
from loglan_db.model_export import AddonExportWordConverter
from loglan_db.model_html import DEFAULT_HTML_STYLE


@dataclass
class Meaning:
    """Meaning Class"""
    mid: int
    technical: str
    definitions: List[str]
    used_in: str


class AddonWordTranslator:
    """
    Additional methods for HTMLExportWord class
    """

    def definitions_by_key(
            self, key: str, style: str = DEFAULT_HTML_STYLE,
            case_sensitive: bool = False) -> str:

        """
        Args:
            key:
            style:
            case_sensitive:
        Returns:

        """

        return '\n'.join([
            d.export_for_english(key, style) for d in self.definitions
            if self.conditions(key, d.keys, case_sensitive)])

    @staticmethod
    def conditions(x_key: str, x_keys: list, x_case_sensitive: bool) -> bool:
        current_keys = [k.word if x_case_sensitive else k.word.lower() for k in x_keys]
        return any(map(lambda x: fnmatch.fnmatchcase(x, x_key), current_keys))

    @staticmethod
    def translation_by_key(
            key: str, language: str = None, style: str = DEFAULT_HTML_STYLE,
            event_id: Union[BaseEvent, int, str] = None, case_sensitive: bool = False) -> Optional[str]:
        """
        Get information about loglan words by key in a foreign language
        Args:
            key:
            language:
            style:
            event_id:
            case_sensitive:
        Returns:

        """

        words = HTMLExportWord.by_key(
            key=key, language=language, event_id=event_id,
            case_sensitive=case_sensitive).all()

        if not words:
            return None

        current_key = key if case_sensitive else key.lower()
        blocks = [word.definitions_by_key(
            key=current_key, style=style, case_sensitive=case_sensitive) for word in words]

        return '\n'.join(blocks).strip()


class HTMLExportWord(BaseWord, AddonWordGetter, AddonWordTranslator, AddonExportWordConverter):
    """
    HTMLExportWord Class
    """

    _definitions = db.relationship(
        "HTMLExportDefinition", lazy='dynamic', back_populates="_source_word", viewonly=True)

    @classmethod
    def html_all_by_name(
            cls, name: str, style: str = DEFAULT_HTML_STYLE,
            event_id: Union[BaseEvent, int, str] = None,
            case_sensitive: bool = False) -> Optional[str]:
        """
        Convert all words found by name into one HTML string
        Args:
            name: Name of the search word
            style: HTML design style
            event_id:
            case_sensitive:
        Returns:

        """

        words_template = {
            "normal": '<div class="words">\n%s\n</div>\n',
            "ultra": '<ws>\n%s\n</ws>\n',
        }

        if not event_id:
            event_id = BaseEvent.latest().id

        event_id = int(event_id) if isinstance(event_id, (int, str)) else BaseEvent.id

        words = cls.by_name(
            name=name, event_id=event_id,
            case_sensitive=case_sensitive
        ).all()

        if not words:
            return None

        items = cls._get_stylized_words(words, style)

        return words_template[style] % "\n".join(items)

    @staticmethod
    def _get_stylized_words(
            words: list, style: str = DEFAULT_HTML_STYLE) -> List[str]:
        """

        Args:
            words:
            style:

        Returns:

        """
        word_template = {
            "normal": '<div class="word" wid="%s">\n'
                      '<div class="word_line"><span class="word_name">%s</span>,</div>\n'
                      '<div class="meanings">\n%s\n</div>\n</div>',
            "ultra": '<w wid="%s"><wl>%s,</wl>\n<ms>\n%s\n</ms>\n</w>',
        }
        grouped_words = groupby(words, lambda ent: ent.name)
        group_words = {k: list(g) for k, g in grouped_words}
        items = []
        for word_name, words_list in group_words.items():
            meanings = "\n".join([word.html_meaning(style) for word in words_list])
            items.append(word_template[style] % (word_name.lower(), word_name, meanings))
        return items

    def html_origin(self, style: str = DEFAULT_HTML_STYLE):
        """

        Args:
            style:

        Returns:

        """
        orig = self.origin
        orig_x = self.origin_x

        if not (orig or orig_x):
            return str()

        origin = self._generate_origin(orig, orig_x)

        if style == "normal":
            return f'<span class="m_origin">&lt;{origin}&gt;</span> '
        return f'<o>&lt;{origin}&gt;</o> '

    @staticmethod
    def _generate_origin(orig: str, orig_x: str) -> str:
        """
        Generate basic 'origin' string
        Args:
            orig:
            orig_x:

        Returns:

        """
        if not orig_x:
            return orig

        if not orig:
            return orig_x

        return f'{orig}={orig_x}'

    def html_definitions(self, style: str = DEFAULT_HTML_STYLE):
        """
        :param style:
        :return:
        """
        return [d.export_for_loglan(style=style) for d in self.definitions]

    def meaning(self, style: str = DEFAULT_HTML_STYLE) -> Meaning:
        """
        :param style:
        :return:
        """
        html_affixes, html_match, html_rank,\
            html_source, html_type, html_used_in,\
            html_year, t_technical = self.get_styled_values(style)

        html_tech = t_technical % f'{html_match}{html_type}{html_source}{html_year}{html_rank}'
        html_tech = f'{html_affixes}{self.html_origin(style)}{html_tech}'
        return Meaning(self.id, html_tech, self.html_definitions(style), html_used_in)

    @staticmethod
    def _tagger(tag: str, value: Optional[str], default_value: Optional[str] = str()):
        return tag % value if value else default_value

    def used_in_as_html(self, style: str = DEFAULT_HTML_STYLE) -> str:
        tags = {
            "normal": '<a class="m_cpx">%s</a>',
            "ultra": '<cpx>%s</cpx>',
        }
        return " |&nbsp;".join(sorted(
            {tags[style] % cpx.name for cpx in filter(None, self.complexes)}
        ))

    def get_styled_values(self, style: str = DEFAULT_HTML_STYLE) -> tuple:
        """

        Args:
            style:

        Returns:

        """
        tags = {
            "normal": [
                '<span class="m_afx">%s</span> ', '<span class="m_match">%s</span> ',
                '<span class="m_rank">%s</span>', '<span class="m_author">%s</span> ',
                '<span class="m_type">%s</span> ', '<span class="m_use">%s</span>',
                '<span class="m_year">%s</span> ', '<span class="m_technical">%s</span>'],
            "ultra": [
                '<afx>%s</afx> ', '%s ', '%s', '%s ', '%s ',
                '<use>%s</use>', '%s ', '<tec>%s</tec>'],
        }

        values = [self.e_affixes, self.match, self.rank, self.e_source, self.type.type,
                  self.used_in_as_html(style), self.e_year, None]
        default_values = [str(), str(), str(), str(), str(), None, str(), tags[style][-1]]

        return tuple(self._tagger(tag, value, default_value) for tag, value, default_value
                     in zip(tags[style], values, default_values))

    def html_meaning(self, style: str = DEFAULT_HTML_STYLE) -> str:
        """

        Args:
            style:

        Returns:

        """
        n_l = "\n"
        meaning = self.meaning(style)
        if style == "normal":
            used_in_list = f'<div class="used_in">Used In: ' \
                           f'{meaning.used_in}</div>\n</div>' \
                if meaning.used_in else "</div>"
            return f'<div class="meaning" id="{meaning.mid}">\n' \
                   f'<div class="technical">{meaning.technical}</div>\n' \
                   f'<div class="definitions">{n_l}' \
                   f'{n_l.join(meaning.definitions)}\n</div>\n{used_in_list}'

        used_in_list = f'<us>Used In: {meaning.used_in}</us>\n</m>' \
            if meaning.used_in else '</m>'
        return f'<m>\n<t>{meaning.technical}</t>\n' \
               f'<ds>{n_l}' \
               f'{n_l.join(meaning.definitions)}\n</ds>\n{used_in_list}'
